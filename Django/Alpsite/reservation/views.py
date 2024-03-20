from datetime import date, time, datetime, timedelta
import calendar
from typing import Any, Dict
from django.utils.safestring import mark_safe
from django.urls import reverse, re_path
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import  ListView, TemplateView, FormView
from django.contrib import messages
from django.db.models import Q
from .forms import ReservationForm
from alpsite.decorator import you_shall_not_pass, staff_required
from .models import Reservation
from alp.models import InformationDetail, Contact
from application.models import Userinfo
from .utils import Calendar
from django.core.mail import send_mail
from django.template.loader import render_to_string


@method_decorator(you_shall_not_pass(), name='dispatch')
class ReservationPage(FormView):
    form_class = ReservationForm
    template_name = "reservation/reservation.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        str_query_date = self.request.GET.get('selectedDate', None)
        if str_query_date:
            try:
                query_date = datetime.strptime(str_query_date, '%Y-%m-%d').date()
            except ValueError:
                query_date = None
        else:
            query_date = datetime.today()
        
        ### Dates to navigate ###
        first = query_date.replace(day=1)
        prev_month = first - timedelta(days=1)

        days_in_month = calendar.monthrange(query_date.year, query_date.month)[1]
        last = query_date.replace(day=days_in_month)
        next_month = last + timedelta(days=1)        

        context['this_month'] = datetime.today().strftime('%Y-%m-%d')
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        
        # Creates a calendar 
        cal = Calendar(query_date.year, query_date.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        return context

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form: Any) -> HttpResponse:
       
        data = form.cleaned_data
        
        user = self.request.user
        creation_datetime = timezone.make_aware(datetime.now())
        from_date = data['from_date'] 
        to_date = data['to_date'] 
        approved = False

        new_reservation_data = {
                    'creation_datetime' : creation_datetime,
                    'from_date' : from_date,
                    'to_date' : to_date,
                    'user' : user,
                    'approved' : approved,
                }
            
        if from_date > to_date or vacancy_check(new_reservation_data):
            messages.add_message(self.request, messages.WARNING, 'Reservierung nicht möglich') 
        else:
            new_reservation = Reservation(**new_reservation_data)
            new_reservation.save()
            messages.add_message(self.request, messages.SUCCESS, 'Reservierung erfolgt')
            self.send_approval_reminder(new_reservation)
        
        return super().form_valid(form)

    def get_success_url(self):
        selected_date = self.request.GET.get('selectedDate')
        success_url = f'/reservation/'
        if selected_date:
            success_url += f'?selectedDate={selected_date}'
        return success_url

    ### Send Mail for Approval ###
        
    def send_approval_reminder(self, reservation):
        if self.request:
            try:
                referer = self.request.META['HTTP_REFERER']
                parts = referer.split(reverse('reservation:reservation'), 1)
                base_url = parts[0]
            except AttributeError: 
                return 
            
        email_subject = 'Neue Reservationsanfrage vorhanden'
        alp_link = base_url
        message = "Reservationsanfrage auf der Alp"
        recipients_query = Contact.objects.filter(gives_permission=True)
        recipient_list = [contact.email for contact in recipients_query]
        html_content = render_to_string('emails/reservationApplication.html', 
                                        {
                                        'reservation': reservation,
                                        'huette_link': alp_link
                                        })
        from_email = 'diealphuette@gmx.ch'
        
        send_mail(email_subject, message, from_email, recipient_list, html_message=html_content)


### Validation Checks ####

def vacancy_check (reservation_data):   
    start = reservation_data['from_date']
    end = reservation_data['to_date']

    reservations = Reservation.objects.filter(from_date__year = reservation_data['from_date'].year,
                                                from_date__month = reservation_data['from_date'].month)

    starts_whitin = Q(from_date__gte=start, from_date__lte=end)
    ends_whitin = Q(to_date__gte=start, to_date__lte=end)
    swallows = Q(from_date__gte=start, to_date__lte=end)
    encapsulate = Q(from_date__lte=start, to_date__gte=end)

    reservation_check = reservations.filter(starts_whitin | ends_whitin | encapsulate | swallows)

    return bool(reservation_check)


@method_decorator(staff_required(), name='dispatch')
class MaintenancePage(TemplateView):
    http_method_names = ["get", "post"]
    template_name = "reservation/maintenance.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        ### Reservation Maintenance ###

        delete_request = self.request.GET.get('delete', None)
        approve_request = self.request.GET.get('approve', None)

        if delete_request:

            to_delete = Reservation.objects.get(id=delete_request)
            msg = "abgelehnt"
            self.send_reservation_confirmation(to_delete, msg)
            to_delete.delete()
        if approve_request:
            to_appove = Reservation.objects.get(id=approve_request)
            to_appove.approved = True
            to_appove.save()
            msg = "bestätigt"
            self.send_reservation_confirmation(to_appove, msg)

        ### QR-Code Generator ###
        info_id = self.request.GET.get('qr', None)
        if info_id:
            context["info_detail"] = InformationDetail.objects.get(id=info_id)
            ### Get abolute path to info_detail view ###
            info_detail_url = reverse_lazy('alp:info_detail', args=[int(info_id)])
            context["info_detail_url"] = self.request.build_absolute_uri(info_detail_url)
        
        context['reservation_requests'] = Reservation.objects.filter(approved=False)
        context['information_details'] = InformationDetail.objects.all()
        context['user_applications'] = Userinfo.objects.filter(user__is_active=False)

        return context
    
    ### Send Mail as info @user ###

    def send_reservation_confirmation(self, reservation, msg):
        if self.request:
            try:
                referer = self.request.META['HTTP_REFERER']
                parts = referer.split(reverse('reservation:maintenance'), 1)
                base_url = parts[0]
            except AttributeError: 
                return 
            
        email_subject = 'Reservationsanfrage ' + msg
        alp_link = base_url
        message = "Reservationsanfrage auf der Alp-Hütte ist " + msg
        recipient_list = [reservation.user.email]
        html_content = render_to_string('emails/reservationConfirmation.html', 
                                        {
                                        'msg': msg,
                                        'reservation': reservation,
                                        'huette_link': alp_link
                                        })
        from_email = 'diealphuette@gmx.ch'
        
        send_mail(email_subject, message, from_email, recipient_list, html_message=html_content)

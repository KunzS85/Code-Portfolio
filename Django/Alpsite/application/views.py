from typing import Any
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy
from .forms import ApplicationForm
from alpsite.decorator import staff_required
from django.utils.decorators import method_decorator
from .models import Userinfo
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from alp.models import Contact


class ApplicationFormView(FormView):
    template_name = 'application/applicationform.html'
    form_class = ApplicationForm
    success_url = reverse_lazy('alp:home')

    def form_valid(self, form):
        user = form.save()
        self.send_login_application(user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    def send_login_application(self, user):
        if self.request:
            try:
                referer = self.request.META['HTTP_REFERER']
                parts = referer.split(reverse('application:applicationForm'), 1)
                base_url = parts[0]
            except AttributeError: 
                return 
            
        email_subject = 'Neue Loginanfrage vorhanden'
        alp_link = base_url
        message = "Loginanfrage auf der Alp"
        recipients_query = Contact.objects.filter(gives_permission=True)
        recipient_list = [contact.email for contact in recipients_query]
        html_content = render_to_string('emails/loginApplication.html', 
                                        {
                                        'user': user,
                                        'huette_link': alp_link
                                        })
        from_email = 'diealphuette@gmx.ch'
        
        send_mail(email_subject, message, from_email, recipient_list, html_message=html_content)

    

@method_decorator(staff_required(), name='dispatch')
class ApplicationAcceptanceView(TemplateView):
    http_method_names = ["get"]
    template_name = 'application/applicationacceptance.html'


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        userinfo = Userinfo.objects.get(user__id=self.kwargs.get('id'))
        
        context['userinfo'] = userinfo

        return context


class UserDecisionView(DetailView):
    model = Userinfo
    template_name = 'application/user_detail.html'
    context_object_name = 'userinfo'        

    def post(self, request, *args, **kwargs):
        delete_request = request.POST.get('delete', None)
        approve_request = request.POST.get('approve', None)

        if delete_request:
            user = User.objects.get(id=delete_request)            
            msg = "abgelehnt."
            msg_add_on = ""
            self.send_user_application_confirmation(user, msg, msg_add_on)
            user.delete()
            return redirect('reservation:maintenance')

        if approve_request:
            user = User.objects.get(id=approve_request)
            user.is_active = True
            user.save()
            msg = "bestätigt"
            msg_add_on = "Willkommen auf der Website."
            self.send_user_application_confirmation(user, msg, msg_add_on)
            return redirect('reservation:maintenance')

        return super().post(request, *args, **kwargs)
    
    ### Send Mail as info @NewUser ###
    
    def send_user_application_confirmation(self, user, msg, msg_add_on):
        if self.request:
            try:
                referer = self.request.META['HTTP_REFERER']
                parts = referer.split(reverse('application:userinfo', kwargs={'id':user.id}), 1)
                base_url = parts[0]
            except AttributeError: 
                return 
            
        email_subject = 'Deine Loginanfrage ist ' + msg
        alp_link = base_url
        message = "Deine Loginanfrage auf der Alp-Hütte ist " + msg
        recipient_list = [user.email]
        html_content = render_to_string('emails/loginConfirmation.html', 
                                        {
                                        'msg': msg,
                                        'msg_add_on' : msg_add_on,
                                        'huette_link': alp_link
                                        })
        from_email = 'diealphuette@gmx.ch'
        
        send_mail(email_subject, message, from_email, recipient_list, html_message=html_content)

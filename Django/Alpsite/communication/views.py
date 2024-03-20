from typing import Any, Dict
import json
from django.http import HttpResponse, HttpRequest
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.generic import  FormView
from .forms import PwResetApplicationForm, PwResetForm


class PwResetPage(FormView):
    form_class = PwResetApplicationForm
    template_name = "communication/pwresetapplication.html"
    success_url = "/login/"

    def form_valid(self, form):

        data = form.cleaned_data
        userquery = User.objects.filter(username=data['username'], email=data['user_email'])
        
        if not userquery:
            messages.add_message(self.request, messages.WARNING, 'Die Angaben sind falsch')
        if userquery:
            user = userquery[0]
            self.send_password_reset_mail(user)
            
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
 
    def send_password_reset_mail(self, user):
        if self.request:
            try:
                referer = self.request.META['HTTP_REFERER']
                parts = referer.split(reverse('communication:pwreset'), 1)
                base_url = parts[0]
            except AttributeError: 
                return 

        email_subject = 'Zugangsdaten erneuern'
        alp_link = base_url
        reset_link = base_url + reverse('communication:pwresetform', kwargs={'id': user.id})
        message = reset_link
        html_content = render_to_string('emails/pwreset.html', 
                                        {'title': email_subject,
                                        'name': user.username,
                                        'huette_link': alp_link,
                                        'reset_link': reset_link})
        from_email = 'diealphuette@gmx.ch'
        recipient_list = [user.email]
        
        send_mail(email_subject, message, from_email, recipient_list, html_message=html_content)
        

class PwResetFormPage(FormView):
    form_class = PwResetForm
    template_name = "communication/pwresetform.html"
    success_url = "/login/"
    
    def form_valid(self, form):

        data = form.cleaned_data
        user_id = self.kwargs['id']
        user = User.objects.get(id=user_id)
        user_query = User.objects.filter(username=data['username'], email=data['user_email'])
        
        if not user_query or not user:
            messages.add_message(self.request, messages.WARNING, 'Die Angaben sind falsch')
        else:
            if data['password_one'] != data['password_two']:
                messages.add_message(self.request, messages.WARNING, 'Passwörter stimmen nicht überein')
            else:
                if user_query.exists() and user_query.count() == 1:
                    retrieved_user = user_query.first()
                    if retrieved_user == user:
                        user.set_password(data['password_one'])
                        user.save()
                    else:
                       messages.add_message(self.request, messages.WARNING, 'Der Fehler sitzt wahrscheinlich vor dem Bildschirm') 

        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
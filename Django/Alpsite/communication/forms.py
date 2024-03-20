from django import forms
from django.contrib.auth.models import User

class PwResetApplicationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=10)
    user_email = forms.EmailField(label='E-Mail')


class PwResetForm(forms.Form):
    username = forms.CharField(label='Username', max_length=10)
    user_email = forms.EmailField(label='E-Mail')
    password_one = forms.CharField(label='Neues Passwort', widget=forms.PasswordInput)
    password_two = forms.CharField(label='Passwort bestätigen', widget=forms.PasswordInput)

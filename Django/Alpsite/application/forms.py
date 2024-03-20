from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Userinfo

class ApplicationForm(forms.Form):
    fname = forms.CharField(label='Vorname', max_length=250)
    lname = forms.CharField(label='Nachname', max_length=250)
    mobil = forms.CharField(label='Mobilnummer', max_length=14)
    email = forms.EmailField(label='E-Mail')
    street = forms.CharField(label='Strasse', max_length=50)
    street_nr = forms.IntegerField(label='Hausnummer')
    zip_code = forms.IntegerField(label='Postleitzahl')
    location = forms.CharField(label='Ort', max_length=50)
    self_description = forms.CharField(label='Wer bin ich?', widget=forms.Textarea)
    uname = forms.CharField(label='Username (max. 10 Zeichen)', max_length=10)
    pword = forms.CharField(label='Passwort', widget=forms.PasswordInput)

    def clean_pword(self):
        passwort = self.cleaned_data.get('pword')
        try:
            validate_password(passwort)
        except forms.ValidationError as error:
            raise forms.ValidationError(error)
        return passwort

    def clean(self):
        cleaned_data = super().clean()
        uname = cleaned_data.get('uname')
        email = cleaned_data.get('email')
        mobil = cleaned_data.get('mobil')

        if User.objects.filter(username=uname).exists():
            self.add_error('uname', 'Dieser Benutzername ist bereits vergeben.')

        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Es existiert bereits ein Benutzer mit dieser E-Mail.')

        if Userinfo.objects.filter(mobil=mobil).exists():
            self.add_error('mobil', 'Es existiert bereits ein Benutzer mit dieser Nummer.')

    def save(self):
        if not self.errors:
            data = self.cleaned_data
            user = User.objects.create_user(
                username=data['uname'],
                email=data['email'],
                first_name=data['fname'],
                last_name=data['lname'],
                password=data['pword'],
                is_active=False
            )
            Userinfo.objects.create(
                user=user,
                mobil=data['mobil'],
                street=data['street'],
                street_nr=data['street_nr'],
                zip_code=data['zip_code'],
                location=data['location'],
                self_description=data['self_description']
            )
            return user
    

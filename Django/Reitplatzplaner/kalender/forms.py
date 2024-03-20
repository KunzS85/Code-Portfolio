from django import forms
from .models import EVENT_DECLARATIONS

class WeekReservationForm(forms.Form):
    event_date_start = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'id' : 'datum',
                'style' : 'margin-right : 15px;'
            }
        ))
    event_time_start = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'id' : 'zeit',
                'style' : 'margin-right : 15px;'
            }
    ))

class DayReservationForm(forms.Form):
    event_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'id' : 'datum',
                'style' : 'margin-right : 15px;'
            }
        ))
    event_time_start = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'id' : 'zeit',
                'style' : 'margin-right : 15px;'
            }
    ))
    event_time_end = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'id' : 'zeit',
                'style' : 'margin-right : 15px;'
            }
    ))
    use_type = forms.CharField(
        widget=forms.Select(choices=EVENT_DECLARATIONS)
    )

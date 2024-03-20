from django import forms

class ReservationForm(forms.Form):
    from_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'id' : 'Von:',
                'style' : 'margin-right : 15px;'
            }
        ))
    
    to_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'id' : 'Bis:',
                'style' : 'margin-right : 15px;'
            }
        ))
from django import forms

class MaterialForm(forms.Form):
    item = forms.CharField(max_length=250)
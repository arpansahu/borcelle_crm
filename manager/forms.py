from django.forms import TextInput, EmailInput, HiddenInput
from django.urls import reverse


from django import forms

from manager.models import Contacts


class ContactsForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    country_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    gst = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class ContactsModelForm(forms.ModelForm):
    class Meta:
        model = Contacts

        fields = (
            'name',
            'country_code',
            'phone',
            'gst',
            'email',
            'address'
        )

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'country_code': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'gst': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'address': TextInput(attrs={'class': 'form-control'}),
        }


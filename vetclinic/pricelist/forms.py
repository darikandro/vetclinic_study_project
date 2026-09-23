from django import forms
from pricelist.models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
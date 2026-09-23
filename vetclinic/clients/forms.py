from django import forms
from phonenumber_field.formfields import PhoneNumberField
from clients.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class ClientCreationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['surname', 'name', 'patronymic', 'phone_number', 'email']


class ClientSearchForm(forms.Form):
    surname = forms.CharField(
        label="Фамилия", 
        max_length=60,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'})
    )
    phone_number = PhoneNumberField(
        label="Номер телефона",
        region="BY",  
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': '8 033 000-00-00'
        })
    )
from django import forms
from pets.models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = '__all__'


class PetClientForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'type', 'breed', 'gender', 'birth_date', 'photo']
        
from django import forms

from userinterface.morgan.models import Dog_profiles


class DogProfile(forms.ModelForm):
    class Meta:
        model=Dog_profiles
        fields='__all__'

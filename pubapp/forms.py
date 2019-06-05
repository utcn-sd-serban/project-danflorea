from django import forms
from django.contrib.auth.models import User

from pubapp.models import Character


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'role', 'birth_year', 'expiration_year']

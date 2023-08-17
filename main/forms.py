from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    
    phone = forms.CharField(label='phone')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'shudhanshu'}),
            'first_name': forms.TextInput(attrs={'class': 'shudhanshu'}),
            'last_name': forms.TextInput(attrs={'class': 'shudhanshu'}),
            'email': forms.EmailInput(attrs={'class': 'shudhanshu'}),

        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=("Password"), strip=False,  widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


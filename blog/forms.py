from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class LoginForm(forms.Form):

    login = forms.CharField(required=False, label='Nickname: ', max_length=20, widget=forms.TextInput)
    password = forms.CharField(required=False, label='Password: ', max_length=20, widget=forms.PasswordInput)


class RegisterForm(forms.Form):

    login = forms.CharField(label='Nickname: ', max_length=20, widget=forms.TextInput)
    password = forms.CharField( label='Password: ', max_length=20, widget=forms.PasswordInput)
    email = forms.EmailField(label='E-mail: ', max_length=30, widget=forms.TextInput)


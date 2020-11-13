from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Ticket, Comment


class TicketForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Ticket
        fields = ['name', 'surname', 'email', 'phone_number', 'event', 'captcha']
        readonly_fields = ('published_date',)

        widgets = {
            'event': forms.HiddenInput()
        }


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['name', 'email', 'subject', 'content', 'event', 'captcha']
        readonly_fields = ('published_date',)

        widgets = {
            'event': forms.HiddenInput()
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(max_length=15)
    surname = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'surname', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


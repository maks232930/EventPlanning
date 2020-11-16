from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from .models import Ticket, Comment


class TicketForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Ticket
        fields = ['name', 'surname', 'email', 'event', 'captcha']
        readonly_fields = ('published_date',)

        widgets = {
            'event': forms.HiddenInput(),
            'name': forms.HiddenInput(),
            'surname': forms.HiddenInput(),
            'email': forms.HiddenInput()
        }


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['name', 'email', 'last_name', 'content', 'event', 'captcha']
        readonly_fields = ('published_date',)

        widgets = {
            'event': forms.HiddenInput(),
            'email': forms.HiddenInput(),
            'last_name': forms.HiddenInput(),
            'name': forms.HiddenInput(),
        }


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = 'username, password'


class UpdateUser(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')


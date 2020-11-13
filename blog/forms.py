from captcha.fields import CaptchaField
from django import forms
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



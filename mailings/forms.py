from django import forms
from .models import Client, Message, Mailing


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["email", "full_name", "comment"]


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "status", "message", "clients"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "clients": forms.SelectMultiple(attrs={"size": 6}),
        }
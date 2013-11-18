__author__ = 'ricky'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    message = forms.CharField()


class EventForm(forms.Form):
    title = forms.CharField()
    detail = forms.Textarea()
    date = forms.DateTimeField()
    limit = forms.IntegerField()

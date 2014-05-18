# -*- coding: utf-8 -*-
__author__ = 'ricky'

from django import forms

from models import *


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    message = forms.CharField()

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_title', 'event_detail', 'event_date', 'event_limit', 'event_hostname', 'event_type']

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"标记部分为必选项")
        else:
            cleaned_data = super(EventForm, self).clean()
        return cleaned_data



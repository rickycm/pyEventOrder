# -*- coding: utf-8 -*-
__author__ = 'ricky'

from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    message = forms.CharField()


class EventForm(forms.Form):
    title = forms.CharField(label='主题')
    detail = forms.CharField(label='详细信息', widget=forms.Textarea)
    date = forms.DateTimeField(label='活动时间', widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                                                            "pickSeconds": False}))
    limit = forms.IntegerField(label='人数限制')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-eventForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.add_input(Submit('submit', '保存'))

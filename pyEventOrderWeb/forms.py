# -*- coding: utf-8 -*-
__author__ = 'ricky'

from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset
from pyEventOrderWeb.models import *


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    message = forms.CharField()


class EventForm(forms.Form):
    title = forms.CharField(label='主题')
    detail = forms.CharField(label='详细信息', widget=forms.Textarea)
    date = forms.DateTimeField(
        label='活动时间',
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm","pickSeconds": False})
    )
    limit = forms.IntegerField(label='人数限制')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-eventForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.add_input(Submit('submit', '保存'))


class EventForm2(forms.ModelForm):
    event_title = forms.CharField(label=u"主题", required=True, error_messages={'required': u'必选项'})
    event_detail = forms.CharField(
        label=u'详细信息',
        widget=forms.Textarea(
            attrs={
                'placeholder': u"请输入事件详细信息。",
                'rows': 5,
                'style': "width:100%",
            }
        ),
        required=True,
        error_messages={'required': u'必选项'}
    )
    event_date = forms.DateTimeField(
        label=u'活动时间',
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm", "pickSeconds": False}),
        required=True,
        error_messages={'required': u'必选项'}
    )
    event_limit = forms.IntegerField(label=u'人数限制', error_messages={'required': u'必选项'})
    updated_by = forms.CharField(required=False, widget=forms.HiddenInput())
    event_type = forms.TypedChoiceField(
        label = u'活动类型',
        choices = ((1, "event"), (0, "order")),
        coerce = lambda x: bool(int(x)),
        #widget = forms.RadioSelect,
        widget=forms.HiddenInput(),
        initial = '1',
        required = True,
    )

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        Div(
            Div(Fieldset('event_title', 'event_detail', 'event_date', css_class='col-md-6')),
            Div(Fieldset('event_limit','event_type', css_class='col-md-6'))
        )
    )

    class Meta:
        fields = ('event_title', 'event_date', 'event_detail', 'event_limit')
        model = event

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"以下标记部分为必选项")
        else:
            cleaned_data = super(EventForm2, self).clean()
        return cleaned_data

class SettingForm(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput)
    inputname = forms.CharField(max_length=50, label='',
                               widget=forms.TextInput(attrs={'placeholder':'您在订活动时使用的名字',}))
    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-settingForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.add_input(Submit('submit', '保存'))


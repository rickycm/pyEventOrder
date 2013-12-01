# coding=utf-8
__author__ = 'Aston'

from django import forms
from models import WeixinApp

class SendMessageForm(forms.Form):
    sender = forms.ModelChoiceField(queryset=WeixinApp.objects.all(),required=True,label='发信公众号')
    receiver = forms.CharField(label='接收人')
    message = forms.CharField(max_length=512,label='文本消息')

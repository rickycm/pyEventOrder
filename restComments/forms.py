# coding=utf-8
__author__ = 'Aston'

from django import forms
from models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post']
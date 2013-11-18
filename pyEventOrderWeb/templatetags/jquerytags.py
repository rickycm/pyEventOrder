# -*- coding: utf-8 -*-
# __author__ = 'Aston'
#修改了原来django-jquery-js包中间的一些错误，从而可以在正确获得jquery.js文件。

from django.conf import settings
from django.forms.widgets import flatatt
from django.template import Library

from jquery.utils import jquery_path

register = Library()


@register.simple_tag
def jquery_script():
    return '<script{0}></script>'.format(flatatt({
        'type': 'text/javascript',
        'src': settings.STATIC_URL + jquery_path,
    }))

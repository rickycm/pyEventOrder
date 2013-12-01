__author__ = 'Aston'
from django.conf.urls import patterns, url

urlpatterns = patterns('djWeixinApp.views',
    url(r'^Weixin/$', 'sendMessage'),
)
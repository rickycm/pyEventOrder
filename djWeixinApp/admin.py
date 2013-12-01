from django.contrib import admin
from djWeixinApp.models import *

class WeixinAppAdmin(admin.ModelAdmin):
    list_display = ('openid', 'information', 'app_id', 'app_secret')
    fields = ('openid', 'information', 'app_id', 'app_secret')

admin.site.register(WeixinApp, WeixinAppAdmin)
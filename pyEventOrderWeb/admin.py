__author__ = 'ricky'
from django.contrib import admin
from pyEventOrderWeb.models import event, participant, wechat_user

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'updated_by', 'updated_date', 'event_date')
    search_fields = ('event_title', 'updated_by', 'event_type', 'event_detail')
    list_filter = ('updated_date',)
    date_hierarchy = 'updated_date'

admin.site.register(event, EventAdmin)
admin.site.register(participant)
admin.site.register(wechat_user)
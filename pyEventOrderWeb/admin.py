__author__ = 'ricky'
from django.contrib import admin
from pyEventOrderWeb.models import event, participant, wechat_user

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'updated_by', 'updated_date', 'event_date')
    search_fields = ('event_title', 'updated_by', 'event_type', 'event_detail')
    list_filter = ('updated_date',)
    date_hierarchy = 'updated_date'

class Wechat_userAdmin(admin.ModelAdmin):
    list_display = ('wechat_fakeID', 'wechat_username', 'wechat_inputname', 'wechat_usertype', 'openid', 'initialized')
    fields = ('wechat_fakeID', 'wechat_username', 'wechat_inputname', 'wechat_usertype', 'openid', 'initialized')

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('event_ID', 'partici_name', 'partici_type', 'partici_openid', 'register_time')


admin.site.register(event, EventAdmin)
admin.site.register(participant, ParticipantAdmin)
admin.site.register(wechat_user, Wechat_userAdmin)
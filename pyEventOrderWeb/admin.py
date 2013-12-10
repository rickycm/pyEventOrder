__author__ = 'ricky'
from django.contrib import admin
from pyEventOrderWeb.models import event, participant, wechat_user

class Wechat_userAdmin(admin.ModelAdmin):
    list_display = ('openid', 'inputname', 'last_login', 'email', 'email_valid')
    fields = ('openid', 'inputname', 'last_login', 'email', 'email_valid')

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'related_updated_by', 'updated_date', 'event_date')
    search_fields = ('event_title', 'updated_by', 'event_type', 'event_detail')
    list_filter = ('updated_date',)
    date_hierarchy = 'updated_date'
    def related_updated_by(self, obj):
        return obj.updated_by.inputname
    related_updated_by.short_description = 'updated_by'

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('event_ID', 'partici_name', 'partici_type', 'related_partici_user', 'register_time')
    def related_partici_user(self, obj):
        return obj.partici_user.inputname
    related_partici_user.short_description = 'partici_user'

admin.site.register(event, EventAdmin)
admin.site.register(participant, ParticipantAdmin)
admin.site.register(wechat_user, Wechat_userAdmin)
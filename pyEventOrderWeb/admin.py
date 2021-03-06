__author__ = 'ricky'
from django.contrib import admin

from pyEventOrderWeb.models import Event, Participant


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_title', 'related_updated_by', 'updated_date', 'event_date', 'participant_count')
    search_fields = ('event_title', 'updated_by', 'event_type', 'event_detail')
    list_filter = ('updated_date',)
    date_hierarchy = 'updated_date'
    def related_updated_by(self, obj):
        return obj.updated_by.first_name
    related_updated_by.short_description = 'updated_by'
    def participant_count(self, obj):
        return Participant.objects.filter(event_ID=obj).count()
    participant_count.short_description = 'participant'

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('event_ID', 'partici_name', 'partici_type', 'related_partici_user', 'register_time')
    def related_partici_user(self, obj):
        return obj.partici_user.first_name
    related_partici_user.short_description = 'partici_user'

admin.site.register(Event, EventAdmin)
admin.site.register(Participant, ParticipantAdmin)
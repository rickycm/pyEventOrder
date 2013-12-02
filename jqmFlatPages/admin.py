from django.contrib import admin
from models import JqmFlatPage

class JqmFlatPageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'page_id')

admin.site.register(JqmFlatPage, JqmFlatPageAdmin)
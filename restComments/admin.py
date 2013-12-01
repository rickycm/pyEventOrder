from django.contrib import admin
from models import *

class CommentAdmin(admin.ModelAdmin):
    list_display = ('userid','post','answer','created')

admin.site.register(Comment, CommentAdmin)
# Register your models here.

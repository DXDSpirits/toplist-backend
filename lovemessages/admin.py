from django.contrib import admin
from lovemessages.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'site', 'content', 'time_created']


admin.site.register(Message, MessageAdmin)

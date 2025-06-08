from django.contrib import admin
from .models import Client, Message, Mailing, Attempt

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'owner']
    search_fields = ['email', 'full_name']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'owner']
    search_fields = ['subject', 'body']

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'start_time', 'end_time', 'owner']
    list_filter = ['status']
    filter_horizontal = ['clients']

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['mailing', 'status', 'time']
    list_filter = ['status']
    readonly_fields = ['time']

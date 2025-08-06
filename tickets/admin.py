from django.contrib import admin
from .models import Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'assigned_to', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'created_by__username', 'assigned_to__username')
    ordering = ('-created_at',)

admin.site.register(Ticket, TicketAdmin)

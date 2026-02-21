from django.contrib import admin

from .models import Lead
# Register your models here.

class LeadAdmin(admin.ModelAdmin):
    list_filter = ("status", "source", "created_at")
    list_display = ("first_name", "last_name", "email", "status", "source", "created_at")

admin.site.register(Lead, LeadAdmin)
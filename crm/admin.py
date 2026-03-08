from django.contrib import admin

from .models import Lead, Note
# Register your models here.

class LeadAdmin(admin.ModelAdmin):
    list_filter = ("status", "source", "created_at", "updated_at")
    list_display = ("first_name", "last_name", "email", "status", "source", "created_at", "updated_at", "owner")
    readonly_fields = ("created_at", "updated_at")

admin.site.register(Lead, LeadAdmin)

class NoteAdmin(admin.ModelAdmin):
    list_display = ("created_at", "lead", "note_text")

admin.site.register(Note, NoteAdmin)
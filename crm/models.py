from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Status(models.TextChoices):
    NEW = "new", "New"
    CONTACTED = "contacted", "Contacted"
    WON = "won", "Won"
    LOST = "lost", "Lost"

class Source(models.TextChoices):
    WEBSITE ="website", "Website"
    INSTAGRAM = "instagram", "Instagram"
    TELEGRAM = "telegram","Telegram"
    REFERRAL = "referral","Referral"

class Lead(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=25, blank=True)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.WEBSITE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.get_status_display()} "
    

class Note(models.Model):
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return f"Note for {self.lead} at {self.created_at}"
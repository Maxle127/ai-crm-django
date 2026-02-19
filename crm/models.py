from django.db import models

# Create your models here.

class Lead(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    source = models.CharField(max_length=15)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
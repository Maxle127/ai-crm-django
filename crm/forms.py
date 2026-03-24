from django import forms
from .models import Lead, Profile

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["first_name", "last_name", "email", "phone", "source", "status", "attachment"]
        widgets = {
            "attachment": forms.FileInput(),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
        widgets = {
            "avatar": forms.FileInput(),
        }
        
from django import forms
from .models import Lead, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
        
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
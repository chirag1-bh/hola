from django import forms
from .models import Doctor

class DoctorApplicationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'name', 'email', 'phone', 'specialization', 'qualification',
            'experience', 'hospital', 'city', 'pincode', 'degree_proof',
            'available_days', 'available_time', 'consultation_fee'
        ]
        widgets = {
            'available_days': forms.TextInput(attrs={'placeholder': 'Mon-Fri'}),
            'available_time': forms.TextInput(attrs={'placeholder': '10 AM - 5 PM'}),
        }

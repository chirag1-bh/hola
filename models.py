from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    state = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=20, null=True, blank=True)
    telephone = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    # 🔹 Linked with Django User model for login
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='hospital_profile')


    # 🔹 Existing fields
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)

    # 🔹 Optional doctor info for profile
    city = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"


class Patient(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    APPOINTMENT_TYPES = (
        ('doctor', 'Doctor Appointment'),
        ('general', 'General Inquiry'),
    )

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled")
    ]

    appointment_type = models.CharField(
        max_length=10, choices=APPOINTMENT_TYPES, default='general'
    )

    # General Inquiry fields
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, default='0000000000')
    email = models.EmailField(blank=True, null=True)
    query = models.TextField(blank=True, null=True)

    # Doctor appointment fields
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.appointment_type == 'doctor' and self.patient and self.doctor:
            return f"{self.patient.name} → {self.doctor.name} on {self.date.strftime('%Y-%m-%d %H:%M')}"
        else:
            return f"General Appointment: {self.name} - {self.query[:20] if self.query else 'No query'}"

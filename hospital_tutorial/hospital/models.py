from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='patient'
    )

    def __str__(self):
        return self.username


class Doctor(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'}
    )

    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'}
    )

    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class Appointment(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()

    medical_report = models.FileField(
        upload_to='medical_reports/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.username} -> {self.doctor.user.username}"

class Prescription(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE
    )

    medicine = models.TextField(blank=True, null=True)
    dosage = models.TextField(blank=True, null=True)
    advice = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription - {self.appointment.patient.user.username}"

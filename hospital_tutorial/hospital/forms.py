from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import (
    CustomUser,
    Patient,
    Appointment,
)


class DoctorRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class PatientRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = "__all__"


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = [
            'doctor',
            'appointment_date',
            'appointment_time',
            'reason',
            'medical_report',
        ]

        widgets = {
            'doctor': forms.Select(attrs={
                'class': 'form-control'
            }),

            'appointment_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'appointment_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'reason': forms.Textarea(
                attrs={
                    'rows': 4,
                    'class': 'form-control',
                    'placeholder': 'Reason for appointment'
                }
            ),
        }


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your full name',
            'class': 'form-control'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-control'
        })
    )

    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your phone number',
            'class': 'form-control'
        })
    )

    subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter subject',
            'class': 'form-control'
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Write your message...',
            'class': 'form-control',
            'rows': 5
        })
    )


    from django import forms
from .models import Prescription




from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            "medicine",
            "dosage",
            "advice",
        ]

        widgets = {
            "medicine": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),
            "dosage": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
            "advice": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),
        }
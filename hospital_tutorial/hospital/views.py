from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PatientForm, AppointmentForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import Prescription
from .forms import PrescriptionForm
from django.shortcuts import get_object_or_404

from .models import CustomUser, Patient, Doctor, Appointment
from .forms import (
    DoctorRegisterForm,
    PatientRegisterForm,
    PatientForm,
)


# ==========================
# Authentication
# ==========================
def login_view(request):

    if request.user.is_authenticated:
        if request.user.role == "doctor":
            return redirect("doctor_dashboard")
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.role == "doctor":
                return redirect("doctor_dashboard")

            return redirect("home")

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, "accounts/login.html")

#doctor only show appoinment
@login_required(login_url='login')
def appointment_list(request):

    if request.user.role == "patient":
        patient = Patient.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=patient)

    else:
        doctor = Doctor.objects.get(user=request.user)

        print("Logged in doctor:", doctor)
        print("Doctor ID:", doctor.id)

        appointments = Appointment.objects.filter(doctor=doctor)

        print("Appointments found:", appointments.count())

        for appointment in appointments:
            print(
                appointment.patient.user.username,
                appointment.doctor.user.username
            )

    return render(
        request,
        "appointments/appointment_list.html",
        {"appointments": appointments}
    )

@login_required(login_url='login')
def appointment_list(request):

    if request.user.role != "doctor":
        return redirect("home")

    doctor = Doctor.objects.get(user=request.user)

    appointments = Appointment.objects.filter(
        doctor=doctor
    )

    return render(
        request,
        "appointments/appointment_list.html",
        {
            "appointments": appointments
        }
    )#---------------------------------


def logout_view(request):
    logout(request)
    return redirect("login")


def doctor_register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = DoctorRegisterForm()

    if request.method == "POST":
        form = DoctorRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = "doctor"
            user.save()

            Doctor.objects.create(
                user=user,
                specialization="General",
                phone=""
            )

            return redirect("login")

    return render(
        request,
        "accounts/doctor_register.html",
        {"form": form}
    )


def patient_register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = PatientRegisterForm()

    if request.method == "POST":
        form = PatientRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = "patient"
            user.save()

            Patient.objects.create(
                user=user,
                age=0,
                gender="",
                phone=""
            )

            return redirect("login")

    return render(
        request,
        "accounts/patient_register.html",
        {"form": form}
    )

# ==========================
# Public Pages
# ==========================

@login_required(login_url="login")
def home(request):
    return render(request, "home.html")


@login_required(login_url="login")
def about(request):
    return render(request, "about.html")


@login_required(login_url="login")
def contact(request):
    return render(request, "contact.html")


@login_required(login_url="login")
def service(request):
    return render(request, "service.html")


# ==========================
# Dashboard
# ==========================

@login_required(login_url="login")
def dashboard(request):
    return render(request, "dashboard/dashboard.html")


@login_required(login_url="login")
def doctor_dashboard(request):

    if request.user.role != "doctor":
        return redirect("dashboard")

    return render(request, "dashboard/doctor_dashboard.html")


# ==========================
# Patients
# ==========================

@login_required(login_url="login")
def patient_list(request):

    patients = Patient.objects.all()

    return render(
        request,
        "patients/patients_list.html",
        {"patients": patients}
    )


@login_required(login_url="login")
def add_patient(request):

    form = PatientForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("patient_list")

    return render(
        request,
        "patients/add_patient.html",
        {"form": form}
    )


# ==========================
# Doctors
# ==========================

@login_required(login_url="login")
def doctor_list(request):
    doctors = Doctor.objects.all()

    return render(
        request,
        "doctors/doctor_list.html",
        {"doctors": doctors}
    )


@login_required(login_url="login")
def add_doctor(request):
    return render(request, "doctors/add_doctor.html")


# ==========================
# Appointments
# ==========================

@login_required(login_url='login')
def appointment_list(request):

    if request.user.role == "patient":

        patient = Patient.objects.get(user=request.user)

        appointments = Appointment.objects.filter(
            patient=patient
        )

    else:

        doctor = Doctor.objects.get(user=request.user)

        appointments = Appointment.objects.filter(
            doctor=doctor
        )

    return render(
        request,
        "appointments/appointment_list.html",
        {
            "appointments": appointments
        }
    )


#booking

from .forms import AppointmentForm

@login_required(login_url='login')
def book_appointment(request):

    if request.user.role != "patient":
        return redirect("doctor_dashboard")

    patient = Patient.objects.get(user=request.user)

    if request.method == "POST":

        form = AppointmentForm(request.POST, request.FILES)

        if form.is_valid():

            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()

            return redirect("appointment_list")

    else:
        form = AppointmentForm()

    return render(
        request,
        "appointments/book_appointment.html",
        {"form": form}
    )


def contact(request):

    form = ContactForm()

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            body = f"""
Name: {name}
Email: {email}
Phone: {phone}

Message:

{message}
"""

            send_mail(
    subject=subject,
    message=body,
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[settings.EMAIL_HOST_USER],
    fail_silently=False,
)
            return render(
                request,
                "contact.html",
                {
                    "form": ContactForm(),
                    "success": True
                }
            )

    return render(
        request,
        "contact.html",
        {
            "form": form
        }
    )

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect("login")




from django.shortcuts import get_object_or_404

@login_required(login_url="login")
def approve_appointment(request, id):

    if request.user.role != "doctor":
        return redirect("home")

    appointment = get_object_or_404(Appointment, id=id)

    appointment.status = "Approved"
    appointment.save()

    return redirect("appointment_list")



@login_required(login_url="login")
def delete_appointment(request, id):

    if request.user.role != "doctor":
        return redirect("home")

    appointment = get_object_or_404(Appointment, id=id)

    appointment.delete()

    return redirect("appointment_list")

    appointment = get_object_or_404(Appointment, id=id)

    appointment.delete()

    return redirect("appointment_list")



from .models import Appointment, Prescription
from .forms import PrescriptionForm


@login_required
def create_prescription(request, id):

    appointment = get_object_or_404(Appointment, id=id)

    if request.method == "POST":
        form = PrescriptionForm(request.POST)

        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()

            return redirect("appointment_list")

    else:
        form = PrescriptionForm()

    return render(
        request,
        "prescription/create.html",
        {
            "form": form,
            "appointment": appointment,
        }
    )

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def create_prescription(request, id):

    appointment = get_object_or_404(Appointment, id=id)

    prescription, created = Prescription.objects.get_or_create(
        appointment=appointment
    )

    if request.method == "POST":
        form = PrescriptionForm(
            request.POST,
            instance=prescription   # <-- IMPORTANT
        )

        if form.is_valid():
            form.save()
            return redirect("appointment_list")

    else:
        form = PrescriptionForm(instance=prescription)

    return render(
        request,
        "prescription/create_prescription.html",
        {
            "form": form,
            "appointment": appointment,
        },
    )

from .models import Prescription
from django.shortcuts import get_object_or_404

@login_required(login_url="login")
def view_prescription(request, id):

    appointment = get_object_or_404(Appointment, id=id)

    prescription = get_object_or_404(
        Prescription,
        appointment=appointment
    )

    return render(
        request,
        "prescription/view_prescription.html",
        {
            "appointment": appointment,
            "prescription": prescription,
        },
    )

@login_required(login_url="login")
def create_prescription(request, id):

     if request.user.role != "doctor":
        return redirect("home")

     appointment = get_object_or_404(Appointment, id=id)

     prescription = Prescription.objects.filter(
        appointment=appointment
    ).first()

     if request.method == "POST":

        if prescription:
            form = PrescriptionForm(request.POST, instance=prescription)
        else:
            form = PrescriptionForm(request.POST)

        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()
            return redirect("appointment_list")

     else:

        if prescription:
            form = PrescriptionForm(instance=prescription)
        else:
            form = PrescriptionForm()

        return render(
        request,
        "prescription/create_prescription.html",
        {
            "form": form,
            "appointment": appointment
        }
    )
     
@login_required(login_url="login")
def view_prescription(request, id):

    appointment = get_object_or_404(Appointment, id=id)
    prescription = get_object_or_404(Prescription, appointment=appointment)

    # Doctor can view only their own prescriptions
    if request.user.role == "doctor":
        if appointment.doctor.user != request.user:
            return redirect("home")

    # Patient can view only their own prescriptions
    elif request.user.role == "patient":
        if appointment.patient.user != request.user:
            return redirect("home")

    else:
        return redirect("home")

    return render(
        request,
        "prescription/view_prescription.html",
        {
            "appointment": appointment,
            "prescription": prescription,
        },
    )
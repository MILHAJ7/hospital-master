from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),

    path('doctor-register/', views.doctor_register, name='doctor_register'),
    path('patient-register/', views.patient_register, name='patient_register'),

    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.add_patient, name='add_patient'),

    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),

    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('service/', views.service, name='service'),

  
    path(
    "appointment/approve/<int:id>/",
    views.approve_appointment,
    name="approve_appointment",
   ),

    path(
    "appointment/delete/<int:id>/",
    views.delete_appointment,
    name="delete_appointment",
            ),
    
    path(
    "prescription/<int:id>/",
    views.create_prescription,
    name="create_prescription",
),

path(
    "prescription/<int:id>/",
    views.create_prescription,
    name="create_prescription"
),
path(
    "prescription/view/<int:id>/",
    views.view_prescription,
    name="view_prescription",
),

]
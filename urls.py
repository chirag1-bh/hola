from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from hospital import views

urlpatterns = [
    path('', views.home, name='home'),
    path("appointments/", views.appointment_view, name="appointment_list"),  # Changed to appointment_view
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('book/', views.book_appointment, name='book_appointment'),
    path("hospitals/", views.hospital_list, name="hospital_list"),  # ✅ Hospitals List Page
    path("hospital-autocomplete/", views.hospital_autocomplete, name="hospital_autocomplete"),
    path('specialization/', views.specializations, name='specializations'),
    path('specialization/cardiology/', views.cardiology, name='cardiology'),
    path('specialization/dermatology/', views.dermatology, name='dermatology'),
    path('specialization/orthopedics/', views.orthopedics, name='orthopedics'),
    path('specialization/pediatrics/', views.pediatrics, name='pediatrics'),
    path('specialization/neurology/', views.neurology, name='neurology'),
    path('specialization/gynecology/', views.gynecology, name='gynecology'),
    path('specialization/ophthalmology/', views.ophthalmology, name='ophthalmology'),
    path('specialization/dentistry/', views.dentistry, name='dentistry'),
    path("account/", views.account, name="account"),
    path("doctor/login/", views.doctor_login, name="doctor_login"),
    path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("doctor/logout/", views.doctor_logout, name="doctor_logout"),
    path('doctor/login/', views.doctor_login_page, name='doctor-login-page'),
    path('doctor/profile/', views.doctor_profile_page, name='doctor-profile-page'),
    path('find-doctors/', views.find_doctors, name='find_doctors'),
    path('doctors/<str:specialization>/', views.doctors_by_specialization, name='doctors_by_specialization'),
    
]

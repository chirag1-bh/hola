from django.shortcuts import render, redirect
from .models import Hospital, Doctor, Patient, Appointment
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_GET


def doctor_login_page(request):
    return render(request, 'doctor_login.html')

def doctor_profile_page(request):
    return render(request, 'doctor_profile.html')


# -------------------- HOME --------------------
def home(request):
    hospitals = Hospital.objects.all()
    doctors = Doctor.objects.all()
    
    # Add demo doctors if they don’t exist
    qrg_hospital = Hospital.objects.filter(name__icontains="qrg").first()
    abcd_hospital = Hospital.objects.filter(name__icontains="abcd").first()
    
    if qrg_hospital and not Doctor.objects.filter(name="Puneet").exists():
        Doctor.objects.create(
            name="Puneet",
            specialization="Naali Expert",
            hospital=qrg_hospital
        )
    
    if abcd_hospital and not Doctor.objects.filter(name="Sherpal Bairagi").exists():
        Doctor.objects.create(
            name="Sherpal Bairagi",
            specialization="Acting Expert",
            hospital=abcd_hospital
        )
    
    return render(request, "hospital/home.html", {"hospitals": hospitals, "doctors": doctors})


# -------------------- BOOK APPOINTMENT --------------------
def book_appointment(request):
    if request.method == "POST":
        if 'patient_name' in request.POST:  # Doctor appointment form
            patient_name = request.POST.get("patient_name")
            patient_email = request.POST.get("patient_email")
            patient_phone = request.POST.get("patient_phone")
            doctor_id = request.POST.get("doctor")
            date_str = request.POST.get("date")

            try:
                patient = Patient.objects.get(phone=patient_phone)
                patient.name = patient_name
                patient.email = patient_email
                patient.save()
            except Patient.DoesNotExist:
                patient = Patient.objects.create(
                    name=patient_name,
                    email=patient_email,
                    phone=patient_phone
                )
            except Patient.MultipleObjectsReturned:
                patient = Patient.objects.filter(phone=patient_phone).first()
                patient.name = patient_name
                patient.email = patient_email
                patient.save()

            try:
                appointment_date = datetime.fromisoformat(date_str)
            except ValueError:
                try:
                    appointment_date = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    appointment_date = datetime.now()

            doctor = Doctor.objects.get(id=doctor_id)
            appointment = Appointment.objects.create(
                appointment_type='doctor',
                patient=patient,
                doctor=doctor,
                date=appointment_date,
                phone=patient_phone
            )

            subject = "Appointment Confirmation"
            message = f"""
Hello {patient.name},

Your appointment has been successfully booked!

📅 Date: {appointment.date.strftime('%Y-%m-%d %H:%M')}
👨‍⚕️ Doctor: {doctor.name} ({doctor.specialization})
🏥 Hospital: {doctor.hospital.name}

Thank you for using our Hospital Appointment System!
            """
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [patient.email],
                    fail_silently=False,
                )
                messages.success(request, f"✅ Appointment booked successfully for {patient.name}. Confirmation email sent to {patient.email}.")
            except Exception as e:
                messages.success(request, f"✅ Appointment booked for {patient.name}. (Email failed: {str(e)})")
            
            return redirect('home')
        
        else:  # General inquiry form
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            query = request.POST.get("query")

            Appointment.objects.create(
                appointment_type='general',
                name=name,
                phone=phone,
                email=email,
                query=query
            )
            
            messages.success(request, '🎉 Your inquiry has been submitted successfully! We’ll contact you soon.')
            return redirect("home")

    doctors = Doctor.objects.all()
    return render(request, "hospital/book_appointment.html", {"doctors": doctors})


# -------------------- SIGNUP --------------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, '🎉 Account created successfully! Welcome to our Hospital App.')
        return redirect("home")

    return render(request, "registration/signup.html")


# -------------------- APPOINTMENT PAGE --------------------
def appointment_view(request):
    appointments = Appointment.objects.all().order_by("-date")
    return render(request, "hospital/appointment.html", {"appointments": appointments})


# -------------------- HOSPITAL LIST WITH PAGINATION --------------------
def hospital_list(request):
    hospital_list = Hospital.objects.all().order_by("name")
    paginator = Paginator(hospital_list, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "hospital/hospital_list.html", {"page_obj": page_obj})


# -------------------- AUTOCOMPLETE --------------------
@require_GET
def hospital_autocomplete(request):
    q = request.GET.get("q", "").strip()
    city = request.GET.get("city", "").strip()
    qs = Hospital.objects.all()
    if q:
        qs = qs.filter(name__icontains=q)
    if city:
        qs = qs.filter(state__icontains=city)
    qs = qs.values("id", "name")[:10]
    return JsonResponse(list(qs), safe=False)


# -------------------- SPECIALIZATION PAGES --------------------
def specializations(request):
    return render(request, 'hospital/specializations.html')

def cardiology(request):
    return render(request, 'hospital/cardiology.html')

def dermatology(request):
    return render(request, 'hospital/dermatology.html')

def orthopedics(request):
    return render(request, 'hospital/orthopedics.html')

def pediatrics(request):
    return render(request, 'hospital/pediatrics.html')

def neurology(request):
    return render(request, 'hospital/neurology.html')

def gynecology(request):
    return render(request, 'hospital/gynecology.html')

def ophthalmology(request):
    return render(request, 'hospital/ophthalmology.html')

def dentistry(request):
    return render(request, 'hospital/dentistry.html')


# -------------------- ACCOUNT PAGE --------------------
def account(request):
    return render(request, "hospital/account.html")



# ==============================
# 🩺 DOCTOR LOGIN + DASHBOARD
# ==============================
def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('doctor_dashboard')
        else:
            messages.error(request, "❌ Invalid username or password.")
            return render(request, 'hospital/doctor_login.html')

    return render(request, 'hospital/doctor_login.html')


@login_required
def doctor_dashboard(request):
    doctor = Doctor.objects.filter(user=request.user).first()
    if not doctor:
        messages.warning(request, "Doctor profile not linked with this user.")
        return redirect('doctor_login')

    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date')
    patients = [appt.patient for appt in appointments if appt.patient]

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'patients': patients,
        'total_appointments': appointments.count(),
        'total_patients': len(set(patients)),
    }
    return render(request, 'hospital/doctor_dashboard.html', context)


def doctor_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('doctor_login')


# ==============================
# 🩻 FIND DOCTORS
# ==============================
def find_doctors(request):
    specializations = Doctor.objects.values_list('specialization', flat=True).distinct()
    doctors = Doctor.objects.all()
    return render(request, 'find_doctors.html', {'specializations': specializations, 'doctors': doctors})


def doctors_by_specialization(request, specialization):
    doctors = Doctor.objects.filter(specialization=specialization)
    return render(request, 'doctors_by_specialization.html', {
        'specialization': specialization,
        'doctors': doctors
    })


def doctor_login_page(request):
    return render(request, 'doctor_login.html')

def doctor_profile_page(request):
    return render(request, 'doctor_profile.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, date, timedelta
from .models import Patient, Doctor, Appointment
from .forms import PatientForm, UserRegisterForm, DoctorForm, AppointmentForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'patients/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('patient_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'patients/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def patient_list(request):
    query = request.GET.get('q', '')
    if query:
        patients = Patient.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients, 'query': query})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patients/patient_detail.html', {'patient': patient})


@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            messages.success(request, 'Patient created successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {'form': form, 'action': 'Create'})


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {'form': form, 'action': 'Update', 'patient': patient})


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully!')
        return redirect('patient_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})


# Doctor views
@login_required
def doctor_list(request):
    query = request.GET.get('q', '')
    if query:
        doctors = Doctor.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(specialization__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        doctors = Doctor.objects.all()
    return render(request, 'patients/doctor_list.html', {'doctors': doctors, 'query': query})


@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    # Get upcoming appointments for this doctor
    upcoming_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gte=date.today()
    ).exclude(status='CANCELLED').order_by('appointment_date', 'appointment_time')[:10]
    return render(request, 'patients/doctor_detail.html', {
        'doctor': doctor,
        'upcoming_appointments': upcoming_appointments
    })


@login_required
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, 'Doctor added successfully!')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm()
    return render(request, 'patients/doctor_form.html', {'form': form, 'action': 'Add'})


@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor updated successfully!')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'patients/doctor_form.html', {'form': form, 'action': 'Update', 'doctor': doctor})


# Appointment views
@login_required
def appointment_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    
    appointments = Appointment.objects.all()
    
    if query:
        appointments = appointments.filter(
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(doctor__first_name__icontains=query) |
            Q(doctor__last_name__icontains=query)
        )
    
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    return render(request, 'patients/appointment_list.html', {
        'appointments': appointments,
        'query': query,
        'status_filter': status_filter
    })


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'patients/appointment_detail.html', {'appointment': appointment})


@login_required
def appointment_book(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.created_by = request.user
            try:
                appointment.save()
                messages.success(request, 'Appointment booked successfully!')
                return redirect('appointment_detail', pk=appointment.pk)
            except Exception as e:
                messages.error(request, f'Error booking appointment: {str(e)}')
    else:
        form = AppointmentForm()
    
    # Get available doctors for display
    available_doctors = Doctor.objects.filter(is_available=True)
    
    return render(request, 'patients/appointment_book.html', {
        'form': form,
        'available_doctors': available_doctors
    })


@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Appointment updated successfully!')
                return redirect('appointment_detail', pk=appointment.pk)
            except Exception as e:
                messages.error(request, f'Error updating appointment: {str(e)}')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'patients/appointment_form.html', {
        'form': form,
        'action': 'Update',
        'appointment': appointment
    })


@login_required
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.status = 'CANCELLED'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully!')
        return redirect('appointment_list')
    return render(request, 'patients/appointment_confirm_cancel.html', {'appointment': appointment})


@login_required
def available_time_slots(request, doctor_id, date_str):
    """API endpoint to get available time slots for a doctor on a specific date"""
    try:
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Define working hours (9 AM to 5 PM with 1-hour slots)
        time_slots = []
        for hour in range(9, 17):
            slot_time = f"{hour:02d}:00"
            # Check if this slot is already booked
            is_booked = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=slot_time
            ).exclude(status='CANCELLED').exists()
            
            time_slots.append({
                'time': slot_time,
                'available': not is_booked
            })
        
        return render(request, 'patients/time_slots.html', {
            'time_slots': time_slots,
            'doctor': doctor,
            'date': appointment_date
        })
    except Exception as e:
        messages.error(request, f'Error fetching time slots: {str(e)}')
        return redirect('appointment_book')

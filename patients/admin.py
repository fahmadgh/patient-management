from django.contrib import admin
from .models import Patient, Doctor, Appointment

# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone_number', 'email']
    ordering = ['-created_at']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'specialization', 'phone_number', 'email', 'is_available']
    search_fields = ['first_name', 'last_name', 'specialization', 'email']
    list_filter = ['specialization', 'is_available']
    date_hierarchy = 'created_at'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'timezone']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name']
    list_filter = ['status', 'appointment_date', 'doctor']
    date_hierarchy = 'appointment_date'
    autocomplete_fields = ['patient']

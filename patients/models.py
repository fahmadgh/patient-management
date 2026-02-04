from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, date

# Create your models here.

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    medical_history = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
        return age


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('GP', 'General Practitioner'),
        ('CARD', 'Cardiologist'),
        ('DERM', 'Dermatologist'),
        ('NEUR', 'Neurologist'),
        ('ORTH', 'Orthopedist'),
        ('PEDI', 'Pediatrician'),
        ('PSYC', 'Psychiatrist'),
        ('SURG', 'Surgeon'),
        ('OTHER', 'Other'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=10, choices=SPECIALIZATION_CHOICES)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.get_specialization_display()}"
    
    def get_full_name(self):
        return f"Dr. {self.first_name} {self.last_name}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SCHEDULED')
    notes = models.TextField(blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['appointment_date', 'appointment_time']
        # Prevent double booking - one doctor cannot have overlapping appointments
        unique_together = [['doctor', 'appointment_date', 'appointment_time']]
        indexes = [
            models.Index(fields=['appointment_date', 'appointment_time']),
            models.Index(fields=['doctor', 'appointment_date']),
            models.Index(fields=['patient', 'appointment_date']),
        ]
    
    def __str__(self):
        return f"{self.patient.get_full_name()} with {self.doctor.get_full_name()} on {self.appointment_date} at {self.appointment_time}"
    
    def clean(self):
        # Validate appointment is not in the past
        if self.appointment_date and self.appointment_time:
            appointment_datetime = datetime.combine(self.appointment_date, self.appointment_time)
            if timezone.is_aware(appointment_datetime):
                appointment_datetime = timezone.make_naive(appointment_datetime)
            if appointment_datetime < timezone.now().replace(tzinfo=None):
                raise ValidationError('Cannot book appointments in the past.')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

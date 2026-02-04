# Patient Management System

A fully functional patient management system built with Django and SQLite, featuring user authentication, patient management, doctor management, and appointment booking with a simple, clean user interface.

## Features

- **User Authentication**: Secure login and registration system
- **Patient Management**: Complete CRUD (Create, Read, Update, Delete) operations for patient records
- **Doctor Management**: Manage doctor profiles with specializations and availability status
- **Appointment Booking**: Schedule appointments between patients and doctors with timezone support
- **Search Functionality**: Search patients by name, phone, or email; search doctors by name or specialization
- **Comprehensive Patient Records**: Track personal information, medical history, medications, and allergies
- **Appointment Tracking**: View, update, and cancel appointments with status management
- **Double Booking Prevention**: Database constraints and validation to prevent scheduling conflicts
- **Timezone Support**: Book appointments across different timezones (400+ timezones supported)
- **Responsive UI**: Clean and professional user interface
- **SQLite Database**: Lightweight database for easy setup and portability

## Requirements

- Python 3.8+
- Django 4.2.26
- pytz (for timezone support)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/fahmadgh/patient-management.git
cd patient-management
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run database migrations:
```bash
python manage.py migrate
```

4. Create a superuser account:
```bash
python manage.py createsuperuser
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Access the application at `http://localhost:8000`

## Usage

### First-Time Setup

1. Navigate to `http://localhost:8000` in your browser
2. Click "Register here" to create a new account
3. Fill in your username, email, and password
4. Login with your new credentials

### Managing Patients

**Add a New Patient:**
1. Click "Add Patient" in the navigation bar
2. Fill in the patient's personal and medical information
3. Click "Create Patient" to save

**View Patient List:**
- Click "Patients" in the navigation bar to see all patients
- Use the search box to find specific patients

**View Patient Details:**
- Click "View" next to any patient in the list
- See comprehensive patient information including medical history

**Edit Patient Information:**
- Click "Edit" on the patient detail page
- Update the information as needed
- Click "Update Patient" to save changes

**Delete a Patient:**
- Click "Delete" on the patient detail page
- Confirm the deletion

### Managing Doctors

**Add a New Doctor:**
1. Click "Doctors" in the navigation bar
2. Click "+ Add New Doctor"
3. Fill in the doctor's information and specialization
4. Set availability status
5. Click "Add Doctor" to save

**View Doctor List:**
- Click "Doctors" in the navigation bar to see all doctors
- Search doctors by name, specialization, or email

**View Doctor Details:**
- Click "View" next to any doctor in the list
- See doctor information and upcoming appointments

**Edit Doctor Information:**
- Click "Edit" on the doctor detail page
- Update availability status or other information
- Click "Update Doctor" to save changes

### Booking and Managing Appointments

**Book a New Appointment:**
1. Click "Book Appointment" in the navigation bar
2. Select the patient and doctor from the dropdowns
3. Choose the appointment date and time
4. Select your timezone
5. Add any notes (optional)
6. Click "Book Appointment" to confirm

**View Appointments:**
- Click "Appointments" in the navigation bar
- Filter by status (Scheduled, Confirmed, Cancelled, Completed)
- Search by patient or doctor name

**View Appointment Details:**
- Click "View" next to any appointment
- See complete appointment information including status and notes

**Update an Appointment:**
- Click "Edit" on the appointment detail page
- Modify the date, time, or other details
- Click "Update Appointment" to save

**Cancel an Appointment:**
- Click "Cancel" on the appointment detail page
- Confirm the cancellation

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin` to manage users and patients with advanced features.

## Default Credentials (for testing)

If you created a superuser during setup, use those credentials. Otherwise, create a new account through the registration page.

## Project Structure

```
patient-management/
├── patient_management_system/  # Main project settings
│   ├── settings.py            # Django settings
│   ├── urls.py                # URL routing
│   └── wsgi.py                # WSGI configuration
├── patients/                  # Patients app
│   ├── models.py             # Patient, Doctor, and Appointment models
│   ├── views.py              # View logic for all features
│   ├── forms.py              # Forms for patient, doctor, and appointments
│   ├── urls.py               # URL patterns
│   ├── templates/            # HTML templates
│   │   └── patients/         # App-specific templates
│   │       ├── base.html              # Base template with navigation
│   │       ├── patient_*.html         # Patient management templates
│   │       ├── doctor_*.html          # Doctor management templates
│   │       └── appointment_*.html     # Appointment booking templates
│   └── admin.py              # Admin configuration
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## Technologies Used

- **Backend**: Django 4.2.26
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3 (no external CSS frameworks)
- **Authentication**: Django built-in authentication system

## Security Notes

⚠️ **Important**: This is a development/demo project. For production use:
- Change the SECRET_KEY in `settings.py` and store it in environment variables
- Set `DEBUG = False` in production
- Configure `ALLOWED_HOSTS` properly
- Use a production-grade database (PostgreSQL, MySQL, etc.)
- Enable HTTPS
- Implement additional security measures as needed

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.
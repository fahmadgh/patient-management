# Patient Management System

A fully functional patient management system built with Django and SQLite, featuring user authentication and a simple, clean user interface.

## Features

- **User Authentication**: Secure login and registration system
- **Patient Management**: Complete CRUD (Create, Read, Update, Delete) operations for patient records
- **Search Functionality**: Search patients by name, phone, or email
- **Comprehensive Patient Records**: Track personal information, medical history, medications, and allergies
- **Responsive UI**: Clean and professional user interface
- **SQLite Database**: Lightweight database for easy setup and portability

## Requirements

- Python 3.8+
- Django 4.2.26

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
│   ├── models.py             # Patient model
│   ├── views.py              # View logic
│   ├── forms.py              # Forms for patient and user
│   ├── urls.py               # URL patterns
│   ├── templates/            # HTML templates
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
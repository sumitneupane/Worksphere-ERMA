# WorkSphere ERMA - Setup Guide

## Installation Steps

### Step 1: Install Python
Make sure Python 3.7 or higher is installed:
```bash
python --version
```

### Step 2: Install Flask
```bash
pip install flask
```

### Step 3: Run the Application

**Windows:**
```
start.bat
```

**Mac/Linux:**
```
chmod +x start.sh
./start.sh
```

### Step 4: Access the System
Open your browser and go to:
```
http://localhost:5000
```

## First Time Setup

The system will automatically:
1. Create the SQLite database
2. Set up all required tables
3. Insert sample data
4. Initialize departments
5. Create admin and employee users
6. Generate sample training courses
7. Create sample schedules

## Testing the System

### Test Admin Features:
1. Login as admin (admin/admin123)
2. Navigate through all admin pages
3. Try adding a new user
4. Create a training course
5. Assign training to employees
6. Handle a support ticket
7. Generate a payslip

### Test Employee Features:
1. Login as john.doe (john.doe/password123)
2. View your schedule
3. Submit a leave request
4. Complete a training course
5. Create a support ticket
6. Send a chat message
7. View your payslips

### Test MFA Feature:
1. As admin, toggle MFA for a user
2. Logout and login as that user
3. Enter the 6-digit code displayed
4. Access should be granted

## Configuration

All settings are in `app.py`:
- Database name: `DATABASE = 'worksphere.db'`
- Secret key: `app.secret_key`
- Port: `app.run(port=5000)`

## No Additional Setup Required

The system is designed to work immediately with:
- No manual database setup
- No configuration files
- No environment variables
- No additional dependencies beyond Flask

Just run and use!

---
WorkSphere ERMA - Ready to Deploy

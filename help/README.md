# WorkSphere ERMA - Employee and Roster Management Application

## Complete System with Enhanced Features

WorkSphere ERMA is a comprehensive employee and roster management system for the hospitality industry, now featuring:

### Core Features
- User Management (Employee & Admin roles)
- Department Management
- Schedule Management
- Leave Request Management
- Profile Management

### NEW Enhanced Features
1. **Multi-Factor Authentication (MFA)**
   - OTP verification for enhanced security
   - Toggle MFA on/off for individual users
   - 6-digit verification codes with 5-minute expiration

2. **Training Module**
   - Course creation and management
   - Assignment tracking
   - Completion monitoring
   - Progress reporting
   - Category-based organization

3. **Support Ticket System**
   - Priority-based ticketing
   - Category management
   - Assignment workflow
   - Conversation threading
   - Status tracking (Open/In Progress/Closed)

4. **Employee ChatHub**
   - Real-time internal messaging
   - One-on-one conversations
   - Unread message indicators
   - Auto-refresh functionality
   - User availability status

5. **Payslip Management**
   - Secure payslip generation
   - Gross pay and deductions tracking
   - Payment history
   - Period-based organization
   - Employee self-service access

## System Requirements

- Python 3.7 or higher
- Flask
- SQLite
- Modern web browser (Chrome, Firefox, Edge, Safari)

## Quick Start

### Windows:
1. Double-click `start.bat`
2. Open browser to http://localhost:5000

### Mac/Linux:
1. Run `./start.sh`
2. Open browser to http://localhost:5000

## Login Credentials

### Admin Access:
- Username: admin
- Password: admin123

### Employee Access:
- Username: john.doe
- Password: password123

Additional employees: jane.smith, mike.wilson, sarah.johnson, david.brown (all use password123)

## Features Overview

### For Employees:
- View personal schedules
- Submit leave requests
- Complete assigned training
- Create support tickets
- Chat with colleagues
- Access payslips
- Update profile information

### For Administrators:
- Manage all users and departments
- Create and assign schedules
- Review and approve leave requests
- Assign training courses
- Handle support tickets
- Generate payslips
- View reports and analytics
- Access audit logs
- Configure system settings
- Enable/disable MFA for users

## Database

The system automatically creates and initializes `worksphere.db` with:
- 1 admin user
- 5 employee users
- 5 departments
- 5 training courses
- Sample schedules for the next 7 days

## File Structure

```
WorkSphere_ERMA/
├── app.py                 # Main Flask application
├── worksphere.db          # SQLite database (auto-created)
├── templates/             # HTML templates
│   ├── login.html
│   ├── verify_mfa.html
│   ├── employee_*.html    # Employee pages
│   └── admin_*.html       # Admin pages
├── static/
│   ├── css/
│   │   └── style.css      # Dark elegant theme
│   └── images/
│       └── logo.png       # System logo
├── start.bat              # Windows startup
├── start.sh               # Unix startup
└── README.md              # This file
```

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control
- MFA support with OTP codes
- CSRF protection via Flask
- SQL injection prevention

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Port Configuration

Default port: 5000
To change: Edit `app.run(port=5000)` in app.py

## Troubleshooting

**Cannot start server:**
- Ensure Python 3.7+ is installed
- Run `pip install flask`
- Check if port 5000 is available

**Database errors:**
- Delete worksphere.db and restart
- System will recreate database automatically

**Login issues:**
- Use correct credentials (see above)
- Clear browser cache and cookies

## Support

For issues or questions, contact your system administrator.

## Version

WorkSphere ERMA v2.0 - Enhanced Edition with MFA, Training, Support, Chat, and Payslip features

---
Developed for the hospitality industry

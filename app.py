from flask import Flask, render_template, request, redirect, session, flash, send_file, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import sqlite3
import os
from datetime import datetime, timedelta
import secrets
import random
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()  # loads your .env file
print("MAIL USER:", os.getenv('MAIL_USERNAME'))  # should print your Gmail

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'worksphere_fallback_key')

# ── Upload Configuration ─────────────────────────────────────
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'mp4', 'mov', 'avi', 'mkv', 'webm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload size (for videos)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ── Mail Configuration ──────────────────────────────────────
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('WorkSphere ERMA', os.getenv('MAIL_USERNAME'))

mail = Mail(app)
def send_otp_email(recipient_email, otp_code, recipient_name="User"):
    try:
        msg = Message(
            subject="WorkSphere ERMA - Your Verification Code",
            sender=('WorkSphere ERMA', app.config['MAIL_USERNAME']),
            recipients=[recipient_email]
        )
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; 
                    background: #1a1a2e; color: #ffffff; padding: 30px; border-radius: 10px;">
            <h2 style="color: #4f8ef7; margin-bottom: 5px;">WorkSphere ERMA</h2>
            <hr style="border-color: #4f8ef7; margin-bottom: 20px;">
            <p>Hello <strong>{recipient_name}</strong>,</p>
            <p>Your one-time verification code is:</p>
            <div style="background: #2a2a4a; padding: 20px; text-align: center; 
                        border-radius: 8px; margin: 20px 0;">
                <span style="font-size: 36px; font-weight: bold; 
                             color: #4f8ef7; letter-spacing: 8px;">{otp_code}</span>
            </div>
            <p>This code expires in <strong>10 minutes</strong>.</p>
            <p style="color: #aaaaaa; font-size: 12px;">
                Do not share this code with anyone. WorkSphere staff will never ask for your OTP.
            </p>
        </div>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False
DATABASE = 'worksphere.db'

from flask import g

def get_db():
    """Return a per-request database connection, creating it if needed."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            timeout=20,                   # wait up to 20s if locked
            check_same_thread=False
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")    # WAL allows concurrent reads
        g.db.execute("PRAGMA busy_timeout=20000")  # 20s busy timeout at SQLite level
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Automatically close DB connection at the end of every request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Audit log helper
def log_action(action, details=None):
    """Record an action to the audit log."""
    try:
        user_id = session.get('user_id')
        ip_address = request.remote_addr
        conn = get_db()
        conn.execute(
            'INSERT INTO audit_logs (user_id, action, details, ip_address) VALUES (?, ?, ?, ?)',
            (user_id, action, details, ip_address)
        )
        conn.commit()
    except Exception as e:
        print(f"[AUDIT LOG ERROR] {e}")

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect('/login')
        if session.get('actual_role') != 'admin':
            flash('Admin access required', 'error')
            return redirect('/employee/dashboard')
        return f(*args, **kwargs)
    return decorated_function

# Employee required decorator
def employee_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect('/login')
        # Admins who switched to employee view are allowed through
        if session.get('actual_role') == 'admin' and session.get('role') == 'employee':
            return f(*args, **kwargs)
        # Regular employees are allowed through
        if session.get('role') == 'employee':
            return f(*args, **kwargs)
        # Admins still in admin view should not access employee routes
        flash('Employee access required', 'error')
        return redirect('/admin/dashboard')
    return decorated_function

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE, timeout=20)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL,
            department_id INTEGER,
            phone TEXT,
            address TEXT,
            hire_date TEXT,
            status TEXT DEFAULT 'active',
            mfa_enabled INTEGER DEFAULT 0,
            mfa_secret TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Departments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            manager_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Schedules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            shift_date TEXT NOT NULL,
            shift_start TEXT NOT NULL,
            shift_end TEXT NOT NULL,
            position TEXT,
            notes TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Leave requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            leave_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            reviewed_by INTEGER,
            reviewed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Audit logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            ip_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # MFA codes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mfa_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Training courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            duration_hours INTEGER,
            category TEXT,
            status TEXT DEFAULT 'active',
            material_filename TEXT,
            material_filepath TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Training assignments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            assigned_by INTEGER,
            assigned_date TEXT,
            due_date TEXT,
            completion_date TEXT,
            status TEXT DEFAULT 'assigned',
            score INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES training_courses (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Support tickets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT DEFAULT 'medium',
            description TEXT,
            status TEXT DEFAULT 'open',
            assigned_to INTEGER,
            resolution TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            closed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Ticket responses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ticket_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            is_internal INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES support_tickets (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Chat messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            recipient_id INTEGER,
            message TEXT NOT NULL,
            is_group INTEGER DEFAULT 0,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users (id),
            FOREIGN KEY (recipient_id) REFERENCES users (id)
        )
    ''')
    
    # Payslips table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payslips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            pay_period TEXT NOT NULL,
            gross_pay REAL NOT NULL,
            deductions REAL DEFAULT 0,
            net_pay REAL NOT NULL,
            payment_date TEXT,
            status TEXT DEFAULT 'generated',
            file_path TEXT,
            file_name TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # ── Run migrations for existing databases ──────────────────
    migrate_db(cursor)

    # Insert sample departments
    departments = [
        ('Front Desk', 'Guest reception and check-in services'),
        ('Housekeeping', 'Room cleaning and maintenance'),
        ('Food & Beverage', 'Restaurant and bar services'),
        ('Kitchen', 'Food preparation and culinary services'),
        ('Management', 'Administrative and leadership roles')
    ]
    
    for dept in departments:
        cursor.execute('INSERT OR IGNORE INTO departments (name, description) VALUES (?, ?)', dept)
    
    # Insert admin user
    admin_hash = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password, role, full_name, department_id, phone, hire_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('admin', 'admin@worksphere.com', admin_hash, 'admin', 'System Administrator', 5, '+1-555-0100', '2024-01-01'))
    
    # Insert sample employees
    employees = [
        ('john.doe', 'john.doe@worksphere.com', 'password123', 'employee', 'John Doe', 1, '+1-555-0101', '123 Main St', '2024-01-15'),
        ('jane.smith', 'jane.smith@worksphere.com', 'password123', 'employee', 'Jane Smith', 2, '+1-555-0102', '456 Oak Ave', '2024-02-01'),
        ('mike.wilson', 'mike.wilson@worksphere.com', 'password123', 'employee', 'Mike Wilson', 3, '+1-555-0103', '789 Pine Rd', '2024-01-20'),
        ('sarah.johnson', 'sarah.johnson@worksphere.com', 'password123', 'employee', 'Sarah Johnson', 4, '+1-555-0104', '321 Elm St', '2024-03-01'),
        ('david.brown', 'david.brown@worksphere.com', 'password123', 'employee', 'David Brown', 1, '+1-555-0105', '654 Maple Dr', '2024-02-15')
    ]
    
    for emp in employees:
        emp_hash = generate_password_hash(emp[2])
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password, role, full_name, department_id, phone, address, hire_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (emp[0], emp[1], emp_hash, emp[3], emp[4], emp[5], emp[6], emp[7], emp[8]))
    
    # Insert sample training courses
    courses = [
        ('Customer Service Excellence', 'Advanced customer service techniques and best practices', 8, 'Customer Service'),
        ('Food Safety & Hygiene', 'Essential food safety protocols and hygiene standards', 4, 'Safety'),
        ('Emergency Response Training', 'Emergency procedures and first aid basics', 6, 'Safety'),
        ('Hotel Management Systems', 'Training on property management software', 12, 'Technology'),
        ('Team Leadership Skills', 'Leadership and team management fundamentals', 16, 'Management')
    ]
    
    for course in courses:
        cursor.execute('''
            INSERT OR IGNORE INTO training_courses (title, description, duration_hours, category, created_by)
            VALUES (?, ?, ?, ?, 1)
        ''', course)
    
    # Insert sample schedules
    today = datetime.now()
    for i in range(7):
        shift_date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
        for user_id in range(2, 7):
            cursor.execute('''
                INSERT OR IGNORE INTO schedules (user_id, shift_date, shift_start, shift_end, position, created_by)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, shift_date, '09:00', '17:00', 'Staff', 1))
    
    conn.commit()
    conn.close()

    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def migrate_db(cursor):
    """Add new columns to existing databases without destroying data."""
    migrations = [
        ("training_courses", "material_filename", "TEXT"),
        ("training_courses", "material_filepath", "TEXT"),
        ("payslips", "file_name", "TEXT"),
    ]
    for table, column, col_type in migrations:
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
        except Exception:
            pass  # Column already exists — safe to ignore


# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        if session['role'] == 'admin':
            return redirect('/admin/dashboard')
        else:
            return redirect('/employee/dashboard')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        cursor = conn.cursor()
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND status = "active"', (username,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            # Check if MFA is enabled
            if user['mfa_enabled']:
                session['temp_user_id'] = user['id']
                session['temp_role'] = user['role']
                session['temp_username'] = user['username']
                
                # Generate OTP
                otp = str(random.randint(100000, 999999))
                expires_at = datetime.now() + timedelta(minutes=5)
                
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO mfa_codes (user_id, code, expires_at) VALUES (?, ?, ?)',
                             (user['id'], otp, expires_at))
                conn.commit()
                
                # Get user's email and send OTP
                email_sent = send_otp_email(user['email'], otp, user['username'])

                if email_sent:
                    flash('A verification code has been sent to your registered email address.', 'info')
                else:
                    flash(f'Could not send email. Temporary code: {otp}', 'warning')
                return redirect('/verify-mfa')
            else:
                session['user_id'] = user['id']
                session['actual_role'] = user['role']
                session['role'] = user['role']
                session['username'] = user['username']
                log_action('login', f"User '{user['username']}' logged in")
                
                if user['role'] == 'admin':
                    return redirect('/admin/dashboard')
                else:
                    return redirect('/employee/dashboard')
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/verify-mfa', methods=['GET', 'POST'])
def verify_mfa():
    if 'temp_user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        code = request.form.get('code')
        
        conn = get_db()
        cursor = conn.cursor()
        mfa_record = cursor.execute('''
            SELECT * FROM mfa_codes 
            WHERE user_id = ? AND code = ? AND used = 0 AND expires_at > ?
            ORDER BY created_at DESC LIMIT 1
        ''', (session['temp_user_id'], code, datetime.now())).fetchone()
        
        if mfa_record:
            cursor.execute('UPDATE mfa_codes SET used = 1 WHERE id = ?', (mfa_record['id'],))
            conn.commit()
            
            session['user_id'] = session.pop('temp_user_id')
            session['actual_role'] = session.pop('temp_role')
            session['role'] = session['actual_role']
            session['username'] = session.pop('temp_username')
            log_action('login', f"User '{session['username']}' logged in via MFA")
            
            if session['role'] == 'admin':
                return redirect('/admin/dashboard')
            else:
                return redirect('/employee/dashboard')
        else:
            flash('Invalid or expired MFA code', 'error')
    
    return render_template('verify_mfa.html')

@app.route('/logout')
def logout():
    log_action('logout', f"User '{session.get('username')}' logged out")
    session.clear()
    flash('You have been logged out', 'success')
    return redirect('/login')

@app.route('/switch-view')
def switch_view():
    """Toggle between admin and employee view for admin-role users only."""
    if 'user_id' not in session or session.get('actual_role') != 'admin':
        flash('Access denied', 'error')
        return redirect('/login')
    if session.get('role') == 'admin':
        session['role'] = 'employee'
        log_action('switch_view', "Switched to Employee View")
        flash('Switched to Employee View', 'info')
        return redirect('/employee/dashboard')
    else:
        session['role'] = 'admin'
        log_action('switch_view', "Switched to Admin View")
        flash('Switched to Admin View', 'info')
        return redirect('/admin/dashboard')

@app.route('/admin/switch-to-employee')
@admin_required
def switch_to_employee_view():
    session['viewing_as_employee'] = True
    flash('Switched to Employee View. Use the banner at the top to return to Admin Panel.', 'info')
    return redirect('/employee/dashboard')

@app.route('/switch-to-admin')
def switch_to_admin_view():
    if session.get('role') != 'admin':
        return redirect('/login')
    session.pop('viewing_as_employee', None)
    flash('Switched back to Admin Panel.', 'success')
    return redirect('/admin/dashboard')

# Employee routes
@app.route('/employee/dashboard')
@employee_required
def employee_dashboard():
    conn = get_db()
    cursor = conn.cursor()
    
    user_id = session['user_id']
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get today's schedule
    schedule = cursor.execute('''
        SELECT * FROM schedules WHERE user_id = ? AND shift_date = ?
    ''', (user_id, today)).fetchone()
    
    # Get pending leave requests
    pending_leaves = cursor.execute('''
        SELECT COUNT(*) as count FROM leave_requests WHERE user_id = ? AND status = 'pending'
    ''', (user_id,)).fetchone()['count']
    
    # Get upcoming training
    upcoming_training = cursor.execute('''
        SELECT COUNT(*) as count FROM training_assignments 
        WHERE user_id = ? AND status = 'assigned'
    ''', (user_id,)).fetchone()['count']
    
    # Get open tickets
    open_tickets = cursor.execute('''
        SELECT COUNT(*) as count FROM support_tickets 
        WHERE user_id = ? AND status != 'closed'
    ''', (user_id,)).fetchone()['count']
    
    # Get unread messages
    unread_messages = cursor.execute('''
        SELECT COUNT(*) as count FROM chat_messages 
        WHERE recipient_id = ? AND is_read = 0
    ''', (user_id,)).fetchone()['count']
    
    return render_template('employee_dashboard.html', 
                         schedule=schedule,
                         pending_leaves=pending_leaves,
                         upcoming_training=upcoming_training,
                         open_tickets=open_tickets,
                         unread_messages=unread_messages)

@app.route('/employee/schedule')
@employee_required
def employee_schedule():
    conn = get_db()
    cursor = conn.cursor()
    
    user_id = session['user_id']
    schedules = cursor.execute('''
        SELECT * FROM schedules WHERE user_id = ? ORDER BY shift_date DESC
    ''', (user_id,)).fetchall()
    return render_template('employee_schedule.html', schedules=schedules)

@app.route('/employee/leave', methods=['GET', 'POST'])
@employee_required
def employee_leave():
    if request.method == 'POST':
        user_id = session['user_id']
        leave_type = request.form.get('leave_type')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        reason = request.form.get('reason')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO leave_requests (user_id, leave_type, start_date, end_date, reason)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, leave_type, start_date, end_date, reason))
        conn.commit()
        
        flash('Leave request submitted successfully', 'success')
        log_action('leave_request_submitted', f"Leave type: {leave_type}, {start_date} to {end_date}")
        return redirect('/employee/leave')
    
    conn = get_db()
    cursor = conn.cursor()
    user_id = session['user_id']
    
    leave_requests = cursor.execute('''
        SELECT * FROM leave_requests WHERE user_id = ? ORDER BY created_at DESC
    ''', (user_id,)).fetchall()
    return render_template('employee_leave.html', leave_requests=leave_requests)

@app.route('/employee/profile', methods=['GET', 'POST'])
@employee_required
def employee_profile():
    user_id = session['user_id']
    
    if request.method == 'POST':
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET phone = ?, address = ? WHERE id = ?', (phone, address, user_id))
        conn.commit()
        
        flash('Profile updated successfully', 'success')
        log_action('profile_updated', "Employee updated their contact details")
        return redirect('/employee/profile')
    
    conn = get_db()
    cursor = conn.cursor()
    
    user = cursor.execute('''
        SELECT u.*, d.name as department_name 
        FROM users u 
        LEFT JOIN departments d ON u.department_id = d.id 
        WHERE u.id = ?
    ''', (user_id,)).fetchone()
    return render_template('employee_profile.html', user=user)

@app.route('/employee/training')
@employee_required
def employee_training():
    conn = get_db()
    cursor = conn.cursor()
    user_id = session['user_id']
    
    assignments = cursor.execute('''
        SELECT ta.*, tc.title, tc.description, tc.duration_hours, tc.category,
               tc.material_filename,
               u.full_name as assigned_by_name
        FROM training_assignments ta
        JOIN training_courses tc ON ta.course_id = tc.id
        LEFT JOIN users u ON ta.assigned_by = u.id
        WHERE ta.user_id = ?
        ORDER BY ta.created_at DESC
    ''', (user_id,)).fetchall()
    return render_template('employee_training.html', assignments=assignments)

@app.route('/employee/training/complete/<int:assignment_id>', methods=['POST'])
@employee_required
def complete_training(assignment_id):
    user_id = session['user_id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Verify this assignment belongs to the user
    assignment = cursor.execute('SELECT * FROM training_assignments WHERE id = ? AND user_id = ?',
                               (assignment_id, user_id)).fetchone()
    
    if assignment:
        cursor.execute('''
            UPDATE training_assignments 
            SET status = 'completed', completion_date = ?, score = 100
            WHERE id = ?
        ''', (datetime.now().strftime('%Y-%m-%d'), assignment_id))
        conn.commit()
        flash('Training marked as completed', 'success')
        log_action('training_completed', f"Completed training assignment ID {assignment_id}")
    return redirect('/employee/training')

@app.route('/employee/support', methods=['GET', 'POST'])
@employee_required
def employee_support():
    if request.method == 'POST':
        user_id = session['user_id']
        subject = request.form.get('subject')
        category = request.form.get('category')
        priority = request.form.get('priority')
        description = request.form.get('description')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO support_tickets (user_id, subject, category, priority, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, subject, category, priority, description))
        ticket_id = cursor.lastrowid
        conn.commit()
        
        flash('Support ticket created successfully', 'success')
        log_action('ticket_created', f"Created ticket #{ticket_id}: {subject}")
        return redirect(f'/employee/support/view/{ticket_id}')
    
    conn = get_db()
    cursor = conn.cursor()
    user_id = session['user_id']
    
    tickets = cursor.execute('''
        SELECT * FROM support_tickets WHERE user_id = ? ORDER BY created_at DESC
    ''', (user_id,)).fetchall()
    return render_template('employee_support.html', tickets=tickets)

@app.route('/employee/support/view/<int:ticket_id>', methods=['GET', 'POST'])
@employee_required
def view_support_ticket(ticket_id):
    user_id = session['user_id']
    
    if request.method == 'POST':
        message = request.form.get('message')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ticket_responses (ticket_id, user_id, message)
            VALUES (?, ?, ?)
        ''', (ticket_id, user_id, message))
        cursor.execute('UPDATE support_tickets SET updated_at = ? WHERE id = ?',
                      (datetime.now(), ticket_id))
        conn.commit()
        
        flash('Response added successfully', 'success')
        return redirect(f'/employee/support/view/{ticket_id}')
    
    conn = get_db()
    cursor = conn.cursor()
    
    ticket = cursor.execute('''
        SELECT st.*, u.full_name as creator_name, a.full_name as assigned_name
        FROM support_tickets st
        JOIN users u ON st.user_id = u.id
        LEFT JOIN users a ON st.assigned_to = a.id
        WHERE st.id = ? AND st.user_id = ?
    ''', (ticket_id, user_id)).fetchone()
    
    if not ticket:
        flash('Ticket not found', 'error')
        return redirect('/employee/support')
    
    responses = cursor.execute('''
        SELECT tr.*, u.full_name as responder_name, u.role
        FROM ticket_responses tr
        JOIN users u ON tr.user_id = u.id
        WHERE tr.ticket_id = ?
        ORDER BY tr.created_at ASC
    ''', (ticket_id,)).fetchall()
    return render_template('employee_support_view.html', ticket=ticket, responses=responses)

@app.route('/employee/chat')
@employee_required
def employee_chat():
    conn = get_db()
    cursor = conn.cursor()
    user_id = session['user_id']
    
    # Get all users except current user
    users = cursor.execute('''
        SELECT id, full_name, role, department_id FROM users 
        WHERE id != ? AND status = 'active'
        ORDER BY full_name
    ''', (user_id,)).fetchall()
    
    # Get recent conversations - SQLite compatible version
    conversations = []
    
    # Get all unique users this person has chatted with
    cursor.execute('''
        SELECT DISTINCT 
            CASE 
                WHEN sender_id = ? THEN recipient_id 
                ELSE sender_id 
            END as other_id
        FROM chat_messages
        WHERE sender_id = ? OR recipient_id = ?
    ''', (user_id, user_id, user_id))
    
    chat_partners = cursor.fetchall()
    
    # For each chat partner, get their details and last message
    for partner in chat_partners:
        other_id = partner[0]
        
        # Get user details
        user_details = cursor.execute('''
            SELECT full_name, role FROM users WHERE id = ?
        ''', (other_id,)).fetchone()
        
        if not user_details:
            continue
        
        # Get last message
        last_msg = cursor.execute('''
            SELECT message, created_at FROM chat_messages 
            WHERE (sender_id = ? AND recipient_id = ?) 
               OR (sender_id = ? AND recipient_id = ?)
            ORDER BY created_at DESC LIMIT 1
        ''', (user_id, other_id, other_id, user_id)).fetchone()
        
        # Get unread count
        unread = cursor.execute('''
            SELECT COUNT(*) FROM chat_messages 
            WHERE sender_id = ? AND recipient_id = ? AND is_read = 0
        ''', (other_id, user_id)).fetchone()[0]
        
        conversations.append({
            'other_user_id': other_id,
            'full_name': user_details[0],
            'role': user_details[1],
            'last_message': last_msg[0] if last_msg else 'No messages yet',
            'unread_count': unread,
            'last_time': last_msg[1] if last_msg else ''
        })
    
    # Sort by last message time
    conversations.sort(key=lambda x: x.get('last_time', ''), reverse=True)
    return render_template('employee_chat.html', users=users, conversations=conversations)

@app.route('/employee/chat/messages/<int:other_user_id>')
@employee_required
def get_chat_messages(other_user_id):
    conn = get_db()
    cursor = conn.cursor()
    user_id = session['user_id']
    
    # Mark messages as read
    cursor.execute('''
        UPDATE chat_messages SET is_read = 1 
        WHERE sender_id = ? AND recipient_id = ?
    ''', (other_user_id, user_id))
    conn.commit()
    
    # Get messages
    messages = cursor.execute('''
        SELECT cm.*, u.full_name as sender_name
        FROM chat_messages cm
        JOIN users u ON cm.sender_id = u.id
        WHERE (sender_id = ? AND recipient_id = ?) 
           OR (sender_id = ? AND recipient_id = ?)
        ORDER BY created_at ASC
    ''', (user_id, other_user_id, other_user_id, user_id)).fetchall()
    
    messages_list = []
    for msg in messages:
        messages_list.append({
            'id': msg['id'],
            'sender_id': msg['sender_id'],
            'sender_name': msg['sender_name'],
            'message': msg['message'],
            'created_at': msg['created_at'],
            'is_own': msg['sender_id'] == user_id
        })
    
    return jsonify(messages_list)

@app.route('/employee/chat/send', methods=['POST'])
@employee_required
def send_chat_message():
    user_id = session['user_id']
    recipient_id = request.form.get('recipient_id')
    message = request.form.get('message')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_messages (sender_id, recipient_id, message)
        VALUES (?, ?, ?)
    ''', (user_id, recipient_id, message))
    conn.commit()
    
    return jsonify({'success': True})

@app.route('/employee/payslips')
@employee_required
def employee_payslips():
    conn = get_db()
    cursor = conn.cursor()
    user_id = session['user_id']
    
    payslips = cursor.execute('''
        SELECT * FROM payslips WHERE user_id = ? ORDER BY created_at DESC
    ''', (user_id,)).fetchall()
    return render_template('employee_payslips.html', payslips=payslips)

# ── File Download Routes ─────────────────────────────────────

@app.route('/admin/download/payslip/<int:payslip_id>')
@admin_required
def download_payslip_admin(payslip_id):
    conn = get_db()
    cursor = conn.cursor()
    payslip = cursor.execute('SELECT * FROM payslips WHERE id = ?', (payslip_id,)).fetchone()
    if payslip and payslip['file_path'] and os.path.exists(payslip['file_path']):
        return send_file(payslip['file_path'], as_attachment=True,
                         download_name=payslip['file_name'] or 'payslip.pdf')
    flash('File not found', 'error')
    return redirect('/admin/payslips')

@app.route('/employee/download/payslip/<int:payslip_id>')
@employee_required
def download_payslip_employee(payslip_id):
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    payslip = cursor.execute('SELECT * FROM payslips WHERE id = ? AND user_id = ?',
                             (payslip_id, user_id)).fetchone()
    if payslip and payslip['file_path'] and os.path.exists(payslip['file_path']):
        return send_file(payslip['file_path'], as_attachment=True,
                         download_name=payslip['file_name'] or 'payslip.pdf')
    flash('File not found', 'error')
    return redirect('/employee/payslips')

@app.route('/admin/download/training/<int:course_id>')
@admin_required
def download_training_material_admin(course_id):
    conn = get_db()
    cursor = conn.cursor()
    course = cursor.execute('SELECT * FROM training_courses WHERE id = ?', (course_id,)).fetchone()
    if course and course['material_filepath'] and os.path.exists(course['material_filepath']):
        return send_file(course['material_filepath'], as_attachment=True,
                         download_name=course['material_filename'] or 'material.pdf')
    flash('File not found', 'error')
    return redirect('/admin/training')

@app.route('/employee/download/training/<int:course_id>')
@employee_required
def download_training_material_employee(course_id):
    conn = get_db()
    cursor = conn.cursor()
    course = cursor.execute('SELECT * FROM training_courses WHERE id = ?', (course_id,)).fetchone()
    if course and course['material_filepath'] and os.path.exists(course['material_filepath']):
        filename = course['material_filename'] or 'material'
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        # Stream videos inline so the browser can play them; download everything else
        is_video = ext in {'mp4', 'mov', 'avi', 'mkv', 'webm'}
        return send_file(course['material_filepath'],
                         as_attachment=not is_video,
                         download_name=filename)
    flash('File not found', 'error')
    return redirect('/employee/training')

# Admin routes
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db()
    cursor = conn.cursor()
    
    stats = {
        'total_users': cursor.execute('SELECT COUNT(*) as count FROM users WHERE role = "employee"').fetchone()['count'],
        'total_departments': cursor.execute('SELECT COUNT(*) as count FROM departments').fetchone()['count'],
        'pending_leaves': cursor.execute('SELECT COUNT(*) as count FROM leave_requests WHERE status = "pending"').fetchone()['count'],
        'active_schedules': cursor.execute('SELECT COUNT(*) as count FROM schedules WHERE shift_date >= date("now")').fetchone()['count'],
        'open_tickets': cursor.execute('SELECT COUNT(*) as count FROM support_tickets WHERE status != "closed"').fetchone()['count'],
        'active_training': cursor.execute('SELECT COUNT(*) as count FROM training_assignments WHERE status = "assigned"').fetchone()['count']
    }
    
    # Recent activity
    recent_leaves = cursor.execute('''
        SELECT lr.*, u.full_name 
        FROM leave_requests lr 
        JOIN users u ON lr.user_id = u.id 
        ORDER BY lr.created_at DESC LIMIT 5
    ''').fetchall()
    
    recent_tickets = cursor.execute('''
        SELECT st.*, u.full_name 
        FROM support_tickets st 
        JOIN users u ON st.user_id = u.id 
        ORDER BY st.created_at DESC LIMIT 5
    ''').fetchall()
    return render_template('admin_dashboard.html', stats=stats, recent_leaves=recent_leaves, recent_tickets=recent_tickets)

@app.route('/admin/users')
@admin_required
def admin_users():
    conn = get_db()
    cursor = conn.cursor()
    
    users = cursor.execute('''
        SELECT u.*, d.name as department_name 
        FROM users u 
        LEFT JOIN departments d ON u.department_id = d.id 
        WHERE u.role = "employee"
        ORDER BY u.full_name
    ''').fetchall()
    
    departments = cursor.execute('SELECT * FROM departments ORDER BY name').fetchall()
    return render_template('admin_users.html', users=users, departments=departments)

@app.route('/admin/users/add', methods=['POST'])
@admin_required
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    full_name = request.form.get('full_name')
    department_id = request.form.get('department_id')
    phone = request.form.get('phone')
    address = request.form.get('address')
    
    hashed_password = generate_password_hash(password)
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password, role, full_name, department_id, phone, address, hire_date)
            VALUES (?, ?, ?, 'employee', ?, ?, ?, ?, ?)
        ''', (username, email, hashed_password, full_name, department_id, phone, address, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
        
        flash('User added successfully', 'success')
        log_action('user_added', f"Added new employee: {username} ({full_name})")
    except sqlite3.IntegrityError:
        flash('Username or email already exists', 'error')
    
    return redirect('/admin/users')

@app.route('/admin/users/edit/<int:user_id>', methods=['POST'])
@admin_required
def edit_user(user_id):
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    department_id = request.form.get('department_id')
    phone = request.form.get('phone')
    address = request.form.get('address')
    status = request.form.get('status')
    role = request.form.get('role', 'employee')

    # Validate role value to prevent arbitrary values being saved
    if role not in ('admin', 'employee'):
        role = 'employee'

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET full_name = ?, email = ?, department_id = ?, phone = ?, address = ?, status = ?, role = ?
        WHERE id = ?
    ''', (full_name, email, department_id, phone, address, status, role, user_id))
    conn.commit()
    
    flash('User updated successfully', 'success')
    log_action('user_updated', f"Updated user ID {user_id}: name={full_name}, role={role}, status={status}")
    return redirect('/admin/users')

@app.route('/admin/users/toggle-mfa/<int:user_id>', methods=['POST'])
@admin_required
def toggle_mfa(user_id):
    conn = get_db()
    cursor = conn.cursor()
    
    user = cursor.execute('SELECT mfa_enabled FROM users WHERE id = ?', (user_id,)).fetchone()
    new_status = 0 if user['mfa_enabled'] else 1
    
    cursor.execute('UPDATE users SET mfa_enabled = ? WHERE id = ?', (new_status, user_id))
    conn.commit()
    
    flash(f'MFA {"enabled" if new_status else "disabled"} successfully', 'success')
    log_action('mfa_toggled', f"MFA {'enabled' if new_status else 'disabled'} for user ID {user_id}")
    return redirect('/admin/users')

@app.route('/admin/departments')
@admin_required
def admin_departments():
    conn = get_db()
    cursor = conn.cursor()
    
    departments = cursor.execute('''
        SELECT d.*, u.full_name as manager_name,
               (SELECT COUNT(*) FROM users WHERE department_id = d.id) as employee_count
        FROM departments d
        LEFT JOIN users u ON d.manager_id = u.id
        ORDER BY d.name
    ''').fetchall()
    
    users = cursor.execute('SELECT id, full_name FROM users WHERE role = "employee" ORDER BY full_name').fetchall()
    return render_template('admin_departments.html', departments=departments, users=users)

@app.route('/admin/departments/add', methods=['POST'])
@admin_required
def add_department():
    name = request.form.get('name')
    description = request.form.get('description')
    manager_id = request.form.get('manager_id')
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO departments (name, description, manager_id) VALUES (?, ?, ?)',
                      (name, description, manager_id if manager_id else None))
        conn.commit()
        
        flash('Department added successfully', 'success')
        log_action('department_added', f"Added department: {name}")
    except sqlite3.IntegrityError:
        flash('Department name already exists', 'error')
    
    return redirect('/admin/departments')

@app.route('/admin/departments/edit/<int:dept_id>', methods=['POST'])
@admin_required
def edit_department(dept_id):
    name = request.form.get('name')
    description = request.form.get('description')
    manager_id = request.form.get('manager_id')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE departments SET name = ?, description = ?, manager_id = ? WHERE id = ?',
                  (name, description, manager_id if manager_id else None, dept_id))
    conn.commit()
    
    flash('Department updated successfully', 'success')
    log_action('department_updated', f"Updated department ID {dept_id}: {name}")
    return redirect('/admin/departments')

@app.route('/admin/schedules')
@admin_required
def admin_schedules():
    conn = get_db()
    cursor = conn.cursor()
    
    schedules = cursor.execute('''
        SELECT s.*, u.full_name, d.name as department_name
        FROM schedules s
        JOIN users u ON s.user_id = u.id
        LEFT JOIN departments d ON u.department_id = d.id
        ORDER BY s.shift_date DESC, s.shift_start
    ''').fetchall()
    
    users = cursor.execute('SELECT id, full_name FROM users WHERE role = "employee" AND status = "active" ORDER BY full_name').fetchall()
    return render_template('admin_schedules.html', schedules=schedules, users=users)

@app.route('/admin/schedules/add', methods=['POST'])
@admin_required
def add_schedule():
    user_id = request.form.get('user_id')
    shift_date = request.form.get('shift_date')
    shift_start = request.form.get('shift_start')
    shift_end = request.form.get('shift_end')
    position = request.form.get('position')
    notes = request.form.get('notes')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO schedules (user_id, shift_date, shift_start, shift_end, position, notes, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, shift_date, shift_start, shift_end, position, notes, session['user_id']))
    conn.commit()
    
    flash('Schedule added successfully', 'success')
    log_action('schedule_added', f"Added schedule for user ID {user_id} on {shift_date} ({shift_start}-{shift_end})")
    return redirect('/admin/schedules')

@app.route('/admin/schedules/delete/<int:schedule_id>', methods=['POST'])
@admin_required
def delete_schedule(schedule_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM schedules WHERE id = ?', (schedule_id,))
    conn.commit()
    
    flash('Schedule deleted successfully', 'success')
    log_action('schedule_deleted', f"Deleted schedule ID {schedule_id}")
    return redirect('/admin/schedules')

@app.route('/admin/leave-requests')
@admin_required
def admin_leave_requests():
    conn = get_db()
    cursor = conn.cursor()
    
    leave_requests = cursor.execute('''
        SELECT lr.*, u.full_name, d.name as department_name
        FROM leave_requests lr
        JOIN users u ON lr.user_id = u.id
        LEFT JOIN departments d ON u.department_id = d.id
        ORDER BY lr.created_at DESC
    ''').fetchall()
    return render_template('admin_leave_requests.html', leave_requests=leave_requests)

@app.route('/admin/leave-requests/update/<int:request_id>', methods=['POST'])
@admin_required
def update_leave_request(request_id):
    status = request.form.get('status')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE leave_requests 
        SET status = ?, reviewed_by = ?, reviewed_at = ?
        WHERE id = ?
    ''', (status, session['user_id'], datetime.now(), request_id))
    conn.commit()
    
    flash(f'Leave request {status}', 'success')
    log_action('leave_request_updated', f"Leave request ID {request_id} marked as {status}")
    return redirect('/admin/leave-requests')

@app.route('/admin/training')
@admin_required
def admin_training():
    conn = get_db()
    cursor = conn.cursor()
    
    courses = cursor.execute('SELECT * FROM training_courses ORDER BY created_at DESC').fetchall()
    return render_template('admin_training.html', courses=courses)

@app.route('/admin/training/add', methods=['POST'])
@admin_required
def add_training_course():
    title = request.form.get('title')
    description = request.form.get('description')
    duration_hours = request.form.get('duration_hours')
    category = request.form.get('category')

    material_filename = None
    material_filepath = None

    file = request.files.get('material_file')
    if file and file.filename and allowed_file(file.filename):
        material_filename = secure_filename(file.filename)
        # Prefix with timestamp to avoid collisions
        unique_name = f"training_{datetime.now().strftime('%Y%m%d%H%M%S')}_{material_filename}"
        material_filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(material_filepath)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO training_courses (title, description, duration_hours, category, material_filename, material_filepath, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, duration_hours, category, material_filename, material_filepath, session['user_id']))
    conn.commit()
    
    flash('Training course added successfully', 'success')
    log_action('training_course_added', f"Added course: {title} (category: {category})")
    return redirect('/admin/training')

@app.route('/admin/training/assign/<int:course_id>', methods=['GET', 'POST'])
@admin_required
def assign_training(course_id):
    if request.method == 'POST':
        user_ids = request.form.getlist('user_ids')
        due_date = request.form.get('due_date')
        
        conn = get_db()
        cursor = conn.cursor()
        
        for user_id in user_ids:
            cursor.execute('''
                INSERT INTO training_assignments (course_id, user_id, assigned_by, assigned_date, due_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (course_id, user_id, session['user_id'], datetime.now().strftime('%Y-%m-%d'), due_date))
        
        conn.commit()
        
        flash('Training assigned successfully', 'success')
        log_action('training_assigned', f"Assigned course ID {course_id} to {len(user_ids)} employee(s)")
        return redirect('/admin/training')
    
    conn = get_db()
    cursor = conn.cursor()
    
    course = cursor.execute('SELECT * FROM training_courses WHERE id = ?', (course_id,)).fetchone()
    users = cursor.execute('SELECT id, full_name, department_id FROM users WHERE role = "employee" AND status = "active" ORDER BY full_name').fetchall()
    return render_template('admin_training_assign.html', course=course, users=users)

@app.route('/admin/training/assignments')
@admin_required
def admin_training_assignments():
    conn = get_db()
    cursor = conn.cursor()
    
    assignments = cursor.execute('''
        SELECT ta.*, tc.title as course_title, u.full_name as employee_name, d.name as department_name
        FROM training_assignments ta
        JOIN training_courses tc ON ta.course_id = tc.id
        JOIN users u ON ta.user_id = u.id
        LEFT JOIN departments d ON u.department_id = d.id
        ORDER BY ta.created_at DESC
    ''').fetchall()
    return render_template('admin_training_assignments.html', assignments=assignments)

@app.route('/admin/support')
@admin_required
def admin_support():
    conn = get_db()
    cursor = conn.cursor()
    
    tickets = cursor.execute('''
        SELECT st.*, u.full_name as creator_name, a.full_name as assigned_name
        FROM support_tickets st
        JOIN users u ON st.user_id = u.id
        LEFT JOIN users a ON st.assigned_to = a.id
        ORDER BY st.created_at DESC
    ''').fetchall()
    
    users = cursor.execute('SELECT id, full_name FROM users WHERE role = "employee" AND status = "active" ORDER BY full_name').fetchall()
    return render_template('admin_support.html', tickets=tickets, users=users)

@app.route('/admin/support/view/<int:ticket_id>', methods=['GET', 'POST'])
@admin_required
def admin_view_ticket(ticket_id):
    if request.method == 'POST':
        action = request.form.get('action')
        
        conn = get_db()
        cursor = conn.cursor()
        
        if action == 'respond':
            message = request.form.get('message')
            cursor.execute('''
                INSERT INTO ticket_responses (ticket_id, user_id, message)
                VALUES (?, ?, ?)
            ''', (ticket_id, session['user_id'], message))
            cursor.execute('UPDATE support_tickets SET updated_at = ? WHERE id = ?',
                          (datetime.now(), ticket_id))
        
        elif action == 'assign':
            assigned_to = request.form.get('assigned_to')
            cursor.execute('UPDATE support_tickets SET assigned_to = ?, updated_at = ? WHERE id = ?',
                          (assigned_to, datetime.now(), ticket_id))
        
        elif action == 'close':
            resolution = request.form.get('resolution')
            cursor.execute('''
                UPDATE support_tickets 
                SET status = 'closed', resolution = ?, closed_at = ?, updated_at = ?
                WHERE id = ?
            ''', (resolution, datetime.now(), datetime.now(), ticket_id))
        
        elif action == 'reopen':
            cursor.execute('''
                UPDATE support_tickets 
                SET status = 'open', closed_at = NULL, updated_at = ?
                WHERE id = ?
            ''', (datetime.now(), ticket_id))
        
        conn.commit()
        
        flash('Ticket updated successfully', 'success')
        log_action('ticket_updated', f"Ticket ID {ticket_id} action: {action}")
        return redirect(f'/admin/support/view/{ticket_id}')
    
    conn = get_db()
    cursor = conn.cursor()
    
    ticket = cursor.execute('''
        SELECT st.*, u.full_name as creator_name, a.full_name as assigned_name
        FROM support_tickets st
        JOIN users u ON st.user_id = u.id
        LEFT JOIN users a ON st.assigned_to = a.id
        WHERE st.id = ?
    ''', (ticket_id,)).fetchone()
    
    if not ticket:
        flash('Ticket not found', 'error')
        return redirect('/admin/support')
    
    responses = cursor.execute('''
        SELECT tr.*, u.full_name as responder_name, u.role
        FROM ticket_responses tr
        JOIN users u ON tr.user_id = u.id
        WHERE tr.ticket_id = ?
        ORDER BY tr.created_at ASC
    ''', (ticket_id,)).fetchall()
    
    users = cursor.execute('SELECT id, full_name FROM users WHERE role = "employee" AND status = "active" ORDER BY full_name').fetchall()
    return render_template('admin_support_view.html', ticket=ticket, responses=responses, users=users)

@app.route('/admin/payslips')
@admin_required
def admin_payslips():
    conn = get_db()
    cursor = conn.cursor()
    
    payslips = cursor.execute('''
        SELECT p.*, u.full_name as employee_name, d.name as department_name
        FROM payslips p
        JOIN users u ON p.user_id = u.id
        LEFT JOIN departments d ON u.department_id = d.id
        ORDER BY p.created_at DESC
    ''').fetchall()
    
    users = cursor.execute('SELECT id, full_name FROM users WHERE role = "employee" AND status = "active" ORDER BY full_name').fetchall()
    return render_template('admin_payslips.html', payslips=payslips, users=users)

@app.route('/admin/payslips/generate', methods=['POST'])
@admin_required
def generate_payslip():
    user_id = request.form.get('user_id')
    pay_period = request.form.get('pay_period')
    gross_pay = request.form.get('gross_pay')
    deductions = request.form.get('deductions', 0)

    net_pay = float(gross_pay) - float(deductions)

    file_path = None
    file_name = None

    file = request.files.get('payslip_file')
    if file and file.filename and allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        unique_name = f"payslip_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_name}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(file_path)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO payslips (user_id, pay_period, gross_pay, deductions, net_pay, payment_date, file_path, file_name, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, pay_period, gross_pay, deductions, net_pay,
          datetime.now().strftime('%Y-%m-%d'), file_path, file_name, session['user_id']))
    conn.commit()
    
    flash('Payslip generated successfully', 'success')
    log_action('payslip_generated', f"Generated payslip for user ID {user_id}, period: {pay_period}, net: ${net_pay:.2f}")
    return redirect('/admin/payslips')

@app.route('/admin/reports')
@admin_required
def admin_reports():
    conn = get_db()
    cursor = conn.cursor()
    
    # Department statistics
    dept_stats = cursor.execute('''
        SELECT d.name, COUNT(u.id) as employee_count
        FROM departments d
        LEFT JOIN users u ON d.id = u.department_id AND u.role = 'employee'
        GROUP BY d.id, d.name
        ORDER BY employee_count DESC
    ''').fetchall()
    
    # Leave statistics
    leave_stats = cursor.execute('''
        SELECT status, COUNT(*) as count
        FROM leave_requests
        GROUP BY status
    ''').fetchall()
    
    # Training statistics
    training_stats = cursor.execute('''
        SELECT status, COUNT(*) as count
        FROM training_assignments
        GROUP BY status
    ''').fetchall()
    
    # Support ticket statistics
    ticket_stats = cursor.execute('''
        SELECT status, COUNT(*) as count
        FROM support_tickets
        GROUP BY status
    ''').fetchall()
    return render_template('admin_reports.html', 
                         dept_stats=dept_stats,
                         leave_stats=leave_stats,
                         training_stats=training_stats,
                         ticket_stats=ticket_stats)

@app.route('/admin/audit-logs')
@admin_required
def admin_audit_logs():
    conn = get_db()
    cursor = conn.cursor()
    
    logs = cursor.execute('''
        SELECT al.*, u.username
        FROM audit_logs al
        LEFT JOIN users u ON al.user_id = u.id
        ORDER BY al.created_at DESC
        LIMIT 100
    ''').fetchall()
    return render_template('admin_audit_logs.html', logs=logs)

@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    if request.method == 'POST':
        # Handle password change
        if 'current_password' in request.form:
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            conn = get_db()
            cursor = conn.cursor()
            user = cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
            
            if check_password_hash(user['password'], current_password):
                if new_password == confirm_password:
                    hashed_password = generate_password_hash(new_password)
                    cursor.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, session['user_id']))
                    conn.commit()
                    log_action('password_changed', "Admin changed their password")
                    flash('Password updated successfully', 'success')
                else:
                    flash('New passwords do not match', 'error')
            else:
                flash('Current password is incorrect', 'error')
        
        return redirect('/admin/settings')
    
    conn = get_db()
    cursor = conn.cursor()
    
    user = cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    return render_template('admin_settings.html', user=user)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    if not os.path.exists(DATABASE):
        init_db()
        print('Database initialized successfully!')
    else:
        # Run migrations on existing DB
        conn = sqlite3.connect(DATABASE, timeout=20)
        migrate_db(conn.cursor())
        conn.commit()
        conn.close()
    
    app.run(debug=True, host='0.0.0.0', port=5000)

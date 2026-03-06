#!/usr/bin/env python3
"""
WorkSphere ERMA - Database Reset Script
This script will delete the existing database and create a fresh one with all sample data.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

DATABASE = 'worksphere.db'

def reset_database():
    # Remove old database
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print(f"✓ Removed old database: {DATABASE}")
    
    # Create new connection
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    print(f"✓ Created new database: {DATABASE}")
    
    # Create all tables
    print("\nCreating tables...")
    
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
    print("  ✓ users")
    
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
    print("  ✓ departments")
    
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
    print("  ✓ schedules")
    
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
    print("  ✓ leave_requests")
    
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
    print("  ✓ audit_logs")
    
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
    print("  ✓ mfa_codes")
    
    # Training courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            duration_hours INTEGER,
            category TEXT,
            status TEXT DEFAULT 'active',
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("  ✓ training_courses")
    
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
    print("  ✓ training_assignments")
    
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
    print("  ✓ support_tickets")
    
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
    print("  ✓ ticket_responses")
    
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
    print("  ✓ chat_messages")
    
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
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    print("  ✓ payslips")
    
    # Insert sample departments
    print("\nInserting departments...")
    departments = [
        ('Front Desk', 'Guest reception and check-in services'),
        ('Housekeeping', 'Room cleaning and maintenance'),
        ('Food & Beverage', 'Restaurant and bar services'),
        ('Kitchen', 'Food preparation and culinary services'),
        ('Management', 'Administrative and leadership roles')
    ]
    
    for dept in departments:
        cursor.execute('INSERT INTO departments (name, description) VALUES (?, ?)', dept)
    print(f"  ✓ Added {len(departments)} departments")
    
    # Insert admin user
    print("\nCreating users...")
    admin_hash = generate_password_hash('admin123')
    cursor.execute('''
        INSERT INTO users (username, email, password, role, full_name, department_id, phone, hire_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('admin', 'admin@worksphere.com', admin_hash, 'admin', 'System Administrator', 5, '+1-555-0100', '2024-01-01', 'active'))
    print("  ✓ admin / admin123")
    
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
            INSERT INTO users (username, email, password, role, full_name, department_id, phone, address, hire_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (emp[0], emp[1], emp_hash, emp[3], emp[4], emp[5], emp[6], emp[7], emp[8], 'active'))
        print(f"  ✓ {emp[0]} / password123")
    
    # Insert sample training courses
    print("\nCreating training courses...")
    courses = [
        ('Customer Service Excellence', 'Advanced customer service techniques and best practices', 8, 'Customer Service'),
        ('Food Safety & Hygiene', 'Essential food safety protocols and hygiene standards', 4, 'Safety'),
        ('Emergency Response Training', 'Emergency procedures and first aid basics', 6, 'Safety'),
        ('Hotel Management Systems', 'Training on property management software', 12, 'Technology'),
        ('Team Leadership Skills', 'Leadership and team management fundamentals', 16, 'Management')
    ]
    
    for course in courses:
        cursor.execute('''
            INSERT INTO training_courses (title, description, duration_hours, category, created_by)
            VALUES (?, ?, ?, ?, 1)
        ''', course)
    print(f"  ✓ Added {len(courses)} training courses")
    
    # Insert sample schedules
    print("\nCreating schedules...")
    today = datetime.now()
    schedule_count = 0
    for i in range(7):
        shift_date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
        for user_id in range(2, 7):
            cursor.execute('''
                INSERT INTO schedules (user_id, shift_date, shift_start, shift_end, position, created_by)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, shift_date, '09:00', '17:00', 'Staff', 1))
            schedule_count += 1
    print(f"  ✓ Created {schedule_count} schedules for next 7 days")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ DATABASE RESET COMPLETE!")
    print("="*60)
    print("\n📋 Login Credentials:")
    print("\n  Admin:")
    print("    Username: admin")
    print("    Password: admin123")
    print("\n  Employees:")
    print("    john.doe / password123")
    print("    jane.smith / password123")
    print("    mike.wilson / password123")
    print("    sarah.johnson / password123")
    print("    david.brown / password123")
    print("\n🚀 You can now start the application!")
    print("="*60 + "\n")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("WorkSphere ERMA - Database Reset")
    print("="*60)
    print("\nThis will delete the existing database and create a fresh one.")
    
    response = input("\nContinue? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y']:
        print("\nResetting database...\n")
        reset_database()
    else:
        print("\nOperation cancelled.")

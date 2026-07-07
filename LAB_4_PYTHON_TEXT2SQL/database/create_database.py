#!/usr/bin/env python3
"""
Create and populate SQLite database for HR Management System
This script creates the database schema and inserts sample data
"""

import sqlite3
import os
from datetime import datetime, timedelta
import random

# ── Seed for reproducibility ──────────────────────────────────────────────────
random.seed(42)


def create_database(db_path='hr.db'):
    """Create SQLite database with schema and sample data"""

    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    print(f"Creating database: {db_path}")

    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)

    print("✓ Schema created")

    insert_sample_data(cursor)

    conn.commit()
    verify_database(cursor)
    conn.close()

    print(f"\n✓ Database created successfully: {db_path}")
    print(f"  Location: {os.path.abspath(db_path)}")


def insert_sample_data(cursor):
    """Insert sample data into all tables"""

    print("\nInserting sample data...")

    # ── Departments ───────────────────────────────────────────────────────────
    departments = [
        ('DEPT001', 'Engineering',  'Bangkok',    15),
        ('DEPT002', 'HR',           'Bangkok',     8),
        ('DEPT003', 'Finance',      'Bangkok',    10),
        ('DEPT004', 'Sales',        'Chiang Mai', 12),
        ('DEPT005', 'Operations',   'Phuket',     10),
    ]
    cursor.executemany(
        'INSERT INTO departments (department_id, department_name, location, head_count_budget) VALUES (?,?,?,?)',
        departments
    )
    print(f"  ✓ Inserted {len(departments)} departments")

    # ── Employees (managers first, then their direct reports) ─────────────────
    # Row: (employee_id, full_name, department_id, job_title, employment_type, hire_date, salary, manager_id)
    employees = [
        # ── Department Heads (no manager) ──
        ('EMP001', 'Somchai Pattana',     'DEPT001', 'Engineering Manager',  'Full-time', '2019-03-15', 120000, None),
        ('EMP002', 'Narin Srisuk',        'DEPT002', 'HR Manager',           'Full-time', '2018-06-01', 110000, None),
        ('EMP003', 'Pimchanok Thongchai', 'DEPT003', 'Finance Manager',      'Full-time', '2017-11-20', 115000, None),
        ('EMP004', 'Waree Kaewnoi',       'DEPT004', 'Sales Manager',        'Full-time', '2020-01-10', 105000, None),
        ('EMP005', 'Thanakorn Yodrak',    'DEPT005', 'Operations Manager',   'Full-time', '2019-07-22', 100000, None),

        # ── Engineering ──
        ('EMP006', 'Arisa Moonthong',     'DEPT001', 'Senior Software Engineer', 'Full-time', '2020-04-01', 95000, 'EMP001'),
        ('EMP007', 'Krit Jantaraporn',    'DEPT001', 'Software Engineer',        'Full-time', '2021-08-15', 75000, 'EMP001'),
        ('EMP008', 'Lalita Chaisuwan',    'DEPT001', 'Software Engineer',        'Full-time', '2022-02-28', 72000, 'EMP001'),
        ('EMP009', 'Natthawut Burana',    'DEPT001', 'Data Engineer',            'Full-time', '2021-05-10', 80000, 'EMP001'),
        ('EMP010', 'Pensri Rattana',      'DEPT001', 'QA Engineer',              'Full-time', '2022-09-01', 68000, 'EMP001'),
        ('EMP011', 'Rungrot Siriporn',    'DEPT001', 'DevOps Engineer',          'Full-time', '2020-11-15', 90000, 'EMP001'),
        ('EMP012', 'Siriporn Chaichana',  'DEPT001', 'Software Engineer',        'Contract',  '2023-01-01', 65000, 'EMP001'),
        ('EMP013', 'Tanawat Pholdee',     'DEPT001', 'Junior Developer',         'Full-time', '2023-06-01', 55000, 'EMP006'),
        ('EMP014', 'Unchalee Wongkam',    'DEPT001', 'Junior Developer',         'Full-time', '2023-07-15', 55000, 'EMP006'),

        # ── HR ──
        ('EMP015', 'Varanya Sooksai',     'DEPT002', 'HR Officer',               'Full-time', '2020-03-01', 65000, 'EMP002'),
        ('EMP016', 'Wanchai Prempree',    'DEPT002', 'Recruiter',                'Full-time', '2021-10-01', 60000, 'EMP002'),
        ('EMP017', 'Ying Wattana',        'DEPT002', 'Payroll Specialist',       'Full-time', '2019-12-01', 70000, 'EMP002'),
        ('EMP018', 'Zara Pimchan',        'DEPT002', 'HR Officer',               'Part-time', '2022-04-01', 38000, 'EMP002'),

        # ── Finance ──
        ('EMP019', 'Anan Boonsri',        'DEPT003', 'Senior Accountant',        'Full-time', '2019-08-15', 88000, 'EMP003'),
        ('EMP020', 'Bunyarit Chaimongkol','DEPT003', 'Accountant',               'Full-time', '2021-01-10', 68000, 'EMP003'),
        ('EMP021', 'Chanida Thanakit',    'DEPT003', 'Financial Analyst',        'Full-time', '2020-06-01', 80000, 'EMP003'),
        ('EMP022', 'Darunee Petcharat',   'DEPT003', 'Accountant',               'Full-time', '2022-03-15', 65000, 'EMP003'),
        ('EMP023', 'Eknarin Suksamran',   'DEPT003', 'Payroll Accountant',       'Contract',  '2023-02-01', 60000, 'EMP003'),

        # ── Sales ──
        ('EMP024', 'Fon Charoenwong',     'DEPT004', 'Senior Sales Executive',   'Full-time', '2020-05-01', 78000, 'EMP004'),
        ('EMP025', 'Gamon Prachaya',      'DEPT004', 'Sales Executive',          'Full-time', '2021-09-01', 62000, 'EMP004'),
        ('EMP026', 'Hathai Rattanawong',  'DEPT004', 'Sales Executive',          'Full-time', '2022-01-15', 60000, 'EMP004'),
        ('EMP027', 'Ittipat Noinoi',      'DEPT004', 'Sales Executive',          'Full-time', '2021-11-01', 60000, 'EMP004'),
        ('EMP028', 'Janya Srisuwan',      'DEPT004', 'Account Manager',          'Full-time', '2020-08-01', 72000, 'EMP004'),
        ('EMP029', 'Kamolchanok Yimram',  'DEPT004', 'Sales Coordinator',        'Part-time', '2022-06-01', 35000, 'EMP004'),

        # ── Operations ──
        ('EMP030', 'Laksana Pornprasit',  'DEPT005', 'Operations Supervisor',    'Full-time', '2020-02-01', 75000, 'EMP005'),
        ('EMP031', 'Manop Taweekul',      'DEPT005', 'Logistics Coordinator',    'Full-time', '2021-04-15', 58000, 'EMP005'),
        ('EMP032', 'Natchaya Sonthi',     'DEPT005', 'Logistics Coordinator',    'Full-time', '2022-08-01', 56000, 'EMP005'),
        ('EMP033', 'Oraphan Ruangrit',    'DEPT005', 'Warehouse Officer',        'Full-time', '2021-06-01', 52000, 'EMP005'),
        ('EMP034', 'Pakorn Srikham',      'DEPT005', 'Warehouse Officer',        'Full-time', '2022-10-01', 50000, 'EMP005'),
        ('EMP035', 'Quam Pornthep',       'DEPT005', 'Warehouse Officer',        'Contract',  '2023-03-01', 48000, 'EMP005'),
    ]
    cursor.executemany(
        '''INSERT INTO employees
           (employee_id, full_name, department_id, job_title, employment_type, hire_date, salary, manager_id)
           VALUES (?,?,?,?,?,?,?,?)''',
        employees
    )
    print(f"  ✓ Inserted {len(employees)} employees")

    # ── Leave Requests ────────────────────────────────────────────────────────
    leave_types   = ['Annual', 'Sick', 'Personal', 'Maternity', 'Unpaid']
    leave_weights = [0.45,     0.30,   0.15,       0.05,        0.05]
    statuses      = ['Approved', 'Approved', 'Approved', 'Pending', 'Rejected']

    emp_ids = [e[0] for e in employees]
    base    = datetime(2024, 1, 1)
    leave_rows = []

    for i in range(1, 121):
        leave_id   = f"LV{str(i).zfill(4)}"
        emp_id     = random.choice(emp_ids)
        ltype      = random.choices(leave_types, weights=leave_weights)[0]
        status     = random.choice(statuses)
        days       = 90 if ltype == 'Maternity' else random.randint(1, 5)
        start_dt   = base + timedelta(days=random.randint(0, 340))
        end_dt     = start_dt + timedelta(days=days - 1)
        leave_rows.append((leave_id, emp_id, ltype,
                           start_dt.strftime('%Y-%m-%d'),
                           end_dt.strftime('%Y-%m-%d'),
                           days, status))

    cursor.executemany(
        '''INSERT INTO leave_requests
           (leave_id, employee_id, leave_type, start_date, end_date, days_taken, status)
           VALUES (?,?,?,?,?,?,?)''',
        leave_rows
    )
    print(f"  ✓ Inserted {len(leave_rows)} leave requests")

    # ── Performance Reviews ───────────────────────────────────────────────────
    review_rows = []
    manager_map = {e[0]: e[7] for e in employees}   # emp_id → manager_id

    for idx, emp in enumerate(employees):
        emp_id     = emp[0]
        reviewer   = manager_map[emp_id] if manager_map[emp_id] else emp_id
        rating     = round(random.uniform(2.5, 5.0), 1)
        period     = '2024-H1'
        review_id  = f"REV{str(idx + 1).zfill(3)}"

        if rating >= 4.5:
            comment = "Outstanding performance. Exceeds all targets."
        elif rating >= 4.0:
            comment = "Strong contributor. Meets and often exceeds expectations."
        elif rating >= 3.0:
            comment = "Solid performance. Meets most expectations."
        else:
            comment = "Needs improvement in key areas. Action plan in progress."

        review_rows.append((review_id, emp_id, period, rating, reviewer, comment))

    cursor.executemany(
        '''INSERT INTO performance_reviews
           (review_id, employee_id, review_period, rating, reviewer_id, comments)
           VALUES (?,?,?,?,?,?)''',
        review_rows
    )
    print(f"  ✓ Inserted {len(review_rows)} performance reviews")


def verify_database(cursor):
    """Verify database contents"""

    print("\nVerifying database...")
    for table in ['departments', 'employees', 'leave_requests', 'performance_reviews']:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  ✓ {table}: {count} records")

    cursor.execute("SELECT COUNT(*) FROM v_high_performers")
    print(f"  ✓ v_high_performers: {cursor.fetchone()[0]} employees rated ≥ 4.0")


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path    = os.path.join(script_dir, 'hr.db')

    print("=" * 60)
    print("SQLite Database Creation Script")
    print("HR Management System")
    print("=" * 60)

    create_database(db_path)

    print("\n" + "=" * 60)
    print("Database is ready for use!")
    print("=" * 60)

# Made with Bob

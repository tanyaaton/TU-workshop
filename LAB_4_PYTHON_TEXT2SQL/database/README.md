# SQLite Database for HR Management System

This directory contains the SQLite database and related files for LAB 4.

## 📁 Files

- **`schema.sql`** — Database schema: tables, indexes, and views
- **`create_database.py`** — Python script to create and populate the database
- **`hr.db`** — SQLite database file (created by running `create_database.py`)

## 🗄️ Database Structure

### Tables

#### 1. `departments`
Master data for each department in the organisation.

```sql
CREATE TABLE departments (
    department_id     TEXT PRIMARY KEY,
    department_name   TEXT NOT NULL,
    location          TEXT NOT NULL,
    head_count_budget INTEGER NOT NULL DEFAULT 0
);
```

**Sample Data:** 5 departments — Engineering, HR, Finance, Sales, Operations

---

#### 2. `employees`
Master data for all employees, including a self-referencing `manager_id`.

```sql
CREATE TABLE employees (
    employee_id     TEXT PRIMARY KEY,
    full_name       TEXT NOT NULL,
    department_id   TEXT NOT NULL,
    job_title       TEXT NOT NULL,
    employment_type TEXT NOT NULL DEFAULT 'Full-time',  -- Full-time | Part-time | Contract
    hire_date       DATE NOT NULL,
    salary          REAL NOT NULL,
    manager_id      TEXT  -- FK → employees(employee_id)
);
```

**Sample Data:** 35 employees across 5 departments (Bangkok, Chiang Mai, Phuket)

---

#### 3. `leave_requests`
Tracks all employee leave history.

```sql
CREATE TABLE leave_requests (
    leave_id    TEXT PRIMARY KEY,
    employee_id TEXT NOT NULL,
    leave_type  TEXT NOT NULL,  -- Annual | Sick | Maternity | Personal | Unpaid
    start_date  DATE NOT NULL,
    end_date    DATE NOT NULL,
    days_taken  INTEGER NOT NULL DEFAULT 1,
    status      TEXT NOT NULL DEFAULT 'Pending'  -- Approved | Pending | Rejected
);
```

**Sample Data:** 120 leave requests across 2024

---

#### 4. `performance_reviews`
Periodic performance ratings submitted by managers.

```sql
CREATE TABLE performance_reviews (
    review_id     TEXT PRIMARY KEY,
    employee_id   TEXT NOT NULL,
    review_period TEXT NOT NULL,   -- e.g. '2024-H1'
    rating        REAL NOT NULL,   -- 1.0 – 5.0
    reviewer_id   TEXT NOT NULL,   -- FK → employees(employee_id)
    comments      TEXT
);
```

**Sample Data:** 35 reviews (one per employee) for period `2024-H1`

---

### Views

#### `v_headcount_by_department`
Compares actual headcount to the approved budget and shows salary statistics per department.

```sql
SELECT department_name, location, head_count_budget,
       actual_headcount, open_positions,
       avg_salary, min_salary, max_salary, total_salary_cost
FROM v_headcount_by_department;
```

#### `v_leave_summary`
Leave days consumed per employee, broken down by leave type.

```sql
SELECT full_name, department_name,
       annual_days_used, sick_days_used, personal_days_used,
       maternity_days_used, total_days_taken, pending_requests
FROM v_leave_summary;
```

#### `v_high_performers`
Employees with a performance rating ≥ 4.0.

```sql
SELECT full_name, job_title, department_name,
       salary, review_period, rating, comments
FROM v_high_performers;
```

#### `v_salary_band`
Salary distribution (min / max / avg) grouped by department and job title.

```sql
SELECT department_name, job_title, employment_type,
       headcount, min_salary, max_salary, avg_salary, total_monthly_cost
FROM v_salary_band;
```

---

## 🚀 Quick Start

### Create the Database

```bash
cd LAB_4_PYTHON_TEXT2SQL/database
python3 create_database.py
```

This will:
1. Remove any existing `hr.db`
2. Create a fresh `hr.db`
3. Execute schema from `schema.sql`
4. Insert all sample data
5. Verify record counts

### Query the Database

**Using SQLite CLI:**

```bash
sqlite3 hr.db

.tables
.schema employees

SELECT * FROM v_headcount_by_department;
SELECT * FROM v_high_performers LIMIT 10;

.quit
```

**Using Python:**

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('hr.db')

df = pd.read_sql_query("SELECT * FROM v_headcount_by_department", conn)
print(df)

conn.close()
```

---

## 📊 Sample Queries

### Headcount & Organisation

```sql
-- Headcount vs budget per department
SELECT * FROM v_headcount_by_department;

-- Employees in Engineering
SELECT full_name, job_title, hire_date, salary
FROM employees
JOIN departments ON employees.department_id = departments.department_id
WHERE departments.department_name = 'Engineering'
ORDER BY salary DESC;

-- Contract employees
SELECT full_name, job_title, department_id
FROM employees
WHERE employment_type = 'Contract';
```

### Salary Analysis

```sql
-- Salary band by department + job title
SELECT * FROM v_salary_band ORDER BY avg_salary DESC;

-- Highest paid employees
SELECT full_name, job_title, salary
FROM employees
ORDER BY salary DESC
LIMIT 10;

-- Average salary by employment type
SELECT employment_type,
       COUNT(*) AS headcount,
       ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY employment_type;
```

### Leave Management

```sql
-- Leave summary per employee
SELECT * FROM v_leave_summary ORDER BY total_days_taken DESC;

-- Pending leave requests
SELECT e.full_name, lr.leave_type, lr.start_date, lr.end_date, lr.days_taken
FROM leave_requests lr
JOIN employees e ON lr.employee_id = e.employee_id
WHERE lr.status = 'Pending';

-- Total sick days by department
SELECT d.department_name, SUM(lr.days_taken) AS total_sick_days
FROM leave_requests lr
JOIN employees e ON lr.employee_id = e.employee_id
JOIN departments d ON e.department_id = d.department_id
WHERE lr.leave_type = 'Sick' AND lr.status = 'Approved'
GROUP BY d.department_name
ORDER BY total_sick_days DESC;
```

### Performance

```sql
-- High performers
SELECT * FROM v_high_performers;

-- Average rating by department
SELECT d.department_name, ROUND(AVG(pr.rating), 2) AS avg_rating
FROM performance_reviews pr
JOIN employees e ON pr.employee_id = e.employee_id
JOIN departments d ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY avg_rating DESC;
```

---

## 🔧 Maintenance

### Add a New Employee

```sql
INSERT INTO employees (employee_id, full_name, department_id, job_title, employment_type, hire_date, salary, manager_id)
VALUES ('EMP036', 'New Employee', 'DEPT001', 'Software Engineer', 'Full-time', '2024-08-01', 70000, 'EMP001');
```

### Record a Leave Request

```sql
INSERT INTO leave_requests (leave_id, employee_id, leave_type, start_date, end_date, days_taken, status)
VALUES ('LV0121', 'EMP001', 'Annual', '2024-12-23', '2024-12-27', 5, 'Approved');
```

---

## 📝 Notes

- Database file: `hr.db` (~100 KB with sample data)
- SQLite version: 3.x compatible
- Character encoding: UTF-8
- Date format: `YYYY-MM-DD`
- Supports Thai and English employee names

---

**Made with Bob**

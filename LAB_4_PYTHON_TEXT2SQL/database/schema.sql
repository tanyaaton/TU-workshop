-- SQLite Database Schema for HR Management System
-- Created for LAB 4: Python Text-to-SQL Workshop

-- Drop tables if they exist (for clean setup)
DROP VIEW IF EXISTS v_salary_band;
DROP VIEW IF EXISTS v_high_performers;
DROP VIEW IF EXISTS v_leave_summary;
DROP VIEW IF EXISTS v_headcount_by_department;
DROP TABLE IF EXISTS performance_reviews;
DROP TABLE IF EXISTS leave_requests;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

-- Departments Table
-- Stores department master data
CREATE TABLE departments (
    department_id   TEXT PRIMARY KEY,
    department_name TEXT NOT NULL,
    location        TEXT NOT NULL,
    head_count_budget INTEGER NOT NULL DEFAULT 0,
    CHECK (head_count_budget >= 0)
);

-- Employees Table
-- Stores employee master data
CREATE TABLE employees (
    employee_id     TEXT PRIMARY KEY,
    full_name       TEXT NOT NULL,
    department_id   TEXT NOT NULL,
    job_title       TEXT NOT NULL,
    employment_type TEXT NOT NULL DEFAULT 'Full-time',
    hire_date       DATE NOT NULL,
    salary          REAL NOT NULL,
    manager_id      TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (manager_id)    REFERENCES employees(employee_id),
    CHECK (employment_type IN ('Full-time', 'Part-time', 'Contract')),
    CHECK (salary >= 0)
);

-- Leave Requests Table
-- Tracks employee leave history
CREATE TABLE leave_requests (
    leave_id    TEXT PRIMARY KEY,
    employee_id TEXT NOT NULL,
    leave_type  TEXT NOT NULL,
    start_date  DATE NOT NULL,
    end_date    DATE NOT NULL,
    days_taken  INTEGER NOT NULL DEFAULT 1,
    status      TEXT NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    CHECK (leave_type IN ('Annual', 'Sick', 'Maternity', 'Personal', 'Unpaid')),
    CHECK (status IN ('Approved', 'Pending', 'Rejected')),
    CHECK (days_taken > 0)
);

-- Performance Reviews Table
-- Stores periodic employee performance ratings
CREATE TABLE performance_reviews (
    review_id     TEXT PRIMARY KEY,
    employee_id   TEXT NOT NULL,
    review_period TEXT NOT NULL,
    rating        REAL NOT NULL,
    reviewer_id   TEXT NOT NULL,
    comments      TEXT,
    FOREIGN KEY (employee_id)  REFERENCES employees(employee_id),
    FOREIGN KEY (reviewer_id)  REFERENCES employees(employee_id),
    CHECK (rating >= 1.0 AND rating <= 5.0)
);

-- Indexes for better query performance
CREATE INDEX idx_employees_department  ON employees(department_id);
CREATE INDEX idx_employees_manager     ON employees(manager_id);
CREATE INDEX idx_employees_type        ON employees(employment_type);
CREATE INDEX idx_leave_employee        ON leave_requests(employee_id);
CREATE INDEX idx_leave_type            ON leave_requests(leave_type);
CREATE INDEX idx_leave_status          ON leave_requests(status);
CREATE INDEX idx_review_employee       ON performance_reviews(employee_id);
CREATE INDEX idx_review_period         ON performance_reviews(review_period);
CREATE INDEX idx_review_rating         ON performance_reviews(rating);

-- ─────────────────────────────────────────────
-- Views
-- ─────────────────────────────────────────────

-- View: Headcount by Department
-- Compares actual headcount to approved budget and shows avg salary
CREATE VIEW v_headcount_by_department AS
SELECT
    d.department_id,
    d.department_name,
    d.location,
    d.head_count_budget,
    COUNT(e.employee_id)                        AS actual_headcount,
    (d.head_count_budget - COUNT(e.employee_id)) AS open_positions,
    ROUND(AVG(e.salary), 2)                     AS avg_salary,
    ROUND(MIN(e.salary), 2)                     AS min_salary,
    ROUND(MAX(e.salary), 2)                     AS max_salary,
    ROUND(SUM(e.salary), 2)                     AS total_salary_cost
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name, d.location, d.head_count_budget
ORDER BY actual_headcount DESC;

-- View: Leave Summary per Employee (current year)
CREATE VIEW v_leave_summary AS
SELECT
    e.employee_id,
    e.full_name,
    e.department_id,
    d.department_name,
    SUM(CASE WHEN lr.leave_type = 'Annual'    AND lr.status = 'Approved' THEN lr.days_taken ELSE 0 END) AS annual_days_used,
    SUM(CASE WHEN lr.leave_type = 'Sick'      AND lr.status = 'Approved' THEN lr.days_taken ELSE 0 END) AS sick_days_used,
    SUM(CASE WHEN lr.leave_type = 'Personal'  AND lr.status = 'Approved' THEN lr.days_taken ELSE 0 END) AS personal_days_used,
    SUM(CASE WHEN lr.leave_type = 'Maternity' AND lr.status = 'Approved' THEN lr.days_taken ELSE 0 END) AS maternity_days_used,
    SUM(CASE WHEN lr.status = 'Approved'      THEN lr.days_taken ELSE 0 END)                            AS total_days_taken,
    COUNT(CASE WHEN lr.status = 'Pending'     THEN 1 END)                                               AS pending_requests
FROM employees e
JOIN departments d ON e.department_id = d.department_id
LEFT JOIN leave_requests lr ON e.employee_id = lr.employee_id
GROUP BY e.employee_id, e.full_name, e.department_id, d.department_name
ORDER BY total_days_taken DESC;

-- View: High Performers (rating >= 4.0 in latest review)
CREATE VIEW v_high_performers AS
SELECT
    e.employee_id,
    e.full_name,
    e.job_title,
    d.department_name,
    e.salary,
    pr.review_period,
    pr.rating,
    pr.comments
FROM employees e
JOIN departments d         ON e.department_id = d.department_id
JOIN performance_reviews pr ON e.employee_id  = pr.employee_id
WHERE pr.rating >= 4.0
ORDER BY pr.rating DESC, e.full_name;

-- View: Salary Band by Department and Job Title
CREATE VIEW v_salary_band AS
SELECT
    d.department_name,
    e.job_title,
    e.employment_type,
    COUNT(e.employee_id)        AS headcount,
    ROUND(MIN(e.salary), 2)     AS min_salary,
    ROUND(MAX(e.salary), 2)     AS max_salary,
    ROUND(AVG(e.salary), 2)     AS avg_salary,
    ROUND(SUM(e.salary), 2)     AS total_monthly_cost
FROM employees e
JOIN departments d ON e.department_id = d.department_id
GROUP BY d.department_name, e.job_title, e.employment_type
ORDER BY d.department_name, avg_salary DESC;

-- Made with Bob

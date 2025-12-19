-- SQL program Table :-

-- Show all databases 
show databases;

-- Create Database
CREATE DATABASE IF NOT EXISTS company_db;
use company_db;

-- Create Departments Table
create table departments (
dept_id int primary key auto_increment,
dept_name varchar(100) not null,
location varchar(100)
);

-- Create Employees Table
create table employees (
emp_id int primary key auto_increment,
first_name varchar(50) not null,
last_name varchar(50) not null,
email varchar(100) unique,
phone varchar(20),
hire_date date not null,
job_title varchar(100),
salary decimal(10, 2),
dept_id int,
manager_id int,
foreign key (dept_id) references departments(dept_id),
foreign key(manager_id) references employees(emp_id)
);

-- Insert Sample Departments
insert into departments (dept_name, location) values
('Human Resources', 'New York'),
('Engineering', 'San Francisco'),
('Sales', 'Chicago'),
('Marketing','Los Angeles'),
('Finance','New york');

-- Insert Sample Employees
insert into employees (first_name, last_name, email, phone, hire_date, job_title, salary, dept_id, manager_id) values
('John','smith','john.smith@company.com','555-0101','2020-01-15','CEO',150000.00,NUll, NULL),
('Sarah','Johnson','sarah.j@company.com','555-0102','2020-03-20','HR Manager',85000.00,1,1),
('Michael', 'Brown', 'michael.b@company.com', '555-0103', '2021-06-10', 'Engineering Manager', 95000.00, 2, 1),
('Emily', 'Davis', 'emily.d@company.com', '555-0104', '2021-08-15', 'Software Engineer', 75000.00, 2, 3),
('David', 'Wilson', 'david.w@company.com', '555-0105', '2022-01-20', 'Software Engineer', 72000.00, 2, 3),
('Lisa', 'Anderson', 'lisa.a@company.com', '555-0106', '2022-03-12', 'Sales Manager', 88000.00, 3, 1),
('James', 'Martinez', 'james.m@company.com', '555-0107', '2022-05-18', 'Sales Representative', 55000.00, 3, 6),
('Jennifer', 'Garcia', 'jennifer.g@company.com', '555-0108', '2023-02-14', 'Marketing Specialist', 62000.00, 4, 1);

-- Query 1: View all employees
select *from employees;

-- Query 1: List all employees with their department names
select e.emp_id, e.first_name, e.last_name, e.job_title, e.salary, d.dept_name
from employees e
left join departments d on e.dept_id =d.dept_id
order by e.emp_id;

-- Query 2: Find employees earning above average salary
SELECT first_name, last_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC;

-- Query 3: Count employees by department
SELECT d.dept_name, COUNT(e.emp_id) AS employee_count
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_name
ORDER BY employee_count DESC;

-- Query 4: Find managers and their direct reports
SELECT 
    m.first_name AS manager_first_name,
    m.last_name AS manager_last_name,
    e.first_name AS employee_first_name,
    e.last_name AS employee_last_name,
    e.job_title
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id
ORDER BY m.emp_id, e.emp_id;


-- Query 5: Calculate average salary by department
SELECT d.dept_name, AVG(e.salary) AS avg_salary, COUNT(e.emp_id) AS num_employees
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_name
HAVING COUNT(e.emp_id) > 0
ORDER BY avg_salary DESC;


-- Query 6: Find employees hired in the last year
SELECT first_name, last_name, hire_date, job_title
FROM employees
WHERE hire_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
ORDER BY hire_date DESC;


-- Query 7: Update employee salary (example)
UPDATE employees SET salary = salary * 1.05 WHERE emp_id = 4;

-- Query 8: Search employees by name
SELECT * FROM employees WHERE first_name LIKE '%John%' OR last_name LIKE '%John%';-- 

-- create Database if NOT exists student_db;

-- use student_db;

-- create table students (
-- id int primary key auto_increment,
-- name varchar(50),
-- age int,
-- course varchar(50));

-- desc students;

-- alter table students
-- add column marks float;

-- show tables;

-- insert into students (name, age,course)
-- values
-- ('Rahul',19,'BCA');

-- insert into students (name, age,course)
-- values
-- ('Amit',21,'BCA'),
-- ('Priya',20,'BSc CS'),
-- ('Sneha',19,'BCA'),
-- ('Vikash',22,'BCA');

-- select  * FROM students;


-- create view bca_students as
-- select id, name, age
-- from students
-- where course = 'BCA';
-- insert into students (name,course)
-- values
-- ('Riya','BCA'),
-- ('Karan','BSc CS');

-- select * from bca_students;

-- create view student_summary as
-- select
-- course,
-- AVG(age) as avg_age,
-- COUNT(*) as total_students
-- from students
-- group by course;

-- desc student_summary;

-- select * from student_summary;


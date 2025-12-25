import json
import csv
from datetime import datetime
from collections import defaultdict, Counter
from pathlib import Path
import pickle
import bisect

class StudentIndexer:
    """Advanced student record management with multiple indexes - Pure Python"""
    
    def __init__(self):
        # Main data storage
        self.students = {}  # student_id -> student_data
        self.courses = {}   # course_code -> course_data
        self.enrollments = defaultdict(list)  # student_id -> [enrollments]
        
        # Indexes for fast searching (sorted lists)
        self.index_by_last_name = defaultdict(list)  # last_name -> [student_ids]
        self.index_by_grade = defaultdict(list)      # grade_level -> [student_ids]
        self.index_by_gpa = []                        # sorted list of (gpa, student_id)
        self.index_by_email = {}                      # email -> student_id
        
        # Course indexes
        self.index_by_department = defaultdict(list)  # department -> [course_codes]
        self.course_enrollments = defaultdict(list)   # course_code -> [student_ids]
    
    def add_student(self, student_id, first_name, last_name, email=None, 
                   phone=None, date_of_birth=None, grade_level=None, gpa=None):
        """Add a new student and update all indexes"""
        if student_id in self.students:
            print(f"✗ Error: Student ID {student_id} already exists")
            return False
        
        if email and email in self.index_by_email:
            print(f"✗ Error: Email {email} already registered")
            return False
        
        student = {
            'student_id': student_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'date_of_birth': date_of_birth,
            'enrollment_date': datetime.now().date().isoformat(),
            'grade_level': grade_level,
            'gpa': gpa,
            'status': 'active'
        }
        
        # Add to main storage
        self.students[student_id] = student
        
        # Update indexes
        self.index_by_last_name[last_name.lower()].append(student_id)
        
        if grade_level is not None:
            self.index_by_grade[grade_level].append(student_id)
        
        if gpa is not None:
            # Insert into sorted GPA index using binary search
            bisect.insort(self.index_by_gpa, (gpa, student_id))
        
        if email:
            self.index_by_email[email] = student_id
        
        print(f"✓ Added student: {first_name} {last_name} ({student_id})")
        return True
    
    def add_course(self, course_code, course_name, credits=3, department=None):
        """Add a new course"""
        if course_code in self.courses:
            print(f"✗ Error: Course {course_code} already exists")
            return False
        
        course = {
            'course_code': course_code,
            'course_name': course_name,
            'credits': credits,
            'department': department
        }
        
        self.courses[course_code] = course
        
        if department:
            self.index_by_department[department.lower()].append(course_code)
        
        print(f"✓ Added course: {course_name} ({course_code})")
        return True
    
    def enroll_student(self, student_id, course_code, semester, grade=None, score=None):
        """Enroll a student in a course"""
        if student_id not in self.students:
            print(f"✗ Error: Student {student_id} not found")
            return False
        
        if course_code not in self.courses:
            print(f"✗ Error: Course {course_code} not found")
            return False
        
        enrollment = {
            'student_id': student_id,
            'course_code': course_code,
            'semester': semester,
            'grade': grade,
            'score': score,
            'enrollment_date': datetime.now().isoformat()
        }
        
        self.enrollments[student_id].append(enrollment)
        self.course_enrollments[course_code].append(student_id)
        
        return True
    
    def search_by_id(self, student_id):
        """Search student by ID - O(1) lookup"""
        return self.students.get(student_id)
    
    def search_by_name(self, last_name):
        """Search students by last name - O(1) with index"""
        student_ids = self.index_by_last_name.get(last_name.lower(), [])
        return [self.students[sid] for sid in student_ids]
    
    def search_by_partial_name(self, name_part):
        """Search students by partial name match"""
        results = []
        name_part = name_part.lower()
        
        for student_id, student in self.students.items():
            if (name_part in student['first_name'].lower() or 
                name_part in student['last_name'].lower()):
                results.append(student)
        
        return results
    
    def search_by_email(self, email):
        """Search student by email - O(1) lookup"""
        student_id = self.index_by_email.get(email)
        return self.students.get(student_id) if student_id else None
    
    def search_by_grade_level(self, grade_level):
        """Search students by grade level - O(1) with index"""
        student_ids = self.index_by_grade.get(grade_level, [])
        students = [self.students[sid] for sid in student_ids]
        # Sort by GPA descending
        return sorted(students, key=lambda s: s.get('gpa') or 0, reverse=True)
    
    def search_by_gpa_range(self, min_gpa, max_gpa):
        """Search students by GPA range - O(log n) with binary search"""
        results = []
        
        # Find the range in sorted GPA index
        start_idx = bisect.bisect_left(self.index_by_gpa, (min_gpa, ''))
        end_idx = bisect.bisect_right(self.index_by_gpa, (max_gpa, '\xff'))
        
        for gpa, student_id in self.index_by_gpa[start_idx:end_idx]:
            results.append(self.students[student_id])
        
        return sorted(results, key=lambda s: s['gpa'], reverse=True)
    
    def get_top_students(self, n=10):
        """Get top N students by GPA - O(n)"""
        # Already sorted in descending order
        top_entries = self.index_by_gpa[-n:][::-1]
        return [self.students[sid] for gpa, sid in top_entries]
    
    def get_student_courses(self, student_id):
        """Get all courses for a student"""
        enrollments = self.enrollments.get(student_id, [])
        result = []
        
        for enrollment in enrollments:
            course = self.courses[enrollment['course_code']]
            result.append({
                'course_code': course['course_code'],
                'course_name': course['course_name'],
                'semester': enrollment['semester'],
                'grade': enrollment['grade'],
                'score': enrollment['score']
            })
        
        return result
    
    def get_course_students(self, course_code):
        """Get all students in a course"""
        student_ids = self.course_enrollments.get(course_code, [])
        results = []
        
        for student_id in student_ids:
            student = self.students[student_id]
            # Find the enrollment for this course
            enrollment = next(
                (e for e in self.enrollments[student_id] 
                 if e['course_code'] == course_code), 
                None
            )
            
            results.append({
                'student_id': student_id,
                'first_name': student['first_name'],
                'last_name': student['last_name'],
                'grade': enrollment['grade'] if enrollment else None,
                'score': enrollment['score'] if enrollment else None
            })
        
        # Sort by score descending
        return sorted(results, key=lambda s: s['score'] or 0, reverse=True)
    
    def get_statistics(self):
        """Get comprehensive statistics"""
        stats = {}
        
        # Total students
        stats['total_students'] = len(self.students)
        
        # Average GPA
        gpas = [s['gpa'] for s in self.students.values() if s['gpa'] is not None]
        stats['average_gpa'] = round(sum(gpas) / len(gpas), 2) if gpas else None
        stats['median_gpa'] = round(sorted(gpas)[len(gpas)//2], 2) if gpas else None
        
        # Students per grade level
        stats['students_per_grade'] = [
            (grade, len(students)) 
            for grade, students in sorted(self.index_by_grade.items())
        ]
        
        # Honor students (GPA >= 3.5)
        stats['honor_students'] = sum(1 for s in self.students.values() if s.get('gpa', 0) >= 3.5)
        
        # Total courses
        stats['total_courses'] = len(self.courses)
        
        # Most popular courses
        course_popularity = [
            (code, len(students), self.courses[code]['course_name'])
            for code, students in self.course_enrollments.items()
        ]
        stats['popular_courses'] = sorted(course_popularity, key=lambda x: x[1], reverse=True)[:5]
        
        # Department statistics
        dept_counter = Counter()
        for course in self.courses.values():
            if course['department']:
                dept_counter[course['department']] += 1
        stats['courses_per_department'] = dept_counter.most_common()
        
        return stats
    
    def generate_report(self, student_id):
        """Generate comprehensive student report"""
        student = self.search_by_id(student_id)
        if not student:
            return None
        
        courses = self.get_student_courses(student_id)
        
        report = {
            'student_info': {
                'id': student['student_id'],
                'name': f"{student['first_name']} {student['last_name']}",
                'email': student['email'],
                'phone': student['phone'],
                'grade_level': student['grade_level'],
                'gpa': student['gpa'],
                'enrollment_date': student['enrollment_date'],
                'status': student['status']
            },
            'courses': courses,
            'total_courses': len(courses),
            'total_credits': sum(
                self.courses[c['course_code']]['credits'] 
                for c in courses
            )
        }
        
        return report
    
    def export_to_csv(self, filename="students_export.csv"):
        """Export all students to CSV"""
        if not self.students:
            print("No students to export")
            return
        
        with open(filename, 'w', newline='') as f:
            # Get all keys from first student
            fieldnames = list(self.students[next(iter(self.students))].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(self.students.values())
        
        print(f"✓ Exported {len(self.students)} students to {filename}")
    
    def export_to_json(self, filename="students_export.json"):
        """Export all data to JSON"""
        data = {
            'students': list(self.students.values()),
            'courses': list(self.courses.values()),
            'enrollments': {k: v for k, v in self.enrollments.items()},
            'export_date': datetime.now().isoformat(),
            'statistics': self.get_statistics()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Exported to {filename}")
    
    def save_to_pickle(self, filename="student_index.pkl"):
        """Save entire index to pickle file"""
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        print(f"✓ Saved index to {filename}")
    
    @staticmethod
    def load_from_pickle(filename="student_index.pkl"):
        """Load index from pickle file"""
        with open(filename, 'rb') as f:
            indexer = pickle.load(f)
        print(f"✓ Loaded index from {filename}")
        return indexer

def main():
    print("=== STUDENT RECORD INDEXING SYSTEM (Pure Python) ===\n")
    
    # Initialize
    indexer = StudentIndexer()
    
    # Add sample students
    print("1. ADDING STUDENTS")
    indexer.add_student("S001", "Alice", "Johnson", "alice.j@school.edu", grade_level=10, gpa=3.8)
    indexer.add_student("S002", "Bob", "Smith", "bob.s@school.edu", grade_level=10, gpa=3.5)
    indexer.add_student("S003", "Charlie", "Brown", "charlie.b@school.edu", grade_level=11, gpa=3.9)
    indexer.add_student("S004", "Diana", "Martinez", "diana.m@school.edu", grade_level=11, gpa=3.7)
    indexer.add_student("S005", "Eve", "Johnson", "eve.j@school.edu", grade_level=12, gpa=4.0)
    indexer.add_student("S006", "Frank", "Lee", "frank.l@school.edu", grade_level=12, gpa=3.6)
    print()
    
    # Add courses
    print("2. ADDING COURSES")
    indexer.add_course("MATH101", "Algebra I", 4, "Mathematics")
    indexer.add_course("ENG101", "English Literature", 3, "English")
    indexer.add_course("SCI101", "Physics", 4, "Science")
    indexer.add_course("HIST101", "World History", 3, "History")
    indexer.add_course("MATH201", "Calculus", 4, "Mathematics")
    print()
    
    # Enroll students
    print("3. ENROLLING STUDENTS")
    indexer.enroll_student("S001", "MATH101", "Fall 2024", "A", 92.5)
    indexer.enroll_student("S001", "ENG101", "Fall 2024", "A-", 88.0)
    indexer.enroll_student("S002", "MATH101", "Fall 2024", "B+", 87.0)
    indexer.enroll_student("S003", "SCI101", "Fall 2024", "A", 95.0)
    indexer.enroll_student("S005", "MATH101", "Fall 2024", "A+", 98.0)
    indexer.enroll_student("S005", "MATH201", "Fall 2024", "A", 96.0)
    print("✓ Students enrolled in courses\n")
    
    # Search by ID
    print("4. SEARCH BY ID (S001)")
    student = indexer.search_by_id("S001")
    if student:
        print(f"  Found: {student['first_name']} {student['last_name']} - GPA: {student['gpa']}")
    print()
    
    # Search by name
    print("5. SEARCH BY NAME (Johnson)")
    results = indexer.search_by_name("Johnson")
    for student in results:
        print(f"  {student['student_id']}: {student['first_name']} {student['last_name']} - Grade {student['grade_level']}, GPA: {student['gpa']}")
    print()
    
    # Search by partial name
    print("6. SEARCH BY PARTIAL NAME (ar)")
    results = indexer.search_by_partial_name("ar")
    for student in results:
        print(f"  {student['student_id']}: {student['first_name']} {student['last_name']}")
    print()
    
    # Search by grade level
    print("7. SEARCH BY GRADE LEVEL (Grade 11)")
    results = indexer.search_by_grade_level(11)
    for student in results:
        print(f"  {student['student_id']}: {student['first_name']} {student['last_name']} - GPA: {student['gpa']}")
    print()
    
    # Search by GPA range
    print("8. SEARCH BY GPA RANGE (3.7 - 4.0)")
    results = indexer.search_by_gpa_range(3.7, 4.0)
    for student in results:
        print(f"  {student['student_id']}: {student['first_name']} {student['last_name']} - Grade {student['grade_level']}, GPA: {student['gpa']}")
    print()
    
    # Top students
    print("9. TOP STUDENTS (Top 3)")
    top = indexer.get_top_students(3)
    for student in top:
        print(f"  {student['student_id']}: {student['first_name']} {student['last_name']} - GPA: {student['gpa']}")
    print()
    
    # Get student courses
    print("10. STUDENT COURSES (S005)")
    courses = indexer.get_student_courses("S005")
    for course in courses:
        print(f"  {course['course_code']}: {course['course_name']} - {course['semester']} - Grade: {course['grade']} ({course['score']})")
    print()
    
    # Get course students
    print("11. COURSE ROSTER (MATH101)")
    students = indexer.get_course_students("MATH101")
    for student in students:
        print(f"  {student['student_id']}: {student['first_name']} {student['last_name']} - Score: {student['score']}")
    print()
    
    # Statistics
    print("12. STATISTICS")
    stats = indexer.get_statistics()
    print(f"Total Students: {stats['total_students']}")
    print(f"Average GPA: {stats['average_gpa']}")
    print(f"Median GPA: {stats['median_gpa']}")
    print(f"Honor Students (GPA >= 3.5): {stats['honor_students']}")
    print(f"Total Courses: {stats['total_courses']}")
    print("\nStudents per Grade:")
    for grade, count in stats['students_per_grade']:
        print(f"  Grade {grade}: {count} students")
    print("\nMost Popular Courses:")
    for code, count, name in stats['popular_courses']:
        print(f"  {code} ({name}): {count} students")
    print()
    
    # Generate report
    print("13. STUDENT REPORT (S001)")
    report = indexer.generate_report("S001")
    if report:
        print(f"Student: {report['student_info']['name']}")
        print(f"ID: {report['student_info']['id']}")
        print(f"Email: {report['student_info']['email']}")
        print(f"Grade Level: {report['student_info']['grade_level']}")
        print(f"GPA: {report['student_info']['gpa']}")
        print(f"Total Courses: {report['total_courses']}")
        print(f"Total Credits: {report['total_credits']}")
        print("Courses:")
        for course in report['courses']:
            print(f"  {course['course_code']}: {course['course_name']} - {course['grade']} ({course['score']})")
    print()
    
    # Export data
    print("14. EXPORT DATA")
    indexer.export_to_csv("demo_students.csv")
    indexer.export_to_json("demo_students.json")
    indexer.save_to_pickle("demo_students.pkl")
    print()
    
    # Cleanup demo files
    try:
        Path("demo_students.csv").unlink(missing_ok=True)
        Path("demo_students.json").unlink(missing_ok=True)
        Path("demo_students.pkl").unlink(missing_ok=True)
        print("✓ Demo files cleaned up")
    except Exception as e:
        print(f"Note: {e}")

if __name__ == "__main__":
    main()

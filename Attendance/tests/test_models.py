from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.utils import timezone

from Attendance.models import Faculty, Department, Programme, Staff, Student, Course, RegisteredStudent, \
    StudentAttendance, CourseAttendance, Person


class PersonModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="username", password="password")
        Person.objects.create(user=user, last_name="John", first_name="Doe", is_staff=False)

    def test_user_label(self):
        person = get_object_or_404(Person, last_name="John")
        field_label = person._meta.get_field("user").verbose_name
        self.assertEqual(field_label, "user")

    def test_last_name_label(self):
        person = get_object_or_404(Person, last_name="John")
        field_label = person._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "last name")

    def test_last_name_max_length(self):
        person = get_object_or_404(Person, last_name="John")
        max_length = person._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 100)

    def test_first_name_label(self):
        person = get_object_or_404(Person, last_name="John")
        field_label = person._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_first_name_max_length(self):
        person = get_object_or_404(Person, last_name="John")
        max_length = person._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 100)

    def test_is_staff_label(self):
        person = get_object_or_404(Person, last_name="John")
        field_label = person._meta.get_field("is_staff").verbose_name
        self.assertEqual(field_label, "is staff")

    def test_image_label(self):
        person = get_object_or_404(Person, last_name="John")
        field_label = person._meta.get_field("image").verbose_name
        self.assertEqual(field_label, "image")


class FacultyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Faculty.objects.create(faculty_name="Computing And Applied Sciences")

    def test_faculty_name_label(self):
        faculty = get_object_or_404(Faculty, faculty_name="Computing And Applied Sciences")
        field_label = faculty._meta.get_field('faculty_name').verbose_name
        self.assertEqual(field_label, 'faculty name')

    def test_faculty_name_max_length(self):
        faculty = get_object_or_404(Faculty, faculty_name="Computing And Applied Sciences")
        max_length = faculty._meta.get_field('faculty_name').max_length
        self.assertEqual(max_length, 100)


class DepartmentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        faculty = Faculty.objects.create(faculty_name="Computing And Applied Sciences")
        Department.objects.create(faculty=faculty, department_name="Computer Science")

    def test_faculty_name_label(self):
        department = get_object_or_404(Department, department_name="Computer Science")
        field_label = department._meta.get_field('faculty').verbose_name
        self.assertEqual(field_label, 'faculty')

    def test_department_name_label(self):
        department = get_object_or_404(Department, department_name="Computer Science")
        field_label = department._meta.get_field('department_name').verbose_name
        self.assertEqual(field_label, 'department name')

    def test_department_name_max_length(self):
        department = get_object_or_404(Department, department_name="Computer Science")
        max_length = department._meta.get_field('department_name').max_length
        self.assertEqual(max_length, 50)


class ProgrammeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        faculty = Faculty.objects.create(faculty_name="Computing And Applied Sciences")
        department = Department.objects.create(faculty=faculty, department_name="Computer Science")
        Programme.objects.create(department=department, programme_name="Computer Science")

    def test_department_label(self):
        programme = get_object_or_404(Programme, programme_name="Computer Science")
        field_label = programme._meta.get_field('department').verbose_name
        self.assertEqual(field_label, 'department')

    def test_programme_name_label(self):
        programme = get_object_or_404(Programme, programme_name="Computer Science")
        field_label = programme._meta.get_field('programme_name').verbose_name
        self.assertEqual(field_label, 'programme name')

    def test_programme_name_max_length(self):
        programme = get_object_or_404(Programme, programme_name="Computer Science")
        max_length = programme._meta.get_field('programme_name').max_length
        self.assertEqual(max_length, 100)


class StaffModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        faculty = Faculty.objects.create(faculty_name="Computing And Applied Sciences")
        department = Department.objects.create(faculty=faculty, department_name="Computer Science")
        user = User.objects.create_user(username="username", password="password")
        person = Person.objects.create(user=user, last_name="John", first_name="Doe", is_staff=False)
        Staff.objects.create(person=person, staff_id="ID01", post="Lecturer I", department=department)

    def test_person_label(self):
        staff = get_object_or_404(Staff, staff_id="ID01")
        field_label = staff._meta.get_field("person").verbose_name
        self.assertEqual(field_label, "person")

    def test_staff_id_label(self):
        staff = get_object_or_404(Staff, staff_id="ID01")
        field_label = staff._meta.get_field("staff_id").verbose_name
        self.assertEqual(field_label, "staff id")

    def test_staff_id_max_length(self):
        staff = get_object_or_404(Staff, staff_id="ID01")
        max_length = staff._meta.get_field("staff_id").max_length
        self.assertEqual(max_length, 10)

    def test_post_label(self):
        staff = get_object_or_404(Staff, staff_id="ID01")
        field_label = staff._meta.get_field("post").verbose_name
        self.assertEqual(field_label, "post")

    def test_post_max_length(self):
        staff = get_object_or_404(Staff, staff_id="ID01")
        max_length = staff._meta.get_field("post").max_length
        self.assertEqual(max_length, 25)

    def test_department_label(self):
        staff = get_object_or_404(Staff, staff_id="ID01")
        field_label = staff._meta.get_field("department").verbose_name
        self.assertEqual(field_label, "department")


class StudentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        faculty = Faculty.objects.create(faculty_name="Computing And Applied Sciences")
        department = Department.objects.create(faculty=faculty, department_name="Computer Science")
        programme = Programme.objects.create(department=department, programme_name="Computer Science")
        user1 = User.objects.create_user(username="usernam", password="passwor")
        person1 = Person.objects.create(user=user1, last_name="Joh", first_name="Do", is_staff=False)
        staff = Staff.objects.create(person=person1, staff_id="ID01", post="Lecturer I", department=department)
        course1 = Course.objects.create(course_name="course", course_code="CDG657", course_unit=2, level="100", department=department,
                              lecturer=staff)
        course2 = Course.objects.create(course_name="course2", course_code="CDG65", course_unit=2, level="200", department=department,
                                        lecturer=staff)
        user = User.objects.create_user(username="username", password="password")
        person = Person.objects.create(user=user, last_name="John", first_name="Doe", is_staff=False)
        student = Student.objects.create(person=person, matric_no="MAC54653", level="100", programme=programme)

    def test_person_label(self):
        student = get_object_or_404(Student, matric_no="MAC54653")
        field_label = student._meta.get_field("person").verbose_name
        self.assertEqual(field_label, "person")

    def test_matric_no_label(self):
        student = get_object_or_404(Student, matric_no="MAC54653")
        field_label = student._meta.get_field("matric_no").verbose_name
        self.assertEqual(field_label, "matric no")

    def test_matric_no_max_length(self):
        student = get_object_or_404(Student, matric_no="MAC54653")
        max_length = student._meta.get_field("matric_no").max_length
        self.assertEqual(max_length, 10)

    def test_programme_label(self):
        student = get_object_or_404(Student, matric_no="MAC54653")
        field_label = student._meta.get_field("programme").verbose_name
        self.assertEqual(field_label, "programme")


class CourseModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        faculty = Faculty.objects.create(faculty_name="Computing And Applied Sciences")
        department = Department.objects.create(faculty=faculty, department_name="Computer Science")
        user = User.objects.create_user(username="username", password="password")
        person = Person.objects.create(user=user, last_name="John", first_name="Doe", is_staff=False)
        staff = Staff.objects.create(person=person, staff_id="ID01", post="Lecturer I",
                                     department=department)
        Course.objects.create(course_name="course", course_code="CDG657", course_unit=2, level="100", department=department,
                              lecturer=staff)

    def test_course_name_label(self):
        course = get_object_or_404(Course, course_name="course")
        field_label = course._meta.get_field("course_name").verbose_name
        self.assertEqual(field_label, "course name")

    def test_course_name_max_length(self):
        course = get_object_or_404(Course, course_name="course")
        max_length = course._meta.get_field("course_name").max_length
        self.assertEqual(max_length, 100)

    def test_course_code_label(self):
        course = get_object_or_404(Course, course_name="course")
        field_label = course._meta.get_field("course_code").verbose_name
        self.assertEqual(field_label, "course code")

    def test_course_code_max_length(self):
        course = get_object_or_404(Course, course_name="course")
        max_length = course._meta.get_field("course_code").max_length
        self.assertEqual(max_length, 7)

    def test_course_unit_label(self):
        course = get_object_or_404(Course, course_name="course")
        field_label = course._meta.get_field("course_unit").verbose_name
        self.assertEqual(field_label, "course unit")

    def test_level_label(self):
        course = get_object_or_404(Course, course_name="course")
        field_label = course._meta.get_field("level").verbose_name
        self.assertEqual(field_label, "level")

    def test_level_max_length(self):
        course = get_object_or_404(Course, course_name="course")
        max_length = course._meta.get_field("level").max_length
        self.assertEqual(max_length, 3)

    def test_semester_label(self):
        course = get_object_or_404(Course, course_name="course")
        field_label = course._meta.get_field("semester").verbose_name
        self.assertEqual(field_label, "semester")

    def test_semester_max_length(self):
        course = get_object_or_404(Course, course_name="course")
        max_length = course._meta.get_field("semester").max_length
        self.assertEqual(max_length, 3)

    def test_department_label(self):
        course = get_object_or_404(Course, course_name="course")
        field_label = course._meta.get_field("department").verbose_name
        self.assertEqual(field_label, "department")

    def test_lecturer_label(self):
        course = get_object_or_404(Course, course_name="course")
        field_label = course._meta.get_field("lecturer").verbose_name
        self.assertEqual(field_label, "lecturer")


class RegisteredStudentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        faculty = Faculty.objects.create(faculty_name="Computing And Applied Sciences")
        department = Department.objects.create(faculty=faculty, department_name="Computer Science")
        programme = Programme.objects.create(department=department, programme_name="Computer Science")
        user = User.objects.create_user(username="username", password="password")
        person = Person.objects.create(user=user, last_name="John", first_name="Doe", is_staff=False)
        staff = Staff.objects.create(person=person, staff_id="ID01", post="Lecturer I",
                                     department=department)
        course = Course.objects.create(course_name="course", course_code="CDG657", course_unit=2, level="100", department=department,
                                       lecturer=staff)
        user2 = User.objects.create_user(username="usernam", password="passwor")
        person2 = Person.objects.create(user=user2, last_name="John", first_name="Doe", is_staff=False)
        student1 = Student.objects.create(person=person2, matric_no="MAC54653", programme=programme)
        user3 = User.objects.create_user(username="userna", password="passwo")
        person3 = Person.objects.create(user=user3, last_name="John", first_name="Doe", is_staff=False)
        student2 = Student.objects.create(person=person3, matric_no="MAC54343", programme=programme)
        registered_students = RegisteredStudent.objects.create(course=course)
        registered_students.students.add(student1)
        registered_students.students.add(student2)

    def test_course_label(self):
        course = get_object_or_404(Course, course_name="course")
        registered_student = get_object_or_404(RegisteredStudent, course=course)
        field_label = registered_student._meta.get_field("course").verbose_name
        self.assertEqual(field_label, "course")

    def test_students_label(self):
        course = get_object_or_404(Course, course_name="course")
        registered_student = get_object_or_404(RegisteredStudent, course=course)
        field_label = registered_student._meta.get_field("students").verbose_name
        self.assertEqual(field_label, "students")

    def test_session_label(self):
        course = get_object_or_404(Course, course_name="course")
        registered_student = get_object_or_404(RegisteredStudent, course=course)
        field_label = registered_student._meta.get_field("session").verbose_name
        self.assertEqual(field_label, "session")

    def test_session_max_length(self):
        course = get_object_or_404(Course, course_name="course")
        registered_student = get_object_or_404(RegisteredStudent, course=course)
        max_length = registered_student._meta.get_field("session").max_length
        self.assertEqual(max_length, 10)


class StudentAttendanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        faculty = Faculty.objects.create(faculty_name="Computing And Applied Sciences")
        department = Department.objects.create(faculty=faculty, department_name="Computer Science")
        programme = Programme.objects.create(department=department, programme_name="Computer Science")
        user = User.objects.create_user(username="username", password="password")
        person = Person.objects.create(user=user, last_name="John", first_name="Doe", is_staff=False)
        student = Student.objects.create(person=person, matric_no="MAC54653", programme=programme)
        StudentAttendance.objects.create(student=student, date=timezone.now())

    def test_student_label(self):
        student = get_object_or_404(Student, matric_no="MAC54653")
        student_attendance = get_object_or_404(StudentAttendance, student=student)
        field_label = student_attendance._meta.get_field("student").verbose_name
        self.assertEqual(field_label, "student")

    def test_is_present_label(self):
        student = get_object_or_404(Student, matric_no="MAC54653")
        student_attendance = get_object_or_404(StudentAttendance, student=student)
        field_label = student_attendance._meta.get_field("is_present").verbose_name
        self.assertEqual(field_label, "is present")

    def test_date_label(self):
        student = get_object_or_404(Student, matric_no="MAC54653")
        student_attendance = get_object_or_404(StudentAttendance, student=student)
        field_label = student_attendance._meta.get_field("date").verbose_name
        self.assertEqual(field_label, "date")

    def test_session_label(self):
        student = get_object_or_404(Student, matric_no="MAC54653")
        student_attendance = get_object_or_404(StudentAttendance, student=student)
        field_label = student_attendance._meta.get_field("session").verbose_name
        self.assertEqual(field_label, "session")

    def test_session_max_length(self):
        student = get_object_or_404(Student, matric_no="MAC54653")
        student_attendance = get_object_or_404(StudentAttendance, student=student)
        max_length = student_attendance._meta.get_field("session").max_length
        self.assertEqual(max_length, 10)


class CourseAttendanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        faculty = Faculty.objects.create(faculty_name="Computing And Applied Sciences")
        department = Department.objects.create(faculty=faculty, department_name="Computer Science")
        programme = Programme.objects.create(department=department, programme_name="Computer Science")
        user = User.objects.create_user(username="username", password="password")
        person = Person.objects.create(user=user, last_name="John", first_name="Doe", is_staff=False)
        staff = Staff.objects.create(person=person, staff_id="ID01", post="Lecturer I",
                                     department=department)
        course = Course.objects.create(course_name="course", course_code="CDG657", course_unit=2, level="100", department=department,
                                       lecturer=staff)
        person2 = Person.objects.create(user=user, last_name="John", first_name="Doe", is_staff=False)
        student = Student.objects.create(person=person2, matric_no="MAC54653", programme=programme)
        student_attendance1 = StudentAttendance.objects.create(student=student, date=timezone.now())
        course_att = CourseAttendance.objects.create(course=course, date=timezone.now())
        course_att.student_attendance.add(student_attendance1)

    def test_course_label(self):
        course = get_object_or_404(Course, course_name="course")
        course_attendance = get_object_or_404(CourseAttendance, course=course)
        field_label = course_attendance._meta.get_field("course").verbose_name
        self.assertEqual(field_label, "course")

    def test_student_attendance_label(self):
        course = get_object_or_404(Course, course_name="course")
        course_attendance = get_object_or_404(CourseAttendance, course=course)
        field_label = course_attendance._meta.get_field("student_attendance").verbose_name
        self.assertEqual(field_label, "student attendance")

    def test_date_label(self):
        course = get_object_or_404(Course, course_name="course")
        course_attendance = get_object_or_404(CourseAttendance, course=course)
        field_label = course_attendance._meta.get_field("date").verbose_name
        self.assertEqual(field_label, "date")

    def test_session_label(self):
        course = get_object_or_404(Course, course_name="course")
        course_attendance = get_object_or_404(CourseAttendance, course=course)
        field_label = course_attendance._meta.get_field("session").verbose_name
        self.assertEqual(field_label, "session")

    def test_session_max_length(self):
        course = get_object_or_404(Course, course_name="course")
        course_attendance = get_object_or_404(CourseAttendance, course=course)
        max_length = course_attendance._meta.get_field("session").max_length
        self.assertEqual(max_length, 10)

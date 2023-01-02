from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone

from Attendance.extra import ContentTypeRestrictedFileField


class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    image = ContentTypeRestrictedFileField(upload_to='AttendanceSystem/profile-image',
                                           max_upload_size=5242880,
                                           content_types=['image/jpeg', 'image/jpg', 'image/png'],
                                           null=True,
                                           blank=True,
                                           max_length=250)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Faculty(models.Model):
    faculty_name = models.CharField(max_length=100, null=False, blank=False, choices=[
        ('Computing And Applied Sciences', 'Computing And Applied Sciences'),
        ('Arts, Management And Social Sciences', 'Arts, Management And Social Sciences'),
    ])

    def __str__(self):
        return self.faculty_name


class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=50, null=False, blank=False, choices=[
        ('Computer Science', 'Computer Science'),
        ('Biological Science', 'Biological Science'),
        ('Chemical Science', 'Chemical Science'),
        ('Business Administration', 'Business Administration'),
        ('Mass Communication', 'Mass Communication'),
        ('Criminology', 'Criminology'),
        ('Accounting', 'Accounting'),
    ])

    def __str__(self):
        return self.department_name


class Programme(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    programme_name = models.CharField(max_length=100, null=False, blank=False, choices=[
        ('Computer Science', 'Computer Science'),
        ('Software Engineering', 'Software Engineering'),
        ('Cyber Security', 'Cyber Security'),
        ('Biochemistry', 'Biochemistry'),
        ('Industrial Chemistry', 'Industrial Chemistry'),
        ('Business Administration', 'Business Administration'),
        ('Mass Communication', 'Mass Communication'),
        ('Criminology', 'Criminology'),
        ('Microbiology', 'Microbiology'),
        ('Economics', 'Economics'),
        ('Accounting', 'Accounting'),
    ])

    def __str__(self):
        return self.programme_name


class Staff(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=10, null=False, blank=False)
    post = models.CharField(max_length=25, null=False, blank=False, choices=[
        ('Lecturer I', 'Lecturer I'),
        ('Lecturer II', 'Lecturer II'),
    ])
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.staff_id


class Course(models.Model):
    course_name = models.CharField(max_length=100, null=False, blank=False)
    course_code = models.CharField(max_length=7, null=False, blank=False)
    course_unit = models.IntegerField()
    level = models.CharField(max_length=3, null=False, blank=False, choices=[
        ('100', '100'),
        ('200', '200'),
        ('300', '300'),
        ('400', '400'),
    ])
    semester = models.CharField(max_length=3, null=False, blank=False, choices=[
        ('1st', '1st'),
        ('2nd', '2nd'),
    ])
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_code


class Student(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    matric_no = models.CharField(max_length=10, null=False, blank=False)
    level = models.CharField(max_length=3, null=False, blank=False, choices=[
        ('100', '100'),
        ('200', '200'),
        ('300', '300'),
        ('400', '400'),
    ])
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)

    def __str__(self):
        return self.matric_no


class RegisteredCourses(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    session = models.CharField(max_length=10, null=False, blank=False, default='2022/2023', choices=[
        ('2022/2023', '2022/2023'),
        ('2023/2024', '2023/2024'),
        ('2024/2025', '2024/2025'),
        ('2025/2026', '2025/2026'),
        ('2026/2027', '2026/2027'),
        ('2027/2028', '2027/2028'),
        ('2028/2029', '2028/2029'),
        ('2029/2030', '2029/2030'),
    ])


class RegisteredStudent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, null=True, blank=True)
    session = models.CharField(max_length=10, null=False, blank=False, default='2022/2023', choices=[
        ('2022/2023', '2022/2023'),
        ('2023/2024', '2023/2024'),
        ('2024/2025', '2024/2025'),
        ('2025/2026', '2025/2026'),
        ('2026/2027', '2026/2027'),
        ('2027/2028', '2027/2028'),
        ('2028/2029', '2028/2029'),
        ('2029/2030', '2029/2030'),
    ])

    def __str__(self):
        return f'{self.course}'


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)
    date = models.DateField()
    session = models.CharField(max_length=10, null=False, blank=False, default='2022/2023', choices=[
        ('2022/2023', '2022/2023'),
        ('2023/2024', '2023/2024'),
        ('2024/2025', '2024/2025'),
        ('2025/2026', '2025/2026'),
        ('2026/2027', '2026/2027'),
        ('2027/2028', '2027/2028'),
        ('2028/2029', '2028/2029'),
        ('2029/2030', '2029/2030'),
    ])

    def __str__(self):
        return f'{self.student} - {self.is_present}'


class CourseAttendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_attendance = models.ManyToManyField(StudentAttendance)
    date = models.DateField()
    session = models.CharField(max_length=10, null=False, blank=False, default='2022/2023', choices=[
        ('2022/2023', '2022/2023'),
        ('2023/2024', '2023/2024'),
        ('2024/2025', '2024/2025'),
        ('2025/2026', '2025/2026'),
        ('2026/2027', '2026/2027'),
        ('2027/2028', '2027/2028'),
        ('2028/2029', '2028/2029'),
        ('2029/2030', '2029/2030'),
    ])

    def __str__(self):
        return f'{self.course} - {self.date}'


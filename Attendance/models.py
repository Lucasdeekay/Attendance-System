from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from Attendance.extra import ContentTypeRestrictedFileField


session = '2022/2023'


class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250, null=False, blank=False)
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    is_staff = models.BooleanField(default=False)
    image = ContentTypeRestrictedFileField(upload_to='AttendanceSystem/profile-image',
                                           max_upload_size=5242880,
                                           content_types=['image/jpeg', 'image/jpg', 'image/png'],
                                           null=True,
                                           blank=True,
                                           max_length=250)

    def __str__(self):
        return f'{self.full_name}'


class Faculty(models.Model):
    faculty_name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.faculty_name


class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.department_name


class Programme(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    programme_name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.programme_name


class Staff(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=25, null=False, blank=False)
    designation = models.CharField(max_length=25)
    post = models.CharField(max_length=25)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.staff_id


class Course(models.Model):
    course_title = models.CharField(max_length=100, null=False, blank=False)
    course_code = models.CharField(max_length=10, null=False, blank=False)
    course_unit = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


    def __str__(self):
        return self.course_code


class CourseAllocation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='lecturer')
    others = models.ManyToManyField(Staff)
    session = models.CharField(max_length=10, default=session)

    def __str__(self):
        return f"{self.course}"


class Student(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    matric_no = models.CharField(max_length=10, null=False, blank=False)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    year_of_entry = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.matric_no


class RegisteredStudent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    semester = models.CharField(max_length=3, choices=[
        ('1st', '1st'),
        ('2nd', '2nd'),
    ])
    session = models.CharField(max_length=10, default=session)

    def __str__(self):
        return f'{self.course}'


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)
    date = models.DateField()
    session = models.CharField(max_length=10, default=session)

    def __str__(self):
        return f'{self.student} - {self.is_present}'


class CourseAttendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_attendance = models.ManyToManyField(StudentAttendance)
    date = models.DateField()
    time = models.TimeField()
    session = models.CharField(max_length=10, default=session)

    def __str__(self):
        return f'{self.course} - {self.date}'


class Password(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    recovery_password = models.CharField(max_length=12, null=False)
    time = models.DateTimeField(null=False)
    is_active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return f"{self.person} -> {self.recovery_password}"

    def expiry(self):
        if (timezone.now() - self.time) >= timezone.timedelta(hours=1):
            self.is_active = False
        else:
            pass
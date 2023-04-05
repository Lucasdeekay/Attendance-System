from django.contrib import admin
from .models import Staff, Student, Faculty, Programme, Department, StudentAttendance, Course, CourseAttendance, \
    RegisteredStudent, Person, Password, CourseAllocation


class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'gender', 'email', 'is_staff', 'image')


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_name',)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'department_name')


class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('department', 'programme_name')


class StaffAdmin(admin.ModelAdmin):
    list_display = ('person', 'staff_id', 'designation', 'post', 'department')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('person', 'matric_no', 'programme', 'year_of_entry')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_code', 'course_unit', 'department')


class CourseAllocationAdmin(admin.ModelAdmin):
    list_display = ('course', 'lecturer', 'session')


class RegisteredStudentsAdmin(admin.ModelAdmin):
    list_display = ('course', 'semester', 'session')


class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'is_present', 'date', 'session')


class CourseAttendanceAdmin(admin.ModelAdmin):
    list_display = ('course', 'date', 'time', 'session')


class PasswordAdmin(admin.ModelAdmin):
    list_display = ('person', 'recovery_password', 'time', 'is_active')


admin.site.register(Person, PersonAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseAllocation, CourseAllocationAdmin)
admin.site.register(RegisteredStudent, RegisteredStudentsAdmin)
admin.site.register(StudentAttendance, StudentAttendanceAdmin)
admin.site.register(CourseAttendance, CourseAttendanceAdmin)
admin.site.register(Password, PasswordAdmin)
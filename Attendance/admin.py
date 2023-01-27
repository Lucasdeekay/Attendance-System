from django.contrib import admin
from .models import Staff, Student, Faculty, Programme, Department, StudentAttendance, Course, CourseAttendance, \
    RegisteredStudent, Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'first_name', 'is_staff', 'image')


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_name',)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'department_name')


class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('department', 'programme_name')


class StaffAdmin(admin.ModelAdmin):
    list_display = ('person', 'staff_id', 'post')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('person', 'matric_no', 'level', 'programme')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_code', 'programme', 'lecturer')


class RegisteredStudentsAdmin(admin.ModelAdmin):
    list_display = ('course', 'session')


class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'is_present', 'date', 'session')


class CourseAttendanceAdmin(admin.ModelAdmin):
    list_display = ('course', 'date', 'session')


admin.site.register(Person, PersonAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(RegisteredStudent, RegisteredStudentsAdmin)
admin.site.register(StudentAttendance, StudentAttendanceAdmin)
admin.site.register(CourseAttendance, CourseAttendanceAdmin)

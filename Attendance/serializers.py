from rest_framework import serializers

from Attendance.models import Faculty, Department, Staff, Student, Course, StudentAttendance, CourseAttendance, \
    Programme, RegisteredStudent, Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class ProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programme
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class RegisteredStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredStudent
        fields = "__all__"


class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = "__all__"


class CourseAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAttendance
        fields = "__all__"

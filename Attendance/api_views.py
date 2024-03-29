from rest_framework import viewsets
from Attendance.models import Faculty, Department, Staff, Student, Course, StudentAttendance, CourseAttendance, \
    Programme, RegisteredStudent, Person, Password, CourseAllocation
from Attendance.serializers import FacultySerializer, DepartmentSerializer, StaffSerializer, StudentSerializer, \
    CourseSerializer, StudentAttendanceSerializer, CourseAttendanceSerializer, ProgrammeSerializer, \
    RegisteredStudentSerializer, PersonSerializer, PasswordSerializer, CourseAllocationSerializer


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class FacultyViewSet(viewsets.ModelViewSet):
    serializer_class = FacultySerializer
    queryset = Faculty.objects.all()


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class ProgrammeViewSet(viewsets.ModelViewSet):
    serializer_class = ProgrammeSerializer
    queryset = Programme.objects.all()


class StaffViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseAllocationViewSet(viewsets.ModelViewSet):
    serializer_class = CourseAllocationSerializer
    queryset = CourseAllocation.objects.all()


class RegisteredStudentViewSet(viewsets.ModelViewSet):
    serializer_class = RegisteredStudentSerializer
    queryset = RegisteredStudent.objects.all()


class StudentAttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = StudentAttendanceSerializer
    queryset = StudentAttendance.objects.all()


class CourseAttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = CourseAttendanceSerializer
    queryset = CourseAttendance.objects.all()


class PasswordViewSet(viewsets.ModelViewSet):
    serializer_class = PasswordSerializer
    queryset = Password.objects.all()
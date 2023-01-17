from django.urls import path, include
from rest_framework import routers

from Attendance import views
from Attendance.views import DashboardView, AttendanceRegisterView, AttendanceSheetView, SettingsView, \
    PrintAttendanceSheetView, LoginView, LogoutView, RegisterCoursesView, RegisteredCoursesView, MailView
from Attendance.api_views import FacultyViewSet, DepartmentViewSet, StaffViewSet, StudentViewSet, CourseViewSet, \
    StudentAttendanceViewSet, CourseAttendanceViewSet, ProgrammeViewSet, RegisteredStudentViewSet, PersonViewSet, \
    RegisteredCoursesViewSet

app_name = 'Attendance'

router = routers.DefaultRouter()
router.register('person', PersonViewSet)
router.register('faculty', FacultyViewSet)
router.register('department', DepartmentViewSet)
router.register('programme', ProgrammeViewSet)
router.register('staff', StaffViewSet)
router.register('student', StudentViewSet)
router.register('course', CourseViewSet)
router.register('registered_courses', RegisteredCoursesViewSet)
router.register('registered_student', RegisteredStudentViewSet)
router.register('student_attendance', StudentAttendanceViewSet)
router.register('course_attendance', CourseAttendanceViewSet)

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('profile/settings', SettingsView.as_view(), name="settings"),
    path('profile/settings/mail', MailView.as_view(), name="mail"),
    path('profile/settings/mail/send', views.send_mail, name="send_mail"),
    path('profile/settings/update_password', views.update_password, name="update_password"),
    path('profile/settings/update_image', views.update_image, name="update_image"),
    path('course_registration', RegisterCoursesView.as_view(), name="register_courses"),
    path('course_registration/add_course', views.add_course, name="add_course"),
    path('course_registration/registered_courses', RegisteredCoursesView.as_view(), name="registered_courses"),
    path('course_registration/registered_courses/get', views.get_registered_courses, name="get_registered_courses"),
    path('course_registration/filter_by_semester', views.submit_semester, name="submit_semester"),
    path('attendance', AttendanceRegisterView.as_view(), name="attendance_register"),
    path('attendance/search', views.search_attendance_register, name="search_attendance_register"),
    path('attendance/validate', views.validate_checkbox, name="validate_checkbox"),
    path('attendance/get_attendance_records', views.get_attendance_records, name="get_attendance_records"),
    path('attendance/submit_course', views.submit_course, name="submit_course"),
    path('attendance/view', AttendanceSheetView.as_view(), name="attendance_sheet"),
    path('attendance/view/search', views.search_attendance_sheet, name="search_attendance_sheet"),
    path('attendance/print', PrintAttendanceSheetView.as_view(), name="print_attendance_sheet"),
    path('attendance/upload', views.upload_attendance_sheet, name="upload_attendance_sheet"),
    path('api/', include(router.urls))
]

from django.urls import path, include
from rest_framework import routers

from Attendance import views
from Attendance.views import DashboardView, AttendanceRegisterView, AttendanceSheetView, SettingsView, \
    PrintAttendanceSheetView, LoginView, LogoutView, MailView, ForgotPasswordView, CheckUserView
from Attendance.api_views import FacultyViewSet, DepartmentViewSet, StaffViewSet, StudentViewSet, CourseViewSet, \
    StudentAttendanceViewSet, CourseAttendanceViewSet, ProgrammeViewSet, RegisteredStudentViewSet, PersonViewSet

app_name = 'Attendance'

router = routers.DefaultRouter()
router.register('person', PersonViewSet)
router.register('faculty', FacultyViewSet)
router.register('department', DepartmentViewSet)
router.register('programme', ProgrammeViewSet)
router.register('staff', StaffViewSet)
router.register('student', StudentViewSet)
router.register('course', CourseViewSet)
router.register('registered_student', RegisteredStudentViewSet)
router.register('student_attendance', StudentAttendanceViewSet)
router.register('course_attendance', CourseAttendanceViewSet)

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('forgot_password/<int:id>', ForgotPasswordView.as_view(), name="forgot_password"),
    path('forgot_password/verify_user', CheckUserView.as_view(), name="verify_user"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('profile/settings', SettingsView.as_view(), name="settings"),
    path('profile/settings/mail', MailView.as_view(), name="mail"),
    path('profile/settings/mail/send', views.send_mail, name="send_mail"),
    path('profile/settings/update_password', views.update_password, name="update_password"),
    path('profile/settings/update_image', views.update_image, name="update_image"),
    path('profile/settings/upload', views.upload_file, name="upload_file"),
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

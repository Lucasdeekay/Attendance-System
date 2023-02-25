from django.urls import path, include
from rest_framework import routers

from Attendance import views
from Attendance.views import DashboardView, AttendanceRegisterView, AttendanceSheetView, SettingsView, \
    PrintAttendanceSheetView, LoginView, LogoutView, ForgotPasswordView, UploadView, \
    PasswordRetrievalView, UpdatePasswordView, TrackAttendanceView, UpdateRecordsView
from Attendance.api_views import FacultyViewSet, DepartmentViewSet, StaffViewSet, StudentViewSet, CourseViewSet, \
    StudentAttendanceViewSet, CourseAttendanceViewSet, ProgrammeViewSet, RegisteredStudentViewSet, PersonViewSet, \
    PasswordViewSet

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
router.register('password', PasswordViewSet)

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot_password'),
    path('forgot-password/<int:user_id>/retrieve-password', PasswordRetrievalView.as_view(), name='password_retrieval'),
    path('forgot-password/<int:user_id>/retrieve-password/update-password', UpdatePasswordView.as_view(), name='update_password'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('upload', UploadView.as_view(), name="upload"),
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('profile/settings', SettingsView.as_view(), name="settings"),
    path('profile/settings/update_password', views.update_password, name="update_password"),
    path('profile/settings/update_image', views.update_image, name="update_image"),
    path('profile/settings/upload', views.upload_file, name="upload_file"),
    path('profile/settings/register_student', views.register_student, name="register_student"),
    path('attendance', AttendanceRegisterView.as_view(), name="attendance_register"),
    path('attendance/search', views.search_attendance_register, name="search_attendance_register"),
    path('attendance/validate', views.validate_checkbox, name="validate_checkbox"),
    path('attendance/get_attendance_records', views.get_attendance_records, name="get_attendance_records"),
    path('attendance/submit_course', views.submit_course, name="submit_course"),
    path('attendance/view', AttendanceSheetView.as_view(), name="attendance_sheet"),
    path('attendance/view/search', views.search_attendance_sheet, name="search_attendance_sheet"),
    path('attendance/track_student', TrackAttendanceView.as_view(), name="track_attendance"),
    path('attendance/track_student/search', views.get_students, name="get_students"),
    path('attendance/track_student/view_attendance', views.get_student_attendance, name="get_student_attendance"),
    path('attendance/print', PrintAttendanceSheetView.as_view(), name="print_attendance_sheet"),
    path('attendance/upload', views.upload_attendance_sheet, name="upload_attendance_sheet"),
    path('attendance/update_records', UpdateRecordsView.as_view(), name="update_records"),
    path('attendance/admin/add_student', views.add_student, name="add_student"),
    path('attendance/admin/add_staff', views.add_staff, name="add_staff"),
    path('api/', include(router.urls))
]

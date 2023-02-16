import datetime
import io
import xlsxwriter

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from Attendance.forms import LoginForm, UpdatePasswordForm, StaffRegisterForm, StudentRegisterForm
from Attendance.functions import get_number_of_course_attendance_absent, get_number_of_ineligible_students, \
    get_number_of_eligible_students, get_number_of_course_attendance_present, \
    get_number_of_course_attendance_percentage, upload_attendance, upload_student, upload_staff, upload_course, \
    upload_department, upload_registered_students, upload_programme, upload_faculty
from Attendance.models import Staff, Course, RegisteredStudent, CourseAttendance, Student, \
    StudentAttendance, Person, Programme
from Attendance.utils import render_to_pdf

from AttendanceSystem.settings import EMAIL_HOST_USER


# Create a login view
class LoginView(View):
    # Add template name
    template_name = 'auth_login.html'

    # Create get function
    def get(self, request):
        # Check if user is logged in
        if request.user.is_authenticated:
            # Redirect back to dashboard if true
            return HttpResponseRedirect(reverse('Attendance:dashboard'))
        # Otherwise
        else:
            #  Get login form
            form = LoginForm()
            # load the page with the form
            return render(request, self.template_name, {'form': form})

    # Create post function to process te form on submission
    def post(self, request):
        # Get the submitted form
        form = LoginForm(request.POST)
        #  Check if the form is valid
        if form.is_valid():
            # Process the input
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password'].strip()
            # Authenticate the user login details
            user = authenticate(request, username=username, password=password)
            # Check if user exists
            if user is not None:
                # Log in the user
                login(request, user)
                # Redirect to dashboard page
                return HttpResponseRedirect(reverse('Attendance:dashboard'))
            # If user does not exist
            else:
                # Create an error message
                messages.error(request, "Invalid login details")
                # Redirect back to the login page
                return HttpResponseRedirect(reverse('Attendance:login'))


# Create a forgot password view
class ForgotPasswordView(View):
    # Add template name
    template_name = 'forgot_password.html'

    # Create get function
    def get(self, request, id):
        form = UpdatePasswordForm()
        # load the page with the form
        return render(request, self.template_name, {'form': form})

    # Create post function to process the form on submission
    def post(self, request, id):
        # Get the submitted form
        form = UpdatePasswordForm(request.POST)
        #  Check if the form is valid
        if form.is_valid():
            # Get user input
            password = form.cleaned_data['password'].strip()
            confirm_password = form.cleaned_data['confirm_password'].strip()
            # Check if both passwords match
            if password == confirm_password:
                user = get_object_or_404(User, id=id)
                # Update password
                user.set_password(password)
                # Save updated data
                user.save()

                messages.success(request, "Password successfully updated")

                # Redirect back to dashboard if true
                return HttpResponseRedirect(reverse('Attendance:login'))

            else:
                messages.success(request, "Password does not match")

                # Redirect back to dashboard if true
                return HttpResponseRedirect(reverse('Attendance:forgot_password'))


class CheckUserView(View):
    # Add template name
    template_name = 'verify_user.html'

    def get(self, request):
        # Check if user is logged in
        if request.user.is_authenticated:
            # Redirect back to dashboard if true
            return HttpResponseRedirect(reverse('Attendance:dashboard'))
        # Otherwise
        else:
            # load the page with the form
            return render(request, self.template_name)

    def post(self, request):
        user_id = request.POST.get('user_id')
        try:
            staff = get_object_or_404(Staff, staff_id=user_id)
            user = staff.person.user
            return HttpResponseRedirect(reverse('Attendance:forgot_password', args=(user.id,)))
        except Exception:
            try:
                student = get_object_or_404(Student, matric_no=user_id)
                user = student.person.user
                return HttpResponseRedirect(reverse('Attendance:forgot_password', args=(user.id,)))
            except Exception:
                messages.error(request, "User does not exist")
                return HttpResponseRedirect(reverse('Attendance:verify_user'))


# Create a dashboard view
class DashboardView(View):
    # Add template name
    template_name = 'dashboard.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Get today's date
        date = timezone.now().date().today()
        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            staff = get_object_or_404(Staff, person=person)
            programmes = Programme.objects.filter(department=staff.department)
            #  Filter all the courses in staff department
            courses = Course.objects.filter(department=staff.department)
            # Get all the course codes
            course_codes = [
                x.course_code for x in courses
            ]
            # Get the total number of students for each course
            course_total_students = [
                len(RegisteredStudent.objects.get(course=x).students.all()) for x in courses if
                RegisteredStudent.objects.filter(course=x).count() > 0
            ]
            # Get the number of programs offering each course
            course_total_programs = []
            for course in courses:
                if RegisteredStudent.objects.filter(course=course).count() > 0:
                    students = RegisteredStudent.objects.get(course=course).students.all()
                    program_list = []
                    for student in students:
                        program_list.append(student.programme)
                    course_total_programs.append(len(set(program_list)))

            eligible_status = [
                get_number_of_eligible_students(x) for x in courses if
                RegisteredStudent.objects.filter(course=x).count() > 0
            ]

            ineligible_status = [
                get_number_of_ineligible_students(x) for x in courses if
                RegisteredStudent.objects.filter(course=x).count() > 0
            ]

            zipped = zip(course_codes, course_total_students, course_total_programs, eligible_status, ineligible_status)
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': staff,
                'zipped': zipped,
                'eligible': sum(eligible_status),
                'ineligible': sum(ineligible_status),
                'courses': courses,
                'date': date,
            }
        # Otherwise
        else:
            # Get the current logged in student
            student = get_object_or_404(Student, person=person)
            try:
                # Get all the registered courses by the student
                reg_students = RegisteredStudent.objects.all()
                # Get all the courses taken by the student
                courses = [
                    x.course for x in reg_students if student in x.students.all()
                ]
                # Get all the course codes
                course_codes = [
                    x.course_code for x in courses
                ]
                # Get the number of times present for each course
                course_attendance_present = [
                    get_number_of_course_attendance_present(x, student) for x in courses
                ]
                # Get the number of times absent for each course
                course_attendance_absent = [
                    get_number_of_course_attendance_absent(x, student) for x in courses
                ]
                # Get the percentage of attendance for each course
                course_attendance_percentage = [
                    get_number_of_course_attendance_percentage(x, student) for x in courses
                ]
                no_of_eligible_courses = [
                    x for x in course_attendance_percentage if x >= 75
                ]
                no_of_ineligible_courses = [
                    x for x in course_attendance_percentage if x < 75
                ]
                zipped = zip(course_codes, course_attendance_present, course_attendance_absent,
                             course_attendance_percentage)
            except Exception:
                courses = {}
                zipped = []
                no_of_eligible_courses = [0]
                no_of_ineligible_courses = [0]

            # Create a dictionary of data to be accessed on the page
            context = {
                'user': student,
                'zipped': zipped,
                'courses': courses,
                'eligible': len(no_of_eligible_courses),
                'ineligible': len(no_of_ineligible_courses),
                'date': date,
            }
        # Load te page with the data
        return render(request, self.template_name, context)


# Create a attendance register view
class AttendanceRegisterView(View):
    # Add template name
    template_name = 'attendance_register.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            current_staff = get_object_or_404(Staff, person=person)
            #  Filter all the courses in staff department
            courses = Course.objects.filter(department=current_staff.department)
            # Get the current date
            date = timezone.now().date().today()
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': current_staff,
                'date': date,
                'courses': courses,
            }
            # login to te page with the data
            return render(request, self.template_name, context)
        # Otherwise
        else:
            # Redirect to dashboard
            return HttpResponseRedirect(reverse("Attendance:dashboard"))


# Create function view to process ajax request
def submit_course(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get the user input
        course_code = request.POST.get("course").upper()
        date_input = request.POST.get('date')

        course_code = " ".join([course_code[:3], course_code[-3:]])

        # Get the course using the course code
        course = get_object_or_404(Course, course_code=course_code)
        # split the date input and convert to datetime object
        user_date = date_input.split('-')
        user_date = datetime.date(int(user_date[0]), int(user_date[1]), int(user_date[2]))

        # Get the registered students for the course
        student_records = get_object_or_404(RegisteredStudent, course=course)
        # Use a try block
        try:
            # Get course attendance for the course for today
            course_attendance = get_object_or_404(CourseAttendance, date=user_date, course=course)
            # Get a list of all the ids of students in the course attendance
            student_attendance_ids = course_attendance.student_attendance.values_list('student')
            # Create a list 2d list containing each student name and matric no
            student_bio = [
                [get_object_or_404(Student, id=x[0]).person.full_name,
                 get_object_or_404(Student, id=x[0]).matric_no] for x in student_attendance_ids
            ]
            # Create a dictionary of data containing the list of all registered student for the course
            # and the list of individual attendance for the course
            context = {
                'student_records': list(student_records.students.all().values()),
                'student_attendance': list(course_attendance.student_attendance.all().values_list()),
                'student_bio': student_bio,
                'date': date_input,
                'course': course_code,
            }
            # return data back to the page
            return JsonResponse(context)
        # If course attendance has not been created before
        except Exception:
            # Create course attendance for the course for today
            course_attendance = CourseAttendance.objects.create(course=course, date=user_date)
            # Loop through all the registered students
            for std in student_records.students.values():
                student = get_object_or_404(Student, matric_no=std['matric_no'])
                # Create a student attendance for each student
                student_attendance = StudentAttendance.objects.create(student=student, is_present=False, date=user_date)
                # Add the individual student attendance to the course attendance
                course_attendance.student_attendance.add(student_attendance)

            student_records = student_records.students.all()
            # Get all students records
            student_bio = [
                [x.person.full_name, x.matric_no] for x in student_records
            ]

            # Create a dictionary of data containing the list of all registered student for the course
            # and the list of individual attendance for the course
            context = {
                'student_records': list(student_records.values()),
                'student_attendance': list(course_attendance.student_attendance.all().values_list()),
                'student_bio': student_bio,
                'date': date_input,
                'course': course_code,
            }
            # return data back to the page
            return JsonResponse(context)


# Create function view to process ajax request
def search_attendance_register(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get user input
        course_code = request.POST.get('course').upper()
        date_input = request.POST.get('date')
        text = request.POST.get('text')
        mode = request.POST.get('searchMethod')

        course_code = " ".join([course_code[:3], course_code[-3:]])

        # Get the course using the course code
        course = get_object_or_404(Course, course_code=course_code)
        # split the date input and convert to datetime object
        user_date = date_input.split('-')
        user_date = datetime.date(int(user_date[0]), int(user_date[1]), int(user_date[2]))
        # Get the registered students for the course
        registered_students = get_object_or_404(RegisteredStudent, course=course)
        # Get the required course attendance using the course and converted date
        course_attendance = get_object_or_404(CourseAttendance, course=course, date=user_date)

        # Check mode
        if mode == 'matric_no':
            try:
                # Get the search results
                students = Student.objects.filter(matric_no__icontains=text)

                student_records = [
                    [x.person.full_name, x.matric_no] for x in students if x in registered_students.students.all()
                ]

                student_attendance = [
                    [course_attendance.student_attendance.get(student=x).id,
                     course_attendance.student_attendance.get(student=x).is_present] for x in students if
                    x in registered_students.students.all()
                ]

                # Create a dictionary of data to be returned to the page
                context = {
                    'student_records': student_records,
                    'student_attendance': student_attendance,
                }
                # return data back to page
                return JsonResponse(context)
            # if course attendance does not exist
            except Exception:
                return JsonResponse({'student_records': []})
        else:
            try:
                # Filter search
                persons = Person.objects.filter(full_name__icontains=text)

                students = [
                    get_object_or_404(Student, person=x) for x in persons
                ]

                student_records = [
                    [x.person.full_name, x.matric_no] for x in students if
                    x in registered_students.students.all()
                ]

                student_attendance = [
                    [course_attendance.student_attendance.get(student=x).id,
                     course_attendance.student_attendance.get(student=x).is_present] for x in students if
                    x in registered_students.students.all()
                ]
                # Create a dictionary of data to be returned to the page
                context = {
                    'student_records': student_records,
                    'student_attendance': student_attendance,
                }
                # return data back to page
                return JsonResponse(context)
            except Exception:
                return JsonResponse({'student_attendance': []})


# Create function view to process ajax request
def validate_checkbox(request):
    # check if request method is POST
    if request.method == 'POST':
        # Get user input
        student_id = request.POST.get('id')
        is_present = request.POST.get('value')
        # Get attendance details of current student
        student = get_object_or_404(StudentAttendance, id=student_id)

        # Toggle and update the student attendance in response to clicking on the checkbox
        if is_present == 'true':
            student.is_present = False
        else:
            student.is_present = True

        # Save the updated data
        student.save()
        print(student)

        # Create a dictionary of data to be returned to the page
        context = {
            'msg': f"{student.student.matric_no}'s attendance status updated",
            'color': 'alert alert-success',
        }
        # return data back to page
        return JsonResponse(context)


# Create an attendance sheet view
class AttendanceSheetView(View):
    # Add template name
    template_name = 'attendance_sheet.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            current_staff = get_object_or_404(Staff, person=person)
            #  Filter all the courses in staff department
            courses = Course.objects.filter(department=current_staff.department)
            # Get the current date
            date = timezone.now().date().today()
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': current_staff,
                'date': date,
                'courses': courses,
            }
            # login to te page with the data
            return render(request, self.template_name, context)
        # Otherwise
        else:
            # Redirect to dashboard
            return HttpResponseRedirect(reverse("Attendance:dashboard"))


# Create function view to process ajax request
def get_attendance_records(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get user input
        course_code = request.POST.get('course').upper()
        date_input = request.POST.get('date')

        course_code = " ".join([course_code[:3], course_code[-3:]])

        # Get the course using the course code
        course = get_object_or_404(Course, course_code=course_code)
        # split the date input and convert to datetime object
        user_date = date_input.split('-')
        user_date = datetime.date(int(user_date[0]), int(user_date[1]), int(user_date[2]))

        # use a try block
        try:
            # Get the required course attendance using the course and converted date
            course_attendance = get_object_or_404(CourseAttendance, course=course, date=user_date)
            # Get a list of all the ids of students in the course attendance
            student_attendance_ids = course_attendance.student_attendance.values_list('student')
            # Get a list of the current attendance status of all the students offering the course
            student_attendance_status = course_attendance.student_attendance.values_list('is_present')
            # Create a list 2d list containing each student name and matric no
            student_attendance_info = [
                [get_object_or_404(Student, id=x[0]).person.full_name,
                 get_object_or_404(Student, id=x[0]).matric_no] for x in student_attendance_ids
            ]

            # Create a dictionary of data to be returned to the page
            context = {
                'student_attendance_status': list(student_attendance_status),
                'student_attendance_info': student_attendance_info,
                'date': date_input,
                'course': course_code,
            }
            # return data back to page
            return JsonResponse(context)
        # if course attendance does not exist
        except Exception:
            return JsonResponse({'student_attendance_info': []})


# Create function view to process ajax request
def search_attendance_sheet(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get user input
        course_code = request.POST.get('course').upper()
        date_input = request.POST.get('date')
        text = request.POST.get('text')
        mode = request.POST.get('searchMethod')

        course_code = " ".join([course_code[:3], course_code[-3:]])

        # Get the course using the course code
        course = get_object_or_404(Course, course_code=course_code)
        # split the date input and convert to datetime object
        user_date = date_input.split('-')
        user_date = datetime.date(int(user_date[0]), int(user_date[1]), int(user_date[2]))
        # Get the registered students for the course
        registered_students = get_object_or_404(RegisteredStudent, course=course)
        # Get the required course attendance using the course and converted date
        course_attendance = get_object_or_404(CourseAttendance, course=course, date=user_date)

        # Check mode
        if mode == 'matric_no':
            try:
                # Get the search results
                students = Student.objects.filter(matric_no__icontains=text)
                student_attendance_info = [
                    [x.person.full_name, x.matric_no] for x in students if
                    x in registered_students.students.all()
                ]

                student_attendance_status = [
                    course_attendance.student_attendance.get(student=x).is_present for x in students if
                    x in registered_students.students.all()
                ]
                # Create a dictionary of data to be returned to the page
                context = {
                    'student_attendance_status': list(student_attendance_status),
                    'student_attendance_info': student_attendance_info,
                }
                # return data back to page
                return JsonResponse(context)
            # if course attendance does not exist
            except Exception:
                return JsonResponse({'student_attendance_info': []})
        else:
            try:
                # Filter search
                persons = Person.objects.filter(full_name__icontains=text)

                students = []
                for x in persons:
                    try:
                        std = get_object_or_404(Student, person=x)
                        students.append(std)
                    except Exception:
                        pass

                student_attendance_info = [
                    [x.person.full_name, x.matric_no] for x in students if
                    x in registered_students.students.all()
                ]

                student_attendance_status = [
                    course_attendance.student_attendance.get(student=x).is_present for x in students if
                    x in registered_students.students.all()
                ]
                # Create a dictionary of data to be returned to the page
                context = {
                    'student_attendance_status': list(student_attendance_status),
                    'student_attendance_info': student_attendance_info,
                }
                # return data back to page
                return JsonResponse(context)
            except Exception:
                return JsonResponse({'student_attendance_info': []})


# Create a settings view
class SettingsView(View):
    # Add template name
    template_name = 'settings.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        form = UpdatePasswordForm()
        # Get the current logged in staff
        person = get_object_or_404(Person, user=request.user)
        # Get the current date
        date = timezone.now().date().today()

        superuser = False
        if request.user.is_superuser:
            superuser = True

        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            staff = get_object_or_404(Staff, person=person)
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': staff,
                'date': date,
                'form': form,
                'superuser': superuser,
            }
        # Otherwise
        else:
            # Get the current logged in staff
            student = get_object_or_404(Student, person=person)
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': student,
                'date': date,
                'form': form,
                'superuser': superuser,
            }
        # login to te page with the data
        return render(request, self.template_name, context)


# Create function view to process ajax request
def update_password(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get the submitted form
        form = UpdatePasswordForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            # Get user input
            password = form.cleaned_data['password'].strip()
            confirm_password = form.cleaned_data['confirm_password'].strip()
            # Check if both passwords match
            if password == confirm_password:
                # Update password
                request.user.set_password(password)
                # Save updated data
                request.user.save()
                # Create a dictionary of data to be returned to the page
                context = {
                    'msg': "Password successfully changed",
                    'color': 'alert alert-success'
                }
                # return data back to page
                return JsonResponse(context)
            # If passwords do not match
            else:
                # Create a dictionary of data to be returned to the page
                context = {
                    'msg': "Password does not match",
                    'color': 'alert alert-danger'
                }
                # return data back to page
                return JsonResponse(context)


# Create function view to process ajax request
def update_image(request):
    # Get user input
    image = request.FILES.get('image')
    person = get_object_or_404(Person, user=request.user)
    person.image = image
    person.save()
    # Create a dictionary of data to be returned to the page
    messages.success(request, "Profile picture successfully updated")
    # return data back to page
    return HttpResponseRedirect(reverse("Attendance:settings"))


# Create post function to process the form on submission
def upload_file(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get user input
        file = request.FILES.get('file')
        file_type = request.POST.get('type')

        if file_type == "student":
            try:
                upload_student(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:settings"))
        elif file_type == "staff":
            try:
                upload_staff(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:settings"))
        elif file_type == "course":
            try:
                upload_course(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:settings"))
        elif file_type == "programme":
            try:
                upload_programme(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:settings"))
        elif file_type == "department":
            try:
                upload_department(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:settings"))
        elif file_type == "faculty":
            try:
                upload_faculty(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:settings"))
        elif file_type == "reg_student":
            try:
                upload_registered_students(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:settings"))

        messages.error(request, "File upload successful")
        return HttpResponseRedirect(reverse("Attendance:settings"))


# Create a mail view
class MailView(View):
    # Add template name
    template_name = 'mail.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Get the current date
        date = timezone.now().date().today()
        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            current_staff = get_object_or_404(Staff, person=person)
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': current_staff,
                'date': date,
            }
        # Otherwise
        else:
            # Get the current logged in student
            student = get_object_or_404(Student, person=person)
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': student,
                'date': date,
            }
        # login to te page with the data
        return render(request, self.template_name, context)


# Create a function to send mail
def send_mail(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get user input
        email = request.POST.get('email')
        title = request.POST.get('title')
        msg = request.POST.get('msg')

        context = {'title': title, 'msg': msg}
        html_message = render_to_string('email.html', context=context)
        send_mail(title, msg, EMAIL_HOST_USER, [email], html_message=html_message, fail_silently=False)

        # Create a dictionary of data to be returned to the page
        context = {
            'msg': "Mail has been successfully sent",
            'color': 'alert alert-success',
        }
        # return data back to page
        return JsonResponse(context)


# Create a print attendance sheet view
class PrintAttendanceSheetView(View):
    # Add template name
    template_name = 'print_attendance.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Get the current date
        date = timezone.now().date().today()
        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            current_staff = get_object_or_404(Staff, person=person)
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': current_staff,
                'date': date,
            }
        # Otherwise
        else:
            # Get the current logged in student
            student = get_object_or_404(Student, person=person)
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': student,
                'date': date,
            }

        # login to te page with the data
        return render(request, self.template_name, context)

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create post method to handle form submission
    def post(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Check if user is a staff
        if person.is_staff:
            # Get user input
            course_code = request.POST.get('course').upper()

            course_code = " ".join([course_code[:3], course_code[-3:]])

            try:
                # Get the course using the course code
                course = get_object_or_404(Course, course_code=course_code)
            except Exception:
                #  Create an error message
                messages.error(request, f"{course} does not exist")
                # Redirect back to the current page
                return HttpResponseRedirect(reverse('Attendance:print_attendance_sheet'))

            # Use a try block
            try:
                # Get course attendance for the course for specified date
                course_attendance = CourseAttendance.objects.filter(course=course).order_by("date")
                # Get all course attendance dates
                course_attendance_dates = CourseAttendance.objects.filter(course=course).order_by("date").values_list(
                    'date')
                # Get list of students offering course
                reg_students = RegisteredStudent.objects.get(course=course)
                reg_students = reg_students.students.all().order_by('matric_no')

                if len(course_attendance) == 0:
                    #  Create an error message
                    messages.error(request, f"Attendance for {course} does not exist")
                    # Redirect back to the current page
                    return HttpResponseRedirect(reverse('Attendance:print_attendance_sheet'))

            # If course attendance has not been created before
            except Exception:
                #  Create an error message
                messages.error(request, f"Attendance for {course} does not exist")
                # Redirect back to the current page
                return HttpResponseRedirect(reverse('Attendance:print_attendance_sheet'))

            # Create an in-memory output file for the workbook
            output = io.BytesIO()

            # Create an excel spreadsheet workbook
            attendance_book = xlsxwriter.Workbook(output)

            # Give the file created a name
            filename = f"{course}.xlsx"

            # Add a worksheet
            attendance_sheet = attendance_book.add_worksheet(f"{course}")

            # Instantiate the rows and columns
            row = col = 0

            # Create row headers
            attendance_sheet.write(row, col, "Last Name")
            attendance_sheet.write(row, col + 1, "First Name")
            attendance_sheet.write(row, col + 2, "Matric No")

            # Fill in the respective dates
            for index, date in enumerate(course_attendance_dates):
                date_col = 3
                attendance_sheet.write(row, date_col + index, date[0].strftime("%d/%m/%Y"))

            attendance_sheet.write(row, len(course_attendance_dates) + 3, "Eligiblity (%)")
            attendance_sheet.write(row, len(course_attendance_dates) + 4, "Eligible")

            # Fill in the names and matric_no
            for student in reg_students:
                attendance_sheet.write(row + 1, col, student.person.last_name)
                attendance_sheet.write(row + 1, col + 1, student.person.first_name)
                attendance_sheet.write(row + 1, col + 2, student.matric_no)

                row += 1

            date_col = 3
            # Loop through all attendance
            for att in course_attendance:
                date_row = 1
                # Loop through registered student for the course
                for student in reg_students:
                    try:
                        # Get current student attendance
                        std_att = att.student_attendance.get(student=student)
                        attendance_sheet.write(date_row, date_col, std_att.is_present)
                        date_row += 1
                    except Exception:
                        pass

                date_col += 1

            std_row = 1
            # Loop through registered student for the course
            for student in reg_students:
                present = get_number_of_course_attendance_percentage(course, student)
                attendance_sheet.write(std_row, len(course_attendance_dates) + 3, f"{present} %")
                if present < 75:
                    attendance_sheet.write(std_row, len(course_attendance_dates) + 4, "No")
                else:
                    attendance_sheet.write(std_row, len(course_attendance_dates) + 4, "Yes")

                std_row += 1

            # Close workbook
            attendance_book.close()

            # Rewind the buffer
            output.seek(0)

            # Set up the Http response informing the browser that this is xlsx file and not html file
            response = HttpResponse(
                output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename={filename}'

            # return response back to page
            return response

        else:
            # Get the current person logged in
            person = get_object_or_404(Person, user=request.user)
            # Get the current logged in student
            student = get_object_or_404(Student, person=person)
            # Get today's date
            date = timezone.now().date().today()
            try:
                # Get all the registered courses by the student
                reg_students = RegisteredStudent.objects.all()
                # Get all the courses taken by the student
                courses = [
                    x.course for x in reg_students if student in x.students.all()
                ]
                # Get all the course codes
                course_codes = [
                    x.course_code for x in courses
                ]
                # Get the percentage of attendance for each course
                course_attendance_percentage = [
                    get_number_of_course_attendance_percentage(x, student) for x in courses
                ]
                zipped = zip(course_codes, course_attendance_percentage)
            except Exception:
                courses = {}
                zipped = []

            # Create a dictionary of data to be accessed on the page
            context = {
                'user': student,
                'zipped': zipped,
                'courses': courses,
                'date': date,
            }

            open('templates/temp.html', "w").write(render_to_string('slip.html', context))

            # Converting the HTML template into a PDF file
            pdf = render_to_pdf('temp.html')

            response = HttpResponse(pdf, content_type='application/pdf')

            response['Content-Disposition'] = f'attachment; filename={student.person.full_name} Attendance Slip.pdf'

            # rendering the template
            return response


# create a function to handle upload of excel sheet
def upload_attendance_sheet(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get user input
        file = request.FILES.get('file')
        upload_attendance(file)

        messages.success(request, "File upload successful")
        # return data back to page
        return HttpResponseRedirect(reverse("Attendance:print_attendance_sheet"))


# Create a logout view
class LogoutView(View):

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # logout user
        logout(request)
        # redirect to login page
        return HttpResponseRedirect(reverse('Attendance:login'))


def error_404(request, exception):
    return render(request, 'error_400.html')


def error_500(request):
    return render(request, 'error_400.html')

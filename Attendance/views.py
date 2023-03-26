import datetime
import io
import string

import xlsxwriter

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from Attendance.forms import LoginForm, UpdatePasswordForm, StaffRegisterForm, StudentRegisterForm, ForgotPasswordForm, \
    PasswordRetrievalForm, UploadImageForm, ChangePasswordForm, UpdateEmailForm, UploadFileForm
from Attendance.functions import get_number_of_course_attendance_absent, get_number_of_course_attendance_present, \
    get_number_of_course_attendance_percentage, upload_student, upload_staff, upload_course, \
    upload_department, upload_programme, upload_faculty, upload_course_attendance, \
    upload_student_course_registration, get_spreadsheed_data_as_list, \
    get_number_of_unique_programs, get_list_of_unique_programs, get_total_number_of_students, allocate_courses, \
    get_all_selected_status
from Attendance.models import Staff, Course, RegisteredStudent, CourseAttendance, Student, \
    StudentAttendance, Person, Programme, Password, Department, CourseAllocation
from Attendance.utils import render_to_pdf

from AttendanceSystem.settings import EMAIL_HOST_USER

import random

random = random.Random()

session = '2022/2023'


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
                if user.check_password("password"):
                    # Create an error message
                    messages.error(request, "Kindly update your default password to enhance security")
                    # Redirect back to the login page
                    return HttpResponseRedirect(
                        reverse('Attendance:password_update_before_login', args=(user.username,)))
                else:
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
    def get(self, request):
        form = ForgotPasswordForm()
        # load the page with the form
        return render(request, self.template_name, {'form': form})

    # Create post function to process the form on submission
    def post(self, request):
        # Get the submitted form
        form = ForgotPasswordForm(request.POST)
        #  Check if the form is valid
        if form.is_valid():
            user_id = form.cleaned_data['user_id'].strip()
            email = form.cleaned_data['email'].strip()

            try:
                user = User.objects.get(username=user_id)
            except Exception:
                messages.error(request, "User does not exist")
                return HttpResponseRedirect(reverse('Attendance:forgot_password'))

            try:
                person = Person.objects.get(email=email)
            except Exception:
                messages.error(request, "Email does not exist")
                return HttpResponseRedirect(reverse('Attendance:forgot_password'))

            if user.username == user_id and person.email == email:
                person = Person.objects.get(user=user)
                recovery_password = ''.join(
                    [random.choice(string.ascii_letters + string.digits) for i in range(12)])
                subject = 'Password Recovery'

                if Password.objects.filter(is_active=True, person=person).count() > 0:
                    all_passwords = Password.objects.filter(is_active=True, person=person)
                    for password in all_passwords:
                        password.is_active = False

                Password.objects.create(person=person, recovery_password=recovery_password,
                                        time=timezone.now())

                msg = f"Recovery password will expire after an hour. Your password is displayed below"
                context = {'title': subject, 'msg': msg, 'recovery_password': recovery_password}
                html_message = render_to_string('email.html', context=context)

                send_mail(subject, msg, EMAIL_HOST_USER, [email], html_message=html_message, fail_silently=False)

                messages.success(request, "Recovery password has been successfully sent")

                # Redirect back to dashboard if true
                return HttpResponseRedirect(reverse('Attendance:password_retrieval', args=(user.id,)))

            else:
                messages.success(request, "Password does not match")

                # Redirect back to page
                return HttpResponseRedirect(reverse('Attendance:forgot_password'))


# Create a forgot password view
class LoginPasswordUpdateView(View):
    # Add template name
    template_name = 'password_update_before_login.html'

    # Create get function
    def get(self, request, username):
        form = UpdatePasswordForm()
        # load the page with the form
        return render(request, self.template_name, {'form': form})

    # Create post function to process the form on submission
    def post(self, request, username):
        # Check if request method is POST
        if request.method == "POST":
            user = User.objects.get(username=username)
            # Get the submitted form
            form = UpdatePasswordForm(request.POST)
            # Check if form is valid
            if form.is_valid():
                # Get user input
                old_password = form.cleaned_data['old_password'].strip()
                password = form.cleaned_data['password'].strip()
                confirm_password = form.cleaned_data['confirm_password'].strip()
                # Check if old password match
                if user.check_password(old_password):
                    if password == old_password:
                        # Create message report
                        messages.error(request, "Previous password cannot be used")
                        # return data back to page
                        return HttpResponseRedirect(
                            reverse('Attendance:password_update_before_login', args=(user.username,)))
                    elif password == "password":
                        # Create message report
                        messages.error(request, "Password cannot be 'password'")
                        # return data back to page
                        return HttpResponseRedirect(
                            reverse('Attendance:password_update_before_login', args=(user.username,)))
                    else:
                        # Check if both passwords match
                        if password == confirm_password:
                            # Update password
                            user.set_password(password)
                            # Save updated data
                            user.save()
                            # Create message report
                            messages.success(request, "Password successfully changed")
                            # return data back to page
                            return HttpResponseRedirect(reverse("Attendance:login"))
                        # If passwords do not match
                        else:
                            # Create message report
                            messages.error(request, "New password does not match")
                            # return data back to page
                            return HttpResponseRedirect(
                                reverse('Attendance:password_update_before_login', args=(user.username,)))
                # Otherwise
                else:
                    messages.error(request, "Old password entered does not match")
                    # return data back to page
                    return HttpResponseRedirect(
                        reverse('Attendance:password_update_before_login', args=(user.username,)))


# Create a password retrieval view
class PasswordRetrievalView(View):
    template_name = 'password_retrieval.html'

    def get(self, request, user_id):
        form = PasswordRetrievalForm()
        user = get_object_or_404(User, id=user_id)
        context = {'user': user, 'user_id': user_id, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        if request.method == 'POST':
            form = PasswordRetrievalForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password'].strip()
                all_password = Password.objects.all()
                user = get_object_or_404(User, id=user_id)
                person = get_object_or_404(Person, user=user)

                for passcode in all_password:
                    if passcode.person == person and passcode.recovery_password == password and passcode.is_active:
                        passcode.expiry()
                        subject = 'Password Recovery Successful'
                        msg = "Account has been successfully recovered. Kindly proceed to update your password"
                        context = {'title': subject, 'msg': msg}
                        html_message = render_to_string('email.html', context=context)

                        send_mail(subject, msg, EMAIL_HOST_USER, [person.email], html_message=html_message,
                                  fail_silently=False)

                        messages.success(request,
                                         'Account has been successfully recovered. Kindly update your password')
                        return HttpResponseRedirect(reverse('Attendance:update_password', args=(user_id,)))
                else:
                    messages.error(request,
                                   "Incorrect recovery password. Click on resend to get the retrieval password again")
                    return HttpResponseRedirect(reverse('Attendance:password_retrieval', args=(user_id,)))


# Create an update password view
class UpdatePasswordView(View):
    template_name = 'update_password.html'

    def get(self, request, user_id):
        form = ChangePasswordForm()
        user = get_object_or_404(User, id=user_id)
        context = {'user': user, 'user_id': user_id, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data['password'].strip()
                password2 = form.cleaned_data['confirm_password'].strip()

                if password1 == "password":
                    messages.error(request, "Password cannot be 'password'")
                    return HttpResponseRedirect(reverse('Attendance:update_password', args=(user_id,)))

                else:
                    if password1 == password2:
                        user = User.objects.get(id=user_id)
                        user.set_password(password1)
                        user.save()

                        subject = 'Password Update Successful'
                        msg = "Account password has  been successfully changed"
                        context = {'title': subject, 'msg': msg}
                        html_message = render_to_string('email.html', context=context)

                        send_mail(subject, msg, EMAIL_HOST_USER, [user.email], html_message=html_message,
                                  fail_silently=False)

                        messages.success(request, 'Password successfully changed')
                        return HttpResponseRedirect(reverse('Attendance:login'))
                    else:
                        messages.error(request, "Password does not match")
                        return HttpResponseRedirect(reverse('Attendance:update_password', args=(user_id,)))


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

        superuser = False
        is_staff = False
        if request.user.is_superuser:
            superuser = True
        if request.user.is_staff:
            is_staff = True

        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            staff = get_object_or_404(Staff, person=person)
            #  Filter all the courses in staff department
            course_allocation = CourseAllocation.objects.filter(lecturer=staff, session=session)
            courses = list(map(lambda x: x.course, course_allocation))

            # Get all the course codes
            course_codes = list(map(lambda x: x.course_code, courses))
            # Get the total number of students for each course
            course_total_students = list(map(lambda x: get_total_number_of_students(x), courses))
            course_total_programs = list(map(lambda x: get_number_of_unique_programs(x), courses))
            course_total_programs_list = list(map(lambda x: get_list_of_unique_programs(x), courses))

            zipped = zip(course_codes, course_total_students, course_total_programs, course_total_programs_list)
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': staff,
                'zipped': zipped,
                'courses': courses,
                'date': date,
                'superuser': superuser,
                'staff': is_staff,
            }
        # Otherwise
        else:
            # Get the current logged in student
            student = get_object_or_404(Student, person=person)
            try:
                # Get all the registered courses by the student
                reg_students = RegisteredStudent.objects.filter(session=session)

                courses = [
                    reg_std.course for reg_std in reg_students if student in reg_std.students.all()
                ]
                course_codes = [
                    reg_std.course.course_code for reg_std in reg_students if student in reg_std.students.all()
                ]
                course_attendance_present = [
                    get_number_of_course_attendance_present(reg_std.course, student) for reg_std in reg_students if
                    student in reg_std.students.all()
                ]
                course_attendance_absent = [
                    get_number_of_course_attendance_absent(reg_std.course, student) for reg_std in reg_students if
                    student in reg_std.students.all()
                ]
                course_attendance_percentage = [
                    get_number_of_course_attendance_percentage(reg_std.course, student) for reg_std in reg_students if
                    student in reg_std.students.all()
                ]
                no_of_eligible_courses = []
                no_of_ineligible_courses = []
                for percentage in course_attendance_percentage:
                    if percentage >= 75:
                        no_of_eligible_courses.append(percentage)
                    else:
                        no_of_ineligible_courses.append(percentage)

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
                'superuser': superuser,
                'staff': is_staff,
            }
        # Load te page with the data
        return render(request, self.template_name, context)


# Create a contact us view
class ContactView(View):
    # Add template name
    template_name = 'contact_us.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Get today's date
        date = timezone.now().date().today()

        superuser = False
        is_staff = False
        if request.user.is_superuser:
            superuser = True
        if request.user.is_staff:
            is_staff = True

        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            staff = get_object_or_404(Staff, person=person)

            # Create a dictionary of data to be accessed on the page
            context = {
                'user': staff,
                'date': date,
                'superuser': superuser,
                'staff': is_staff,
            }
        # Otherwise
        else:
            # Get the current logged in student
            student = get_object_or_404(Student, person=person)
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': student,
                'date': date,
                'superuser': superuser,
                'staff': is_staff,
            }
        # Load te page with the data
        return render(request, self.template_name, context)

    @method_decorator(login_required())
    # Create post function
    def post(self, request):
        person = Person.objects.get(user=request.user)
        admins = User.objects.filter(is_superuser=True)
        admin_mails = [
            Person.objects.get(user=user).email for user in admins if Person.objects.filter(user=user).count() > 0
        ]
        # Check if request method is POST
        if request.method == "POST":
            # Get user input
            msg = request.POST.get("text")
            title = f"MAIL TICKET FROM {person.full_name}"
            context = {'title': title, 'msg': msg}
            html_message = render_to_string('email.html', context=context)

            send_mail(title, msg, EMAIL_HOST_USER, admin_mails, html_message=html_message, fail_silently=False)

            messages.success(request, 'Mail has been successfully sent')
            return HttpResponseRedirect(reverse('Attendance:contact_us'))


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

        superuser = False
        is_staff = False
        if request.user.is_superuser:
            superuser = True
        if request.user.is_staff:
            is_staff = True

        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            current_staff = get_object_or_404(Staff, person=person)
            #  Filter all the courses in staff department
            course_allocation = CourseAllocation.objects.filter(lecturer=current_staff, session=session)
            courses = [
                course_all.course for course_all in course_allocation
            ]
            # Get the current date
            date = timezone.now().date().today()
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': current_staff,
                'date': date,
                'courses': courses,
                'superuser': superuser,
                'staff': is_staff,
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
        att_rec = request.POST.get('attrec')

        # Get the course using the course code
        course = get_object_or_404(Course, course_code=course_code)
        # split the date input and convert to datetime object
        user_date = date_input.split('-')
        user_date = datetime.date(int(user_date[0]), int(user_date[1]), int(user_date[2]))

        # Get the registered students for the course
        student_records = get_object_or_404(RegisteredStudent, course=course, session=session)

        filter_val = {"course": course, "date": user_date}

        # If user wants an existing record
        if att_rec == "existing":
            # if course attendance does not exist
            if CourseAttendance.objects.filter(**filter_val).count() > 1:
                # Get the required course attendance using the course and converted date
                fil_course_attendance = CourseAttendance.objects.filter(**filter_val)
                fil_course_attendance = [
                    [x.id, x.time] for x in fil_course_attendance
                ]
                # Create a dictionary of data to be returned to the page
                context = {
                    'course_attendance': list(fil_course_attendance),
                }
                # return data back to page
                return JsonResponse(context)
            else:
                # Get course attendance for the course for today
                course_attendance = get_object_or_404(CourseAttendance, date=user_date, course=course)
                # Get a list of all the ids of students in the course attendance
                student_attendance_ids = course_attendance.student_attendance.values_list('student')
                # Get a list of all the ids of students in the course attendance
                student_attendance_status = course_attendance.student_attendance.values('is_present')
                # Know if all atendance are true or not
                all_selected = get_all_selected_status(student_attendance_status)
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
                    'course_att_id': course_attendance.id,
                    'all_selected': all_selected
                }
                # return data back to the page
                return JsonResponse(context)
        # If course attendance has not been created before
        else:
            # Get current time
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            # Create course attendance for the course for today
            course_attendance = CourseAttendance.objects.create(course=course, date=user_date, time=current_time)
            # Loop through all the registered students
            for std in student_records.students.values():
                student = get_object_or_404(Student, matric_no=std['matric_no'])
                # Create a student attendance for each student
                student_attendance = StudentAttendance.objects.create(student=student, course=course, is_present=False,
                                                                      date=user_date, session=session)
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
                'course_att_id': course_attendance.id,
                'all_selected': 'no',
            }
            # return data back to the page
            return JsonResponse(context)


# Create function view to process ajax request
def submit_course_with_time(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get user input
        time = request.POST.get('time')

        # Get the required course attendance using the course and converted date
        course_attendance = get_object_or_404(CourseAttendance, id=int(time))

        # Get the registered students for the course
        student_records = get_object_or_404(RegisteredStudent, course=course_attendance.course, session=session)
        # Get a list of all the ids of students in the course attendance
        student_attendance_ids = course_attendance.student_attendance.values_list('student')
        # Get a list of all the ids of students in the course attendance
        student_attendance_status = course_attendance.student_attendance.values('is_present')
        # Know if all atendance are true or not
        all_selected = get_all_selected_status(student_attendance_status)
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
            'course_att_id': course_attendance.id,
            'all_selected': all_selected,
        }
        # return data back to the page
        return JsonResponse(context)


# Create function view to process ajax request
def search_attendance_register(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get user input
        course_att_id = request.POST.get('course_att_id')
        text = request.POST.get('text')
        mode = request.POST.get('searchMethod')

        # Get course attendance for the course for today
        course_attendance = get_object_or_404(CourseAttendance, id=int(course_att_id))
        # Get the registered students for the course
        registered_students = get_object_or_404(RegisteredStudent, course=course_attendance.course, session=session)

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
                    'course_att_id': course_attendance.id,
                    'mode': mode,
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
                    'course_att_id': course_attendance.id,
                    'mode': mode,
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

        # Create a dictionary of data to be returned to the page
        context = {
            'msg': f"{student.student.matric_no}'s attendance status updated",
            'color': 'alert alert-success',
        }
        # return data back to page
        return JsonResponse(context)


# Create function view to process ajax request
def select_all_checkboxes(request):
    # check if request method is POST
    if request.method == 'POST':
        # Get user input
        course_att_id = request.POST.get('course_att_id')
        is_present = request.POST.get('value')
        # Get attendance details of current student
        course_attendance = get_object_or_404(CourseAttendance, id=course_att_id)

        # Toggle and update the student attendance in response to clicking on the checkbox
        if is_present == 'true':
            for student_attendance in course_attendance.student_attendance.all():
                student_attendance.is_present = False
                student_attendance.save()

            # Create a dictionary of data to be returned to the page
            output = {
                'msg': f"All attendance status has been deselected",
                'color': 'alert alert-success',
                'selected': 'false',
            }
        else:
            for student_attendance in course_attendance.student_attendance.all():
                student_attendance.is_present = True
                student_attendance.save()

            # Create a dictionary of data to be returned to the page
            output = {
                'msg': f"All attendance status has been selected",
                'color': 'alert alert-success',
                'selected': 'true',
            }

        course_attendance.save()

        # Get the registered students for the course
        student_records = get_object_or_404(RegisteredStudent, course=course_attendance.course, session=session)

        # Get a list of all the ids of students in the course attendance
        student_attendance_ids = course_attendance.student_attendance.values_list('student')
        # Get a list of all the ids of students in the course attendance
        student_attendance_status = course_attendance.student_attendance.values('is_present')
        # Know if all atendance are true or not
        all_selected = get_all_selected_status(student_attendance_status)
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
            'course_att_id': course_attendance.id,
            'msg': output['msg'],
            'color': output['color'],
            'selected': output['selected'],
            'all_selected': all_selected,
        }
        # return data back to the page
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

        superuser = False
        is_staff = False
        if request.user.is_superuser:
            superuser = True
        if request.user.is_staff:
            is_staff = True

        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            current_staff = get_object_or_404(Staff, person=person)
            #  Filter all the courses in staff department
            course_allocation = CourseAllocation.objects.filter(lecturer=current_staff, session=session)
            courses = [
                course_all.course for course_all in course_allocation
            ]
            # Get the current date
            date = timezone.now().date().today()
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': current_staff,
                'date': date,
                'courses': courses,
                'superuser': superuser,
                'staff': is_staff,
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

        # Get the course using the course code
        course = get_object_or_404(Course, course_code=course_code)
        # split the date input and convert to datetime object
        user_date = date_input.split('-')
        user_date = datetime.date(int(user_date[0]), int(user_date[1]), int(user_date[2]))

        filter_val = {"course": course, "date": user_date}

        # if course attendance does not exist
        if CourseAttendance.objects.filter(**filter_val).count() < 1:
            return JsonResponse({'student_attendance_info': []})
        # if course attendance exists and it's only one
        elif CourseAttendance.objects.filter(**filter_val).count() == 1:
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
                'course_att_id': course_attendance.id,
            }
            # return data back to page
            return JsonResponse(context)
        # if course attendance exists and it's more than one
        else:
            # Get the required course attendance using the course and converted date
            fil_course_attendance = CourseAttendance.objects.filter(**filter_val)
            fil_course_attendance = [
                [x.id, x.time] for x in fil_course_attendance
            ]
            # Create a dictionary of data to be returned to the page
            context = {
                'course_attendance': list(fil_course_attendance),
            }
            # return data back to page
            return JsonResponse(context)


# Create function view to process ajax request
def get_attendance_records_with_time(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get user input
        time = request.POST.get('time')

        # Get the required course attendance using the course and converted date
        course_attendance = get_object_or_404(CourseAttendance, id=int(time))

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
            'course_att_id': course_attendance.id,
        }
        # return data back to page
        return JsonResponse(context)


# Create function view to process ajax request
def search_attendance_sheet(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get user input
        course_att_id = request.POST.get('course_att_id').upper()
        text = request.POST.get('text')
        mode = request.POST.get('searchMethod')

        # Get the required course attendance using the course and converted date
        course_attendance = get_object_or_404(CourseAttendance, id=int(course_att_id))
        # Get the registered students for the course
        registered_students = get_object_or_404(RegisteredStudent, course=course_attendance.course, session=session)

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


# Create an attendance sheet view
class TrackAttendanceView(View):
    # Add template name
    template_name = 'track_attendance.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)

        superuser = False
        is_staff = False
        if request.user.is_superuser:
            superuser = True
        if request.user.is_staff:
            is_staff = True

        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            current_staff = get_object_or_404(Staff, person=person)
            # Get the current date
            date = timezone.now().date().today()
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': current_staff,
                'date': date,
                'superuser': superuser,
                'staff': is_staff,
            }
            # login to te page with the data
            return render(request, self.template_name, context)
        # Otherwise
        else:
            # Redirect to dashboard
            return HttpResponseRedirect(reverse("Attendance:dashboard"))


# create a function to get students
def get_students(request):
    # Check if request method is POST
    if request.method == "POST":
        text = request.POST.get('text').upper()
        mode = request.POST.get('searchMethod')
        if mode == 'matric_no':
            # Get the search results
            students = Student.objects.filter(matric_no__icontains=text)

            students = [
                [x.person.id, x.person.full_name, x.matric_no] for x in students
            ]
        else:
            # Filter search
            persons = Person.objects.filter(full_name__icontains=text)
            students = [
                [get_object_or_404(Student, person=x).id, x.full_name, get_object_or_404(Student, person=x).matric_no]
                for x in persons
                if Student.objects.filter(person=x).count() > 0
            ]
            print(students)
        context = {
            'students': students,
        }
        return JsonResponse(context)


# create a function to get students
def get_student_attendance(request):
    # Check if request method is POST
    if request.method == "POST":
        person_id = request.POST.get('id')
        # Get the current logged in student
        person = get_object_or_404(Person, id=person_id)
        student = get_object_or_404(Student, person=person)
        try:
            # Get all the registered courses by the student
            reg_students = RegisteredStudent.objects.filter(session=session)
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
            zipped = []
            no_of_eligible_courses = [0]
            no_of_ineligible_courses = [0]

        # Create a dictionary of data to be accessed on the page
        context = {
            'zipped': list(zipped),
            'eligible': len(no_of_eligible_courses),
            'ineligible': len(no_of_ineligible_courses),
        }
        return JsonResponse(context)


# Create a settings view
class UploadView(View):
    # Add template name
    template_name = 'upload.html'

    # Create get function
    def get(self, request):
        # login to te page with the data
        return render(request, self.template_name)

    # Create post function
    def post(self, request):
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
                    return HttpResponseRedirect(reverse("Attendance:upload"))
            elif file_type == "staff":
                try:
                    upload_staff(file)
                except Exception:
                    messages.error(request, "Error uploading file")
                    return HttpResponseRedirect(reverse("Attendance:upload"))
            elif file_type == "course":
                try:
                    upload_course(file)
                except Exception:
                    messages.error(request, "Error uploading file")
                    return HttpResponseRedirect(reverse("Attendance:upload"))
            elif file_type == "allocate":
                try:
                    allocate_courses(file)
                except Exception:
                    messages.error(request, "Error uploading file")
                    return HttpResponseRedirect(reverse("Attendance:upload"))
            elif file_type == "programme":
                try:
                    upload_programme(file)
                except Exception:
                    messages.error(request, "Error uploading file")
                    return HttpResponseRedirect(reverse("Attendance:upload"))
            elif file_type == "department":
                try:
                    upload_department(file)
                except Exception:
                    messages.error(request, "Error uploading file")
                    return HttpResponseRedirect(reverse("Attendance:upload"))
            elif file_type == "faculty":
                try:
                    upload_faculty(file)
                except Exception:
                    messages.error(request, "Error uploading file")
                    return HttpResponseRedirect(reverse("Attendance:upload"))
            elif file_type == "reg_student":
                try:
                    upload_student_course_registration(file)
                except Exception:
                    messages.error(request, "Error uploading file")
                    return HttpResponseRedirect(reverse("Attendance:upload"))

            messages.success(request, "File upload successful")
            return HttpResponseRedirect(reverse("Attendance:upload"))


# Create a settings view
class SettingsView(View):
    # Add template name
    template_name = 'settings.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        form = UpdatePasswordForm()
        image_form = UploadImageForm()
        email_form = UpdateEmailForm()
        # Get the current logged in staff
        person = get_object_or_404(Person, user=request.user)
        # Get the current date
        date = timezone.now().date().today()

        superuser = False
        is_staff = False
        if request.user.is_superuser:
            superuser = True
        if request.user.is_staff:
            is_staff = True

        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            user = get_object_or_404(Staff, person=person)
            #  Filter all the courses in staff department
            course_allocation = CourseAllocation.objects.filter(lecturer=user, session=session)
            courses = [
                course_all.course for course_all in course_allocation
            ]
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': user,
                'date': date,
                'form': form,
                'courses': courses,
                'superuser': superuser,
                'staff': is_staff,
                'image_form': image_form,
                'email_form': email_form,
            }
        # Otherwise
        else:
            # Get the current logged in staff
            user = get_object_or_404(Student, person=person)

            # Create a dictionary of data to be accessed on the page
            context = {
                'user': user,
                'date': date,
                'form': form,
                'superuser': superuser,
                'staff': is_staff,
                'image_form': image_form,
                'email_form': email_form,
            }
        # login to te page with the data
        return render(request, self.template_name, context)


# Create function view to process request
def update_password(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get the submitted form
        form = UpdatePasswordForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            # Get user input
            old_password = form.cleaned_data['old_password'].strip()
            password = form.cleaned_data['password'].strip()
            confirm_password = form.cleaned_data['confirm_password'].strip()
            # Check if old password match
            if request.user.check_password(old_password):
                if password == old_password:
                    # Create message report
                    messages.error(request, "Previous password cannot be used")
                    # return data back to page
                    return HttpResponseRedirect(reverse("Attendance:settings"))
                elif password == "password":
                    # Create message report
                    messages.error(request, "Password cannot be 'password'")
                    # return data back to page
                    return HttpResponseRedirect(reverse("Attendance:settings"))
                else:
                    # Check if both passwords match
                    if password == confirm_password:
                        # Update password
                        request.user.set_password(password)
                        # Save updated data
                        request.user.save()
                        # Create message report
                        messages.success(request, "Password successfully changed")
                        # return data back to page
                        return HttpResponseRedirect(reverse("Attendance:settings"))
                    # If passwords do not match
                    else:
                        # Create message report
                        messages.error(request, "New password does not match")
                        # return data back to page
                        return HttpResponseRedirect(reverse("Attendance:settings"))
            # Otherwise
            else:
                messages.error(request, "Old password entered does not match")
                # return data back to page
                return HttpResponseRedirect(reverse("Attendance:settings"))


# Create function view to process request
def update_email(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get the submitted form
        form = UpdatePasswordForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            # Get user input
            email = form.cleaned_data['email'].strip()

            person = get_object_or_404(Person, user=request.user)
            person.email = email
            person.save()
            messages.error(request, "Email address successfully updated")
            # return data back to page
            return HttpResponseRedirect(reverse("Attendance:settings"))


# Create function view to process image update
def update_image(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get the submitted form
        form = UploadImageForm(request.POST, request.FILES)
        # Check if form is valid
        if form.is_valid():
            # Get user input
            image = form.cleaned_data['image']
            person = get_object_or_404(Person, user=request.user)
            person.image = image
            person.save()
            # Create a dictionary of data to be returned to the page
            messages.success(request, "Profile picture successfully updated")
            # return data back to page
            return HttpResponseRedirect(reverse("Attendance:settings"))


# Create function view to process ajax request
def register_student(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get user input
        matric_no = request.POST.get('matric_no').strip()
        course_code = request.POST.get('course').strip()
        semester = request.POST.get('semester').strip()

        # Get the course using the course code
        course = get_object_or_404(Course, course_code=course_code)

        # Get student
        try:
            student = Student.objects.get(matric_no=matric_no)
        except Exception:
            messages.error(request, f"Student with Matric No, {matric_no}, does not exists")
            # return data back to page
            return HttpResponseRedirect(reverse("Attendance:settings"))

        reg_students = get_object_or_404(RegisteredStudent, course=course, semester=semester, session=session)
        if student not in reg_students.students.all():
            reg_students.students.add(student)
        else:
            messages.error(request, "Student has already been registered for the course")
        # return data back to page
        return HttpResponseRedirect(reverse("Attendance:settings"))


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

        # Get form
        file_form = UploadFileForm()

        superuser = False
        is_staff = False
        if request.user.is_superuser:
            superuser = True
        if request.user.is_staff:
            is_staff = True

        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            user = get_object_or_404(Staff, person=person)
            # Get the current logged in staff
            current_staff = get_object_or_404(Staff, person=person)
            #  Filter all the courses in staff department
            course_allocation = CourseAllocation.objects.filter(lecturer=current_staff, session=session)
            courses = [
                course_all.course for course_all in course_allocation
            ]
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': user,
                'date': date,
                'courses': courses,
                'superuser': superuser,
                'staff': is_staff,
                'file_form': file_form,
            }

        # Otherwise
        else:
            # Get the current logged in student
            user = get_object_or_404(Student, person=person)

            # Create a dictionary of data to be accessed on the page
            context = {
                'user': user,
                'date': date,
                'superuser': superuser,
                'staff': is_staff,
                'file_form': file_form,
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
                course_attendance = CourseAttendance.objects.filter(course=course, session=session).order_by("date")
                # Get list of students offering course
                reg_students = RegisteredStudent.objects.get(course=course, session=session)
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

            students_records = get_spreadsheed_data_as_list(course, reg_students, course_attendance)

            for record in students_records:
                for data in record:
                    attendance_sheet.write(row, col, data)
                    col += 1
                row += 1
                col = 0

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
            # Get all the registered courses by the student
            reg_students = RegisteredStudent.objects.all()
            # Get all the course codes
            course_codes = []
            # Get the percentage of attendance for each course
            course_attendance_percentage = []
            for reg_std in reg_students:
                if student in reg_std.students.all():
                    course_codes.append(reg_std.course.course_code)
                    course_attendance_percentage.append(
                        get_number_of_course_attendance_percentage(reg_std.course, student))

            zipped = zip(course_codes, course_attendance_percentage)

            # Create a dictionary of data to be accessed on the page
            context = {
                'user': student,
                'zipped': zipped,
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
        # Get the submitted form
        form = UploadFileForm(request.POST, request.FILES)
        # Check if form is valid
        if form.is_valid():
            # Get user input
            session = form.cleaned_data["session"]
            file = form.cleaned_data['file']
            upload_course_attendance(file, session)

            messages.success(request, "File upload successful")
            # return data back to page
            return HttpResponseRedirect(reverse("Attendance:print_attendance_sheet"))


# Create a print attendance sheet view
class UpdateRecordsView(View):
    # Add template name
    template_name = 'update_records.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Get the current date
        date = timezone.now().date().today()

        #  Get forms
        staff_form = StaffRegisterForm()
        student_form = StudentRegisterForm()

        superuser = False
        is_staff = False
        if request.user.is_superuser:
            superuser = True
        if request.user.is_staff:
            is_staff = True

        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            user = get_object_or_404(Staff, person=person)
        # Otherwise
        else:
            # Get the current logged in student
            user = get_object_or_404(Student, person=person)

        # Create a dictionary of data to be accessed on the page
        context = {
            'user': user,
            'date': date,
            'superuser': superuser,
            'staff_form': staff_form,
            'staff': is_staff,
            'student_form': student_form,
        }

        # login to te page with the data
        return render(request, self.template_name, context)


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
                return HttpResponseRedirect(reverse("Attendance:update_records"))
        elif file_type == "staff":
            try:
                upload_staff(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:update_records"))
        elif file_type == "course":
            try:
                upload_course(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:update_records"))
        elif file_type == "allocate":
            try:
                allocate_courses(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:update_records"))
        elif file_type == "programme":
            try:
                upload_programme(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:update_records"))
        elif file_type == "department":
            try:
                upload_department(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:update_records"))
        elif file_type == "faculty":
            try:
                upload_faculty(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:update_records"))
        elif file_type == "reg_student":
            try:
                upload_student_course_registration(file)
            except Exception:
                messages.error(request, "Error uploading file")
                return HttpResponseRedirect(reverse("Attendance:update_records"))

        messages.success(request, "File upload successful")
        return HttpResponseRedirect(reverse("Attendance:update_records"))


def add_student(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get the submitted form
        form = StudentRegisterForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            # Get user input
            full_name = form.cleaned_data['full_name'].upper().strip()
            matric_no = form.cleaned_data['matric_no'].upper().strip()
            email = form.cleaned_data['email'].upper().strip()
            gender = form.cleaned_data['gender'].upper().strip()
            programme = form.cleaned_data['programme'].upper().strip()
            year_of_entry = form.cleaned_data['year_of_entry'].upper().strip()

            user = User.objects.create_user(username=matric_no, password="password")
            programme = get_object_or_404(Programme, programme_name=programme)
            person = Person.objects.create(user=user, full_name=full_name, email=email,
                                           gender=gender)
            student = Student.objects.create(person=person, matric_no=matric_no,
                                             programme=programme,
                                             year_of_entry=year_of_entry)
            student.save()

            messages.success(request, "Student successfully added")
            return HttpResponseRedirect(reverse('Attendance:update_records'))


def add_staff(request):
    # Check if request method is POST
    if request.method == "POST":
        # Get the submitted form
        form = StaffRegisterForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            # Get user input
            full_name = form.cleaned_data['full_name'].upper().strip()
            email = form.cleaned_data['email'].upper().strip()
            gender = form.cleaned_data['gender'].upper().strip()
            department = form.cleaned_data['department'].upper().strip()

            staff_id = full_name.split()[-1]
            user = User.objects.create_user(username=staff_id, password="password")
            person = Person.objects.create(user=user, full_name=full_name, email=email, gender=gender, is_staff=True)
            department = get_object_or_404(Department, department_name=department)
            staff = Staff.objects.create(person=person, staff_id=staff_id, department=department)
            staff.save()

            messages.success(request, "Staff successfully added")
            return HttpResponseRedirect(reverse('Attendance:update_records'))


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

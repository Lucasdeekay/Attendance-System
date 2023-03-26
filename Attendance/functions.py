import datetime
import pandas as pd
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from Attendance.models import CourseAttendance, RegisteredStudent, Student, Course, StudentAttendance, Person, Staff, \
    Faculty, Department, Programme, CourseAllocation

session = '2022/2023'


def get_all_selected_status(student_attendance_status):
    all_selected = [
        x['is_present'] for x in student_attendance_status
    ]
    all_selected_status = list(set(all_selected))
    if len(all_selected_status) > 1:
        all_selected_status = "no"
    else:
        if all_selected_status[0]:
            all_selected_status = "yes"
        else:
            all_selected_status = "no"

    return all_selected_status


# function gets short code for programmes
def get_programme_short_code(prog_names):
    if prog_names == "CYBER SECURITY":
        return "CYB"
    elif prog_names == "COMPUTER SCIENCE":
        return "CSC"
    elif prog_names == "SOFTWARE ENGINEERING":
        return "SEN"
    elif prog_names == "MICROBIOLOGY":
        return "MCB"
    elif prog_names == "INDUSTRIAL CHEMISTRY":
        return "ICH"
    elif prog_names == "BIOCHEMISTRY":
        return "BCH"
    elif prog_names == "BUSINESS ADMINISTRATION":
        return "BUS"
    elif prog_names == "ECONOMICS":
        return "ECO"
    elif prog_names == "ACCOUNTING":
        return "ACC"
    elif prog_names == "MASS COMMUNICATION":
        return "MAS"
    elif prog_names == "CRIMINOLOGY":
        return "CRM"
    else:
        return prog_names


# function checks date instance and if it includes a bracket
def take_attendance(date, course, session, student, attendance, index):
    if date.find("(") == -1:
        # split the date input and convert to datetime object
        user_date = date.strip().split('/')
        user_date = datetime.date(int(user_date[2][:4]), int(user_date[1][:2]), int(user_date[0][:2]))

        filter_val = {'course': course, 'date': user_date}

        if CourseAttendance.objects.filter(**filter_val).count() == 0:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            course_atendance = CourseAttendance.objects.create(course=course, date=user_date, time=time,
                                                               session=session)
        else:
            course_atendance = CourseAttendance.objects.get(course=course, date=user_date,
                                                               session=session)

        filter_value = {'student':student, 'course': course, 'date': user_date}

        if StudentAttendance.objects.filter(**filter_value).count() == 0:
            std_att = StudentAttendance.objects.create(student=student, course=course, date=user_date,
                                                       session=session)
            if attendance[index] == "Y":
                std_att.is_present = True

            std_att.save()
            course_atendance.student_attendance.add(std_att)
            course_atendance.save()
        else:
            pass
    else:
        date = date[:date.find("(")]
        # split the date input and convert to datetime object
        user_date = date.strip().split('/')
        user_date = datetime.date(int(user_date[2][:4]), int(user_date[1][:2]), int(user_date[0][:2]))

        time = datetime.datetime.now().strftime("%H:%M:%S")
        course_atendance = CourseAttendance.objects.create(course=course, date=user_date, time=time,
                                                           session=session)

        std_att = StudentAttendance.objects.create(student=student, course=course, date=user_date,
                                                   session=session)
        if attendance[index] == "Y":
            std_att.is_present = True

        std_att.save()
        course_atendance.student_attendance.add(std_att)
        course_atendance.save()


# function returns the percentage a student is present for a course
def get_weekly_course_attendance_percentage(course_attendance, student):
    present = 0
    absent = 0
    for att in course_attendance:
        try:
            student_att = att.student_attendance.get(student=student)
            if student_att.is_present:
                present += 1
            else:
                absent += 1
        except Exception:
            pass
    if absent == 0:
        return 0
    else:
        return round((present / (present + absent)) * 100, 2)


# function gets students record list
def get_spreadsheed_data_as_list(course, reg_students, course_attendance):
    std_record = []

    headings = ["Full Name", "Matric No"]
    for att in course_attendance:
        headings.append(f"{att.date}")
    headings.append("Eligibility (%)")
    headings.append("Eligible")

    std_record.append(headings)

    for std in reg_students:
        std_list = [std.person.full_name, std.matric_no]
        student = Student.objects.get(matric_no=std.matric_no)

        for att in course_attendance:
            try:
                course_att = att.student_attendance.get(student=student)
                std_list.append(course_att.is_present)
            except Exception:
                std_list.append(False)

        present = get_number_of_course_attendance_percentage(course, std)
        std_list.append(f'{present}%')
        if present < 75:
            std_list.append("No")
        else:
            std_list.append("Yes")

        std_record.append(std_list)
    return std_record


# function gets students record list
def get_spreadsheed_data_as_list_weekly_attendance(days):
    std_record = []

    headings = ["Full Name", "Matric No", "Programme", "Attendance (%)"]
    std_record.append(headings)

    for std in Student.objects.all():
        std_list = [std.person.full_name, std.matric_no, std.programme.programme_name]

        course_attendance = []
        for day in days:
            course_atts = CourseAttendance.objects.filter(date=day)
            for att in course_atts:
                if att.student_attendance.filter(student=std).count() > 0:
                    course_attendance.append(att)

        percentage = get_weekly_course_attendance_percentage(course_attendance, std)
        if percentage <= 50:
            std_list.append(percentage)
        std_record.append(std_list)

    return std_record


# function gets students record list
def get_spreadsheed_data_as_list_weekly_attendance_per_department(days, department):
    std_record = []

    headings = ["Full Name", "Matric No", "Programme", "Attendance (%)"]
    std_record.append(headings)

    for std in Student.objects.all():
        if std.programme in Programme.objects.filter(department=department):
            std_list = [std.person.full_name, std.matric_no, std.programme.programme_name]

            course_attendance = []
            for day in days:
                courses = Course.objects.filter(department=department)
                for course in courses:
                    course_atts = CourseAttendance.objects.filter(course=course, date=day)
                    for att in course_atts:
                        if att.student_attendance.filter(student=std).count() > 0:
                            course_attendance.append(att)

            percentage = get_weekly_course_attendance_percentage(course_attendance, std)
            if percentage <= 50:
                std_list.append(percentage)
            std_record.append(std_list)

    return std_record


# function returns the total amount of times a student is present for a course
def get_number_of_course_attendance_present(course, student):
    all_attendance = CourseAttendance.objects.filter(course=course, session=session)
    present = 0
    for att in all_attendance:
        try:
            student_att = att.student_attendance.get(student=student)
            if student_att.is_present:
                present += 1
        except Exception:
            pass
    return present


# function returns the total amount of times a student is absent for a course
def get_number_of_course_attendance_absent(course, student):
    all_attendance = CourseAttendance.objects.filter(course=course, session=session)
    absent = 0
    for att in all_attendance:
        try:
            student_att = att.student_attendance.get(student=student)
            if not student_att.is_present:
                absent += 1
        except Exception:
            pass
    return absent


# function returns the percentage a student is present for a course
def get_number_of_course_attendance_percentage(course, student):
    all_attendance = CourseAttendance.objects.filter(course=course, session=session)
    present = 0
    absent = 0
    for att in all_attendance:
        try:
            student_att = att.student_attendance.get(student=student)
            if student_att.is_present:
                present += 1
            else:
                absent += 1
        except Exception:
            pass
    if (present + absent) == 0:
        return 0
    else:
        return round((present / (present + absent)) * 100, 2)


def get_total_number_of_students(course):
    if RegisteredStudent.objects.filter(course=course, session=session).count() > 0:
        all_students = RegisteredStudent.objects.get(course=course, session=session).students.all()
        return len(all_students)
    else:
        return 0


# Function returns the total number of eligible students
def get_number_of_eligible_students(course):
    if RegisteredStudent.objects.filter(course=course, session=session).count() > 0:
        all_students = RegisteredStudent.objects.get(course=course, session=session).students.all()
        eligible = 0
        for std in all_students:
            eligibilty_percentage = get_number_of_course_attendance_percentage(course, std)
            if eligibilty_percentage >= 75:
                eligible += 1
        return eligible
    else:
        return 0


# Function returns the total number of ineligible students
def get_number_of_ineligible_students(course):
    if RegisteredStudent.objects.filter(course=course, session=session).count() > 0:
        all_students = RegisteredStudent.objects.get(course=course, session=session).students.all()
        ineligible = 0
        for std in all_students:
            eligibilty_percentage = get_number_of_course_attendance_percentage(course, std)
            if eligibilty_percentage < 75:
                ineligible += 1
        return ineligible
    else:
        return 0


def get_number_of_unique_programs(course):
    if RegisteredStudent.objects.filter(course=course, session=session).count() > 0:
        all_students = RegisteredStudent.objects.get(course=course, session=session).students.all()
        program_list = []
        for student in all_students:
            program_list.append(get_programme_short_code(student.programme.programme_name))
        return len(set(program_list))
    else:
        return 0


def get_list_of_unique_programs(course):
    if RegisteredStudent.objects.filter(course=course, session=session).count() > 0:
        all_students = RegisteredStudent.objects.get(course=course, session=session).students.all()
        program_list = []
        for student in all_students:
            program_list.append(get_programme_short_code(student.programme.programme_name))
        return ", ".join(set(program_list))
    else:
        return 'None'


def upload_staff(file):
    df = pd.read_excel(file)
    data = zip(df.values.tolist())
    for index, i in enumerate(data):
        data2 = []
        for j in i[0]:
            data2.append(j)

        full_name, gender, dep, email, desig, post = data2

        staff_id = full_name.split()[-1]

        if User.objects.filter(username=staff_id.upper().strip()).count() < 1:
            user = User.objects.create_user(username=staff_id.upper(), password="password", email=email)

            if str(email) == 'nan':
                person = Person.objects.create(user=user, full_name=full_name.upper(), gender=gender.upper().strip(),
                                               is_staff=True)
            else:
                person = Person.objects.create(user=user, full_name=full_name.upper(), gender=gender.upper().strip(),
                                               email=email, is_staff=True)

            department = get_object_or_404(Department, department_name=dep.upper())
            staff = Staff.objects.create(person=person, staff_id=staff_id.upper(), designation=desig.upper(),
                                         post=post.upper(), department=department)
            staff.save()


def upload_student(file):
    df = pd.read_excel(file)
    data = zip(df.values.tolist())
    for index, i in enumerate(data):
        data2 = []
        for j in i[0]:
            data2.append(j)

        matric_no, full_name, moe, yoa, fac, dep, prog, gender, email = data2
        if prog == 'CRIMINOLOGY AND SECURITY STUDIES':
            prog = "CRIMINOLOGY"
        elif prog == 'CYBERSECURITY':
            prog = "CYBER SECURITY"
        if User.objects.filter(username=matric_no.upper().strip()).count() < 1:
            user = User.objects.create_user(username=matric_no.upper().strip(), password="password", email=email)
            programme = get_object_or_404(Programme, programme_name=prog.upper().strip())

            if str(email) == 'nan':
                person = Person.objects.create(user=user, full_name=full_name.upper(), gender=gender.upper().strip())
            else:
                person = Person.objects.create(user=user, full_name=full_name.upper(), email=email,
                                               gender=gender.upper().strip())

            student = Student.objects.create(person=person, matric_no=matric_no.upper().strip(),
                                             programme=programme,
                                             year_of_entry=yoa.strip())
            student.save()


def upload_faculty(file):
    df = pd.read_excel(file)
    data = zip(df.values.tolist())
    for index, i in enumerate(data):
        data2 = []
        for j in i[0]:
            data2.append(j)

        fac = data2[0]
        if Faculty.objects.filter(faculty_name=fac.upper()).count() < 1:
            faculty = Faculty.objects.create(faculty_name=fac.upper())

            faculty.save()


def upload_department(file):
    df = pd.read_excel(file)
    data = zip(df.values.tolist())
    for index, i in enumerate(data):
        data2 = []
        for j in i[0]:
            data2.append(j)

        fac, dep_name = data2
        faculty = get_object_or_404(Faculty, faculty_name=fac.upper())
        if Department.objects.filter(department_name=dep_name.upper()).count() < 1:
            department = Department.objects.create(faculty=faculty, department_name=dep_name.upper())
            department.save()


def upload_programme(file):
    df = pd.read_excel(file)
    data = zip(df.values.tolist())
    for index, i in enumerate(data):
        data2 = []
        for j in i[0]:
            data2.append(j)

        dep, prog_name = data2
        department = get_object_or_404(Department, department_name=dep.upper())
        if Programme.objects.filter(programme_name=prog_name.upper()).count() < 1:
            programme = Programme.objects.create(department=department, programme_name=prog_name.upper())
            programme.save()


def upload_course(file):
    excel_file = pd.ExcelFile(file)
    for department in excel_file.sheet_names:
        df = pd.read_excel(file, sheet_name=department)
        data = zip(df.values.tolist())
        for index, i in enumerate(data):
            data2 = []
            for j in i[0]:
                data2.append(j)

            course_code, course_title, course_unit, status = data2

            department = get_object_or_404(Department, department_name=str(department).upper())

            if str(course_code).strip() != "nan" and Course.objects.filter(
                    course_code=course_code.strip().upper()).count() < 1:
                course = Course.objects.create(course_title=course_title.strip().upper(),
                                               course_code=course_code.strip().upper(),
                                               course_unit=course_unit, department=department)
                course.save()


def allocate_courses(file):
    df = pd.read_excel(file)
    data = zip(df.values.tolist())
    for index, i in enumerate(data):
        data2 = []
        for j in i[0]:
            data2.append(j)

        code, lecturer, others = data2

        course = Course.objects.get(course_code=code)
        if Staff.objects.filter(staff_id=lecturer).count() == 1:
            lecturer = get_object_or_404(Staff, staff_id=lecturer)
        elif lecturer == "HOD":
            lecturer = get_object_or_404(Staff, department=course.programme.department, post="HOD")
        else:
            lecturer = get_object_or_404(Staff, department=course.programme.department, post="HOD")

        if CourseAllocation.objects.filter(course=course).count() < 1:
            course_allocation = CourseAllocation.objects.create(course=course, lecturer=lecturer, session=session)

            if str(others).strip() != "nan":
                if others.strip().split(" ")[0].upper() == "ALL":
                    all_lecturers = Staff.objects.filter(department=course.programme.department)
                    for lecturer in all_lecturers:
                        if lecturer.post != "HOD":
                            course_allocation.others.add(lecturer)
                else:
                    others = others.strip().split("/")
                    for x in others:
                        lecturer = x.upper().split()[-1]
                        if Staff.objects.filter(staff_id=lecturer).count() == 1:
                            lecturer = get_object_or_404(Staff, staff_id=lecturer)
                            course_allocation.others.add(lecturer)

        else:
            course_allocation = get_object_or_404(CourseAllocation, course=course, session=session)
            course_allocation.lecturer = lecturer

            if len(course_allocation.others.all()) > 0:
                for lecturer in course_allocation.others.all():
                    course_allocation.others.remove(lecturer)

            if str(others).strip() != "nan":
                if others.strip().split(" ")[0].upper() == "ALL":
                    all_lecturers = Staff.objects.filter(department=course.programme.department)
                    for lecturer in all_lecturers:
                        if lecturer.post != "HOD":
                            course_allocation.others.add(lecturer)
                else:
                    others = others.strip().split("/")
                    for x in others:
                        lecturer = x.upper().split()[-1]
                        if Staff.objects.filter(staff_id=lecturer).count() == 1:
                            lecturer = get_object_or_404(Staff, staff_id=lecturer)
                            course_allocation.others.add(lecturer)

        course_allocation.save()


def upload_student_course_registration(file):
    excel_file = pd.ExcelFile(file)
    for course_code in excel_file.sheet_names:
        df = pd.read_excel(file, sheet_name=course_code)
        data = zip(df.values.tolist())
        for index, i in enumerate(data):
            data2 = []
            for j in i[0]:
                data2.append(j)

            matric_no, sch_session, semester = data2

            if Student.objects.filter(matric_no=matric_no).count() == 1:
                student = Student.objects.get(matric_no=matric_no.strip().upper())
                if Course.objects.filter(course_code=course_code.strip().upper()).count() == 1:
                    course = Course.objects.get(course_code=course_code.strip().upper())
                    if RegisteredStudent.objects.filter(course=course, session=sch_session).count() == 1:
                        reg_students = get_object_or_404(RegisteredStudent, course=course, session=sch_session.strip())
                    else:
                        reg_students = RegisteredStudent.objects.create(course=course, semester=semester.lower(),
                                                                        session=sch_session.strip())

                    if student not in reg_students.students.all():
                        reg_students.students.add(student)

                    reg_students.save()


def upload_course_attendance(file, sch_session):
    excel_file = pd.ExcelFile(file)
    for course_code in excel_file.sheet_names:
        df = pd.read_excel(file, sheet_name=course_code)
        data = zip(df.values.tolist())
        fn, mn, *dates = df.columns.tolist()
        for index, i in enumerate(data):
            data2 = []
            for j in i[0]:
                data2.append(j)

            full_name, matric_no, *attendance = data2

            course = Course.objects.get(course_code=course_code)
            if Student.objects.filter(matric_no=matric_no).count() == 1:
                student = Student.objects.get(matric_no=matric_no)

                for index, date in enumerate(dates):

                    if isinstance(date, datetime.datetime):
                        date = str(date.date()).split("-")
                        date = '/'.join([date[2], date[1], date[0]])
                        take_attendance(date, course, sch_session, student, attendance, index)
                    elif date.find("/") != -1:
                        take_attendance(date, course, sch_session, student, attendance, index)
                    else:
                        pass

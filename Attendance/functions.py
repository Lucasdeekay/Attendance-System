import datetime

import pandas as pd
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from Attendance.models import CourseAttendance, RegisteredStudent, Student, Course, StudentAttendance, Person, Staff, \
    Faculty, Department, Programme


# function returns the total amount of times a student is present for a course
def get_number_of_course_attendance_present(course, student):
    all_attendance = CourseAttendance.objects.filter(course=course)
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
    all_attendance = CourseAttendance.objects.filter(course=course)
    absent = 0
    for att in all_attendance:
        try:
            student_att = att.student_attendance.get(student=student)
            if not student_att.is_present:
                absent += 1
        except Exception:
            pass
    return absent


# function returns the total amount of times a student is present for a course
def get_number_of_course_attendance_percentage(course, student):
    all_attendance = CourseAttendance.objects.filter(course=course)
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
    if absent == 0:
        return 0
    else:
        return round((present / (present + absent)) * 100, 2)


# Function returns the total number of eligible students
def get_number_of_eligible_students(course):
    all_students = RegisteredStudent.objects.get(course=course).students.all()
    eligible = 0
    for std in all_students:
        eligibilty_percentage = get_number_of_course_attendance_percentage(course, std)
        if eligibilty_percentage >= 75:
            eligible += 1
    return eligible


# Function returns the total number of ineligible students
def get_number_of_ineligible_students(course):
    all_students = RegisteredStudent.objects.get(course=course).students.all()
    ineligible = 0
    for std in all_students:
        eligibilty_percentage = get_number_of_course_attendance_percentage(course, std)
        if eligibilty_percentage < 75:
            ineligible += 1
    return ineligible


def upload_attendance(file):
    excel_file = pd.ExcelFile(file)
    for course_code in excel_file.sheet_names:
        df = pd.read_excel(file, sheet_name=course_code)

        for index, value in enumerate(df.values):
            if 'NAME OF STUDENTS' in value:
                df = pd.DataFrame(df.values[index + 1:])
                break

        for index, value in enumerate(df.values):
            new_list = set(value)
            if len(new_list) <= 2:
                df.drop(index, inplace=True)

        headings = df.values[0]
        headings[0] = 'index'
        headings[1] = 'Name Of Students'
        headings[2] = 'Matric No'
        headings[-1] = 'Eligibility Status'
        headings[-2] = 'Attendance (%)'
        headings[-3] = 'Number Of Times Absent'
        headings[-4] = 'Total Attendance'

        df = df.T.dropna().T
        headings = df.values[0]
        df.columns = headings.tolist()
        df.drop(0, inplace=True)
        df.drop(columns=['index', 'Name Of Students'], inplace=True)

        data = zip(df.values.tolist())
        for index, value in enumerate(data):
            data2 = []
            for tup in zip(df.columns, value[0]):
                data2.append(tup)

            matric_no = ''
            for val in data2:
                if val[0] == 'Matric No':
                    matric_no = val[1]
                else:
                    date = val[0].split(' ')[0]
                    status = val[1]

                    user_date = date.split('/')
                    user_date = datetime.date(int(user_date[2]), int(user_date[1]), int(user_date[0]))

                    student = get_object_or_404(Student, matric_no=matric_no.upper())
                    attendance_status = False
                    if status == 'Y':
                        attendance_status = True

                    course = get_object_or_404(Course, course_code=course_code.upper())

                    student_attendance = StudentAttendance.objects.create(student=student, course=course, is_present=attendance_status,
                                                                          date=user_date)

                    try:
                        course_attendance = get_object_or_404(CourseAttendance, course=course)
                    except Exception:
                        course_attendance = CourseAttendance.objects.create(course=course, date=user_date)
                    finally:
                        course_attendance.student_attendance.add(student_attendance)


def upload_staff(file):
    df = pd.read_excel(file)
    data = zip(df.values.tolist())
    for index, i in enumerate(data):
        data2 = []
        for j in i[0]:
            data2.append(j)

        index, full_name, gender, dep, email, post = data2

        staff_id = full_name.split()[-1]
        user = User.objects.create_user(username=staff_id.upper(), password="password")

        if str(email) == 'nan':
            person = Person.objects.create(user=user, full_name=full_name.upper(), gender=gender.upper().strip(), is_staff=True)
        else:
            person = Person.objects.create(user=user, full_name=full_name.upper(), gender=gender.upper().strip(), email=email, is_staff=True)

        department = get_object_or_404(Department, department_name=dep.upper())
        staff = Staff.objects.create(person=person, staff_id=staff_id.upper(), post=post, department=department)
        staff.save()


def upload_student(file):
    df = pd.read_excel(file)
    data = zip(df.values.tolist())
    for index, i in enumerate(data):
        data2 = []
        for j in i[0]:
            data2.append(j)

        matric_no, full_name, moe, yoa, fac, dep, prog, gender, email = data2[:8]
        if prog == 'CRIMINOLOGY AND SECURITY STUDIES':
            prog = "CRIMINOLOGY"
        elif prog == 'CYBERSECURITY':
            prog = "CYBER SECURITY"
        try:
            user = get_object_or_404(User, username=matric_no.upper().strip())
            if user:
                pass
        except Exception:
            user = User.objects.create_user(username=matric_no.upper().strip(), password="password")
            programme = get_object_or_404(Programme, programme_name=prog.upper().strip())

            if str(email) == 'nan':
                person = Person.objects.create(user=user, full_name=full_name.upper(), gender=gender.upper().strip())
            else:
                person = Person.objects.create(user=user, full_name=full_name.upper(), email=email, gender=gender.upper().strip())

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

            num, course_code, course_title, course_unit, status, lecturer, others = data2
            department = get_object_or_404(Department, department_name=department)

            lecturer = str(lecturer).upper().strip().split()[-1]
            if Staff.objects.filter(staff_id=lecturer).count() == 1:
                lecturer = get_object_or_404(Staff, staff_id=lecturer)
                print(num, lecturer)
            else:
                lecturer = get_object_or_404(Staff, department=department, post="HOD")
                print(num, lecturer)

            if Course.objects.filter(course_code=' '.join(course_code.strip().upper().split())).count() < 1:
                course = Course.objects.create(course_title=course_title.strip().upper(), course_code=' '.join(course_code.strip().upper().split()),
                                               course_unit=course_unit, department=department, lecturer=lecturer)
                if str(others).strip() != "nan":
                    if others.strip().upper() == "ALL LECTURERS":
                        all_lecturers = Staff.objects.filter(department=department)
                        for lecturer in all_lecturers:
                            if lecturer.post != "HOD":
                                course.others.add(lecturer)
                    else:
                        others = others.strip().split("/")
                        for x in others:
                            lecturer = x.upper().split()[-1]
                            if Staff.objects.filter(staff_id=lecturer).count() == 1:
                                lecturer = get_object_or_404(Staff, staff_id=lecturer)
                                course.others.add(lecturer)
                course.save()


def upload_registered_students(file):
    excel_file = pd.ExcelFile(file)
    for course_code in excel_file.sheet_names:
        df = pd.read_excel(file, sheet_name=course_code)

        for index, value in enumerate(df.values):
            if 'NAME OF STUDENTS' in value:
                df = pd.DataFrame(df.values[index + 1:])
                break

        for index, value in enumerate(df.values):
            new_list = set(value)
            if len(new_list) <= 2:
                df.drop(index, inplace=True)

        headings = df.values[0]
        headings[0] = 'index'
        headings[1] = 'Name Of Students'
        headings[2] = 'Matric No'
        df.columns = headings.tolist()
        df = df['Matric No']

        for i in df:
            if Student.objects.filter(matric_no=i).count() == 1 and i != 'Matric No':
                student = Student.objects.get(matric_no=i)
                if Course.objects.filter(course_code=course_code, department=student.programme.department).count() == 1:
                    course = Course.objects.get(course_code=course_code, department=student.programme.department)
                    if RegisteredStudent.objects.filter(course=course).count() == 1:
                        reg_students = get_object_or_404(RegisteredStudent, course=course)
                    else:
                        reg_students = RegisteredStudent.objects.create(course=course)
                    reg_students.students.add(student)


def student_course_registration(file):
    excel_file = pd.ExcelFile(file)
    for sheet in excel_file.sheet_names:
        df = pd.read_excel(file, sheet_name=sheet)
        data = zip(df.values.tolist())
        for index, i in enumerate(data):
            data2 = []
            for j in i[0]:
                data2.append(j)

            matric_no, course_code, session, semester = data2

            if Student.objects.filter(matric_no=i).count() == 1 and i != 'Matric No':
                student = Student.objects.get(matric_no=i)
                if Course.objects.filter(course_code=course_code, department=student.programme.department).count() == 1:
                    course = Course.objects.get(course_code=course_code, department=student.programme.department)
                    if RegisteredStudent.objects.filter(course=course).count() == 1:
                        reg_students = get_object_or_404(RegisteredStudent, course=course)
                    else:
                        reg_students = RegisteredStudent.objects.create(course=course)
                    reg_students.students.add(student)

                    reg_students.save()

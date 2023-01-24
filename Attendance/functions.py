import datetime

import pandas as pd
from django.shortcuts import get_object_or_404

from Attendance.models import CourseAttendance, RegisteredStudent, Student, Course, StudentAttendance


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
        return round((present/(present + absent)) * 100, 2)


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

            user = ''
            for val in data2:
                if val[0] == 'Matric No':
                    user = val[1]
                else:
                    date = val[0].split(' ')[0]
                    status = val[1]

                    user_date = date.split('/')
                    user_date = datetime.date(int(user_date[2]), int(user_date[1]), int(user_date[0]))

                    student = get_object_or_404(Student, matric_no=user)
                    attendance_status = False
                    if status == 'Y':
                        attendance_status = True

                    course = get_object_or_404(Course, course_code=course_code)

                    student_attendance = StudentAttendance.objects.create(student=student, is_present=attendance_status, date=user_date)

                    try:
                        course_attendance = get_object_or_404(CourseAttendance, course=course)
                    except Exception:
                        course_attendance = CourseAttendance.objects.create(course=course, date=user_date)
                    finally:
                        course_attendance.student_attendance.add(student_attendance)

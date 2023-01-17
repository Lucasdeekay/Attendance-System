from Attendance.models import CourseAttendance, RegisteredStudent


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
    return (present/(present + absent)) * 100


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

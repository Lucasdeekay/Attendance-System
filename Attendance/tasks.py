import datetime
import io

import xlsxwriter
from django.core.mail import EmailMessage

from Attendance.functions import get_spreadsheed_data_as_list_weekly_attendance
from Attendance.models import Password
from AttendanceSystem.settings import EMAIL_HOST_USER


def send_email():
    current_day = datetime.datetime.today()
    days = []
    # if current_day.weekday() == 5:
    for i in range(5):
        day = current_day - datetime.timedelta(days=i)
        days.append(day.date())

    # Create an in-memory output file for the workbook
    output = io.BytesIO()

    # Create an excel spreadsheet workbook
    attendance_book = xlsxwriter.Workbook(output)

    # Give the file created a name
    filename = f"Attendance For The Week ({days[-1]} - {days[0]}).xlsx"

    # Add a worksheet
    attendance_sheet = attendance_book.add_worksheet()

    # Instantiate the rows and columns
    row = col = 0

    students_records = get_spreadsheed_data_as_list_weekly_attendance(days)

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

    subject = 'Weekly Attendance Report'
    msg = "This is the weekly report of students who have 50% or less attendance for this week. The link for " \
          "downloading a document containing more detailed information concerning the students is attached below. " \
          "Kindly click on the link below to download"

    message = EmailMessage(subject, msg, EMAIL_HOST_USER, ['lucasdeekay98@gmail.com'],)
    message.attach(filename, output.getvalue(), 'application/vnd.ms-excel')
    message.send()


def update_password_validity():
    active_passwords = Password.objects.filter(is_active=True)
    for password in active_passwords:
        password.expiry()
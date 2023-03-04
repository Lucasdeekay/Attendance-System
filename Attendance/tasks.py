from django.core.mail import send_mail
from django.template.loader import render_to_string

from Attendance.models import Password
from AttendanceSystem.settings import EMAIL_HOST_USER


def send_email():
    subject = 'Weekly Attendance Report'
    msg = "This is the weekly report of students who have 50% or less attendance for this week. The link for " \
          "downloading a document containing more detailed information concerning the students is attached below. " \
          "Kindly click on the link below to download"
    context = {'title': subject, 'msg': msg, 'url': True}
    html_message = render_to_string('email.html', context=context)

    send_mail(subject, msg, EMAIL_HOST_USER, ['lucasdeekay98@gmail.com'], html_message=html_message,
              fail_silently=False)


def update_password_validity():
    active_passwords = Password.objects.filter(is_active=True)
    for password in active_passwords:
        password.expiry()
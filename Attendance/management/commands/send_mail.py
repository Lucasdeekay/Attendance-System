import datetime

from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.template.loader import render_to_string

from AttendanceSystem.settings import EMAIL_HOST_USER


class Command(BaseCommand):
    today = datetime.date.today()
    weekday = today.weekday()

    def send_email(self):

        subject = 'Weekly Update'
        msg = 'Sending weekly mail'

        if self.weekday == 2:
            context = {'title': subject, 'msg': msg}
            html_message = render_to_string('email.html', context=context)

            send_mail(subject, msg, EMAIL_HOST_USER, ['lucasdeekay98@gmail.com'], html_message=html_message, fail_silently=False)
            self.stdout.write('Mails sent')
        else:
            self.stderr.write('Mails not sent')
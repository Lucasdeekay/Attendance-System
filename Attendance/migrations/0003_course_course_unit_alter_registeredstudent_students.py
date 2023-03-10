# Generated by Django 4.1.3 on 2022-12-24 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0002_remove_student_courses_registeredcourses'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_unit',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='registeredstudent',
            name='students',
            field=models.ManyToManyField(blank=True, null=True, to='Attendance.student'),
        ),
    ]

# Generated by Django 4.1.3 on 2023-01-29 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0006_remove_course_department_course_programme_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='lecturer',
        ),
        migrations.RemoveField(
            model_name='person',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='middle_name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='level',
        ),
        migrations.AddField(
            model_name='course',
            name='course_unit',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='full_name',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='gender',
            field=models.CharField(default='MALE', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='department',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Attendance.department'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='year_of_entry',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]

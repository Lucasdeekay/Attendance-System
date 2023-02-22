# Generated by Django 4.1.3 on 2023-02-22 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0012_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='lecturer',
            field=models.ForeignKey(default=74, on_delete=django.db.models.deletion.CASCADE, to='Attendance.staff'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registeredstudent',
            name='semester',
            field=models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], default='', max_length=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='courseattendance',
            name='session',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='session',
            field=models.CharField(max_length=10),
        ),
    ]

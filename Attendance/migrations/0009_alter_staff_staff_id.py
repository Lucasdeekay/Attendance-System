# Generated by Django 4.1.3 on 2023-02-09 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0008_alter_course_course_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='staff_id',
            field=models.CharField(max_length=25),
        ),
    ]
# Generated by Django 4.1.3 on 2023-02-20 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0010_remove_course_programme_course_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(default='', max_length=254),
            preserve_default=False,
        ),
    ]
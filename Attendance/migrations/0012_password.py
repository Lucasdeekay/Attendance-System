# Generated by Django 4.1.3 on 2023-02-20 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0011_person_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Password',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recovery_password', models.CharField(max_length=12)),
                ('time', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Attendance.person')),
            ],
        ),
    ]

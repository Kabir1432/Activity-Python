# Generated by Django 4.2.5 on 2023-09-29 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0013_studentotp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentotp',
            old_name='OTP',
            new_name='otp',
        ),
    ]

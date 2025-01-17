# Generated by Django 4.2.1 on 2023-07-12 12:41

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0003_multitoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationuser',
            name='age',
        ),
        migrations.RemoveField(
            model_name='applicationuser',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='applicationuser',
            name='height',
        ),
        migrations.RemoveField(
            model_name='applicationuser',
            name='is_phoneOtp_verified',
        ),
        migrations.RemoveField(
            model_name='applicationuser',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='applicationuser',
            name='location',
        ),
        migrations.RemoveField(
            model_name='applicationuser',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='applicationuser',
            name='nationality',
        ),
        migrations.RemoveField(
            model_name='applicationuser',
            name='old_latitude',
        ),
        migrations.RemoveField(
            model_name='applicationuser',
            name='old_longitude',
        ),
        migrations.RemoveField(
            model_name='applicationuser',
            name='weight',
        ),
        migrations.AddField(
            model_name='applicationuser',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='applicationuser',
            name='user_type',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], max_length=16, null=True, verbose_name='User Type'),
        ),
        migrations.AlterField(
            model_name='applicationuser',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, error_messages={'unique': 'A user with that phone already exists.'}, max_length=128, null=True, region=None, unique=True, verbose_name='Mobile Number'),
        ),
    ]

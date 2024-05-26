# Generated by Django 4.2.1 on 2023-07-13 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0004_remove_applicationuser_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationuser',
            name='user_type',
            field=models.CharField(blank=True, choices=[('student', 'Student'), ('admin', 'Admin'), ('sub_admin', 'Sub Admin'), ('ngo', 'NGO'), ('college', 'College')], max_length=16, null=True, verbose_name='User Type'),
        ),
    ]
# Generated by Django 4.2.5 on 2024-02-09 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0019_studentdetails_google_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentdetails',
            name='disable_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
# Generated by Django 4.2.1 on 2023-09-19 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_studentdetails_deactivation_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FAQ',
        ),
    ]

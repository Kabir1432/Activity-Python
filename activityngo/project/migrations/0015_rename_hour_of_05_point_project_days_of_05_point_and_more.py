# Generated by Django 4.2.1 on 2023-08-24 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_remove_project_number_of_hours_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='hour_of_05_point',
            new_name='days_of_05_point',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='hour_of_10_point',
            new_name='days_of_10_point',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='hour_of_20_point',
            new_name='days_of_20_point',
        ),
    ]

# Generated by Django 4.2.5 on 2023-10-13 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_project', '0011_studenttaskstatus_task2_submissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studenttaskstatus',
            name='task2_submissions',
        ),
        migrations.AddField(
            model_name='studenttaskstatus',
            name='task3_submissions',
            field=models.PositiveIntegerField(default=1, verbose_name='task 3 submissions'),
        ),
    ]
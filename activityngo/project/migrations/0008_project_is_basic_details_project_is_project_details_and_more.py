# Generated by Django 4.2.1 on 2023-08-21 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_studentfeedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_basic_details',
            field=models.BooleanField(default=False, verbose_name='Basic Details'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_project_details',
            field=models.BooleanField(default=False, verbose_name='Project Details'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_task_1',
            field=models.BooleanField(default=False, verbose_name='Task 1'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_task_10',
            field=models.BooleanField(default=False, verbose_name='Task 10'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_task_2',
            field=models.BooleanField(default=False, verbose_name='Task 2'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_task_3',
            field=models.BooleanField(default=False, verbose_name='Task 3'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_task_4',
            field=models.BooleanField(default=False, verbose_name='Task 4'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_task_5',
            field=models.BooleanField(default=False, verbose_name='Task 5'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_task_6',
            field=models.BooleanField(default=False, verbose_name='Task 6'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_task_7',
            field=models.BooleanField(default=False, verbose_name='Task 7'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_task_8',
            field=models.BooleanField(default=False, verbose_name='Task 8'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_task_9',
            field=models.BooleanField(default=False, verbose_name='Task 9'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_task_summary',
            field=models.BooleanField(default=False, verbose_name='Task Summary'),
        ),
    ]
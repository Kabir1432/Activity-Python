# Generated by Django 4.2.5 on 2023-10-17 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_project', '0014_alter_videoquestionanswers_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenttaskstatus',
            name='submit_time_task_1',
            field=models.DateTimeField(blank=True, null=True, verbose_name='submit time task 1'),
        ),
        migrations.AddField(
            model_name='studenttaskstatus',
            name='submit_time_task_10',
            field=models.DateTimeField(blank=True, null=True, verbose_name='submit time task 10'),
        ),
        migrations.AddField(
            model_name='studenttaskstatus',
            name='submit_time_task_2',
            field=models.DateTimeField(blank=True, null=True, verbose_name='submit time task 2'),
        ),
        migrations.AddField(
            model_name='studenttaskstatus',
            name='submit_time_task_3',
            field=models.DateTimeField(blank=True, null=True, verbose_name='submit time task 3'),
        ),
        migrations.AddField(
            model_name='studenttaskstatus',
            name='submit_time_task_4',
            field=models.DateTimeField(blank=True, null=True, verbose_name='submit time task 4'),
        ),
        migrations.AddField(
            model_name='studenttaskstatus',
            name='submit_time_task_5',
            field=models.DateTimeField(blank=True, null=True, verbose_name='submit time task 5'),
        ),
        migrations.AddField(
            model_name='studenttaskstatus',
            name='submit_time_task_6',
            field=models.DateTimeField(blank=True, null=True, verbose_name='submit time task 6'),
        ),
        migrations.AddField(
            model_name='studenttaskstatus',
            name='submit_time_task_7',
            field=models.DateTimeField(blank=True, null=True, verbose_name='submit time task 7'),
        ),
        migrations.AddField(
            model_name='studenttaskstatus',
            name='submit_time_task_8',
            field=models.DateTimeField(blank=True, null=True, verbose_name='submit time task 8'),
        ),
        migrations.AddField(
            model_name='studenttaskstatus',
            name='submit_time_task_9',
            field=models.DateTimeField(blank=True, null=True, verbose_name='submit time task 9'),
        ),
    ]

# Generated by Django 4.2.5 on 2023-10-13 07:03

import activityngo.utils.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_usermanual_other_projects_video_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermanual',
            name='project_task_1',
        ),
        migrations.RemoveField(
            model_name='usermanual',
            name='project_task_10',
        ),
        migrations.RemoveField(
            model_name='usermanual',
            name='project_task_11',
        ),
        migrations.RemoveField(
            model_name='usermanual',
            name='project_task_2',
        ),
        migrations.RemoveField(
            model_name='usermanual',
            name='project_task_3',
        ),
        migrations.RemoveField(
            model_name='usermanual',
            name='project_task_4',
        ),
        migrations.RemoveField(
            model_name='usermanual',
            name='project_task_5',
        ),
        migrations.RemoveField(
            model_name='usermanual',
            name='project_task_6',
        ),
        migrations.RemoveField(
            model_name='usermanual',
            name='project_task_7',
        ),
        migrations.RemoveField(
            model_name='usermanual',
            name='project_task_8',
        ),
        migrations.RemoveField(
            model_name='usermanual',
            name='project_task_9',
        ),
        migrations.AlterField(
            model_name='usermanual',
            name='project_task_file_10',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task 10 tutorial file'),
        ),
        migrations.AlterField(
            model_name='usermanual',
            name='project_task_file_11',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task 11 tutorial file'),
        ),
        migrations.AlterField(
            model_name='usermanual',
            name='project_task_file_3',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task 3 tutorial file'),
        ),
        migrations.AlterField(
            model_name='usermanual',
            name='project_task_file_4',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task 4 tutorial file'),
        ),
        migrations.AlterField(
            model_name='usermanual',
            name='project_task_file_5',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task 5 tutorial file'),
        ),
        migrations.AlterField(
            model_name='usermanual',
            name='project_task_file_6',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task 6 tutorial file'),
        ),
        migrations.AlterField(
            model_name='usermanual',
            name='project_task_file_7',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task 7 tutorial file'),
        ),
        migrations.AlterField(
            model_name='usermanual',
            name='project_task_file_8',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task 8 tutorial file'),
        ),
        migrations.AlterField(
            model_name='usermanual',
            name='project_task_file_9',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task 9 tutorial file'),
        ),
    ]

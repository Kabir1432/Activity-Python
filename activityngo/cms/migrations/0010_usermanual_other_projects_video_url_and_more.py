# Generated by Django 4.2.5 on 2023-10-13 06:47

import activityngo.utils.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_alter_cms_meta_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermanual',
            name='other_projects_video_url',
            field=models.URLField(blank=True, max_length=251, null=True, verbose_name='video url'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='other_screenshot_tutorial',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_screenshot_tutorial_path, verbose_name='text_tutorial'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='other_text_tutorial',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_text_tutorial_path, verbose_name='text_tutorial'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_1',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='How To Complete Task 1'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_10',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='How To Complete Task 10'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_11',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='How To Complete Task 11'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_2',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='How To Complete Task 2'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_3',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='How To Complete Task 3'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_4',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='How To Complete Task 4'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_5',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='How To Complete Task 5'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_6',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='How To Complete Task 6'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_7',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='How To Complete Task 7'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_8',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='How To Complete Task 8'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_9',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='How To Complete Task 9'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_file_1',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task 1 tutorial file'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_file_10',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task tutorial file'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_file_11',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task tutorial file'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_file_2',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task 2 tutorial file'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_file_3',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task tutorial file'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_file_4',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task tutorial file'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_file_5',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task tutorial file'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_file_6',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task tutorial file'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_file_7',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task tutorial file'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_file_8',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task tutorial file'),
        ),
        migrations.AddField(
            model_name='usermanual',
            name='project_task_file_9',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_user_manual_project_task_tutorial, verbose_name='Complete task tutorial file'),
        ),
    ]

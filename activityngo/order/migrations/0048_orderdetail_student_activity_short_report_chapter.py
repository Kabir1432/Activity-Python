# Generated by Django 4.2.5 on 2024-01-30 08:09

import activityngo.utils.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0047_orderdetail_student_activity_task_2_and_10'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='student_activity_short_report_chapter',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_student_activity_chapters_file_filename),
        ),
    ]
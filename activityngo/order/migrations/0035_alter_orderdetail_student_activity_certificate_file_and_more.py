# Generated by Django 4.2.5 on 2024-01-11 08:00

import activityngo.utils.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0034_orderdetail_student_activity_certificate_page_1_to_5_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='student_activity_certificate_file',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_student_activity_certificate_file_filename),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='student_activity_certificate_page_1_to_5_file',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_student_activity_certificate_page_1_to_5_file_filename),
        ),
    ]

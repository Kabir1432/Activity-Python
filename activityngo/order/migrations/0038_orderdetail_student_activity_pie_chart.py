# Generated by Django 4.2.5 on 2024-01-17 05:35

import activityngo.utils.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0037_orderdetail_report_generate_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='student_activity_pie_chart',
            field=models.ImageField(blank=True, null=True, upload_to=activityngo.utils.utils.get_student_pie_chart_filename),
        ),
    ]

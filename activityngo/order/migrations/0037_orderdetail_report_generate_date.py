# Generated by Django 4.2.5 on 2024-01-16 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0036_orderdetail_student_activity_chapters'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='report_generate_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Report generate date'),
        ),
    ]
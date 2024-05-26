# Generated by Django 4.2.1 on 2023-09-14 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cron_logger', '0002_alter_cronlogger_cron_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cronlogger',
            name='cron_name',
            field=models.CharField(choices=[('discount_start_end_cron', 'discount_start_end_cron'), ('remove_log_of_after_7_days', 'remove_log_of_after_7_days'), ('empty_cart_model', 'empty_cart_model'), ('inactive_student_after_1_year', 'inactive_student_after_1_year'), ('inactive_5_year_old_student', 'inactive_5_year_old_student')], max_length=100, verbose_name='Cron Name'),
        ),
    ]

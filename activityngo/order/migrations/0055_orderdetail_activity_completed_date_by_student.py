# Generated by Django 4.2.5 on 2024-02-29 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0054_orderdetail_number_of_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='activity_completed_date_by_student',
            field=models.DateTimeField(null=True, verbose_name='Activity subscribed date By student'),
        ),
    ]

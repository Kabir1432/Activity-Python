# Generated by Django 4.2.5 on 2024-01-19 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0041_orderdetailadmin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='student_activity_pie_chart_21',
        ),
    ]

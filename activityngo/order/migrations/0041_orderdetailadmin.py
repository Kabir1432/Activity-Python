# Generated by Django 4.2.5 on 2024-01-17 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0040_orderdetail_student_activity_pie_chart_10_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetailAdmin',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('order.orderdetail',),
        ),
    ]

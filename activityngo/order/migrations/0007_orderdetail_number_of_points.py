# Generated by Django 4.2.1 on 2023-08-23 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_orderdetail_project_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='number_of_points',
            field=models.CharField(choices=[('points_20', '20 Points'), ('points_10', '10 Points'), ('points_05', '05 Points')], default='points_20', max_length=10),
        ),
    ]

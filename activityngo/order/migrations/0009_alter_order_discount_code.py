# Generated by Django 4.2.1 on 2023-08-23 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0002_discount_user'),
        ('order', '0008_orderdetail_create_time_orderdetail_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='discount_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='discount.discount'),
        ),
    ]

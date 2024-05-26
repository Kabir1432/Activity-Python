# Generated by Django 4.2.5 on 2024-02-09 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0049_alter_order_discount_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='activity_completed_date',
            field=models.DateTimeField(null=True, verbose_name='Activity completed date'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='activity_subscribed_date',
            field=models.DateTimeField(null=True, verbose_name='Activity subscribed date'),
        ),
    ]
# Generated by Django 4.2.1 on 2023-08-23 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_order_discount_code'),
        ('cart', '0013_remove_orderdetail_order_remove_orderdetail_product_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DiscountCode',
        ),
    ]

# Generated by Django 4.2.1 on 2023-08-23 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_gstcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='quantity',
        ),
    ]

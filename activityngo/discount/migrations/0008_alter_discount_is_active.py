# Generated by Django 4.2.1 on 2023-08-31 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0007_alter_discountusage_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]

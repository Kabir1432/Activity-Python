# Generated by Django 4.2.1 on 2023-08-25 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0003_discountusage'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='discountusage',
            unique_together=set(),
        ),
    ]

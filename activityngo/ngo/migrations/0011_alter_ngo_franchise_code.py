# Generated by Django 4.2.1 on 2023-07-19 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngo', '0010_ngo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ngo',
            name='franchise_code',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]

# Generated by Django 4.2.1 on 2023-07-12 13:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngo', '0005_alter_organization_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=10, validators=[django.core.validators.MinValueValidator(-90)], verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=10, validators=[django.core.validators.MinValueValidator(-180)], verbose_name='longitude'),
        ),
    ]
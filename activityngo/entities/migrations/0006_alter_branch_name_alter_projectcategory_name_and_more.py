# Generated by Django 4.2.5 on 2023-11-21 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0005_batches_disable_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(error_messages={'unique': 'Branch name already exists.'}, max_length=128, unique=True, verbose_name='Branch Name'),
        ),
        migrations.AlterField(
            model_name='projectcategory',
            name='name',
            field=models.CharField(error_messages={'unique': 'Activity Category name already exists.'}, max_length=256, unique=True, verbose_name='Project Category Name'),
        ),
        migrations.AlterField(
            model_name='projecttype',
            name='type',
            field=models.CharField(error_messages={'unique': 'Activity Type already exists.'}, max_length=64, unique=True, verbose_name='Project Type'),
        ),
    ]

# Generated by Django 4.2.1 on 2023-09-04 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0014_alter_collegebatches_college_degree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='address',
            field=models.TextField(verbose_name='College Address'),
        ),
        migrations.AlterField(
            model_name='college',
            name='name',
            field=models.CharField(error_messages={'unique': 'College name already exists.'}, max_length=64, unique=True, verbose_name='College Name'),
        ),
    ]

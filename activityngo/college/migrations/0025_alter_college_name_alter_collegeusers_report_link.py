# Generated by Django 4.2.5 on 2023-11-21 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0024_collegecollaboration_meta_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='name',
            field=models.CharField(error_messages={'unique': 'College name already exists.'}, max_length=256, unique=True, verbose_name='College Name'),
        ),
        migrations.AlterField(
            model_name='collegeusers',
            name='report_link',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Report Link'),
        ),
    ]

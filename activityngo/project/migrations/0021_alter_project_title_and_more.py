# Generated by Django 4.2.5 on 2023-11-22 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_project_is_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Project Title'),
        ),
        migrations.AlterField(
            model_name='projectdetails',
            name='field_visit_mandation',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Field Visit Mandation'),
        ),
    ]

# Generated by Django 4.2.1 on 2023-09-01 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0012_collegebatches'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collegebatches',
            old_name='college',
            new_name='college_degree',
        ),
    ]
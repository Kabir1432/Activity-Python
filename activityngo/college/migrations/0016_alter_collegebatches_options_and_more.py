# Generated by Django 4.2.1 on 2023-09-04 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0015_alter_college_address_alter_college_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collegebatches',
            options={'verbose_name': 'CollegeBatches', 'verbose_name_plural': 'College Batches'},
        ),
        migrations.AlterModelOptions(
            name='collegedegree',
            options={'verbose_name': 'College Degree', 'verbose_name_plural': 'College Degree'},
        ),
    ]
# Generated by Django 4.2.1 on 2023-07-31 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngo', '0023_alter_directors_director_no_alter_directors_pan_no'),
        ('project', '0002_projectdetails'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProjectBasicDetails',
            new_name='Project',
        ),
    ]

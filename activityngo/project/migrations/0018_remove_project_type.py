# Generated by Django 4.2.5 on 2023-11-08 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_alter_project_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='type',
        ),
    ]
# Generated by Django 4.2.5 on 2023-11-10 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0019_project_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_visible',
            field=models.BooleanField(default=False, verbose_name='Is Visible'),
        ),
    ]

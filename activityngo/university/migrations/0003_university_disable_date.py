# Generated by Django 4.2.1 on 2023-07-17 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_remove_university_project_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='disable_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

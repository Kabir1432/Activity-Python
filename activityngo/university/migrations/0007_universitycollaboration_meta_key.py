# Generated by Django 4.2.5 on 2023-10-19 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0006_universitycollaboration_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='universitycollaboration',
            name='meta_key',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True),
        ),
    ]

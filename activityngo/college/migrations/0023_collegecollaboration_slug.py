# Generated by Django 4.2.5 on 2023-10-19 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0022_branchbatches_disable_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collegecollaboration',
            name='slug',
            field=models.SlugField(blank=True, max_length=64, null=True, verbose_name='slug'),
        ),
    ]
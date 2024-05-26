# Generated by Django 4.2.1 on 2023-07-17 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0002_alter_branch_name_alter_degree_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='disable_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='degree',
            name='disable_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='projectcategory',
            name='disable_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='projecttype',
            name='disable_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='disable_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

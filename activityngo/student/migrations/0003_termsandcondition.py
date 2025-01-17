# Generated by Django 4.2.1 on 2023-08-14 10:37

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_aboutus_contactus_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsAndCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('meta_value', tinymce.models.HTMLField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

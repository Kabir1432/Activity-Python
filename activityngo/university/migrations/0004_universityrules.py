# Generated by Django 4.2.1 on 2023-08-16 05:56

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0003_university_disable_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniversityRules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('meta_value', tinymce.models.HTMLField()),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='university_rules', to='university.university', verbose_name='University Rules')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

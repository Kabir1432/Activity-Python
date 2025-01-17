# Generated by Django 4.2.1 on 2023-08-17 06:15

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0007_alter_collegeusers_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollegeCollaboration',
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
        migrations.CreateModel(
            name='CollegeCMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('meta_key', models.CharField(choices=[('about_us', 'about_us'), ('our_work', 'OUR WORK'), ('activity_point_projects', 'Activity Point Projects'), ('contact_us', 'Contact Us')], max_length=32)),
                ('slug', models.SlugField(blank=True, max_length=64, null=True, unique=True, verbose_name='slug')),
                ('meta_value', tinymce.models.HTMLField()),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='college_cms', to='college.college')),
            ],
            options={
                'verbose_name': 'College CMS',
                'verbose_name_plural': 'College CMS',
                'unique_together': {('college', 'meta_key')},
            },
        ),
    ]

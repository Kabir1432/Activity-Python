# Generated by Django 4.2.1 on 2023-08-17 13:19

import activityngo.utils.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_complaints'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='complaints',
            options={'verbose_name': 'Complaint', 'verbose_name_plural': 'Complaints'},
        ),
        migrations.AddField(
            model_name='complaints',
            name='issue',
            field=models.TextField(blank=True, null=True, verbose_name='Issue'),
        ),
        migrations.CreateModel(
            name='ComplaintsMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(height_field='height_photo', upload_to=activityngo.utils.utils.get_complaint_photo_random_filename, width_field='width_photo')),
                ('width_photo', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('height_photo', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('complaints', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints_media', to='student.complaints')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
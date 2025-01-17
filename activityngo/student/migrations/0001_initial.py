# Generated by Django 4.2.1 on 2023-08-14 06:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entities', '0005_batches_disable_date'),
        ('university', '0003_university_disable_date'),
        ('college', '0007_alter_collegeusers_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('id_number', models.CharField(max_length=64, verbose_name='Student ID Number')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_batch', to='entities.batches', verbose_name='Student Batch')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_branch', to='entities.branch', verbose_name='Student Branch')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_college', to='college.college', verbose_name='Student College')),
                ('college_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='college_states', to='entities.state', verbose_name='Student College State')),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_degree', to='entities.degree', verbose_name='Student Degree')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_details', to=settings.AUTH_USER_MODEL, verbose_name='Student')),
                ('student_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_states', to='entities.state', verbose_name='Student State')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_university', to='university.university', verbose_name='Student University')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

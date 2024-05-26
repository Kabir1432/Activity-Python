# Generated by Django 4.2.1 on 2023-09-01 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0005_batches_disable_date'),
        ('college', '0011_collegedegree'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollegeBatches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('batches', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='college_degree', to='entities.batches')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colleges_degree', to='college.collegedegree')),
            ],
            options={
                'verbose_name': 'College',
                'verbose_name_plural': 'Colleges',
            },
        ),
    ]

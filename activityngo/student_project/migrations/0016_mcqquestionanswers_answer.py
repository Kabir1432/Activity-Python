# Generated by Django 4.2.5 on 2023-10-20 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_types', '0031_videoquestion_thumbnail'),
        ('student_project', '0015_studenttaskstatus_submit_time_task_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mcqquestionanswers',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mcq_question_answers', to='question_types.mcqoption'),
        ),
    ]

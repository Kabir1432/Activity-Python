# Generated by Django 4.2.5 on 2023-10-16 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_project', '0012_remove_studenttaskstatus_task2_submissions_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dropdownquestionanswers',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='essayquestionanswers',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='exitquestionanswers',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='mcqquestionanswers',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='numericquestionanswers',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='percentagequestionanswers',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='shortquestionanswers',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='surveysdetails',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='uploadphotoquestionanswers',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='videoquestionanswers',
            unique_together=set(),
        ),
    ]

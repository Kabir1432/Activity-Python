# Generated by Django 4.2.5 on 2023-11-01 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_project', '0021_exitquestionanswers_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dropdownquestionanswers',
            name='reject_reason',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Reject Reason'),
        ),
        migrations.AddField(
            model_name='essayquestionanswers',
            name='reject_reason',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Reject Reason'),
        ),
        migrations.AddField(
            model_name='exitquestionanswers',
            name='reject_reason',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Reject Reason'),
        ),
        migrations.AddField(
            model_name='mcqquestionanswers',
            name='reject_reason',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Reject Reason'),
        ),
        migrations.AddField(
            model_name='numericquestionanswers',
            name='reject_reason',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Reject Reason'),
        ),
        migrations.AddField(
            model_name='percentagequestionanswers',
            name='reject_reason',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Reject Reason'),
        ),
        migrations.AddField(
            model_name='shortquestionanswers',
            name='reject_reason',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Reject Reason'),
        ),
        migrations.AddField(
            model_name='uploadphotoquestionanswers',
            name='reject_reason',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Reject Reason'),
        ),
        migrations.AddField(
            model_name='videoquestionanswers',
            name='reject_reason',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Reject Reason'),
        ),
    ]

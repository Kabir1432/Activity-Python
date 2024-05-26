# Generated by Django 4.2.1 on 2023-08-16 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_studentfeedback'),
        ('question_types', '0018_alter_shortanswerquestion_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='numericquestion',
            options={'verbose_name': 'Numeric Question', 'verbose_name_plural': 'Numeric Questions'},
        ),
        migrations.AlterField(
            model_name='numericquestion',
            name='action_needed',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Action Needed by Student'),
        ),
        migrations.AlterField(
            model_name='numericquestion',
            name='answer_character_maximum_limit',
            field=models.IntegerField(blank=True, null=True, verbose_name='Answer Character Maximum Limit'),
        ),
        migrations.AlterField(
            model_name='numericquestion',
            name='answer_character_minimum_limit',
            field=models.IntegerField(blank=True, null=True, verbose_name='Answer Character Minimum Limit'),
        ),
        migrations.AlterField(
            model_name='numericquestion',
            name='characters_allowed_in_answer_box',
            field=models.IntegerField(blank=True, null=True, verbose_name='Characters allowed in Answer Box'),
        ),
        migrations.AlterField(
            model_name='numericquestion',
            name='copy_paste_answer_box',
            field=models.BooleanField(default=True, verbose_name='Copy – Paste option in Answer box'),
        ),
        migrations.AlterField(
            model_name='numericquestion',
            name='copy_paste_question_box',
            field=models.BooleanField(default=True, verbose_name='Copy – Paste option in Question box'),
        ),
        migrations.AlterField(
            model_name='numericquestion',
            name='no_of_digits_allowed',
            field=models.IntegerField(blank=True, null=True, verbose_name='No. of Digits allowed'),
        ),
        migrations.AlterField(
            model_name='numericquestion',
            name='question_character_maximum_limit',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Question Character Maximum Limit'),
        ),
        migrations.AlterField(
            model_name='numericquestion',
            name='special_characters_in_questions',
            field=models.BooleanField(default=True, verbose_name='Special Characters in Questions'),
        ),
        migrations.AlterUniqueTogether(
            name='numericquestion',
            unique_together={('project', 'main_task_number', 'sub_task_number')},
        ),
    ]

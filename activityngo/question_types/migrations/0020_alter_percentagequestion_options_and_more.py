# Generated by Django 4.2.1 on 2023-08-16 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_studentfeedback'),
        ('question_types', '0019_alter_numericquestion_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='percentagequestion',
            options={'verbose_name': 'Percentage Question', 'verbose_name_plural': 'Percentage Questions'},
        ),
        migrations.AlterField(
            model_name='percentagequestion',
            name='action_needed',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Action Needed by Student'),
        ),
        migrations.AlterField(
            model_name='percentagequestion',
            name='answer_character_maximum_limit',
            field=models.IntegerField(blank=True, null=True, verbose_name='Answer Character Maximum Limit'),
        ),
        migrations.AlterField(
            model_name='percentagequestion',
            name='answer_character_minimum_limit',
            field=models.IntegerField(blank=True, null=True, verbose_name='Answer Character Minimum Limit'),
        ),
        migrations.AlterField(
            model_name='percentagequestion',
            name='characters_allowed_in_answer_box',
            field=models.IntegerField(blank=True, null=True, verbose_name='Characters allowed in Answer Box'),
        ),
        migrations.AlterField(
            model_name='percentagequestion',
            name='copy_paste_answer_box',
            field=models.BooleanField(default=True, verbose_name='Copy – Paste option in Answer box'),
        ),
        migrations.AlterField(
            model_name='percentagequestion',
            name='special_characters_in_answer',
            field=models.BooleanField(default=True, verbose_name='Special Characters in Answer'),
        ),
        migrations.AlterField(
            model_name='percentagequestion',
            name='special_characters_in_questions',
            field=models.BooleanField(default=True, verbose_name='Special Characters in Questions'),
        ),
        migrations.AlterUniqueTogether(
            name='percentagequestion',
            unique_together={('project', 'main_task_number', 'sub_task_number')},
        ),
    ]
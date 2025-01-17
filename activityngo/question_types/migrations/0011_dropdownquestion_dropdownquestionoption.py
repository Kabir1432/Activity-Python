# Generated by Django 4.2.1 on 2023-08-01 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_types', '0010_mcqoption_right_answer_option_among_multiple_choice'),
    ]

    operations = [
        migrations.CreateModel(
            name='DropdownQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('question', models.CharField(max_length=512, verbose_name='Question')),
                ('number_of_options', models.IntegerField(verbose_name='Number of Options')),
                ('question_character_maximum_limit', models.IntegerField(null=True, verbose_name='Question Character Maximum Limit')),
                ('copy_paste_question_box', models.BooleanField(verbose_name='Copy – Paste option in Question box')),
                ('special_characters_in_questions', models.BooleanField(verbose_name='Special Characters in Questions')),
                ('number_of_dropdowns_in_mcq', models.IntegerField(null=True, verbose_name='Number of Dropdowns in MCQ')),
                ('copy_paste_answer_mcq_option_box', models.BooleanField(verbose_name='Copy – Paste option in Answer box')),
                ('special_characters_in_mcq_option_box', models.BooleanField(verbose_name='Special Characters in MCQ Option box')),
                ('action_needed', models.CharField(max_length=512, verbose_name='Action Needed by Student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DropdownQuestionOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('option', models.CharField(max_length=512, verbose_name='Option')),
                ('right_answer_option_among_multiple_choice', models.BooleanField(default=False, verbose_name='right_answer_option_among_multiple_choice')),
                ('dropdown_question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dropdown_question_option', to='question_types.dropdownquestion')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

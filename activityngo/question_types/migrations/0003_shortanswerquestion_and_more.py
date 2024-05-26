# Generated by Django 4.2.1 on 2023-07-31 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question_types', '0002_essay_question_alter_videoquestion_title_max_limit_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortAnswerQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('question_character_maximum_limit', models.CharField(max_length=512, verbose_name='Question Character Maximum Limit')),
                ('copy_paste_question_box', models.BooleanField(verbose_name='Copy – Paste option in Question box')),
                ('special_characters_in_questions', models.BooleanField(verbose_name='Special Characters in Questions')),
                ('action_needed', models.CharField(max_length=512, verbose_name='Action Needed by Student')),
                ('characters_allowed_in_answer_box', models.CharField(max_length=512, verbose_name='Characters allowed in Answer Box')),
                ('special_characters_in_answer_box', models.BooleanField(verbose_name='Special Characters in Answer Box')),
                ('grammar_check_in_answer_box', models.BooleanField(verbose_name='Grammar Check in Answer Box')),
                ('answer_character_minimum_limit', models.BooleanField(verbose_name='Answer Character Minimum Limit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='Essay_Question',
            new_name='EssayQuestion',
        ),
    ]

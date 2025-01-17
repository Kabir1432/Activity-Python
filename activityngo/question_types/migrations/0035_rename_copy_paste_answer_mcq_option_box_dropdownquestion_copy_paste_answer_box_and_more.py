# Generated by Django 4.2.5 on 2023-11-08 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question_types', '0034_shortanswerquestion_copy_paste_answer_box'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dropdownquestion',
            old_name='copy_paste_answer_mcq_option_box',
            new_name='copy_paste_answer_box',
        ),
        migrations.RenameField(
            model_name='dropdownquestion',
            old_name='special_characters_in_mcq_option_box',
            new_name='special_characters_in_answer_box',
        ),
        migrations.RenameField(
            model_name='exittestquestion',
            old_name='copy_paste_answer_mcq_option_box',
            new_name='copy_paste_answer_box',
        ),
        migrations.RenameField(
            model_name='exittestquestion',
            old_name='special_characters_in_mcq_option_box',
            new_name='special_characters_in_answer_box',
        ),
        migrations.RenameField(
            model_name='mcqquestion',
            old_name='copy_paste_answer_mcq_option_box',
            new_name='copy_paste_answer_box',
        ),
        migrations.RenameField(
            model_name='mcqquestion',
            old_name='special_characters_in_mcq_option_box',
            new_name='special_characters_in_answer_box',
        ),
    ]

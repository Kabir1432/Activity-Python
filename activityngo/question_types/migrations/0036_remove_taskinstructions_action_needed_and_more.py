# Generated by Django 4.2.5 on 2024-01-08 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question_types', '0035_rename_copy_paste_answer_mcq_option_box_dropdownquestion_copy_paste_answer_box_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskinstructions',
            name='action_needed',
        ),
        migrations.RemoveField(
            model_name='taskinstructions',
            name='copy_paste_option_in_instruction_box',
        ),
        migrations.RemoveField(
            model_name='taskinstructions',
            name='image_in_instruction_box',
        ),
        migrations.RemoveField(
            model_name='taskinstructions',
            name='instructions_character_maximum_limit',
        ),
        migrations.RemoveField(
            model_name='taskinstructions',
            name='special_characters_in_instruction_box',
        ),
        migrations.RemoveField(
            model_name='taskinstructions',
            name='url_in_instruction_box',
        ),
    ]

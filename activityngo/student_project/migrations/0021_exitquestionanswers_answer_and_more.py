# Generated by Django 4.2.5 on 2023-11-01 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_types', '0034_shortanswerquestion_copy_paste_answer_box'),
        ('student_project', '0020_dropdownquestionanswers_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exitquestionanswers',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exit_question_answers', to='question_types.exittestquestionoption'),
        ),
        migrations.DeleteModel(
            name='ExitSelectedOptions',
        ),
    ]
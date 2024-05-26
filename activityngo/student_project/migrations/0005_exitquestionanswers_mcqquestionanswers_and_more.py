# Generated by Django 4.2.1 on 2023-08-25 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_types', '0028_taskinstructions_task_completed_hours'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0010_alter_order_order_number_alter_order_user'),
        ('student_project', '0004_shortquestionanswers'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExitQuestionAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Submitted', 'Submitted')], max_length=10, verbose_name='Status')),
                ('order_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exit_question_order_details', to='order.orderdetail')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exit_question_answers', to='question_types.exittestquestion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exit_question_answers_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Exit Question Answers',
                'verbose_name_plural': 'Exit Questions Answers',
                'unique_together': {('question', 'user', 'order_details')},
            },
        ),
        migrations.CreateModel(
            name='MCQQuestionAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Submitted', 'Submitted')], max_length=10, verbose_name='Status')),
                ('order_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcq_question_order_details', to='order.orderdetail')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcq_question_answers', to='question_types.mcqquestion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcq_question_answers_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'MCQ Question Answers',
                'verbose_name_plural': 'MCQ Questions Answers',
                'unique_together': {('question', 'user', 'order_details')},
            },
        ),
        migrations.CreateModel(
            name='MCQSelectedOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('answer', models.CharField(blank=True, max_length=512, null=True, verbose_name='Answer')),
                ('question_answers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcq_selected_options', to='student_project.mcqquestionanswers')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExitSelectedOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('answer', models.CharField(blank=True, max_length=512, null=True, verbose_name='Answer')),
                ('question_answers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exit_selected_options', to='student_project.exitquestionanswers')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PercentageQuestionAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Submitted', 'Submitted')], max_length=10, verbose_name='Status')),
                ('answer', models.CharField(blank=True, max_length=512, null=True, verbose_name='Answer')),
                ('order_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='percentage_question_order_details', to='order.orderdetail')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='percentage_question_answers', to='question_types.percentagequestion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='percentage_question_answers_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Percentage Question Answers',
                'verbose_name_plural': 'Percentage Questions Answers',
                'unique_together': {('question', 'user', 'order_details')},
            },
        ),
        migrations.CreateModel(
            name='NumericQuestionAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Submitted', 'Submitted')], max_length=10, verbose_name='Status')),
                ('answer', models.CharField(blank=True, max_length=512, null=True, verbose_name='Answer')),
                ('order_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numeric_question_order_details', to='order.orderdetail')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numeric_question_answers', to='question_types.numericquestion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numeric_question_answers_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Numeric Question Answers',
                'verbose_name_plural': 'Numeric Questions Answers',
                'unique_together': {('question', 'user', 'order_details')},
            },
        ),
        migrations.CreateModel(
            name='DropDownQuestionAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Submitted', 'Submitted')], max_length=10, verbose_name='Status')),
                ('answer', models.CharField(blank=True, max_length=512, null=True, verbose_name='Answer')),
                ('order_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dropdown_question_order_details', to='order.orderdetail')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dropdown_question_answers', to='question_types.dropdownquestion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dropdown_question_answers_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'DropDown Question Answers',
                'verbose_name_plural': 'DropDown Questions Answers',
                'unique_together': {('question', 'user', 'order_details')},
            },
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-28 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity_report', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportcontent',
            old_name='Abstract',
            new_name='abstract',
        ),
        migrations.RenameField(
            model_name='reportcontent',
            old_name='Chapter_01',
            new_name='chapter_01',
        ),
        migrations.RenameField(
            model_name='reportcontent',
            old_name='Chapter_02',
            new_name='chapter_02',
        ),
        migrations.RenameField(
            model_name='reportcontent',
            old_name='Chapter_03',
            new_name='chapter_03',
        ),
        migrations.RenameField(
            model_name='reportcontent',
            old_name='Chapter_04',
            new_name='chapter_04',
        ),
        migrations.RenameField(
            model_name='reportcontent',
            old_name='Chapter_05',
            new_name='chapter_05',
        ),
        migrations.RenameField(
            model_name='reportcontent',
            old_name='Chapter_06',
            new_name='chapter_06',
        ),
        migrations.RenameField(
            model_name='reportcontent',
            old_name='Chapter_07',
            new_name='chapter_07',
        ),
    ]

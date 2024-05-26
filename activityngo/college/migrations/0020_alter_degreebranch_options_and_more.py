# Generated by Django 4.2.5 on 2023-09-25 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0005_batches_disable_date'),
        ('college', '0019_branchbatches_degreebranch_remove_college_branch_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='degreebranch',
            options={'verbose_name': 'Degree Branch', 'verbose_name_plural': 'Degree Branch'},
        ),
        migrations.AlterUniqueTogether(
            name='collegedegree',
            unique_together={('college', 'degree')},
        ),
        migrations.AlterUniqueTogether(
            name='degreebranch',
            unique_together={('college_degree', 'branch')},
        ),
    ]

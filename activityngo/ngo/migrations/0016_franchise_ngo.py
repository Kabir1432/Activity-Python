# Generated by Django 4.2.1 on 2023-07-24 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ngo', '0015_franchise'),
    ]

    operations = [
        migrations.AddField(
            model_name='franchise',
            name='ngo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ngo_franchise', to='ngo.ngo'),
        ),
    ]

# Generated by Django 3.0.2 on 2020-01-28 11:09

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20200127_0429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(validators=[profiles.models.dateValidator]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lastname',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

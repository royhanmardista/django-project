# Generated by Django 3.0.2 on 2020-01-28 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20200128_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='nationality',
        ),
    ]

# Generated by Django 3.0.2 on 2020-01-28 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_auto_20200128_1550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user_id',
            new_name='user',
        ),
    ]

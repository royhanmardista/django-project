# Generated by Django 3.0.2 on 2020-01-28 14:08

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_remove_profile_nationality'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='nationality',
            field=django_countries.fields.CountryField(default='non', max_length=2),
        ),
    ]
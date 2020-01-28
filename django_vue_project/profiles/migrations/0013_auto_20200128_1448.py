# Generated by Django 3.0.2 on 2020-01-28 14:48

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_profile_nationality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nationality',
            field=django_countries.fields.CountryField(default='ID', max_length=2),
        ),
    ]
# Generated by Django 3.0.2 on 2020-01-25 19:27

import django.core.validators
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='firstname',
            field=models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=6),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nationality',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
# Generated by Django 3.0.2 on 2020-01-26 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20200126_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='default.jpg', upload_to='profile_pic'),
        ),
    ]

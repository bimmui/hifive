# Generated by Django 3.1.7 on 2021-08-14 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_blacklisted',
            field=models.BooleanField(default=False),
        ),
    ]
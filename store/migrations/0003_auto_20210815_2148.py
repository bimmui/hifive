# Generated by Django 3.1.7 on 2021-08-16 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_users_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.URLField(blank=True, max_length=500, unique=True),
        ),
    ]
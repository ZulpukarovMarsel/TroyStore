# Generated by Django 5.0.1 on 2024-02-03 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productphoto',
            name='photo',
            field=models.ImageField(upload_to='photo_product'),
        ),
    ]
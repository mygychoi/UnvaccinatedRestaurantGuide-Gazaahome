# Generated by Django 3.2 on 2021-11-19 12:45

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beauty', '0005_remove_face_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='face',
            name='temp',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='image'),
        ),
    ]

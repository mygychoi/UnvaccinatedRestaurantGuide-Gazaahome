# Generated by Django 3.2 on 2021-11-19 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beauty', '0008_face_temp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='face',
            name='temp',
        ),
    ]

# Generated by Django 3.2 on 2021-11-18 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recode',
            name='face',
            field=models.ImageField(upload_to='beauty/faces/%Y/%m/%d/'),
        ),
    ]
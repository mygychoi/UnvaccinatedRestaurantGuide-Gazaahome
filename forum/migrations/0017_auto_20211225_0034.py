# Generated by Django 3.2.9 on 2021-12-25 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0016_alter_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
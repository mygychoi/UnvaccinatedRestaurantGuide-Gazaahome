# Generated by Django 3.2.9 on 2021-12-31 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_forum', '0004_remove_videotag_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]

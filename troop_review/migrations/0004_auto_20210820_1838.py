# Generated by Django 3.2 on 2021-08-20 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troop_review', '0003_alter_review_training'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='discipline',
            field=models.CharField(choices=[('very_high', '빡세다'), ('high', '세다'), ('nomal', '보통'), ('low', '약하다'), ('very_low', '빠졌다')], default='nomal', max_length=9),
        ),
        migrations.AlterField(
            model_name='review',
            name='training',
            field=models.CharField(choices=[('very_high', '매우 많음'), ('high', '많음'), ('nomal', '보통'), ('low', '적음'), ('very_low', '매우 적음')], default='nomal', max_length=9),
        ),
    ]

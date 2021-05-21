# Generated by Django 3.2 on 2021-05-21 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workday', '0006_auto_20210521_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculator',
            name='end_date',
            field=models.DateField(help_text='날짜형식: <em>2021-01-01</em>'),
        ),
        migrations.AlterField(
            model_name='calculator',
            name='start_date',
            field=models.DateField(help_text='날짜형식: <em>2021-01-01</em>'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='end_date',
            field=models.DateField(help_text='날짜형식: <em>2021-01-01</em>'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='start_date',
            field=models.DateField(help_text='날짜형식: <em>2021-01-01</em>'),
        ),
    ]

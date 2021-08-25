# Generated by Django 3.2 on 2021-08-25 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20210825_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='barracks_count',
            field=models.IntegerField(verbose_name='barracks'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='calculator_count',
            field=models.IntegerField(verbose_name='calculator'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='calculator_increment',
            field=models.IntegerField(verbose_name='calculator increment'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='comment_count',
            field=models.IntegerField(verbose_name='comment'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='guest_book_count',
            field=models.IntegerField(verbose_name='guest book'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='leave_count',
            field=models.IntegerField(verbose_name='leave'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='post_count',
            field=models.IntegerField(verbose_name='post'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='review_count',
            field=models.IntegerField(verbose_name='review'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='state_date',
            field=models.DateField(verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='troop_count',
            field=models.IntegerField(verbose_name='troop'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='user_count',
            field=models.IntegerField(verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='user_increment',
            field=models.IntegerField(verbose_name='user increment'),
        ),
    ]

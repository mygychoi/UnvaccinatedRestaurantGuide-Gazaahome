# Generated by Django 3.2.9 on 2021-12-29 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corona', '0013_restaurantdeleterequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='FastRestaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('verifieded', models.BooleanField(default=False)),
                ('url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(max_length=20)),
                ('tags', models.CharField(blank=True, max_length=20)),
                ('unvaccinated_pass', models.CharField(max_length=20)),
                ('num_likes', models.IntegerField(default=0)),
                ('num_dislikes', models.IntegerField(default=0)),
                ('num_comments', models.IntegerField(default=0)),
            ],
        ),
    ]

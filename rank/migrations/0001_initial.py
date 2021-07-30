# Generated by Django 3.2 on 2021-07-30 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workday', '0008_alter_calculator_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankingChart',
            fields=[
                ('calculator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='workday.calculator')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('end_workday', models.DateField(blank=True, null=True)),
                ('num_workdays', models.IntegerField(blank=True, null=True)),
                ('num_remaindays', models.IntegerField(blank=True, null=True)),
                ('percent', models.FloatField(blank=True, null=True)),
                ('workday_percent', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

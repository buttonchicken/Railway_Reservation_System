# Generated by Django 2.2.20 on 2021-11-27 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0025_auto_20211127_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='train_status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_id', models.CharField(max_length=6)),
                ('last_departure_station', models.CharField(max_length=1)),
                ('last_departure_date', models.CharField(max_length=100)),
            ],
        ),
    ]

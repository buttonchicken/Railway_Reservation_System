# Generated by Django 2.2.20 on 2021-11-26 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0019_remove_train_capacity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_id', models.CharField(max_length=6)),
                ('DepartureDate', models.CharField(default='', max_length=25)),
                ('current_capacity', models.IntegerField(default=0)),
            ],
        ),
    ]

# Generated by Django 2.2.20 on 2021-11-22 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Members',
        ),
    ]

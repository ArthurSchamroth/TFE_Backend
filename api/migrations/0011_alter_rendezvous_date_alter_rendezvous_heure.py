# Generated by Django 4.0 on 2022-04-11 14:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_rendezvous'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rendezvous',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='rendezvous',
            name='heure',
            field=models.TimeField(default=datetime.datetime.now),
        ),
    ]

# Generated by Django 4.0 on 2022-04-18 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_rendezvous_type_soin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichepatient',
            name='age',
            field=models.DateField(null=True),
        ),
    ]

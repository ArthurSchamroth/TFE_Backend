# Generated by Django 4.0 on 2022-05-16 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_alter_routine_videos'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichepatient',
            name='autorisation_consultation',
            field=models.BooleanField(default=False),
        ),
    ]

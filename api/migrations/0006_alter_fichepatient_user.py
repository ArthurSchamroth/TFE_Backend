# Generated by Django 4.0 on 2022-04-04 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0018_remove_user_naissance'),
        ('api', '0005_alter_fichepatient_adresse_alter_fichepatient_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichepatient',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]

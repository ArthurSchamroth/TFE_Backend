# Generated by Django 4.0 on 2022-04-11 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_commentaire_commentaire'),
    ]

    operations = [
        migrations.CreateModel(
            name='RendezVous',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('heure', models.TimeField()),
                ('type_rdv', models.CharField(choices=[('D', 'Domicile'), ('C', 'Cabinet')], max_length=1)),
                ('description', models.TextField(max_length=320, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fichepatient')),
            ],
        ),
    ]

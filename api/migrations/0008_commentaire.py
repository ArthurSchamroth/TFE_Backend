# Generated by Django 4.0 on 2022-04-07 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0018_remove_user_naissance'),
        ('api', '0007_alter_fichepatient_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auteur_nom', models.CharField(max_length=32)),
                ('auteur_prenom', models.CharField(max_length=32)),
                ('commentaire', models.TextField(blank=True, max_length=1024)),
                ('date_heure', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]

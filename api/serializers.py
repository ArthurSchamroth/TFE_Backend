from rest_framework import serializers
from .models import FichePatient, Commentaire, RendezVous, Message, VideoTuto, Routine
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        FichePatient.objects.Create(user=user)
        return user


class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = ('id', 'user', 'auteur_nom', 'auteur_prenom', 'commentaire', 'date_heure')


class FichePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichePatient
        fields = ('id', 'user', "nom", "prenom", "age", "adresse_mail", 'type_kine', "description_probleme", "adresse",
                  "autorisation_consultation")


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ("key", "user", "created")


class RendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = ('id', 'user', 'date', 'heure', 'type_rdv', 'description', 'type_soin')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'user', 'date', 'heure', 'dest', 'contenu')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoTuto
        fields = ('id', 'titre', 'url')


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ('id', 'user', 'titre_routine', 'description_detaillee', 'videos')

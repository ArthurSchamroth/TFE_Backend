from django.shortcuts import render
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import FichePatient, Commentaire, RendezVous, Message, VideoTuto, Routine
from .serializers import FichePatientSerializer, UserSerializer, \
    TokenSerializer, CommentaireSerializer, RendezVousSerializer, MessageSerializer, VideoSerializer, RoutineSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.forms.models import model_to_dict
import json


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['DELETE'])
    def del_user(self, request):
        if 'id' in request.data:
            try:
                user_id = request.data['id']
                user = User.objects.get(id=user_id)
                user.delete()
                response = {'result': 'ok'}
                return Response(response)
            except:
                response = {'result': 'pas ok'}
                return Response(response)
        else:
            response = {'result': "pas d'id"}
            return Response(response)

class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['POST'])
    def getSpecificToken(self, request, token=None):
        if 'token' in request.data:
            try:
                user = request.user
                token = request.data['token']
                patient_wth_token = Token.objects.get(key=token)
                id = patient_wth_token.user_id
                user = patient_wth_token.user.username
                email = patient_wth_token.user.email
                prenom = patient_wth_token.user.first_name
                nom = patient_wth_token.user.last_name
                actif = patient_wth_token.user.is_active
                try:
                    ficheId = patient_wth_token.user.fichepatient.id
                    ficheTypeKine = patient_wth_token.user.fichepatient.type_kine
                    ficheAge = patient_wth_token.user.fichepatient.age
                    ficheAdresse = patient_wth_token.user.fichepatient.adresse
                    ficheProb = patient_wth_token.user.fichepatient.description_probleme
                    autorisation = patient_wth_token.user.fichepatient.autorisation_consultation
                    response = {'id': id, 'username': user, 'email': email, 'prenom': prenom,
                                'nom': nom, 'fiche': ficheId, "type_kine": ficheTypeKine, 'age': ficheAge,
                                'adresse': ficheAdresse, 'probleme': ficheProb, 'autorisation': autorisation}
                except:
                    response = {'id': id, 'username': user, 'email': email, 'prenom': prenom,
                                'nom': nom, 'actif': actif}
                return Response(response, status=status.HTTP_200_OK)

            except:
                response = {'result': "token inconnu"}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'result': 'Pas de token'}
            return Response(response, status=status.HTTP_200_OK)


class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['POST'])
    def update_commentaire(self, request, user=None):
        if 'user' in request.data:
            user_id = request.data['user']
            comm = Commentaire.objects.get(user=user_id)
            comm.auteur_nom = request.data['auteur_nom']
            comm.auteur_prenom = request.data['auteur_prenom']
            comm.commentaire = request.data['commentaire']
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            comm.date_heure = now
            comm.save()
            response = {'user': 'ok'}
            return Response(response)
        else:
            response = {'user': 'pas ok'}
            return Response(response)

    @action(detail=False, methods=['DELETE'])
    def del_commentaire(self, request):
        if 'id' in request.data:
            try:
                comm_id = request.data['id']
                comm = Commentaire.objects.get(id=comm_id)
                comm.delete()
                response = {'result': 'ok'}
                return Response(response)
            except:
                response = {'result': 'pas ok'}
                return Response(response)
        else:
            response = {'result': "pas d'id"}
            return Response(response)


class FichePatientViewSet(viewsets.ModelViewSet):
    queryset = FichePatient.objects.all()
    serializer_class = FichePatientSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['POST'])
    def update_fiche(self, request, user=None):
        if 'user' in request.data:
            user_id = request.data['user']
            fiche = FichePatient.objects.get(user=user_id)
            fiche.type_kine = request.data['type_kine']
            fiche.description_probleme = request.data['description_probleme']
            fiche.adresse = request.data['adresse']
            try:
                fiche.nom = request.data['nom']
                fiche.prenom = request.data['prenom']
                fiche.adresse_mail = request.data['adresse_mail']
                fiche.age = request.data['age']
                fiche.save()
            except:
                fiche.save()

            response = {'user': 'ok'}
            return Response(response)
        else:
            response = {'user': 'pas ok'}
            return Response(response)

    @action(detail=False, methods=["POST"])
    def getSpecificFiche(self, request, user=None):
        if 'username' in request.data:
            try:
                username = request.data['username']
                patient = User.objects.get(username=username)
                id = patient.id
                nom = patient.fichepatient.nom
                prenom = patient.fichepatient.prenom
                username = patient.username
                naissance = patient.fichepatient.age
                adresse = patient.fichepatient.adresse
                adresse_mail = patient.fichepatient.adresse_mail
                description_prob = patient.fichepatient.description_probleme
                type_besoin = patient.fichepatient.type_kine
                response = {'id': id, 'nom': nom, 'prenom': prenom, 'naissance': naissance,
                            'adresse': adresse, 'adresse_mail': adresse_mail,
                            'description_prob': description_prob, 'type_kine': type_besoin, 'username': username}
                return Response(response, status=status.HTTP_200_OK)

            except:
                response = {'message': 'it s not working'}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'NOOOOO'}
            return Response(response, status=status.HTTP_200_OK)


class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['DELETE'])
    def del_rdv(self, request):
        if 'id' in request.data:
            try:
                rdv_id = request.data['id']
                rdv = RendezVous.objects.get(id=rdv_id)
                rdv.delete()
                response = {'result': 'ok'}
                return Response(response)
            except:
                response = {'result': 'pas ok'}
                return Response(response)
        else:
            response = {'result': "pas d'id"}
            return Response(response)

    @action(detail=False, methods=["POST"])
    def getListSpecificRdv(self, request):
        if 'fiche' in request.data:
            try:
                tableau_response = []
                username = request.data['fiche']
                rdvs = RendezVous.objects.filter(user=username)
                for i in rdvs:
                    object = {'id': i.id, 'nom': i.user.nom, 'prenom': i.user.prenom, 'type_soin': i.type_soin,
                              'adresse': i.user.adresse, 'date': i.date, 'heure': i.heure, 'type_rdv': i.type_rdv,
                              'description': i.description}
                    tableau_response.append(object)

                response = {'result': tableau_response}
                return Response(response, status=status.HTTP_200_OK)

            except:
                response = {'message': 'it s not working'}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'NOOOOO'}
            return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def getRdvByDate(self, request):
        if 'date' in request.data:
            try:
                tableau_response = []
                date = request.data['date']
                rdvs = RendezVous.objects.filter(date=date)
                for i in rdvs:
                    object = {'id': i.id, 'nom': i.user.nom, 'prenom': i.user.prenom, 'type_kine': i.type_soin,
                              'adresse': i.user.adresse, 'date': i.date, 'heure': i.heure, 'type_rdv': i.type_rdv,
                              'description': i.description}
                    tableau_response.append(object)

                response = {'result': tableau_response}
                return Response(response, status=status.HTTP_200_OK)

            except:
                response = {'message': 'it s not working'}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'NOOOOO'}
            return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def getSpecificRdv(self, request):
        if 'id' in request.data:
            try:
                numero_rdv = request.data['id']
                rdv = RendezVous.objects.get(id=numero_rdv)
                id = rdv.id
                nom = rdv.user.nom
                prenom = rdv.user.prenom
                adresse = rdv.user.adresse
                type_kine = rdv.user.type_kine
                date = rdv.date
                heure = rdv.heure
                description = rdv.description
                response = {'id': id, 'nom': nom, 'prenom': prenom, 'adresse': adresse, 'type_kine': type_kine,
                            'date': date, 'heure': heure, 'description': description}
                return Response(response, status=status.HTTP_200_OK)

            except:
                response = {'message': 'pas d\'id correspondante'}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'pas d\'id'}
            return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def getAllRdvsWithName(self, request):
        rdvs = RendezVous.objects.all()
        result = []
        for i in rdvs:
            objet = {'id': i.id, "nom": i.user.nom, "prenom": i.user.prenom, "date": i.date, "heure": i.heure,
                     "type_soin": i.type_soin, "description": i.description}
            result.append(objet)
        response = {"result": result}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def getRdvSpecificPatient(self, request):
        if 'patient' in request.data:
            try:
                patient = request.data['patient']
                rdvs = RendezVous.objects.filter(user=patient)
                result = []
                for i in rdvs:
                    id = i.id
                    user = i.user.id
                    prenom_patient = i.user.prenom
                    nom_patient = i.user.nom
                    date = i.date
                    heure = i.heure
                    type_rdv = i.type_rdv
                    description = i.description
                    type_soin = i.type_soin
                    objet = {'id': id, 'user': user, 'date': date, 'heure': heure, 'type_rdv': type_rdv,
                             'description': description, 'type_soin': type_soin, 'nom_patient': nom_patient,
                             'prenom_patient': prenom_patient}
                    result.append(objet)
                response = {'result': result}
                return Response(response, status=status.HTTP_200_OK)

            except:
                response = {'message': 'pas de patient correspondant'}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'pas de patient'}
            return Response(response, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['DELETE'])
    def del_msg(self, request):
        if 'id' in request.data:
            try:
                msg_id = request.data['id']
                msg = Message.objects.get(id=msg_id)
                msg.delete()
                response = {'result': 'ok'}
                return Response(response)
            except:
                response = {'result': 'pas ok'}
                return Response(response)
        else:
            response = {'result': "pas d'id"}
            return Response(response)

    @action(detail=False, methods=["POST"])
    def getAllAuthors(self, request):
        messages = Message.objects.all()
        result = []
        auteurs = []
        for i in messages:
            auteur = i.user.prenom + " " + i.user.nom
            if auteur not in auteurs:
                auteurs.append(auteur)
                objet = {"auteur": auteur, "auteur_id": i.user_id}
                result.append(objet)
        response = {"result": result}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def getMessagesFromSpecificUser(self, request):
        if 'dest' in request.data:
            try:
                tableau_response = []
                username = request.data['dest']
                messages = Message.objects.filter(dest=username)
                for i in messages:
                    object = {'id': i.id, 'date': i.date, 'heure': i.heure, 'dest': i.dest,
                              'contenu': i.contenu}
                    tableau_response.append(object)

                response = {'result': tableau_response}
                return Response(response, status=status.HTTP_200_OK)

            except:
                response = {'message': 'it s not working'}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'NOOOOO'}
            return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def getMessagesMadeByAUser(self, request):
        if 'user' in request.data:
            try:
                tableau_response = []
                user = request.data['user']
                messages = Message.objects.filter(user_id=user)
                for i in messages:
                    object = {'id': i.id, 'date': i.date, 'heure': i.heure, 'dest': i.dest,
                              'contenu': i.contenu}
                    tableau_response.append(object)

                response = {'result': tableau_response}
                return Response(response, status=status.HTTP_200_OK)

            except:
                response = {'message': 'utilisateur inconnu'}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'pas d\'utilisateur'}
            return Response(response, status=status.HTTP_200_OK)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = VideoTuto.objects.all()
    serializer_class = VideoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['GET'])
    def allInfosVideos(self, request):
        videos = VideoTuto.objects.all()
        liste = []
        for i in videos:
            objt = {"id": i.id, "titre": i.titre, "url": i.url}
            liste.append(objt)
        response = {'result': liste}
        return Response(response)

class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['DELETE'])
    def del_routine(self, request):
        if 'id' in request.data:
            try:
                routine_id = request.data['id']
                routine = Routine.objects.get(id=routine_id)
                routine.delete()
                response = {'result': 'ok'}
                return Response(response)
            except:
                response = {'result': 'pas ok'}
                return Response(response)
        else:
            response = {'result': "pas d'id"}
            return Response(response)

    @action(detail=False, methods=['POST'])
    def getRoutineSpecificUser(self, request):
        if 'user' in request.data:
            try:
                user = request.data['user']
                tableau_response = []
                liste_videos = []
                routines = Routine.objects.filter(user=user)
                for i in routines:
                    for j in i.videos.all():
                        videos = {'id': j.id, 'titre': j.titre, 'url': j.url}
                        liste_videos.append(videos)
                    objet = {
                        'id': i.id, 'user': i.user.id, 'titre_routine': i.titre_routine,
                        'description_detaillee': i.description_detaillee, 'videos': liste_videos
                    }
                    tableau_response.append(objet)
                response = {'result': tableau_response}
                return Response(response, status=status.HTTP_200_OK)
            except:
                response = {'result': 'Ce patient ne possède pas de routine dédiée.'}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'result': 'pas de user'}
            return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def getInfosSpecificRoutine(self, request):
        if 'routine' in request.data:
            try:
                routine = request.data['routine']
                tableau_response = []
                liste_videos = []
                routines = Routine.objects.filter(titre_routine=routine)
                for i in routines:
                    for j in i.videos.all():
                        videos = {'id': j.id, 'titre': j.titre, 'url': j.url}
                        liste_videos.append(videos)
                    objet = {
                        'id': i.id, 'user': i.user.id, 'titre_routine': i.titre_routine,
                        'description_detaillee': i.description_detaillee, 'videos': liste_videos
                    }
                    tableau_response.append(objet)
                response = {'result': tableau_response}
                return Response(response, status=status.HTTP_200_OK)
            except:
                response = {'result': 'Ce patient ne possède pas de routine dédiée.'}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'result': 'pas de user'}
            return Response(response, status=status.HTTP_200_OK)
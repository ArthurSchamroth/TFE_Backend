from django.test import TestCase, Client
from django.contrib.auth.models import User
from api.models import FichePatient, Commentaire, RendezVous, Message, VideoTuto, Routine
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
import json


class SiteTestCase(TestCase):

    def setUp(self):
        self.user = User()
        self.user.username = "TestUserUsername"

        self.user.save()

        self.user2 = User.objects.create_user(
            username="testUsername",
            password="testMdp"
        )
        token, created = Token.objects.get_or_create(user=self.user2)
        self.client = Client(HTTP_AUTHORIZATION="Token " + token.key)
        self.fichePatient = FichePatient()
        self.fichePatient.user = self.user2
        self.fichePatient.nom = "Nom"
        self.fichePatient.prenom = "Prenom"
        self.fichePatient.age = "2000-07-28"
        self.fichePatient.adresse_mail = "Test@hotmail.com"
        self.fichePatient.type_kine = "K"
        self.fichePatient.description_probleme = "Voici une description de test"
        self.fichePatient.adresse = "rue du Test n°1 Louvain-la-Neuve"
        self.fichePatient.autorisation_consultation = "Oui"

        self.fichePatient.save()

    def test_create_fiche_complete(self):
        nbre_element_avant = FichePatient.objects.count()

        fiche = FichePatient()
        fiche.user = self.user
        fiche.nom = "NomTest"
        fiche.prenom = "PrenomTest"
        fiche.age = "2000-07-28"
        fiche.adresse_mail = "Test@gmail.com"
        fiche.type_kine = "K"
        fiche.description_probleme = "Voici une description de test"
        fiche.adresse = "rue du Test n°1 Louvain-la-Neuve"
        fiche.autorisation_consultation = "Oui"

        fiche.save()
        nbre_element_apres = FichePatient.objects.count()
        self.assertTrue(nbre_element_apres == nbre_element_avant + 1)

    def test_create_commentaire_complet(self):
        nbre_element_avant = Commentaire.objects.count()

        commentaire = Commentaire()
        commentaire.user = self.user
        commentaire.auteur_prenom = "Prenom"
        commentaire.auteur_nom = "Nom"
        commentaire.commentaire = "Petit commentaire de test"

        commentaire.save()
        nbre_element_apres = Commentaire.objects.count()
        self.assertTrue(nbre_element_apres == nbre_element_avant + 1)

    def test_create_message_complet(self):
        nbre_element_avant = Message.objects.count()

        message = Message()
        message.user = self.fichePatient
        message.dest = "Nom"
        message.contenu = "Petit commentaire de test"

        message.save()
        nbre_element_apres = Message.objects.count()
        self.assertTrue(nbre_element_apres == nbre_element_avant + 1)

    def test_create_VideoTuto_complet(self):
        nbre_element_avant = VideoTuto.objects.count()

        video = VideoTuto()
        video.titre = "Titre De Video"
        video.url = "https://www.youtube.com/watch?v=Ci7_kJ0FzVk&ab_channel=CrypStanaterYT"

        video.save()
        nbre_element_apres = VideoTuto.objects.count()
        self.assertTrue(nbre_element_apres == nbre_element_avant + 1)

    def test_create_Routine_complet(self):
        nbre_element_avant = Routine.objects.count()

        routine = Routine()
        routine.user = self.fichePatient
        routine.titre_routine = "Routine pour test"
        routine.description_detaillee = "Voici une description complète"

        routine.save()
        nbre_element_apres = Routine.objects.count()
        self.assertTrue(nbre_element_apres == nbre_element_avant + 1)

    def test_create_RendezVous_complet(self):
        nbre_element_avant = RendezVous.objects.count()

        rdv = RendezVous()
        rdv.user = self.fichePatient
        rdv.type_rdv = "D"
        rdv.description = "Description de rdv"
        rdv.type_soin = "Type de soin"

        rdv.save()
        nbre_element_apres = RendezVous.objects.count()
        self.assertTrue(nbre_element_apres == nbre_element_avant + 1)

    def test_listing_users_requete(self):
        c = Client()
        response = c.get("/api/users/")
        self.assertTrue(response.status_code == 200)

    def test_ajout_del_commentaire_requete(self):
        c = Client()
        d = APIClient()
        nbre_element_avant = Commentaire.objects.count()
        response = c.post("/api/commentaires/", {"user": self.user.id, "auteur_nom": "NomAuteur",
                                                 "auteur_prenom": "PrenomAuteur",
                                                 "commentaire": "petit commentaire"})
        # 201 signifie que l'objet a bien été créé
        self.assertTrue(response.status_code == 201)

        nbre_element_apres = Commentaire.objects.count()
        self.assertTrue(nbre_element_avant + 1 == nbre_element_apres)
        # Suppression du commentaire

        response3 = d.delete("/api/commentaires/del_commentaire/", ({}))
        self.assertTrue(response3.status_code == 200)
        a = response3.content.decode()
        self.assertTrue(a == '{"result":"pas d\'id"}')

        response4 = d.delete("/api/commentaires/del_commentaire/", ({'id': 99}))
        self.assertTrue(response4.status_code == 200)
        a = response4.content.decode()
        self.assertTrue(a == '{"result":"pas ok"}')

        response2 = d.delete("/api/commentaires/del_commentaire/", ({'id': 1}))
        self.assertTrue(response2.status_code == 200)
        nbre_element = Commentaire.objects.count()
        # 0 car je n'ai créé que un seul commentaire dans ce test et je viens de le supprimer.
        self.assertTrue(nbre_element == 0)
        a = response2.content.decode()
        self.assertTrue(a == '{"result":"ok"}')

    def test_requetes_rdv(self):
        c = self.client
        response = c.post("/api/rendezVous/",
                          {"user": self.fichePatient.id, "date": "2022-05-30", "heure": "09:00:00",
                           "type_rdv": "D",
                           "description": "description_rdv"})

        # 201, le rdv a été créé
        self.assertTrue(response.status_code == 201)
        nbre_element = RendezVous.objects.count()
        self.assertTrue(nbre_element == 1)

        # je tente de le recup -> ok
        response2 = c.post("/api/rendezVous/getSpecificRdv/", {"id": 1})
        self.assertTrue(json.loads(response2.content.decode())["description"] == "description_rdv")
        self.assertTrue(response2.status_code == 200)

        # je vérifie le nombre de rdv -> 1 -> ok
        response3 = c.get("/api/rendezVous/")
        self.assertTrue(response3.status_code == 200)
        self.assertTrue(len(json.loads(response3.content.decode())) == 1)

        # je teste avec un body vide -> pas d'id -> ok
        response4 = c.post("/api/rendezVous/getSpecificRdv/", {})
        self.assertTrue(response4.status_code == 200)
        self.assertTrue(json.loads(response4.content.decode())["message"] == "pas d'id")

        # je teste avec une id inexistante -> pas d'id correspondate -> ok
        response5 = c.post("/api/rendezVous/getSpecificRdv/", {"id": 99})
        self.assertTrue(response5.status_code == 200)
        self.assertTrue(json.loads(response5.content.decode())["message"] == "pas d'id correspondante")

        # je teste de récupérer les rendez-vous via l'id de l'utilisateur -> 1 rdv pour l'utilisateur 1 -> ok
        response6 = c.post("/api/rendezVous/getRdvSpecificPatient/", {"patient": 1})
        self.assertTrue(response6.status_code == 200)
        self.assertTrue(len(json.loads(response6.content.decode())["result"]) == 1)

        # je teste avec aucun patient -> pas de patient -> ok
        response7 = c.post("/api/rendezVous/getRdvSpecificPatient/", {})
        self.assertTrue(response7.status_code == 200)
        self.assertTrue(json.loads(response7.content.decode())["message"] == "pas de patient")

    def test_del_user_incorrect(self):
        c = APIClient()
        response = c.delete("/api/users/del_user/", {})
        self.assertTrue(response.status_code == 200)
        a = response.content.decode()
        self.assertTrue(a == '{"result":"pas d\'id"}')

    def test_requete_message(self):
        c = self.client
        response = c.post("/api/message/",
                          {"user": self.fichePatient.id, "date": "2022-05-30", "heure": "09:00:00",
                           "dest": "Destinataire", "contenu": "Contenu du message"
                           })
        self.assertTrue(response.status_code == 201)
        nbre_element = Message.objects.count()
        self.assertTrue(nbre_element == 1)

        # erreur 400 car certains paramètres obligatoires ne sont pas fournis (dest et contenu)
        response = c.post("/api/message/",
                          {"user": self.fichePatient.id, "date": "2022-05-30", "heure": "09:00:00"})
        self.assertTrue(response.status_code == 400)

        # je teste la récupération des différents auteurs de msgs -> ici on en a qu'un
        response = c.post("/api/message/getAllAuthors/")
        self.assertTrue(response.status_code == 200)
        a = response.content.decode()
        self.assertTrue(a == '{"result":[{"auteur":"Prenom Nom","auteur_id":1}]}')

        # je teste la récupération des messages écrits par un seul auteur spécifiquement
        response = c.post("/api/message/getMessagesMadeByAUser/", {"user": 1})
        self.assertTrue(response.status_code == 200)
        a = response.content.decode()
        self.assertTrue(a == '{"result":[{"id":1,"date":"2022-05-30","heure":"09:00:00","dest":"Destinataire",'
                             '"contenu":"Contenu du message"}]}')

        response = c.post("/api/message/getMessagesMadeByAUser/", {})
        self.assertTrue(response.status_code == 200)
        a = response.content.decode()
        self.assertTrue(a == '{"message":"pas d\'utilisateur"}')

    def test_requete_token_inconnu(self):
        c = self.client
        response = c.post("/api/tokens/getSpecificToken/", {"token": "f66753586c9a5973c05c0fc877b34955f4b3cf1c"})
        self.assertTrue(response.status_code == 200)
        a = response.content.decode()
        self.assertTrue(a == '{"result":"token inconnu"}')

    def test_get_token_incorrect(self):
        c = Client()
        response = c.post("/api/tokens/getSpecificToken/", {})
        self.assertTrue(response.status_code == 200)
        a = response.content.decode()
        self.assertTrue(a == '{"result":"Pas de token"}')


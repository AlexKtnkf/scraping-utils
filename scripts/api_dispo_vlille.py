# script de requête de la météo prévue à partir de l'API de Openweathermap
# enregistrée en local sur fichier json et poussée en MongoDB
# ---------------------------------------------------------

# importation des différentes librairies nécessaires pour le script
import time

from datetime import datetime

from util_functions.date_methods import serialize_date
from util_functions.db_methods import mongo_cloud_push
from util_functions.scrap_methods import call_api

# !! A VERIFIER ATTENTIVEMENT AVANT TOUTE EXECUTION EN PROD !!
# paramètres du script à exécuter :
# -------------------
# api à requêter
url = 'https://opendata.lillemetropole.fr/api/records/1.0/search/' \
      '?dataset=vlille-realtime&facet=libelle&facet=nom' \
      '&facet=commune&facet=etat&facet=type&facet=etatconnexion&rows=300'
# fréquence de requête en secondes
rate = 60
# chaîne de connexion MongoDB (si applicable)
mongo_uri = None
# hôte de la base de données (laisser vide si utilisation chaîne de connexion)
host = None
# port de la db (laisser vide si utilisation chaîne de connexion)
port = None
# nom d'utilisateur (laisser vide si utilisation chaîne de connexion OU pas d'authentification requise)
user_login = None
# nom d'utilisateur (laisser vide si utilisation chaîne de connexion OU pas d'authentification requise)
user_pass = None
# nom de la db
db_name = 'bclue_datalake'
# nom de la collection où ranger les données
collection_name = 'vlille_availability_realtime'
# fonction de traitement
def callback(data):
    timestamp = data['records'][0]['record_timestamp'].replace("T", " ")
    ts = serialize_date(timestamp, str_format='%Y-%m-%d %H:%M:%S%z')
    data['date_infos'] = ts
   # return None


def fetch_data(beat, url):
    while True:
        data = call_api(url, callback)
        mongo_cloud_push(data, mongo_uri, db_name, collection_name)
        time.sleep(beat)


fetch_data(rate, url)


import time

from util_functions.date_methods import serialize_date
from util_functions.db_methods import mongo_cloud_push
from util_functions.scrap_methods import scrap_website


# méthode de requête du nombre de kilomètre de bouchon autour de la ville de Lille
# obtenu grâce au webscraping du site Coyote

# !! A VERIFIER ATTENTIVEMENT AVANT TOUTE EXECUTION EN PROD !!
# paramètres du script à exécuter :
# -------------------
# site à aspirer
url = 'https://www.ilevia.fr/cms/institutionnel/se-deplacer/#infos-trafic'
# fréquence de passage en secondes
rate = 300
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
db_name = '<nom_à_remplir>'
# nom de la collection où ranger les données
collection_name = '<nom_à_remplir>'
# fonction de traitement
def callback(soup, timestamp):
    is_disruption = 0
    for text in soup('div', {'class': 'l-ligne__item'}):
        vignettes = text.find_all('img')
        for vignette in vignettes:
            src = vignette.get('src')
            if 'metro' in src:
                is_disruption = 1
    ts = serialize_date(timestamp)
    data = {'timestamp': timestamp, 'date_infos': ts, 'ismetrodown': is_disruption}
    return data


def fetch_data(beat, url):
    while True:
        data = scrap_website(url, callback)
        mongo_cloud_push(data, mongo_uri, db_name, collection_name)
        time.sleep(beat)


fetch_data(rate, url)


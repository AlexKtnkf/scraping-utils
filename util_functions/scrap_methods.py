# fonctions de récupération d'infos
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
from bs4 import BeautifulSoup


# requêtage API
def call_api(link, callback):
    dataitems = requests_retry_session().get(link)
    # récupération du fichier json contenu sur l'API
    data = dataitems.json()
    # appel de la fonction de traitement (aucun effet si vide)
    try:
        callback(data)
    except:
        pass
    return data


# scraping site web
# si pas de fonction callback renseignée
def scrap_website(link, callback):
    source = requests_retry_session().get(link).text
    soup = BeautifulSoup(source, 'lxml')
    timestamp = datetime.now()
    data = {}
    # appel de la fonction de traitement (sinon, retournera timestamp + titre du site)
    if callback(soup, timestamp) is not None:
        data = callback(soup, timestamp)
    else:
        data = {
            'timestamp': datetime.now().isoformat(),
            'site_title': soup.title.string
        }
    return data


# gestion des reconnexions
def requests_retry_session(
        retries=15,
        backoff_factor=120,
        status_forcelist=(500, 502, 504),
        session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session



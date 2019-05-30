# Programme de collecte de données

 
## Installation des dépendances

    pip install -r requirements.txt

## Préparation des scripts

Deux exemples de scripts sont présents dans le dossier `/scripts` :

- requêtage API _(disponibilité des V'Lille en exemple)_

- scraping site Web _(page info trafic du réseau Ilévia en exemple)_

Il faut soigneusement renseigner les paramètres demandés. 
Une fonction de nettoyage / traitement appelée `callback()` peut être définie par l'utilisateur.

> Par défaut, ces scripts envoient simplement les données récoltées sur une MongoDB en cloud. Mais d'autres fonctions peuvent être utilisées, elles sont stockées dans le dossier `/util_functions`. Il faut recomposer la fonction `fetch_data()` donnée en exemple en fonction de ce que l'on souhaite.

## Exécution

Pour exécuter tous les scripts en même temps :

    python launcher.py

> Attention : `launcher.py` ouvrira autant de terminaux dans de nouveaux processus qu'il y a de scripts dans le dossier `/scripts` !
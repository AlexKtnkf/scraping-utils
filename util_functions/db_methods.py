from datetime import datetime
from pymongo import MongoClient
import sys

# fonction permettant d'ajouter un document à une collection MongoDB locale
def mongo_local_push(extracted_json, host_address, host_port, database_name, collection_name):
    try:
        client = MongoClient(host_address, host_port, serverSelectionTimeoutMS=3)
        db = client[database_name]
        collection = db[collection_name]
        collection.insert_one(extracted_json)
        client.close()
        print(sys.argv[0] + ' ' + datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + ' - enregistrement Mongo effectué')
    except Exception as err:
        print(err)


# même fonction mais pour une MongoDB sur le cloud
def mongo_cloud_push(extracted_json, mongo_uri, database_name, collection_name):
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        collection.insert_one(extracted_json)
        client.close()
        print(sys.argv[0] + ' ' + datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + ' - enregistrement Mongo effectué')
    except Exception as err:
        print(err)

# fonction pour vérifier la présence de valeurs dans une collection
# renseigner soit le paramètre mongo_uri, soit host_address et host_port et éventuellement userlogin et userpass
# exemple :
# print(mongo_check_from_coll({'cod':"200"}, 'localhost', 27017, 'bclue_datalake', 'weather_predictions'))
def mongo_check_from_coll(query, database_name, collection_name, mongo_uri=None, host_address=None, host_port=None, user_login=None, user_pass=None ):
    items_found = {}
    try:
        if mongo_uri is not None:
            client = MongoClient(mongo_uri)
        else:
            client = MongoClient(host_address, host_port)
        db = client[database_name]
        if user_login is not None and user_pass is not None:
            db.authenticate(name=user_login, password=user_pass)
        collection = db[collection_name]
        items_found = collection.find(query)
        client.close()
    except Exception as err:
        print(err)
    return items_found



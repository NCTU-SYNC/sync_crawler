# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
import pymongo
import datetime
import hashlib

headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

def get_page(url):

    """Returns a BeautifulSoup object with a given url

    Argument type: string
    """
    r = requests.get(url, headers = headers)#get HTML
    r.encoding='UTF-8'
    soup = BeautifulSoup(r.text,"html.parser")
    return soup

def generate_hash(data):
    
    """Returns a SHA1 hash of the given data string

    """
    result = hashlib.sha1(data.encode('utf-8'))
    return result.hexdigest()

def log_info(msg):
    now = datetime.datetime.now()
    print("[{0}][INFO] {1}".format(now.strftime("%Y-%m-%d %H:%M:%S"),msg))

def get_db_instance(database,collection,mongodb_uri='mongodb://localhost:27017/'):
    """Returns a collection from the given database and mongoDB.

    Arguments:
        database: type string
        collection: type string
        mongodb_uri: type string, sample format: mongodb://localhost:27017/
    """
    if(database=="None"):
        print("database: none")
        return None
    print(database,"ttt")
    print("database: hit  "+mongodb_uri)
    client = MongoClient(mongodb_uri)
    db = client[database]
    return db[collection]

def update_dbs(collection_local,collection_main,collection_dev_main,news_dict):
    """Update both the local database and main database with news_dict.

    Arguments:
    collection_local - local database
    collection_main - sync main database
    news_dict - document

    Procedures:
    1. First check whether there exists a document with the same url hash.
    2. If yes, check whether content is modified, update both dbs if modified, otherwise do nothing.
    3. Otherwise, insert new document into local db, update main db with upsert.
    """
    find = collection_local.find_one( {'url_hash': news_dict['url_hash']} )
    if find:
        if find['content_hash'] != news_dict['content_hash']:
            collection_local.update_one({'_id': find['_id']},{'$set':news_dict})
            if collection_main!=None:
                collection_main.update_one({'url_hash': news_dict['url_hash']},{'$set':news_dict})
            if collection_dev_main!=None:
                collection_dev_main.update_one({'url_hash': news_dict['url_hash']},{'$set':news_dict})
    else:
        collection_local.insert_one(news_dict)
        del news_dict['_id']
        print(collection_main)
        print("hello")
        if collection_main!=None:
            print("any?")
            collection_main.replace_one({'url_hash': news_dict['url_hash']},news_dict,upsert=True)
        if collection_dev_main!=None:
            collection_dev_main.replace_one({'url_hash': news_dict['url_hash']},news_dict,upsert=True)

def convert_to_utc(date_object):
    """ Convert a naive datetime object to aware datetime object with timezone = utc """
    tz = timezone(timedelta(hours=+8))
    new_date = date_object.replace(tzinfo = tz)
    new_date = new_date.astimezone(tz)
    utc_time = new_date.astimezone(timezone.utc)
    return utc_time

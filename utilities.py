# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
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

def db_init(database,media):
    """Returns a MongoClient collection instance depending on the media.
    
    Argument type: string
    """
    #db initialization
    client = MongoClient()
    db = client[database]
    return db[media]

def db_update(collection,news_dict):
    """Updates the database with news_dict.

    The function is described as follows:
    1. First check whether there exists a document with the same url hash.
    2. If yes, check whether content is modified, update if modified, otherwise do nothing.
    3. Otherwise, insert new document.
    """
    find = collection.find_one( {'url_hash': news_dict['url_hash']} )
    if find:
        if find['content_hash'] != news_dict['content_hash']:
            log_info('{0}: data updated, link: {1}'.format(news_dict['media'],news_dict['url']))
            collection.update_one({'_id': find['_id']},{'$set':news_dict})
        # collection.update_one({'url_hash': news_dict['url_hash'],
        #     'content_hash':{'$ne':news_dict['content_hash']}},
        #     {'$set':news_dict})
    else:
        collection.insert_one(news_dict)

def dbs_update(collection,collection_main,news_dict):
    """Update both the local database and main database with news_dict.

    Arguments:
    collection - local database
    collection_main - sync main database
    news_dict - document

    Procedures:
    1. First check whether there exists a document with the same url hash.
    2. If yes, check whether content is modified, update both dbs if modified, otherwise do nothing.
    3. Otherwise, insert new document into local db, update main db with upsert.
    """
    find = collection.find_one( {'url_hash': news_dict['url_hash']} )
    if find:
        if find['content_hash'] != news_dict['content_hash']:
            log_info('{0}: data updated, link: {1}'.format(news_dict['media'],news_dict['url']))
            collection.update_one({'_id': find['_id']},{'$set':news_dict})
            collection_main.update_one({'url_hash': news_dict['url_hash']},{'$set':news_dict})
    else:
        collection.insert_one(news_dict)
        del news_dict['_id']
        collection_main.replace_one({'url_hash': news_dict['url_hash']},news_dict,upsert=True)

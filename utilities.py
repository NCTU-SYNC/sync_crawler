# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import hashlib

headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

def get_page(url):

    """Returns a BeautifulSoup object with a given url

    Parameter type: string
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

def db_init(media):
    """Returns a MongoClient collection instance depending on the media.
    
    Parameter type: string
    """
    #db initialization
    client = MongoClient()
    db = client.sync
    if media == '中央社':
        return db.cna
    elif media == '中時':
        return db.chinatimes
    elif media == '華視':
        return db.cts
    elif media == '東森':
        return db.ebc
    elif media == 'ettoday':
        return db.ettoday
    elif media == '台灣事實查核中心':
        return db.factcheckcenter
    elif media == '自由時報':
        return db.ltn
    elif media == '風傳媒':
        return db.storm
    elif media == '聯合':
        return db.udn
    else:
        return db.other

def db_update(collection,news_dict):
    """Updates the database with news_dict.

    The function is described as follows:
    1. First check whether there exists a document with the same url hash.
    2. If yes, check whether content is modified, update if modified, otherwise do nothing.
    3. Otherwise, insert new document.
    """
    find = collection.find_one( {'url_hash': news_dict['url_hash']} )
    if find:
        collection.update_one({'url_hash': news_dict['url_hash'],
            'content_hash':{'$ne':news_dict['content_hash']}},
            {'$set':news_dict})
    else:
        collection.insert_one(news_dict)
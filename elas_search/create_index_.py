from pymongo import MongoClient
from configparser import ConfigParser
from elasticsearch import Elasticsearch

database_config = ConfigParser(interpolation=None)
database_config.read('..\database_config.ini')

username = database_config['elastic']['username']
secret   = database_config['elastic']['secret']
local_secret = database_config['elastic']['local_secret']

es = Elasticsearch(f"http://{username}:{local_secret}@localhost:9200")
# es = Elasticsearch(f"https://{username}:{secret}@212b-140-113-214-146.jp.ngrok.io")

MONGODB_URI = database_config['cache']['uri']

LOCAL_DATABASE    = database_config['cache']['db']
LOCAL_COLLECTION  = database_config['cache']['collection']


MAIN_DATABASE     = database_config['main']['db']
MAIN_COLLECTION   = database_config['main']['collection']
# DEV_MAIN_DATABASE = database_config['dev-main']['db']
# DEV_MAIN_COLLECTION   = database_config['dev-main']['collection']

def index_DB_data(_db_uri,_db,_col,offset,limitNum,index,doc_type):
    client = MongoClient(_db_uri)
    db  = client[_db]
    col = db[_col]
    Newses=col.find().skip(offset).limit(limitNum)

    for news in Newses:
        print(news['title'],type(news['_id']),news['_id'])
        doc = {
            'title'  : news['title'],
            'content': news['content']
        }
        es.index(index=index,doc_type=doc_type,id=news['_id'],body=doc)



# index_DB_data(MONGODB_URI,LOCAL_DATABASE,LOCAL_COLLECTION,0,15,"cache","cacheType")  #345
index_DB_data(MONGODB_URI,MAIN_DATABASE,MAIN_COLLECTION ,0,100000,"main","mainType")    #1000,000
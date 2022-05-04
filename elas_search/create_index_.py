from pymongo import MongoClient
from configparser import ConfigParser
from elasticsearch import Elasticsearch

database_config = ConfigParser(interpolation=None)
database_config.read('..\database_config.ini')

MONGODB_URI_LOCAL = database_config['cache']['uri']
LOCAL_DATABASE    = database_config['cache']['db']
LOCAL_COLLECTION  = database_config['cache']['collection']

username = database_config['elastic']['username']
secret   = database_config['elastic']['secret']
es = Elasticsearch(
    ['https://localhost:9200/'],
    basic_auth=(username,secret),
)



# MONGODB_URI_MAIN  = database_config['main']['uri']
# MAIN_DATABASE     = database_config['main']['db']
# MAIN_COLLECTION   = database_config['main']['collection']
# DEV_MAIN_DATABASE = database_config['dev-main']['db']
# DEV_MAIN_COLLECTION   = database_config['dev-main']['collection']
client = MongoClient(MONGODB_URI_LOCAL)
db  = client[LOCAL_DATABASE]
col = db[LOCAL_COLLECTION]

offset = 0
limitNum  = 15
Newses=col.find().skip(offset).limit(limitNum)



for news in Newses:
    print(news['title'],type(news['_id']),news['_id'])
    doc = {
        'title'  : news['title'],
        'content': news['content']
    }
    es.index(index="news",id=news['_id'],document=doc)
# es.indices.refresh(index="news")   
# resp = es.get(index="news", id=1)
# print(resp['_source'])



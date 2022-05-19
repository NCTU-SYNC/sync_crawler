from configparser import ConfigParser
from elasticsearch import Elasticsearch

database_config = ConfigParser(interpolation=None)
database_config.read('..\database_config.ini')

username = database_config['elastic']['username']
secret   = database_config['elastic']['secret']
local_secret = database_config['elastic']['local_secret']

es = Elasticsearch(f"http://{username}:{local_secret}@localhost:9200")
# es = Elasticsearch(f"https://{username}:{secret}@212b-140-113-214-146.jp.ngrok.io")


body={
    "from":0,
    "size":10000,   #可以試試看10001
    "query": {
        "match": {
            "content":"酷喔"   #doc_type  #能源 電動車 
        }
    }
}
resp = es.search(index="main", body=body)
# print(resp)
print(f"Got {resp['hits']['total']['value']} Hits:")
limit=5
for index,hit in enumerate(resp['hits']['hits']):
    if limit == index:
        break
    print(hit["_source"]["title"])
    print((hit["_score"]))
    # print(hit["_source"]["content"],end="\n\n")




    
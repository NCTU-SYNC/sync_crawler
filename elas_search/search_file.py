from configparser import ConfigParser
from elasticsearch import Elasticsearch

database_config = ConfigParser(interpolation=None)
database_config.read('..\database_config.ini')

username = database_config['elastic']['username']
secret   = database_config['elastic']['secret']
local_secret = database_config['elastic']['local_secret']

es = Elasticsearch(f"http://{username}:{local_secret}@localhost:9200")
# es = Elasticsearch(f"https://{username}:{secret}@212b-140-113-214-146.jp.ngrok.io")

es.indices.put_settings(index = "main",
   body = {
      "index": {
         "max_result_window": 500000     #設定 一個node之中  一次搜索 的最大數量 預設 10000
      }
   })

body={
    # "from":0,
    # "size":100001,   
    "query": {
        "match_all": {
            # "content":"酷喔"  
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




    
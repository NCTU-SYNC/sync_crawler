from elasticsearch import Elasticsearch

# Elastic search configuation
es = Elasticsearch("http://localhost:9200")

# es.indices.refresh(index="news")
query={
    "match_all": {}
}
resp = es.search(index="news", query=query)
limit=100
for index,hit in enumerate(resp['hits']['hits']):
    if limit == index:
        break
    print(hit["_source"]["title"])
    print((hit["_score"]))
    print(hit["_source"]["content"],end="\n\n")





query = {
    "match": {
        "content":"能源 電動車 "
    }
}

resp = es.search(index="news", query=query)
# print(resp)
print(f"Got {resp['hits']['total']['value']} Hits:")
limit=5
for index,hit in enumerate(resp['hits']['hits']):
    if limit == index:
        break
    print(hit["_source"]["title"])
    print((hit["_score"]))
    print(hit["_source"]["content"],end="\n\n")
    
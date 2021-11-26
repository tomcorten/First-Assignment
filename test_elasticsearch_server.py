import requests
import json
from elasticsearch import Elasticsearch

def search(query):
    e = Elasticsearch()
    p = { "query" : { "query_string" : { "query" : query }}}

    response = e.search(index="wikidata_en",  body=json.dumps(p),  request_timeout=30, size = 30)
    

    id_labels = {}
    if response:
        for hit in response['hits']['hits']:
                source = hit['_source']
                if ('schema_name' in source):
                    label = source['schema_name']
                elif ('schema_description' in source):
                    label = source['schema_description']
                else:
                    continue
                id = hit['_id']
                id_labels.setdefault(id, set()).add(label)
    return id_labels

if __name__ == '__main__':
    import sys
    try:
        _, QUERY = sys.argv
    except Exception as e:
        QUERY = 'Vrije Universiteit Amsterdam'

    for entity, labels in search(QUERY).items():
        print(entity, labels)

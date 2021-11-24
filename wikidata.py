import json

import trident
KBPATH='assets/wikidata-20200203-truthy-uri-tridentdb'

def trident_search(entity):
    db = trident.Db(KBPATH)
    id_of_test = db.lookup_id(entity)
    object_from_subject = db.o_aggr_froms(id_of_test)
    object_from_subject_text = [db.lookup_str(i) for i in object_from_subject]
    return (len(object_from_subject_text))

from elasticsearch import Elasticsearch

def elastic_search(query, n=20):
    e = Elasticsearch()
    p = { "query" : { "query_string" : { "query" : query }}}
    response = e.search(index="wikidata_en", body=json.dumps(p), size=n)
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
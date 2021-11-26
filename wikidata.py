import json

import trident
KBPATH='assets/wikidata-20200203-truthy-uri-tridentdb'

from elasticsearch import Elasticsearch

import threading 

lock = threading.Lock()

class TridentHandler:
    def __init__(self, db):
        self._terms = {}
        self._db = db

    def lookup(self, term):
        if term not in self._terms:
            self._terms[term] = self._db.lookup_id(term)
        return self._terms[term]
    
    def o_aggr_froms(self, term):
        return self._db.o_aggr_froms(self.lookup(term))

db = trident.Db(KBPATH)
handler = TridentHandler(db)

def trident_search(entity):
    lock.acquire()
    
    object_from_subject = handler.o_aggr_froms(entity)
    object_from_subject_text = [handler._db.lookup_str(i) for i in object_from_subject]
    yield (len(object_from_subject_text))
    
    lock.release()



def elastic_search(query, n=20):
    e = Elasticsearch()
    p = { "query" : { "query_string" : { "query" : query }}}
    response = e.search(index="wikidata_en", body=json.dumps(p), size=n, request_timeout=30)
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
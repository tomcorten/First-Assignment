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


def get_amount_objects(entity):
    lock.acquire()
    
    object_from_subject = handler.o_aggr_froms(entity)
    object_from_subject_text = [handler._db.lookup_str(i) for i in object_from_subject]
    yield (len(object_from_subject_text))
    
    lock.release()

    

def check_candidate(named_entity, entity_page ,overlap_dict):

    entity_predicates = get_predicates_from_subject(entity_page)
    if (overlap_dict[named_entity[0]]).issubset(set(entity_predicates)):
        return entity_page
   

def elastic_search(query, n=20):
    e = Elasticsearch()
    p = { "query" : { "query_string" : { "query" : query }}}
    response = e.search(index="wikidata_en", body=json.dumps(p), size=n, request_timeout = 30)
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


def get_predicates_from_subject(subject):

    entitie_pos = db.po(db.lookup_id(subject))
    predicates = ([po[0] for po in entitie_pos])

    return predicates


def get_predicates_overlap(entities):

    #define list which holds predicates for each entity
    p_list = []
    #get all predicates
    for entity in entities:
        predicates = get_predicates_from_subject(entity)
        p_list.append(predicates)
    overlap = (set.intersection(*map(set, p_list)))

    return (overlap)


def ne_based_model(candidate, random_overlap):

    #get po's from candidate
    id_of_test = db.lookup_id(candidate)
    contents_of_subject = db.po(id_of_test)
    #check whether predicates of the overlap of five persons is in candidate predicates
    predicates_of_candidate = [po[0] for po in contents_of_subject]
    if random_overlap.issubset(set(predicates_of_candidate)):
        print('CHECK')
    else:
        print('NO')


def get_random_entities(predicate,label):

    query="""PREFIX wde: <http://www.wikidata.org/entity/> \
        PREFIX wdp: <http://www.wikidata.org/prop/direct/> \
        PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> \
        select ?s where { ?s wdp:""" + predicate + """ wde:""" + label + """ . } 
        OFFSET 210 #random number variable
        LIMIT 10
    """

    #get query of n random entities
    persons = db.sparql(query)
    #results = db.sparql(query)
    json_results = json.loads(persons)
    variables = json_results["head"]["vars"]

    entity_list = []
    results = json_results["results"]
    for b in results["bindings"]:
        for var in variables:
            entity_list.append("<"+ b[var]["value"] + ">")
    return entity_list

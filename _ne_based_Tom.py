from bs4.element import ResultSet
import trident
import json
import re

KBPATH='assets/wikidata-20200203-truthy-uri-tridentdb'    
db = trident.Db(KBPATH)



def get_p_overlap(entities):

    #define list which holds predicates for each entity
    p_list = []
    #get all predicates
    for entity in entities:
        entitie_pos = db.po(db.lookup_id(entity))
        predicates = ([po[0] for po in entitie_pos])
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


def base_model(candidate):

    id_of_test = db.lookup_id(candidate)
    contents_of_subject = db.po(id_of_test)

    return (len(contents_of_subject))


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

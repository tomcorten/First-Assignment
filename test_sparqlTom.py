import trident
import json

KBPATH='assets/wikidata-20200203-truthy-uri-tridentdb'

#Retrieve first 10 entities of type (P31) city (Q515)
query="""PREFIX wde: <http://www.wikidata.org/entity/> \
    PREFIX wdp: <http://www.wikidata.org/prop/direct/> \
    PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> \
    select ?s where { ?s wdp:P31 wde:Q5 . } LIMIT 10
    
   """
    
    
db = trident.Db(KBPATH)

def link_entity(candidate):

    term = candidate #should be the url of the entity e.g. "<http://www.wikidata.org/entity/Q15257>"
    term_id = db.lookup_id(term)
    object_from_subject = db.o_aggr_froms(term_id)
    object_from_subject_text = [db.lookup_str(i) for i in object_from_subject]
    if "<http://www.wikidata.org/entity/Q5>" in object_from_subject_text: #this is the entity page for HUMAN
        print("SUCCES")
        return True


def base_model(candidate):

    id_of_test = db.lookup_id(candidate)
    contents_of_subject = db.po(id_of_test)
    return (len(contents_of_subject))


# Load the KB
results = db.sparql(query)

json_results = json.loads(results)
print('KW', results)
print("*** VARIABLES ***")
variables = json_results["head"]["vars"]
print(variables)

print("\n*** BINDINGS ***")
results = json_results["results"]
for b in results["bindings"]:
    line = ""
    for var in variables:
        line += var + ": " + b[var]["value"] + " "
    print(line)

print("\n*** STATISTICS ***")
print(json_results['stats'])



class TridentHandler:
    def __init__(self, db):
        self._terms = {}
        self._db = db

    def lookup(self, term):
        if term not in self._terms:
            self._terms[term] = db.search_id(term)
        return self._terms[term]
    
    def contents_of_subject(self, term):
        return self._db.po(self.lookup(term[0]))

    def indegree_of_subject(self, term):
        return self._db.indegree(self.lookup(term[0]))

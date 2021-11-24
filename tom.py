import gzip
from os import link
import re
from typing import Text
from bs4 import BeautifulSoup
from test_elasticsearch_server import search
from test_sparqlTom import base_model
from pprint import pprint

import spacy 
nlp = spacy.load("en_core_web_sm")

#from flair.data import Sentence
#from flair.models import SequenceTagger
#tagger = SequenceTagger.load('ner')

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

KEYNAME = "WARC-TREC-ID"



def clean(data):
    soup = BeautifulSoup(data, 'html.parser')
    clean = ""

    # Loop through every p tag within the payload  
    for paragraph in soup.find_all("p"):
    # Remove any left over HTML tags
        stripped = re.sub('<[^>]*>', '', str(paragraph))
            
        # Number of \n tags in the stripped string
        nLength = len(stripped.split('\n'))
                
        # The length of the string
        strLength = len(stripped)

        # If the string has a length of more than 100
        # and contains less than 3 \n tags, 
        # add it to the final result
        # if strLength > 100 and nLength < 3:
        clean += stripped + '\n'
    return clean.replace('\n', ' ')   


def get_entities_nltk(cleaned):   
    for sent in nltk.sent_tokenize(cleaned):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                return (chunk.label(), ' '.join(c[0] for c in chunk)) 

def get_entities_spacy(cleaned):
    doc = nlp(cleaned)
    text_results = ([(X.label_, X.text) for X in doc.ents])
    for word in text_results:
        return word

def get_entities_flair(cleaned):
    
    sentence = Sentence(cleaned)
    # run NER over sentence
    tagger.predict(sentence)
    # iterate over entities and print
    # iterate over entities and print
    for entity in sentence.get_spans('ner'):
        pass
        # print(entity)

# The goal of this function process the webpage and returns a list of labels -> entity ID
def find_labels(payload):
    if payload == '':
        return

    # The variable payload contains the source code of a webpage and some additional meta-data.
    # We firt retrieve the ID of the webpage, which is indicated in a line that starts with KEYNAME.
    # The ID is contained in the variable 'key'
    key = None
    for line in payload.splitlines():
        if line.startswith(KEYNAME):
            key = line.split(': ')[1]
            break
        
    # Problem 1: The webpage is typically encoded in HTML format.
    # We should get rid of the HTML tags and retrieve the text. How can we do it?

    cleaned = clean(payload)
    # Problem 2: Let's assume that we found a way to retrieve the text from a webpage. How can we recognize the
    # entities in the text?
    
    #print(cleaned)
    if (cleaned!=''):
        chunk = get_entities_spacy(cleaned)

        if chunk == None:
            return
        elif chunk[0] == 'ORDINAL':
            return
        elif chunk[0] == 'CARDINAL':
            return
        elif chunk[0] == 'TIME':
            return
        elif chunk[0] == 'DATE':
            return
        elif chunk[0] == 'MONEY':
            return

        # Problem 3: We now have to disambiguate the entities in the text. For instance, let's assugme that we identified
        # the entity "Michael Jordan". Which entity in Wikidata is the one that is referred to in the text?

        QUERY = chunk[1]
        po_dict = {}
        try:
            for entity, labels in search(QUERY).items():
                candidate_pos = (base_model(entity))
                po_dict[entity] = candidate_pos
            if po_dict:
                max_key = max(po_dict, key=po_dict.get)
                if (max_key):
                    yield key, QUERY, max_key
        except:
            return


    # To tackle this problem, you have access to two tools that can be useful. The first is a SPARQL engine (Trident)
    # with a local copy of Wikidata. The file "test_sparql.py" shows how you can execute SPARQL queries to retrieve
    # valuable knowledge. Please be aware that a SPARQL engine is not the best tool in case you want to lookup for
    # some strings. For this task, you can use elasticsearch, which is also installed in the docker image.
    # The file start_elasticsearch_server.sh will start the elasticsearch server while the file
    # test_elasticsearch_server.py shows how you can query the engine.

    # A simple implementation would be to first query elasticsearch to retrieve all the entities with a label
    # that is similar to the text found in the web page. Then, you can access the SPARQL engine to retrieve valuable
    # knowledge that can help you to disambiguate the entity. For instance, if you know that the webpage refers to persons
    # then you can query the knowledge base to filter out all the entities that are not persons...

    # Obviously, more sophisticated implementations that the one suggested above are more than welcome :-)


    # For now, we are cheating. We are going to returthe labels that we stored in sample-labels-cheat.txt
    # Instead of doing that, you should process the text to identify the entities. Your implementation should return
    # the discovered disambiguated entities with the same format so that I can check the performance of your program.
    # cheats = dict((line.split('\t', 2) for line in open('data/sample-labels-cheat.txt').read().splitlines()))
    # for label, wikidata_id in cheats.items():
    #     if key and (label in payload):
    #         yield key, label, wikidata_id


def split_records(stream):
    payload = ''
    for line in stream:
        if line.strip() == "WARC/1.0":
            yield payload
            payload = ''
        else:
            payload += line
    yield payload

if __name__ == '__main__':
    import sys
    try:
        _, INPUT = sys.argv
    except Exception as e:
        print('Usage: python starter-code.py INPUT')
        sys.exit(0)

    with gzip.open(INPUT, 'rt', errors='ignore') as fo:
        for record in split_records(fo):
            for key, label, wikidata_id in find_labels(record):
                print(key + '\t' + label + '\t' + wikidata_id)


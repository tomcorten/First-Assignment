import gzip
import re

import threading

from bs4 import BeautifulSoup

from ner import get_entities_nltk, get_entities_spacy, get_entities_stanza
from wikidata import trident_search, elastic_search

KEYNAME = "WARC-TREC-ID"

def clean(data):
    soup = BeautifulSoup(data, 'html.parser')
    clean = ""

      
    options = [
            "h1",
            # "h2",
            # "h3",
            # "h4",
            "p",
            # "a",
        ]

    # Loop through every p tag within the payload  
    for paragraph in soup.find_all(options):
    # Remove any left over HTML tags
        stripped = re.sub('<[^>]*>', '', str(paragraph))
            
        # Number of \n tags in the stripped string
        nLength = len(stripped.split('\n'))
                
        # The length of the string
        strLength = len(stripped)

        # If the string has a length of more than 100
        # and contains less than 3 \n tags, 
        # add it to the final result
        if strLength > 50 and nLength < 4:
            clean += stripped + '\n'

    return clean.replace('\n', ' ')   

def find_labels(payload):
    if payload == '':
        return

    key = None
    for line in payload.splitlines():
        if line.startswith(KEYNAME):
            key = line.split(': ')[1]
            break


    cleaned = clean(payload)

    if (cleaned!=''):
        for chunk in get_entities_spacy(cleaned):
            if chunk == None:
                continue
            elif chunk[0] == 'ORDINAL':
                continue
            elif chunk[0] == 'CARDINAL':
                continue
            elif chunk[0] == 'TIME':
                continue
            elif chunk[0] == 'DATE':
                continue
            elif chunk[0] == 'MONEY':
                continue

            QUERY = chunk[1]
            po_dict = {}
            try:
                for entity, labels in elastic_search(QUERY).items():
                    candidate_pos = (trident_search(entity))
                    po_dict[entity] = candidate_pos
                if po_dict:
                    max_key = max(po_dict, key=po_dict.get)
                    if (max_key):
                        yield key, QUERY, max_key
            except:
                continue


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

    threads = []
    with gzip.open(INPUT, 'rt', errors='ignore') as fo:
        for record in split_records(fo):
            def find():
                for key, label, wikidata_id in find_labels(record):
                    print(key + '\t' + label + '\t' + wikidata_id)
            threads.append(threading.Thread(target=find))
            threads[len(threads) - 1].start()
    
    l = threading.Lock()
    l.acquire()
    l.acquire()
import gzip
import re

import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

from bs4 import BeautifulSoup

from test_elasticsearch_server import search

import trident
KBPATH='assets/wikidata-20200203-truthy-uri-tridentdb'


# import flair
# from flair.data import Sentence
# from flair.models import SequenceTagger


KEYNAME = "WARC-TREC-ID"

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
    def clean(data):
    
        soup = BeautifulSoup(data, 'html.parser')
        clean = ""

        # Loop through every p tag within the payload  
        for paragraph in soup.find_all('p'):
            # Remove any left over HTML tags
            stripped = re.sub('<[^>]*>', '', str(paragraph))
            
            # Number of \n tags in the stripped string
            nLength = len(stripped.split('\n'))
            
            # The length of the string
            strLength = len(stripped)

            # If the string has a length of more then 100
            # and contains less than 3 \n tags, 
            # add it to the final result
            if strLength > 100 and nLength < 3:
                clean += stripped + '\n'

        return clean.replace('\n', '')   
    # The resulting string
    # print(clean)

    # Problem 2: Let's assume that we found a way to retrieve the text from a webpage. How can we recognize the
    # entities in the text?

    def get_entities_nltk(cleaned):   

        if(cleaned != ""):
            
            # Loop through tokenised version of the data
            for sent in nltk.sent_tokenize(cleaned):
                # Apply POS tagging to sentenice and loop through
                for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                    # Maybwe we can do something here?
                    if hasattr(chunk, 'label'):
                        return (chunk.label(), ' '.join(c[0] for c in chunk))

    cleaned = clean(payload)

    chunks = get_entities_nltk(cleaned)
    


    
    # Problem 3: We now have to disambiguate the entities in the text. For instance, let's assugme that we identified
    # the entity "Michael Jordan". Which entity in Wikidata is the one that is referred to in the text?
    
    
    if chunks is not None:
        
        QUERY = chunks[1]
        items = search(QUERY).items()
        
        # something something sparql

        for entity, labels in items:
            
            if key and (chunks[1] in payload):
                print(key, chunks[1], entity)
                yield key, chunks[1], entity

        # "For instance, if you know that the webpage refers to persons
        # then you can query the knowledge base to filter out all the entities that are not persons..."
        

        db = trident.Db(KBPATH)    
        query = """
            PREFIX wde: <http://www.wikidata.org/entity/Q12621138>
            PREFIX 
        """

        results = db.sparql(query)

        
    

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
    # cheats = dict((line.split('\t', 2) for line in open(
    #     'data/sample-labels-cheat.txt').read().splitlines()))
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
                # print(key + '\t' + label + '\t' + wikidata_id)
                pass

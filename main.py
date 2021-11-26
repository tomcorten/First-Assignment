# Dependencies
import gzip
import re
import threading

# Modules
from clean import clean

# NER Approaches
from ner_spacy import get_entities_spacy
# Other attempted approaches
# from ner_nltk import get_entities_nltk
# from ner_stanza import get_entities_stanza

from wikidata import trident_search, elastic_search

KEYNAME = "WARC-TREC-ID"

def find_labels(payload):
    """
    Find labels function processes and returns the payload by:

    1. Cleans a HTML payload into raw text
    2. Recognizes entities within the sentences 
        and returns them as chunks
    3. Runs the chunks through ElasticSeach and Trident to refine results

    @param: payload: A Literal of HTML files

    @returns A list of predictions
    """

    result = []
    if payload == '':
        return result

    key = None
    for line in payload.splitlines():
        if line.startswith(KEYNAME):
            key = line.split(': ')[1]
            break


    # Get the cleaned text from the payload
    cleaned = clean(payload)

    if (cleaned!=''):

        # Loop through each named entitiy chunk
        for chunk in get_entities_spacy(cleaned):
            
            # If the chunk is empty continue
            if chunk == None:
                continue
            
            # Set the query to be the label of the chunk
            QUERY = chunk[1]
            po_dict = {}

            try:
                # Run the query through elastic search
                for entity, labels in elastic_search(QUERY).items():
                    # Ignore labels that are only numbers and special characters
                    label = next(iter(labels))
                    
                    if label.isdigit(): 
                        #or bool(re.search('&|%|;', label)):
                        continue
                
                    # Run the resulting entity through trident
                    # and return the candidate pos
                    for candidate_pos in trident_search(entity):
                        # set the candidate pos in the po dictionary
                        po_dict[entity] = candidate_pos

                if po_dict:
                    # Check if the po_dict has the max key for a current chunk
                    max_key = max(po_dict, key=po_dict.get)
                    if (max_key):
                        # And if so, append to the result
                        result.append([key, QUERY, max_key])
            
            # Catch connection errors from elastic search
            except ConnectionError as e:
                print("Error connecting to elastic search")
                raise e
            # Any other errors e.g. invalid words we can just continue the loop
            except Exception as e:
                print(key, e)
                continue
    return result


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

    filename = "sample_predictions.tsv"
    open(filename, 'w').close()

    threads = []
    with gzip.open(INPUT, 'rt', errors='ignore') as fo:
        for record in split_records(fo):
            # def find():
            results = []
            for result in find_labels(record):
                key = result[0]
                label = result[1]
                wikidata_id = result[2]

                print(key + '\t' + label + '\t' + wikidata_id)
                results.append([key, label, wikidata_id])
                
            # Write to the sample predctions file
            # (Just so we can add to the file and see print statements at the same time)
            file = open(filename, "a")  
            file.write("".join([result[0] + '\t' + result[1] + '\t' + result[2] + '\n' for result in results]))
            file.close()
            
            # threads.append(threading.Thread(target=find))
            # threads[len(threads) - 1].start()
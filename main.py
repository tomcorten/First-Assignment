# Dependencies
import gzip
import threading

# Modules
from clean import clean
from ner import get_entities_nltk, get_entities_spacy, get_entities_stanza
from wikidata import trident_search, elastic_search

KEYNAME = "WARC-TREC-ID"

def find_labels(payload):
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
            
            QUERY = chunk[1]
            po_dict = {}
            try:
                for entity, labels in elastic_search(QUERY).items():
                    candidate_pos = (trident_search(entity))
                    po_dict[entity] = candidate_pos
                if po_dict:
                    max_key = max(po_dict, key=po_dict.get)
                    if (max_key):
                        result.append([key, QUERY, max_key])
            # Catch connection errors from elastic search
            except ConnectionError as e:
                print("Error connecting to elastic search")
                raise e
            # Any other errors continue
            except:
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
            def find():
                results = []
                for result in find_labels(record):
                    key = result[0]
                    label = result[1]
                    wikidata_id = result[2]

                    print(key + '\t' + label + '\t' + wikidata_id)
                    results.append([key, label, wikidata_id])
                    
                file = open(filename, "a")  
                file.write("".join([result[0] + '\t' + result[1] + '\t' + result[2] + '\n' for result in results]))
                file.close()

            threads.append(threading.Thread(target=find))
            threads[len(threads) - 1].start()
# Dependencies
import gzip
import threading

# Modules
from clean import clean
from ner_nltk import get_entities_nltk, get_entities_spacy, get_entities_stanza
from wikidata import get_amount_objects, elastic_search, get_random_entities, get_predicates_overlap, check_candidate

KEYNAME = "WARC-TREC-ID"

# PERS = get_random_entities('P31' ,'Q5') # get 20 random instances of Q5: human
# LOC = get_random_entities('P31','Q486972') # get 20 random instances of Q486972: human settlement
# ORG = get_random_entities('P31','Q6881511') # get 20 random instances of Q6881511: enterprise

# pers_overlap = get_predicates_overlap(PERS)
# org_overlap = get_predicates_overlap(ORG)
# loc_overlap = get_predicates_overlap(LOC)

# overlap_dict = {'PERSON' : pers_overlap, 'ORG' : org_overlap, 'GPE' : loc_overlap}

LABEL_DICT = {}

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
                    # Ignore labels that are only numbers and special characters
                    label = next(iter(labels))
                    
                    if label.isdigit() or "&" in label: 
                        continue

                    # Attempted predicates overlap, not finished on time
                    # if chunk[0] in overlap_dict.keys():           
                    #         entity_page = check_candidate(chunk, entity ,overlap_dict)
                    #         if entity_page:
                    #             result.append([key, QUERY, chunk[1]])

                    for candidate_pos in get_amount_objects(entity):
                        po_dict[entity] = candidate_pos
                if po_dict:
                    max_key = max(po_dict, key=po_dict.get)
                    if (max_key):
                        result.append([key, QUERY, max_key])

            # Catch connection errors from elastic search
            except ConnectionError as e:
                print("Error connecting to elastic search")
                raise e
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

    with gzip.open(INPUT, 'rt', errors='ignore') as fo:
        for record in split_records(fo):
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

            
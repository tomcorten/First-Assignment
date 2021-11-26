# Import Spacy
import spacy 
spacy_nlp = spacy.load("en_core_web_sm")

def get_entities_spacy(cleaned):
    """
    Runs NER on the provided text using spacy

    @param cleaned: A string of raw text

    @returns list[tuple] - resulted named entities in chunks
    """
    # Labels we are not interested in
    blacklist = ['ORDINAL', 'CARDINAL', 'TIME', 'DATE', 'MONEY']


    doc = spacy_nlp(cleaned)

    # return text results
    text_results = ([(X.label_, X.text) for X in doc.ents if X.label_ not in (blacklist)])
    return text_results
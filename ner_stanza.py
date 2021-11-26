# Import Stanz
import stanza
stanza.download('en', processors='tokenize,ner')

stanza_nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

def get_entities_stanza(cleaned):
    """
    Runs NER on the provided text using stanza

    @param cleaned: A string of raw text

    @returns list[tuple] - resulted named entities in chunks
    """

    doc = stanza_nlp(cleaned)
    text_results = ([(ent.type, ent.text) for sent in doc.sentences for ent in sent.ents])
    return text_results

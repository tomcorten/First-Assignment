import spacy 
spacy_nlp = spacy.load("en_core_web_sm")

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

import stanza
stanza.download('en', processors='tokenize,ner')
stanza_nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

def get_entities_nltk(cleaned):   
    for sent in nltk.sent_tokenize(cleaned):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                yield (chunk.label(), ' '.join(c[0] for c in chunk)) 

def get_entities_spacy(cleaned):
    doc = spacy_nlp(cleaned)
    text_results = ([(X.label_, X.text) for X in doc.ents])
    return text_results

def get_entities_stanza(cleaned):
    doc = stanza_nlp(cleaned)
    text_results = ([(ent.type, ent.text) for sent in doc.sentences for ent in sent.ents])
    return text_results
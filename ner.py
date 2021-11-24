import spacy 
nlp = spacy.load("en_core_web_sm")

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

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
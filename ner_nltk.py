# Import and download NLTK dependencies
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def get_entities_nltk(cleaned):
    """
    Runs NER on the provided text using NLTK

    @param cleaned: A string of raw text

    @returns list[tuple] - resulted named entities in chunks
    """

    # Build tokenized words using the sentenice tokenizer and word tokenizer
    tokenized_words = (
        nltk.word_tokenize(sent, preserve_line=True) for sent in nltk.sent_tokenize(cleaned)
    )
    print(tokenized_words)
    # Run POS tagging on tokenized words
    for sent in nltk.pos_tag_sents(tokenized_words):
        # Convert to bigrams for Multi-words
        for items in list(nltk.bigrams(sent)):
            # Convert items to chunks
            for chunk in nltk.ne_chunk(items):
                # Check if the chunk contains a label, and if so join and return
                if hasattr(chunk, 'label'):
                        yield (chunk.label(), ' '.join(c[0] for c in chunk)) 

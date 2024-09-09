# -------------------V1----------------------------------
import spacy
from transformers import pipeline

# Load spaCy's English model for entity extraction
nlp = spacy.load("en_core_web_sm")

# Use transformers for intent recognition
intent_recognition = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')

def process_text(text):
    # Entity Extraction using spaCy
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Intent Recognition using a transformer model
    intent = intent_recognition(text)

    return {
        "entities": entities,
        "intent": intent
    }



# -------------------V2----------------------------------



def preprocess_text(text):
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text.lower())

    cleaned_tokens = []

    for token in doc:
        if not token.is_stop and not token.is_punct:
            cleaned_tokens.append(token.lemma_)

    return " ".join(cleaned_tokens)
def extract_entities(text):
    doc = nlp(text)

    data = {
        "names": [],
        "orgs": [],
        "locations": []
    }

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            data["names"].append(ent.text)
        elif ent.label_ == "ORG":
            data["orgs"].append(ent.text)
        elif ent.label_ == "GPE":
            data["locations"].append(ent.text)

    return data
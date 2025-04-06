__package__ = "pras"



import spacy

nlp = spacy.load("en_core_web_trf")

def segment(text_file, target_file):
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()

    doc = nlp(text)

    with open(target_file, 'w', encoding='utf-8') as file:
        for sentence in doc.sents:
            file.write(sentence.text + '\n')


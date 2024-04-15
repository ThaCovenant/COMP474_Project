import csv

import spacy
from spacy import displacy
from tika import parser
import os

# rom spaCy fishing, DBpedia Spotlight
COURSE_MATERIALS = 'data/courseMaterial'
COURSE_MATERIALS_PLAIN_TEXT = 'plainText'

# load the language model
nlp = spacy.load("en_core_web_sm")

# named entities
named_entities = ['PERSON', 'ORG', 'GPE', 'PRODUCT', 'WORK_OF_ART', 'LANGUAGE', 'EVENT']


def get_file_path(directory, fileName):
    file_path = os.path.join(directory, fileName)
    return file_path


def to_plain_text(inPath):
    # go through dir for all content
    for course_material in os.listdir(inPath):
        course_path = inPath + "/" + course_material
        for course in os.listdir(course_path):
            course_content = course_path + "/" + course
            # print(course_content)
            for filename in os.listdir(course_content):
                file = course_content + "/" + filename
                # print(file)

                extractName = os.path.splitext(filename)[0]
                outPath = COURSE_MATERIALS_PLAIN_TEXT + "/" + course_path + "/" + course
                # print("outPath " + outPath)
                os.makedirs(outPath, exist_ok=True)
                newFile = outPath + "/" + extractName + ".txt"
                # print(newFile)

                # Check if the plaintext file already exists, if so, skip
                if os.path.exists(newFile):
                    print(f"Plaintext file already exists for {filename}. Skipping...")
                    continue

                parsed = parser.from_file(file)
                plainText = parsed['content']
                # print(plainText)

                with open(newFile, "w", encoding="utf-8") as f:
                    f.write(plainText)


def create_topic_triples(doc):
    pass


def link_entity(entity_text):
    # Link to DBpedia
    dbpedia_link = f"http://dbpedia.org/resource/{entity_text.replace(' ', '_')
    .replace('•', '').replace(',', '').replace('.', '').rstrip('_').lstrip('_')
    .lstrip('"').strip('\"')}"

    return dbpedia_link


def link_entities(doc):
    entity_links = []
    for ent in doc.ents:
        # Only link entities that are in named_entities
        if ent.label_ in named_entities:
            entity_link = link_entity(ent.text)
            if entity_link.startswith('http://dbpedia.org/resource/'):
                entity_links.append(entity_link)
                print(f"Link: {entity_link}")
    return entity_links


def process_plaintext(inPath):
    # for all text files inPath
    for root, dirs, files in os.walk(inPath):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # print(f"Plaintext file path {file_path}")
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                doc = nlp(text)
                link_entities(doc)


def process_single_plaintext(file_path):
    all_entity_links = set()
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
        doc = nlp(text)
        create_topic_triples(doc)
        entity_links = link_entities(doc)
        all_entity_links.update(entity_links)
        # visualize(doc)

    with open("entity_links.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Link"])
        for link in all_entity_links:
            # entity = link.split('/')[-1].replace('_', ' ')
            writer.writerow([link])


# Visualize all named entities
def visualize(doc):
    # displacy.serve(doc, style="ent")
    # To restrict the visualization to specific entity types, modify the options parameter
    options = {"ents": ["Chatbot", "API", "Notes"]}
    displacy.serve(doc, style="ent", options=options)


def main():
    # to_plain_text(COURSE_MATERIALS)
    # process_plaintext(COURSE_MATERIALS_PLAIN_TEXT)
    process_single_plaintext('plainText/data/courseMaterial/COMP474/Lectures/slides01.txt')


if __name__ == '__main__':
    main()
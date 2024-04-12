import spacy
from spacy import displacy
from spacy.language import Language
from tika import parser
import os

# rom spaCy fishing, DBpedia Spotlight
COURSE_MATERIALS = 'data/courseMaterial'
COURSE_MATERIALS_PLAIN_TEXT = 'plainText'

# load the language model
nlp = spacy.load("en_core_web_sm")


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


def link_entity(ent):
    print("Entity:", ent.text)


def create_topic_triples():
    print("link triples properly")


def link_entities(doc):
    for ent in doc.ents:
        link_entity(ent)
    pass


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
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
        doc = nlp(text)
        link_entities(doc)
        visualize(doc)


# Visualize all named entities
def visualize(doc):
    # displacy.serve(doc, style="ent")
    # To restrict the visualization to specific entity types, modify the options parameter
    options = {"ents": ["Chatbot", "API", "Notes"]}
    displacy.serve(doc, style="ent", options=options)


# # To restrict the visualization to specific entity types, modify the options parameter
# options = {"ents": ["ORG", "MONEY", "DATE"]}
# displacy.serve(doc, style="ent", options=options)


def main():
    to_plain_text(COURSE_MATERIALS)
    # process_plaintext(COURSE_MATERIALS_PLAIN_TEXT)
    process_single_plaintext('plainText/data/courseMaterial/COMP474/Lectures/slides01.txt')


if __name__ == '__main__':
    main()

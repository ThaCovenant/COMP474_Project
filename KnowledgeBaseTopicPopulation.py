import csv
import spacy
from rdflib import URIRef, RDF
from spacy import displacy
from tika import parser
import os

from AutomatedKnowledgeBaseConstruction import URIGenerator, create_graph
from Namespaces import namespaces, init_graph
file_path_topics_new = "Triples/topicsNew.ttl"

# rom spaCy fishing, DBpedia Spotlight
COURSE_MATERIALS = 'data/courseMaterial'
COURSE_MATERIALS_PLAIN_TEXT = 'plainText'

# load the language model
nlp = spacy.load("en_core_web_sm")

# named entities
named_entities = ["IBM", "Watson", "Alexa", "Microsoft", "Knowledge Graphs", "Eliza", "API", "Intelligent Systems",
                  "OWL", "SPARQL", "Deep Learning", "Neural Networks", "SAAS", "RAM", "GPT-3", "Graphs", "Functions",
                  "Relations", "Sets", "Union", "Transitive", "Chatbot", "Domain", "Range"]


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


def create_topic_triples(g, entity, link, courseName, filetype, i):
    # contentURI = URIRef(URIGenerator('COMP474', 'Lectures', 1))
    contentURI = URIRef(URIGenerator(courseName, filetype, i))
    topicURI = URIRef(namespaces['topic'] + entity)
    g.add((topicURI, RDF.type, namespaces['topic'].topic))
    g.add((topicURI, namespaces['topic'].topicProvenanceInformation, contentURI))
    g.add((topicURI, namespaces['topic'].DBpediaEntry, URIRef(link)))
    # print(g.serialize(format='turtle'))

    return g


def link_entity(entity_text):
    # Example: Link to DBpedia
    dbpedia_link = f"http://dbpedia.org/resource/{entity_text.replace(' ', '_')}"
    return dbpedia_link


def link_entities(doc):
    entity_links = []
    for ent in doc.ents:
        # Only link entities that are in named_entities
        # print(ent.text)
        if ent.text in named_entities:
            entity_link = link_entity(ent.text)
            if entity_link.startswith('http://dbpedia.org/resource/'):
                entity_links.append((ent.text.replace(' ', ''), entity_link))
                # print(f"Entity: {ent.text.replace(' ', '')}, Link: {entity_link}")
    return entity_links


def process_plaintext(inPath):
    # for all text files inPath
    g = init_graph()
    all_entity_links = set()
    for root, dirs, files in os.walk(inPath):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            print(f"Plaintext file path {file_path}")
            path_components = file_path.split("\\")
            # Extract course name and file type
            course_name = path_components[3]  # COMP335
            file_type = path_components[4]  # Assignments
            # print("Course Name:", course_name)
            # print("File Type:", file_type)
            file_number = ''
            for char in file_name:
                if char.isdigit():
                    file_number += char
            if file_number:
                counter = int(file_number)
            # print("Counter:", counter)

            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                doc = nlp(text)
                entity_links = link_entities(doc)
                all_entity_links.update(entity_links)

            with open("entity_links.csv", "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Entity", "Link"])
                for entity, link in all_entity_links:
                    # writer.writerow([entity, link])
                    g = g + create_topic_triples(g, entity, link, course_name, file_type, counter)

    return g

# def process_single_plaintext(file_path):
#     g = init_graph()
#     all_entity_links = set()
#     with open(file_path, "r", encoding="utf-8") as file:
#         text = file.read()
#         doc = nlp(text)
#         entity_links = link_entities(doc)
#         all_entity_links.update(entity_links)
#
#     with open("entity_links.csv", "w", newline="", encoding="utf-8") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(["Entity", "Link"])
#         for entity, link in all_entity_links:
#             # writer.writerow([entity, link])
#             g = g + create_topic_triples(g, entity, link)
#
#     return g


# def main():
#     # to_plain_text(COURSE_MATERIALS)
#     # g7 = process_plaintext(COURSE_MATERIALS_PLAIN_TEXT)
#     # process_single_plaintext('plainText/data/courseMaterial/COMP474/Lectures/slides01.txt')
#
#     # g7 = process_single_plaintext('plainText/data/courseMaterial/COMP474/Lectures/slides01.txt')
#     # create_graph(g7, file_path_topics_new)
#
#
# if __name__ == '__main__':
#     main()

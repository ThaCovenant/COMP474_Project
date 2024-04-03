import spacy
from spacy import displacy
from spacy.language import Language
from tika import parser
import os

# rom spaCy fishing, DBpedia Spotlight
file_path_courseMaterial_Comp335 = "data/courseMaterial/COMP335/Assignments"
file_path_courseMaterial_Comp335_out = "data/courseMaterial/COMP335/Assignments/Plaintext"


def toPlainText(inPath, outPath):
    # nlp = spacy.load("en_core_web_sm")
    # doc = nlp(
    #     """Superman was born on the planet Krypton and was given the name Kal-El at birth. As a baby, his parents sent him to Earth in a small spaceship moments before Krypton was destroyed in a natural cataclysm. His ship landed in the American countryside, near the fictional town of Smallville. He was found and adopted by farmers Jonathan and Martha Kent, who named him Clark Kent. Clark developed various superhuman abilities, such as incredible strength and impervious skin. His adoptive parents advised him to use his abilities for the benefit of humanity, and he decided to fight crime as a vigilante. To protect his privacy, he changes into a colorful costume and uses the alias "Superman" when fighting crime. Clark Kent resides in the fictional American city of Metropolis, where he works as a journalist for the Daily Planet. Superman's supporting characters include his love interest and fellow journalist Lois Lane, Daily Planet photographer Jimmy Olsen, and editor-in-chief Perry White. His classic foe is Lex Luthor, who is either a mad scientist or a ruthless businessman, depending on the story.""")
    # for sent in doc.sents: # individual sentences
    #     print(sent.text)
    # for token in doc:
    #     print(token.text, token.lemma_, token.pos_, token.dep_)
    #     # attributes of each token; lemmas, POS tags, syntatic dependencies
    # doc = nlp("I prefer a direct flight to Chicago.")
    # displacy.serve(doc, style="dep") # http://localhost:5000/

    # doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
    # for ent in doc.ents:
    #     print(ent.text, ent.start_char, ent.end_char, ent.label_)

    # text = "European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices"
    # doc = nlp(text)
    #
    # # Visualize all named entities
    # displacy.serve(doc, style="ent")
    #
    # # To restrict the visualization to specific entity types, modify the options parameter
    # options = {"ents": ["ORG", "MONEY", "DATE"]}
    # displacy.serve(doc, style="ent", options=options)

    # @Language.component("custom_title_counter")
    # def custom_title_counter(doc):
    #     title_count = sum(1 for token in doc if token.is_title)
    #     print(f"This document has {title_count} title-cased tokens.")
    #     return doc
    #
    # # Load the English language model
    # nlp = spacy.load("en_core_web_sm")
    #
    # # Add the custom component to the pipeline
    # nlp.add_pipe("custom_title_counter", last=True)
    #
    # # Print the pipeline components
    # print(nlp.pipe_names)
    #
    # # Process the paragraph
    # text = """Concordia University (French: Université Concordia; commonly referred to as Concordia) is a public comprehensive research university located in Montreal, Quebec, Canada. Founded in 1974 following the merger of Loyola College and Sir George Williams University, Concordia is one of the three universities in Quebec where English is the primary language of instruction (the others being McGill University and Bishops University). As of the 2018–19 academic year, there were 46,829 students enrolled in credit courses at Concordia, making the university among the largest in Canada by enrollment. The university has two campuses, set approximately 7 kilometres (4 miles) apart: Sir George Williams Campus is the main campus, located in Downtown Montreal in an area known as Quartier Concordia; and Loyola Campus in the residential district of Notre-Dame-de-Grâce. """
    # doc = nlp(text)
    #
    # # Visualize all named entities
    # displacy.serve(doc, style="ent")
    #
    # # To restrict the visualization to specific entity types, modify the options parameter
    # options = {"ents": ["ORG", "MONEY", "DATE"]}
    # displacy.serve(doc, style="ent", options=options)

    # go through dir for all content
    for filename in os.listdir(inPath):
        file = inPath + "/" + filename
        print(file)

        os.makedirs(outPath, exist_ok=True)

        parsed = parser.from_file(file)
        plainText = parsed["content"]

        extractName = os.path.splitext(filename)[0]

        newFile = outPath + "/" + extractName + ".txt"
        print(newFile)

        with open(newFile, "w", encoding="utf-8") as f:
            f.write(plainText)





def entityLinking():

    print("link entities topic tp DBpedia and or Wikidata")


def createTopicTriples():

    print("link triples properly")


def main():
    toPlainText(file_path_courseMaterial_Comp335, file_path_courseMaterial_Comp335_out)


if __name__ == '__main__':
    main()

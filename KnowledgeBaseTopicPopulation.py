import spacy
from spacy import displacy
from spacy.language import Language
from tika import parser
import os

# rom spaCy fishing, DBpedia Spotlight
COURSE_MATERIALS = 'data/courseMaterial'
COURSE_MATERIALS_PLAIN_TEXT = 'plainText'


def get_file_path(directory, fileName):
    file_path = os.path.join(directory, fileName)
    return file_path


def to_plain_text(inPath):
    # go through dir for all content
    for course_material in os.listdir(inPath):
        course_path = inPath + "/" + course_material
        for course in os.listdir(course_path):
            course_content = course_path + "/" + course
            print(course_content)
            for filename in os.listdir(course_content):
                file = course_content + "/" + filename
                print(file)

                extractName = os.path.splitext(filename)[0]

                outPath = COURSE_MATERIALS_PLAIN_TEXT + "/" + course_path + "/" + course
                print("outPath " + outPath)
                os.makedirs(outPath, exist_ok=True)

                newFile = outPath + "/" + extractName + ".txt"
                print(newFile)

                # Check if the plaintext file already exists, if so, skip
                if os.path.exists(newFile):
                    print(f"Plaintext file already exists for {filename}. Skipping...")
                    continue

                parsed = parser.from_file(file)
                plainText = parsed['content']
                # print(plainText)

                with open(newFile, "w", encoding="utf-8") as f:
                    f.write(plainText)



def entityLinking():
    print("link entities topic tp DBpedia and or Wikidata")


def createTopicTriples():
    print("link triples properly")


def main():
    to_plain_text(COURSE_MATERIALS)


if __name__ == '__main__':
    main()

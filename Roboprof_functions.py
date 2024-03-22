import rdflib
import csv
import pandas as pd

from rdflib.namespace import FOAF


# Load RDF data from turtle files
file_path1 = "RDFs/Courses.ttl"
file_path2 = "RDFs/Lectures.ttl"
file_path3 = "RDFs/Student_Schema.ttl"
file_path4 = "RDFs/Topics.ttl"
file_path5 = "RDFs/University_Schema.ttl"
file_path6 = "RDFs/Merged.ttl"


def createGraphs():
    g1 = rdflib.Graph()
    g2 = rdflib.Graph()
    g3 = rdflib.Graph()
    g4 = rdflib.Graph()
    g5 = rdflib.Graph()

    g1.parse(file_path1, format="ttl")
    g2.parse(file_path2, format="ttl")
    g3.parse(file_path3, format="ttl")
    g4.parse(file_path4, format="ttl")
    g5.parse(file_path4, format="ttl")

    g6 = g1 + g2 + g3 + g4 + g5
    # print(len(g6))

    # Write the merged graph to a file in Turtle format
    with open(file_path6, "w", encoding="utf-8") as f:
        f.write(g6.serialize(format="turtle"))

    return g6

def URIGenerator(course,filetype,nb):
    if nb < 9:
        match filetype:
            case "Lecture":
                if course == "COMP335":
                    x = "file:///home/roboprof/" + course + "/Lectures/slides0" + str(nb) + ".ppt"
                else:
                    x = "file:///home/roboprof/" +course + "/Lectures/slides0" + str(nb) +".pdf"
                return x
            case "Worksheet":
                x = "file:///home/roboprof/" +course + "/Worksheet/worksheet0" + str(nb) +".pdf"
                return x
            case "Assignment":
                x = "file:///home/roboprof/" + course + "/Assignments/asg" + str(nb) + ".pdf"
                return x
    else:
        match filetype:
            case "Lecture":
                if course == "COMP335":
                    if nb == 19:
                        x = "file:///home/roboprof/" + course + "/Lectures/slides" + str(nb) + ".pptx"
                    else:
                        x = "file:///home/roboprof/" + course + "/Lectures/slides" + str(nb) + ".ppt"
                else:
                    x = "file:///home/roboprof/" + course + "/Lectures/slides" + str(nb) + ".pdf"
                return x
            case "Worksheet":
                x = "file:///home/roboprof/" + course + "/Worksheet/worksheet" + str(nb) + ".pdf"
                return x
            case "Assignment":
                x = "file:///home/roboprof/" + course + "/Assignments/asg" + str(nb) + ".pdf"
                return x

def load_grades():
    file_path = "data/students_grades.csv"
    df = pd.read_csv(file_path)

    df_fname = df['First Name']
    df_lname = df['Last Name']
    df_id = df['ID']
    df_mail = df['Email']
    df_subject = df['Subject']
    df_subject_id = df['Subject_ID']
    df_grade = df['Grade']

    return








# ##################################
# university_name = "Concordia Univerity"
#
# results = g.query(query)
# print(f"The following courses are offered at {university_name}")
# for row in results:
#     print(row.course)

# ########################## How many credits is [course] [id] worth?
#
#
# course_code = None
# course_id = None
# for word in words:
#     if word.isalpha():
#         course_code = word
#     elif word.isdigit():
#         course_id = word
#
# results = g.query(query)
# for row in results:
#     print(f"{course_code} {course_id} is worth {row.credits} credits.")



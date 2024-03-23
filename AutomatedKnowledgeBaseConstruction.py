import csv
import pandas as pd

from rdflib import URIRef, Graph, Literal, Namespace, RDF, FOAF, RDFS

# Load RDF data from turtle files
file_path_students = "data/students_grades.csv"
file_path_merge = "Triples/MergedTriples.ttl"
file_path_students_KB = "Triples/Students.ttl"
file_path_triples = "Triples/triples.ttl"


# Command to create user defined namespaces
kb = URIRef("http://example.org/knowledge-base#")
student = Namespace("http://example.org/student#")
course = Namespace("http://example.org/course#")
grade = Namespace("http://example.org/grade#")
ex = Namespace("http://example.org/")


def extractStudentData():
    student_data = pd.read_csv(file_path_students, header=0)

    return student_data


# Convert student data to RDF triples
def studentDataToRDFTriples(student_data):
    g = Graph()

    # Add the namespace for known prefixes to the graph
    g.bind("foaf", FOAF)
    g.bind("rdfs", RDFS)
    g.bind("rdf", RDF)
    g.bind("student", student)
    g.bind("course", course)
    g.bind("grade", grade)

    # print(g.serialize(format='turtle'))

    for index, row in student_data.iterrows():
        student_uri = URIRef(student + str(row["ID"]))
        g.add((student_uri, RDF.type, ex.student))
        # Properties
        g.add((student_uri, student.hasFirstName, Literal(row["First Name"])))
        g.add((student_uri, student.hasLastName, Literal(row["Last Name"])))
        g.add((student_uri, student.hasIDNumber, Literal(row["ID"])))

        # Define course as a class
        course_uri = URIRef(course + row["Course"].replace(" ", ""))
        g.add((course_uri, RDF.type, ex.course))

        # Create separate triples for each course taken by each student
        g.add((student_uri, student.hasCompletedCourse, course_uri))

        # Associate grade with course
        grade_uri = URIRef(grade + str(row['ID']) + '/' + row['Course'].replace(" ", ""))
        g.add((student_uri, student.hasGrade, grade_uri))
        g.add((grade_uri, student.gradeValue, Literal(row["Grade"])))
        g.add((grade_uri, student.gradeForCourse, course_uri))
    return g


def mergeGraphs(g1, g2):

    # g1.parse(file_path_merge, format="ttl")

    g3 = g1 + g2
    # print(len(g6))

    return g3


def createGraph(g1, filePath):
    # Write the merged graph to a file in Turtle format
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(g1.serialize(format="turtle"))


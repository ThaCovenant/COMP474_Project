import csv
import pandas as pd

from rdflib import URIRef, Graph, Literal, Namespace, RDF, FOAF, RDFS

# Load RDF data from turtle files
file_path_students = "data/students_grades.csv"
file_path_merge = "Triples/MergedTriples.ttl"

# Command to create user defined namespaces
kb = URIRef("http://example.org/knowledge-base#")
rdfs = URIRef("http://www.w3.org/2000/01/rdf-schema#")
student = Namespace("http://example.org/student")


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

    # g.add((student.Amish, RDF.type, student.Student))
    # g.add((student.Amish, RDFS.label, Literal("Student")))
    # g.add((student.Amish, RDFS.hasCompetency, Literal("KnowledgeGraphs")))
    # g.add((student.Amish, RDFS.hasEmail, Literal("Amish@gmail.com")))
    # g.add((student.Amish, RDFS.hasFirstName, Literal("Amish")))
    # g.add((student.Amish, RDFS.hasLastName, Literal("Patel")))
    # g.add((student.Amish, RDFS.hasGrade, Literal("A")))
    # g.add((student.Amish, RDFS.hasIDNumber, Literal("40044279")))

    # print(g.serialize(format='turtle'))

    for index, row in student_data.iterrows():
        student_uri = URIRef(student + str(row["ID"]))
        g.add((student_uri, RDF.type, RDFS.Class))
        g.add((student_uri, student.hasFirstName, Literal(row["First Name"])))
        g.add((student_uri, student.hasLastName, Literal(row["Last Name"])))
        g.add((student_uri, student.hasIDNumber, Literal(row["ID"])))
        # course_uri = URIRef(row["Subject_ID"])
        # g.add((student_uri, student.hasCompletedCourse, course_uri))
        # g.add((course_uri, RDF.type, student.Course))  # Assuming course is defined elsewhere
        # g.add((student_uri, student.hasGrade, Literal(row["Grade"])))
        # # Assuming Competency is defined elsewhere and linked properly
        # g.add((student_uri, student.hasCompetency, Literal(row["Competency"])))
        print(student_uri)
    return g


def createGraphs(g1, g2):
    g1 = Graph()
    g2 = Graph()

    g1.parse(file_path_merge, format="ttl")

    g3 = g1 + g2
    # print(len(g6))

    # Write the merged graph to a file in Turtle format
    with open(file_path_merge, "w", encoding="utf-8") as f:
        f.write(g3.serialize(format="turtle"))

    return g3


def main():
    print(extractStudentData())
    g = studentDataToRDFTriples(extractStudentData())
    print(g.serialize(format='turtle'))

    # graph = createGraphs()
    # # print(graph.serialize(format='turtle'))
    #
    # # Loop through each triple in the graph (subj, pred, obj)
    # for s, p, o in graph:
    #     # Print the subject, predicate and the object
    #     print(s, p, o)


if __name__ == '__main__':
    main()

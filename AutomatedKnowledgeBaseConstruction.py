import csv
import pandas as pd

from rdflib import URIRef, Graph, Literal, Namespace, RDF

# Load RDF data from turtle files
file_path_students = "data/students_grades.csv"
file_path_merge = "Triples/MergedGraph.ttl"

kb = URIRef("http://example.org/knowledge-base#")
rdfs = URIRef("http://example.org/rdfs#")


def extractStudentData():
    student_data = pd.read_csv(file_path_students, header=0)

    return student_data


# Convert student data to RDF triples
def studentDataToRDFTriples(student_data):
    g = Graph()
    for index, row in student_data.iterrows():
        student_uri = kb["student_" + str(row["ID"])]
        g.add((student_uri, RDF.type, rdfs.Student))
        g.add((student_uri, rdfs.hasFirstName, Literal(row["First Name"])))
        g.add((student_uri, rdfs.hasLastName, Literal(row["Last Name"])))
        g.add((student_uri, rdfs.hasGrade, Literal(row["Grade"])))
        # Assuming Subject and Subject_ID are also properties of the student
        g.add((student_uri, rdfs.hasSubject, Literal(row["Subject"])))
        g.add((student_uri, rdfs.hasSubjectID, Literal(row["Subject_ID"])))
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

    # graph = createGraphs()
    # # print(graph.serialize(format='turtle'))
    #
    # # Loop through each triple in the graph (subj, pred, obj)
    # for s, p, o in graph:
    #     # Print the subject, predicate and the object
    #     print(s, p, o)


if __name__ == '__main__':
    main()

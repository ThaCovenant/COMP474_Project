from rdflib import URIRef, Graph, Literal, Namespace, RDF, FOAF, RDFS

# Load RDF data from turtle files
file_path1 = "RDFs/Courses.ttl"
file_path2 = "RDFs/Lectures.ttl"
file_path3 = "RDFs/Student_Schema.ttl"
file_path4 = "RDFs/Topics.ttl"
file_path5 = "RDFs/University_Schema.ttl"
file_path6 = "RDFs/MergedNew.ttl"
file_path_students = "data/students_grades.csv"
file_path_merge = "Triples/MergedTriples.ttl"
file_path_students_KB = "Triples/students.ttl"


def mergedSchema():
    g1 = Graph()
    g2 = Graph()
    g3 = Graph()
    g4 = Graph()
    g5 = Graph()

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


def chatbotInterface():

    print("This is chatbot interface")

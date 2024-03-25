from rdflib import Graph
from Roboprof_functions import mergedSchema
from AutomatedKnowledgeBaseConstruction import (studentDataToRDFTriples,
                                                extractStudentData,
                                                createGraph,
                                                topicTriplesGenerator)

file_path1 = "RDFs/Courses.ttl"
file_path2 = "RDFs/Lectures.ttl"
file_path3 = "RDFs/Student_Schema.ttl"
file_path5 = "RDFs/University_Schema.ttl"
file_path6 = "RDFs/Merged.ttl"
file_path_students = "data/students_grades.csv"
file_path_merge = "Triples/MergedTriples.ttl"
file_path_students_KB = "Triples/students.ttl"
file_path_triples = "Triples/triples.ttl"
file_path_topics = "Triples/topics.ttl"
file_path_courseMaterial_Comp335 = "data/courseMaterial/COMP335"
file_path_courseMaterial_Comp474 = "data/courseMaterial/COMP474"
file_path_lecture = "Triples/lectures.ttl"


def main():
    mergedSchema()

    g1 = studentDataToRDFTriples(extractStudentData())
    createGraph(g1, file_path_students_KB)

    g2 = Graph()
    g2.parse(file_path_triples, format="ttl")
    # print(g2.serialize(format='turtle'))

    folders = [file_path_courseMaterial_Comp335, file_path_courseMaterial_Comp474]
    g3 = topicTriplesGenerator(folders)
    createGraph(g3, file_path_lecture)

    # g4 = Graph()
    # g4.parse(file_path_topics, format="ttl")

    g5 = g1 + g2 + g3
    # print(g5.serialize(format='turtle'))
    createGraph(g5, file_path_merge)


if __name__ == '__main__':
    main()

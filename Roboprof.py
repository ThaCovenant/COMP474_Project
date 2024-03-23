# from Roboprof_functions
from AutomatedKnowledgeBaseConstruction import studentDataToRDFTriples, extractStudentData, createGraph, mergeGraphs
from rdflib import Graph

file_path1 = "RDFs/Courses.ttl"
file_path2 = "RDFs/Lectures.ttl"
file_path3 = "RDFs/Student_Schema.ttl"
file_path4 = "RDFs/Topics.ttl"
file_path5 = "RDFs/University_Schema.ttl"
file_path6 = "RDFs/Merged.ttl"
file_path_students = "data/students_grades.csv"
file_path_merge = "Triples/MergedTriples.ttl"
file_path_students_KB = "Triples/Students.ttl"
file_path_triples = "Triples/triples.ttl"
file_path_topics = "Triples/topics.ttl"


def main():
    # graph = createGraphs()
    # print(graph.serialize(format='turtle'))
    # print(extractStudentData())
    g1 = studentDataToRDFTriples(extractStudentData())
    # print(g.serialize(format='turtle'))
    g2 = Graph()
    g2.parse(file_path_triples, format="ttl")

    g3 = mergeGraphs(g1, g2)
    createGraph(g3, file_path_merge)

    g4 = Graph()
    g4.parse(file_path_topics, format="ttl")
    g5 = mergeGraphs(g3, g4)


    print(g5.serialize(format='turtle'))


if __name__ == '__main__':
    main()

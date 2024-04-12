from rdflib import Graph
from Roboprof_functions import mergedSchema
from AutomatedKnowledgeBaseConstruction import (student_data_to_rdf_triples,
                                                extract_student_data,
                                                create_graph,
                                                create_content_triples, extract_courses_data)

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
file_path_courses = "Triples/courses.ttl"


def main():
    mergedSchema()

    g1 = student_data_to_rdf_triples(extract_student_data())
    create_graph(g1, file_path_students_KB)

    g2 = Graph()
    g2.parse(file_path_triples, format="ttl")
    # print(g2.serialize(format='turtle'))

    folders = [file_path_courseMaterial_Comp335, file_path_courseMaterial_Comp474]
    g3 = create_content_triples(folders)
    create_graph(g3, file_path_lecture)

    # g4 = Graph()
    # g4.parse(file_path_topics, format="ttl")

    g5 = extract_courses_data()
    create_graph(g5, file_path_courses)

    g6 = g1 + g2 + g3 + g5
    # print(g5.serialize(format='turtle'))
    create_graph(g6, file_path_merge)


if __name__ == '__main__':
    main()

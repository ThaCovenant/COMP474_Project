import os

from rdflib import Graph

from KnowledgeBaseTopicPopulation import COURSE_MATERIALS_PLAIN_TEXT, process_plaintext
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
file_path_topics = "Triples/topics.ttl"
# file_path_topics_new = "Triples/topicsNew.ttl"
file_path_courseMaterial_Comp335 = "data/courseMaterial/COMP335"
file_path_courseMaterial_Comp474 = "data/courseMaterial/COMP474"
file_path_lecture = "Triples/lectures.ttl"
file_path_courses = "Triples/courses.ttl"


def verify_graph(file_path, overwrite=False):
    if overwrite:
        print(f"TTL file '{file_path}' overwite.")
        return True
    elif os.path.exists(file_path):
        print(f"TTL file '{file_path}' already exists. Skipping creation.")
        return False
    else:
        print(f"TTL file '{file_path}' created.")
        return True


def main():
    # mergedSchema()
    g1 = Graph()
    if verify_graph(file_path_students_KB, True):
        g1 = student_data_to_rdf_triples(extract_student_data())
        create_graph(g1, file_path_students_KB)

    g3 = Graph()
    if verify_graph(file_path_lecture):
        folders = [file_path_courseMaterial_Comp335, file_path_courseMaterial_Comp474]
        g3 = create_content_triples(folders)
        create_graph(g3, file_path_lecture)

    g4 = Graph()
    if verify_graph(file_path_topics):
        g4 = process_plaintext(COURSE_MATERIALS_PLAIN_TEXT)
        create_graph(g4, file_path_topics)

    g5 = Graph()
    if verify_graph(file_path_lecture):
        g5 = extract_courses_data()
        create_graph(g5, file_path_courses)

    if verify_graph(file_path_merge):
        g6 = (g1.parse(file_path_students_KB, format="ttl") +
              g3.parse(file_path_lecture, format="ttl") +
              g4.parse(file_path_topics, format="ttl") +
              g5.parse(file_path_courses, format="ttl"))
        # print(g5.serialize(format='turtle'))
        create_graph(g6, file_path_merge)


if __name__ == '__main__':
    main()

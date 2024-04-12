import os.path

import pandas as pd
from rdflib import URIRef, Graph, Literal, Namespace, RDF, FOAF, RDFS, XSD

# Load RDF data from turtle files
file_path_students = "data/students_grades.csv"
file_path_courses = "data/CU_SR_OPEN_DATA_CATALOG.csv"
file_path_merge = "Triples/MergedTriples.ttl"
file_path_students_KB = "Triples/students.ttl"
file_path_triples = "Triples/triples.ttl"

# Command to create user defined namespaces
namespaces = {
    'kb': Namespace("http://example.org/knowledge-base#"),
    'student': Namespace("http://example.org/student/"),
    'course': Namespace("http://example.org/course/"),
    'lecture': Namespace("http://example.org/lecture/"),
    'slides': Namespace("http://example.org/slides/"),
    'lectureContent': Namespace("http://example.org/lectureContent/"),
    'worksheets': Namespace("http://example.org/worksheets/"),
    'other': Namespace("http://example.org/other/"),
    'readings': Namespace("http://example.org/readings/"),
    'assignments': Namespace("http://example.org/assignments/"),
    'completedCourse': Namespace("http://example.org/completedCourse/"),
    'topic': Namespace("http://example.org/topic/"),
    'university': Namespace("https://www.wikidata.org/entity/Q3918"),
    'wd': Namespace("https://www.wikidata.org/wiki/"),
    'dp': Namespace("http://dbpedia.org/resource/")
}


# Bind namespaces
def bind_namespaces(graph):
    for prefix, ns in namespaces.items():
        graph.bind(prefix, ns)


# Initialize RDF graph
def init_graph():
    graph = Graph()
    bind_namespaces(graph)
    return graph


def create_graph(g1, filePath):
    # Write the merged graph to a file in Turtle format
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(g1.serialize(format="turtle"))


def URIGenerator(courseName, filetype, nb):
    if nb < 9:
        match filetype:
            case "Lectures":
                if courseName == "COMP335":
                    x = "file:///home/roboprof/" + courseName + "/Lectures/slide" + str(nb) + ".ppt"
                else:
                    x = "file:///home/roboprof/" + courseName + "/Lectures/slide" + str(nb) + ".pdf"
                return x
            case "Worksheets":
                x = "file:///home/roboprof/" + courseName + "/Worksheets/worksheet" + str(nb) + ".pdf"
                return x
            case "Assignments":
                x = "file:///home/roboprof/" + courseName + "/Assignments/asg" + str(nb) + ".pdf"
                return x
    else:
        match filetype:
            case "Lectures":
                if courseName == "COMP335":
                    if nb == 19:
                        x = "file:///home/roboprof/" + courseName + "/Lectures/slide" + str(nb) + ".pptx"
                    else:
                        x = "file:///home/roboprof/" + courseName + "/Lectures/slide" + str(nb) + ".ppt"
                else:
                    x = "file:///home/roboprof/" + courseName + "/Lectures/slide" + str(nb) + ".pdf"
                return x
            case "Worksheets":
                x = "file:///home/roboprof/" + courseName + "/Worksheets/worksheet" + str(nb) + ".pdf"
                return x
            case "Assignments":
                x = "file:///home/roboprof/" + courseName + "/Assignments/asg" + str(nb) + ".pdf"
                return x


def count_files_in_folder(path):
    if not os.path.exists(path):
        print("Error: The provided path is not a directory.")
        return
    #
    files = os.listdir(path)
    # print(files)
    # numFiles = len(files)
    # print(numFiles)

    return len(files)


def content_triples_gen(graph, courseName, fileType, fileName, content, i):
    g = graph
    # Create course_uri instance of class course
    course_uri = URIRef(namespaces['course'] + courseName)

    # Create lectureURI instance of Lecture Class
    lectureURI = URIRef(namespaces['lecture'] + courseName + "Lecture" + str(i))  # lec1
    g.add((lectureURI, RDF.type, namespaces['lecture'].lecture))  # lecture:lec1 a lecture:lecture
    g.add((course_uri, namespaces['course'].hasLecture, lectureURI))  # course:course_uri lecture:hasLecture, lecture:lec1
    g.add((lectureURI, RDFS.label, Literal("Lecture")))
    g.add((lectureURI, RDFS.comment, Literal("This is a lecture.", lang='en')))

    # Lecture lectureURI Properties
    g.add((lectureURI, namespaces['lecture'].lectureNumber, Literal(i, datatype=XSD.integer)))
    # g.add((lectureURI, lecture.lectureName, Literal("Lecture Name")))
    lectureContentURI = URIRef(namespaces['lectureContent'] + courseName + "LectureContents")

    g.add((lectureURI, namespaces['lecture'].hasContent, lectureContentURI))

    # Create lectureContentURI instance of lectureContent Class
    g.add((lectureContentURI, RDF.type, namespaces['lectureContent'].lectureContent))

    # Create contentURI instance of Slides class
    contentURI = URIRef(URIGenerator(courseName, fileType, i))
    # Subclass instance of lectureContent
    contentClass = URIRef(content + fileName)

    # print(contentURI)
    g.add((contentURI, RDF.type, contentClass))
    g.add((contentURI, RDFS.subClassOf, lectureContentURI))
    g.add((contentURI, RDFS.label, Literal(fileName + str(i))))
    g.add((contentURI, RDFS.comment, Literal(fileName + " of lecture " + str(i), lang='en')))

    return g


def create_content_triples(courseFolders):
    g = init_graph()

    for folder in courseFolders:
        courseName = folder.split("/")[-1]

        lectureFolderLectures = os.path.join(folder, "Lectures")

        courseURI = URIRef(namespaces['course'] + courseName)  # lec1
        g.add((courseURI, RDF.type, namespaces['course'].course))

        if os.path.exists(lectureFolderLectures):
            numFiles = count_files_in_folder(lectureFolderLectures)
            for i in range(1, numFiles + 1):
                fileType = "Lectures"
                fileName = "Slides"

                g1 = content_triples_gen(g, courseName, fileType, fileName, namespaces['slides'], i)
                g = g + g1

        lectureFolderAssignments = os.path.join(folder, "Assignments")
        if os.path.exists(lectureFolderAssignments):
            numFiles = count_files_in_folder(lectureFolderAssignments)
            for i in range(1, numFiles + 1):
                fileType = "Assignments"
                fileName = "Assignments"

                g1 = content_triples_gen(g, courseName, fileType, fileName, namespaces['assignments'], i)
                g = g + g1

        lectureFolderWorksheets = os.path.join(folder, "Worksheets")
        if os.path.exists(lectureFolderWorksheets):
            numFiles = count_files_in_folder(lectureFolderWorksheets)
            for i in range(1, numFiles + 1):
                fileType = "Worksheets"
                fileName = "Worksheets"

                g1 = content_triples_gen(g, courseName, fileType, fileName, namespaces['worksheets'], i)
                g = g + g1
    return g


def extract_student_data():
    studentData = pd.read_csv(file_path_students, header=0)

    return studentData


# Convert student data to RDF triples
def student_data_to_rdf_triples(student_data):
    g = init_graph()

    gradeMapping = {
        'A+': 4.3, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'D-': 0.7,
        'F': 0.0
    }

    # print(g.serialize(format='turtle'))

    for index, row in student_data.iterrows():
        # Create studentURI instance of class Student
        studentURI = URIRef(namespaces['student'] + str(row["ID"]))
        g.add((studentURI, RDF.type, namespaces['student'].student))
        g.add((studentURI, RDFS.label, Literal("Student")))
        g.add((studentURI, RDFS.comment, Literal("This is a Student Class.", lang='en')))

        # Student Properties
        g.add((studentURI, namespaces['student'].hasFirstName, Literal(row["First Name"])))
        g.add((studentURI, namespaces['student'].hasLastName, Literal(row["Last Name"])))
        g.add((studentURI, namespaces['student'].hasIDNumber, Literal(row["ID"])))

        # Create courseURI instance of class course
        courseURI = URIRef(namespaces['course'] + row["Course"].replace(" ", ""))

        # Student Properties continue
        if row["Grade"] is not None and row["Grade"] in gradeMapping:
            completedCourseURI = URIRef(
                namespaces['completedCourse'] + str(row["ID"]) +
                row["Course"].replace(" ", "") +
                str(row["Date"]).replace("/", ""))
            g.add((studentURI, namespaces['student'].hasCompletedCourse, completedCourseURI))
            g.add((completedCourseURI, RDF.type, namespaces['completedCourse'].completedCourse))
            g.add((completedCourseURI, RDF.type, courseURI))
            g.add((completedCourseURI, namespaces['student'].hasGrade, Literal(row["Grade"])))
            g.add((completedCourseURI, namespaces['student'].completedOn, Literal(row["Date"], datatype=XSD.date)))

            # If statement for passing course to get competency
            numGrade = gradeMapping[row["Grade"]]
            if numGrade > 0.0:
                g.add((studentURI, namespaces['student'].hasCompetency, namespaces['topic'].KnowledgeGraph))

    return g


def extract_courses_data():
    g = init_graph()

    # Add the namespace for known prefixes to the graph

    universityURI = URIRef(Literal("https://www.concordia.ca/"))
    g.add((universityURI, RDF.type, namespaces['university'].university))
    g.add((universityURI, namespaces['university'].Name, Literal("Concordia")))
    g.add((universityURI, namespaces['university'].WikidataEntry, namespaces['dp'].Concordia_University))
    g.add((universityURI, namespaces['university'].DBpediaEntry, namespaces['wd'].Q326342))
    g.add((universityURI, RDFS.label, Literal("university")))
    g.add((universityURI, RDFS.comment, Literal("A university.", lang='en')))

    googleURI = "http://google.com/"

    courseData = pd.read_csv(file_path_courses, encoding='utf-16')

    for index, row in courseData.iterrows():
        # Create courseURI instance of class course
        courseURI = URIRef(namespaces['course'] + Literal(row["Subject"]) + Literal(row["Catalog"]))
        g.add((courseURI, RDF.type, namespaces['course'].course))
        g.add((courseURI, RDFS.label, Literal("course")))
        g.add((courseURI, RDFS.comment, Literal("A course offered by the university.", lang='en')))
        g.add((courseURI, namespaces['course'].courseName, Literal(row["Long Title"])))
        g.add((courseURI, namespaces['course'].courseSubject, Literal(row["Subject"])))
        g.add((courseURI, namespaces['course'].courseNumber, Literal(row["Catalog"])))
        g.add((courseURI, namespaces['course'].courseCredit, Literal(row["Class Units"], datatype=XSD.decimal)))
        g.add((courseURI, namespaces['course'].courseDescription, Literal(row["Component Descr"])))
        courseLink = URIRef(googleURI + Literal(row["Subject"]) + Literal(row["Catalog"]))
        g.add((courseURI, RDFS.seeAlso, courseLink))
        g.add((courseURI, namespaces['course'].offeredBy, universityURI))

    return g

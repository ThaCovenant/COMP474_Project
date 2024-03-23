import os.path

import pandas as pd

from rdflib import URIRef, Graph, Literal, Namespace, RDF, FOAF, RDFS

# Load RDF data from turtle files
file_path_students = "data/students_grades.csv"
file_path_merge = "Triples/MergedTriples.ttl"
file_path_students_KB = "Triples/students.ttl"
file_path_triples = "Triples/triples.ttl"

# Command to create user defined namespaces
kb = URIRef("http://example.org/knowledge-base#")
student = Namespace("http://example.org/student#")
course = Namespace("http://example.org/course#")
grade = Namespace("http://example.org/grade#")
lecture = Namespace("http://example.org/lecture#")
slides = Namespace("http://example.org/slides#")
lectureContent = Namespace("http://example.org/lectureContent#")
worksheets = Namespace("http://example.org/worksheets#")
other = Namespace("http://example.org/other#")
readings = Namespace("http://example.org/readings#")
ex = Namespace("http://example.org/")
assignments = Namespace("http://example.org/assignments#")


def createGraph(g1, filePath):
    # Write the merged graph to a file in Turtle format
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(g1.serialize(format="turtle"))


def URIGenerator(courseName, filetype, nb):
    if nb < 9:
        match filetype:
            case "Lecture":
                if courseName == "COMP335":
                    x = "file:///home/roboprof/" + courseName + "/Lectures/slides0" + str(nb) + ".ppt"
                else:
                    x = "file:///home/roboprof/" + courseName + "/Lectures/slides0" + str(nb) + ".pdf"
                return x
            case "Worksheet":
                x = "file:///home/roboprof/" + courseName + "/Worksheet/worksheet0" + str(nb) + ".pdf"
                return x
            case "Assignment":
                x = "file:///home/roboprof/" + courseName + "/Assignments/asg" + str(nb) + ".pdf"
                return x
    else:
        match filetype:
            case "Lecture":
                if courseName == "COMP335":
                    if nb == 19:
                        x = "file:///home/roboprof/" + courseName + "/Lectures/slides" + str(nb) + ".pptx"
                    else:
                        x = "file:///home/roboprof/" + courseName + "/Lectures/slides" + str(nb) + ".ppt"
                else:
                    x = "file:///home/roboprof/" + courseName + "/Lectures/slides" + str(nb) + ".pdf"
                return x
            case "Worksheet":
                x = "file:///home/roboprof/" + courseName + "/Worksheet/worksheet" + str(nb) + ".pdf"
                return x
            case "Assignment":
                x = "file:///home/roboprof/" + courseName + "/Assignments/asg" + str(nb) + ".pdf"
                return x


def countFilesInFolder(path):
    if not os.path.exists(path):
        print("Error: The provided path is not a directory.")
        return
    #
    files = os.listdir(path)
    # print(files)
    # numFiles = len(files)
    # print(numFiles)

    return len(files)


def topicTriplesGenerator(courseFolders):
    g = Graph()

    g.bind("lecture", lecture)
    g.bind("lectureContent", lectureContent)
    g.bind("assignments", assignments)
    g.bind("worksheets", worksheets)
    g.bind("other", other)
    g.bind("readings", readings)
    g.bind("slides", slides)

    courseNames = []

    for folder in courseFolders:
        courseName = folder.split("/")[-1]

        lectureFolderLectures = os.path.join(folder, "Lectures")
        if os.path.exists(lectureFolderLectures):
            numFiles = countFilesInFolder(lectureFolderLectures)
            for i in range(1, numFiles + 1):
                # Define class LectureContent
                lectureContentURI = URIRef(lectureContent + str(i))
                g.add((lectureContentURI, RDF.type, lectureContent.lectureContent))
                g.add((lectureContentURI, RDFS.label, Literal("Lecture Content")))
                g.add((lectureContentURI, RDFS.comment,
                       Literal("Lecture Content: Worksheets, Readings, Other...", lang='en')))

                # Define class slides
                slidesURI = URIGenerator(courseName, "Lecture", i)
                g.add((URIRef(slidesURI), RDF.type, slides.slides))
                g.add((URIRef(slidesURI), RDFS.subClassOf, lectureContent.lectureContent))
                g.add((URIRef(slidesURI), RDFS.label, Literal("Lecture Slides")))
                g.add((URIRef(slidesURI), RDFS.comment, Literal("Slides of lecture.", lang='en')))

                # Define class lecture
                lectureURI = URIRef(lecture + str(i))
                g.add((lectureURI, RDF.type, lecture.lecture))
                # Create separate triples for each lecture part each course
                g.add((URIRef(lectureURI), RDFS.subClassOf, URIRef(course + courseName)))
                g.add((URIRef(lectureURI), RDFS.label, Literal("Lecture")))
                g.add((URIRef(lectureURI), RDFS.comment, Literal("This is a lecture.", lang='en')))
                g.add((lectureContentURI, RDFS.subClassOf, URIRef(lectureURI)))

        lectureFolderAssignments = os.path.join(folder, "Assignments")
        if os.path.exists(lectureFolderAssignments):
            numFiles = countFilesInFolder(lectureFolderAssignments)
            for i in range(1, numFiles + 1):
                # Define class LectureContent
                lectureContentURI = URIRef(lectureContent + str(i))
                g.add((lectureContentURI, RDF.type, lectureContent.lectureContent))
                g.add((lectureContentURI, RDFS.label, Literal("Lecture Content")))
                g.add((lectureContentURI, RDFS.comment,
                       Literal("Lecture Content: Worksheets, Readings, Other...", lang='en')))

                # Define class assignments
                assignmentsURI = URIGenerator(courseName, "Assignment", i)
                g.add((URIRef(assignmentsURI), RDF.type, assignments.assignments))
                g.add((URIRef(assignmentsURI), RDFS.subClassOf, lectureContent.lectureContent))
                g.add((URIRef(assignmentsURI), RDFS.label, Literal("Assignments PDF")))
                g.add((URIRef(assignmentsURI), RDFS.comment, Literal("Assignments of lecture.", lang='en')))

                # Define class lecture
                lectureURI = URIRef(lecture + str(i))
                g.add((lectureURI, RDF.type, lecture.lecture))
                # Create separate triples for each lecture part each course
                g.add((URIRef(lectureURI), RDFS.subClassOf, URIRef(course + courseName)))
                g.add((URIRef(lectureURI), RDFS.label, Literal("Lecture")))
                g.add((URIRef(lectureURI), RDFS.comment, Literal("This is a lecture.", lang='en')))
                g.add((lectureContentURI, RDFS.subClassOf, URIRef(lectureURI)))

        lectureFolderAssignments = os.path.join(folder, "Worksheet")
        if os.path.exists(lectureFolderAssignments):
            numFiles = countFilesInFolder(lectureFolderAssignments)
            for i in range(1, numFiles + 1):
                # Define class LectureContent
                lectureContentURI = URIRef(lectureContent + str(i))
                g.add((lectureContentURI, RDF.type, lectureContent.lectureContent))
                g.add((lectureContentURI, RDFS.label, Literal("Lecture Content")))
                g.add((lectureContentURI, RDFS.comment,
                       Literal("Lecture Content: Worksheets, Readings, Other...", lang='en')))

                # Define class Worksheet
                worksheetsURI = URIGenerator(courseName, "Worksheet", i)
                g.add((URIRef(worksheetsURI), RDF.type, worksheets.worksheets))
                g.add((URIRef(worksheetsURI), RDFS.subClassOf, lectureContent.lectureContent))
                g.add((URIRef(worksheetsURI), RDFS.label, Literal("Worksheet PDF")))
                g.add((URIRef(worksheetsURI), RDFS.comment, Literal("Worksheet of lecture.", lang='en')))

                # Define class lecture
                lectureURI = URIRef(lecture + str(i))
                g.add((lectureURI, RDF.type, lecture.lecture))
                # Create separate triples for each lecture part each course
                g.add((URIRef(lectureURI), RDFS.subClassOf, URIRef(course + courseName)))
                g.add((URIRef(lectureURI), RDFS.label, Literal("Lecture")))
                g.add((lectureContentURI, RDFS.subClassOf, URIRef(lectureURI)))

    return g


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
        g.add((student_uri, RDF.type, student.student))
        g.add((student_uri, RDFS.label, Literal("Student")))
        g.add((student_uri, RDFS.comment, Literal("This is a Student Class.", lang='en')))

        # Properties
        g.add((student_uri, student.hasFirstName, Literal(row["First Name"])))
        g.add((student_uri, student.hasLastName, Literal(row["Last Name"])))
        g.add((student_uri, student.hasIDNumber, Literal(row["ID"])))

        # Define course as a class
        course_uri = URIRef(course + row["Course"].replace(" ", ""))
        g.add((course_uri, RDF.type, ex.course))
        g.add((course_uri, RDFS.label, Literal("course")))
        g.add((course_uri, RDFS.comment, Literal("A course offered by the university.", lang='en')))

        # Create separate triples for each course taken by each student
        g.add((student_uri, student.hasCompletedCourse, course_uri))

        # Associate grade with course
        grade_uri = URIRef(grade + str(row['ID']) + '/' + row['Course'].replace(" ", ""))
        g.add((student_uri, student.hasGrade, grade_uri))
        g.add((grade_uri, student.gradeValue, Literal(row["Grade"])))
        g.add((grade_uri, student.gradeForCourse, course_uri))
        g.add((grade_uri, RDFS.label, Literal("grade")))
        g.add((grade_uri, RDFS.comment, Literal("Grade of student.", lang='en')))

    return g

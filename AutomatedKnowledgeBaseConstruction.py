import os.path

import pandas as pd

from rdflib import URIRef, Graph, Literal, Namespace, RDF, FOAF, RDFS, XSD

# Load RDF data from turtle files
file_path_students = "data/students_grades.csv"
file_path_merge = "Triples/MergedTriples.ttl"
file_path_students_KB = "Triples/students.ttl"
file_path_triples = "Triples/triples.ttl"

# Command to create user defined namespaces
kb = URIRef("http://example.org/knowledge-base#")
student = Namespace("http://example.org/student/")
course = Namespace("http://example.org/course/")

lecture = Namespace("http://example.org/lecture/")
slides = Namespace("http://example.org/slides/")
lectureContent = Namespace("http://example.org/lectureContent/")
worksheets = Namespace("http://example.org/worksheets/")
other = Namespace("http://example.org/other/")
readings = Namespace("http://example.org/readings/")
ex = Namespace("http://example.org/")
assignments = Namespace("http://example.org/assignments#")


def createGraph(g1, filePath):
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
    g.bind("course", course)
    g.bind("foaf", FOAF)
    g.bind("rdfs", RDFS)
    g.bind("rdf", RDF)
    g.bind("xsd", XSD)

    for folder in courseFolders:
        courseName = folder.split("/")[-1]

        lectureFolderLectures = os.path.join(folder, "Lectures")
        if os.path.exists(lectureFolderLectures):
            numFiles = countFilesInFolder(lectureFolderLectures)
            for i in range(1, numFiles + 1):
                # Create lectureURI instance of Lecture class
                lectureURI = URIRef(lecture + courseName + "_Lecture_" + str(i))
                g.add((lectureURI, RDF.type, lecture.lecture))
                g.add((lectureURI, RDFS.label, Literal("Lecture")))
                g.add((lectureURI, RDFS.comment, Literal("This is a lecture.", lang='en')))

                # Create course_uri instance of class course
                course_uri = URIRef(course + courseName)
                # print(course_uri)
                g.add((course_uri, RDF.type, course.course))
                g.add((course_uri, course.courseName, Literal(courseName)))

                # Lecture lectureURI Properties
                g.add((lectureURI, lecture.lectureNumber, Literal(i, datatype=XSD.integer)))
                g.add((lectureURI, lecture.partOfCourse, course_uri))
                g.add((lectureURI, lecture.lectureContent, lectureContent.slides))

                # Create slidesURI instance of Slides class
                slidesURI = URIGenerator(courseName, "Lectures", i)
                # print(slidesURI)
                g.add((URIRef(slidesURI), RDF.type, slides.slides))
                g.add((URIRef(slidesURI), RDFS.subClassOf, lectureContent.lectureContent))
                g.add((URIRef(slidesURI), RDFS.label, Literal("Slides PDF")))
                g.add((URIRef(slidesURI), RDFS.comment, Literal("Slides of lecture.", lang='en')))

        lectureFolderAssignments = os.path.join(folder, "Assignments")
        if os.path.exists(lectureFolderAssignments):
            numFiles = countFilesInFolder(lectureFolderAssignments)
            for i in range(1, numFiles + 1):
                # Create lectureURI instance of Lecture class
                lectureURI = URIRef(lecture + courseName + "_Lecture_" + str(i))
                g.add((lectureURI, RDF.type, lecture.lecture))
                g.add((lectureURI, RDFS.label, Literal("Lecture")))
                g.add((lectureURI, RDFS.comment, Literal("This is a lecture.", lang='en')))

                # Create course_uri instance of class course
                course_uri = URIRef(course + courseName)
                # print(course_uri)
                g.add((course_uri, RDF.type, course.course))
                g.add((course_uri, course.courseName, Literal(courseName)))

                # Lecture lectureURI Properties
                g.add((lectureURI, lecture.lectureNumber, Literal(i, datatype=XSD.integer)))
                g.add((lectureURI, lecture.partOfCourse, course.courseName))
                g.add((lectureURI, lecture.lectureContent, lectureContent.assignments))

                # Create assignmentURI instance of Assignment class
                assignmentsURI = URIGenerator(courseName, "Assignments", i)
                g.add((URIRef(assignmentsURI), RDF.type, assignments.assignments))
                g.add((URIRef(assignmentsURI), RDFS.subClassOf, lectureContent.lectureContent))
                g.add((URIRef(assignmentsURI), RDFS.label, Literal("Assignments PDF")))
                g.add((URIRef(assignmentsURI), RDFS.comment, Literal("Assignments of lecture.", lang='en')))

        lectureFolderWorksheets = os.path.join(folder, "Worksheets")
        if os.path.exists(lectureFolderWorksheets):
            numFiles = countFilesInFolder(lectureFolderWorksheets)
            for i in range(1, numFiles + 1):
                # Create lectureURI instance of Lecture class
                lectureURI = URIRef(lecture + courseName + "_Lecture_" + str(i))
                g.add((lectureURI, RDF.type, lecture.lecture))
                g.add((lectureURI, RDFS.label, Literal("Lecture")))
                g.add((lectureURI, RDFS.comment, Literal("This is a lecture.", lang='en')))

                # Create course_uri instance of class course
                course_uri = URIRef(course + courseName)
                # print(course_uri)
                g.add((course_uri, RDF.type, course.course))
                g.add((course_uri, course.courseName, Literal(courseName)))

                # Lecture lectureURI Properties
                g.add((lectureURI, lecture.lectureNumber, Literal(i, datatype=XSD.integer)))
                g.add((lectureURI, lecture.partOfCourse, course.courseName))
                g.add((lectureURI, lecture.lectureContent, lectureContent.worksheets))

                # Create assignmentURI instance of Assignment class
                worksheetsURI = URIGenerator(courseName, "Worksheets", i)
                g.add((URIRef(worksheetsURI), RDF.type, worksheets.worksheets))
                g.add((URIRef(worksheetsURI), RDFS.subClassOf, lectureContent.lectureContent))
                g.add((URIRef(worksheetsURI), RDFS.label, Literal("This is a Worksheets")))
                g.add((URIRef(worksheetsURI), RDFS.comment, Literal("Worksheets of lecture.", lang='en')))
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

    # print(g.serialize(format='turtle'))

    for index, row in student_data.iterrows():
        # Create student_uri instance of class Student
        student_uri = URIRef(student + str(row["ID"]))
        g.add((student_uri, RDF.type, student.student))
        g.add((student_uri, RDFS.label, Literal("Student")))
        g.add((student_uri, RDFS.comment, Literal("This is a Student Class.", lang='en')))

        # Student Properties
        g.add((student_uri, student.hasFirstName, Literal(row["First Name"])))
        g.add((student_uri, student.hasLastName, Literal(row["Last Name"])))
        g.add((student_uri, student.hasIDNumber, Literal(row["ID"])))

        # Create course_uri instance of class course
        course_uri = URIRef(course + row["Course"].replace(" ", ""))
        g.add((course_uri, RDF.type, course.course))
        g.add((course_uri, RDFS.label, Literal("course")))
        g.add((course_uri, RDFS.comment, Literal("A course offered by the university.", lang='en')))
        g.add((course_uri, course.courseName, Literal(row["Course"].replace(" ", ""))))

        # Student Properties continue
        g.add((student_uri, student.hasCompletedCourse, course_uri))
        g.add((student_uri, student.hasGrade, Literal(row["Grade"])))

        # Associate grade with course

    return g

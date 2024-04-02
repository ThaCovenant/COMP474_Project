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
assignments = Namespace("http://example.org/assignments/")
completedCourse = Namespace("http://example.org/completedCourse/")
topic = Namespace("http://example.org/topic/")
university = Namespace("https://www.wikidata.org/entity/Q3918")
wd = Namespace("https://www.wikidata.org/wiki/")
dp = Namespace("http://dbpedia.org/resource/")


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


def createTriples(courseName, fileType, fileName, content, i):
    g = Graph()
    # Create course_uri instance of class course
    course_uri = URIRef(course + courseName)

    # Create lectureURI instance of Lecture Class
    lectureURI = URIRef(lecture + courseName + "Lecture" + str(i))  # lec1
    g.add((lectureURI, RDF.type, lecture.lecture))  # lecture:lec1 a lecture:lecture
    g.add((course_uri, course.hasLecture, lectureURI))  # course:course_uri lecture:hasLecture, lecture:lec1
    g.add((lectureURI, RDFS.label, Literal("Lecture")))
    g.add((lectureURI, RDFS.comment, Literal("This is a lecture.", lang='en')))

    # Lecture lectureURI Properties
    g.add((lectureURI, lecture.lectureNumber, Literal(i, datatype=XSD.integer)))
    # g.add((lectureURI, lecture.lectureName, Literal("Lecture Name")))
    lectureContentURI = URIRef(lectureContent + courseName + "LectureContents")

    g.add((lectureURI, lecture.hasContent, lectureContentURI))

    # Create lectureContentURI instance of lectureContent Class
    g.add((lectureContentURI, RDF.type, lectureContent.lectureContent))

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


def createContentTriples(courseFolders):
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

        courseURI = URIRef(course + courseName)  # lec1
        g.add((courseURI, RDF.type, course.course))

        if os.path.exists(lectureFolderLectures):
            numFiles = countFilesInFolder(lectureFolderLectures)
            for i in range(1, numFiles + 1):
                fileType = "Lectures"
                fileName = "Slides"

                g1 = createTriples(courseName, fileType, fileName, slides, i)
                g = g + g1

        lectureFolderAssignments = os.path.join(folder, "Assignments")
        if os.path.exists(lectureFolderAssignments):
            numFiles = countFilesInFolder(lectureFolderAssignments)
            for i in range(1, numFiles + 1):
                fileType = "Assignments"
                fileName = "Assignments"

                g1 = createTriples(courseName, fileType, fileName, assignments, i)
                g = g + g1

        lectureFolderWorksheets = os.path.join(folder, "Worksheets")
        if os.path.exists(lectureFolderWorksheets):
            numFiles = countFilesInFolder(lectureFolderWorksheets)
            for i in range(1, numFiles + 1):
                fileType = "Worksheets"
                fileName = "Worksheets"

                g1 = createTriples(courseName, fileType, fileName, worksheets, i)
                g = g + g1
    return g


def extractStudentData():
    studentData = pd.read_csv(file_path_students, header=0)

    return studentData


# Convert student data to RDF triples
def studentDataToRDFTriples(student_data):
    g = Graph()

    # Add the namespace for known prefixes to the graph
    g.bind("foaf", FOAF)
    g.bind("rdfs", RDFS)
    g.bind("rdf", RDF)
    g.bind("student", student)
    g.bind("course", course)
    g.bind("completedCourse", completedCourse)
    g.bind("topic", topic)

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
        studentURI = URIRef(student + str(row["ID"]))
        g.add((studentURI, RDF.type, student.student))
        g.add((studentURI, RDFS.label, Literal("Student")))
        g.add((studentURI, RDFS.comment, Literal("This is a Student Class.", lang='en')))

        # Student Properties
        g.add((studentURI, student.hasFirstName, Literal(row["First Name"])))
        g.add((studentURI, student.hasLastName, Literal(row["Last Name"])))
        g.add((studentURI, student.hasIDNumber, Literal(row["ID"])))

        # Create courseURI instance of class course
        courseURI = URIRef(course + row["Course"].replace(" ", ""))

        # Student Properties continue
        if row["Grade"] is not None and row["Grade"] in gradeMapping:
            completedCourseURI = URIRef(
                completedCourse + str(row["ID"]) +
                row["Course"].replace(" ", "") +
                str(row["Date"]).replace("/", ""))
            g.add((studentURI, student.hasCompletedCourse, completedCourseURI))
            g.add((completedCourseURI, RDF.type, completedCourse.completedCourse))
            g.add((completedCourseURI, RDF.type, courseURI))
            g.add((completedCourseURI, student.hasGrade, Literal(row["Grade"])))
            g.add((completedCourseURI, student.completedOn, Literal(row["Date"], datatype=XSD.date)))

            # If statement for passing course to get competency
            numGrade = gradeMapping[row["Grade"]]
            if numGrade > 0.0:
                g.add((studentURI, student.hasCompetency, topic.KnowledgeGraph))

    return g


def extractCoursesData():
    g = Graph()

    # Add the namespace for known prefixes to the graph
    g.bind("foaf", FOAF)
    g.bind("rdfs", RDFS)
    g.bind("rdf", RDF)
    g.bind("course", course)
    g.bind("university", university)
    g.bind("wd", wd)
    g.bind("dp", dp)

    universityURI = URIRef(Literal("https://www.concordia.ca/"))
    g.add((universityURI, RDF.type, university.university))
    g.add((universityURI, university.Name, Literal("Concordia")))
    g.add((universityURI, university.WikidataEntry, dp.Concordia_University))
    g.add((universityURI, university.DBpediaEntry, wd.Q326342))
    g.add((universityURI, RDFS.label, Literal("university")))
    g.add((universityURI, RDFS.comment, Literal("A university.", lang='en')))

    googleURI = "http://google.com/"

    courseData = pd.read_csv(file_path_courses, encoding='utf-16')

    for index, row in courseData.iterrows():
        # Create courseURI instance of class course
        courseURI = URIRef(course + Literal(row["Subject"]) + Literal(row["Catalog"]))
        g.add((courseURI, RDF.type, course.course))
        # g.add((courseURI, RDFS.label, Literal("course")))
        # g.add((courseURI, RDFS.comment, Literal("A course offered by the university.", lang='en')))
        g.add((courseURI, course.courseName, Literal(row["Long Title"])))
        g.add((courseURI, course.courseSubject, Literal(row["Subject"])))
        g.add((courseURI, course.courseNumber, Literal(row["Catalog"])))
        g.add((courseURI, course.courseCredit, Literal(row["Class Units"], datatype=XSD.decimal)))
        g.add((courseURI, course.courseDescription, Literal(row["Component Descr"])))
        courseLink = URIRef(googleURI + Literal(row["Subject"]) + Literal(row["Catalog"]))
        g.add((courseURI, RDFS.seeAlso, courseLink))
        g.add((courseURI, course.offeredBy, universityURI))

    return g

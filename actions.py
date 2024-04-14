"""
TO DO:
EVERYTTHING
THIS IS JUST TESTING FOR NOW
NEED TO CONNECT TO FUSEKI FOR QUERY
"""
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rdflib import Graph, Namespace, Literal, URIRef


    









#Q1
class ActionListCoursesByUniversity(Action):
    def name(self) -> Text:
        #return "action_list_courses_by_university"
        return "utter_all_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        university_name = next(tracker.get_latest_entity_values("university_name"), None)
        
        if university_name:
            courses = self.execute_sparql_query_for_courses_by_university(university_name)
            if courses:
                dispatcher.utter_message(text=f"The courses offered by {university_name} are: {courses}")
            else:
                dispatcher.utter_message(text="Sorry, I couldn't find any courses offered by the specified university.")
        else:
            dispatcher.utter_message(text="Please provide a university name.")
        
        return []

    def execute_sparql_query_for_courses_by_university(self, university_name: Text) -> Text:
        with open("queries/q1.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{university_name}", university_name)
        
        
        
        
        # Execute SPARQL query to fetch courses offered by the specified university
        # Example:
        # result = execute_query("SELECT ?course WHERE { ... }")
        # courses = [row["course"] for row in result]
        # return ", ".join(courses)
        return "Course 1, Course 2, Course 3"  # Dummy data for demonstration







#Q2
class ActionCoursesByTopic(Action):
    def name(self) -> Text:
        return "utter_topic_discussed"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        topic = next(tracker.get_latest_entity_values("topic"), None)

        if topic:
            courses = self.execute_sparql_query_for_courses(topic)
            if courses:
                dispatcher.utter_message(text=f"The courses discussing {topic} are: {', '.join(courses)}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any courses discussing {topic}.")
        else:
            dispatcher.utter_message(text="Please provide the topic.")

        return []

    def execute_sparql_query_for_courses(self, topic: Text) -> List[Text]:
        with open("queries/q2.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{topic}", topic)
        
        # Execute SPARQL query to fetch courses discussing the specified topic
        # Example:
        # result = execute_query("SELECT ?courseName ?courseNumber WHERE { ... }")
        # courses = [(row["courseName"], row["courseNumber"]) for row in result]
        # return courses
        return ["Course A", "Course B", "Course C"]  # Dummy data for demonstration






#Q3
class ActionTopicsOfCourseLecture(Action):
    def name(self) -> Text:
        return "utter_topics_covered"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = next(tracker.get_latest_entity_values("course_name"), None)
        course_number = next(tracker.get_latest_entity_values("course_number"), None)
        lecture_number = next(tracker.get_latest_entity_values("lecture_number"), None)

        if course_name and course_number and lecture_number:
            topics = self.execute_sparql_query_for_topics(course_name, course_number, lecture_number)
            if topics:
                dispatcher.utter_message(text=f"The topics covered in {course_name} {course_number} during lecture {lecture_number} are: {', '.join(topics)}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any topics covered in {course_name} {course_number} during lecture {lecture_number}.")
        else:
            dispatcher.utter_message(text="Please provide the course name, course number, and lecture number.")

        return []

    def execute_sparql_query_for_topics(self, course_name: Text, course_number: Text, lecture_number: Text) -> List[Text]:
        with open("queries/q3.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{course_name}", course_name)
        sparql_query = sparql_query.replace("{course_number}", course_number)
        sparql_query = sparql_query.replace("{lecture_number}", lecture_number)
        # Execute SPARQL query to fetch topics covered during the specified lecture in the course
        # Example:
        # result = execute_query("SELECT ?topic WHERE { ... }")
        # topics = [row["topic"] for row in result]
        # return topics
        return ["Topic A", "Topic B", "Topic C"]







#Q4
class ActionCoursesByUniversityAndSubject(Action):
    def name(self) -> Text:
        return "utter_all_courses_of_subject"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        university_name = next(tracker.get_latest_entity_values("university_name"), None)
        subject = next(tracker.get_latest_entity_values("subject"), None)

        if university_name and subject:
            courses = self.execute_sparql_query_for_courses(university_name, subject)
            if courses:
                dispatcher.utter_message(text=f"The courses offered by {university_name} within {subject} are: {courses}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any courses offered by {university_name} within {subject}.")
        else:
            dispatcher.utter_message(text="Please provide both the university name and subject.")

        return []

    def execute_sparql_query_for_courses(self, university_name: Text, subject: Text) -> Text:
        with open("queries/q4.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{university_name}", university_name)
        sparql_query = sparql_query.replace("{subject}", subject)

        # Execute SPARQL query to fetch courses offered by the specified university within the subject
        # Example:
        # result = execute_query("SELECT ?course WHERE { ... }")
        # courses = [row["course"] for row in result]
        # return ", ".join(courses)
        return "Course 1, Course 2, Course 3"  # Dummy data for demonstration






#Q5
class ActionRecommendedMaterialsForTopic(Action):
    def name(self) -> Text:
        return "utter_recommended_materials"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        topic = next(tracker.get_latest_entity_values("topic"), None)
        course_name = next(tracker.get_latest_entity_values("course_name"), None)
        course_number = next(tracker.get_latest_entity_values("course_number"), None)

        if topic and course_name and course_number:
            materials = self.execute_sparql_query_for_recommended_materials(topic, course_name, course_number)
            if materials:
                dispatcher.utter_message(text=f"The recommended materials for studying {topic} in {course_name} {course_number} are: {materials}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any recommended materials for studying {topic} in {course_name} {course_number}.")
        else:
            dispatcher.utter_message(text="Please provide the topic, course name, and course number.")

        return []

    def execute_sparql_query_for_recommended_materials(self, topic: Text, course_name: Text, course_number: Text) -> Text:
        with open("queries/q5.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{topic}", topic)
        sparql_query = sparql_query.replace("{course_name}", course_name)
        sparql_query = sparql_query.replace("{course_number}", course_number)
        
        # Execute SPARQL query to fetch recommended materials for the specified topic in the course
        # Example:
        # result = execute_query("SELECT ?material WHERE { ... }")
        # materials = [row["material"] for row in result]
        # return ", ".join(materials)
        return "Recommended materials"  # Dummy data for demonstration










#Q6
class ActionCreditsForCourse(Action):
    def name(self) -> Text:
        return "utter_credits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = next(tracker.get_latest_entity_values("course_name"), None)
        course_number = next(tracker.get_latest_entity_values("course_number"), None)

        if course_name and course_number:
            credits = self.execute_sparql_query_for_credits(course_name, course_number)
            if credits is not None:
                dispatcher.utter_message(text=f"The number of credits for {course_name} {course_number} is: {credits}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find the number of credits for {course_name} {course_number}.")
        else:
            dispatcher.utter_message(text="Please provide both the course name and course number.")

        return []

    def execute_sparql_query_for_credits(self, course_name: Text, course_number: Text) -> Optional[int]:
        with open("queries/q6.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{course_name}", course_name)
        sparql_query = sparql_query.replace("{course_number}", course_number)

        # Execute SPARQL query to fetch the number of credits for the specified course
        # Example:
        # result = execute_query("SELECT ?credits WHERE { ... }")
        # credits = result[0]["credits"] if result else None
        # return credits
        return 3  # Dummy data for demonstration





#Q7
class ActionAdditionalResourcesForCourse(Action):
    def name(self) -> Text:
        return "utter_additional_resources"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_name = next(tracker.get_latest_entity_values("course_name"), None)
        course_number = next(tracker.get_latest_entity_values("course_number"), None)
        
        if course_name and course_number:
            resources = self.execute_sparql_query_for_additional_resources(course_name, course_number)
            if resources:
                dispatcher.utter_message(text=f"The additional resources available for {course_name} {course_number} are: {resources}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any additional resources for {course_name} {course_number}.")
        else:
            dispatcher.utter_message(text="Please provide both the course name and course number.")
        
        return []

    def execute_sparql_query_for_additional_resources(self, course_name: Text, course_number: Text) -> Text:
        with open("queries/q7.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{course_name}", course_name)
        sparql_query = sparql_query.replace("{course_number}", course_number)

        # Execute SPARQL query to fetch additional resources for the specified course
        # Example:
        # result = execute_query("SELECT ?resource WHERE { ... }")
        # resources = [row["resource"] for row in result]
        # return ", ".join(resources)
        return "Additional resources"  # Dummy data for demonstration










#Q8
class ActionContentForLecture(Action):
    def name(self) -> Text:
        return "utter_detail_content"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        lecture_number = next(tracker.get_latest_entity_values("lecture_number"), None)
        course_name = next(tracker.get_latest_entity_values("course_name"), None)
        course_number = next(tracker.get_latest_entity_values("course_number"), None)
        
        if lecture_number and course_name and course_number:
            content = self.execute_sparql_query_for_content(lecture_number, course_name, course_number)
            if content:
                dispatcher.utter_message(text=f"The content available for lecture {lecture_number} in {course_name} {course_number} is: {content}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any content for lecture {lecture_number} in {course_name} {course_number}.")
        else:
            dispatcher.utter_message(text="Please provide the lecture number, course name, and course number.")
        
        return []

    def execute_sparql_query_for_content(self, lecture_number: Text, course_name: Text, course_number: Text) -> Text:
        with open("queries/q8.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{lecture_number}", lecture_number)
        sparql_query = sparql_query.replace("{course_name}", course_name)
        sparql_query = sparql_query.replace("{course_number}", course_number)
        
        # Execute SPARQL query to fetch content for the specified lecture in the course
        # Example:
        # result = execute_query("SELECT ?content WHERE { ... }")
        # content = [row["content"] for row in result]
        # return ", ".join(content)
        return "Content from PDF files"  # Dummy data for demonstration






#Q9
class ActionReadingMaterials(Action):
    def name(self) -> Text:
        return "utter_reading_materials"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        topic = next(tracker.get_latest_entity_values("topic"), None)
        course_name = next(tracker.get_latest_entity_values("course_name"), None)
        course_number = next(tracker.get_latest_entity_values("course_number"), None)
        
        if topic and course_name and course_number:
            materials = self.execute_sparql_query_for_competencies(topic, course_name, course_number)
            if materials:
                dispatcher.utter_message(text=f"The competencies gained after completing {course_name} {course_number} are: {competencies}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any competencies for {course_name} {course_number}.")
        else:
            dispatcher.utter_message(text="Please provide both the course name and course number.")
        
        return []

    def execute_sparql_query_for_reading_materials(self, topic: Text, course_name: Text, course_number: Text) -> Text:
        with open("queries/q9.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{topic}", topic)
        sparql_query = sparql_query.replace("{course_name}", course_name)
        sparql_query = sparql_query.replace("{course_number}", course_number)
        # Execute SPARQL query to fetch reading materials for the specified topic in the course
        # Example:
        # result = execute_query("SELECT ?material WHERE { ... }")
        # materials = [row["material"] for row in result]
        # return ", ".join(materials)
        return "Lecture slides, Worksheets"  # Dummy data for demonstration









#Q10
class ActionCompetenciesForCourse(Action):
    def name(self) -> Text:
        return "utter_competencies_gained"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_name = next(tracker.get_latest_entity_values("course_name"), None)
        course_number = next(tracker.get_latest_entity_values("course_number"), None)
        
        if course_name and course_number:
            competencies = self.execute_sparql_query_for_competencies(course_name, course_number)
            if competencies:
                dispatcher.utter_message(text=f"The competencies gained after completing {course_name} {course_number} are: {competencies}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any competencies for {course_name} {course_number}.")
        else:
            dispatcher.utter_message(text="Please provide both the course name and course number.")
        
        return []

    def execute_sparql_query_for_competencies(self, course_name: Text, course_number: Text) -> Text:
        with open("queries/q10.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{course_name}", course_name)
        sparql_query = sparql_query.replace("{course_number}", course_number)
        # Execute SPARQL query to fetch competencies for the specified course
        # Example:
        # result = execute_query("SELECT ?competency WHERE { ... }")
        # competencies = [row["competency"] for row in result]
        # return ", ".join(competencies)
        return "Competency 1, Competency 2, Competency 3"  # Dummy data for demonstration






#Q11
class ActionGetGrades(Action):
    def name(self) -> Text:
        return "utter_grades"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        student_name = next(tracker.get_latest_entity_values("student_name"), None)
        student_id = next(tracker.get_latest_entity_values("student_id"), None)
        
        if student_name:
            grades = self.execute_sparql_query_for_grades_by_name(student_name)
        elif student_id:
            grades = self.execute_sparql_query_for_grades_by_id(student_id)
        else:
            dispatcher.utter_message(text="Please provide a student name or ID.")
            return []
        
        if grades:
            dispatcher.utter_message(text=f"The grades of {student_name} are: {grades}")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find grades for the specified student.")
        
        return []

    def execute_sparql_query_for_grades_by_name(self, student_name: Text) -> Text:
        with open("queries/q11.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{student_name}", student_name)
        # Execute SPARQL query to fetch grades for the specified student by name
        # Example:
        # result = execute_query("SELECT ?grade WHERE { ... }")
        # grades = [row["grade"] for row in result]
        # return ", ".join(grades)
        return "A, B, C"  # Dummy data for demonstration
    
    def execute_sparql_query_for_grades_by_id(self, student_id: Text) -> Text:
        with open("queries/q8.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{student_id}", student_id)
        # Execute SPARQL query to fetch grades for the specified student by ID
        # Example:
        # result = execute_query("SELECT ?grade WHERE { ... }")
        # grades = [row["grade"] for row in result]
        # return ", ".join(grades)
        return "A, B, C"  # Dummy data for demonstration






#Q12
class ActionStudentsCompletedCourse(Action):
    def name(self) -> Text:
        return "utter_students_completed_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_name = next(tracker.get_latest_entity_values("course_name"), None)
        course_number = next(tracker.get_latest_entity_values("course_number"), None)
        
        if course_name and course_number:
            students = self.execute_sparql_query_for_students_completed_course(course_name, course_number)
            if students:
                dispatcher.utter_message(text=f"The following students have completed {course_name} {course_number}: {students}")
            else:
                dispatcher.utter_message(text=f"Sorry, no students have completed {course_name} {course_number}.")
        else:
            dispatcher.utter_message(text="Please provide both the course name and course number.")
        
        return []

    def execute_sparql_query_for_students_completed_course(self, course_name: Text, course_number: Text) -> Text:
        with open("queries/q12.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{course_name}", course_name)
        sparql_query = sparql_query.replace("{course_number}", course_number)
        # Execute SPARQL query to fetch students who have completed the specified course
        # Example:
        # result = execute_query("SELECT ?student WHERE { ... }")
        # students = [row["student"] for row in result]
        # return ", ".join(students)
        return "Student 1, Student 2, Student 3"  # Dummy data for demonstration






#Q13
class ActionPrintTranscript(Action):
    def name(self) -> Text:
        #return "action_print_transcript"
        return "utter_transcript"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        student_name = next(tracker.get_latest_entity_values("student_name"), None)
        transcript = self.execute_sparql_query_for_transcript(student_name)
        
        if transcript:
            dispatcher.utter_message(text=f"Transcript for {student_name}:\n{transcript}")
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find a transcript for {student_name}.")
        
        return []

    def execute_sparql_query_for_transcript(self, student_name: Text, student_id: Text, transcript: Text) -> Text:
        with open("queries/q13.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{student_name}", student_name)
        sparql_query = sparql_query.replace("{student_id}", student_id)
        sparql_query = sparql_query.replace("{transcript}", transcript)
        # Execute SPARQL query to fetch transcript for the specified student
        # Example:
        # result = execute_query("SELECT ?course ?grade WHERE { ... }")
        # transcript = [(row["course"], row["grade"]) for row in result]
        # return "\n".join([f"{course}: {grade}" for course, grade in transcript])
        return "Course 1: A\nCourse 2: B\nCourse 3: C"  # Dummy data for demonstration





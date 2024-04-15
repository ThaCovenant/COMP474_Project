# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []



"""




{'head': {'vars': ['subject']}, 'results': {'bindings': [{'subject': {'type': 'uri', 'value': 'http://example.org/course/ACCO220'}}
TO DO:
NEED TO CONNECT TO FUSEKI FOR QUERY
TEST AND FIX
"""
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rdflib import Graph, Namespace, Literal, URIRef
import requests
    



#Q1
class ActionListCoursesByUniversity(Action):
    def name(self) -> Text:
        #return "action_list_courses_by_university"
        return "action_q1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #dispatcher.utter_message(text=f"The courses offered by {university_name}")

        #university_name = next(tracker.get_latest_entity_values("university_name"), None)
        university_name = tracker.get_slot("university_name")
        #print(university_name)
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
        sparql_query = sparql_query.replace("{university_name}", university_name.lower())

        print(sparql_query)
        fuseki_url = "http://localhost:3030/test/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        print(response)
        
        if response.status_code == 200:
            data = response.json()      #Response from the server in json format.
            # Extract and format results
            #results = "\n".join([f"{binding['course']['value']}" for binding in data['results']['bindings']])
            #return results
            subjects = [binding['subject']['value'].split('/')[-1] for binding in data['results']['bindings']]
            subjects_string = "\n".join(subjects)
            return subjects_string
            #return data
        else:
            return None
        





#Q2
class ActionCoursesByTopic(Action):
    def name(self) -> Text:
        return "action_q2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #topic = next(tracker.get_latest_entity_values("topic"), None)
        topic = tracker.get_slot("topic")

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
        

        fuseki_url = "http://localhost:3030/ds/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            #results = "\n".join([f"{binding['course_name']['value']}: {binding['course_id']['value']}" for binding in data['results']['bindings']])
            #return results
            return data
        else:
            return None






#Q3
class ActionTopicsOfCourseLecture(Action):
    def name(self) -> Text:
        return "action_q3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #course_name = next(tracker.get_latest_entity_values("course_name"), None)
        #course_number = next(tracker.get_latest_entity_values("course_number"), None)
        #lecture_number = next(tracker.get_latest_entity_values("lecture_number"), None)

        course = tracker.get_slot("course")
        lecture_number = tracker.get_slot("lecture_number")

        #if course_name and course_number and lecture_number:
        if course and lecture_number:
            #topics = self.execute_sparql_query_for_topics(course_name, course_number, lecture_number)
            topics = self.execute_sparql_query_for_topics(course, lecture_number)
            if topics:
                #dispatcher.utter_message(text=f"The topics covered in {course_name} {course_number} during lecture {lecture_number} are: {', '.join(topics)}")
                dispatcher.utter_message(text=f"The topics covered in {course} during lecture {lecture_number} are: {', '.join(topics)}")
            else:
                #dispatcher.utter_message(text=f"Sorry, I couldn't find any topics covered in {course_name} {course_number} during lecture {lecture_number}.")
                dispatcher.utter_message(text=f"Sorry, I couldn't find any topics covered in {course} during lecture {lecture_number}.")
        else:
            dispatcher.utter_message(text="Please provide the course name, course number, and lecture number.")

        return []

    #def execute_sparql_query_for_topics(self, course_name: Text, course_number: Text, lecture_number: Text) -> List[Text]:
    def execute_sparql_query_for_topics(self, course: Text, lecture_number: Text) -> List[Text]:
        with open("queries/q3.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        #sparql_query = sparql_query.replace("{course_name}", course_name)
        #sparql_query = sparql_query.replace("{course_number}", course_number)
        sparql_query = sparql_query.replace("{course}", course.upper())
        sparql_query = sparql_query.replace("{lecture_number}", lecture_number)

        fuseki_url = "http://localhost:3030/ds/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            #results = "\n".join([f"{binding['topic']['value']}" for binding in data['results']['bindings']])
            #return results
            return data
        else:
            return None





#Q4
class ActionCoursesByUniversityAndSubject(Action):
    def name(self) -> Text:
        return "action_q4"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #university_name = next(tracker.get_latest_entity_values("university_name"), None)
        #subject = next(tracker.get_latest_entity_values("subject"), None)

        university_name = tracker.get_slot("university_name")
        subject = tracker.get_slot("subject")


        if university_name and subject:
        #if university_name:
            courses = self.execute_sparql_query_for_courses(university_name, subject)
            #courses = self.execute_sparql_query_for_courses(university_name, subject)
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
        sparql_query = sparql_query.replace("{university_name}", university_name.lower())
        sparql_query = sparql_query.replace("{subject}", subject.upper())

        fuseki_url = "http://localhost:3030/ds/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            #results = "\n".join([f"{binding['course_name']['value']}: {binding['course_id']['value']}" for binding in data['results']['bindings']])
            #return results
            return data
        else:
            return None








#Q5
class ActionRecommendedMaterialsForTopic(Action):
    def name(self) -> Text:
        return "action_q5"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #topic = next(tracker.get_latest_entity_values("topic"), None)
        #course_name = next(tracker.get_latest_entity_values("course_name"), None)
        #course_number = next(tracker.get_latest_entity_values("course_number"), None)


        #topic = tracker.get_slot("topic")
        course = tracker.get_slot("course")

        #if topic and course_name and course_number:
        if course:
            #materials = self.execute_sparql_query_for_recommended_materials(topic, course_name, course_number)
            materials = self.execute_sparql_query_for_recommended_materials(course)
            if materials:
                #dispatcher.utter_message(text=f"The recommended materials for studying {topic} in {course_name} {course_number} are: {materials}")
                dispatcher.utter_message(text=f"The recommended materials for studying in {course} are: {materials}")
            else:
                #dispatcher.utter_message(text=f"Sorry, I couldn't find any recommended materials for studying {topic} in {course_name} {course_number}.")
                dispatcher.utter_message(text=f"Sorry, I couldn't find any recommended materials for studying in {course}.")
        else:
            dispatcher.utter_message(text="Please provide the topic, course name, and course number.")

        return []

    #def execute_sparql_query_for_recommended_materials(self, topic: Text, course_name: Text, course_number: Text) -> Text:
    def execute_sparql_query_for_recommended_materials(self, course: Text) -> Text:
        with open("queries/q5.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        #sparql_query = sparql_query.replace("{topic}", topic)
        #sparql_query = sparql_query.replace("{course_name}", course_name)
        #sparql_query = sparql_query.replace("{course_number}", course_number)

        sparql_query = sparql_query.replace("{course}", course.upper())

        fuseki_url = "http://localhost:3030/ds/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            #results = "\n".join([f"{binding['slides']['value']}: {binding['worksheets']['value']}" for binding in data['results']['bindings']])
            #results = "\n".join([f"{binding['material']['value']}" for binding in data['results']['bindings']])
            #return results
            return data
        else:
            return None
        











#Q6
class ActionCreditsForCourse(Action):
    def name(self) -> Text:
        return "action_q6"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        course = tracker.get_slot("course")

        #if course_name and course_number:
        if course:
            #credits = self.execute_sparql_query_for_credits(course_name, course_number)
            credits = self.execute_sparql_query_for_credits(course)
            if credits is not None:
                #dispatcher.utter_message(text=f"The number of credits for {course_name} {course_number} is: {credits}")
                dispatcher.utter_message(text=f"The number of credits for {course} is: {credits}")
            else:
                #dispatcher.utter_message(text=f"Sorry, I couldn't find the number of credits for {course_name} {course_number}.")
                dispatcher.utter_message(text=f"Sorry, I couldn't find the number of credits for {course}.")
        else:
            dispatcher.utter_message(text="Please provide both the course name and course number.")

        return []

    #def execute_sparql_query_for_credits(self, course_name: Text, course_number: Text) -> Optional[int]:
    def execute_sparql_query_for_credits(self, course: Text) -> Optional[int]:
        with open("queries/q6.txt", "r") as file:
            sparql_query = file.read()


        sparql_query = sparql_query.replace("{course}", course.upper())

        fuseki_url = "http://localhost:3030/ds/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            #results = "\n".join([f"{binding['credits']['value']}" for binding in data['results']['bindings']])
            #return results
            return data
        else:
            return None





#Q7
class ActionAdditionalResourcesForCourse(Action):
    def name(self) -> Text:
        return "action_q7"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        course = tracker.get_slot("course")
        
        #if course_name and course_number:
        if course:
            #resources = self.execute_sparql_query_for_additional_resources(course_name, course_number)
            resources = self.execute_sparql_query_for_additional_resources(course)
            if resources:
                #dispatcher.utter_message(text=f"The additional resources available for {course_name} {course_number} are: {resources}")
                dispatcher.utter_message(text=f"The additional resources available for {course} are: {resources}")
            else:
                #dispatcher.utter_message(text=f"Sorry, I couldn't find any additional resources for {course_name} {course_number}.")
                dispatcher.utter_message(text=f"Sorry, I couldn't find any additional resources for {course}.")
        else:
            dispatcher.utter_message(text="Please provide both the course name and course number.")
        
        return []

    #def execute_sparql_query_for_additional_resources(self, course_name: Text, course_number: Text) -> Text:
    def execute_sparql_query_for_additional_resources(self, course: Text) -> Text:
        with open("queries/q7.txt", "r") as file:
            sparql_query = file.read()


        sparql_query = sparql_query.replace("{course}", course.upper)


        fuseki_url = "http://localhost:3030/ds/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            #results = "\n".join([f"{binding['link']['value']}" for binding in data['results']['bindings']])
            #return results
            return data
        else:
            return None











#Q8
class ActionContentForLecture(Action):
    def name(self) -> Text:
        return "action_q8"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #lecture_number = next(tracker.get_latest_entity_values("lecture_number"), None)
        #course_name = next(tracker.get_latest_entity_values("course_name"), None)
        #course_number = next(tracker.get_latest_entity_values("course_number"), None)

        lecture_number = tracker.get_slot("lecture_number")
        course = tracker.get_slot("course")
        
        #if lecture_number and course_name and course_number:
        if lecture_number and course:
            #content = self.execute_sparql_query_for_content(lecture_number, course_name, course_number)
            content = self.execute_sparql_query_for_content(lecture_number, course)
            if content:
                #dispatcher.utter_message(text=f"The content available for lecture {lecture_number} in {course_name} {course_number} is: {content}")
                dispatcher.utter_message(text=f"The content available for lecture {lecture_number} in {course} is: {content}")
            else:
                #dispatcher.utter_message(text=f"Sorry, I couldn't find any content for lecture {lecture_number} in {course_name} {course_number}.")
                dispatcher.utter_message(text=f"Sorry, I couldn't find any content for lecture {lecture_number} in {course}.")
        else:
            dispatcher.utter_message(text="Please provide the lecture number, course name, and course number.")
        
        return []

    #def execute_sparql_query_for_content(self, lecture_number: Text, course_name: Text, course_number: Text) -> Text:
    def execute_sparql_query_for_content(self, lecture_number: Text, course: Text) -> Text:
        with open("queries/q8.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{lecture_number}", lecture_number)
        sparql_query = sparql_query.replace("{course}", course.upper())

        
        fuseki_url = "http://localhost:3030/ds/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            #results = "\n".join([f"{binding['lecture']['value']}: {binding['material']['value']}" for binding in data['results']['bindings']])
            #return results
            return data
        else:
            return None
        







#Q9
class ActionReadingMaterials(Action):
    def name(self) -> Text:
        return "action_q9"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #topic = next(tracker.get_latest_entity_values("topic"), None)
        #course_name = next(tracker.get_latest_entity_values("course_name"), None)
        #course_number = next(tracker.get_latest_entity_values("course_number"), None)

        
        course = tracker.get_slot("course")

        
        #if topic and course_name and course_number:
            #materials = self.execute_sparql_query_for_competencies(topic, course_name, course_number)
        if course:
            materials = self.execute_sparql_query_for_competencies(course)
            if materials:
                #dispatcher.utter_message(text=f"The competencies gained after completing {course_name} {course_number} are: {competencies}")
                dispatcher.utter_message(text=f"The competencies gained after completing {course} are: {competencies}")
            else:
                #dispatcher.utter_message(text=f"Sorry, I couldn't find any competencies for {course_name} {course_number}.")
                dispatcher.utter_message(text=f"Sorry, I couldn't find any competencies for {course}.")
        else:
            dispatcher.utter_message(text="Please provide both the course name and course number.")
        
        return []

    #def execute_sparql_query_for_reading_materials(self, topic: Text, course_name: Text, course_number: Text) -> Text:
    def execute_sparql_query_for_reading_materials(self, course: Text) -> Text:
        with open("queries/q9.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        #sparql_query = sparql_query.replace("{topic}", topic)
        #sparql_query = sparql_query.replace("{course_name}", course_name)
        #sparql_query = sparql_query.replace("{course_number}", course_number)
        
        sparql_query = sparql_query.replace("{course}", course.upper())




        fuseki_url = "http://localhost:3030/ds/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            #results = "\n".join([f"{binding['topic']['value']}: {binding['material']['value']}" for binding in data['results']['bindings']])
            #return results
            return data
        else:
            return None










#Q10
class ActionCompetenciesForCourse(Action):
    def name(self) -> Text:
        return "action_q10"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        course = tracker.get_slot("course")
        
        #if course_name and course_number:
        #    competencies = self.execute_sparql_query_for_competencies(course_name, course_number)
        if course:
            competencies = self.execute_sparql_query_for_competencies(course)
            if competencies:
                #dispatcher.utter_message(text=f"The competencies gained after completing {course_name} {course_number} are: {competencies}")
                dispatcher.utter_message(text=f"The competencies gained after completing {course} are: {competencies}")
            else:
                #dispatcher.utter_message(text=f"Sorry, I couldn't find any competencies for {course_name} {course_number}.")
                dispatcher.utter_message(text=f"Sorry, I couldn't find any competencies for {course}.")
        else:
            dispatcher.utter_message(text="Please provide both the course name and course number.")
        
        return []

    #def execute_sparql_query_for_competencies(self, course_name: Text, course_number: Text) -> Text:
    def execute_sparql_query_for_competencies(self, course: Text) -> Text:
        with open("queries/q10.txt", "r") as file:
            sparql_query = file.read()


        sparql_query = sparql_query.replace("{course}", course.upper())



        fuseki_url = "http://localhost:3030/ds/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            #results = "\n".join([f"{binding['topic']['value']}" for binding in data['results']['bindings']])
            #return results
            return data
        else:
            return None





#Q11
class ActionGetGrades(Action):
    def name(self) -> Text:
        return "action_q11"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #student_name = next(tracker.get_latest_entity_values("student_name"), None)
        #student_id = next(tracker.get_latest_entity_values("student_id"), None)

        student_id = tracker.get_slot("student_id")
        course = tracker.get_slot("course")

        
        if student_id and course:
            grades = self.execute_sparql_query_for_grades_by_name(student_id, course)
            if grades:
                dispatcher.utter_message(text=f"The grades of {student_id} are: {grades}")
            else:
                dispatcher.utter_message(text="Sorry, I couldn't find grades for the specified student.")
        #elif student_id:
        #    grades = self.execute_sparql_query_for_grades_by_id(student_id)
        else:
            dispatcher.utter_message(text="Please provide a student ID and course.")
        
        #if grades:
        #    dispatcher.utter_message(text=f"The grades of {student_name} are: {grades}")
        #else:
        #    dispatcher.utter_message(text="Sorry, I couldn't find grades for the specified student.")
        
        return []

 
    
    def execute_sparql_query_for_grades_by_id(self, student_id: Text, course: Text) -> Text:
        with open("queries/q11.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{student_id}", student_id)
        sparql_query = sparql_query.replace("{course}", course.upper())





        fuseki_url = "http://localhost:3030/ds/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            #results = "\n".join([f"{binding['student_id']['value']}: {binding['grade']['value']}" for binding in data['results']['bindings']])
            #return results
            return data
        else:
            return None







#Q12
class ActionStudentsCompletedCourse(Action):
    def name(self) -> Text:
        return "action_q12"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course = tracker.get_slot("course")
        
        if course and course:
            students = self.execute_sparql_query_for_students_completed_course(course)
            if students:
                dispatcher.utter_message(text=f"The following students have completed {course}: {students}")
            else:
                dispatcher.utter_message(text=f"Sorry, no students have completed {course}.")
        else:
            dispatcher.utter_message(text="Please provide both the course name and course number.")
        
        return []

    def execute_sparql_query_for_students_completed_course(self, course: Text) -> Text:
        with open("queries/q12.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{course}", course.upper())

        fuseki_url = "http://localhost:3030/ds/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            #results = "\n".join([f"{binding['student_id']['value']}" for binding in data['results']['bindings']])
            #return results
            return data
        else:
            return None


    

        






#Q13
"""
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


        #return "Course 1: A\nCourse 2: B\nCourse 3: C"  # Dummy data for demonstration
"""



class ActionPrintTranscript(Action):
    def name(self) -> Text:
        return "action_q13"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #student_name = next(tracker.get_latest_entity_values("student_name"), None)
        #
        student_id = tracker.get_slot("student_id")

        if student_id:
            transcript = self.execute_sparql_query_for_transcript(student_id)
            if transcript:
                dispatcher.utter_message(text=f"Transcript for {student_id}:\n{transcript}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find a transcript for {student_id}.")
        else:
            dispatcher.utter_message(text=f"Sorry, please provide a correct student ID.")

        return []

    def execute_sparql_query_for_transcript(self, student_id: Text) -> Text:
        with open("queries/q13.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{student_id}", student_id)

        fuseki_url = "http://localhost:3030/ds/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            #results = "\n".join([f"{binding['course']['value']}: {binding['grade']['value']}" for binding in data['results']['bindings']])
            #return results
            return data
        else:
            return None




#Query 14
class ActionPrintTranscript(Action):
    def name(self) -> Text:
        return "action_q14"

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

    def execute_sparql_query_for_transcript(self, student_name: Text) -> Text:
        with open("queries/q13.txt", "r") as file:
            sparql_query = file.read()

        # Replace placeholders in the query with actual values
        sparql_query = sparql_query.replace("{student_name}", student_name)

        fuseki_url = "http://localhost:3030/ds/query"  # Adjust the endpoint URL accordingly
        response = requests.post(fuseki_url, data={'query': sparql_query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            results = "\n".join([f"{binding['course']['value']}: {binding['grade']['value']}" for binding in data['results']['bindings']])
            return results
        else:
            return None


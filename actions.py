"""
TO DO:
EVERYTTHING
THIS IS JUST TESTING FOR NOW
"""
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetGrades(Action):
    def name(self)  -> Text:
        return"action_get_grades"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any])    -> List[Dict[Text, Any]]:
        
        student_name = tracker.get_slot("student_name")
        grades = self.fetch_grades(student_name)

        if grades:
            dispatcher.utter_message(template="utter_grades", student_name=student_name, grades=grades)
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find grades for {}.".format(student_name))
        return []
    
    def fetch_grades(self, student_name: Text) -> Text:
        return "A, B, C"






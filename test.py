pip install rasa
rasa init --no-prompt
rasa train
rasa shell
rasa run actions --debug
rasa interactive

class QueryFuseki(Action):
    def name(self) -> Text:
        return "action_query_fuseki"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        query = """
            PREFIX rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns
            PREFIX foaf: http://xmlns.com/foaf/0.1/
            SELECT ?name ?age
            WHERE {
                ?person foaf:name ?name .
                ?person foaf:age ?age .
            }
        """

        fuseki_url = "http://localhost:3030/"
        response = requests.post(fuseki_url, data={'query': query})

        if response.status_code == 200:
            data = response.json()
            # Extract and format results
            results = [(binding['name']['value'], binding['age']['value']) for binding in data['results']['bindings']]
            dispatcher.utter_message("Here are the results: {}".format(results))
        else:
            dispatcher.utter_message("Failed to query Fuseki server.")

        return []
    


import requests
from typing import List, Dict, Text, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionPrintTranscript(Action):
    def name(self) -> Text:
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
        







        






class ActionPrintTranscript(Action):
    def name(self) -> Text:
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
# COMP474_Project
Build an intelligent agent that can answer university course and student related questions, using a knowledge graph and natural language processing

## describe each file
- RDFs: contains all the schemas   
- Triples folder: contains generated and written Triples
- data folder: contains courseMaterial and students_grades.csv
- courseMaterial folder: contains COMP335 and COMP474 folders
- COMP335 folders: contains Lectures, Worksheet, Assignments
- COMP474 folders: contains Lectures, Worksheet
- Roboprof.py: main file calls functions from AutomatedKnowledgeBaseConstruction.py.
- AutomatedKnowledgeBaseConstruction.py: contains all the functions necessary to run this project such as building the Knowledge Base and selecting the right query to create outut files.
- Queries folder holds each query as required in the project in separate files.
- Data holds course materials, Concordia's datasets and students data.

## steps to execute code for building knowledge base
- Run the "Roboprof.py" file


## steps to setup Fuseki Jena
- Run the exe file for the server.
- Upload dataset from project to the server. Dataset can befound in folder Triples>MergedTriples.ttl

## steps to execute RASA chatbot
- In terminal, enter "rasa train" to train the model.
- In another terminal enter "rasa run actions"
- Enter "rasa shell" to start communicating with the chatbot.



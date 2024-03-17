import rdflib
import csv

from rdflib.namespace import FOAF

g1 = rdflib.Graph()
g2 = rdflib.Graph()
g3 = rdflib.Graph()
g4 = rdflib.Graph()
g5 = rdflib.Graph()

file_path1 = "Turtles/Courses.ttl"
file_path2 = "Turtles/Lectures.ttl"
file_path3 = "Turtles/Student_Schema.ttl"
file_path4 = "Turtles/Topics.ttl"
file_path5 = "Turtles/University_Schema.ttl"
file_path6 = "Turtles/Merged.ttl"

g1.parse(file_path1, format="ttl")
g2.parse(file_path2, format="ttl")
g3.parse(file_path3, format="ttl")
g4.parse(file_path4, format="ttl")
g5.parse(file_path4, format="ttl")

# Print the number of triples in the graph
print(len(g1))
print(len(g2))
print(len(g3))
print(len(g4))
print(len(g5))

# Loop through each triple in the graph (subj, pred, obj)
#for s, p, o in g1:
    # Print the subject, predicate and the object
#    print(s, p, o)

#print(g1.serialize(format='turtle'))
#print(g2.serialize(format='turtle'))
#print(g3.serialize(format='turtle'))
#print(g4.serialize(format='turtle'))
#print(g5.serialize(format='turtle'))

g6 = g1 + g2 + g3 + g4 + g5
#print(len(g6))

# Write the merged graph to a file in Turtle format
with open(file_path6, "w", encoding="utf-8") as f:
    f.write(g6.serialize(format="turtle"))


# Open the CSV file
with open('CU_SR_OPEN_DATA_CATALOG.csv', newline='') as csvfile:
    # Create a CSV reader object
    reader = csv.reader(csvfile)

    # Iterate over each row in the CSV file
    for row in reader:
        # Access elements of each row by index
        print(row)





# Which city is Joe studying in? First define the namespaces:
#user = rdflib.Namespace("http://example.org/")
#wdt = rdflib.Namespace("http://www.wikidata.org/prop/direct/")

# Find the university where Joe studies
#for uni in g.objects(subject=user.joe, predicate=user.studiesAt):
    # Find the city where this university is located using Wikidata Property:P276
#    for city in g.objects(subject=uni, predicate=wdt.P276):
#        print(f"Joe studies in the city: {city}")
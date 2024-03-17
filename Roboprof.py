import rdflib
from rdflib.namespace import FOAF

g1 = rdflib.Graph()

g1.parse("http://www.wikidata.org/entity/Q326342.ttl")
# Print the number of triples in the graph g1
print(len(g1))

g2 = rdflib.Graph()

# Load the local graph create above
g2.parse("triples.ttl", format="turtle")

# Print the number of triples in the graph g2
print(len(g2))

# Merge (union) the two graphs
g = g1 + g2

# Print the total number of triples present in the merged graph
print(len(g))

# Write the merged graph to a file in Turtle format
with open("Newtriples.ttl", "w", encoding="utf-8") as f:
    f.write(g.serialize(format="turtle"))



# Which city is Joe studing in? First define the namespaces:
user = rdflib.Namespace("http://example.org/")
wdt = rdflib.Namespace("http://www.wikidata.org/prop/direct/")

# Find the university where Joe studies
for uni in g.objects(subject=user.joe, predicate=user.studiesAt):
    # Find the city where this university is located using Wikidata Property:P276
    for city in g.objects(subject=uni, predicate=wdt.P276):
        print(f"Joe studies in the city: {city}")

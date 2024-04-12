from rdflib import URIRef, Graph, Literal, Namespace, RDF, FOAF, RDFS, XSD

# Command to create user defined namespaces
namespaces = {
    'kb': Namespace("http://example.org/knowledge-base#"),
    'student': Namespace("http://example.org/student/"),
    'course': Namespace("http://example.org/course/"),
    'lecture': Namespace("http://example.org/lecture/"),
    'slides': Namespace("http://example.org/slides/"),
    'lectureContent': Namespace("http://example.org/lectureContent/"),
    'worksheets': Namespace("http://example.org/worksheets/"),
    'other': Namespace("http://example.org/other/"),
    'readings': Namespace("http://example.org/readings/"),
    'assignments': Namespace("http://example.org/assignments/"),
    'completedCourse': Namespace("http://example.org/completedCourse/"),
    'topic': Namespace("http://example.org/topic/"),
    'university': Namespace("https://www.wikidata.org/entity/Q3918"),
    'wd': Namespace("https://www.wikidata.org/wiki/"),
    'dp': Namespace("http://dbpedia.org/resource/"),
    'google': Namespace("http://google.com/")
}


# Bind namespaces
def bind_namespaces(graph):
    for prefix, ns in namespaces.items():
        graph.bind(prefix, ns)


# Initialize RDF graph
def init_graph():
    graph = Graph()
    bind_namespaces(graph)
    return graph


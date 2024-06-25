from rdflib import Graph, Namespace


CUBE = Namespace("https://cube.link/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
DCT = Namespace("http://purl.org/dc/terms/")
SCHEMA = Namespace("http://schema.org/")
SH = Namespace("http://www.w3.org/ns/shacl#")


Namespaces = {
    "cube": CUBE,
    "dcat": DCAT,
    "dct": DCT,
    "schema": SCHEMA
}


def bind_namespaces(graph: Graph) -> Graph:
    for prefix, nmspc in Namespaces.items():
        graph.bind(prefix=prefix, namespace=nmspc)
    return graph

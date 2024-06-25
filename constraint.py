from rdflib import Graph, Literal, RDF, XSD, URIRef
import yaml
from namespaces import bind_namespaces, CUBE, SH


class Constraint:
    _graph: Graph
    _dict: dict
    _shape_uri: URIRef


    def __init__(self, yml: str):
        with open(yml, "rt", encoding="utf-8") as yml_input:
            self._dict = yaml.load(yml_input, yaml.Loader)
        self._shape_uri = URIRef(self._dict.get("shape-URI"))
        self._setup_constraint()
        self.serialize(path="constraint.ttl")


    def serialize(self, path: str):
        self._graph.serialize(destination=path, format="turtle", encoding="utf-8")
    
    def _setup_constraint(self) -> Graph:
        graph = Graph()
        graph = bind_namespaces(graph=graph)
        self._graph = graph
        self._add(s=self._shape_uri, p=RDF.type, o=CUBE.ObservationConstraint)
        self._add(s=self._shape_uri, p=SH.closed, o=Literal(True, datatype=XSD.boolean))

        
    def _add(self, s: URIRef, p: URIRef, o: URIRef | Literal):
        self._graph.add((s, p, o))

if __name__ == "__main__":
    constraint = Constraint(yml="shape_Form.yml")

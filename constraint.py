from rdflib import BNode, Graph, Literal, RDF, XSD, URIRef
import yaml
from namespaces import bind_namespaces, CUBE, QUDT, SCHEMA, SH


class Constraint:
    _graph: Graph
    _dict: dict
    _shape_uri: URIRef


    def __init__(self, yml: str):
        with open(yml, "rt", encoding="utf-8") as yml_input:
            self._dict = yaml.load(yml_input, yaml.Loader)
        self._shape_uri = URIRef(self._dict.get("shape-URI"))
        self._setup_constraint()
        self._construct_shape()
        self.serialize(path="constraint.ttl")


    def serialize(self, path: str):
        self._graph.serialize(destination=path, format="turtle", encoding="utf-8")

    def _construct_shape(self):
        for dim_dict in self._dict.get("dimensions"):
            bnode = BNode()
            self._add(self._shape_uri, SH.property, bnode)
            self._construct_dimension(bnode, dim_dict)

    def _construct_dimension(self, dim_node: BNode, dim_dict: dict):
        # Dimension type
        match dim_dict.get("dimension-type"):
            case "Key Dimension":
                # Key Dimension: expect an IRI
                self._add(dim_node, RDF.type, CUBE.KeyDimension)
                self._add(dim_node, SH.nodeKind, SH.IRI)
            case "Measure Dimension":
                # todo: min and max construction
                self._add(dim_node, RDF.type, CUBE.MeasureDimension)
            case "Error Dimension":
                # todo: implementation
                exit

        # Name and description
        for lang, name in dim_dict.get("name").items():
            self._add(dim_node, SCHEMA.name, Literal(name, lang=lang))
        for lang, desc in dim_dict.get("description").items():
            self._add(dim_node, SCHEMA.description, Literal(desc, lang=lang))

        # Min and Max Count
        self._add(dim_node, SH.maxCount, Literal(1))
        self._add(dim_node, SH.minCount, Literal(1))

        # Scale Type
        match dim_dict.get("scale-type"):
            case "ratio":
                self._add(dim_node, QUDT.scaleType, QUDT.RatioScale)
            case "interval":
                self._add(dim_node, QUDT.scaleType, QUDT.IntervalScale)
            case "ordinal":
                self._add(dim_node, QUDT.scaleType, QUDT.OrdinalScale)
            case "nominal":
                self._add(dim_node, QUDT.scaleType, QUDT.NominalScale)
            case _:
                exit
    
    def _setup_constraint(self) -> Graph:
        graph = Graph()
        graph = bind_namespaces(graph=graph)
        self._graph = graph
        self._add(self._shape_uri, RDF.type, CUBE.ObservationConstraint)
        self._add(self._shape_uri, RDF.type, SH.NodeShape)
        self._add(self._shape_uri, SH.closed, Literal(True, datatype=XSD.boolean))

        
    def _add(self, s: URIRef, p: URIRef, o: URIRef | Literal | BNode):
        self._graph.add((s, p, o))

if __name__ == "__main__":
    constraint = Constraint(yml="shape_Form.yml")

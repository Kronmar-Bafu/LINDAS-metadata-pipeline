from rdflib import BNode, Graph, Literal, RDF, XSD, URIRef
import yaml
from namespaces import bind_namespaces, CUBE, META, QUDT, SCHEMA, SH, TIME, UNIT


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
        order = 1
        for dim_dict in self._dict.get("dimensions"):
            bnode = BNode()
            self._add(self._shape_uri, SH.property, bnode)
            self._construct_dimension(bnode, dim_dict, order=order)
            order += 1

    def _construct_dimension(self, dim_node: BNode, dim_dict: dict, order: int):
        # Dimension type
        match dim_dict.get("dimension-type"):
            case "Key Dimension":
                # Key Dimension: expect an IRI
                self._add(dim_node, RDF.type, CUBE.KeyDimension)
                self._add(dim_node, SH.nodeKind, SH.IRI)
            case "Measure Dimension":
                # todo: min and max construction
                self._add(dim_node, RDF.type, CUBE.MeasureDimension)
                self._add(dim_node, SH.nodeKind, SH.Literal)
                unit_iri = self._get_unit_iri(unit = dim_dict.get("unit"))
                self._add(dim_node, QUDT.hasUnit, unit_iri)
            case "Error Dimension":
                # todo: implementation
                pass

        # Name and description
        for lang, name in dim_dict.get("name").items():
            self._add(dim_node, SCHEMA.name, Literal(name, lang=lang))
        for lang, desc in dim_dict.get("description").items():
            self._add(dim_node, SCHEMA.description, Literal(desc, lang=lang))

        # Min-, Max-count and order
        self._add(dim_node, SH.maxCount, Literal(1))
        self._add(dim_node, SH.minCount, Literal(1))
        self._add(dim_node, SH.order, Literal(order))

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
        
        # Path
        self._add(dim_node, SH.path, URIRef(dim_dict.get("path")))

        # optional 
        if "data-kind" in dim_dict.keys():
            kind_node = BNode()
            self._add(dim_node, META.dataKind, kind_node)
            self._construct_data_kind(kind_node, dim_dict.get("data-kind"))
    
    @staticmethod
    def _get_unit_iri(unit: str) -> URIRef:
        match unit:
            case "percent":
                return UNIT.PERCENT
    
    def _construct_data_kind(self, kind_node: BNode, kind_dict: dict):
        match kind_dict.get("type"):
            case "temporal":
                self._add(kind_node, RDF.type, TIME.GeneralDateTimeDescription)
                match kind_dict.get("unit"):
                    case "second":
                        self._add(kind_node, TIME.unitType, TIME.unitSecond)
                    case "minute":
                        self._add(kind_node, TIME.unitType, TIME.unitMinute)
                    case "hour":
                        self._add(kind_node, TIME.unitType, TIME.unitHour)
                    case "day":
                        self._add(kind_node, TIME.unitType, TIME.unitDay)
                    case "week":
                        self._add(kind_node, TIME.unitType, TIME.unitWeek)
                    case "month":
                        self._add(kind_node, TIME.unitType, TIME.unitMonth)
                    case "year":
                        self._add(kind_node, TIME.unitType, TIME.unitYear)
                    case _:
                        exit
            case "spatial":
                self._add(kind_node, RDF.type, SCHEMA.GeoShape)
                    

    
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

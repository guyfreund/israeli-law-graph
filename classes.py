from constants import XML_NAMESPACE, EdgeType
import xml.etree.ElementTree as ET


class Graph(object):
    def __init__(self, vertexes, edges):
        self.V: set[Vertex] = vertexes
        self.E: set[Edge] = edges


class Edge(object):
    def __init__(self, from_vertex, to_vertex):
        self.from_vertex: Vertex = from_vertex
        self.to_vertex: Vertex = to_vertex
        self.type: str = self.classify_edge_type(self.from_vertex, self.to_vertex)

    def __eq__(self, other):
        return all([
            self.type == other.type,
            self.from_vertex == other.from_vertex,
            self.to_vertex == other.to_vertex
        ])

    def __hash__(self):
        return hash((self.from_vertex, self.to_vertex, self.type))

    @staticmethod
    def classify_edge_type(from_vertex, to_vertex):
        return EdgeType.Generic


class Vertex(object):
    def __init__(self, law_path, element):
        self.law_path: str = law_path
        self.element: ET.Element = element
        self.in_edges: set[Edge] = set()
        self.out_edges: set[Edge] = set()

    def __eq__(self, other):
        return all([
            self.law_path == other.law_path,
            self.element.attrib == other.element.attrib,
            self.element.text == other.element.text,
            self.element.tag == other.element.tag,
            self.element.tail == other.element.tail
        ])

    def __hash__(self):
        return hash((self.law_path, str(self.element.attrib), self.element.tail, self.element.text, self.element.tag))

    def add_in_edge(self, edge):
        self.in_edges.add(edge)

    def add_out_edge(self, edge):
        self.out_edges.add(edge)


class Law(Vertex):
    def __init__(self, path):
        tree: ET.ElementTree = ET.parse(path)
        root: ET.Element = tree.getroot()
        super().__init__(law_path=path, element=root)
        self.path: str = path
        self.tree: ET.ElementTree = tree
        self.root: ET.Element = root
        frbr_work_uri: str = self.root.find(f'.//{XML_NAMESPACE}FRBRWork').find(f'.//{XML_NAMESPACE}FRBRuri').attrib['value']
        self.frbr_work_uri: str = frbr_work_uri[1:] if frbr_work_uri.startswith('/') else frbr_work_uri
        self.title: str = self.root.find(f'.//{XML_NAMESPACE}body').find(f'./{XML_NAMESPACE}title') \
            .find(f'./{XML_NAMESPACE}content').find(f'./{XML_NAMESPACE}p').text
        self.hrefs: list = self.get_ref_elements()
        self.parent_map: dict = {c: p for p in self.tree.iter() for c in p}

    def get_ref_elements(self):
        return self.root.findall(f'.//{XML_NAMESPACE}ref')


class Chapter(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law


class Point(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law


class Section(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law


class Part(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law


class Appendix(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law


class Preamble(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law


class Subtitle(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law


class WrapUp(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law

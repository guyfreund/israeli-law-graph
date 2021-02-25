from constants import XML_NAMESPACE, EdgeType, ANCESTOR_TAGS, Tag

import xml.etree.ElementTree as ET


class Graph(object):
    """ A class used to represent a Graph """
    def __init__(self, vertexes, edges):
        self.V: set[Vertex] = vertexes
        self.E: set[Edge] = edges


class Edge(object):
    """ A class used to represent an Edge """
    def __init__(self, from_vertex, to_vertex, ref):
        self.from_vertex: Vertex = from_vertex
        self.to_vertex: Vertex = to_vertex
        self.ref = ref
        self.type: str = self.classify_edge_type(self.from_vertex, self.to_vertex)

    def __eq__(self, other):
        return all([
            self.type == other.type,
            self.ref.tag == other.ref.tag,
            self.ref.attrib == other.ref.attrib,
            self.ref.text == other.ref.text,
            self.ref.tail == other.ref.tail,
            self.from_vertex == other.from_vertex,
            self.to_vertex == other.to_vertex
        ])

    def __hash__(self):
        return hash((
            self.from_vertex, self.to_vertex, self.type, self.ref.tag, str(self.ref.attrib), self.ref.text,
            self.ref.tail
        ))

    @staticmethod
    def classify_edge_type(from_vertex, to_vertex):
        return EdgeType.Generic


class Vertex(object):
    """ A class used to represent a Vertex """
    def __init__(self, law_path, element):
        self.law_path: str = law_path
        self.element: ET.Element = element
        self.in_edges: set[Edge] = set()
        self.out_edges: set[Edge] = set()
        self.unique = str()
        self.children_unique = str()
        self.parent_unique = str()
        self.tag = 'Vertex'

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
    """ A class used to represent a Law """
    def __init__(self, path):
        tree: ET.ElementTree = ET.parse(path)
        root: ET.Element = tree.getroot()
        super().__init__(law_path=path, element=root)
        self.tag = Tag.Law
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

    def get_path_from_root(self, element):
        path = element.tag.replace(XML_NAMESPACE, '')
        parent = self.parent_map.get(element)
        while parent:
            if parent.tag in ANCESTOR_TAGS:
                path = f"{parent.tag.replace(XML_NAMESPACE, '')} eId={parent.attrib['eId']}/{path}"
            else:
                path = f"{parent.tag.replace(XML_NAMESPACE, '')}/{path}"
            parent = self.parent_map.get(parent)
        return path


class Chapter(Vertex):
    """ A class used to represent a Chapter in a Law """
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Chapter

        # hashing fields
        self.unique = element.find(f'.//{XML_NAMESPACE}title').find(f'.//{XML_NAMESPACE}content').find(f'.//{XML_NAMESPACE}p').text
        self.children_unique = [f'{c.attrib}{c.text}{c.tag}{c.tail}' for c in element.iter()]
        self.parent = law.parent_map.get(element)
        self.g_parent = law.parent_map.get(self.parent)
        self.index_in_g_parent = [c for c in self.g_parent].index(self.parent) if self.g_parent else -1
        self.index_in_parent = [c for c in self.parent].index(element)
        self.parent_unique = f'{self.parent.attrib}{self.parent.text}{self.parent.tag}{self.parent.tail}' \
                             f'{self.index_in_parent}{self.index_in_g_parent}'

    def __eq__(self, other):
        return all([
            self.law_path == other.law_path,
            self.parent_unique == other.parent_unique,
            self.children_unique == other.children_unique,
            self.unique == other.unique,
            self.element.attrib == other.element.attrib,
            self.element.text == other.element.text,
            self.element.tag == other.element.tag,
            self.element.tail == other.element.tail
        ])

    def __hash__(self):
        return hash((
            self.law_path, self.unique, self.parent_unique, str(self.children_unique), str(self.element.attrib),
            self.element.tail, self.element.text, self.element.tag
        ))


class Point(Vertex):
    """ A class used to represent a Point in a Law """
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Point

        # hashing fields
        self.unique = ""
        self.children_unique = [f'{c.attrib}{c.text}{c.tag}{c.tail}' for c in element.iter()]
        self.parent = law.parent_map.get(element)
        self.g_parent = law.parent_map.get(self.parent)
        self.gg_parent = law.parent_map.get(self.g_parent)
        self.ggg_parent = law.parent_map.get(self.gg_parent)
        self.gggg_parent = law.parent_map.get(self.ggg_parent)
        self.ggggg_parent = law.parent_map.get(self.gggg_parent)
        self.gggggg_parent = law.parent_map.get(self.ggggg_parent)
        self.index_in_parent = [c for c in self.parent].index(element)
        self.index_in_g_parent = [c for c in self.g_parent].index(self.parent) if self.g_parent else -1
        self.index_in_gg_parent = [c for c in self.gg_parent].index(self.g_parent) if self.gg_parent else -1
        self.index_in_ggg_parent = [c for c in self.ggg_parent].index(self.gg_parent) if self.ggg_parent else -1
        self.index_in_gggg_parent = [c for c in self.gggg_parent].index(self.ggg_parent) if self.gggg_parent else -1
        self.index_in_ggggg_parent = [c for c in self.ggggg_parent].index(self.gggg_parent) if self.ggggg_parent else -1
        self.index_in_gggggg_parent = [c for c in self.gggggg_parent].index(self.ggggg_parent) if self.gggggg_parent else -1
        self.parent_unique = f'{self.parent.attrib}{self.parent.text}{self.parent.tag}{self.parent.tail}' \
                             f'{self.index_in_parent}{self.index_in_g_parent}{self.index_in_gg_parent}' \
                             f'{self.index_in_ggg_parent}{self.index_in_gggg_parent}{self.index_in_ggggg_parent}' \
                             f'{self.index_in_gggggg_parent}'

    def __eq__(self, other):
        return all([
            self.law_path == other.law_path,
            self.parent_unique == other.parent_unique,
            self.children_unique == other.children_unique,
            self.unique == other.unique,
            self.element.attrib == other.element.attrib,
            self.element.text == other.element.text,
            self.element.tag == other.element.tag,
            self.element.tail == other.element.tail
        ])

    def __hash__(self):
        return hash((
            self.law_path, self.unique, self.parent_unique, str(self.children_unique), str(self.element.attrib),
            self.element.tail, self.element.text, self.element.tag
        ))


class Section(Vertex):
    """ A class used to represent a Section in a Law """
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Section

        # hashing fields
        self.unique = ""
        self.children_unique = [f'{c.attrib}{c.text}{c.tag}{c.tail}' for c in element.iter()]
        self.parent = law.parent_map.get(element)
        self.g_parent = law.parent_map.get(self.parent)
        self.index_in_g_parent = [c for c in self.g_parent].index(self.parent) if self.g_parent else -1
        self.index_in_parent = [c for c in self.parent].index(element)
        self.parent_unique = f'{self.parent.attrib}{self.parent.text}{self.parent.tag}{self.parent.tail}' \
                             f'{self.index_in_parent}{self.index_in_g_parent}'

    def __eq__(self, other):
        return all([
            self.law_path == other.law_path,
            self.parent_unique == other.parent_unique,
            self.children_unique == other.children_unique,
            self.unique == other.unique,
            self.element.attrib == other.element.attrib,
            self.element.text == other.element.text,
            self.element.tag == other.element.tag,
            self.element.tail == other.element.tail
        ])

    def __hash__(self):
        return hash((
                    self.law_path, self.unique, self.parent_unique, str(self.children_unique), str(self.element.attrib),
                    self.element.tail, self.element.text, self.element.tag))


class Part(Vertex):
    """ A class used to represent a Part in a Law """
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Part

        # hashing fields
        self.unique = ""
        self.children_unique = [f'{c.attrib}{c.text}{c.tag}{c.tail}' for c in element.iter()]
        self.parent = law.parent_map.get(element)
        self.g_parent = law.parent_map.get(self.parent)
        self.index_in_g_parent = [c for c in self.g_parent].index(self.parent) if self.g_parent else -1
        self.index_in_parent = [c for c in self.parent].index(element)
        self.parent_unique = f'{self.parent.attrib}{self.parent.text}{self.parent.tag}{self.parent.tail}' \
                             f'{self.index_in_parent}{self.index_in_g_parent}'

    def __eq__(self, other):
        return all([
            self.law_path == other.law_path,
            self.parent_unique == other.parent_unique,
            self.children_unique == other.children_unique,
            self.unique == other.unique,
            self.element.attrib == other.element.attrib,
            self.element.text == other.element.text,
            self.element.tag == other.element.tag,
            self.element.tail == other.element.tail
        ])

    def __hash__(self):
        return hash((
                    self.law_path, self.unique, self.parent_unique, str(self.children_unique), str(self.element.attrib),
                    self.element.tail, self.element.text, self.element.tag))


class Appendix(Vertex):
    """ A class used to represent an Appendix in a Law """
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Appendix

        # hashing fields
        self.unique = ""
        self.children_unique = [f'{c.attrib}{c.text}{c.tag}{c.tail}' for c in element.iter()]
        self.parent = law.parent_map.get(element)
        self.g_parent = law.parent_map.get(self.parent)
        self.index_in_g_parent = [c for c in self.g_parent].index(self.parent) if self.g_parent else -1
        self.index_in_parent = [c for c in self.parent].index(element)
        self.parent_unique = f'{self.parent.attrib}{self.parent.text}{self.parent.tag}{self.parent.tail}' \
                             f'{self.index_in_parent}{self.index_in_g_parent}'

    def __eq__(self, other):
        return all([
            self.law_path == other.law_path,
            self.parent_unique == other.parent_unique,
            self.children_unique == other.children_unique,
            self.unique == other.unique,
            self.element.attrib == other.element.attrib,
            self.element.text == other.element.text,
            self.element.tag == other.element.tag,
            self.element.tail == other.element.tail
        ])

    def __hash__(self):
        return hash((
                    self.law_path, self.unique, self.parent_unique, str(self.children_unique), str(self.element.attrib),
                    self.element.tail, self.element.text, self.element.tag
        ))


class Preamble(Vertex):
    """ A class used to represent a Preamble in a Law """
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Preamble

        # hashing fields
        self.unique = ""
        self.children_unique = [f'{c.attrib}{c.text}{c.tag}{c.tail}' for c in element.iter()]
        self.parent = law.parent_map.get(element)
        self.g_parent = law.parent_map.get(self.parent)
        self.index_in_g_parent = [c for c in self.g_parent].index(self.parent) if self.g_parent else -1
        self.index_in_parent = [c for c in self.parent].index(element)
        self.parent_unique = f'{self.parent.attrib}{self.parent.text}{self.parent.tag}{self.parent.tail}' \
                             f'{self.index_in_parent}{self.index_in_g_parent}'

    def __eq__(self, other):
        return all([
            self.law_path == other.law_path,
            self.parent_unique == other.parent_unique,
            self.children_unique == other.children_unique,
            self.unique == other.unique,
            self.element.attrib == other.element.attrib,
            self.element.text == other.element.text,
            self.element.tag == other.element.tag,
            self.element.tail == other.element.tail
        ])

    def __hash__(self):
        return hash((
                    self.law_path, self.unique, self.parent_unique, str(self.children_unique), str(self.element.attrib),
                    self.element.tail, self.element.text, self.element.tag
        ))


class Subtitle(Vertex):
    """ A class used to represent a Subtitle in a Law """
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Subtitle

        # hashing fields
        self.unique = ""
        self.children_unique = [f'{c.attrib}{c.text}{c.tag}{c.tail}' for c in element.iter()]
        self.parent = law.parent_map.get(element)
        self.g_parent = law.parent_map.get(self.parent)
        self.index_in_g_parent = [c for c in self.g_parent].index(self.parent) if self.g_parent else -1
        self.index_in_parent = [c for c in self.parent].index(element)
        self.parent_unique = f'{self.parent.attrib}{self.parent.text}{self.parent.tag}{self.parent.tail}' \
                             f'{self.index_in_parent}{self.index_in_g_parent}'

    def __eq__(self, other):
        return all([
            self.law_path == other.law_path,
            self.parent_unique == other.parent_unique,
            self.children_unique == other.children_unique,
            self.unique == other.unique,
            self.element.attrib == other.element.attrib,
            self.element.text == other.element.text,
            self.element.tag == other.element.tag,
            self.element.tail == other.element.tail
        ])

    def __hash__(self):
        return hash((
                    self.law_path, self.unique, self.parent_unique, str(self.children_unique), str(self.element.attrib),
                    self.element.tail, self.element.text, self.element.tag
        ))


class WrapUp(Vertex):
    """ A class used to represent a WrapUp in a Law """
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.WrapUp

        # hashing fields
        self.unique = ""
        self.children_unique = [f'{c.attrib}{c.text}{c.tag}{c.tail}' for c in element.iter()]
        self.parent = law.parent_map.get(element)
        self.g_parent = law.parent_map.get(self.parent)
        self.index_in_g_parent = [c for c in self.g_parent].index(self.parent) if self.g_parent else -1
        self.index_in_parent = [c for c in self.parent].index(element)
        self.parent_unique = f'{self.parent.attrib}{self.parent.text}{self.parent.tag}{self.parent.tail}' \
                             f'{self.index_in_parent}{self.index_in_g_parent}'

    def __eq__(self, other):
        return all([
            self.law_path == other.law_path,
            self.parent_unique == other.parent_unique,
            self.children_unique == other.children_unique,
            self.unique == other.unique,
            self.element.attrib == other.element.attrib,
            self.element.text == other.element.text,
            self.element.tag == other.element.tag,
            self.element.tail == other.element.tail
        ])

    def __hash__(self):
        return hash((
                    self.law_path, self.unique, self.parent_unique, str(self.children_unique), str(self.element.attrib),
                    self.element.tail, self.element.text, self.element.tag
        ))


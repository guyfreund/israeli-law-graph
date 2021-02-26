from constants import XML_NAMESPACE, EdgeType, ANCESTOR_TAGS, Tag

import xml.etree.ElementTree as ET

global_id = 0


class Graph(object):
    def __init__(self, vertexes, edges):
        self._v: set[Vertex] = vertexes
        self._e: set[Edge] = edges

    @property
    def V(self):
        return self._v

    @property
    def E(self):
        return self._e


class Edge(object):
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

    def classify_edge_type(self, from_vertex, to_vertex):
        if type(from_vertex) is Preamble:
            if hash(to_vertex) == hash(from_vertex.law):
                return EdgeType.Law_Preamble  # Preamble of a law

        if hash(to_vertex) == hash(from_vertex.law):
            return EdgeType.Section_of_law  # Edge to it's own law

        if type(to_vertex) is not Law and type(from_vertex) is not Law:
            if hash(to_vertex.law) == hash(from_vertex.law):
                return EdgeType.No_Type  # vertexes under the same law
            else:
                return EdgeType.Reference_to_section_of_another_law # vertexes under different laws

        if type(to_vertex) is Law and type(from_vertex) is not Law:
            return EdgeType.Reference_to_another_law  # from not law to law

        return EdgeType.Generic


class Vertex(object):
    def __init__(self, law_path, element):
        self.law_path: str = law_path
        self.element: ET.Element = element
        self.in_edges: set[Edge] = set()
        self.out_edges: set[Edge] = set()
        self.unique = str()
        self.children_unique = str()
        self.parent_unique = str()
        self.tag = 'Vertex'
        self.id = self.get_id()
        # title and body are used on neo4j browser UI
        self.law: Law = None
        self.title = ''
        self.body = ''

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

    @staticmethod
    def get_id():
        global global_id
        global_id += 1
        if global_id == 70839:
            print()
        return global_id


class Law(Vertex):
    def __init__(self, path):
        tree: ET.ElementTree = ET.parse(path)
        root: ET.Element = tree.getroot()
        super().__init__(law_path=path, element=root)
        self.law: Law = self
        self.tag = Tag.Law
        self.path: str = path
        self.tree: ET.ElementTree = tree
        self.root: ET.Element = root
        frbr_work_uri: str = self.root.find(f'.//{XML_NAMESPACE}FRBRWork').find(f'.//{XML_NAMESPACE}FRBRuri').attrib[
            'value']
        self.frbr_work_uri: str = frbr_work_uri[1:] if frbr_work_uri.startswith('/') else frbr_work_uri
        self.title: str = self.root.find(f'.//{XML_NAMESPACE}body').find(f'./{XML_NAMESPACE}title') \
            .find(f'./{XML_NAMESPACE}content').find(f'./{XML_NAMESPACE}p').text\
            .replace('"', '""').replace('\n', ' ')
        self.hrefs: list = self.get_ref_elements()
        self.parent_map: dict = {c: p for p in self.tree.iter() for c in p}
        self.body = ''

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
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Chapter

        self.title: str = self.find_title().replace('"', '""') .replace('\n', ' ')

        # handling hashing
        self.unique = element.find(f'.//{XML_NAMESPACE}title').find(f'.//{XML_NAMESPACE}content').find(
            f'.//{XML_NAMESPACE}p').text
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

    def find_title(self):
        try:
            from_num = self.element.find(f'./{XML_NAMESPACE}num').text
            if from_num is None:
                from_num = ''
        except TypeError:
            from_num = ''
        try:
            from_p = self.element.find(f'./{XML_NAMESPACE}title') \
                .find(f'./{XML_NAMESPACE}content').find(f'./{XML_NAMESPACE}p').text
            if from_p is None:
                from_p = ''
        except TypeError:
            from_p = ''

        return (from_num + ' ' + from_p).strip()


class Point(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Point

        self.title: str = self.find_title().replace('"', '""').replace('\n', ' ')
        self.body: str = self.find_body().strip().replace('"', '""').replace('\n', ' ')

        # handling hashing
        self.unique = ''
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
        self.index_in_gggggg_parent = [c for c in self.gggggg_parent].index(
            self.ggggg_parent) if self.gggggg_parent else -1
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

    def find_title(self):

        try:
            number = self.element.find(f'./{XML_NAMESPACE}num').text
            if number is None:
                raise AttributeError
        except AttributeError:
            number = ''

        try:
            heading = self.element.find(f'./{XML_NAMESPACE}heading').find(f'./{XML_NAMESPACE}authorialNote').\
                find(f'./{XML_NAMESPACE}p').text
        except AttributeError:
            heading = ''

        if heading != '' and number != '':
            return (number + " " + heading).strip()

        # if heading is empty but number is not, this might be a sub point inside a point
        # if so, build the point's title by the number of 'point' appearing in the eId
        # if number != '':
        eid = self.element.attrib['eId']
        removed_underscores = eid.replace('_', ' ')
        removed_wrapup = removed_underscores.replace('wrapup', ' ')
        removed_none = removed_wrapup.replace('none', ' ')
        removed_points = list(filter(lambda s: s != '', map(lambda a: a.strip(), removed_none.split('point'))))
        if number != '':
            removed_points[len(removed_points) - 1] = number
        final_form = '. '.join(removed_points)
        return final_form

    def find_title_rec(self, e: ET.Element):
        text = ''
        if len(e) == 0:
            text += '' if e.text is None else e.text
            text += '' if e.tail is None else e.tail
        else:
            text += '' if e.text is None else e.text
            # t = e.find(f'./{XML_NAMESPACE}p')
            for sub_t in e:
                text += self.find_title_rec(sub_t)
            text += '' if e.tail is None else e.tail
        return text

    def find_body(self):
        try:
            body = self.find_body_rec(self.element.find(f'./{XML_NAMESPACE}content').find(f'./{XML_NAMESPACE}p'))
        except AttributeError:
            body = ''
        return body.strip()

    def find_body_rec(self, e: ET.Element):
        text = ''
        if len(e) == 0:
            text += '' if e.text is None else e.text
            text += '' if e.tail is None else e.tail
        else:
            text += '' if e.text is None else e.text
            # t = e.find(f'./{XML_NAMESPACE}p')
            for sub_t in e:
                text += self.find_body_rec(sub_t)
            text += '' if e.tail is None else e.tail
        return text


class Section(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Section

        self.title = self.find_title().replace('"', '""').replace('\n', ' ')
        self.body = self.find_body().replace('"', '""').replace('\n', ' ')

        # handling hashing
        self.unique = ''
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

    def find_title(self):
        try:
            from_num = self.element.find(f'./{XML_NAMESPACE}num').text
            return from_num if len(from_num) > 0 else self.element.find(f'./{XML_NAMESPACE}title') \
                .find(f'./{XML_NAMESPACE}content').find(f'./{XML_NAMESPACE}p').text
        except TypeError:
            pass
        return ""

    def find_body(self):
        try:
            return self.element.find(f'./{XML_NAMESPACE}title') \
                .find(f'./{XML_NAMESPACE}content').find(f'./{XML_NAMESPACE}p').text
        except TypeError:
            pass
        return ''


class Part(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Part

        self.title = self.find_title().replace('"', '""').replace('\n', ' ')

        # handling hashing
        self.unique = ''
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

    def find_title(self):
        try:
            from_num = self.element.find(f'./{XML_NAMESPACE}num').text
            if from_num is None:
                from_num = ''
        except TypeError:
            from_num = ''
        try:
            from_p = self.element.find(f'./{XML_NAMESPACE}title') \
                .find(f'./{XML_NAMESPACE}content').find(f'./{XML_NAMESPACE}p').text
            if from_p is None:
                from_p = ''
        except TypeError:
            from_p = ''

        return (from_num + ' ' + from_p).strip()


class Appendix(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Appendix

        self.title = self.find_title().replace('"', '""').replace('\n', ' ')

        # handling hashing
        self.unique = ''
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

    def find_title(self):
        try:
            return self.element.find(f'./{XML_NAMESPACE}title') \
                .find(f'./{XML_NAMESPACE}content').find(f'./{XML_NAMESPACE}p').text
        except TypeError:
            pass
        return ''


class Preamble(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Preamble

        self.title = \
                     self.find_title(element).strip().replace('"', '""').replace('\n', ' ')

        # handling hashing
        self.unique = ''
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

    def find_title(self, e: ET.Element):
        text = ''
        if len(e) == 0:
            text += '' if e.text is None else e.text
            text += '' if e.tail is None else e.tail
        else:
            text += '' if e.text is None else e.text
            # t = e.find(f'./{XML_NAMESPACE}p')
            for sub_t in e:
                text += self.find_title(sub_t)
            text += '' if e.tail is None else e.tail
        return text


class Subtitle(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.Subtitle

        self.title = self.find_title(self.element.find(f'./{XML_NAMESPACE}content').find(f'./{XML_NAMESPACE}p'))\
            .strip().replace('"', '""').replace('\n', ' ')

        # handling hashing
        self.unique = ''
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

    def find_title(self, e: ET.Element):
        text = ''
        if len(e) == 0:
            text += '' if e.text is None else e.text
            text += '' if e.tail is None else e.tail
        else:
            text += '' if e.text is None else e.text
            # t = e.find(f'./{XML_NAMESPACE}p')
            for sub_t in e:
                text += self.find_title(sub_t)
            text += '' if e.tail is None else e.tail
        return text


class WrapUp(Vertex):
    def __init__(self, law, element):
        super().__init__(law_path=law.path, element=element)
        self.law: Law = law
        self.tag = Tag.WrapUp

        self.title = self.find_title().replace('"', '""').replace('\n', ' ')
        self.body = self.find_body().replace('"', '""').replace('\n', ' ')

        # handling hashing
        self.unique = ''
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

    def find_title(self):
        try:
            number = self.element.find(f'./{XML_NAMESPACE}num').text
            if number is None:
                raise AttributeError
        except AttributeError:
            number = ''

        eid = self.element.attrib['eId']
        removed_underscores = eid.replace('_', ' ')
        removed_wrapup = removed_underscores.replace('wrapup', ' ')
        removed_none = removed_wrapup.replace('none', ' ')
        removed_points = list(filter(lambda s: s != '', map(lambda a: a.strip(), removed_none.split('point'))))
        if number != '':
            removed_points[len(removed_points) - 1] = number
        final_form = '. '.join(removed_points)
        return final_form

    def find_body(self):
        try:
            body = self.find_body_rec(self.element.find(f'./{XML_NAMESPACE}content').find(f'./{XML_NAMESPACE}p'))
        except AttributeError:
            body = ''
        return body.strip()

    def find_body_rec(self, e: ET.Element):
        text = ''
        if len(e) == 0:
            text += '' if e.text is None else e.text
            text += '' if e.tail is None else e.tail
        else:
            text += '' if e.text is None else e.text
            # t = e.find(f'./{XML_NAMESPACE}p')
            for sub_t in e:
                text += self.find_body_rec(sub_t)
            text += '' if e.tail is None else e.tail
        return text

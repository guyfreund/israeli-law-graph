from py2neo import Graph, Node, Relationship
from classes import Graph as OurGraph, Law, Point, Preamble, Part, Section, Chapter, Appendix, Subtitle, WrapUp


def init_graph(our_graph: OurGraph, user: str, password: str, url: str = 'bolt://localhost:7687'):
    graph = Graph(f"{url}", user=user, password=password)
    graph.delete_all()
    tx = graph.begin()

    nodes_dict = create_nodes_dict(our_graph)
    count = 0
    progress = 0.0
    total = len(nodes_dict.values())
    for v in nodes_dict.values():
        tx.create(v)

        if count > (total / 100):
            count = 0
            progress += 1
            print('Vertex Progress', progress, '%')

        count += 1
    count = 0
    progress = 0.0
    total = len(our_graph.E)
    for e in our_graph.E:
        source = e.from_vertex.id
        target = e.to_vertex.id
        new_edge = Relationship(nodes_dict[source], e.type, nodes_dict[target])
        tx.create(new_edge)
        if count > (total / 100):
            count = 0
            progress += 1
            print('Edge Progress', progress, '%')
        count += 1

    tx.commit()


def create_node(v):
    v_class_name = type(v).__name__
    if type(v) is Law:
        return Node(v_class_name, title=v.title, law_uri=v.path)
    elif type(v) is Chapter:
        return Node(v_class_name, title=v.title, law_uri=v.law.path)
    elif type(v) is Point:
        return Node(v_class_name, title=v.title, body=v.body, law_uri=v.law.path)
    elif type(v) is Section:
        return Node(v_class_name, title=v.title, body=v.body, law_uri=v.law.path)
    elif type(v) is Part:
        return Node(v_class_name, title=v.title, law_uri=v.law.path)
    elif type(v) is Appendix:
        return Node(v_class_name, title=v.title, law_uri=v.law.path)
    elif type(v) is Preamble:
        return Node(v_class_name, title=v.title, law_uri=v.law.path)
    elif type(v) is Subtitle:
        return Node(v_class_name, title=v.title, law_uri=v.law.path)
    elif type(v) is WrapUp:
        return Node(v_class_name, title=v.title, law_uri=v.law.path)
    raise Exception("vertex type not recognized")


def create_nodes_dict(g: OurGraph):
    nodes_dict = {}
    for v in g.V:
        nodes_dict[v.id] = create_node(v)
    return nodes_dict


from classes import Vertex, Edge, Graph, Law
from utils import classify_tag, classify_vertex_by_tag_and_eid, get_ref_ancestor_element, build_laws_mapping, \
    parse_ref, classify_eid_by_tag
from error import write_to_errors_file, init_errors_dict
from constants import HREF

import logging

logging.basicConfig(filename='law_graph_logs.log', level=logging.INFO)
# logging.basicConfig(level=logging.INFO)


def get_from_vertex(from_law, ref_element, edges, vertexes_map):
    """ Searches for a to_vertex
    1. Searches for the first ancestor of the element to be the from_vertex
    2. Sets up an inner (law and an element in it) edge: from_law => from_vertex

    """
    from_vertex: Vertex = get_ref_ancestor_element(law=from_law, element=ref_element, vertexes_map=vertexes_map)
    setup_inner_edge(from_law, from_vertex, edges)

    return from_vertex


def get_to_vertex(from_law, ref_element, errors_dict, frbr_work_uri_to_law, edges, vertexes_map):
    """ Searches for a from_vertex
    1. Parse the reference text to get frbr_work_uri prefix and element identifier (eid)
    2. Classify the vertex's tag by the eid
    3. Classify potential eids
    4. Get the to_vertex using it's tag and eid
    5. Sets up an inner (law and an element in it) edge: to_law => to_vertex

    """
    frbr_work_uri, eid = parse_ref(ref_element=ref_element, from_law=from_law, errors_dict=errors_dict)
    if not frbr_work_uri:
        return None

    to_law: Law = frbr_work_uri_to_law[frbr_work_uri]
    tag: str = classify_tag(eid=eid, errors_dict=errors_dict, from_law=from_law, ref_element=ref_element)
    eids: list = classify_eid_by_tag(tag=tag, eid=eid)
    to_vertex: Vertex = classify_vertex_by_tag_and_eid(
        tag=tag, eids=eids, to_law=to_law, errors_dict=errors_dict, from_law=from_law, from_element=ref_element,
        vertexes_map=vertexes_map
    )
    setup_inner_edge(to_law, to_vertex, edges)

    return to_vertex


def setup_inner_edge(law, vertex, edges):
    """ Sets up an inner (law and an element in it) edge """
    inner_edge = Edge(law, vertex, vertex.element)
    edges.add(inner_edge)
    vertex.add_in_edge(inner_edge)
    law.add_out_edge(inner_edge)


def generate_graph():
    """ Generate the graph """
    edges: set = set()
    total_refs: int = 0
    successful_refs: int = 0
    errors_dict = init_errors_dict()
    laws, frbr_work_uri_to_law = build_laws_mapping()
    vertexes_map = {hash(law): law for law in laws}

    for from_law in laws:
        for ref_element in from_law.get_ref_elements():
            from_vertex: Vertex = get_from_vertex(from_law, ref_element, edges, vertexes_map)

            to_vertex: Vertex = get_to_vertex(
                from_law, ref_element, errors_dict, frbr_work_uri_to_law, edges, vertexes_map
            )
            if not to_vertex:
                total_refs += 1
                continue

            # setup an edge and maintain metadata
            edge: Edge = Edge(from_vertex, to_vertex, ref_element)
            edges.add(edge)
            from_vertex.add_out_edge(edge)
            to_vertex.add_in_edge(edge)

            successful_refs += 1
            total_refs += 1
            logging.info(f"{total_refs}. Succeed to handle href {ref_element.attrib[HREF]} in from_law {from_law.path}")

    logging.info(f'{total_refs = }, {successful_refs = }, failed_not_handled_refs = {total_refs - successful_refs}')
    write_to_errors_file(errors_dict)
    return Graph(set(vertexes_map.values()), edges)


def main():
    try:
        graph = generate_graph()
    except Exception as e:
        logging.exception(str(e), exc_info=True)
        raise e


if __name__ == '__main__':
    main()

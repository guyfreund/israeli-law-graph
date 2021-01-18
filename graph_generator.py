from classes import Vertex, Edge, Graph, Law
from utils import classify_tag, classify_vertex_by_tag_and_eid, get_ref_ancestor_element, build_laws_mapping, parse_ref, classify_eid_by_tag
from error import write_to_errors_file, init_errors_dict
from constants import HREF

import logging

logging.basicConfig(filename='law_graph_logs.log', level=logging.INFO)


def generate_graph():
    vertexes: set = set()
    edges: set = set()
    total_refs: int = 0
    successful_refs: int = 0
    failed_but_handled_refs: int = 0
    errors_dict = init_errors_dict()

    laws, frbr_work_uri_to_law = build_laws_mapping()
    for law in laws:
        for ref_element in law.get_ref_elements():
            # get from vertex
            from_vertex: Vertex = get_ref_ancestor_element(law=law, element=ref_element)
            vertexes.add(from_vertex)

            # parse the ref
            frbr_work_uri, eid = parse_ref(ref_element=ref_element, law=law, errors_dict=errors_dict)
            if not frbr_work_uri:
                failed_but_handled_refs += 1
                continue

            # get to vertex
            to_law: Law = frbr_work_uri_to_law[frbr_work_uri]
            tag: str = classify_tag(eid=eid, errors_dict=errors_dict, from_law=law, ref_element=ref_element)
            eids: list = classify_eid_by_tag(tag=tag, eid=eid)
            to_vertex: Vertex = classify_vertex_by_tag_and_eid(tag=tag, eids=eids, to_law=to_law, errors_dict=errors_dict, from_law=law, from_element=ref_element)
            vertexes.add(to_vertex)

            # setup an edge and maintain metadata
            edge: Edge = Edge(from_vertex, to_vertex)
            edges.add(edge)
            from_vertex.add_out_edge(edge)
            to_vertex.add_in_edge(edge)

            successful_refs += 1
            total_refs += 1
            logging.info(f"Succeed to handle href {ref_element.attrib[HREF]} in law {law.path}")

    logging.info(f'{total_refs = }, {successful_refs = }, {failed_but_handled_refs = }, failed_not_handled_refs = {total_refs - successful_refs - failed_but_handled_refs}')
    write_to_errors_file(errors_dict)
    return Graph(vertexes, edges)


def main():
    try:
        graph = generate_graph()
    except Exception as e:
        logging.exception(str(e), exc_info=True)
        raise e


if __name__ == '__main__':
    # @TODO: add all laws to the vertexes
    main()

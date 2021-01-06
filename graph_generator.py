from classes import Vertex, Edge, Graph, Law
from utils import classify_tag, classify_vertex_by_tag_and_eid, get_ref_ancestor_element, split_ref, \
    build_laws_mapping, parse_ref, classify_eid_by_tag, write_non_existing_rules
import traceback


def main():
    vertexes: set = set()
    edges: set = set()
    total_refs: int = 0
    successful_refs: int = 0
    failed_but_handled_refs: int = 0

    laws, frbr_work_uri_to_law = build_laws_mapping()
    for law in laws:
        for ref_element in law.get_ref_elements():
            try:
                # get from vertex
                from_vertex: Vertex = get_ref_ancestor_element(law, ref_element)
                vertexes.add(from_vertex)

                # parse the ref
                frbr_work_uri, eid = parse_ref(ref_element, law.frbr_work_uri)
                if not frbr_work_uri:
                    failed_but_handled_refs += 1
                    continue

                # get to vertex
                to_law: Law = frbr_work_uri_to_law[frbr_work_uri]
                tag: str = classify_tag(eid)
                eids: list = classify_eid_by_tag(tag, eid)
                to_vertex: Vertex = classify_vertex_by_tag_and_eid(tag, eids, to_law)
                vertexes.add(to_vertex)

                # setup an edge and maintain metadata
                edge: Edge = Edge(from_vertex, to_vertex)
                edges.add(edge)
                from_vertex.add_out_edge(edge)
                to_vertex.add_in_edge(edge)
                successful_refs += 1

            except Exception as e:
                print(str(e))
            finally:
                total_refs += 1

    print(f'{total_refs = }, {successful_refs = }, {failed_but_handled_refs = }, '
          f'failed_not_handled_refs = {total_refs - successful_refs - failed_but_handled_refs}')
    write_non_existing_rules()
    graph = Graph(vertexes, edges)


if __name__ == '__main__':
    # @TODO: add all laws to the vertexes
    main()

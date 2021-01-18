from graph_generator import generate_graph
import logging


def validate_graph(graph):
    vertex_count_map = {}
    for edge in graph.E:
        from_vertex = edge.from_vertex
        to_vertex = edge.to_vertex

        if from_vertex not in vertex_count_map:
            vertex_count_map[from_vertex] = {'in': 0, 'out': 0}
        if to_vertex not in vertex_count_map:
            vertex_count_map[to_vertex] = {'in': 0, 'out': 0}

        from_vertex_data = vertex_count_map[from_vertex]
        from_vertex_out = from_vertex_data['out'] + 1
        vertex_count_map[from_vertex].update({'out': from_vertex_out})

        to_vertex_data = vertex_count_map[to_vertex]
        to_vertex_in = to_vertex_data['in'] + 1
        vertex_count_map[to_vertex].update({'in': to_vertex_in})

    errors = 0
    for vertex in graph.V:
        if vertex in vertex_count_map:
            len_in = len(vertex.in_edges)
            len_in_map = vertex_count_map[vertex]['in']
            in_ans = len_in == len_in_map
            if not in_ans:
                errors += 1
                logging.error(f'{errors}. {vertex.law_path}/{vertex.tag}:{vertex.element.attrib["eId"]}. '
                              f'in: {len_in}, in_map: {len_in_map}.')

            len_out = len(vertex.out_edges)
            len_out_map = vertex_count_map[vertex]['out']
            out_ans = len_out == len_out_map
            if not out_ans:
                errors += 1
                logging.error(f'{errors}. {vertex.law_path}/{vertex.tag}:{vertex.element.attrib["eId"]}. '
                              f'out: {len_out}, out_map: {len_out_map}.')
        else:
            if len(vertex.in_edges) > 0 or len(vertex.out_edges) > 0:
                errors += 1
                logging.error(f'{errors}. Vertex not found in edges but has in/out edges.')


def main():
    graph = generate_graph()
    validate_graph(graph)


if __name__ == '__main__':
    main()

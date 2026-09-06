"""Cross-model and adversarial controls; not premises of the cover checker."""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import json

import build
import check


def controls():
    elements, parts, edges = check.permutation_model()
    producer_parts, producer_edges = build.model()
    check.need(parts == producer_parts and edges == producer_edges, 'edge models agree')
    for u in range(40):
        check.need(elements[build.inverse(u)] == check.invert(elements[u]), 'inverse agreement')
        for v in range(40):
            check.need(elements[build.multiply(u, v)] == check.compose(elements[u], elements[v]), 'multiplication agreement')

    # Independently calculate every byte of all twenty full truth columns.
    # Byte k stores assignments 8*k,...,8*k+7, in low-bit-first order.
    truth_bytes = 0
    for bit, column in enumerate(check.truth_columns(20)):
        data = column.to_bytes((1 << 20)//8, 'little')
        for k, byte in enumerate(data):
            expected = sum((((8*k+j) >> bit) & 1) << j for j in range(8))
            check.need(byte == expected, 'literal truth-column interpretation')
            truth_bytes += 1

    doc = json.loads((Path(__file__).parent/'certificate.json').read_text())
    # Build sixteen physical graphs directly from the closed-form group law.
    # Their supplied witnesses must also be monochrome in that other model.
    masks = [0, (1 << 20)-1] + [int.from_bytes(bytes([k, 7*k % 256, 13*k % 16]), 'little') for k in range(1, 15)]
    for mask in masks:
        connection = {u for k, part in enumerate(producer_parts) if mask >> k & 1 for u in part}
        adjacency = [[u != v and build.multiply(build.inverse(u), v) in connection for v in range(40)] for u in range(40)]
        check.need(any(len({adjacency[u][v] for u, v in combinations(q, 2)}) == 1 for q in doc['five_sets']), 'physical fixture witness')

    bad = {}
    bad['empty'] = {'schema': 1, 'five_sets': []}
    bad['one_witness_is_incomplete'] = {'schema': 1, 'five_sets': [doc['five_sets'][0]]}
    bad['duplicate_witness'] = deepcopy(doc)
    bad['duplicate_witness']['five_sets'].insert(0, doc['five_sets'][0])
    bad['duplicate_vertex'] = {'schema': 1, 'five_sets': [[0, 0, 1, 2, 3]]}
    bad['out_of_range'] = {'schema': 1, 'five_sets': [[0, 1, 2, 3, 40]]}
    bad['boolean_vertex'] = {'schema': 1, 'five_sets': [[False, 1, 2, 3, 4]]}
    bad['wrong_schema'] = {'schema': True, 'five_sets': doc['five_sets']}
    bad['unsorted_vertices'] = {'schema': 1, 'five_sets': [[1, 0, 2, 3, 4]]}
    rejected = []
    for name, candidate in bad.items():
        try:
            check.check(candidate)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('bad certificate accepted: '+name)
    return {'status': 'CONTROLS_PASSED', 'multiplications_compared': 1600,
            'inverses_compared': 40, 'truth_column_bytes_checked': truth_bytes,
            'truth_assignment_bits_checked': 8*truth_bytes,
            'physical_graph_fixtures': len(masks), 'rejected_cases': rejected}


if __name__ == '__main__':
    print(json.dumps(controls(), indent=2, sort_keys=True))

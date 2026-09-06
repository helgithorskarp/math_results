"""Independent universal-cover checker using regular permutations and truth columns.

Imports no producer. It needs no enumeration-completeness assumption, SAT
solver, DPLL trace, minimal-support list, or external classification.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def compose(left, right):
    return tuple(left[right[v]] for v in range(40))


def invert(p):
    q = [0]*40
    for i, j in enumerate(p):
        q[j] = i
    return tuple(q)


def permutation_model():
    identity = tuple(range(40))
    a = tuple((v % 5+1) % 5+5*(v//5) for v in range(40))
    b = tuple((2*(v % 5)) % 5+5*((v//5+1) % 8) for v in range(40))
    need(compose(compose(b, a), invert(b)) == compose(a, a), 'b a b^-1 = a^2')
    elements = []
    bpower = identity
    for j in range(8):
        current = bpower
        for i in range(5):
            need(current[0] == i+5*j, 'normal-form labels and regular action')
            elements.append(current)
            current = compose(a, current)
        need(current == bpower, 'a^5 = 1')
        bpower = compose(b, bpower)
    need(bpower == identity and len(set(elements)) == 40, 'b^8 = 1 and forty elements')
    positions = {p: i for i, p in enumerate(elements)}
    for p in elements:
        need(sorted(p) == list(range(40)), 'permutation')
        for q in elements:
            need(compose(p, q) in positions, 'closed group')
    inverses = [invert(p) for p in elements]
    inverse_labels = [positions[p] for p in inverses]
    parts = sorted({tuple(sorted({i, inverse_labels[i]})) for i in range(1, 40)})
    need(len(parts) == 20 and Counter(map(len, parts)) == {1: 1, 2: 19}, 'complete inverse partition')
    index = {element: variable for variable, part in enumerate(parts) for element in part}
    need(set(index) == set(range(1, 40)), 'every nonidentity difference occurs')
    # The inverse left-translation of u sends v to the group difference u^-1 v.
    edge_variables = [[None if u == v else index[inverses[u][v]]
                       for v in range(40)] for u in range(40)]
    need(all(edge_variables[u][v] == edge_variables[v][u]
             for u in range(40) for v in range(40)), 'undirected edge variables')
    return elements, parts, edge_variables


def truth_columns(variables):
    need(type(variables) is int and variables >= 3, 'truth-table variable count')
    byte_count = (1 << variables)//8
    columns = []
    for bit in range(variables):
        if bit < 3:
            pattern = bytes([(0xAA, 0xCC, 0xF0)[bit]])
        else:
            block = 1 << (bit-3)
            pattern = bytes(block)+bytes([255])*block
        columns.append(int.from_bytes(pattern*(byte_count//len(pattern)), 'little'))
    return columns


def check(doc):
    need(type(doc) is dict and set(doc) == {'schema', 'five_sets'}, 'certificate keys')
    need(type(doc['schema']) is int and doc['schema'] == 1, 'schema')
    need(type(doc['five_sets']) is list and len(doc['five_sets']) > 0, 'nonempty witness list')
    rows = doc['five_sets']
    need(all(type(q) is list and len(q) == 5 and all(type(v) is int for v in q) for q in rows), 'five-set format')
    witnesses = [tuple(q) for q in rows]
    need(witnesses == sorted(set(witnesses)), 'canonical distinct witnesses')
    need(all(q == tuple(sorted(set(q))) and 0 <= q[0] and q[-1] < 40 for q in witnesses), 'five distinct physical vertices')
    elements, parts, edge_variables = permutation_model()
    columns = truth_columns(len(parts))
    assignments = 1 << len(parts)
    full = (1 << assignments)-1
    covered = 0
    for q in witnesses:
        all_red = full
        all_blue = full
        # All ten physical pairs are evaluated; repeated variables are harmless.
        for u, v in combinations(q, 2):
            column = columns[edge_variables[u][v]]
            all_red &= column
            all_blue &= full ^ column
        covered |= all_red | all_blue
    need(covered == full, 'some connection set has no supplied monochromatic witness')
    return {'status': 'VERIFIED_C5_SEMIDIRECT_C8_CAYLEY_OBSTRUCTION',
            'group_order': len(elements), 'inverse_class_size_histogram': {str(k): v for k, v in sorted(Counter(map(len, parts)).items())},
            'connection_variables': len(parts), 'connection_sets_covered': assignments,
            'physical_five_sets': len(witnesses), 'physical_pairs_evaluated': 10*len(witnesses),
            'covered_truth_table_sha256': sha256(covered.to_bytes(assignments//8, 'little')).hexdigest(),
            'ramsey_40_cores': 0, 'unrestricted_three_vertex_attachment_bits': 123,
            'excluded_labeled_43_family_size': '2^143',
            'imported_classification': False, 'ramsey_bound_improved': False}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('certificate', type=Path)
    args = ap.parse_args()
    print(json.dumps(check(json.loads(args.certificate.read_text())), indent=2, sort_keys=True))

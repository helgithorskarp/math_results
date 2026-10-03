#!/usr/bin/env python3
"""Independent square-set, literal-lift and closed-family verifier; no generator import."""
import argparse
import hashlib
import json
import struct
from collections import Counter, deque
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, separators=(',', ':'), sort_keys=True).encode()


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def inverse(x, p):
    old_r, r, old_s, s = p, x, 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    need(old_r == 1, 'invertible')
    return old_s % p


def square_data():
    p = 617
    divisor = 2
    while divisor * divisor <= p:
        need(p % divisor != 0, 'prime')
        divisor += 1
    squares = {x * x % p for x in range(1, p)}
    need(len(squares) == 308 and 0 not in squares, 'square coset')
    colors = {x: int(x not in squares) for x in range(1, p)}
    return p, squares, colors


def endpoint_data(p, colors):
    edges = []
    for difference in range(1, p):
        current = 1
        points = []
        for _ in range(6):
            current = (current + difference) % p
            points.append(current)
        if 0 not in points and all(colors[x] != colors[1] for x in points):
            need(len(set(points)) == 6, 'six support columns')
            edges.append({'step': difference, 'support': sorted(points)})
    return edges


def enumerate_hitting_sets(edges):
    # Exact branching: any completion must meet the first unhit edge. No
    # outside-union vertex can occur in a five-cover of five disjoint edges.
    solutions = set()
    def visit(chosen):
        missing = next((e for e in edges if not e & chosen), None)
        if missing is None:
            solutions.add(tuple(sorted(chosen)))
            return
        if len(chosen) == 5:
            return
        for x in sorted(missing):
            visit(chosen | {x})
    visit(set())
    return sorted(solutions)


def check_base(data):
    p, squares, colors = square_data()
    edges = endpoint_data(p, colors)
    support = [set(e['support']) for e in edges]
    need(len(support) == 6, 'complete six endpoint units')
    for i in range(5):
        for j in range(i):
            need(not support[i] & support[j], 'disjoint witness')
    union = set().union(*support)
    inv = {inverse(x, p) for x in union}
    need(not union & inv, 'reciprocal obstruction')
    covers = enumerate_hitting_sets(support)
    need(all(len(x) == 5 for x in covers) and len(covers) == 3888, 'minimum covers')
    avoiding = visiting = 0
    for difference in range(1, p):
        for first in range(p):
            current = first
            column = []
            for _ in range(7):
                column.append(current)
                current = (current + difference) % p
            values = [colors[x] for x in column if x != 0]
            need(len(set(column)) == 7 and len(values) in (6, 7), 'field AP')
            need(0 in values and 1 in values, 'literal partial-character AP mixing')
            if len(values) == 7:
                avoiding += 1
            else:
                visiting += 1
    # Independent offset and root-word controls for the ordinary interval bridge.
    for root_slot in range(7):
        values = [colors[(j - root_slot) % p] for j in range(7) if j != root_slot]
        need(0 in values and 1 in values, 'zero-visit offsets mix')
    root_words = sum(1 for w in range(128) if any((w >> j) & 1 for j in range(7))
                     and any(not ((w >> j) & 1) for j in range(7)))
    expected = {'schema': 'character617-base-v1', 'agent': 'six-vdw-3', 'role': 'researcher',
                'prime': p, 'character_ascii_sha256': hashlib.sha256(''.join(str(colors[x]) for x in range(1, p)).encode()).hexdigest(),
                'endpoint_steps_examined': 616, 'endpoint_unit_supports': edges,
                'five_disjoint_support_indices': [0, 1, 2, 3, 4],
                'support_union': sorted(union), 'support_inverses': sorted(inv), 'reciprocal_overlap': [],
                'undirected_ratio_set': sorted(union | inv), 'minimum_hitting_number': 5,
                'minimum_covers': len(covers), 'minimum_covers_sha256': sha(covers),
                'minimum_cover_union': sorted(set().union(*map(set, covers))),
                'field_start_step_pairs': avoiding + visiting, 'root_avoiding_pairs': avoiding,
                'root_visiting_pairs': visiting, 'partial_monochromatic_pairs': 0,
                'offset_control': {'minus_one': colors[616], 'one': colors[1], 'three': colors[3]},
                'root_words_at_3703': root_words, 'palettes': 2, 'actual_restricted_3703_colorings': 2 * root_words}
    need(data == expected, 'entire base certificate')


def check_lattice(data):
    p, squares, colors = square_data()
    support = set().union(*(set(e['support']) for e in endpoint_data(p, colors)))
    ratios = support | {inverse(v, p) for v in support}
    need(len(ratios) == 66 and all(v not in squares for v in ratios), 'bipartite ratio degree')
    qlist = sorted(squares)
    nonsquares = sorted(set(range(1, p)) - squares)
    # Literal ratio tests rather than producer multiplication; integer bit masks.
    neighbors = {}
    for q in qlist:
        qi = inverse(q, p)
        neighbors[q] = sum(1 << t for t in nonsquares if t * qi % p in ratios)
    records = data['records']
    need(records == sorted(records, key=lambda e: tuple(e['B'])), 'canonical state order')
    states = {}
    histogram = Counter()
    for row in records:
        b = row['B']
        need(b == sorted(set(b)) and len(b) >= 10 and set(b) <= ratios, 'retained common neighbors')
        mask = sum(1 << x for x in b)
        need(mask not in states, 'no duplicate state')
        closure = [q for q in qlist if neighbors[q] & mask == mask]
        need(row == {'B': b, 'A': closure} and len(closure) <= 4, 'literal full square-side closure')
        histogram[str(len(closure))] += 1
        states[mask] = row
    seed = sum(1 << x for x in ratios)
    need(seed in states, 'initial neighborhood present')
    # Closed finite family: every >=10 intersection must be present. This is
    # the completeness check; a submitted list of successful cases is insufficient.
    transitions = 0
    adjacency = {}
    for mask in states:
        children = []
        for q in qlist:
            result = mask & neighbors[q]
            if result.bit_count() >= 10:
                need(result in states, 'missing closed-family transition')
                transitions += 1
                children.append(result)
        adjacency[mask] = children
    visited = {seed}
    queue = deque([seed])
    while queue:
        for result in adjacency[queue.popleft()]:
            if result not in visited:
                visited.add(result)
                queue.append(result)
    need(visited == set(states), 'all submitted states reachable')
    expected = {'schema': 'character617-lattice-v1', 'prime': p, 'minimum_B_size': 10,
                'first_square_vertex': 1, 'square_vertices': len(squares), 'nonsquare_vertices': len(nonsquares),
                'ratio_degree': len(ratios), 'states': len(records), 'retained_transitions': transitions,
                'A_histogram': dict(histogram), 'maximum_A': max(map(int, histogram)),
                'state_records_sha256': sha(records), 'records': records}
    need(data == expected, 'entire lattice certificate')


def check_lift(data):
    p = 617
    n, start, stop = data['interval'], data['start'], data['stop']
    need(n in (3702, 3704) and 1 <= start <= stop <= n, 'literal lift coverage range')
    transcript = hashlib.sha256()
    orientations = Counter()
    for m in range(start, stop + 1):
        for delta in range(1, p):
            ordinary = [m + j * delta for j in range(7)]
            if ordinary[-1] <= n:
                points = ordinary
                orientation = 0
            else:
                points = sorted(m - j * (p - delta) for j in range(7))
                orientation = 6
            need(points[0] >= 1 and points[-1] <= n, 'all seven actual positions in interval')
            diffs = [points[j + 1] - points[j] for j in range(6)]
            need(len(set(diffs)) == 1 and 0 < diffs[0] < p, 'actual positive ordinary AP')
            need(points.index(m) == orientation, 'actual target endpoint')
            for j in range(7):
                position = points[j if orientation == 0 else 6 - j]
                need((position - ordinary[j]) % p == 0, 'literal ordered residue identity')
            orientations[orientation] += 1
            transcript.update(struct.pack('<5H', m, delta, points[0], diffs[0], orientation))
    expected = {'schema': 'character617-lift-v1', 'prime': p, 'interval': n, 'start': start, 'stop': stop,
                'actual_endpoint_pairs': sum(orientations.values()), 'forward_APs': orientations[0],
                'backward_APs': orientations[6], 'actual_lifts_sha256': transcript.hexdigest()}
    need(data == expected, 'entire literal lift record')


def check_transport(data):
    p, squares, colors = square_data()
    rows = endpoint_data(p, colors)[:5]
    start, stop = data['start'], data['stop']
    need(0 <= start <= stop < p, 'root transport coverage range')
    transcript = hashlib.sha256()
    count = 0
    for root in range(start, stop + 1):
        for target in [(root + k) % p for k in range(1, p)]:
            factor = (target - root) % p
            points = []
            for row in rows:
                step = factor * row['step'] % p
                current = target
                for _ in range(6):
                    current = (current + step) % p
                    need(current not in (root, target), 'root and target avoided')
                    need(colors[(current - root) % p] != colors[(target - root) % p], 'opposing literal color')
                    points.append(current)
            need(len(set(points)) == 30, 'thirty distinct support columns')
            transcript.update(struct.pack('<33H', root, target, factor, *points))
            count += 1
    expected = {'schema': 'character617-transport-v1', 'prime': p, 'start': start, 'stop': stop,
                'root_target_parameters': count, 'literal_support_columns': count * 30,
                'transport_sha256': transcript.hexdigest()}
    need(data == expected, 'entire transport record')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    a = parser.parse_args()
    raw = a.input.read_bytes()
    data = json.loads(raw)
    validators = {'character617-base-v1': check_base, 'character617-lattice-v1': check_lattice,
                  'character617-lift-v1': check_lift, 'character617-transport-v1': check_transport}
    need(data.get('schema') in validators, 'known certificate schema')
    validators[data['schema']](data)
    result = {'status': 'VALID', 'schema': data['schema'], 'whole_input_sha256': hashlib.sha256(raw).hexdigest()}
    if a.output:
        a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()

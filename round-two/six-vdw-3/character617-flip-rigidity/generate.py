#!/usr/bin/env python3
"""Exact finite data for the prime-617 character flip graph; standard library."""
import argparse
import hashlib
import itertools
import json
import struct
from pathlib import Path

P = 617
STEPS = (285, 314, 362, 381, 409, 570)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def character():
    require(all(P % d for d in range(2, 25)), '617 must be prime')
    powers = [pow(x, (P - 1) // 2, P) for x in range(1, P)]
    require(set(powers) == {1, P - 1}, 'Euler signs')
    return [None] + [int(v == P - 1) for v in powers]


def endpoints():
    c = character()
    result = []
    for d in range(1, P):
        points = [(1 + j * d) % P for j in range(1, 7)]
        if all(c[x] == 1 for x in points):
            result.append({'step': d, 'support': sorted(points)})
    require(tuple(v['step'] for v in result) == STEPS, 'complete endpoint domain')
    return result


def minimum_covers(edges):
    # Five disjoint primary edges force one vertex from each; the sixth then
    # forces the first choice into its three-point intersection with edge0.
    choices = [sorted(set(edges[0]) & set(edges[5])), *edges[1:5]]
    result = sorted(tuple(sorted(x)) for x in itertools.product(*choices))
    require(len(result) == len(set(result)), 'distinct covers')
    require(all(all(set(x) & set(e) for e in edges) for x in result), 'covers')
    return result


def base():
    c = character()
    rows = endpoints()
    edges = [r['support'] for r in rows]
    require(all(not (set(edges[i]) & set(edges[j]))
                for i in range(5) for j in range(i)), 'five disjoint supports')
    vertices = sorted(set().union(*map(set, edges)))
    inverse = sorted(pow(v, -1, P) for v in vertices)
    overlap = sorted(set(vertices) & set(inverse))
    require(not overlap, 'no reciprocal support pair')
    covers = minimum_covers(edges)
    cover_union = sorted(set().union(*map(set, covers)))
    avoiding = visiting = 0
    for a in range(P):
        for d in range(1, P):
            mask = 0
            zeros = 0
            for j in range(7):
                x = (a + j * d) % P
                if x == 0:
                    zeros += 1
                else:
                    mask |= 1 << c[x]
            require(zeros <= 1 and mask == 3, 'partial field AP must mix')
            if zeros:
                visiting += 1
            else:
                avoiding += 1
    return {'schema': 'character617-base-v1', 'agent': 'six-vdw-3', 'role': 'researcher',
            'prime': P, 'character_ascii_sha256': hashlib.sha256(bytes(48 + x for x in c[1:])).hexdigest(),
            'endpoint_steps_examined': P - 1, 'endpoint_unit_supports': rows,
            'five_disjoint_support_indices': list(range(5)),
            'support_union': vertices, 'support_inverses': inverse, 'reciprocal_overlap': overlap,
            'undirected_ratio_set': sorted(set(vertices) | set(inverse)),
            'minimum_hitting_number': 5, 'minimum_covers': len(covers),
            'minimum_covers_sha256': digest(covers), 'minimum_cover_union': cover_union,
            'field_start_step_pairs': P * (P - 1), 'root_avoiding_pairs': avoiding,
            'root_visiting_pairs': visiting, 'partial_monochromatic_pairs': 0,
            'offset_control': {'minus_one': c[P - 1], 'one': c[1], 'three': c[3]},
            'root_words_at_3703': 2 ** 7 - 2, 'palettes': 2, 'actual_restricted_3703_colorings': 252}


def lattice():
    vertices = {x for e in endpoints() for x in e['support']}
    ratios = vertices | {pow(v, -1, P) for v in vertices}
    squares = sorted(x for x in range(1, P) if pow(x, 308, P) == 1)
    neighbors = {q: {q * d % P for d in ratios} for q in squares}
    seed = frozenset(ratios)
    seen = {seed}
    todo = [seed]
    transitions = 0
    while todo:
        current = todo.pop()
        for q in squares:
            other = frozenset(current & neighbors[q])
            if len(other) >= 10:
                transitions += 1
                if other not in seen:
                    seen.add(other)
                    todo.append(other)
    records = []
    histogram = {}
    for b in sorted(seen, key=lambda s: tuple(sorted(s))):
        a = [q for q in squares if b <= neighbors[q]]
        require(len(a) <= 4, 'no five by ten biclique')
        histogram[str(len(a))] = histogram.get(str(len(a)), 0) + 1
        records.append({'B': sorted(b), 'A': a})
    return {'schema': 'character617-lattice-v1', 'prime': P, 'minimum_B_size': 10,
            'first_square_vertex': 1, 'square_vertices': len(squares), 'nonsquare_vertices': 308,
            'ratio_degree': len(ratios), 'states': len(records), 'retained_transitions': transitions,
            'A_histogram': histogram, 'maximum_A': max(map(int, histogram)),
            'state_records_sha256': digest(records), 'records': records}


def lift(n, start, stop):
    require(n in (3702, 3704) and 1 <= start <= stop <= n, 'lift range')
    h = hashlib.sha256()
    forward = backward = 0
    for m in range(start, stop + 1):
        for d in range(1, P):
            if m + 6 * d <= n:
                a, step, slot = m, d, 0
                forward += 1
            else:
                a, step, slot = m - 6 * (P - d), P - d, 6
                backward += 1
            require(a >= 1 and a + 6 * step <= n, 'actual interval bounds')
            require(a + slot * step == m and 1 <= step < P, 'endpoint')
            require(all((a + (j if slot == 0 else 6 - j) * step) % P
                        == (m + j * d) % P for j in range(7)), 'literal residue lift')
            h.update(struct.pack('<5H', m, d, a, step, slot))
    return {'schema': 'character617-lift-v1', 'prime': P, 'interval': n, 'start': start, 'stop': stop,
            'actual_endpoint_pairs': (stop - start + 1) * (P - 1),
            'forward_APs': forward, 'backward_APs': backward, 'actual_lifts_sha256': h.hexdigest()}


def transport(start, stop):
    require(0 <= start <= stop < P, 'root range')
    c = character()
    h = hashlib.sha256()
    for r in range(start, stop + 1):
        for alpha in range(1, P):
            q = (r + alpha) % P
            points = [(r + alpha * (1 + j * d)) % P for d in STEPS[:5] for j in range(1, 7)]
            require(len(set(points)) == 30 and r not in points and q not in points, 'disjoint transport')
            require(all(c[(t - r) % P] == (c[alpha] ^ 1) for t in points), 'opposite color')
            h.update(struct.pack('<33H', r, q, alpha, *points))
    cases = (stop - start + 1) * (P - 1)
    return {'schema': 'character617-transport-v1', 'prime': P, 'start': start, 'stop': stop,
            'root_target_parameters': cases, 'literal_support_columns': cases * 30,
            'transport_sha256': h.hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=('base', 'lattice', 'lift', 'transport'))
    parser.add_argument('--interval', type=int, default=3704)
    parser.add_argument('--start', type=int)
    parser.add_argument('--stop', type=int)
    parser.add_argument('--output', type=Path, required=True)
    a = parser.parse_args()
    result = {'base': base, 'lattice': lattice,
              'lift': lambda: lift(a.interval, a.start, a.stop),
              'transport': lambda: transport(a.start, a.stop)}[a.stage]()
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, sort_keys=True))


if __name__ == '__main__':
    main()

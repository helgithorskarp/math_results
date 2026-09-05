"""Complete one-component Kempe census from the 42 published potentials."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / 'hadwiger_nelson_heptagon_difference_lifts'
sys.path.insert(0, str(PARENT))
import geometry as F

GRAPH_HASH = '54a68876eb8c55d885905482b8373c5542651f7683bf66d4406ce44825563458'


def components(adj, c, a, b):
    left = {i for i, v in enumerate(c) if v in (a, b)}
    while left:
        root = min(left)
        left.remove(root)
        queue = [root]
        for v in queue:
            for u in sorted(adj[v] & left):
                left.remove(u)
                queue.append(u)
        yield sorted(queue)


def normalize(c, anchors):
    values = [c[v] for v in anchors]
    assert len(set(values)) == 3
    values += sorted(set(range(4)) - set(values))
    table = {v: i for i, v in enumerate(values)}
    return bytes(table[v] for v in c)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph-work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(exist_ok=False, parents=True)
    start = time.perf_counter()
    raw = (args.graph_work / 'graph.json').read_bytes()
    assert sha256(raw).hexdigest() == GRAPH_HASH
    g = json.loads(raw)
    points = list(map(tuple, g['points']))
    host = list(map(tuple, g['host']))
    index = {v: i for i, v in enumerate(points)}
    origin = index[F.ZERO]
    anchors = [origin, index[F.sub(host[7], host[0])],
               index[F.sub(host[14], host[0])]]
    support = {index[F.sub(a, b)]: (i, j)
               for i, a in enumerate(host) for j, b in enumerate(host) if i != j}
    assert len(support) == 420 and origin not in support
    potentials = json.loads((PARENT / 'potentials.json').read_text())
    seeds = []
    for row in potentials:
        c = [0] * len(points)
        for v, (a, b) in support.items():
            c[v] = row[a] ^ row[b]
        c = normalize(c, anchors)
        assert all(c[u] != c[v] for u, v in g['edges'])
        assert all(c[u] != c[v] for u, v in g['sqrt3_pairs'])
        seeds.append(c)
    assert len(set(seeds)) == 42
    seedset = set(seeds)
    adj = [set() for _ in points]
    for u, v in g['edges']:
        adj[u].add(v)
        adj[v].add(u)
    records, outcomes = [], set()
    size_counts = Counter()
    opposite = [index[F.neg(v)] for v in points]
    for si, c in enumerate(seeds):
        for a, b in combinations(range(4), 2):
            for component in components(adj, c, a, b):
                size_counts[len(component)] += 1
                d = bytearray(c)
                for v in component:
                    d[v] ^= a ^ b
                d = normalize(d, anchors)
                assert all(d[u] != d[v] for u, v in g['edges'])
                outcomes.add(d)
                records.append({
                    'seed': si, 'colours': [a, b], 'component': component,
                    'row_sha256': sha256(d).hexdigest(),
                    'potential': d in seedset,
                    'antipodal': all(d[v] == d[opposite[v]] for v in range(len(d))),
                    'monochromatic_pairs': [p for p in g['sqrt3_pairs'] if d[p[0]] == d[p[1]]]
                })
    covered = {tuple(p) for rec in records for p in rec['monochromatic_pairs']}
    residual = set(map(tuple, g['sqrt3_pairs'])) - covered
    rotate = [index[F.mul(F.POW[3], v)] for v in points]
    assert sorted(rotate) == list(range(421))
    edge_set = set(map(tuple, g['edges']))
    assert {tuple(sorted((rotate[a], rotate[b]))) for a, b in edge_set} == edge_set
    orbits, witnesses = [], []
    left = set(map(tuple, g['sqrt3_pairs']))
    while left:
        pair = min(left)
        orbit, current = set(), pair
        while current not in orbit:
            orbit.add(current)
            current = tuple(sorted(rotate[v] for v in current))
        assert current == pair and orbit <= left and len(orbit) == 14
        left -= orbit
        assert orbit <= covered or orbit <= residual
        orbits.append({'representative': list(pair), 'size': len(orbit),
                       'covered': orbit <= covered})
        if orbit <= covered:
            choices = [r for r in records if list(pair) in r['monochromatic_pairs']]
            best = min(choices, key=lambda r: (len(r['component']), r['seed'],
                                              r['colours'], r['component']))
            witnesses.append({'terminal_pair': list(pair), 'potential': potentials[best['seed']],
                              **{k: best[k] for k in ['seed', 'colours', 'component', 'row_sha256']}})
    # Describe the exact remaining set, without asserting any ordinary forcing.
    residual_vertices = {v for pair in residual for v in pair}
    triples = []
    for u in sorted(residual_vertices):
        neighbors = sorted(v for v in residual_vertices if tuple(sorted((u, v))) in residual)
        assert len(neighbors) == 2 and tuple(neighbors) in residual
        if u < neighbors[0]:
            tri = [u] + neighbors
            assert all(F.norm(points[v]) == F.scale(F.ONE, 49) for v in tri)
            assert tuple(sum(points[v][k] for v in tri) for k in range(12)) == F.ZERO
            triples.append(tri)
    out = {
        'graph_sha256': GRAPH_HASH, 'vertices': 421, 'unit_edges': 1848,
        'anchor_labels': anchors, 'normalized_seeds': len(seeds),
        'single_component_swaps': len(records),
        'component_size_histogram': {str(k): v for k, v in sorted(size_counts.items())},
        'distinct_normalized_outcomes': len(outcomes),
        'potential_outcomes': len(outcomes & seedset),
        'nonpotential_outcomes': len(outcomes - seedset),
        'nonantipodal_outcomes': sum(not r['antipodal'] for r in records),
        'antipodal_nonpotential_outcomes': sum(r['antipodal'] and not r['potential'] for r in records),
        'swaps_with_monochromatic_sqrt3_pair': sum(bool(r['monochromatic_pairs']) for r in records),
        'covered_pairs': [list(p) for p in sorted(covered)],
        'unresolved_pairs': [list(p) for p in sorted(residual)],
        'sqrt3_pair_orbits': orbits, 'residual_triangles': triples,
        'post_swap_edges_checked': len(records) * len(g['edges']),
        'post_swap_designated_pairs_checked': len(records) * len(g['sqrt3_pairs']),
        'normalized_outcome_stream_sha256': sha256(b''.join(sorted(outcomes))).hexdigest()
    }
    for name, data in [('result.json', out), ('witnesses.json', witnesses), ('records.json', records)]:
        (args.out / name).write_text(json.dumps(data, indent=2) + '\n')
    (args.out / 'timing.json').write_text(json.dumps({'seconds': time.perf_counter()-start})+'\n')
    print(json.dumps({k: v for k, v in out.items() if k not in
                      ['covered_pairs', 'unresolved_pairs', 'residual_triangles']}, indent=2))


if __name__ == '__main__':
    main()

"""Bounded two-step census; no third layer is generated or searched."""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time

from run import components, normalize, PARENT, GRAPH_HASH


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph-work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    raw = (args.graph_work / 'graph.json').read_bytes()
    assert sha256(raw).hexdigest() == GRAPH_HASH
    g = json.loads(raw)
    pts = list(map(tuple, g['points']))
    lookup = {p: i for i, p in enumerate(pts)}
    host = g['host']
    sub = lambda a, b: tuple(x-y for x, y in zip(a, b))
    origin = lookup[(0,)*12]
    anchors = [origin, lookup[sub(host[7], host[0])], lookup[sub(host[14], host[0])]]
    support = {lookup[sub(a, b)]: (i, j) for i, a in enumerate(host)
               for j, b in enumerate(host) if i != j}
    adj = [set() for _ in pts]
    for u, v in g['edges']:
        adj[u].add(v); adj[v].add(u)
    parent_result = json.loads((Path(__file__).parent / 'expected.json').read_text())
    targets = parent_result['unresolved_pairs']
    seeds = json.loads((PARENT / 'potentials.json').read_text())
    first_rows, provenance = [], []
    for si, p in enumerate(seeds):
        c = [0]*421
        for v, (a, b) in support.items():
            c[v] = p[a] ^ p[b]
        assert all(c[u] != c[v] for u, v in g['edges'])
        for a, b in combinations(range(4), 2):
            for block in components(adj, c, a, b):
                d = bytearray(c)
                for v in block:
                    d[v] ^= a ^ b
                d = normalize(d, anchors)
                assert all(d[u] != d[v] for u, v in g['edges'])
                assert all(d[u] != d[v] for u, v in targets)
                first_rows.append(d)
                provenance.append([si, a, b, block])
    assert len(first_rows) == len(set(first_rows)) == 1260
    first_hash = sha256(b''.join(sorted(first_rows))).hexdigest()
    assert first_hash == parent_result['normalized_outcome_stream_sha256']
    decompositions = []
    covered = set()
    checks = count = 0
    # The criterion is exact for any union of components of one colour pair.
    for c in first_rows:
        groups = []
        for a, b in combinations(range(4), 2):
            blocks = list(components(adj, c, a, b))
            groups.append(blocks)
            count += len(blocks)
            label = {v: i for i, block in enumerate(blocks) for v in block}
            for u, v in targets:
                checks += 1
                if {c[u], c[v]} == {a, b} and label[u] != label[v]:
                    covered.add((u, v))
        decompositions.append(groups)
    # Store full component partitions locally for entrywise comparison.
    trace = {'first_provenance': provenance, 'second_partitions': decompositions}
    encoded = (json.dumps(trace, separators=(',', ':'))+'\n').encode()
    (args.out / 'decompositions.json').write_bytes(encoded)
    result = {
        'scope': 'One component swap, then one component swap; no third step.',
        'graph_sha256': GRAPH_HASH, 'seed_count': len(seeds),
        'distinct_first_rows': len(first_rows),
        'first_row_stream_sha256': first_hash,
        'second_colour_pair_decompositions': len(first_rows)*6,
        'second_components': count,
        'residual_pairs_tested': len(targets),
        'pair_criterion_checks': checks,
        'newly_covered_pairs': [list(p) for p in sorted(covered)],
        'remaining_pairs': [p for p in targets if tuple(p) not in covered],
        'component_trace_sha256': sha256(encoded).hexdigest(),
        'component_trace_bytes': len(encoded)
    }
    (args.out / 'result.json').write_text(json.dumps(result, indent=2)+'\n')
    (args.out / 'timing.json').write_text(json.dumps({'seconds': time.perf_counter()-started})+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'remaining_pairs'}, indent=2))


if __name__ == '__main__':
    main()

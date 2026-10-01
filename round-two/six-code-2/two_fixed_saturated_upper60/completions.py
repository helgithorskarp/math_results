"""Exact residual clique search on the complete 39 two-fixed saturated anchors.

Uses the author's published coloring implementation as a search tool. Every
resource graph is compared with the direct word-intersection graph entrywise.
Incomplete cases leave individual compact resumable files and no upper bound.
"""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
import argparse
import json
import sys
import time
import model as M
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'free_involution_upper68'))
import color
import joint


def residual_graph(words, resources, rows):
    leftover = M.residual(words, resources, rows)
    M.require(all(r['weight'] == 2 and r['replications'][16:] == (0, 0) for r in leftover),
              'residual orbit domain')
    vertices = tuple(r['representative'] for r in leftover)
    sets = tuple(frozenset(r['resources']) for r in leftover)
    adjacency = tuple(sum(1 << j for j in range(len(leftover)) if i != j and not sets[i] & sets[j])
                      for i in range(len(leftover)))
    literal_vertices, literal_adj = joint.residual(words, M.G, 16)
    M.require(vertices == literal_vertices and adjacency == literal_adj,
              'residual resource graph differs from direct word-intersection graph')
    return leftover, adjacency


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stars', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.stars.read_text())
    M.require(data['status'] == 'COMPLETE exact Y-star census', 'incomplete input census')
    args.work.mkdir(parents=True, exist_ok=True)
    resources, rows = M.orbit_carrier()
    records = []
    for i, anchor in enumerate(data['anchors']):
        path = args.work / f'case-{i:02}.json'
        started = time.monotonic()
        words = tuple(anchor['words'])
        M.check_code(words)
        leftover, adjacency = residual_graph(words, resources, rows)
        graph_hash = sha256(M.encoded(dict(vertices=[r['representative'] for r in leftover],
                                         adjacency=adjacency))).hexdigest()
        if path.exists():
            record = json.loads(path.read_text())
            M.require(record['graph_sha256'] == graph_hash and record['status'] == 'COMPLETE',
                      'bad saved residual checkpoint')
            maxima = tuple(tuple(q) for q in json.loads(path.with_suffix('.maxima.json').read_text()))
            alpha = record['alpha']
        else:
            alpha, maxima, nodes = color.maximum_cliques(adjacency)
            M.require(maxima and all(len(q) == len(set(q)) == alpha and
                      all(adjacency[a] >> b & 1 for a,b in combinations(q, 2)) for q in maxima),
                      'color search decoded invalid maximum')
            witness = tuple(sorted(words + tuple(w for j in maxima[0] for w in leftover[j]['words'])))
            stats = M.check_code(witness)
            M.require(len(witness) == 36 + 2*alpha and stats['replications'][16:] == (20, 20),
                      'residual witness decoding')
            record = dict(status='COMPLETE', case=i, fixture=anchor['fixture'], matching=anchor['matching'],
                          vertices=len(adjacency), alpha=alpha, maximum_families=len(maxima),
                          words=36 + 2*alpha, color_nodes=nodes, graph_sha256=graph_hash,
                          maxima_sha256=sha256(M.encoded(maxima)).hexdigest(),
                          witness=witness, seconds=time.monotonic() - started)
            path.with_suffix('.maxima.json').write_bytes(M.encoded(maxima))
            path.write_bytes(M.encoded(record))
        print(json.dumps({k:v for k,v in record.items() if k != 'witness'}, sort_keys=True), flush=True)
        records.append(record)
    args.work.joinpath('summary.json').write_bytes(M.encoded(dict(status='COMPLETE author coloring census',
                                                                  cases=len(records), records=records)))
    print('COMPLETE', len(records), 'cases, bound', max(r['words'] for r in records), flush=True)


if __name__ == '__main__':
    main()

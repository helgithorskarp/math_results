"""Find a K5, I5, or inducedC5 on any input graph of order at least42."""
import argparse
import itertools as it
import json
from pathlib import Path


def graph(data):
    if set(data) != {'n', 'edges'} or type(data['n']) is not int or data['n'] < 42:
        raise ValueError('requires a simple graph of order at least42')
    n = data['n']
    adj = [0] * n
    seen = set()
    for pair in data['edges']:
        if len(pair) != 2 or any(type(x) is not int for x in pair):
            raise ValueError('edge endpoints')
        u, v = pair
        if not 0 <= u < v < n or (u, v) in seen:
            raise ValueError('edge order/range/duplicate')
        seen.add((u, v)); adj[u] |= 1 << v; adj[v] |= 1 << u
    return n, adj


def extract(data):
    n, adj = graph(data)
    full = (1 << n)-1
    rows = [adj, [full ^ (1 << v) ^ adj[v] for v in range(n)]]
    anchor = None
    for u in range(n):
        for v in range(u+1, n):
            color = 0 if adj[u] >> v & 1 else 1
            common = rows[color][u] & rows[color][v]
            if common.bit_count() >= 10:
                anchor = (u, v, color, common)
                break
        if anchor is not None:
            break
    if anchor is None:
        raise RuntimeError('Goodman identity violated: no qualifying edge')
    u, v, color, mask = anchor
    ten = [i for i in range(n) if mask >> i & 1][:10]
    colored = rows[color]
    provenance = {'anchor': [u, v], 'anchor_color': 'red' if color == 0 else 'blue',
                  'common_neighbors': ten, 'common_count': mask.bit_count()}
    def clique(q, edge=True):
        return all(bool(colored[a] >> b & 1) == edge for a, b in it.combinations(q, 2))
    for q in it.combinations(ten, 3):
        if clique(q):
            return dict(provenance, kind='monochromatic5', color=provenance['anchor_color'], vertices=[u, v, *q])
    for q in it.combinations(ten, 5):
        if clique(q, False):
            return dict(provenance, kind='monochromatic5', color='blue' if color == 0 else 'red', vertices=list(q))
    for q in it.combinations(ten, 5):
        if all(sum(colored[a] >> b & 1 for b in q if a != b) == 2 for a in q):
            return dict(provenance, kind='induced_C5', vertices=list(q))
    raise RuntimeError('order10 structural lemma violated')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('graph', type=Path); a = p.parse_args()
    print(json.dumps(extract(json.loads(a.graph.read_text())), sort_keys=True, indent=2))

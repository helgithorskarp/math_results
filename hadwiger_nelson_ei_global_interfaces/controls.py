"""Small truth-table, proof-rejection, and witness-rejection controls."""
import copy
from itertools import combinations, product
import json
from pathlib import Path
import tempfile
import geometry as G
import lrat
from verify import witnesses


def main():
    assignments = 0
    for n in (2, 3):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            edges = [e for k, e in enumerate(possible) if mask >> k & 1]
            for triples in ([[], [(0, 1, 2)]] if n == 3 else [[]]):
                clauses = G.cnf(n, edges, triples, [0, 1])
                for word in product(range(4), repeat=n):
                    model = {4*v+c+1: word[v] == c for v in range(n) for c in range(4)}
                    encoded = all(any(model[abs(lit)] == (lit > 0) for lit in c) for c in clauses)
                    direct = word[0] == 0 and word[1] == 1 and all(word[u] != word[v] for u, v in edges) and all(len({word[v] for v in t}) > 1 for t in triples)
                    G.require(encoded == direct, 'encoding control')
                    assignments += 1
    rejected = 0
    def reject(call):
        nonlocal rejected
        try:
            call()
        except (ValueError, TypeError):
            rejected += 1
            return
        raise ValueError('malformed control was accepted')
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / 'proof.lrat'
        path.write_text('3 0 1 2 0\n')
        G.require(lrat.verify([[1], [-1]], 1, path)['empty_clause'], 'valid RUP control')
        path.write_text('5 2 0 1 2 0\n6 -2 0 3 4 0\n7 0 5 6 0\n')
        G.require(lrat.verify([[1, 2], [-1, 2], [1, -2], [-1, -2]], 2, path)['empty_clause'],
                  'nonempty RUP derivation control')
        for text in ['3 0 1 0\n', '3 0 2 0\n', '3 0 1 7 0\n', '3 0 -1 2 0\n',
                     '2 0 1 2 0\n', '3 0 1 2 1 0\n', '2 d 1 0\n3 0 1 2 0\n',
                     '3 2 0 1 2 0\n', '3 1 -1 0 1 2 0\n', '']:
            path.write_text(text)
            reject(lambda: lrat.verify([[1], [-1]], 1, path))
        path.write_text('2 0 1 0\n')
        reject(lambda: lrat.verify([[1, 2]], 2, path))
    points, triangles, pins = G.half_layer()
    edges = G.edges(points)
    original = G.read(G.ROOT / 'certificate.json')
    for change in ('word', 'duplicate', 'missing', 'pins', 'metadata'):
        bad = copy.deepcopy(original)
        if change == 'word':
            bad['deletion_colourings'][0] = '0' * len(points)
        elif change == 'duplicate':
            bad['selected_triangles'][0] = bad['selected_triangles'][1]
        elif change == 'missing':
            bad['deletion_colourings'].pop()
        elif change == 'pins':
            bad['pins'].reverse()
        else:
            bad['mask'] = 151
        reject(lambda: witnesses(bad, len(points), edges, triangles, pins))
    print(json.dumps({'encoding_assignments': assignments, 'valid_RUP_fixtures': 2,
                      'malformed_controls_rejected': rejected}, sort_keys=True))


if __name__ == '__main__':
    main()

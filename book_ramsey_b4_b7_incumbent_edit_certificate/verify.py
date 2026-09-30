"""Check every listed graph and its two contradictory implication paths.

This small checker does not enumerate the edit ball. Supply enumeration outputs
to additionally compare their complete survivor lists to the compact certificate.
"""
import argparse
import ast
import hashlib
import itertools
import json
from pathlib import Path

if not __debug__:
    raise SystemExit('Run with Python assertions enabled, without -O')


def verify(directory, reports):
    base = json.loads((directory / 'h21.json').read_text())
    cert = json.loads((directory / 'certificate.json').read_text())
    n = base['n']
    assert n == 21
    assert len(base['red_edges']) == len(set(map(tuple, base['red_edges'])))
    assert all(0 <= u < v < n for u, v in base['red_edges'])
    edges = list(itertools.combinations(range(n), 2))
    raw_sets = [g['edits'] for g in cert['graphs']]
    canonical = sorted(raw_sets, key=lambda s: (len(s), s))
    assert raw_sets == canonical
    assert len(set(map(tuple, raw_sets))) == len(raw_sets)
    digest = hashlib.sha256(json.dumps(raw_sets, separators=(',', ':')).encode()).hexdigest()
    assert digest == cert['valid_sets_sha256']

    for graph in cert['graphs']:
        edits = graph['edits']
        assert edits == sorted(set(edits))
        assert all(0 <= i < len(edges) for i in edits)
        assert len(edits) <= cert['radius']
        red = set(map(tuple, base['red_edges'])) ^ {edges[i] for i in edits}
        adj = [set() for _ in range(n)]
        for u, v in red:
            adj[u].add(v)
            adj[v].add(u)

        def color(u, v):
            assert u != v
            return int(v in adj[u])

        def pages(u, v):
            c = color(u, v)
            return [w for w in range(n) if w not in (u, v)
                    and color(u, w) == c and color(v, w) == c]

        for u, v in edges:
            assert len(pages(u, v)) <= (3 if color(u, v) else 6)
        assert len(red) == graph['red_edge_count']
        p, q = graph['positive_to_negative'], graph['negative_to_positive']
        assert len(p) >= 2 and len(q) >= 2
        assert p[0] % 2 == 0 and p[-1] == (p[0] ^ 1)
        assert q[0] == p[-1] and q[-1] == p[0]
        for path in (p, q):
            assert all(type(literal) is int and 0 <= literal < 2 * n for literal in path)
            for a, b in zip(path, path[1:]):
                assert a % 2 != b % 2
                u, v = a // 2, b // 2
                c = 1 - (a % 2)
                assert color(u, v) == c
                assert len(pages(u, v)) == (3 if c else 6)

    for report_path in reports:
        result = json.loads(report_path.read_text())
        assert result['complete'] is True
        assert result['radius'] == cert['radius']
        assert result['valid_edge_index_sets'] == raw_sets
        assert result['valid_sets_sha256'] == digest
    print(f"Verified {len(raw_sets)} valid graphs and all extension contradictions; "
          f"radius={cert['radius']}; survivor_sha256={digest}; "
          f"complete_enumeration_outputs_compared={len(reports)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reports', nargs='*', type=Path)
    parser.add_argument('--source-matrix', type=Path)
    args = parser.parse_args()
    if args.source_matrix:
        raw = args.source_matrix.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == (
            '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55')
        text = raw.decode()
        matrix = ast.literal_eval(text[:text.index('\n\n')])
        base = json.loads(Path(__file__).with_name('h21.json').read_text())
        n = base['n']
        assert len(matrix) == n and all(len(row) == n for row in matrix)
        assert all(matrix[u][u] == 0 for u in range(n))
        assert all(matrix[u][v] == matrix[v][u] and matrix[u][v] in (0, 1)
                   for u in range(n) for v in range(n))
        assert base['red_edges'] == [[u, v] for u in range(n)
                                     for v in range(u + 1, n) if matrix[u][v] == 0]
        print('Primary source byte hash and complemented red-edge fixture agree')
    verify(Path(__file__).parent, args.reports)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Small literal clique controls and physical decoding boundary cases."""
import argparse
from itertools import combinations
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from verify import decode, edge_bytes, family, literal_defects, need, read_graph, recursive_defects


def reject(fn):
    try:
        fn()
    except ValueError:
        return
    raise ValueError('invalid control accepted')


def run():
    graphs = 0
    for n in range(1, 6):
        pairs = list(combinations(range(n), 2))
        for code in range(1 << len(pairs)):
            rows = [0]*n
            for i, (u, v) in enumerate(pairs):
                if code & (1 << i):
                    rows[u] |= 1 << v
                    rows[v] |= 1 << u
            need(literal_defects(rows) == recursive_defects(rows), 'small clique control')
            graphs += 1
    baseline = decode('0'*287)
    for v in range(287):
        word = '0'*v+'1'+'0'*(286-v)
        rows = decode(word)
        need(family(rows) == word, 'single-orbit round trip')
        difference = [(a, b) for a, b in combinations(range(43), 2)
                      if ((rows[a] ^ baseline[a]) >> b) & 1]
        need(len(difference) == 3, 'three physical changed pairs')
    bad = baseline.copy()
    bad[0] ^= 1 << 3
    bad[3] ^= 1
    reject(lambda: family(bad))
    bad_internal = baseline.copy()
    for a, b in combinations(range(3), 2):
        bad_internal[a] ^= 1 << b
        bad_internal[b] ^= 1 << a
    reject(lambda: family(bad_internal))
    reject(lambda: decode('0'*286))
    reject(lambda: decode('2'+'0'*286))
    with TemporaryDirectory(prefix='c3-fourteen-controls-') as tmp:
        p = Path(tmp)/'bad.edges'
        for text in ('42\n', '43\n0 1\n0 1\n', '43\n0 43\n', '43\n1 2\n0 1\n'):
            p.write_text(text)
            reject(lambda: read_graph(p))
        p.write_bytes(edge_bytes(baseline))
        need(read_graph(p) == baseline, 'physical file round trip')
    return {'status': 'PASS', 'small_literal_graphs': graphs,
            'all_single_orbit_controls': 287, 'rejected_cases': 8}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = run()
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))

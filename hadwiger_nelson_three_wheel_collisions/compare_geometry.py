#!/usr/bin/env python3
"""Optional independent labelled-difference reconstruction; no SAT calls."""
from pathlib import Path
import hashlib
import json
import time
from produce import CASES, construct

HERE = Path(__file__).resolve().parent


def main():
    expected = json.loads((HERE/'EXPECTED.json').read_text())
    rows = []
    start = time.monotonic()
    for case, record in zip(CASES, expected['unaligned_congruence_classes']):
        points, edges, ids = construct(case)
        def sha(x):
            return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()
        if sha(points) != record['point_sha256'] or sha(edges) != record['edge_sha256']:
            raise ValueError('independent geometry mismatch')
        rows.append({'norms': case, 'point_entries': len(points), 'edge_entries': len(edges),
                     'entry_level_hashes_match': True})
    print(json.dumps({'independent_geometry': rows, 'seconds': time.monotonic()-start,
                      'SAT_calls': 0}, indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Definition-level cube checker. Imports no constructor or template code."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path


def verify(data: dict) -> dict:
    n = data['dimension']
    if type(n) is not int or not 1 <= n <= 20:
        raise ValueError('invalid dimension')
    masks = data['adjacency_masks']; N = 1 << n
    if len(masks) != N:
        raise ValueError('wrong number of vertices')
    neighbors = []
    for u, mask in enumerate(masks):
        if type(mask) is not int or not 0 <= mask < N:
            raise ValueError('invalid direction mask')
        neighbors.append({u ^ (1 << i) for i in range(n) if mask & (1 << i)})
    for u, ns in enumerate(neighbors):
        for v in ns:
            if u not in neighbors[v]:
                raise ValueError('asymmetric edge')
    # A square is exactly two distinct length-two paths with the same ends.
    for u, ns in enumerate(neighbors):
        ends = set()
        for v in ns:
            for w in neighbors[v]:
                if w == u:
                    continue
                if w in ends:
                    raise ValueError('square present')
                ends.add(w)
    selected = missing = 0
    digest = hashlib.sha256()
    for u, ns in enumerate(neighbors):
        for i in range(n):
            v = u ^ (1 << i)
            if v < u:
                continue
            if v in ns:
                selected += 1
                digest.update(f'{u} {v}\n'.encode('ascii'))
            else:
                missing += 1
                if not any(neighbors[a] & neighbors[v] for a in ns):
                    raise ValueError('missing edge has no length-three path')
    if selected + missing != n * (N // 2):
        raise RuntimeError('host count mismatch')
    return {'dimension':n,'selected_edges_checked':selected,
            'missing_edges_checked':missing,'edge_sha256':digest.hexdigest()}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('witness',type=Path)
    args = p.parse_args()
    print(json.dumps(verify(json.loads(args.witness.read_text())),sort_keys=True))


if __name__ == '__main__':
    main()

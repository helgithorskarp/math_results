#!/usr/bin/env python3
"""Check the complete colouring, its deterministic construction, and pinned incidence data."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import argparse
import json
import construct as C


def verify(work):
    data, host = C.load(work)
    G = C.pinned_import('dense_geometry', C.PRIOR / 'geometry.py', C.GEOMETRY_PIN)
    _, _, hedges = G.distances(G.host())
    C.require(G.digest(hedges) == '11af24079955c011d7ac15812b93f273044f94ce303281676abff341f33cf21a', 'host edges')
    C.check_colors(host, [15] * 506, hedges)
    available = [sum(1 << c for c in range(4) if all(host[v] != c for v in nn))
                 for nn in data['neighbors']]
    C.require(available == data['available_masks'], 'host list reconstruction')
    added, summary = C.extend_lists(available, data['candidate_edges'])
    colors = C.read_colors(C.HERE / 'colors.txt', 1926)
    C.require(colors == host + added, 'deterministic colouring mismatch')
    edges = sorted(hedges + [(v, 506 + i) for i, nn in enumerate(data['neighbors']) for v in nn]
                   + [(506 + i, 506 + j) for i, j in data['candidate_edges']])
    C.check_colors(colors, [15] * len(colors), edges)
    return {
        'vertices': len(colors), 'edges': len(edges),
        'edge_sha256': C.digest(edges),
        'colour_sha256': sha256((C.HERE / 'colors.txt').read_bytes()).hexdigest(),
        'colour_class_sizes': dict(sorted(Counter(colors).items())),
        'preserved_host_colouring': True,
        'candidate_points': len(data['points']),
        'host_edges': len(hedges),
        'host_candidate_edges': sum(map(len, data['neighbors'])),
        'candidate_edges': len(data['candidate_edges']),
        'construction': summary,
        'monochromatic_edges': 0,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(verify(args.work), indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Build the complete compatibility graph and check its path decomposition."""
from collections import Counter
from math import comb
from pathlib import Path
import argparse
import json
import engine as E


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work', type=Path, required=True)
    args = p.parse_args()
    args.work.mkdir(parents=True, exist_ok=False)
    host, colors = E.load()
    fibres, edges, tested, zero_dot = E.build(host, colors)
    paths, incident = E.path_components(edges)
    histogram = sorted(Counter(map(len, paths)).items())
    E.require(histogram == E.read_certificate(), 'path-type certificate mismatch')
    for name, data in [('fibres', fibres), ('edges', edges), ('paths', paths)]:
        (args.work / (name + '.json')).write_text(json.dumps(data, separators=(',', ':')) + '\n')
    result = {
        'host_vertices': len(host), 'host_edges': 2389,
        'differently_coloured_host_pairs': sum(len(ps) for _, ps in fibres),
        'midpoint_palette_fibres': len(fibres),
        'host_pair_pairs_tested': tested,
        'host_pair_triples_in_fibres': sum(comb(len(ps), 3) for _, ps in fibres),
        'compatibility_edges': len(edges), 'zero_dot_compatible_pairs': zero_dot,
        'incident_vertices': incident, 'nontrivial_components': len(paths),
        'path_order_histogram': dict(histogram), 'compatibility_triangles': 0,
        'fibres_sha256': E.G.digest(fibres), 'edges_sha256': E.G.digest(edges),
        'paths_sha256': E.G.digest(paths),
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

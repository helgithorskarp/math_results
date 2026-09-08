#!/usr/bin/env python3
"""Produce compact exact cover and complete-template certificates."""
import argparse,json
from collections import Counter
from itertools import combinations
from pathlib import Path
import family


def produce():
    residues = {x*x % 53 for x in range(1,53)}
    seed = next(s for s in combinations(range(53),5)
                if all((v-u)%53 in residues for u,v in combinations(s,2)))
    translates = sorted({tuple(sorted((v+t)%53 for v in seed)) for t in range(53)})
    incidence = Counter(v for row in translates for v in row)
    classes = [[] for _ in range(54)]
    for u,v in combinations(range(53),2):
        classes[family.two_orbit_index(u,v)].append([u,v])
    return {'schema': 'r55-orbit-dense-deletion-v1',
            'paley53': {'seed': list(seed), 'color': 'red', 'translates': [list(s) for s in translates],
                        'vertex_incidence': [incidence[v] for v in range(53)],
                        'retained_vertex_count': 43, 'deleted_vertex_count': 10,
                        'cover_rows': len(translates), 'maximum_rows_hit_by_deletions': 50,
                        'minimum_surviving_rows': 3, 'farkas_left': 5*43,
                        'farkas_right': 4*53, 'farkas_gap': 3},
            'two_orbit53': {'generator': [(v//26)*26+(v+1)%26 if v < 52 else 52 for v in range(53)],
                            'vertex_orbits': [list(range(26)),list(range(26,52)),[52]],
                            'edge_classes': [{'index': i, 'representative': row[0], 'size': len(row)}
                                             for i,row in enumerate(classes)],
                            'selected_per_orbit': [21,21,1], 'deleted_per_orbit': [5,5,0],
                            'five_seed_translate_multiplicity': 26,
                            'maximum_total_deleted_incidence': 25,
                            'minimum_surviving_translate_multiplicity': 1},
            'inventory': family.inventory()}


def main():
    parser = argparse.ArgumentParser();parser.add_argument('--output', required=True);args = parser.parse_args()
    Path(args.output).write_text(json.dumps(produce(),indent=2,sort_keys=True)+'\n')


if __name__ == '__main__':
    main()

"""Standalone standard-library check of the new literal67 witness.

Imports no census, clique engine, graph decoder or earlier packing code.
The witness alone proves existence, not a maximum or census completeness.
"""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def check(data):
    require(data['words'] == 67 and type(data['blocks']) is list and len(data['blocks']) == 67,
            'literal67 word count')
    masks = data['blocks']
    require(all(type(mask) is int and 0 <= mask < (1 << 18) for mask in masks), 'literal mask domain')
    points = [tuple(i for i in range(18) if mask & (1 << i)) for mask in masks]
    require(all(len(word) == 5 for word in points) and len(set(points)) == 67, 'weight or distinctness')
    owners = {}
    for index, word in enumerate(points):
        for triple in combinations(word, 3):
            require(triple not in owners, 'repeated literal triple')
            owners[triple] = index
    require(len(owners) == 670, 'triple coverage count')
    intersection_census = Counter()
    for first, second in combinations(points, 2):
        common = sum(point in second for point in first)
        require(common <= 2, 'pairwise intersection bound')
        intersection_census[common] += 1
    degrees = [sum(point in word for word in points) for point in range(18)]
    actual_centers = [degrees[point] for point in (17, 15, 16)]
    actual_pairs = [sum(a in word and b in word for word in points)
                    for a, b in ((17, 15), (17, 16), (15, 16))]
    require(actual_centers == data['center_degrees'] == [19, 19, 20], 'literal center degrees')
    require(actual_pairs == data['pair_multiplicities'] == [5, 5, 4], 'literal pair multiplicities')
    require(not any(all(i in word for i in (15, 16, 17)) for word in points), 'covered center triple')
    require(sum(degrees) == 335, 'point incidence sum')
    return {'status': 'PASS_STANDALONE_LITERAL67', 'points': 18, 'words': 67,
            'distinct_triples': len(owners), 'center_degrees': actual_centers,
            'pair_multiplicities': actual_pairs, 'uncovered_center_triple': True,
            'point_degrees': degrees, 'degree_census': dict(sorted(Counter(degrees).items())),
            'intersection_census': dict(sorted(intersection_census.items()))}


def controls(data):
    bad = []
    changed = copy.deepcopy(data); changed['blocks'][1] = changed['blocks'][0]; bad.append(changed)
    changed = copy.deepcopy(data); changed['blocks'].pop(); bad.append(changed)
    changed = copy.deepcopy(data); changed['blocks'][0] |= 1 << 18; bad.append(changed)
    changed = copy.deepcopy(data); changed['blocks'][0] = sum(1 << i for i in (0, 1, 15, 16, 17)); bad.append(changed)
    changed = copy.deepcopy(data); changed['center_degrees'] = [19, 20, 20]; bad.append(changed)
    changed = copy.deepcopy(data); changed['pair_multiplicities'] = [5, 5, 5]; bad.append(changed)
    for changed in bad:
        try:
            check(changed)
        except ValueError:
            continue
        raise ValueError('damaged literal witness accepted')
    return len(bad)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fixture', type=Path)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    data = json.loads(args.fixture.read_text())
    result = check(data)
    result['fixture_sha256'] = hashlib.sha256(args.fixture.read_bytes()).hexdigest()
    if args.controls:
        result['damaged_controls_rejected'] = controls(data)
    print(json.dumps(result, sort_keys=True))

"""Exact normalized local census; six-books-3, researcher, 2026-10-01.

Python 3.11+, standard library. No possible 22-vertex host is enumerated.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

EDGES = tuple(itertools.combinations(range(8), 2))
EDGE_INDEX = {edge: bit for bit, edge in enumerate(EDGES)}
DEGREES = (2, 2, 2, 2, 3, 3, 3, 3)
FORBIDDEN = {(0, 1), (2, 3)}


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def enumerate_stars():
    """Choose every complete forward star, retaining exactly the degrees."""
    remaining = list(DEGREES)

    def visit(v, mask):
        if v == 8:
            if all(d == 0 for d in remaining):
                yield mask
            return
        candidates = [w for w in range(v + 1, 8)
                      if remaining[w] > 0 and (v, w) not in FORBIDDEN]
        wanted = remaining[v]
        if wanted < 0 or wanted > len(candidates):
            return
        for chosen in itertools.combinations(candidates, wanted):
            remaining[v] = 0
            next_mask = mask
            for w in chosen:
                remaining[w] -= 1
                next_mask |= 1 << EDGE_INDEX[v, w]
            if all(d >= 0 for d in remaining):
                yield from visit(v + 1, next_mask)
            for w in chosen:
                remaining[w] += 1
            remaining[v] = wanted

    yield from visit(0, 0)


def neighbors(mask):
    adjacency = [set() for _ in range(10)]
    for bit, (i, j) in enumerate(EDGES):
        if mask & (1 << bit):
            adjacency[i + 2].add(j + 2)
            adjacency[j + 2].add(i + 2)
    for low, pair in ((0, (2, 3)), (1, (4, 5))):
        for j in pair:
            adjacency[low].add(j)
            adjacency[j].add(low)
    need(tuple(map(len, adjacency)) == (2, 2) + (3,) * 8,
         'Wrong local degree vector')
    return adjacency


def pair_upper(adjacency):
    """S0 before nonnegative spine slack; diagonal is the miss count."""
    h = tuple(map(len, adjacency))
    return [[h[i] + 2 if i == j else
             h[i] + h[j] - (5 if j in adjacency[i] else 2)
             - len(adjacency[i] & adjacency[j])
             for j in range(10)] for i in range(10)]


def symmetry_group():
    blocks = {frozenset((0, 1)), frozenset((2, 3))}
    group = []
    for p in itertools.permutations(range(8)):
        if {frozenset(p[i] for i in b) for b in blocks} == blocks:
            group.append(p)
    need(len(group) == 192, 'Wrong alignment stabilizer')
    return group


def transform(mask, permutation):
    result = 0
    for bit, (i, j) in enumerate(EDGES):
        if mask & (1 << bit):
            image = tuple(sorted((permutation[i], permutation[j])))
            result |= 1 << EDGE_INDEX[image]
    return result


def mask_digest(values):
    data = ''.join(f'{m}\n' for m in sorted(values)).encode('ascii')
    return hashlib.sha256(data).hexdigest()


def run():
    raw_list = list(enumerate_stars())
    raw = set(raw_list)
    need(len(raw) == len(raw_list), 'Duplicate labeled graph')
    pair_admissible = set()
    eligible = set()
    triangle_free = set()
    for mask in raw:
        adjacency = neighbors(mask)
        if all(value >= 0 for row in pair_upper(adjacency) for value in row):
            pair_admissible.add(mask)
            if (adjacency[2] & adjacency[3]) != {0} or (adjacency[4] & adjacency[5]) != {1}:
                continue
            eligible.add(mask)
            if all(not (adjacency[i] & adjacency[j])
                   for i in range(10) for j in adjacency[i]):
                triangle_free.add(mask)

    group = symmetry_group()
    unseen = set(eligible)
    records = []
    while unseen:
        representative = min(unseen)
        orbit = {transform(representative, p) for p in group}
        need(orbit <= eligible, 'An orbit leaves the enumerated domain')
        unseen.difference_update(orbit)
        adjacency = neighbors(representative)
        triangles = sum(len(adjacency[i] & adjacency[j])
                        for i in range(10) for j in adjacency[i]) // 6
        records.append({
            'mask': representative,
            'orbit_size': len(orbit),
            'local_triangles': triangles,
            'triangle_free': representative in triangle_free,
            'neighbor_masks': [sum(1 << j for j in row) for row in adjacency],
        })
    summary = {
        'schema': 2,
        'alignment': {'low_neighbors': [[2, 3], [4, 5]],
                      'cubic_labels': list(range(2, 10)),
                      'mask_edges': [list(e) for e in EDGES]},
        'raw_labeled_count': len(raw),
        'pair_admissible_labeled_count': len(pair_admissible),
        'eligible_labeled_count': len(eligible),
        'triangle_free_labeled_count': len(triangle_free),
        'eligible_orbit_count': len(records),
        'triangle_free_orbit_count': sum(r['triangle_free'] for r in records),
        'stabilizer_order': len(group),
        'raw_masks_sha256': mask_digest(raw),
        'pair_admissible_masks_sha256': mask_digest(pair_admissible),
        'eligible_masks_sha256': mask_digest(eligible),
        'triangle_free_masks_sha256': mask_digest(triangle_free),
        'records': records,
    }
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true',
                        help='explicitly replace the compact catalogue')
    args = parser.parse_args()
    result = run()
    serialized = json.dumps(result, indent=2, sort_keys=True) + '\n'
    fixture = Path(__file__).with_name('cores.json')
    if args.write:
        fixture.write_text(serialized)
    else:
        need(fixture.read_text() == serialized, 'Catalogue differs from fresh census')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('alignment', 'records')}, sort_keys=True))


if __name__ == '__main__':
    main()

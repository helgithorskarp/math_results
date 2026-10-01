"""Helper-free inverse-anchor classification of all actual field triples."""
import argparse
from itertools import combinations, permutations
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def audit(path):
    data = json.loads(path.read_text())
    require(data['author'] == 'six-vdw-1' and data['role'] == 'researcher', 'author/role')
    classified = {}
    for triple in combinations(range(31), 3):
        anchors = {(last-first)*pow(second-first, -1, 31) % 31
                   for first, second, last in permutations(triple)}
        require(not anchors & {0, 1}, 'degenerate inverse anchor')
        classified.setdefault(min(anchors), set()).add(triple)
    require(sorted(classified) == [2, 3, 4, 5, 6, 12], 'incomplete inverse ratio quotient')
    seen = set()
    for orbit in data['classes']:
        holes = orbit['holes']
        require(len(holes) == 3 and holes == [0, 1, holes[-1]], 'canonical field triple')
        actual = [tuple(x) for x in orbit['members']]
        require(actual == sorted(set(actual)) and set(actual) == classified[holes[-1]], 'wrong field orbit members')
        require(len(actual) == orbit['orbit_size'] and not seen & set(actual), 'field orbit cardinality/overlap')
        seen.update(actual)
    require(seen == set(combinations(range(31), 3)), 'incomplete field triple cover')
    require(data['affine_group_order'] == 31*30 and data['labeled_triples'] == len(seen) == 4495
            and len(data['classes']) == 6, 'incorrect field coverage metadata')
    # Direct CRT arithmetic, independently of the producer's formula.
    crt_checks = 0
    for r in range(31):
        for s in range(20):
            solutions = [x for x in range(s, 620, 20) if x % 31 == r]
            require(len(solutions) == 1, 'CRT coordinate bijection')
            crt_checks += 1
    return {'status': 'COMPLETE_INVERSE_ANCHOR_FIELD_TRIPLE_COVER', 'triples': len(seen),
            'classes': [[0, 1, t] for t in sorted(classified)],
            'orbit_sizes': [len(classified[t]) for t in sorted(classified)], 'crt_checks': crt_checks}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('triples', type=Path)
    print(json.dumps(audit(parser.parse_args().triples), sort_keys=True), flush=True)

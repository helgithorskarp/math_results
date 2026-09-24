"""Exact checks and automorphisms of the imported 107-link catalogue."""
from collections import Counter
from itertools import combinations, permutations, product
import json
from pathlib import Path

CAT = json.loads((Path(__file__).resolve().parent / 'LINKS.json').read_text())


def move(mask, action):
    return sum(1 << action[p] for p in range(len(action)) if mask >> p & 1)


def point_automorphisms(design):
    """Permute low signatures, then block cells, then equal point signatures."""
    signatures = design['point_signatures']
    low = [s for s in signatures if s.bit_count() == 3]
    columns = [sum(1 << j for j, row in enumerate(low) if row >> b & 1) for b in range(9)]
    cells = {m: tuple(b for b, c in enumerate(columns) if c == m) for m in set(columns)}
    keys = sorted(cells)
    groups = {s: tuple(p for p, row in enumerate(signatures) if row == s) for s in set(signatures)}
    signature_keys = sorted(groups)
    answers = set()
    for perm in permutations(range(len(low))):
        cell_image = {m: move(m, perm) for m in keys}
        if any(cell_image[m] not in cells or len(cells[cell_image[m]]) != len(cells[m]) for m in keys):
            continue
        for bijections in product(*(permutations(cells[cell_image[m]]) for m in keys)):
            block_action = [None] * 9
            for m, targets in zip(keys, bijections):
                for old, new in zip(cells[m], targets):
                    block_action[old] = new
            row_image = {s: move(s, block_action) for s in signature_keys}
            if any(row_image[s] not in groups or len(groups[row_image[s]]) != len(groups[s]) for s in signature_keys):
                continue
            for choices in product(*(permutations(groups[row_image[s]]) for s in signature_keys)):
                action = [None] * 12
                for s, targets in zip(signature_keys, choices):
                    for old, new in zip(groups[s], targets):
                        action[old] = new
                answers.add(tuple(action))
    return sorted(answers)


def validate():
    if [d['id'] for d in CAT] != list(range(107)):
        raise ValueError('wrong catalogue index set')
    aut_count = 0
    for design in CAT:
        blocks = design['blocks']
        if len(blocks) != 9 or len(set(blocks)) != 9 or any(not 0 < b < 4096 or b.bit_count() != 5 for b in blocks):
            raise ValueError('malformed link blocks')
        if any(not any(b >> p & 1 and b >> q & 1 for b in blocks) for p, q in combinations(range(12), 2)):
            raise ValueError('link misses a pair')
        signatures = [sum(1 << j for j, b in enumerate(blocks) if b >> p & 1) for p in range(12)]
        if signatures != design['point_signatures'] or any(not 3 <= s.bit_count() <= 5 for s in signatures):
            raise ValueError('wrong link point signatures')
        actions = point_automorphisms(design)
        for action in actions:
            if set(action) != set(range(12)) or {move(b, action) for b in blocks} != set(blocks):
                raise ValueError('invalid point automorphism')
        if len(actions) != design['automorphism_order']:
            raise ValueError('automorphism order mismatch')
        orbits = sorted({tuple(sorted({action[p] for action in actions})) for p in range(12)})
        if orbits != sorted(map(tuple, design['point_orbits'])):
            raise ValueError('point orbit mismatch')
        aut_count += len(actions)
    return dict(links=len(CAT), point_automorphisms=aut_count)

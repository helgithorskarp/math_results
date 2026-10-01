"""Small exact carrier for the two matched-low anchors; no packing verdict."""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
PAIRS = tuple(combinations(range(15), 2))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def digest(value):
    return sha256(encoded(value)).hexdigest()


def matrix(name):
    if name == 'cycle10':
        missing = {(i, j) for i in range(5) for j in (i, (i+1) % 5)}
    else:
        require(name == 'cycle6_cycle4', 'unknown two-anchor model')
        missing = {(i, j) for i in (0, 1) for j in (0, 1)}
        missing |= {(i, j) for i in (2, 3, 4) for j in (i, 2+(i-1) % 3)}
    cells = tuple((i, j) for i in range(5) for j in range(5) if (i, j) not in missing)
    require(len(cells) == 15 and all(sum(c[k] == i for c in cells) == 3
                                    for k in (0, 1) for i in range(5)), 'wrong matrix degrees')
    anchors = tuple(tuple(sorted((15,)+tuple(x for x, c in enumerate(cells) if c[0] == i)))
                    for i in range(5))
    anchors += tuple(tuple(sorted((16,)+tuple(x for x, c in enumerate(cells) if c[1] == i)))
                     for i in range(5))
    used = Counter(e for q in anchors for e in combinations(q, 2))
    require(len(used) == 60 and set(used.values()) == {1} and (15, 16) not in used,
            'anchor pair repetition')
    eligible = tuple(e for e in PAIRS if e not in used)
    require(len(eligible) == 75, 'wrong residual eligible pair count')
    candidates = tuple(q for q in combinations(range(15), 4)
                       if len({cells[x][0] for x in q}) == len({cells[x][1] for x in q}) == 4)
    direct = tuple(q for q in combinations(range(15), 4)
                   if set(combinations(q, 2)) <= set(eligible))
    require(candidates == direct, 'four-matching and literal candidate factories disagree')
    return cells, anchors, eligible, candidates


def matrix_census():
    """Compare all binary row-degree-two complements with two literal orbits."""
    choices = tuple(combinations(range(5), 2))
    raw = set()
    for rows in product(choices, repeat=5):
        counts = Counter(j for row in rows for j in row)
        if all(counts[j] == 2 for j in range(5)):
            raw.add(tuple((i, j) for i, row in enumerate(rows) for j in row))
    require(len(raw) == 2040, 'complete binary-matrix carrier count mismatch')
    seen, sizes = set(), {}
    for name in ('cycle10', 'cycle6_cycle4'):
        cells, _, _, _ = matrix(name)
        missing = tuple((i, j) for i in range(5) for j in range(5) if (i, j) not in cells)
        orbit = {tuple(sorted((r[i], c[j]) for i, j in missing))
                 for r in permutations(range(5)) for c in permutations(range(5))}
        require(orbit <= raw and not orbit & seen, 'matrix orbit escape or overlap')
        require(len(orbit) == (1440 if name == 'cycle10' else 600), 'matrix orbit-size mismatch')
        sizes[name] = len(orbit)
        seen |= orbit
    require(seen == raw, 'two matrix models do not exhaust the binary carrier')
    return {'labeled_matrices': len(raw), 'orbit_sizes': sizes, 'sha256': digest(sorted(raw))}


def group(name, cells, anchors):
    index = {c: x for x, c in enumerate(cells)}
    maps = set()
    for transpose in (False, True):
        for rows in permutations(range(5)):
            for columns in permutations(range(5)):
                images = tuple((rows[j], columns[i]) if transpose else (rows[i], columns[j])
                               for i, j in cells)
                if set(images) != set(cells):
                    continue
                p = tuple(index[c] for c in images)+(16, 15) if transpose else \
                    tuple(index[c] for c in images)+(15, 16)
                require(len(set(p)) == 17 and {tuple(sorted(p[x] for x in q)) for q in anchors}
                        == set(anchors), 'map changes anchor set')
                maps.add(p)
    expected = 20 if name == 'cycle10' else 48
    require(len(maps) == expected, 'wrong complete anchor group')
    # Direct closure, including both anchor-preserving and exchanging maps.
    require(all(tuple(a[b[x]] for x in range(17)) in maps for a in maps for b in maps),
            'anchor maps are not closed')
    return tuple(sorted(maps))


def high_quotient(maps):
    raw = frozenset(combinations(range(15), 5))
    unseen, result = set(raw), []
    for high in sorted(raw):
        if high not in unseen:
            continue
        orbit = {tuple(sorted(p[x] for x in high)) for p in maps}
        stabilizer = tuple(p for p in maps if tuple(sorted(p[x] for x in high)) == high)
        require(orbit <= unseen and len(orbit)*len(stabilizer) == len(maps),
                'high carrier orbit escape, overlap or divisibility error')
        unseen -= orbit
        result.append((high, len(orbit), stabilizer))
    require(not unseen and sum(n for _, n, _ in result) == 3003, 'high carrier incomplete')
    return result


def instance(high, eligible, candidates):
    high = frozenset(high)
    quota = tuple(2 if x in high else 3 for x in range(15))
    mandatory = tuple(e for e in eligible if not set(e) & high)
    covered_high_anchors = 10-sum(set(e) <= high for e in eligible)
    if covered_high_anchors > 5:
        return None
    columns = tuple(q for q in candidates
                    if len(tuple(combinations(tuple(x for x in q if x in high), 2)))
                    <= 5-covered_high_anchors)
    branches = []
    for triple in range(2):
        double = 5-covered_high_anchors-3*triple
        if double >= 0:
            branches.append((double+2*triple, 2*covered_high_anchors+3*triple, double, triple))
    return quota, mandatory, columns, covered_high_anchors, tuple(branches)

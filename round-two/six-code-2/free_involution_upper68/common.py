"""Exact covered-low-pair carrier and fixed finite-case guards.

Actual author: six-code-2, researcher. The mathematical carrier extends
the marked carrier of six-code-3 and the independent audit of reviewer5.
No executable from those packages is imported.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import json
import time

HERE = Path(__file__).resolve().parent
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def digest(value):
    return sha256(encoded(value)).hexdigest()


class Incomplete(RuntimeError):
    pass


class Guard:
    def __init__(self, nodes=200000, seconds=10):
        require(type(nodes) is int and 0 <= nodes <= 200000, 'invalid node guard')
        require(type(seconds) in (int, float) and 0 < seconds <= 10, 'invalid time guard')
        self.nodes = 0
        self.cap = nodes
        self.seconds = seconds
        self.started = time.monotonic()

    def tick(self):
        self.nodes += 1
        if self.nodes > self.cap or time.monotonic() - self.started > self.seconds:
            raise Incomplete('INCOMPLETE finite-case guard')


def bits(value):
    while value:
        low = value & -value
        yield low.bit_length() - 1
        value ^= low


def mask(points):
    return sum(1 << v for v in points)


def points(value):
    return tuple(bits(value))


def image_word(word, mapping):
    return sum(1 << mapping[v] for v in bits(word))


def image_blocks(blocks, mapping):
    return tuple(sorted(tuple(sorted(mapping[v] for v in q)) for q in blocks))


def model():
    cells = tuple((r, c) for r in range(4) for c in range(4) if r != c)
    anchors = [(12, 13, 15, 16)]
    anchors += [tuple(sorted((15,) + tuple(i for i, cell in enumerate(cells) if cell[0] == r)))
                for r in range(4)]
    anchors += [tuple(sorted((16,) + tuple(i for i, cell in enumerate(cells) if cell[1] == c)))
                for c in range(4)]
    anchors = tuple(sorted(anchors))
    used = frozenset(p for q in anchors for p in combinations(q, 2))
    require(len(anchors) == 9 and len(used) == 54, 'anchor cardinality')
    eligible = tuple(p for p in combinations(range(15), 2) if p not in used)
    columns = tuple(q for q in combinations(range(15), 4)
                    if all(p not in used for p in combinations(q, 2)))
    require(len(eligible) == 80 and len(columns) == 225, 'carrier cardinality')
    return dict(cells=cells, anchors=anchors, used=used, eligible=eligible, columns=columns)


def anchor_group(data):
    lookup = {cell: v for v, cell in enumerate(data['cells'])}
    group = set()
    for p in permutations(range(4)):
        for transpose, exchange in product((False, True), repeat=2):
            moved = tuple(lookup[(p[c], p[r]) if transpose else (p[r], p[c])]
                          for r, c in data['cells'])
            moved += ((13, 12) if exchange else (12, 13)) + (14,)
            moved += (16, 15) if transpose else (15, 16)
            require(sorted(moved) == list(range(17)) and
                    image_blocks(data['anchors'], moved) == data['anchors'], 'invalid anchor map')
            group.add(moved)
    require(len(group) == 96 and all(tuple(a[b[v]] for v in range(17)) in group
                                  for a in group for b in group), 'anchor group closure')
    return tuple(sorted(group))


def compositions(total, slots):
    if slots == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, slots - 1):
            yield (first,) + rest


def move_deficit(deficit, mapping):
    output = [0] * 15
    for v, d in enumerate(deficit):
        output[mapping[v]] = d
    return tuple(output)


def cases(data, group):
    raw = {other + (mark,) for mark in range(1, 6) for other in compositions(5 - mark, 14)}
    require(len(raw) == 3060, 'raw deficit carrier')
    remaining = set(raw)
    result = []
    for deficit in sorted(raw):
        if deficit not in remaining:
            continue
        orbit = {move_deficit(deficit, p) for p in group}
        require(orbit <= remaining, 'deficit orbit overlap or escape')
        remaining -= orbit
        high = frozenset(v for v, d in enumerate(deficit) if d)
        h = len(high)
        quota = tuple(5 - deficit[v] - sum(v in q for q in data['anchors']) for v in range(15))
        budget = (h - 1) * (h - 2) // 2
        used_high = sum(set(p) <= high for p in data['used'])
        columns = tuple(q for q in data['columns']
                        if sum(set(p) <= high for p in combinations(q, 2)) <= budget - used_high)
        mandatory = tuple(p for p in data['eligible'] if not set(p) & high)
        result.append(dict(deficit=deficit, high=tuple(sorted(high)), orbit_size=len(orbit),
                           quota=quota, already_high=used_high, covered_high_budget=budget,
                           columns=columns, mandatory=mandatory,
                           direct=min(quota) < 0 or used_high > budget))
    require(not remaining and len(result) == 108 and
            sum(c['orbit_size'] for c in result) == 3060, 'incomplete deficit quotient')
    return result


def check_star(blocks, expected_reps=None):
    blocks = tuple(sorted(tuple(q) for q in blocks))
    require(len(blocks) == len(set(blocks)) == 20 and
            all(len(q) == 4 and tuple(sorted(set(q))) == q and
                all(type(v) is int and 0 <= v < 17 for v in q) for q in blocks), 'invalid star')
    pairs = Counter(p for q in blocks for p in combinations(q, 2))
    require(len(pairs) == 120 and set(pairs.values()) == {1}, 'star repeats a pair')
    reps = tuple(sum(v in q for q in blocks) for v in range(17))
    require(max(reps) <= 5 and sum(5 - r for r in reps) == 5, 'star replications')
    if expected_reps is not None:
        require(reps == tuple(expected_reps), 'wrong restored replications')
    high = frozenset(v for v, r in enumerate(reps) if r < 5)
    leave = frozenset(combinations(range(17), 2)) - set(pairs)
    require(all(set(p) & high for p in leave), 'low-low leave pair')
    core = tuple(sorted(p for p in leave if set(p) <= high))
    require(len(core) == len(high) - 1, 'high-core edge identity')
    return dict(blocks=blocks, reps=reps, high=tuple(sorted(high)), core=core)

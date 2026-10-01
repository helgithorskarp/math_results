"""Independent recursive incidence reconstruction, exact integer quotas."""
from collections import Counter
from itertools import combinations, permutations
import hashlib
import json

COORDS = [(i, j) for i in range(6) for j in range(i, 6)]
INDEX = {p: k for k, p in enumerate(COORDS)}
SUPPORTS = [tuple(i for i in range(6) if w >> i & 1) for w in range(64)]
DELTA = [sum(1 if i < 4 else -1 for i in row) for row in SUPPORTS]
FEATURES = [tuple(int(i in row and j in row) for i, j in COORDS) for row in SUPPORTS]
POSITIVE = [w for w in range(64) if DELTA[w] > 0]
ONES = [[k for k, x in enumerate(f) if x] for f in FEATURES]
ROOT_PAIRS = list(combinations(range(6), 2))


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'), sort_keys=True).encode()).hexdigest()


def root_matrix(edges):
    rows = [set() for _ in range(6)]
    for i, j in edges:
        rows[i].add(j)
        rows[j].add(i)
    return rows


def root_defects(rows):
    return [2*(sum(1 if j < 4 else -1 for j in rows[i])+(-1 if i < 4 else 1)) for i in range(6)]


def edge_word(rows):
    return sum(int(j in rows[i]) << k for k, (i, j) in enumerate(ROOT_PAIRS))


def root_canonical(rows):
    images = []
    for p in permutations(range(4)):
        for tail in [(4, 5), (5, 4)]:
            perm = p+tail
            relabeled = root_matrix((perm[i], perm[j]) for i, j in ROOT_PAIRS if j in rows[i])
            images.append(edge_word(relabeled))
    return min(images)


def root_census():
    groups = Counter()
    for mask in range(1 << 15):
        rows = root_matrix(p for k, p in enumerate(ROOT_PAIRS) if mask >> k & 1)
        f = root_defects(rows)
        if min(f) >= 0 and sum(f) == 4:
            groups[root_canonical(rows)] += 1
    need(sum(groups.values()) == 127 and len(groups) == 8, 'literal root coverage')
    return groups


# Written examples are names only. The full 32768-word census checks coverage.
EXAMPLES = [
    [(0, 3), (1, 3), (2, 3), (4, 5)],
    [(0, 3), (1, 3), (2, 3), (3, 5), (4, 5)],
    [(0, 3), (1, 3), (2, 3), (3, 4), (3, 5), (4, 5)],
    [(0, 3), (1, 2)],
    [(0, 3), (1, 2), (2, 3), (4, 5)],
    [(0, 3), (1, 2), (2, 3), (3, 5), (4, 5)],
    [(0, 3), (1, 2), (2, 3), (2, 5), (3, 5), (4, 5)],
    [(0, 3), (1, 2), (2, 3), (2, 5), (3, 4), (4, 5)],
]


def specification(profile, w):
    rows = root_matrix(EXAMPLES[profile-1])
    f = root_defects(rows)
    active = [i for i in range(6) if f[i]]
    saturated = [i for i in range(6) if not f[i]]
    degrees = [8]*4+[10]*2
    s = [degrees[i]-len(rows[i]) for i in range(6)]
    G = [[0]*6 for _ in range(6)]
    for i in range(6):
        G[i][i] = s[i]
    for i, j in ROOT_PAIRS:
        defect = w if len(active) == 2 and {i, j} == set(active) else 0
        if j in rows[i]:
            common = 3-defect
        else:
            # Literal blue codegree in a 22-point universe, before root subtraction.
            common = 6-defect-20+degrees[i]+degrees[j]
        G[i][j] = G[j][i] = common-len(rows[i] & rows[j])
    Z = [[s[i]*(3 if j < 4 else 5)-sum(G[i][k] for k in rows[j])
          -2*G[i][j]*int(j >= 4) for j in range(6)] for i in range(6)]
    return {'profile': profile, 'w': w, 'roots': rows, 'f': f, 'active': active,
            'saturated': saturated, 'G': G, 'Z': Z}


def zero_completion(residual, positives, total_rows=16):
    counts = [0]*64
    for word in positives:
        counts[word] += 1
    for i, j in combinations(range(4), 2):
        counts[(1 << i) | (1 << j) | 48] = residual[INDEX[i, j]]
    for i in range(4):
        pair_mass = sum(residual[INDEX[min(i, j), max(i, j)]] for j in range(4) if j != i)
        for j in (4, 5):
            counts[(1 << i) | (1 << j)] = residual[INDEX[i, j]]-pair_mass
    counts[0] = total_rows-sum(counts)
    if min(counts) < 0:
        return None
    positive_counts = Counter(positives)
    rebuilt = [sum((counts[w]-positive_counts[w])*FEATURES[w][k] for w in range(64)) for k in range(21)]
    if tuple(rebuilt) != residual:
        return None
    return counts


def incidences(spec, state_limit=2000000, total_rows=16):
    """Sorted row recursion; prune exact Gram and M^T delta capacities."""
    G = spec['G']
    target = tuple(G[i][j] for i, j in COORDS)
    weighted = tuple(sum(G[i][j]*(1 if j < 4 else -1) for j in range(6)) for i in range(6))
    first_moment = sum(G[i][i]*(1 if i < 4 else -1) for i in range(6))
    need(0 <= first_moment <= 8 and total_rows >= 0, 'first surplus moment/domain')
    if min(target) < 0 or min(weighted) < 0:
        return [], {'states': 0, 'complete_positive_prefixes': 0, 'quota_pruned': True}
    counts = []
    states = 0
    complete = 0

    def visit(start, mass, left, vector, selected):
        nonlocal states, complete
        states += 1
        if states > state_limit:
            raise RuntimeError('INCOMPLETE: incidence state guard reached')
        if len(selected) > total_rows:
            return
        if mass == 0:
            if any(vector):
                return
            complete += 1
            full = zero_completion(left, selected, total_rows)
            if full is not None:
                need(sum(full) == total_rows and all(full[w] == 0 for w in range(64) if DELTA[w] < 0), 'full row domain')
                need([sum(full[w]*FEATURES[w][k] for w in range(64)) for k in range(21)] == list(target), 'full literal Gram')
                counts.append(full)
            return
        if max(vector) > mass:
            return
        second = sum(vector[i]*(1 if i < 4 else -1) for i in range(6))
        if not mass <= second <= 4*mass or (second-mass) % 2:
            return
        for pos in range(start, len(POSITIVE)):
            word = POSITIVE[pos]
            d = DELTA[word]
            if d > mass or d*d > second or any(vector[i] < d for i in SUPPORTS[word]):
                continue
            if any(left[k] == 0 for k in ONES[word]):
                continue
            new_left = list(left)
            for k in ONES[word]:
                new_left[k] -= 1
            new_vector = list(vector)
            for i in SUPPORTS[word]:
                new_vector[i] -= d
            visit(pos, mass-d, tuple(new_left), tuple(new_vector), selected+(word,))

    visit(0, first_moment, target, weighted, ())
    counts.sort()
    need(len({tuple(c) for c in counts}) == len(counts), 'unique sorted multisets')
    return counts, {'states': states, 'complete_positive_prefixes': complete, 'quota_pruned': False}

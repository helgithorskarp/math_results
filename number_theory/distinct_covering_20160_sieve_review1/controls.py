"""Definition-level controls for the independent finite audit."""
from collections import defaultdict
from itertools import product, permutations, combinations
from math import gcd
from hashlib import sha256
import json


def tree_group(p, depth):
    if depth == 0:
        return [(0,)]
    children = tree_group(p, depth-1)
    return [tuple(root[x % p]+p*branch[x % p][x//p] for x in range(p**depth))
            for root in permutations(range(p)) for branch in product(children, repeat=p)]


def controls(M, cover):
    checks = 0
    for p, depth, moduli in ((2, 3, (2, 4)), (2, 3, (4, 8)), (3, 2, (3, 9))):
        group, m = tree_group(p, depth), p**depth
        for values in product(*(range(n) for n in moduli)):
            raw = tuple(zip(moduli, values))
            A = M.canon(raw)
            stabilizer = [f for f in group if all(f[a] % n == a for n, a in A)]
            orbits = {frozenset(f[a] for f in stabilizer) for a in range(m)}
            signatures = defaultdict(set)
            for a in range(m):
                signatures[tuple(gcd(a-b, min(m, n)) for n, b in A)].add(a)
            M.need({frozenset(s) for s in signatures.values()} == orbits, 'full-group/signature mismatch')
            actual = sorted({M.canon(A+((m, a),))[-1][1] for a in range(m)})
            M.need(M.options(m, A) == actual and len(actual) == len(orbits), 'normalized orbit mismatch')
            # An actual group element must realize the normalization of raw.
            M.need(any(all(f[a] % n == b for (n, a), (_, b) in zip(raw, A)) for f in group),
                   'normalization has no realizing tree automorphism')
            checks += 1
    lifted = 0
    for Q in (4, 6, 8, 12):
        subsets = range(1 << Q) if Q <= 8 else (0, 1, (1 << Q)-1, 0x555, 0x924)
        P = M.Period(Q)
        for factor in (1, 2, 3):
            L = Q*factor
            B = [m for m in M.divisors(L) if m >= 2]
            for U in subsets:
                actual_D = sum(bool(U >> (x % Q) & 1) for x in range(L))
                actual_C = sum(max(sum(bool(U >> (x % Q) & 1) for x in range(a, L, m))
                                   for a in range(m)) for m in B)
                M.need(M.uniform(L, Q, U, B, P) == (actual_D, actual_C), 'literal lifted capacity mismatch')
                lifted += 1
    pairs = tuples = 0
    for L in (12, 18, 24, 30):
        P = M.Period(L)
        weights = [(x*x+3*x+L) % 7 for x in range(L)]
        layer_bits = defaultdict(int)
        for x, w in enumerate(weights):
            if w:
                layer_bits[w] |= 1 << x
        layers = tuple(sorted(layer_bits.items()))
        for m, n in combinations([d for d in M.divisors(L) if d >= 2], 2):
            values = [sum(w for x, w in enumerate(weights) if x % m == a or x % n == b)
                      for a in range(m) for b in range(n)]
            digest = sha256(''.join(str(v)+',' for v in values).encode()).hexdigest()
            M.need(P.pairs(layers, m, n) == (max(values), digest, m*n), 'literal pair union mismatch')
            pairs += 1
            tuples += m*n
    # General positive control: a real period12 cover must satisfy every prefix inequality.
    fixture = ((2, 0), (3, 0), (4, 1), (6, 1), (12, 11))
    M.need(all(any(x % m == a for m, a in fixture) for x in range(12)), 'bad positive fixture')
    P = M.Period(12)
    for depth in range(len(fixture)+1):
        A = fixture[:depth]
        B = [m for m, a in fixture[depth:]]
        D, C = M.uniform(12, 12, P.residual(A), B, P)
        M.need(D <= C, 'uniform inequality falsely excludes a known cover')
    # Literal box decoding control and malformed-input rejection.
    P = M.Period(24)
    boxes = [[0b00101101, 0b101, 3], [0b11010010, 0b010, 5]]
    layers, support = P.box_layers(boxes)
    values = P.weights(layers)
    M.need(values == [sum(box[-1] for box in boxes if box[0] >> (x % 8) & 1 and box[1] >> (x % 3) & 1)
                      for x in range(24)], 'literal box predicate mismatch')
    rejected = 0
    for bad in ([boxes[0], boxes[0]], [[1 << 8, 1, 1]], [[1, 1, 0]], [[1, 1, True]]):
        try:
            M.Period(24).box_layers(bad)
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError('malformed box accepted')
    for change in ('duplicate', 'period', 'phase'):
        bad = json.loads(json.dumps(cover))
        if change == 'duplicate':
            bad['congruences'].append(bad['congruences'][0])
        elif change == 'period':
            bad['lcm'] += 8
        else:
            bad['congruences'][0][0] = (bad['congruences'][0][0]+1) % 8
        try:
            M.cover_audit(bad)
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError('malformed or destructive covering accepted')
    return {'entire_small_stabilizer_groups_checked': checks,
            'lifted_capacity_subsets_checked': lifted, 'small_pair_groups_checked': pairs,
            'ordered_literal_pair_phases_checked': tuples,
            'positive_period12_prefixes_checked': len(fixture)+1,
            'literal_box_points_checked': 24, 'corrupted_inputs_rejected': rejected}

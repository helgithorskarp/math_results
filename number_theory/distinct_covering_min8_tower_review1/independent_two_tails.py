#!/usr/bin/env python3
"""six-reviewer-1: independent all-exponents minimum-eight exclusion.

Uses our separate stabilizer signatures, exact Fraction series coefficients,
CRT tuple joins, and arithmetic-progression weight sums. No target code or
solver is imported. Copied compact integer input is checked as untrusted data.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import gcd, lcm
from pathlib import Path
from time import monotonic

from independent_check import (IncompleteSearch, divisors, renamed_residues,
                               representatives, require)

Q = 360
AXES = (8, 9, 5)
ANCHORS = (8, 9, 10, 12, 15, 18, 20)
HERE = Path(__file__).resolve().parent


def coefficients(placed=(), minimum=8):
    """Derive the convergent sums rather than reading coefficient data."""
    result = {}
    for i, j, c in product(range(4), range(3), range(2)):
        g = 2**i * 3**j * 5**c
        binary = Fraction(1, 1-Fraction(1, 2)) if i == 3 else Fraction(1)
        ternary = Fraction(1, 1-Fraction(1, 3)) if j == 2 else Fraction(1)
        result[g] = binary*ternary
    excluded = tuple(n for n in divisors(Q) if n < minimum) + tuple(placed)
    require(len(excluded) == len(set(excluded)), 'duplicate excluded modulus')
    for n in excluded:
        require(n in result, 'excluded modulus outside head')
        result[n] -= 1
    require(all(k >= 0 for k in result.values()), 'negative coefficient')
    return {g: k for g, k in result.items() if k}


def phase_maxima(vector, moduli):
    """Literal arithmetic progressions, independent of population arrays."""
    return {g: max(sum(vector[a::g]) for a in range(g)) for g in moduli}


def scaled_capacity(vector, placed):
    resource = coefficients(placed)
    maxima = phase_maxima(vector, resource)
    value = 2*sum(resource[g]*maxima[g] for g in resource)
    require(value.denominator == 1, 'nonintegral doubled coefficient sum')
    require(resource[Q] == 3 and maxima[Q] > 0,
            'no explicit positive omitted tail term')
    return int(value), maxima


def decode(boxes):
    """Join selected CRT coordinates using a bijection built by remainders."""
    require(type(boxes) is list, 'boxes must be a list')
    join = {tuple(x % q for q in AXES): x for x in range(Q)}
    require(len(join) == Q, 'CRT coordinate join not bijective')
    vector, occupied = [0]*Q, set()
    for box in boxes:
        require(type(box) is list and len(box) == 4 and
                all(type(n) is int for n in box), 'malformed box')
        selected, weight = [], box[3]
        require(weight > 0, 'box weight must be positive')
        for mask, q in zip(box[:3], AXES):
            require(0 < mask < 2**q, 'invalid axis mask')
            selected.append(tuple(a for a in range(q) if mask & (1 << a)))
        points = {join[t] for t in product(*selected)}
        require(points and not (occupied & points), 'empty or overlapping box')
        occupied.update(points)
        for x in points:
            vector[x] = weight
    return vector


def check_support(vector, residues):
    require(len(vector) == Q and all(type(w) is int and w >= 0 for w in vector),
            'invalid integer point weights')
    require(sum(vector) > 0, 'positive demand required')
    require(all(not vector[x] or all(x % m != a for m, a in zip(ANCHORS, residues))
                for x in range(Q)), 'weight on already covered point')


def read_weights(path):
    data = json.loads(path.read_text())
    require(data['format_version'] == 1 and data['Q'] == Q and
            data['axes'] == list(AXES), 'wrong certificate parameters')
    result = {}
    for residues, boxes in data['certificates']:
        require(type(residues) is list and 1 <= len(residues) <= len(ANCHORS) and
                all(type(a) is int and 0 <= a < m for a, m in zip(residues, ANCHORS)),
                'invalid prefix')
        key = tuple(residues)
        require(key not in result, 'duplicate prefix')
        result[key] = boxes
    return result


def finite_coefficients(placed, h2, h3):
    L = Q*2**h2*3**h3
    result = {g: Fraction(0) for g in divisors(Q)}
    for n in divisors(L):
        if n >= 8 and n not in placed:
            g = gcd(Q, n)
            result[g] += Fraction(g, n)
    return result


def search(path, max_nodes=10000, seconds=30):
    certificates, used = read_weights(path), set()
    nodes, uniform, weighted = ([0]*8 for _ in range(3))
    events, equality_vectors = [], []
    start = monotonic()

    def visit(previous):
        depth = len(previous)
        if sum(nodes) >= max_nodes or monotonic()-start > seconds:
            raise IncompleteSearch('independent two-tail replay incomplete')
        nodes[depth] += 1
        # Recompute from congruence definitions; no inherited mask builder.
        residues = tuple(renamed_residues(previous))
        vector = [int(all(x % m != a for m, a in zip(ANCHORS, residues)))
                  for x in range(Q)]
        require(sum(vector) > 0, 'an anchor assignment already covers')
        total, maxima = scaled_capacity(vector, ANCHORS[:depth])
        demand, tag = sum(vector), None
        if total <= 2*demand:
            uniform[depth] += 1
            tag = 'uniform'
        elif residues in certificates:
            vector = decode(certificates[residues])
            check_support(vector, residues)
            total, maxima = scaled_capacity(vector, ANCHORS[:depth])
            demand = sum(vector)
            require(total <= 2*demand, 'weight certificate fails inequality')
            require(residues not in used, 'certificate reached twice')
            used.add(residues)
            weighted[depth] += 1
            tag = 'weighted'
        if tag is not None:
            event = [tag, list(residues), demand, total, sorted(maxima.items())]
            events.append(json.dumps(event, separators=(',', ':')))
            if total == 2*demand:
                equality_vectors.append((ANCHORS[:depth], vector, demand))
            return
        require(depth < len(ANCHORS), 'an uncut terminal assignment remains')
        m = ANCHORS[depth]
        for a in representatives(m, previous):
            visit(previous+((m, a),))

    visit(())
    require(used == set(certificates), 'unused certificate data')
    finite_equalities = 0
    for placed, vector, demand in equality_vectors:
        infinite = coefficients(placed)
        for h2, h3 in product(range(3), repeat=2):
            finite = finite_coefficients(placed, h2, h3)
            maxima = phase_maxima(vector, finite)
            require(all(finite[g] <= infinite.get(g, 0) for g in finite),
                    'finite coefficient exceeds its infinite sum')
            require(sum(finite[g]*maxima[g] for g in finite) < demand,
                    'equality failed to give strict finite exclusion')
            finite_equalities += 1
    events.sort()
    return {
        'agent': 'six-reviewer-1', 'role': 'independent reviewer',
        'Q': Q, 'anchors': list(ANCHORS), 'nodes_per_depth': nodes,
        'uniform_cuts_per_depth': uniform, 'weighted_cuts_per_depth': weighted,
        'nodes': sum(nodes), 'uniform_cuts': sum(uniform),
        'weighted_cuts': sum(weighted), 'uncut_leaves': 0,
        'equality_cuts': len(equality_vectors),
        'strict_finite_equality_checks': finite_equalities,
        'sorted_normalized_terminal_sha256':
            sha256(('\n'.join(events)+'\n').encode()).hexdigest(),
        'weights_file_sha256': sha256(path.read_bytes()).hexdigest(),
    }, events


def controls(path):
    crt_checks = 0
    # Individual weighted class capacities over two independent prime tails.
    for base in (6, 12, 18):
        for vector in ([1]*base, [x % 4 for x in range(base)],
                       [int(x % 3 != 0) for x in range(base)]):
            for h2, h3 in product(range(3), repeat=2):
                L = base*2**h2*3**h3
                lifted = [vector[x % base] for x in range(L)]
                for n in divisors(L):
                    g = gcd(base, n)
                    literal = max(sum(lifted[a::n]) for a in range(n))
                    formula = L//lcm(base, n)*max(sum(vector[a::g]) for a in range(g))
                    require(literal == formula, 'weighted CRT lift identity fails')
                    crt_checks += 1
    # Actual finite geometric coefficient sums, with arbitrary assigned heads.
    coefficient_checks = 0
    for placed in ((), ANCHORS[:3], ANCHORS):
        infinity = coefficients(placed)
        for h2, h3 in product(range(4), repeat=2):
            finite = finite_coefficients(placed, h2, h3)
            r2, r3 = sum(Fraction(1, 2**t) for t in range(h2+1)), \
                sum(Fraction(1, 3**t) for t in range(h3+1))
            for i, j, c in product(range(4), range(3), range(2)):
                g = 2**i*3**j*5**c
                exact = (r2 if i == 3 else 1)*(r3 if j == 2 else 1)
                exact -= int(g < 8)+int(g in placed)
                require(finite[g] == exact and finite[g] <= infinity.get(g, 0),
                        'finite grouped series mismatch')
                coefficient_checks += 1
    # Genuine covering: the infinite rule must allow every nonempty prefix.
    cover = ((2, 0), (3, 0), (4, 1), (6, 1), (12, 11))
    require(all(any(x % n == a for n, a in cover) for x in range(Q)),
            'bad positive-cover fixture')
    for k in range(len(cover)):
        vector = [int(all(x % n != a for n, a in cover[:k])) for x in range(Q)]
        resource = coefficients(tuple(n for n, _ in cover[:k]), minimum=2)
        maxima = phase_maxima(vector, resource)
        require(sum(resource[g]*maxima[g] for g in resource) > sum(vector),
                'a genuine finite covering prefix was excluded')
    rejected = 0
    bad_boxes = ([[1, 1, 1, -1]], [[0, 1, 1, 1]], [[256, 1, 1, 1]],
                 [[1, 1, 1, 1], [1, 1, 1, 2]], [[1, 1, 1, True]])
    for boxes in bad_boxes:
        try:
            decode(boxes)
        except RuntimeError:
            rejected += 1
        else:
            raise RuntimeError('malformed weights were accepted')
    for vector in ([0]*Q, [1]+[0]*(Q-1), [-1]+[0]*(Q-1)):
        try:
            check_support(vector, (0,))
        except RuntimeError:
            rejected += 1
        else:
            raise RuntimeError('invalid support was accepted')
    try:
        search(path, max_nodes=0)
    except IncompleteSearch:
        rejected += 1
    else:
        raise RuntimeError('operational exhaustion was accepted')
    return {'literal_weighted_CRT_checks': crt_checks,
            'finite_grouped_series_checks': coefficient_checks,
            'genuine_cover_prefixes': len(cover), 'rejected_invalid_or_incomplete': rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--weights', type=Path, default=HERE/'two_tails_weights.json')
    parser.add_argument('--events', type=Path, help='scratch-only full terminal records')
    args = parser.parse_args()
    checked = controls(args.weights)
    result, events = search(args.weights)
    result['controls'] = checked
    if args.events is not None:
        args.events.write_text(json.dumps(events)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

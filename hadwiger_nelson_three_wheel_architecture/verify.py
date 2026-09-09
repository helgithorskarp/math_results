#!/usr/bin/env python3
"""Whole-architecture certificate verification, CPython standard library only."""
from pathlib import Path
from itertools import product, combinations
from collections import Counter
import argparse
import hashlib
import json
import algebra as A

HERE = Path(__file__).resolve().parent
W = [(0, 0), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
D = sorted({(a-c, b-d) for (a, b), (c, d) in product(W, repeat=2)})
LABELS = list(product(range(7), repeat=3))


def rotate(q):
    a, b = q
    return -b, a+b


def canonical(ds):
    orbit = []
    for _ in range(6):
        orbit.append(ds); ds = tuple(map(rotate, ds))
    return min(orbit)


def norm(q):
    a, b = q
    return a*a+a*b+b*b


def field4(a, b):
    # F2[z]/(z^2+z+1), encoded 0,1,z,1+z as two bits.
    out = 0
    for _ in range(2):
        if b & 1:
            out ^= a
        a <<= 1
        if a & 4:
            a ^= 7
        b >>= 1
    return out


def colour_words():
    c3 = [(a-b) % 3 for a, b in W]
    c4 = [(a % 2)+2*(b % 2) for a, b in W]
    words = []
    for s, t in product((1, -1), repeat=2):
        words.append((f'F3_{s}_{t}', [(c3[a]+s*c3[b]+t*c3[c]) % 3 for a, b, c in LABELS]))
    for s, t in product((1, 2, 3), repeat=2):
        words.append((f'F4_{s}_{t}', [c4[a] ^ field4(s, c4[b]) ^ field4(t, c4[c]) for a, b, c in LABELS]))
    return words


def input_polynomials():
    # Completeness: D is the complete displacement set of W; common sixth-root
    # rotation preserves squared distance, allowing the exact sixfold quotient.
    orbits = sorted({canonical(ds) for ds in product(D, repeat=3)})
    A.need(len(D) == 19 and len(orbits) == 1144, 'complete displacement domain')
    mapping = {ds: A.unit_polynomial(ds) for ds in orbits}
    return mapping, sorted(set(mapping.values()))


def factor_check(cert, polynomials):
    A.need(cert['coefficient_order'] == 'x exponent outer, y exponent inner, each 0,1,2', 'monomial order')
    coeffs = cert['factors']
    A.need(coeffs == sorted(coeffs) and len(set(map(tuple, coeffs))) == len(coeffs), 'unique ordered factors')
    factors = [A.vector(c) for c in coeffs]
    for c, f in zip(coeffs, factors):
        A.need(f and A.degree(f) >= 1 and list(A.primitive(f)) == c, 'primitive nonconstant factor')
    decomposition = cert['factorization']
    A.need(len(decomposition) == len(polynomials), 'complete polynomial factorization rows')
    for p, row in zip(polynomials, decomposition):
        A.need(all(type(i) is int and 0 <= i < len(factors) for i in row), 'factor index')
        if p == (0,)*9:
            A.need(row == [], 'automatic edge factor row')
            continue
        q = A.ONE
        for i in row:
            q = A.mul(q, factors[i])
        A.need(A.primitive(q) == p, 'exact factor multiplication identity')
    return factors, {p: set(row) for p, row in zip(polynomials, decomposition)}


def pair_inventory(displacements, decomposition):
    base = []; pairs = []
    # Cache all 6859 literal displacements, independently of the graph producer.
    literal = {ds: displacements[canonical(ds)] for ds in product(D, repeat=3)}
    for a, b in combinations(range(343), 2):
        ds = tuple((W[i][0]-W[j][0], W[i][1]-W[j][1]) for i, j in zip(LABELS[a], LABELS[b]))
        p = literal[ds]
        if p == (0,)*9:
            base.append((a, b))
        else:
            pairs.append((a, b, decomposition[p]))
    expected = []
    for a, b in combinations(range(343), 2):
        changes = [j for j in range(3) if LABELS[a][j] != LABELS[b][j]]
        if len(changes) == 1:
            j = changes[0]; u = W[LABELS[a][j]]; v = W[LABELS[b][j]]
            if norm((u[0]-v[0], u[1]-v[1])) == 1:
                expected.append((a, b))
    A.need(base == expected and len(base) == 1764, 'Cartesian product base')
    return base, pairs


def covering(factors, active, base, pairs):
    degrees = {i: A.degree(factors[i]) for i in active}
    rows = []
    for name, word in colour_words():
        A.need(len(word) == 343 and set(word) <= {0, 1, 2, 3}, 'four-colour palette')
        A.need(all(word[a] != word[b] for a, b in base), 'product colouring')
        bad = set()
        for a, b, ids in pairs:
            if word[a] == word[b]:
                bad.update(ids)
        bad.intersection_update(active)
        rows.append({'name': name, 'bad': bad, 'bad_degree_sum': sum(degrees[i] for i in bad)})
    A.need(not set.intersection(*(r['bad'] for r in rows)), 'all event factors covered')
    scores = []
    for j, r in enumerate(rows):
        protect = {f: min((i for i, q in enumerate(rows) if f not in q['bad']),
                          key=lambda i: (rows[i]['bad_degree_sum'], i)) for f in r['bad']}
        score = sum(degrees[f]*rows[i]['bad_degree_sum'] for f, i in protect.items())
        scores.append((score, j, protect))
    score, primary, protect = min(scores, key=lambda r: (r[0], r[1]))
    selected = sorted({tuple(sorted((f, g))) for f, i in protect.items() for g in rows[i]['bad']})
    A.need(all(f != g for f, g in selected), 'protecting word excludes the first factor')
    bound = sum(degrees[f]*degrees[g] for f, g in selected)
    return rows, {
        'primary_word': rows[primary]['name'], 'primary_index': primary,
        'protecting_word_rule': 'minimum bad-degree sum, then smallest word index, among words proper on the factor graph',
        'primary_bad_factors': len(rows[primary]['bad']), 'ordered_degree_bound': score,
        'distinct_curve_pairs': len(selected), 'bezout_intersection_bound': bound,
        'maximum_selected_degree_product': max(degrees[f]*degrees[g] for f, g in selected),
        'curve_pair_sha256': hashlib.sha256(json.dumps(selected, separators=(',', ':')).encode()).hexdigest(),
        'protecting_assignment_sha256': hashlib.sha256(json.dumps(sorted(protect.items()), separators=(',', ':')).encode()).hexdigest(),
    }


def collisions():
    # With all three coefficients nonzero, circle intersection fixes at most
    # two u values, and v is uniquely recovered. Common rotation changes none.
    nonzero = [d for d in D if d != (0, 0)]
    rows = sorted({canonical(ds) for ds in product(nonzero, repeat=3)})
    counts = Counter(); bound = 0
    for d, e, f in rows:
        discriminant = 4*norm(d)*norm(e)-(norm(f)-norm(d)-norm(e))**2
        count = 2 if discriminant > 0 else 1 if discriminant == 0 else 0
        counts[str(count)] += 1; bound += count
    # Equal-length nonzero W displacements form one sixth-root orbit for
    # each norm. Thus two-coefficient collisions are pair-alignment lines.
    for d in nonzero:
        orbit = set(); q = d
        for _ in range(6):
            orbit.add(q); q = rotate(q)
        A.need(orbit == {e for e in nonzero if norm(e) == norm(d)}, 'pair-collision alignment lemma')
    H = {(a+c, b+d) for (a, b), (c, d) in product(W, repeat=2)}
    expected = {(a, b) for a in range(-2, 3) for b in range(-2, 3) if max(abs(a), abs(b), abs(a+b)) <= 2}
    A.need(H == expected and len(H) == 19 and set(W) <= H, 'accepted H19 family containment')
    return {'nonzero_displacement_orbits': len(rows), 'roots_per_row_histogram': dict(sorted(counts.items())),
            'triple_collision_bound_before_deduplication': bound, 'pair_alignments_covered_by_h4005_h4031': True}


def corruption_controls(cert, polynomials):
    from copy import deepcopy
    tests = []
    x = deepcopy(cert); x['factorization'].pop(); tests.append(('missing factorization row', x))
    x = deepcopy(cert); x['factors'][0][0] += 1; tests.append(('wrong factor coefficient', x))
    x = deepcopy(cert); idx = next(i for i, r in enumerate(x['factorization']) if r)
    x['factorization'][idx] = []; tests.append(('missing factor', x))
    for name, c in tests:
        try:
            factor_check(c, polynomials)
        except ValueError:
            pass
        else:
            raise RuntimeError('accepted corruption: '+name)
    return [name for name, c in tests]


def run(certificate):
    cert = json.loads(certificate.read_text())
    displacements, polynomials = input_polynomials()
    factors, decomposition = factor_check(cert, polynomials)
    positive = [i for i, f in enumerate(factors) if f in (A.DX, A.DY)]
    A.need(len(positive) == 2, 'positive Cayley denominators')
    active = [i for i in range(len(factors)) if i not in positive]
    base, pairs = pair_inventory(displacements, decomposition)
    rows, cover = covering(factors, set(active), base, pairs)
    audit = A.audit_coprime(factors, active)
    collision = collisions()
    import physical_controls
    physical = physical_controls.run(W, LABELS, colour_words())
    return {
        'status': 'THREE_WHEEL_ARCHITECTURE_REDUCED_TO_FINITE_EXACT_EXCEPTION_SET',
        'record_improvement': False, 'maximum_physical_order': 343,
        'canonical_displacements': len(displacements), 'distinct_normalized_unit_polynomials': len(polynomials),
        'factorization_identities_checked': len(polynomials), 'active_event_factors': len(active),
        'excluded_positive_denominator_factors': 2, 'active_factor_degree_histogram': dict(sorted(Counter(str(A.degree(factors[i])) for i in active).items())),
        'formal_label_pairs': 343*342//2, 'cartesian_unit_edges': len(base),
        'explicit_colour_words': len(rows),
        'single_factor_graphs_with_F3_word': sum(any(f not in r['bad'] for r in rows[:4]) for f in active),
        'remaining_single_factor_graphs_with_F4_word': sum(all(f in r['bad'] for r in rows[:4]) for f in active),
        'word_failure_profiles': [{'name': r['name'], 'bad_factors': len(r['bad']), 'bad_degree_sum': r['bad_degree_sum']} for r in rows],
        'finite_intersection_cover': cover, 'coprimality_audit': audit, 'collisions': collision,
        'finite_parameter_pair_upper_bound': cover['bezout_intersection_bound']+collision['triple_collision_bound_before_deduplication'],
        'necessary_real_parameter_field_degree_at_most': max(2, cover['maximum_selected_degree_product']),
        'necessary_real_coordinate_field_degree_at_most': 2*max(2, cover['maximum_selected_degree_product']),
        'physical_controls': physical, 'coprimality_controls': A.controls(),
        'rejected_corruptions': corruption_controls(cert, polynomials),
        'certificate_sha256': hashlib.sha256(certificate.read_bytes()).hexdigest(),
        'proof_replay_solver_calls': 0, 'proof_replay_CAS_calls': 0,
        'exceptional_candidates_chromatically_decided': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE/'certificate.json')
    parser.add_argument('--check-expected', action='store_true')
    args = parser.parse_args(); result = run(args.certificate)
    if args.check_expected:
        A.need(result == json.loads((HERE/'EXPECTED.json').read_text()), 'expected output')
    print(json.dumps(result, indent=2, sort_keys=True))

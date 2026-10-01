#!/usr/bin/env python3
"""six-reviewer-4: complete independent1111-form surplus-eight audit.

No author imports or expected fixtures determine the domain. This extends this reviewer's credited predecessor checker. Ordered surplus
compositions and degree assignments precede quotienting; exact determinants
use prime fields, CRT uniqueness and Hadamard bounds, rather than author
Bareiss/Fraction arithmetic. Python3.11 standard library only.
"""
from collections import Counter
from itertools import combinations, permutations, product
from math import isqrt
from pathlib import Path
import argparse
import hashlib
import json


def require(ok, text):
    if not ok:
        raise ValueError(text)


def canonical_bytes(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':')).encode()


def digest(data):
    return hashlib.sha256(canonical_bytes(data)).hexdigest()


def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p)+1))


def primes():
    result, p = [], 1 << 29
    while len(result) < 8:
        if p % 2 and prime(p):
            result.append(p)
        p += 1
    return result


def determinant_mod(matrix, p):
    a = [[x % p for x in row] for row in matrix]
    value = 1
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            value = -value
        v = a[j][j]
        value = value*v % p
        inverse = pow(v, -1, p)
        for i in range(j+1, len(a)):
            factor = a[i][j]*inverse % p
            if factor:
                for k in range(j+1, len(a)):
                    a[i][k] = (a[i][k]-factor*a[j][k]) % p
            a[i][j] = 0
    return value % p


def determinant_crt(matrix, moduli):
    bound = 1
    for row in matrix:
        square = sum(x*x for x in row)
        root = isqrt(square)
        bound *= root+(root*root != square)
    residue, modulus, proof = 0, 1, []
    for p in moduli:
        r = determinant_mod(matrix, p)
        step = (r-residue)*pow(modulus, -1, p) % p
        residue += modulus*step
        modulus *= p
        proof.append((p, r))
        if modulus > 2*bound:
            break
    require(modulus > 2*bound, 'incomplete CRT determinant proof')
    value = residue if residue <= modulus//2 else residue-modulus
    require(abs(value) <= bound, 'CRT determinant violates Hadamard')
    return value, {'modulus': modulus, 'bound': bound, 'residues': proof}


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(1, total-parts+2):
        for rest in compositions(total-first, parts-1):
            yield (first,)+rest


def canonical_core(types, weights):
    k = len(types)
    pairs = list(combinations(range(k), 2))
    slot = {pair: i for i, pair in enumerate(pairs)}
    return min((tuple(types[i] for i in p),
                tuple(weights[slot[tuple(sorted((p[i], p[j])))]] for i, j in pairs))
               for p in permutations(range(k)))


def core_census(counts, surplus_units):
    """All ordered center types, then all weighted graphs on those centers."""
    result = set()
    ordered = Counter()
    for k in range(1, surplus_units+1):
        pairs = list(combinations(range(k), 2))
        for comp in compositions(surplus_units, k):
            for colors in product((8, 9, 10), repeat=k):
                if any(colors.count(d) > counts[d-8] for d in (8, 9, 10)):
                    continue
                types = tuple((d, 2*q) for d, q in zip(colors, comp))
                budgets = [q+(d % 2) for d, q in types]
                odd_leaves = counts[1]-colors.count(9)
                weights = [0]*len(pairs)

                def visit(j):
                    if j == len(pairs):
                        needed = sum(budgets)
                        if needed <= odd_leaves and (odd_leaves-needed) % 2 == 0:
                            ordered[k] += 1
                            result.add(canonical_core(types, tuple(weights)))
                        return
                    a, b = pairs[j]
                    for w in range(min(budgets[a], budgets[b])+1):
                        weights[j] = w
                        budgets[a] -= w
                        budgets[b] -= w
                        visit(j+1)
                        budgets[a] += w
                        budgets[b] += w
                visit(0)
    return sorted(result, key=lambda key: (len(key[0]), key)), ordered


def make_defect(counts, key):
    types, weights = key
    degrees = [d for d, c in zip((8, 9, 10), counts) for _ in range(c)]
    free = {d: [i for i, x in enumerate(degrees) if x == d] for d in (8, 9, 10)}
    centers = [free[d].pop(0) for d, q in types]
    defect = [[0]*22 for _ in range(22)]
    leaf_count = [q+(d % 2) for d, q in types]
    for (i, j), w in zip(combinations(range(len(types)), 2), weights):
        a, b = centers[i], centers[j]
        defect[a][b] = defect[b][a] = w
        leaf_count[i] -= w
        leaf_count[j] -= w
    for i, c in zip(centers, leaf_count):
        require(c >= 0, 'negative leaf budget')
        for _ in range(c):
            j = free[9].pop(0)
            defect[i][j] = defect[j][i] = 1
    require(len(free[9]) % 2 == 0, 'odd matching remainder')
    for a, b in zip(free[9][::2], free[9][1::2]):
        defect[a][b] = defect[b][a] = 1
    actual = [(degrees[i], sum(defect[i])-degrees[i] % 2)
              for i in range(22) if sum(defect[i]) > degrees[i] % 2]
    require(actual == list(types), 'recovered full incident surplus')
    return degrees, defect


def forced_matrix(degrees, defect):
    return [[(2*degrees[i]-17)**2+4*degrees[i] if i == j
             else 4*(degrees[i]+degrees[j]-14-defect[i][j])
             for j in range(22)] for i in range(22)]


def core_orbit(types, weights):
    pairs = list(combinations(range(len(types)), 2))
    slots = {p: i for i, p in enumerate(pairs)}
    return len({tuple(weights[slots[tuple(sorted((p[i], p[j])))]] for i, j in pairs)
                for p in permutations(range(len(types)))
                if tuple(types[i] for i in p) == types})


def literal_bridge_controls():
    """Signed controls: no book-cap or degree-range hypothesis is imposed."""
    records = []
    edges = list(combinations(range(22), 2))
    masks = [0, (1 << 231)-1]
    for seed in range(1, 7):
        state, mask = seed, 0
        for pos, pair in enumerate(edges):
            state = (1664525*state+1013904223) % (1 << 32)
            if state % 11 < seed+1:
                mask |= 1 << pos
        masks.append(mask)
    for mask in masks:
        red = [set() for _ in range(22)]
        for pos, (i, j) in enumerate(edges):
            if mask >> pos & 1:
                red[i].add(j)
                red[j].add(i)
        blue = [set(range(22))-{i}-red[i] for i in range(22)]
        d = list(map(len, red))
        F = [[0]*22 for _ in range(22)]
        for i, j in edges:
            f = 3-len(red[i] & red[j]) if j in red[i] else 6-len(blue[i] & blue[j])
            F[i][j] = F[j][i] = f
        m = sum(d)//2
        for i in range(22):
            require(sum(F[i]) == 2*m-294+38*d[i]-d[i]**2-2*sum(d[j] for j in red[i]),
                    'literal signed incident-defect bridge')
            require((sum(F[i])-d[i]) % 2 == 0, 'literal signed incident parity')
        require(sum(map(sum, F)) == 132-3*sum((x-10)**2 for x in d),
                'literal signed total-defect bridge')
        K = [[2*int(j in red[i])+(2*d[i]-17)*int(i == j)
              for j in range(22)] for i in range(22)]
        H = forced_matrix(d, F)
        require([[sum(x*y for x, y in zip(a, b)) for b in K] for a in K] == H,
                'literal signed K-square bridge')
        records.append((mask, d, digest(F), digest(H)))
    return {'signed_graphs': len(records), 'incident_identities': 22*len(records),
            'square_entries': 484*len(records), 'control_sha256': digest(records)}


def nonsquare_witness(value):
    for p in range(3, 200, 2):
        if prime(p) and value % p and pow(value % p, (p-1)//2, p) == p-1:
            return p, value % p
    return None


def multiply(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def square_exception(degrees, F, H, moduli):
    """Infer mechanisms from actual matrices, not original case labels."""
    plane_pairs = []
    for a, b in combinations(range(22), 2):
        if all(H[i][a]-H[i][b] == 33*(int(i == a)-int(i == b))
               for i in range(22)):
            plane_pairs.append((a, b))
    if plane_pairs:
        require(len(plane_pairs) == 2 and len(set(sum(plane_pairs, ()))) == 4,
                'two disjoint literal33 contrasts')
        kept = [i for i in range(22) if i not in [b for a, b in plane_pairs]]
        minor = [[H[i][j]-33*int(i == j) for j in kept] for i in kept]
        witness = next(((p, determinant_mod(minor, p)) for p in range(3, 200)
                        if prime(p) and determinant_mod(minor, p)), None)
        require(witness is not None, 'nonzero20-minor proves full33-plane')
        solutions = [(a, b, c) for a, b, c in product(range(9), repeat=3)
                     if (a*a+b*b-33*c*c) % 9 == 0]
        require(len(solutions) == 27 and all(a % 3 == b % 3 == c % 3 == 0
                                             for a, b, c in solutions),
                'primitive rational33 norm obstruction')
        return {'mechanism': 'entire_rational33_plane', 'basis_pairs': plane_pairs,
                'rank_lower_minor_order': 20, 'deleted_indices': [b for a, b in plane_pairs],
                'minor_prime': witness[0], 'minor_nonzero_residue': witness[1],
                'null_vectors': 2, 'norm_mod9_solutions': len(solutions)}

    groups = [[i for i, d in enumerate(degrees) if d == color] for color in (8, 9, 10)]
    require(list(map(len, groups)) == [9, 4, 9], 'last exception histogram')
    Q = [[sum(H[group[0]][j] for j in other) for other in groups] for group in groups]
    for a, group in enumerate(groups):
        for b, other in enumerate(groups):
            constant = H[group[0]][other[0]] if a != b else H[group[0]][group[1]]
            require(all(H[i][j] == constant+25*int(i == j)
                        for i in group for j in other), 'literal25 contrast decomposition')
            require(all(sum(H[i][j] for j in other) == Q[a][b] for i in group),
                    'literal invariant indicator space')
    shifted = [[Q[i][j]-25*int(i == j) for j in range(3)] for i in range(3)]
    require(determinant_crt(shifted, moduli)[0] != 0, 'separate25 and quotient spaces')
    Q2 = multiply(Q, Q)
    trace = sum(Q[i][i] for i in range(3))
    coefficient = (trace*trace-sum(Q2[i][i] for i in range(3)))//2
    determinant = determinant_crt(Q, moduli)[0]
    polynomial = [1, -trace, coefficient, -determinant]
    residues = [sum(c*x**(3-i) for i, c in enumerate(polynomial)) % 5 for x in range(5)]
    require(all(residues), 'monic quotient cubic irreducible modulo5')
    L = [[5, 4, 6], [9, 1, 9], [6, 4, 13]]
    require(multiply(L, L) == Q, 'literal known rational quotient root')
    trL = sum(L[i][i] for i in range(3))
    root_traces = sorted({sign*trL+5*(19-2*k) for sign in (-1, 1) for k in range(20)})
    host_trace = sum(2*d-17 for d in degrees)
    require(len(root_traces) == 40 and host_trace not in root_traces,
            'all rational root traces exclude prescribed host trace')
    require({t % 10 for t in root_traces} == {4, 6} and host_trace % 10 == 2,
            'trace congruence refinement')
    classes = [degrees[i]-8 for i in range(22)]
    scaled = []
    for i in range(22):
        row = []
        for j in range(22):
            a, b = classes[i], classes[j]
            numerator = 36*(L[a][b]-5*int(a == b))
            require(numerator % len(groups[b]) == 0, 'exact scaled root entry')
            row.append(180*int(i == j)+numerator//len(groups[b]))
        scaled.append(row)
    require(scaled == list(map(list, zip(*scaled))), 'literal symmetric positive root control')
    require(multiply(scaled, scaled) == [[1296*x for x in row] for row in H],
            'literal full positive rational square root')
    require(sum(scaled[i][i] for i in range(22)) == 36*114, 'positive trace114 control')
    return {'mechanism': 'rational_root_trace_classification', 'quotient': Q,
            'quotient_charpoly': polynomial, 'mod5_values': residues,
            'det_quotient_minus25I': determinant_crt(shifted, moduli)[0],
            'contrast_dimension': 19, 'quotient_root': L, 'quotient_root_trace': trL,
            'all_rational_root_traces': root_traces, 'trace_residues_mod10': [4, 6],
            'required_host_trace': host_trace, 'positive_symmetric_root_trace': 114,
            'positive_scaled_root_sha256': digest(scaled), 'symmetric_hypothesis_needed_for_trace': False}


def complete_profiles(counts, units):
    result = set()
    for k in range(1, units+1):
        for comp in compositions(units, k):
            for colors in product((8, 9, 10), repeat=k):
                if all(colors.count(d) <= counts[d-8] for d in (8, 9, 10)):
                    result.add(tuple(sorted((d, 2*q) for d, q in zip(colors, comp))))
    return sorted(result, key=lambda key: (len(key), key))


def run():
    moduli = primes()
    require(all(prime(p) for p in moduli) and len(set(moduli)) == 8,
            'distinct proved prime moduli')
    for a, b, c, d in product(range(-2, 3), repeat=4):
        require(determinant_crt([[a, b], [c, d]], moduli)[0] == a*d-b*c,
                'all625 signed2x2 determinant controls')
    templates, all_records, prime_records, square_records = [], {}, [], []
    use_count = Counter()
    for counts in [(7, 10, 5), (9, 4, 9)]:
        keys, ordered = core_census(counts, 4)
        profiles = complete_profiles(counts, 4)
        records, squares, nonempty = [], [], Counter()
        for key in keys:
            d, F = make_defect(counts, key)
            require(sum(map(sum, F)) == counts[1]+8, 'complete incident surplus eight')
            H = forced_matrix(d, F)
            determinant, proof = determinant_crt(H, moduli)
            require(determinant > 0, 'positive exact determinant')
            use_count[len(proof['residues'])] += 1
            r = isqrt(determinant)
            nonempty[key[0]] += 1
            orbit = core_orbit(*key)
            records.append((key, orbit, determinant, r, digest([F, H])))
            if r*r == determinant:
                certificate = square_exception(d, F, H, moduli)
                squares.append({'key': key, 'determinant': determinant, 'root': r,
                                'matrix_sha256': digest(H), 'certificate': certificate})
                square_records.append((counts, key, certificate))
            else:
                require(r*r < determinant < (r+1)**2, 'strict nonsquare interval')
                witness = nonsquare_witness(determinant)
                require(witness is not None, 'small-prime nonsquare witness')
                p, residue = witness
                require(determinant_mod(H, p) == residue and
                        residue not in {x*x % p for x in range(p)},
                        'direct field nonresidue independently agrees')
                prime_records.append((counts, key, p, residue))
        require(set(nonempty) <= set(profiles), 'all generated profiles in complete domain')
        profile_rows = [(p, nonempty[p]) for p in profiles]
        all_records[counts] = records
        templates.append({'histogram': counts, 'red_edges': sum(d)//2,
                          'profiles': len(profiles), 'nonempty_profiles': len(nonempty),
                          'empty_profiles': [p for p in profiles if not nonempty[p]],
                          'canonical_forms': len(keys), 'fixed_type_labeled_cores': sum(r[1] for r in records),
                          'ordered_cores_by_center_count': {str(k): v for k, v in ordered.items()},
                          'all_ordered_type_cores': sum(ordered.values()),
                          'profile_rows_sha256': digest(profile_rows),
                          'complete_exact_records_sha256': digest(records),
                          'nonsquare_cases': len(records)-len(squares), 'square_cases': squares})
    require([t['canonical_forms'] for t in templates] == [768, 343], 'complete two-domain census')
    require(len(prime_records) == 1108 and len(square_records) == 3, 'all determinant branches closed')
    return {'agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer', 'target_height': 8164,
            'complete': True, 'author_imports': False, 'determinant_method': 'prime fields, CRT uniqueness, Hadamard bound',
            'prime_moduli': moduli, 'CRT_prime_counts': {str(k): v for k, v in use_count.items()}, 'templates': templates,
            'small_prime_witness_histogram': {str(k): v for k, v in Counter(p for counts, key, p, r in prime_records).items()},
            'nonzero_nonsquare_cases': len(prime_records),
            'maximum_small_prime_witness': max(p for counts, key, p, r in prime_records),
            'small_prime_stream_sha256': digest(prime_records),
            'square_certificate_stream_sha256': digest(square_records),
            'literal_bridge_controls': literal_bridge_controls(), 'determinant_controls': 625,
            'global_degree_and_prior_budget_theorems_replayed': False, 'Ramsey_endpoint_decided': False}, all_records


def compare_author(path, records):
    """Passive comparison after entire independent mathematical computation."""
    original = json.loads(path.read_text())
    compared = 0
    for template in original['histograms']:
        counts = tuple(template['degree_histogram'])
        reference = {}
        for row in template['records']:
            index, weights, orbit, value, floor_root, fingerprint = row
            types = tuple(tuple(t) for t in template['profiles'][index]['types'])
            key = canonical_core(types, tuple(weights))
            require(key not in reference, 'original key uniqueness')
            reference[key] = (orbit, value, floor_root, fingerprint)
        require(set(reference) == {row[0] for row in records[counts]}, 'entire original domain agrees')
        for key, orbit, determinant, root, fingerprint in records[counts]:
            require(reference[key] == (orbit, determinant, root, fingerprint),
                    'every original orbit, determinant, root and fullF/H entry fingerprint agrees')
            compared += 1
    require(compared == 1111, 'all1111 original records compared')
    return {'records_compared': compared, 'full_F_and_H_entries_authenticated': 2*484*compared,
            'source_data_selected_independent_domain': False, 'all_passed': True}


def compare_full_matrices(path, records):
    original = json.loads(path.read_text())
    required = {(counts, key) for counts, rows in records.items() for key, *_ in rows}
    seen = set()
    for row in original:
        counts = tuple(row['histogram'])
        key = (tuple(tuple(t) for t in row['profile']), tuple(row['weights']))
        identity = (counts, key)
        require(identity in required and identity not in seen, 'literal source matrix domain and uniqueness')
        seen.add(identity)
        d, F = make_defect(counts, key)
        require(row['F'] == F and row['H'] == forced_matrix(d, F),
                'every full source F/H entry agrees literally')
    require(seen == required, 'complete literal matrix comparison')
    return {'records_compared': len(seen), 'literal_entries_compared': 2*484*len(seen),
            'source_data_selected_independent_domain': False, 'all_passed': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', type=Path)
    parser.add_argument('--compare-author', type=Path)
    parser.add_argument('--compare-matrices', type=Path)
    args = parser.parse_args()
    result, records = run()
    if args.check:
        require(canonical_bytes(result) == canonical_bytes(json.loads(args.check.read_text())),
                'complete expected output mismatch')
    if args.compare_author:
        result['author_comparison'] = compare_author(args.compare_author, records)
    if args.compare_matrices:
        result['literal_source_comparison'] = compare_full_matrices(args.compare_matrices, records)
    print(json.dumps(result, sort_keys=True, indent=2))

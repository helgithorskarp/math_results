#!/usr/bin/env python3
"""six-reviewer-4: complete independent53-form first-slack audit.

No author imports or expected fixtures determine the domain. Ordered surplus
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


def run():
    moduli = primes()
    require(all(prime(p) for p in moduli) and len(set(moduli)) == 8,
            'distinct proved prime moduli')
    for matrix, expected in [([[0, 1], [2, 3]], -2), ([[1, 2], [2, 4]], 0), ([[7]], 7)]:
        require(determinant_crt(matrix, moduli)[0] == expected,
                'CRT singular/swap/size1 controls')
    templates, all_records, prime_records = [], {}, []
    use_count = Counter()
    for counts in [(6, 14, 2), (8, 8, 6), (10, 2, 10)]:
        keys, ordered = core_census(counts, 2)
        records = []
        for key in keys:
            d, F = make_defect(counts, key)
            require(sum(map(sum, F)) == counts[1]+4, 'complete incident surplus four')
            H = forced_matrix(d, F)
            determinant, proof = determinant_crt(H, moduli)
            use_count[len(proof['residues'])] += 1
            r = isqrt(determinant)
            require(r*r < determinant < (r+1)**2, 'positive strict nonsquare interval')
            witness = nonsquare_witness(determinant)
            require(witness is not None, 'small-prime determinant witness')
            p, residue = witness
            require(determinant_mod(H, p) == residue, 'direct field determinant agrees')
            require(residue not in {x*x % p for x in range(p)}, 'nonresidue checked directly')
            records.append((key, core_orbit(*key), determinant, r, digest([F, H])))
            prime_records.append((counts, key, p, residue))
        all_records[counts] = records
        templates.append({'histogram': counts, 'red_edges': sum(d)//2, 'profiles': len({k[0] for k in keys}),
                          'canonical_forms': len(keys), 'ordered_cores_by_center_count': dict(ordered),
                          'complete_exact_records_sha256': digest(records)})
    require([t['canonical_forms'] for t in templates] == [22, 22, 9],
            'complete three-domain census')
    histograms = [(a, 32-3*a, 2*a-10) for a in range(23)
                  if 32-3*a >= 0 and 2*a-10 >= 0 and (32-3*a) % 2 == 0]
    require(histograms == list(all_records), 'all parity-slack-four histograms')
    summary = {'agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
               'target_height': 8042, 'determinant_method': 'prime-field elimination, CRT and Hadamard uniqueness',
               'author_imports': False, 'prime_moduli': moduli, 'CRT_prime_counts': dict(use_count),
               'templates': templates, 'nonzero_nonsquare_cases': len(prime_records),
               'maximum_small_prime_witness': max(r[-2] for r in prime_records),
               'small_prime_certificates': prime_records,
               'small_prime_certificates_sha256': digest(prime_records),
               'literal_bridge_controls': literal_bridge_controls(),
               'global_degree_and_saturation_theorems_replayed': False,
               'Ramsey_endpoint_decided': False}
    return summary, all_records


def compare_author(path, records):
    """Passive diagnostic: called only after all53 computations are complete."""
    old = json.loads(path.read_text())
    compared = 0
    require(len(old['template_results']) == 3, 'three original domains')
    for template in old['template_results']:
        counts = tuple(template['degree_histogram'])
        reference = {}
        for row in template['records']:
            types = tuple((d, f-d % 2) for d, f in zip(row['center_classes'], row['center_row_degrees']))
            weights = (row['center_edge_weight'],) if len(types) == 2 else ()
            key = (types, weights)
            require(key not in reference, 'original record key uniqueness')
            reference[key] = row
        require(set(reference) == {r[0] for r in records[counts]}, 'entire original domain')
        for key, orbit, determinant, root, fingerprint in records[counts]:
            d, F = make_defect(counts, key)
            H = forced_matrix(d, F)
            edges = [[i, j, F[i][j]] for i, j in combinations(range(22), 2) if F[i][j]]
            row = reference[key]
            require(row['det_H'] == determinant and row['floor_sqrt_det'] == root
                    and row['defect_edges'] == edges and row['forced_matrix_sha256'] == digest(H),
                    'every original determinant, root, defect edge and full matrix hash agrees')
            compared += 1
    require(compared == 53, 'all53 original records')
    return {'records_compared': compared, 'normal_forms_by_domain': [22, 22, 9],
            'domain_membership_independent_of_author_fixture': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', type=Path)
    parser.add_argument('--compare-author', type=Path, help='optional original first_slack_expected.json')
    args = parser.parse_args()
    result, records = run()
    if args.compare_author:
        result['author_comparison'] = compare_author(args.compare_author, records)
    if args.check:
        require(canonical_bytes(result) == canonical_bytes(json.loads(args.check.read_text())),
                'complete expected output mismatch')
    print(json.dumps(result, sort_keys=True, indent=2))

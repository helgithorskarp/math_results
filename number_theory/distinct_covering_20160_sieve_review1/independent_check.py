#!/usr/bin/env python3
"""Independent finite covering audit by six-reviewer-1 (reviewer).

No author code imports: pairwise p-adic agreement orbits; literal residue
bit sets; value-layer union weights; finite resources for all 53 exclusions.
"""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import product, permutations
import json
from math import gcd, lcm
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


@lru_cache(None)
def axes(n):
    result, p = [], 2
    while p*p <= n:
        q = 1
        while n % p == 0:
            q *= p
            n //= p
        if q > 1:
            result.append((p, q))
        p += 1
    if n > 1:
        result.append((n, n))
    return tuple(result)


@lru_cache(None)
def divisors(n):
    return tuple(m for m in range(1, n+1) if n % m == 0)


def eligible(n):
    return tuple(m for m in divisors(n) if m >= 8)


def canon(A):
    """Relabel original child digits, then reconstruct each class by CRT."""
    names, normalized = {}, []
    for m, a in A:
        coordinates = []
        for p, q in axes(m):
            power, coordinate = 1, 0
            while power < q:
                labels = names.setdefault((p, power, a % power), {})
                digit = a // power % p
                if digit not in labels:
                    labels[digit] = len(labels)
                coordinate += labels[digit]*power
                power *= p
            coordinates.append((q, coordinate))
        normalized.append((m, sum(r*(m//q)*pow(m//q, -1, q)
                                   for q, r in coordinates) % m))
    return tuple(normalized)


def options(m, A):
    """Stabilizer orbits from distances to all previously fixed prefixes."""
    A = tuple(A)
    need(canon(A) == A, 'prefix not normalized')
    factors = [(b, tuple(q for p, q in axes(gcd(m, n)))) for n, b in A]
    representatives, phases = set(), set()
    for a in range(m):
        signature = tuple(gcd(a-b, q) for b, qs in factors for q in qs)
        if signature in representatives:
            continue
        representatives.add(signature)
        B = canon(A+((m, a),))
        need(B[:-1] == A, 'normalization moved the fixed prefix')
        phases.add(B[-1][1])
    need(len(phases) == len(representatives), 'distinct orbits normalized together')
    return sorted(phases)


class Period:
    def __init__(self, Q):
        self.Q = Q
        self.full = (1 << Q)-1
        self.masks, self.axis_masks = {}, {}

    def classes(self, m):
        need(self.Q % m == 0, 'class modulus does not divide period')
        if m not in self.masks:
            seed = sum(1 << x for x in range(0, self.Q, m))
            self.masks[m] = tuple(seed << a for a in range(m))
        return self.masks[m]

    def residual(self, A):
        U = self.full
        for m, a in A:
            U &= ~self.classes(m)[a]
        return U

    def fibre_max(self, U, g):
        if g == self.Q:
            return int(bool(U))
        return max((U & mask).bit_count() for mask in self.classes(g))

    def box_layers(self, boxes):
        qs = tuple(q for p, q in axes(self.Q))
        layers, occupied = defaultdict(int), 0
        for box in boxes:
            need(len(box) == len(qs)+1 and type(box[-1]) is int and box[-1] > 0,
                 'invalid box weight or dimension')
            points = self.full
            for mask, q in zip(box[:-1], qs):
                need(type(mask) is int and 0 < mask < 1 << q, 'invalid axis mask')
                key = (q, mask)
                if key not in self.axis_masks:
                    bits = 0
                    for a in range(q):
                        if mask >> a & 1:
                            bits |= self.classes(q)[a]
                    self.axis_masks[key] = bits
                points &= self.axis_masks[key]
            need(not points & occupied, 'overlapping weight boxes')
            occupied |= points
            layers[box[-1]] |= points
        need(occupied, 'empty weight support')
        return tuple(sorted(layers.items())), occupied

    def weights(self, layers):
        values = [0]*self.Q
        for w, bits in layers:
            while bits:
                one = bits & -bits
                values[one.bit_length()-1] = w
                bits -= one
        return values

    def singles(self, values, m):
        hist = [0]*m
        for x, w in enumerate(values):
            hist[x % m] += w
        return max(hist)

    def pairs(self, layers, m, n):
        largest, digest = 0, sha256()
        for left in self.classes(m):
            for right in self.classes(n):
                union = left | right
                value = sum(w*(union & bits).bit_count() for w, bits in layers)
                largest = max(largest, value)
                digest.update((str(value)+',').encode())
        return largest, digest.hexdigest(), m*n


def uniform(L, Q, U, remaining, period):
    grouped = defaultdict(int)
    for m in remaining:
        grouped[gcd(Q, m)] += L // lcm(Q, m)
    demand = L//Q*U.bit_count()
    capacity = sum(factor*period.fibre_max(U, g) for g, factor in grouped.items())
    return demand, capacity


def search(L, anchor_moduli, visit_completion):
    A_mod = tuple(anchor_moduli)
    need(A_mod and len(set(A_mod)) == len(A_mod) and all(m in eligible(L) for m in A_mod),
         'invalid anchor list')
    Q = lcm(*A_mod)
    period = Period(Q)
    remaining = [tuple(m for m in eligible(L) if m not in A_mod[:depth])
                 for depth in range(len(A_mod)+1)]
    nodes, pruned, leaves, upper = [0]*(len(A_mod)+1), 0, 0, -1
    digest = sha256()

    def walk(A, U):
        nonlocal pruned, leaves, upper
        depth = len(A)
        nodes[depth] += 1
        D, C = uniform(L, Q, U, remaining[depth], period)
        value = L-D+C
        if depth >= 2 and value < L:
            tag = 'cut'
            pruned += 1
        elif depth == len(A_mod):
            tag = 'leaf'
            leaves += 1
            need(visit_completion is not None, 'finite proof has an unexcluded leaf')
            visit_completion(A)
        else:
            m = A_mod[depth]
            for a in options(m, A):
                walk(A+((m, a),), U & ~period.classes(m)[a])
            return
        upper = max(upper, value)
        digest.update((json.dumps([tag, [a for m, a in A], value], separators=(',', ':'))+'\n').encode())

    walk((), period.full)
    return {'L': L, 'anchors': list(A_mod), 'Q': Q, 'upper': upper,
            'excludes': upper < L, 'nodes': nodes, 'pruned': pruned,
            'leaves': leaves, 'proof_events_sha256': digest.hexdigest()}


def replay(cert, expected, progress=False):
    need((cert['format_version'], cert['lower'], cert['upper_exclusive']) == (1, 10080, 30240),
         'invalid finite interval')
    records = {}
    for r in cert['nodes']:
        L, A = r['L'], tuple(tuple(row) for row in r['anchors'])
        need(all(type(m) is int and type(a) is int and m in eligible(L) and 0 <= a < m for m, a in A)
             and len(set(m for m, a in A)) == len(A), 'invalid record classes')
        need(canon(A) == A and (L, A) not in records, 'duplicate or unnormalized record')
        records[L, A] = r
    used, counts, events, pair_events = set(), Counter(), sha256(), sha256()
    boxes = points = phase_pairs = 0

    def complete(L, A, P):
        nonlocal boxes, points, phase_pairs
        key = (L, A)
        need(key in records and key not in used, 'missing or reused proof node')
        used.add(key)
        r, B = records[key], tuple(m for m in eligible(L) if m not in dict(A))
        kind, payload = r['kind'], r['payload']
        counts[kind] += 1
        if kind == 'expanded':
            m = payload['modulus']
            need(m in B and payload['phases'] == options(m, A), 'incomplete child list')
            phases = payload['phases']
            need(phases, 'empty branch')
            events.update((json.dumps([L, A, kind, m, phases], separators=(',', ':'))+'\n').encode())
            for a in phases:
                complete(L, A+((m, a),), P)
            return
        if kind == 'uniform':
            D, C = uniform(L, L, P.residual(A), B, P)
            capacities = None
        else:
            need(kind == 'weighted', 'unknown proof-node kind')
            layers, support = P.box_layers(payload['boxes'])
            need(support & ~P.residual(A) == 0, 'weight at an already covered point')
            D = sum(w*bits.bit_count() for w, bits in layers)
            points += support.bit_count()
            boxes += len(payload['boxes'])
            values = P.weights(layers)
            assigned, groups = set(), []
            for pair in payload.get('pairs', []):
                need(len(pair) == 2 and pair[0] != pair[1] and
                     all(type(m) is int and m in B and m not in assigned for m in pair),
                     'invalid resource pair')
                assigned.update(pair)
                groups.append(tuple(pair))
            groups.extend((m,) for m in B if m not in assigned)
            capacities = []
            for group in groups:
                if len(group) == 1:
                    Cg = P.singles(values, group[0])
                else:
                    Cg, h, tuples = P.pairs(layers, *group)
                    phase_pairs += tuples
                    pair_events.update((json.dumps([L, A, group, h], separators=(',', ':'))+'\n').encode())
                capacities.append(Cg)
            C = sum(capacities)
            counts['grouped_weighted'] += bool(payload.get('pairs'))
        need(D > C and (D, C) == (payload['demand'], payload['capacity']), 'invalid strict cut')
        event = [L, A, kind, D, C] if capacities is None else [L, A, kind, D, list(zip(groups, capacities))]
        events.update((json.dumps(event, separators=(',', ':'))+'\n').encode())

    cases = []
    plan_L = [plan['L'] for plan in cert['plans']]
    need(plan_L == sorted(set(plan_L)), 'duplicate or unordered plans')
    for plan, reference in zip(cert['plans'], expected['cases']):
        L, P = plan['L'], Period(plan['L'])
        before, size = counts.copy(), len(used)
        need(plan['method'] in ('uniform', 'weighted_leaves'), 'unknown plan method')
        manifest = search(L, plan['anchors'], (lambda A: complete(L, A, P))
                          if plan['method'] == 'weighted_leaves' else None)
        delta = counts-before
        case = {'L': L, 'method': plan['method'], 'base_manifest': manifest,
                'completion_nodes': len(used)-size, 'completion_counts': dict(sorted(delta.items()))}
        need(case == reference, 'case mismatch: '+str(L))
        cases.append(case)
        if progress:
            print('checked finite case '+str(L), flush=True)
    need(len(cases) == len(cert['plans']) == len(expected['cases']) == 44, 'missing finite case')
    need(used == set(records), 'unused records')
    summary = {'cases': cases, 'completion_node_counts': dict(sorted(counts.items())),
               'boxes': boxes, 'positive_weight_points_checked': points,
               'pair_phase_tuples_checked': phase_pairs,
               'completion_events_sha256': events.hexdigest(),
               'pair_capacities_sha256': pair_events.hexdigest()}
    for k, v in summary.items():
        need(v == expected[k], 'completion audit mismatch: '+k)
    return summary


def finite_extra(L, hints, anchor_moduli):
    """Finite capacities only: no unrestricted exponent theorem is an input."""
    periods, records, used_hints = {}, {}, set()
    for row in hints['certificates']:
        phases, Q, boxes = row if len(row) == 3 else (row[0], hints['Q'], row[1])
        key = tuple(phases)
        need(key not in records, 'duplicate weight hint')
        records[key] = (Q, boxes)
    Q = lcm(*anchor_moduli)
    need(L % Q == 0, 'anchor period does not divide the finite LCM')
    P = Period(Q)
    nodes, cuts, weighted, digest = Counter(), 0, 0, sha256()

    def walk(A, U):
        nonlocal cuts, weighted
        nodes[len(A)] += 1
        B = tuple(m for m in eligible(L) if m not in dict(A))
        D, C = uniform(L, Q, U, B, P)
        kind = 'uniform'
        if D <= C and tuple(a for m, a in A) in records:
            q, boxes = records[tuple(a for m, a in A)]
            need(L % q == 0 and all(q % m == 0 for m, a in A), 'bad hint period')
            R = periods.setdefault(q, Period(q))
            layers, support = R.box_layers(boxes)
            need(support & ~R.residual(A) == 0, 'weight hint has covered support')
            values = R.weights(layers)
            D = L//q*sum(values)
            C = sum(L//lcm(q, m)*R.singles(values, gcd(q, m)) for m in B)
            kind = 'weighted'
        if D > C:
            cuts += 1
            weighted += kind == 'weighted'
            if kind == 'weighted':
                used_hints.add(tuple(a for m, a in A))
            digest.update((json.dumps([A, kind, D, C], separators=(',', ':'))+'\n').encode())
            return
        need(len(A) < len(anchor_moduli), 'extra finite case has an open leaf: '+str((L, A, D, C)))
        m = anchor_moduli[len(A)]
        for a in options(m, A):
            walk(A+((m, a),), U & ~P.classes(m)[a])

    walk((), P.full)
    need(used_hints == set(records), 'unused finite weight hints')
    return {'L': L, 'anchors': list(anchor_moduli), 'nodes_by_depth': dict(sorted(nodes.items())),
            'strict_terminal_cuts': cuts, 'weighted_cuts': weighted,
            'terminal_events_sha256': digest.hexdigest(), 'open_leaves': 0}


def cover_audit(data):
    rows, L = data['congruences'], data['lcm']
    need(all(type(a) is int and type(m) is int and 0 <= a < m for a, m in rows), 'invalid cover row')
    need([m for a, m in rows] == list(eligible(L)), 'cover does not use precisely eligible divisors')
    need(lcm(*(m for a, m in rows)) == L == 20160 and min(m for a, m in rows) == 8,
         'incorrect cover period or minimum')
    qs, all_bits = tuple(q for p, q in axes(L)), (1 << len(rows))-1
    tables = [tuple(sum(1 << i for i, (a, m) in enumerate(rows)
                        if r % gcd(q, m) == a % gcd(q, m)) for r in range(q)) for q in qs]
    crt = tuple(L//q*pow(L//q, -1, q) for q in qs)
    membership, seen = [0]*L, set()
    for coordinate in product(*(range(q) for q in qs)):
        bits = all_bits
        for r, table in zip(coordinate, tables):
            bits &= table[r]
        x = sum(r*c for r, c in zip(coordinate, crt)) % L
        need(x not in seen and all(x % q == r for q, r in zip(qs, coordinate)), 'CRT bijection failed')
        seen.add(x)
        membership[x] = bits
    need(len(seen) == L and all(membership), 'certificate leaves an uncovered point')
    # Independent definition-level reconstruction, including all private counts.
    literal = [sum(1 << i for i, (a, m) in enumerate(rows) if x % m == a) for x in range(L)]
    need(membership == literal, 'tensor/literal membership mismatch')
    private = Counter(bits.bit_length()-1 for bits in membership if bits.bit_count() == 1)
    need(len(private) == len(rows), 'a certificate class is redundant')
    multiplicities = bytes(bits.bit_count() for bits in membership)
    return {'classes': len(rows), 'lcm': L, 'minimum_modulus': 8,
            'coverage_multiplicities': dict(sorted(Counter(map(str, multiplicities)).items())),
            'multiplicity_bytes_sha256': sha256(multiplicities).hexdigest(),
            'private_points_by_modulus': [[m, private[i]] for i, (a, m) in enumerate(rows)],
            'total_incidences': sum(multiplicities), 'CRT_axes': list(qs),
            'CRT_tuples_checked': len(seen), 'literal_predicates_checked': L*len(rows)}


def main():
    here = Path(__file__).resolve().parent
    root = here.parents[1] if here.parent.name == 'number_theory' else here
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, help='private download directory for certificate and expected')
    parser.add_argument('--cover', type=Path, default=here/'cover.json')
    parser.add_argument('--finite-weights', type=Path, default=here/'finite_weights.json')
    parser.add_argument('--write', type=Path)
    parser.add_argument('--progress', action='store_true')
    args = parser.parse_args()
    inputs = args.inputs or root/'number_theory/distinct_covering_min8_lcm_sieve'
    paths = {'certificate': inputs/'certificate.json', 'author_expected': inputs/'expected.json',
             'cover': args.cover, 'finite_weights': args.finite_weights}
    hashes = {name: sha256(path.read_bytes()).hexdigest() for name, path in paths.items()}
    data = {name: json.loads(path.read_text()) for name, path in paths.items()}
    result = {'agent': 'six-reviewer-1', 'role': 'independent mathematical reviewer',
              'input_sha256': hashes, 'cover': cover_audit(data['cover'])}
    result['sieve_replay'] = replay(data['certificate'], data['author_expected'], args.progress)
    density, retained = [], []
    for L in range(10080, 30240, 8):
        (density if sum(L//m for m in eligible(L)) < L else retained).append(L)
    extras = sorted(set(retained)-set(p['L'] for p in data['certificate']['plans'])-
                    set(data['certificate']['remaining_LCMs']))
    need(extras == [11520, 12960, 14400, 17280, 18000, 19440, 23040, 25920, 28800], 'unexpected finite gap')
    finite = []
    for L in extras:
        three = L in (14400, 18000, 28800)
        hints = {'certificates': data['finite_weights']['cases'].get(str(L), [])}
        anchors = (8, 9, 10, 12, 15, 18, 20, 24, 25, 30) if three else (8, 9, 10, 12, 15, 18, 20, 24)
        finite.append(finite_extra(L, hints, anchors))
        if args.progress:
            print('checked additional finite case '+str(L), flush=True)
    result['extra_finite_exclusions'] = finite
    need(data['finite_weights']['format_version'] == 1 and set(data['finite_weights']['cases']) == {'25920', '28800'},
         'unexpected finite weight case map')
    result['density_exclusion_count'] = len(density)
    result['finite_remaining_LCMs'] = sorted(set(retained)-set(extras)-set(p['L'] for p in data['certificate']['plans']))
    need(len(density) == 2456 and len(retained) == 64 and result['finite_remaining_LCMs'] == data['certificate']['remaining_LCMs'],
         'incomplete exhaustive interval sieve')
    result['possible_L_min_8'] = [L for L in result['finite_remaining_LCMs'] if L <= result['cover']['lcm']]
    import sys
    from controls import controls
    result['controls'] = controls(sys.modules[__name__], data['cover'])
    # Normalize tuples/dictionary keys before expected comparison.
    result = json.loads(json.dumps(result))
    if args.write:
        args.write.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    else:
        need(result == json.loads((here/'expected.json').read_text()), 'reviewer manifest mismatch')
    print(json.dumps({k: v for k, v in result.items() if k not in ('sieve_replay', 'cover')}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

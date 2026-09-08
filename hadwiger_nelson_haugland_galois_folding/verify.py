#!/usr/bin/env python3
"""Certify a lower bound on all edge-preserving pointwise Galois foldings.

Independent Cartesian modular reconstruction and synchronous propagation.
No producer imports, floating arithmetic, SAT solver, or computer algebra.
"""
import argparse
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'hadwiger_nelson_haugland2131_exact_reproduction/graph.json'
SOURCE_SHA = '201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d'


def require(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def arithmetic(cert):
    p, r, t, s = (cert[k] for k in ('prime', 'root42', 'root84', 'sqrt5'))
    require(all(type(v) is int for v in (p, r, t, s)), 'arithmetic types')
    require(p > 7 and all(p % d for d in range(2, isqrt(p)+1)), 'prime')
    require(pow(r, 42, p) == 1 and all(pow(r, 42//q, p) != 1 for q in (2, 3, 7)),
            'exact root order')
    require(t*t % p == r and pow(t, 84, p) == 1, 'root84')
    require(s*s % p == 5 and all(x % p for x in (2, 3, 7)), 'sqrt5 or denominators')
    actions = [(a, e) for a in range(42) if gcd(a, 42) == 1 for e in (1, -1)]
    require(len(actions) == 24, 'Galois action count')
    return p, r, t, s, actions


def cartesian_source(source, cert):
    """Lift each action to Q(zeta84,sqrt5) fixing i, then use real x/y formulas."""
    p, r, t, s, actions = arithmetic(cert)
    I = pow(t, 21, p)
    require(I*I % p == p-1, 'imaginary unit')
    inv2, inv4, inv8, invI = [pow(v, -1, p) for v in (2, 4, 8, I)]
    coordinates = []
    for a, sign in actions:
        lift = a if a % 4 == 1 else a+42
        require(lift % 4 == 1 and lift % 42 == a, 'action lift')
        z = pow(t, lift, p)
        require(pow(z, 21, p) == I and z*z % p == pow(r, a, p), 'lift values')
        sqrt3 = (pow(z, 14, p)-pow(z, -14, p))*invI % p
        require(sqrt3*sqrt3 % p == 3, 'sqrt3')

        def sin(k):
            return (pow(z, k, p)-pow(z, -k, p))*inv2*invI % p

        alpha, beta = pow(sin(12), -1, p), pow(sin(24), -1, p)
        bx, by = sqrt3*(alpha+beta)*inv4 % p, (alpha-beta)*inv4 % p
        vectors = []
        for j in range(42):
            c = (pow(z, 2*j, p)+pow(z, -2*j, p))*inv2 % p
            h = sin(2*j)
            vectors.extend([(c, h), ((bx*c-by*h) % p, (bx*h+by*c) % p)])
        require(all((x*x+y*y) % p == 1 for x, y in vectors), 'unit directions')
        points = [(0, 0)]
        for path in source['paths']:
            x, y = 0, 0
            for step in path:
                require(type(step) is int and 0 <= step < 84, 'path step')
                dx, dy = vectors[step]
                x, y = (x+dx) % p, (y+dy) % p
                points.append((x, y))
            require((x, y) == (0, sqrt3), 'path endpoint')
        g1 = list(dict.fromkeys(points))
        g2 = list(dict.fromkeys(
            [((x+sqrt3*y)*inv2 % p-1, (y-sqrt3*x)*inv2 % p) for x, y in g1] +
            [((x-sqrt3*y)*inv2 % p+1, (y+sqrt3*x)*inv2 % p) for x, y in g1]))
        # Canonical residues must precede deduplication at the +/-1 translations.
        g2 = list(dict.fromkeys((x % p, y % p) for x, y in g2))
        v = sqrt3*sign*s % p
        g3 = list(dict.fromkeys(g2 + [(((7*(x+1)-v*y)*inv8-1) % p,
                                     (7*y+v*(x+1))*inv8 % p) for x, y in g2]))
        require([len(g1), len(g2), len(g3)] == [740, 1066, 2131], 'Cartesian counts')
        for u, w in source['G3_edges']:
            x, y = g3[u]
            X, Y = g3[w]
            require(((x-X)**2+(y-Y)**2) % p == 1, 'source modular edge')
        coordinates.append(g3)
    rows = [tuple((coordinates[k][v][0]+I*coordinates[k][v][1]) % p
                  for k in range(24)) for v in range(2131)]
    require(len(set(rows)) == 2131, 'source shadow collisions')
    ind = {a: k for k, a in enumerate(actions)}
    conjugate = [ind[((-a) % 42, e)] for a, e in actions]
    for v, row in enumerate(rows):
        for k in range(24):
            x, y = coordinates[k][v]
            require((row[k]+row[conjugate[k]])*inv2 % p == x and
                    (row[k]-row[conjugate[k]])*inv2*invI % p == y,
                    'conjugation and Cartesian bridge')
    return rows, actions


def closure(rows, actions):
    ind = {a: k for k, a in enumerate(actions)}
    permutations = [[ind[(a*c % 42, b*d)] for c, d in actions] for a, b in actions]
    sites, lookup, domains = [], {}, []
    for row in rows:
        images = []
        for perm in permutations:
            image = tuple(row[k] for k in perm)
            if image not in lookup:
                lookup[image] = len(sites)
                sites.append(image)
            images.append(lookup[image])
        domains.append(tuple(sorted(set(images))))
    identity = [lookup[row] for row in rows]
    return sites, domains, identity, permutations


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask -= bit


def compatibility(sites, domains, edges, p, actions):
    ind = {a: k for k, a in enumerate(actions)}
    conj = [ind[((-a) % 42, e)] for a, e in actions]

    def unit(i, j):
        x, y = sites[i], sites[j]
        return all((x[k]-y[k])*(x[conj[k]]-y[conj[k]]) % p == 1 for k in range(24))

    table = {}
    for u, v in edges:
        du, dv = domains[u], domains[v]
        if (du, dv) not in table:
            t = {i: sum(1 << j for j in dv if unit(i, j)) for i in du}
            table[du, dv] = t
            table[dv, du] = {j: sum(1 << i for i in du if t[i] >> j & 1) for j in dv}
    return table


def propagate(domains, edges, table, anchor, image):
    """Synchronous complete sweeps, different from the producer's AC-3 queue."""
    current = [sum(1 << i for i in d) for d in domains]
    current[anchor] = 1 << image
    rounds, removed = 0, 0
    while True:
        following = current[:]
        for u, v in edges:
            for x, y in ((u, v), (v, u)):
                t = table[domains[x], domains[y]]
                supported = sum(1 << i for i in bits(current[x]) if t[i] & current[y])
                following[x] &= supported
        require(all(following), 'empty domain despite identity solution')
        if following == current:
            return current, rounds, removed
        removed += sum(a.bit_count()-b.bit_count() for a, b in zip(current, following))
        current = following
        rounds += 1


def separated_witness(domains, vertices):
    require(isinstance(vertices, list) and all(type(v) is int and 0 <= v < len(domains)
                                             for v in vertices), 'witness labels')
    require(len(set(vertices)) == len(vertices), 'duplicate witness')
    union = 0
    for v in vertices:
        require(domains[v] != 0 and not union & domains[v], 'overlapping witness domains')
        union |= domains[v]
    return len(vertices)


def run(cert):
    data = SOURCE.read_bytes()
    require(hashlib.sha256(data).hexdigest() == SOURCE_SHA, 'source hash')
    source = json.loads(data)
    edges = source['G3_edges']
    require(len(edges) == 12530 and edges == sorted(edges) and
            len({tuple(e) for e in edges}) == len(edges) and
            all(len(e) == 2 and all(type(x) is int for x in e) and 0 <= e[0] < e[1] < 2131
                for e in edges), 'source edge format')
    rows, actions = cartesian_source(source, cert)
    sites, domains, identity, perms = closure(rows, actions)
    require(len(sites) == 6049 and len(set(domains)) == 355, 'shadow orbit counts')
    anchor = cert['anchor']
    require(type(anchor) is int and 0 <= anchor < len(rows), 'anchor')
    # Every possible anchor image occurs under a global coordinate permutation.
    require({tuple(rows[anchor][k] for k in perm) for perm in perms} ==
            {sites[i] for i in domains[anchor]}, 'anchor orbit coverage')
    table = compatibility(sites, domains, edges, cert['prime'], actions)
    final, rounds, removed = propagate(domains, edges, table, anchor, identity[anchor])
    require(all(mask >> i & 1 for mask, i in zip(final, identity)), 'lost identity solution')
    bound = separated_witness(final, cert['disjoint_domain_vertices'])
    require(bound == cert['image_order_lower_bound'] == 1251, 'bound')
    histogram = {str(k): sum(d.bit_count() == k for d in final) for k in sorted({d.bit_count() for d in final})}
    result = {'verified': True, 'source_vertices': 2131, 'source_edges': 12530,
              'source_edges_checked_per_action': 12530, 'actions': len(actions),
              'source_complex_shadow_sha256': digest(rows), 'shadow_sites': len(sites),
              'shadow_site_sha256': digest(sites), 'shadow_orbits': len(set(domains)),
              'anchor': anchor, 'anchor_choices_before_normalization': len(domains[anchor]),
              'synchronous_rounds': rounds, 'removed_domain_values': removed,
              'final_domain_size_histogram': histogram,
              'final_domains_sha256': digest([list(bits(d)) for d in final]),
              'pairwise_disjoint_nonempty_domains': bound, 'image_order_lower_bound': bound,
              'lower_bound_attainment_claimed': False, 'target_508_excluded': True,
              'chromatic_lower_bound_reproved': False, 'record_improvement': False}
    return result, final


def controls(cert, final):
    tests = 0
    for key, value in [('prime', 1000000008), ('root42', 1), ('root84', 1), ('sqrt5', 1)]:
        bad = dict(cert)
        bad[key] = value
        try:
            arithmetic(bad)
        except ValueError:
            tests += 1
        else:
            raise ValueError('malformed arithmetic accepted')
    v = cert['disjoint_domain_vertices'][0]
    for bad in [[v, v], [-1], [True]]:
        try:
            separated_witness(final, bad)
        except ValueError:
            tests += 1
        else:
            raise ValueError('malformed witness accepted')
    # Exhaust all list assignments for small domain systems and compare to safe propagation.
    from itertools import product
    fixtures = 0
    for edge_mask in range(8):
        edges = [e for k, e in enumerate([(0, 1), (0, 2), (1, 2)]) if edge_mask >> k & 1]
        for rel in range(1, 8):
            target_edges = [e for k, e in enumerate([(0, 1), (0, 2), (1, 2)]) if rel >> k & 1]
            t = {i: sum(1 << j for j in range(3) if tuple(sorted((i, j))) in target_edges)
                 for i in range(3)}
            # Check one synchronous revision directly against every compatible assignment.
            for masks in product(range(1, 8), repeat=3):
                before = list(masks)
                after = before[:]
                for u, w in edges:
                    for x, y in [(u, w), (w, u)]:
                        after[x] &= sum(1 << i for i in bits(before[x]) if t[i] & before[y])
                for word in product(*(list(bits(m)) for m in masks)):
                    if all(t[word[u]] >> word[w] & 1 for u, w in edges):
                        require(all(after[v] >> word[v] & 1 for v in range(3)), 'unsafe revision')
                fixtures += 1
    return {'malformed_certificates_rejected': tests, 'small_domain_systems_exhausted': fixtures}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-expected', action='store_true')
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    cert = json.loads((HERE/'certificate.json').read_text())
    result, final = run(cert)
    if args.check_expected:
        require(result == json.loads((HERE/'expected.json').read_text()), 'expected output')
    if args.controls:
        result['controls'] = controls(cert, final)
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()

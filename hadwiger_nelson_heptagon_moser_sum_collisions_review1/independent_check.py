#!/usr/bin/env python3
"""Independent exact review of the heptagon--spindle collision closure.

This file imports no module from the reviewed package.  It uses a direct
Q[t,s]/(Phi_42(t), s^2+11) implementation.  Full graph scans use two sound
finite-field filters; every modular candidate is then checked exactly.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
import math
from pathlib import Path


class CheckError(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise CheckError(message)


N = 12
ZK = (Fraction(0),) * N
OK = (Fraction(1),) + ZK[1:]
# Phi_42 = x^12+x^11-x^9-x^8+x^6-x^4-x^3+x+1.
PHI = tuple(map(Fraction, (1, 1, 0, -1, -1, 0, 1, 0, -1, -1, 0, 1, 1)))


def kadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ksub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def kscale(a, q):
    q = Fraction(q)
    return tuple(q * x for x in a)


def kmul(a, b):
    out = [Fraction(0)] * (2 * N - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i + j] += x * y
    for degree in range(2 * N - 2, N - 1, -1):
        lead = out[degree]
        if lead:
            for i in range(N):
                out[degree - N + i] -= lead * PHI[i]
    return tuple(out[:N])


_TPOW = {}


def ktpow(exponent):
    exponent %= 42
    if exponent not in _TPOW:
        value = OK
        x = (Fraction(0), Fraction(1)) + (Fraction(0),) * (N - 2)
        for _ in range(exponent):
            value = kmul(value, x)
        _TPOW[exponent] = value
    return _TPOW[exponent]


def kconj(a):
    out = ZK
    for i, coefficient in enumerate(a):
        if coefficient:
            out = kadd(out, kscale(ktpow(-i), coefficient))
    return out


def kinverse(a):
    columns = [kmul(a, ktpow(j)) for j in range(N)]
    matrix = [[columns[col][row] for col in range(N)] + [Fraction(row == 0)]
              for row in range(N)]
    for col in range(N):
        pivot = next((row for row in range(col, N) if matrix[row][col]), None)
        need(pivot is not None, "noninvertible K element")
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        scale = matrix[col][col]
        matrix[col] = [x / scale for x in matrix[col]]
        for row in range(N):
            if row != col and matrix[row][col]:
                factor = matrix[row][col]
                matrix[row] = [x - factor * y for x, y in zip(matrix[row], matrix[col])]
    result = tuple(matrix[row][-1] for row in range(N))
    need(kmul(a, result) == OK, "K inversion check failed")
    return result


# An L element is a pair (a,b), representing a(t)+b(t)s with s^2=-11.
ZE = (ZK, ZK)
OE = (OK, ZK)
SE = (ZK, OK)


def eadd(a, b):
    return kadd(a[0], b[0]), kadd(a[1], b[1])


def esub(a, b):
    return ksub(a[0], b[0]), ksub(a[1], b[1])


def escale(a, q):
    return kscale(a[0], q), kscale(a[1], q)


def emul(a, b):
    return (ksub(kmul(a[0], b[0]), kscale(kmul(a[1], b[1]), 11)),
            kadd(kmul(a[0], b[1]), kmul(a[1], b[0])))


def econj(a):
    return kconj(a[0]), kscale(kconj(a[1]), -1)


def enorm(a):
    return emul(a, econj(a))


def erat(q):
    return (kscale(OK, Fraction(q)), ZK)


def etpow(exponent):
    return ktpow(exponent), ZK


def ediv_k_numerator(numerator, denominator):
    return kmul(numerator, kinverse(denominator)), ZK


def construct_factors():
    pden = ksub(ktpow(24), ktpow(-24))
    qden = ksub(ktpow(6), ktpow(-6))
    rden = ksub(ktpow(12), ktpow(-12))
    H = []
    for j in range(7):
        H.append(ediv_k_numerator(ktpow(6 * j), pden))
    for j in range(7):
        H.append(ediv_k_numerator(kscale(ktpow(6 * j - 7), -1), qden))
    for j in range(7):
        H.append(ediv_k_numerator(kscale(ktpow(6 * j + 7), -1), rden))
    u, v = esub(H[7], H[0]), esub(H[14], H[0])
    directions = (u, v, eadd(u, v))
    rho = escale(eadd(erat(5), SE), Fraction(1, 6))
    M = [ZE, u, v, eadd(u, v)] + [emul(rho, x) for x in directions]
    return H, M


def decode_row(row):
    need(isinstance(row, list) and len(row) == 2, "malformed encoded element")
    nums, denominator = row
    need(isinstance(nums, list) and len(nums) == 24, "wrong encoded width")
    need(isinstance(denominator, int) and denominator > 0, "bad denominator")
    need(all(isinstance(v, int) for v in nums), "nonintegral coefficient")
    need(math.gcd(denominator, *nums) == 1, "noncanonical encoded element")
    return (tuple(Fraction(v, denominator) for v in nums[:12]),
            tuple(Fraction(v, denominator) for v in nums[12:]))


def is_rational(a):
    return not any(a[0][1:]) and not any(a[1])


def spectrum(points):
    return Counter(enorm(esub(points[i], points[j]))
                   for i, j in combinations(range(len(points)), 2))


def unit_edges_exact(points):
    return [(i, j) for i, j in combinations(range(len(points)), 2)
            if enorm(esub(points[i], points[j])) == OE]


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def prime_factors(n):
    factors = set()
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.add(divisor)
            n //= divisor
        divisor += 1
    if n > 1:
        factors.add(n)
    return factors


def primitive_root(p):
    factors = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise CheckError("primitive root not found")


def tonelli_shanks(n, p):
    n %= p
    need(pow(n, (p - 1) // 2, p) == 1, "quadratic residue required")
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    c = pow(z, q, p)
    x = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    while t != 1:
        i, value = 1, t * t % p
        while value != 1:
            value = value * value % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        x = x * b % p
        t = t * b * b % p
        c = b * b % p
        m = i
    return x


def finite_models(count=2):
    models = []
    k = 1_000_000 // 42 + 1
    while len(models) < count:
        p = 42 * k + 1
        if is_prime(p) and pow(p - 11, (p - 1) // 2, p) == 1:
            g = primitive_root(p)
            t = pow(g, (p - 1) // 42, p)
            s = tonelli_shanks(p - 11, p)
            need(pow(t, 42, p) == 1, "bad t root")
            need(all(pow(t, 42 // q, p) != 1 for q in (2, 3, 7)), "t not primitive")
            need(sum(int(PHI[i]) * pow(t, i, p) for i in range(13)) % p == 0,
                 "Phi42 does not vanish")
            need(s * s % p == p - 11, "bad s root")
            models.append((p, t, s))
        k += 1
    return models


def fraction_mod(q, p):
    return q.numerator % p * pow(q.denominator, -1, p) % p


def evaluate(a, model, conjugated=False):
    p, t, s = model
    if conjugated:
        t = pow(t, -1, p)
        s = -s % p
    power = 1
    value = 0
    for i in range(N):
        value += fraction_mod(a[0][i], p) * power
        value += fraction_mod(a[1][i], p) * power * s
        value %= p
        power = power * t % p
    return value


def complete_edges(points, models):
    images = [[(evaluate(point, model), evaluate(point, model, True))
               for point in points] for model in models]
    edges = []
    candidates = false_positives = 0
    for i, j in combinations(range(len(points)), 2):
        possible = True
        for model, rows in zip(models, images):
            p = model[0]
            value = (rows[i][0] - rows[j][0]) * (rows[i][1] - rows[j][1]) % p
            if value != 1:
                possible = False
                break
        if possible:
            candidates += 1
            if enorm(esub(points[i], points[j])) == OE:
                edges.append((i, j))
            else:
                false_positives += 1
    return edges, candidates, false_positives


def proper(row, edges, n, colours=4):
    return (len(row) == n and all(isinstance(x, int) and 0 <= x < colours for x in row)
            and all(row[i] != row[j] for i, j in edges))


def file_info(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    H, M = construct_factors()
    need(len(H) == len(set(H)) == 21, "H point count")
    need(len(M) == len(set(M)) == 7, "M point count")
    need(emul(SE, SE) == erat(-11) and econj(SE) == escale(SE, -1), "s identities")
    need(enorm(esub(H[7], H[0])) == OE, "u is unit")

    hs, ms = spectrum(H), spectrum(M)
    need((len(hs), len(ms)) == (25, 7), "spectrum sizes")
    need(set(hs) & set(ms) == {OE}, "spectrum intersection")
    need({x for x in hs if is_rational(x)} == {OE}, "H rational spectrum")
    omega = etpow(7)
    gamma = emul(esub(OE, escale(omega, 2)), SE)
    need(emul(gamma, gamma) == erat(33), "gamma squared")
    need(econj(gamma) == gamma and any(gamma[1]), "gamma reality and K exclusion")
    expected_m = Counter({
        OE: 11,
        erat(3): 2,
        erat(Fraction(1, 3)): 2,
        escale(eadd(erat(7), gamma), Fraction(1, 6)): 1,
        escale(esub(erat(7), gamma), Fraction(1, 6)): 1,
        escale(eadd(erat(9), gamma), Fraction(1, 6)): 2,
        escale(esub(erat(9), gamma), Fraction(1, 6)): 2,
    })
    need(ms == expected_m, "exact M radical spectrum")

    hd = {esub(a, b) for a in H for b in H if a != b}
    md = {esub(a, b) for a in M for b in M if a != b}
    need((len(hd), len(md)) == (420, 34), "directed difference counts")
    hnorm = {a: enorm(a) for a in hd}
    mnorm = {b: enorm(b) for b in md}
    collisions = Counter()
    for a in hd:
        for b in md:
            if hnorm[a] == mnorm[b]:
                need(hnorm[a] == OE, "nonunit common difference")
                collisions[emul(a, econj(b))] += 1
    need(len(collisions) == 252 and sum(collisions.values()) == 1176, "collision census")
    need(Counter(collisions.values()) == {2: 84, 6: 168}, "collision multiplicities")

    certificate_path = args.source / "contacts_certificate.json"
    certificate = json.loads(certificate_path.read_text())
    need(isinstance(certificate, list) and len(certificate) == 36, "certificate rows")
    zeta = etpow(6)
    need({emul(zeta, h) for h in H} == set(H), "C7 action on H")
    covered = set()
    representatives = []
    for record in certificate:
        need(set(record) == {"r", "H_colouring", "M_colouring"}, "certificate fields")
        rotation = decode_row(record["r"])
        need(enorm(rotation) == OE, "rotation norm")
        orbit = {emul(etpow(6 * j), rotation) for j in range(7)}
        need(len(orbit) == 7 and not (covered & orbit), "disjoint C7 orbit")
        covered |= orbit
        representatives.append((rotation, record["H_colouring"], record["M_colouring"]))
    need(covered == set(collisions), "certificate orbits cover the full collision set")

    he, me = unit_edges_exact(H), unit_edges_exact(M)
    need((len(he), len(me)) == (42, 11), "factor unit graphs")
    three_colourings = sum(proper(list(row), me, 7, 3) for row in product(range(3), repeat=7))
    need(three_colourings == 0, "spindle unexpectedly three-colourable")

    models = finite_models()
    pair_checks = edge_checks = fibre_checks = exact_candidates = false_positives = 0
    invalid_colours_rejected = 0
    cases = Counter()
    fibre_types = Counter()
    for rotation, p, q in representatives:
        need(proper(p, he, 21) and proper(q, me, 7), "factor colouring")
        rotated_m = [emul(rotation, m) for m in M]
        points = sorted({eadd(h, m) for h in H for m in rotated_m})
        index = {point: i for i, point in enumerate(points)}
        fibres = [[] for _ in points]
        for i, h in enumerate(H):
            for j, m in enumerate(rotated_m):
                fibres[index[eadd(h, m)]].append((i, j))
        need(sum(map(len, fibres)) == 147, "formal sum coverage")
        edges, candidates, false_count = complete_edges(points, models)
        edge_set = set(edges)
        factor = {tuple(sorted((index[eadd(H[a], m)], index[eadd(H[b], m)])))
                  for a, b in he for m in rotated_m}
        factor |= {tuple(sorted((index[eadd(h, rotated_m[a])], index[eadd(h, rotated_m[b])])))
                   for a, b in me for h in H}
        need(factor <= edge_set, "factor edge missing")
        extra = edge_set - factor
        colouring = []
        for fibre in fibres:
            values = {p[a] ^ q[b] for a, b in fibre}
            need(len(values) == 1, "XOR colouring does not descend")
            colouring.append(values.pop())
        need(proper(colouring, edges, len(points)), "improper sum colouring")
        embedding = [index[eadd(H[0], m)] for m in rotated_m]
        need(len(set(embedding)) == 7, "spindle embedding collision")
        need(all(tuple(sorted((embedding[a], embedding[b]))) in edge_set for a, b in me),
             "spindle edge missing")
        bad = colouring.copy()
        bad[edges[0][0]] = bad[edges[0][1]]
        need(not proper(bad, edges, len(points)), "invalid colouring control")
        invalid_colours_rejected += 1
        pair_checks += len(points) * (len(points) - 1) // 2
        edge_checks += len(edges)
        fibre_checks += 147
        exact_candidates += candidates
        false_positives += false_count
        cases[(len(points), len(edges), len(extra))] += 1
        fibre_types[tuple(sorted(Counter(map(len, fibres)).items()))] += 1

    need(cases == {(142, 513, 0): 12, (143, 512, 0): 12,
                   (146, 523, 0): 6, (146, 525, 2): 6}, "representative cases")
    need(pair_checks == 368988 and edge_checks == 18588, "graph scan totals")
    need(fibre_checks == 5292 and invalid_colours_rejected == 36, "witness totals")

    result = {
        "all_checks_passed": True,
        "scope": "all collision orientations of the fixed H+rM family",
        "target_graph_claimed": False,
        "algebra": {
            "representation": "Q[t,s]/(Phi42(t),s^2+11)",
            "H_vertices": len(H),
            "M_vertices": len(M),
            "H_spectrum_size": len(hs),
            "M_spectrum_size": len(ms),
            "spectrum_intersection": [1],
            "H_rational_spectrum": [1],
            "M_radical_spectrum_verified": True,
        },
        "collision_check": {
            "H_directed_differences": len(hd),
            "M_directed_differences": len(md),
            "difference_pair_comparisons": len(hd) * len(md),
            "equal_length_pairs": sum(collisions.values()),
            "rotations": len(collisions),
            "multiplicity_histogram": dict(sorted(Counter(collisions.values()).items())),
            "C7_representatives": len(representatives),
            "certificate_orbits_cover_entrywise": True,
        },
        "graph_check": {
            "representative_pair_checks": pair_checks,
            "representative_edge_checks": edge_checks,
            "formal_sum_representations": fibre_checks,
            "case_histogram": [list(key) + [value] for key, value in sorted(cases.items())],
            "fibre_histograms": [[[[a, b] for a, b in key], value]
                                  for key, value in sorted(fibre_types.items())],
            "proper_XOR_colourings": 36,
            "invalid_colourings_rejected": invalid_colours_rejected,
            "proper_spindle_three_colourings": three_colourings,
            "spindle_embeddings": 36,
        },
        "finite_field_filter": {
            "models": [{"prime": p, "t": t, "s": s} for p, t, s in models],
            "exact_candidates": exact_candidates,
            "false_positives": false_positives,
            "soundness": "exact unit implies unit in each finite-field image; every candidate rechecked exactly",
        },
        "inputs": {
            "contacts_certificate.json": file_info(certificate_path),
            "collisions_certificate.json": file_info(args.source / "collisions_certificate.json"),
        },
    }
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS exact spectra, 252 collision rotations, and 36 four-coloured representatives")


if __name__ == "__main__":
    main()

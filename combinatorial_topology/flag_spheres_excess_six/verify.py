#!/usr/bin/env python3
"""Exact audits of PROOF.md, not an enumeration or topology oracle.

Python 3.11+, standard library only. All checks remain active under python -O.
The graph identity audit uses face counts and triangular basis conversion,
independently of the closed complement formulas it checks.
"""

from fractions import Fraction
from itertools import combinations
from math import comb
import argparse
import hashlib
import json
from pathlib import Path
import random


def require(condition, message):
    if not condition:
        raise ValueError(message)


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def multiply(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c


def gamma_from_faces(f, d, degree):
    """f[j] counts faces of cardinality j, including f[0]=1."""
    h = [sum((-1) ** (k-j) * choose(d-j, k-j) * f[j]
             for j in range(min(k, len(f)-1)+1))
         for k in range(degree+1)]
    g = []
    for k in range(degree+1):
        g.append(h[k] - sum(g[j] * choose(d-2*j, k-j)
                            for j in range(k)))
    return g


def adjacency(n, edges):
    a = [0] * n
    for u, v in edges:
        require(0 <= u < v < n, "invalid edge")
        a[u] |= 1 << v
        a[v] |= 1 << u
    return a


def mask_graph(n, mask):
    return adjacency(n, [e for i, e in enumerate(combinations(range(n), 2))
                         if mask >> i & 1])


def complement(a):
    full = (1 << len(a)) - 1
    return [full ^ (1 << v) ^ row for v, row in enumerate(a)]


def direct_counts(a):
    """Vertices, edges, triangles of the graph a, by direct incidences."""
    n = len(a)
    edges = sum(row.bit_count() for row in a) // 2
    triangles = sum(bool((a[u] >> v & 1) and (a[u] >> w & 1)
                         and (a[v] >> w & 1))
                    for u, v, w in combinations(range(n), 3))
    return [1, n, edges, triangles]


def link_face_counts(h, v):
    vertices = [u for u in range(len(h)) if u != v and not (h[v] >> u & 1)]
    edges = sum(not (h[u] >> w & 1) for u, w in combinations(vertices, 2))
    return [1, len(vertices), edges]


def check_identity(h, d):
    n = len(h)
    ell = n - 2*d
    q = [row.bit_count() for row in h]
    m = sum(q) // 2
    triangles = direct_counts(h)[3]
    g = gamma_from_faces(direct_counts(complement(h)), d, 3)
    a, b = g[2:4]
    require(g[1] == ell, "excess mismatch")
    require(a == d + Fraction(ell*(ell+5), 2) - m, "gamma_2 identity")
    constant = Fraction((ell+4)*(6*d+ell*ell+11*ell), 6)
    predicted_b = constant + sum(Fraction(x*(x-ell-5), 2) for x in q) - triangles
    require(b == predicted_b, "gamma_3 identity")
    local_sum = 0
    for v in range(n):
        neighbors = [u for u in range(n) if h[v] >> u & 1]
        tv = sum(bool(h[u] >> w & 1) for u, w in combinations(neighbors, 2))
        observed = gamma_from_faces(link_face_counts(h, v), d-1, 2)[2]
        predicted = a + ell + 2 + Fraction(q[v]*(q[v]-2*ell-7), 2)
        predicted += sum(q[u] for u in neighbors) - tv
        require(observed == predicted, "individual link identity")
        local_sum += observed
    require(local_sum == (2*d-8)*a+3*b, "summed link identity")
    k = Fraction(ell*(ell*ell+3*ell+20-12*d), 6)
    residual = sum((x-3)*(ell+1-x) for x in q)
    require(b == a+k-Fraction(residual, 2)-triangles, "degree budget identity")
    return n


def graph_audit():
    graph_count = identity_count = link_count = 0
    for n in range(7):
        for mask in range(1 << choose(n, 2)):
            h = mask_graph(n, mask)
            graph_count += 1
            for d in (6, 7, 8, 9):
                link_count += check_identity(h, d)
                identity_count += 1
    rng = random.Random(6112026)
    random_count = 0
    for d in range(6, 13):
        for ell in range(7):
            n = 2*d + ell
            pairs = list(combinations(range(n), 2))
            for numerator in (1, 3, 5):
                edges = [e for e in pairs if rng.randrange(8) < numerator]
                link_count += check_identity(adjacency(n, edges), d)
                identity_count += 1
                random_count += 1
    return {"all_graphs_through_six_vertices": graph_count,
            "additional_deterministic_graphs": random_count,
            "parameterized_identity_instances": identity_count,
            "individual_link_identity_instances": link_count,
            "random_generator": "Python random.Random, seed 6112026"}


def arithmetic_audit():
    # The written proof handles all d by the negative slope -(6ell+2).
    rows = []
    for ell in (4, 5, 6):
        k6 = Fraction(ell*(ell*ell+3*ell+20-72), 6)
        gap = 3*k6-7
        require(gap < 0, "failed gamma_2 contradiction")
        for d in range(6, 201):
            k = Fraction(ell*(ell*ell+3*ell+20-12*d), 6)
            require(3*k-(2*d-5) == gap-(d-6)*(6*ell+2), "slope identity")
        rows.append({"ell": ell, "K_at_d6": int(k6),
                     "S_upper_if_gamma2_negative_at_d6": int(gap),
                     "decrease_per_dimension": 6*ell+2})
    chord_checks = 0
    for ell in range(2, 51):
        for q in range(3, ell+2):
            left = Fraction(q*(q-ell-5), 2)
            right = -Fraction(q+3*(ell+1), 2)
            require(right-left == Fraction((q-3)*(ell+1-q), 2), "chord identity")
            require(left <= right, "chord inequality")
            chord_checks += 1
    return {"gamma2_induction": rows, "degree_chord_checks": chord_checks}


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(total-first, length-1):
                yield (first,) + rest


def profile_audit():
    output = {}
    for d in (8, 9):
        n = 2*d+6
        tested = 0
        survivors = []
        for counts in compositions(n, 5):
            tested += 1
            twice_m = sum(q*c for q, c in zip(range(3, 8), counts))
            if twice_m % 2:
                continue
            a = d+33-twice_m//2
            b_without_triangles = 10*d+170 + sum(
                Fraction(q*(q-11)*c, 2) for q, c in zip(range(3, 8), counts))
            require(b_without_triangles < 0, "high-dimensional gamma_3 bound")
            s0 = (2*d-8)*a + 3*b_without_triangles
            costs = (0, 10, 17, 21, 22) if d == 8 else (0, 11, 19, 24, 26)
            base = 22 if d == 8 else -24
            require(s0 == base-sum(c*w for c, w in zip(counts, costs)), "profile identity")
            if s0 < 0:
                continue
            require(d == 8, "unexpected d9 survivor")
            degree_excess = twice_m-3*n
            require(degree_excess <= 4, "degree excess bound")
            bound = 1+Fraction(degree_excess, 2)
            require(bound <= 3 < 5, "cubic link contradiction")
            survivors.append({"counts_q3_through_q7": list(counts),
                              "T_max": int(s0//3), "gamma_2": a,
                              "D": degree_excess,
                              "cubic_link_gamma2_upper": int(bound)})
        output[str(d)] = {"degree_count_profiles_tested": tested,
                          "profiles_passing_parity_and_S_at_T0": survivors}
    require(len(output["8"]["profiles_passing_parity_and_S_at_T0"]) == 4,
            "unexpected profile census")
    return output


def cycle(length):
    return adjacency(length, sorted({tuple(sorted((i, (i+1) % length)))
                                     for i in range(length)}))


def join(a, b):
    n, m = len(a), len(b)
    return [row | (((1 << m)-1) << n) for row in a] + [
        (row << n) | ((1 << n)-1) for row in b]


def subdivide(a, u, v):
    require(a[u] >> v & 1, "subdivision requires an edge")
    a = a.copy()
    common = a[u] & a[v]
    n = len(a)
    new_neighbors = common | (1 << u) | (1 << v)
    a[u] ^= 1 << v
    a[v] ^= 1 << u
    for w in range(n):
        if new_neighbors >> w & 1:
            a[w] |= 1 << n
    a.append(new_neighbors)
    return a


def all_faces(a):
    faces = [0]
    for v in range(len(a)):
        faces += [mask | (1 << v) for mask in faces if mask & ~a[v] == 0]
    return faces


def fixture(name, a):
    faces = all_faces(a)
    d = max(mask.bit_count() for mask in faces)
    f = [sum(mask.bit_count() == k for mask in faces) for k in range(d+1)]
    gamma = gamma_from_faces(f, d, d//2)
    # Check the full polynomial, not just its low coefficient conversion.
    h = [sum((-1)**(k-j)*choose(d-j, k-j)*f[j] for j in range(k+1))
         for k in range(d+1)]
    reconstructed = [sum(gamma[j]*choose(d-2*j, k-j)
                         for j in range(len(gamma))) for k in range(d+1)]
    require(h == reconstructed == h[::-1], "fixture h/gamma identity")
    qmin = min(row.bit_count() for row in complement(a))
    # Topology follows from the documented join and edge-subdivision construction.
    if d >= 6:
        check_identity(complement(a), d)
    return {"name": name, "n": len(a), "d": d, "ell": len(a)-2*d,
            "minimum_complement_degree": qmin, "faces_by_cardinality": f,
            "gamma": gamma, "faces_including_empty": len(faces)}


def fixture_audit():
    fixtures = []
    b8 = subdivide(join(cycle(5), [0, 0]), 0, 5)
    current = b8
    for ell in range(2, 5):
        f = fixture(f"near_maximal_ell{ell}", current)
        expected = multiply([1, 2], [choose(ell-2, j) for j in range(ell-1)])
        require(f["gamma"] == expected and f["minimum_complement_degree"] > 1,
                "near-maximal fixture")
        fixtures.append(f)
        current = join(current, cycle(5))
    current = cycle(5)
    for ell in range(1, 5):
        f = fixture(f"maximal_ell{ell}", current)
        require(f["gamma"] == [choose(ell, j) for j in range(ell+1)], "maximal fixture")
        fixtures.append(f)
        current = join(current, cycle(5))
    octahedron = join(join([0, 0], [0, 0]), [0, 0])
    b9 = octahedron
    for edge in ((0, 2), (3, 4), (1, 5)):
        b9 = subdivide(b9, *edge)
    boundary = join(b9, b9)
    for suspensions in range(3):
        f = fixture(f"excess6_zero_gamma3_susp{suspensions}", boundary)
        require(f["gamma"][:4] == [1, 6, 9, 0], "boundary fixture")
        require(all(x == 0 for x in f["gamma"][4:]), "suspension coefficient")
        fixtures.append(f)
        boundary = join(boundary, [0, 0])
    product = join(join(cycle(6), cycle(6)), join(cycle(5), cycle(5)))
    f = fixture("excess6_dimension7_minimum2", product)
    require(f["gamma"] == [1, 6, 13, 12, 4] and f["minimum_complement_degree"] == 2,
            "minimum-two fixture")
    fixtures.append(f)
    return fixtures


def polynomial_audit():
    checked = 0
    for ell in range(2, 51):
        expected = multiply([1, 2], [choose(ell-2, j) for j in range(ell-1)])
        # Nonsuspension-link branch: gamma(L)+t gamma(J).
        direct = [choose(ell-1, j) + choose(ell-2, j-1) for j in range(ell)]
        require(direct == expected, "near-maximal equator recurrence")
        if ell >= 3:
            lower = multiply([1, 2], [choose(ell-3, j) for j in range(ell-2)])
            require(multiply([1, 1], lower) == expected, "near-maximal join recurrence")
        checked += 1
    # Independently check (3) in the h basis, on every individual basis term.
    bases = 0
    for d in range(2, 31):
        for i in range(d//2+1):
            h = [choose(d-2*i, k-i) for k in range(d+1)]
            left = [d*h[k] + (k+1)*h[k+1] - k*h[k] for k in range(d)]
            right = [(2*d-4*i)*choose(d-1-2*i, k-i)
                     + i*choose(d-1-2*(i-1), k-(i-1)) for k in range(d)]
            require(left == right, "general link gamma-basis identity")
            bases += 1
    return {"near_maximal_polynomial_instances": checked,
            "link_identity_basis_terms": bases}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", type=Path, help="write canonical audit output")
    args = parser.parse_args()
    result = {"scope": "Exact audit of the written transfer proof; not a topology proof or sphere census",
              "graphs": graph_audit(), "arithmetic": arithmetic_audit(),
              "profiles": profile_audit(), "polynomials": polynomial_audit(),
              "fixtures": fixture_audit()}
    encoded = (json.dumps(result, indent=2, sort_keys=True)+"\n").encode()
    if args.write:
        args.write.write_bytes(encoded)
    else:
        expected = Path(__file__).with_name("EXPECTED.json")
        require(expected.read_bytes() == encoded, "output differs from EXPECTED.json")
    print(json.dumps({"status": "PASS", "sha256": hashlib.sha256(encoded).hexdigest(),
                      "graph_instances": result["graphs"]["parameterized_identity_instances"],
                      "fixtures": len(result["fixtures"])}, sort_keys=True))


if __name__ == "__main__":
    main()

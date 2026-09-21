#!/usr/bin/env python3
"""Exact, direct finite checks for the total-graph fixed-space theorem.

CPython >=3.10, standard library only. Run from any working directory.
--emit writes computed compact evidence to stdout without reading expected.json.
Default compares that evidence exactly with expected.json.
No assertion is used as a validation gate: python -O performs the same checks.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations, product
import argparse
import hashlib
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def edgeset(edges):
    return frozenset(tuple(sorted(e)) for e in edges)


def graph(n, edges):
    e = edgeset(edges)
    require(all(0 <= a < b < n for a, b in e), "invalid simple graph")
    return n, e


def complete(n):
    return graph(n, combinations(range(n), 2))


def automorphisms(g, generators):
    n, edges = g
    for p in generators:
        require(sorted(p) == list(range(n)), "invalid permutation")
        require(edgeset((p[a], p[b]) for a, b in edges) == edges,
                "permutation is not a graph automorphism")


def adjacency(g):
    n, edges = g
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def faces(g):
    """All nonempty cliques; increasing vertex tuples."""
    adj = adjacency(g)
    out = []

    def visit(prefix, candidates):
        for i, v in enumerate(candidates):
            face = prefix + (v,)
            while len(out) < len(face):
                out.append([])
            out[len(face)-1].append(face)
            visit(face, [w for w in candidates[i+1:] if w in adj[v]])

    visit((), list(range(g[0])))
    return out


def triangles(g):
    adj = adjacency(g)
    return [t for t in combinations(range(g[0]), 3)
            if t[1] in adj[t[0]] and t[2] in adj[t[0]]
            and t[2] in adj[t[1]]]


def total_graph(g, generators):
    """Construct adjacencies directly from the three defining rules."""
    n, edges = g
    elist = sorted(edges)
    index = {e: n+i for i, e in enumerate(elist)}
    te = set(edges)
    for e in elist:
        for v in e:
            te.add(tuple(sorted((v, index[e]))))
    for e, f in combinations(elist, 2):
        if set(e) & set(f):
            te.add((index[e], index[f]))
    induced = [list(p) + [index[tuple(sorted((p[a], p[b])))]
                          for a, b in elist] for p in generators]
    tg = graph(n+len(elist), te)
    automorphisms(tg, induced)
    return tg, induced, index


def orbits(n, generators):
    unseen = set(range(n))
    result = []
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        todo = [seed]
        while todo:
            v = todo.pop()
            for p in generators:
                w = p[v]
                if w not in orbit:
                    orbit.add(w)
                    todo.append(w)
        unseen -= orbit
        result.append(tuple(sorted(orbit)))
    return result


def fixed_graph(g, generators):
    """Flag graph of clique vertex-orbits; its clique complex is |Cl G|^H."""
    automorphisms(g, generators)
    adj = adjacency(g)

    def isclique(vs):
        return all(b in adj[a] for a, b in combinations(vs, 2))

    obs = [o for o in orbits(g[0], generators) if isclique(o)]
    edges = [(i, j) for i, j in combinations(range(len(obs)), 2)
             if isclique(obs[i]+obs[j])]
    return graph(len(obs), edges)


def rank_mod(columns, prime):
    """Sparse column reduction with exact integer modular arithmetic."""
    pivots = {}
    for col in columns:
        col = {i: v % prime for i, v in col.items() if v % prime}
        while col:
            pivot = max(col)
            if pivot not in pivots:
                inverse = pow(col[pivot], -1, prime)
                pivots[pivot] = {i: v*inverse % prime for i, v in col.items()}
                break
            factor = col[pivot]
            for i, v in pivots[pivot].items():
                w = (col.get(i, 0)-factor*v) % prime
                if w:
                    col[i] = w
                else:
                    col.pop(i, None)
    return len(pivots)


def trim(values):
    while values and values[-1] == 0:
        values.pop()
    return values


def betti(fs, prime):
    if not fs:
        return []
    ranks = [0]
    for k in range(1, len(fs)):
        lower = {face: i for i, face in enumerate(fs[k-1])}

        def columns():
            for face in fs[k]:
                yield {lower[face[:i]+face[i+1:]]: (-1)**i
                       for i in range(len(face))}
        ranks.append(rank_mod(columns(), prime))
    ranks.append(0)
    b = [len(fs[k])-ranks[k]-ranks[k+1] for k in range(len(fs))]
    require(all(x >= 0 for x in b), "negative Betti number")
    return trim(b)


def canonical(face):
    require(len(set(face)) == len(face), "repeated simplex vertex")
    inv = sum(face[i] > face[j]
              for i in range(len(face)) for j in range(i+1, len(face)))
    return tuple(sorted(face)), (-1)**inv


def clean(chain):
    return {s: c for s, c in chain.items() if c}


def boundary(chain):
    ans = Counter()
    for face, c in chain.items():
        for i in range(len(face)):
            ans[face[:i]+face[i+1:]] += c*(-1)**i
    return clean(ans)


def cycle(tau, index):
    ans = Counter()
    opp = [index[tuple(v for v in tau if v != tau[i])] for i in range(3)]
    for eps in product((0, 1), repeat=3):
        face, sign = canonical(tuple(opp[i] if eps[i] else tau[i]
                                     for i in range(3)))
        ans[face] += sign*(-1)**(3-sum(eps))
    return clean(ans)


def cycle_checks(g, generators, tg, induced, index):
    ts = triangles(g)
    adj = adjacency(tg)
    cycles = {t: cycle(t, index) for t in ts}
    for tau, c in cycles.items():
        require(not boundary(c), "integer octahedral boundary failed")
        require(all(all(b in adj[a] for a, b in combinations(face, 2))
                    for face in c), "cycle uses nonexistent face")
        face, sign = canonical(tuple(index[tuple(v for v in tau if v != tau[i])]
                                     for i in range(3)))
        require(c[face] == sign, "relative generator coefficient failed")
        require(sum(all(v >= g[0] for v in f) for f in c) == 1,
                "unexpected other edge-only face")
        for p, q in zip(generators, induced):
            mapped = Counter()
            for f, coefficient in c.items():
                nf, s = canonical(tuple(q[v] for v in f))
                mapped[nf] += coefficient*s
            nt, s = canonical(tuple(p[v] for v in tau))
            require(clean(mapped) == {f: s*a for f, a in cycles[nt].items()},
                    "orientation character equivariance failed")
    return len(ts), len(ts)*len(generators)


def triangle_counts(g, generators):
    obs = orbits(g[0], generators)
    counts = [0, 0, 0]
    for t in triangles(g):
        st = set(t)
        if all({p[v] for v in t} == st for p in generators):
            count = sum(bool(set(o) & st) for o in obs)
            require(1 <= count <= 3, "wrong triangle orbit number")
            counts[count-1] += 1
    return counts


def multipartite(pair_count):
    return graph(2*pair_count, [(a, b) for a, b in combinations(
        range(2*pair_count), 2) if a//2 != b//2])


def fixtures():
    k3 = complete(3)
    yield "K3_trivial", k3, []
    yield "K3_transposition", k3, [[1, 0, 2]]
    yield "K3_C3", k3, [[1, 2, 0]]
    yield "K3_S3", k3, [[1, 0, 2], [1, 2, 0]]
    yield "K4_C3", complete(4), [[1, 2, 0, 3]]
    yield "K4_transposition", complete(4), [[1, 0, 2, 3]]
    yield "K4_S4", complete(4), [[1, 2, 3, 0], [1, 0, 2, 3]]
    two = graph(6, [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5)])
    yield "two_triangles_exchange", two, [[3, 4, 5, 0, 1, 2]]
    wedge = graph(6, [(0, 1), (0, 2), (1, 2),
                      (0, 3), (3, 4), (4, 5), (0, 5)])
    yield "triangle_wedge_C4_trivial", wedge, []
    yield "triangle_wedge_C4_reflection", wedge, [[0, 2, 1, 3, 4, 5]]
    octa = multipartite(3)
    yield "octahedron_trivial", octa, []
    yield "octahedron_antipodal", octa, [[1, 0, 3, 2, 5, 4]]
    yield "octahedron_pair_cycle", octa, [[2, 3, 4, 5, 0, 1]]
    yield "octahedron_one_pair_flip", octa, [[1, 0, 2, 3, 4, 5]]
    prism = graph(6, set(two[1]) | {(0, 3), (1, 4), (2, 5)})
    yield "triangular_prism_layer_swap", prism, [[3, 4, 5, 0, 1, 2]]
    wheel = graph(5, [(0, 1), (1, 2), (2, 3), (0, 3)]
                  + [(i, 4) for i in range(4)])
    yield "wheel_C4_reflection", wheel, [[1, 0, 3, 2, 4]]
    yield "cross_polytope_S3_trivial", multipartite(4), []
    yield "cross_polytope_S3_one_pair_flip", multipartite(4), [
        [1, 0, 2, 3, 4, 5, 6, 7]]
    # Barycentric subdivision of the six-vertex projective-plane triangulation.
    facets = [(0, 1, 2), (0, 1, 3), (0, 2, 4), (0, 3, 5), (0, 4, 5),
              (1, 2, 5), (1, 3, 4), (1, 4, 5), (2, 3, 4), (2, 3, 5)]
    incidence = Counter(e for t in facets for e in combinations(t, 2))
    require(len(incidence) == 15 and set(incidence.values()) == {2},
            "projective-plane fixture edge incidence")
    nonempty = sorted({s for t in facets for k in range(1, 4)
                       for s in combinations(t, k)}, key=lambda t: (len(t), t))
    comparable = [(i, j) for i, j in combinations(range(len(nonempty)), 2)
                  if set(nonempty[i]) < set(nonempty[j])
                  or set(nonempty[j]) < set(nonempty[i])]
    yield "sd_projective_plane_trivial", graph(len(nonempty), comparable), []


def deformation_checks():
    """Rational controls include ties and every permutation through four edges."""
    count = 0
    times = [F(0), F(1, 3), F(1)]

    def endpoint(t):
        m = sorted(t, reverse=True)[1] if len(t) >= 2 else F(0)
        return tuple(max(x-m, F(0)) for x in t)

    for d in range(5):
        for nums in product(range(5), repeat=d):
            if sum(nums) > 4:
                continue
            t = tuple(F(x, 4) for x in nums)
            r = endpoint(t)
            require(sum(x > 0 for x in r) <= 1, "star image failed")
            require(all(0 <= y <= x for x, y in zip(t, r)), "star positivity")
            if sum(x > 0 for x in t) <= 1:
                require(r == t, "star tree not fixed")
            for p in permutations(range(d)):
                require(endpoint(tuple(t[i] for i in p)) == tuple(r[i] for i in p),
                        "star equivariance")
            for s in times:
                z = tuple((1-s)*x+s*y for x, y in zip(t, r))
                require(all(x >= 0 for x in z) and sum(z) <= 1, "star homotopy")
            count += 1
    for a in range(5):
        for b in range(5-a):
            u, v, e = F(a, 4), F(b, 4), F(4-a-b, 4)
            for s in times:
                z = (u+s*e/2, v+s*e/2, (1-s)*e)
                require(sum(z) == 1 and min(z) >= 0, "incidence homotopy")
                swapped = (v+s*e/2, u+s*e/2, (1-s)*e)
                require(swapped == (z[1], z[0], z[2]), "endpoint exchange")
                if e == 0:
                    require(z == (u, v, e), "original edge not fixed")
    return count


def run():
    results = []
    cycles = signs = 0
    for name, g, generators in fixtures():
        automorphisms(g, generators)
        tg, induced, index = total_graph(g, generators)
        af = faces(fixed_graph(g, generators))
        xf = faces(fixed_graph(tg, induced))
        counts = triangle_counts(g, generators)
        homology = {}
        for prime in (2, 3):
            a, x = betti(af, prime), betti(xf, prime)
            predicted = a + [0]*max(0, 3-len(a))
            for j in range(3):
                predicted[j] += counts[j]
            predicted = trim(predicted)
            require(x == predicted, (name, prime, a, counts, x, predicted))
            homology[str(prime)] = {"A": a, "X": x}
        nc, ns = cycle_checks(g, generators, tg, induced, index)
        cycles += nc
        signs += ns
        results.append({"name": name, "vertices_edges_triangles":
                        [g[0], len(g[1]), len(triangles(g))],
                        "generators": generators, "m1_m2_m3": counts,
                        "fixed_face_counts": {"A": list(map(len, af)),
                                              "X": list(map(len, xf))},
                        "betti": homology})
    byname = {x["name"]: x for x in results}
    require(byname["K3_transposition"]["betti"]["3"]["X"] == [1, 1],
            "reflection control")
    require(byname["K3_C3"]["betti"]["3"]["X"] == [2], "transitive control")
    require(byname["K3_C3"]["betti"]["3"]["A"] == [1],
            "geometric fixed space confused with fixed vertices")
    rp = byname["sd_projective_plane_trivial"]["betti"]
    require(rp["2"]["A"] == [1, 1, 1] and rp["3"]["A"] == [1],
            "torsion control")
    require(byname["cross_polytope_S3_trivial"]["betti"]["3"]["X"]
            == [1, 0, 32, 1], "higher-dimensional control")
    require(byname["two_triangles_exchange"]["betti"]["2"]["X"] == [],
            "empty fixed-space control")
    rejected = []
    # Deliberately false prediction: invariant triangles always add a trivial S2.
    for name in ("K3_transposition", "K3_C3"):
        require(byname[name]["betti"]["3"]["X"] != [1, 0, 1],
                "failed to reject trivially acted-on sphere")
        rejected.append(name+"_trivial_sphere_prediction")
    try:
        automorphisms(graph(3, [(0, 1), (1, 2)]), [[1, 0, 2]])
    except ValueError:
        rejected.append("nonautomorphism")
    else:
        raise ValueError("nonautomorphism not rejected")
    return {"schema": 1, "fixtures": results, "fixture_count": len(results),
            "integer_cycles_checked": cycles,
            "integer_action_signs_checked": signs,
            "rational_star_controls": deformation_checks(),
            "negative_controls_rejected": rejected,
            "coefficient_fields": [2, 3],
            "trust_boundary": "Finite corroboration; universal theorem is the written proof."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.emit:
        print(json.dumps(result, indent=2))
    else:
        expected = Path(__file__).with_name("expected.json").read_bytes()
        require(result == json.loads(expected), "expected evidence mismatch")
        print(json.dumps({"status": "PASS", "fixtures": result["fixture_count"],
              "integer_cycles": result["integer_cycles_checked"],
              "integer_action_signs": result["integer_action_signs_checked"],
              "rational_star_controls": result["rational_star_controls"],
              "expected_sha256": hashlib.sha256(expected).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()

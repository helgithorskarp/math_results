#!/usr/bin/env python3
"""Exact finite validation; never a decision procedure for base asphericity.

Python 3.11+, standard library. Faces are sorted tuples, omitting the empty
face. Inflated vertices are (original_label, copy_number), starting at zero.
"""
import argparse
from collections import Counter, defaultdict, deque
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def closure(facets):
    return {s for f in facets for k in range(1, len(f) + 1)
            for s in combinations(sorted(f), k)}


def validate(K, m):
    require(all(isinstance(x, int) and not isinstance(x, bool) and x >= 1
                for x in m), "positive integer multiplicities required")
    require(K == closure(K), "input is not a simplicial complex")
    require(all(1 <= len(f) <= 3 for f in K), "dimension exceeds two")
    require({f[0] for f in K if len(f) == 1} == set(range(len(m))),
            "vertex labels must be exactly range(len(m))")


def forest(vertices, edges):
    parent = {v: v for v in vertices}

    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v

    for u, v in sorted(edges):
        a, b = root(u), root(v)
        if a == b:
            return False
        parent[a] = b
    return True


def link(K, v):
    return {tuple(x for x in f if x != v) for f in K if v in f and len(f) > 1}


def conditions(K, m):
    S = {v for v, k in enumerate(m) if k > 1}
    c1 = all(forest({f[0] for f in link(K, v) if len(f) == 1},
                    {f for f in link(K, v) if len(f) == 2}) for v in S)
    tris = [set(f) for f in K if len(f) == 3]
    c2 = all(sum(set(e) <= t for t in tris) <= 1
             for e in K if len(e) == 2 and set(e) <= S)
    c3 = all(not t <= S for t in tris)
    return c1, c2, c3


def inflate(K, m):
    return {tuple(zip(f, colors)) for f in K
            for colors in product(*(range(m[v]) for v in f))}


def original(K):
    return {tuple((v, 0) for v in f) for f in K}


def collapse_certificate(I, m):
    """Construct from actual triangles, without invoking the criterion."""
    remaining = set(I)
    certificate = []
    additions = [(v, c) for v, k in enumerate(m) for c in range(1, k)]
    for a in reversed(additions):
        while True:
            triangles = sorted(f for f in remaining if len(f) == 3 and a in f)
            if not triangles:
                break
            incidence = defaultdict(list)
            for t in triangles:
                for x in t:
                    if x != a:
                        incidence[tuple(sorted((a, x)))].append(t)
            free = sorted(e for e, ts in incidence.items() if len(ts) == 1)
            require(free, "cone link contains a cycle")
            e = free[0]
            t = incidence[e][0]
            require(e in remaining, "missing radial edge")
            remaining.remove(t)
            remaining.remove(e)
            certificate.append((t, e))
    return certificate


def replay(I, K0, certificate, restricted=False):
    """Generic verifier: actual face membership and unique coface only."""
    remaining = set(I)
    protected = I & K0
    for t, e in certificate:
        if restricted and t not in remaining:
            continue
        require(t in remaining and e in remaining, "absent collapse face")
        require(len(t) == 3 and len(e) == 2 and set(e) < set(t), "bad pair")
        require(t not in K0 and e not in K0, "deleted original face")
        cofaces = {f for f in remaining if len(f) == 3 and set(e) <= set(f)}
        require(cofaces == {t}, "edge is not free")
        remaining.remove(t)
        remaining.remove(e)
    require(protected <= remaining, "original intersection not preserved")
    require(all(len(f) < 3 or f in K0 for f in remaining), "new triangle left")
    require(remaining == closure(remaining), "result not a subcomplex")
    return remaining


def cycle_from_edges(edges):
    """Find a simple cycle by a path in an independently built forest."""
    adjacency = defaultdict(set)
    for u, v in sorted(edges):
        previous = {u: None}
        queue = deque([u])
        while queue and v not in previous:
            x = queue.popleft()
            for y in sorted(adjacency[x]):
                if y not in previous:
                    previous[y] = x
                    queue.append(y)
        if v in previous:
            path = [v]
            while path[-1] != u:
                path.append(previous[path[-1]])
            return list(reversed(path))
        adjacency[u].add(v)
        adjacency[v].add(u)
    return None


def oriented_add(chain, face, coefficient):
    require(len(set(face)) == len(face), "degenerate oriented simplex")
    inversions = sum(face[i] > face[j] for i in range(len(face))
                     for j in range(i + 1, len(face)))
    chain[tuple(sorted(face))] += coefficient * (-1) ** inversions


def obstruction(K, m):
    S = {v for v, k in enumerate(m) if k > 1}
    chain = Counter()
    for v in sorted(S):
        cycle = cycle_from_edges({f for f in link(K, v) if len(f) == 2})
        if cycle:
            for x, y in zip(cycle, cycle[1:] + cycle[:1]):
                for c in (0, 1):
                    oriented_add(chain, ((v, c), (x, 0), (y, 0)), (-1) ** c)
            return "link_cycle", dict(chain)
    triples = sorted(f for f in K if len(f) == 3)
    pairs = None
    kind = None
    for u, v in sorted(f for f in K if len(f) == 2 and set(f) <= S):
        common = [next(x for x in t if x not in (u, v)) for t in triples
                  if u in t and v in t]
        if len(common) > 1:
            pairs = (((u, 0), (u, 1)), ((v, 0), (v, 1)),
                     ((common[0], 0), (common[1], 0)))
            kind = "duplicated_edge"
            break
    if pairs is None:
        for t in triples:
            if set(t) <= S:
                pairs = tuple(((v, 0), (v, 1)) for v in t)
                kind = "duplicated_triangle"
                break
    require(pairs is not None, "no obstruction")
    for colors in product(range(2), repeat=3):
        oriented_add(chain, tuple(pairs[i][colors[i]] for i in range(3)),
                     (-1) ** sum(colors))
    return kind, dict(chain)


def check_sphere(I, chain):
    require(chain and all(abs(c) == 1 for c in chain.values()), "bad coefficients")
    require(all(len(f) == 3 and f in I for f in chain), "nonface in sphere")
    boundary = Counter()
    deflated = Counter()
    for t, c in chain.items():
        for j in range(3):
            boundary[t[:j] + t[j + 1:]] += (-1) ** j * c
        oriented_add(deflated, tuple(v for v, _ in t), c)
    require(all(c == 0 for c in boundary.values()), "nonzero integral boundary")
    require(all(c == 0 for c in deflated.values()), "nonzero deflated chain")
    P = closure(chain)
    vertices = {f[0] for f in P if len(f) == 1}
    edges = {f for f in P if len(f) == 2}
    require(len(vertices) - len(edges) + len(chain) == 2, "wrong Euler characteristic")
    for e in edges:
        require(sum(set(e) <= set(t) for t in chain) == 2, "nonmanifold edge")
    for v in vertices:
        L = link(P, v)
        lv = {f[0] for f in L if len(f) == 1}
        le = [f for f in L if len(f) == 2]
        require(all(sum(x in e for e in le) == 2 for x in lv), "bad vertex link")
        reached = {min(lv)}
        while True:
            expanded = reached | {x for e in le if reached & set(e) for x in e}
            if expanded == reached:
                break
            reached = expanded
        require(reached == lv, "disconnected vertex link")
    reached = {min(vertices)}
    while True:
        expanded = reached | {x for e in edges if reached & set(e) for x in e}
        if expanded == reached:
            break
        reached = expanded
    require(reached == vertices, "disconnected sphere")


def b2_mod2(K):
    """Definition-level boundary rank, no links or collapse machinery."""
    rows = {e: i for i, e in enumerate(sorted(f for f in K if len(f) == 2))}
    pivots = {}
    columns = 0
    for t in sorted(f for f in K if len(f) == 3):
        columns += 1
        column = sum(1 << rows[e] for e in combinations(t, 2))
        while column:
            pivot = column.bit_length() - 1
            if pivot in pivots:
                column ^= pivots[pivot]
            else:
                pivots[pivot] = column
                break
    return columns - len(pivots)


def base_complexes(n, full_skeleton=False):
    edges = list(combinations(range(n), 2))
    masks = [2 ** len(edges) - 1] if full_skeleton else range(2 ** len(edges))
    for mask in masks:
        chosen = {e for i, e in enumerate(edges) if mask >> i & 1}
        allowed = [t for t in combinations(range(n), 3)
                   if all(e in chosen for e in combinations(t, 2))]
        skeleton = chosen | {(v,) for v in range(n)}
        for tm in range(2 ** len(allowed)):
            yield skeleton | {t for i, t in enumerate(allowed) if tm >> i & 1}


def subcomplexes(I):
    """Enumerate every subcomplex, including missing/isolated vertices."""
    faces = sorted(I, key=lambda f: (len(f), f))

    def visit(index, chosen):
        if index == len(faces):
            yield set(chosen)
            return
        f = faces[index]
        yield from visit(index + 1, chosen)
        if len(f) == 1 or all(e in chosen for e in combinations(f, len(f) - 1)):
            chosen.add(f)
            yield from visit(index + 1, chosen)
            chosen.remove(f)

    yield from visit(0, set())


def rejected(call):
    try:
        call()
    except ValueError:
        return
    raise ValueError("negative control was accepted")


def run():
    stats = Counter()
    digest = hashlib.sha256()
    base_counts = {}
    for n in range(1, 6):
        count = 0
        for K in base_complexes(n, full_skeleton=(n == 5)):
            count += 1
            base_b2 = b2_mod2(K)
            for m in product(range(1, 3 if n == 5 else 4), repeat=n):
                validate(K, m)
                good = all(conditions(K, m))
                I = inflate(K, m)
                K0 = original(K)
                difference = b2_mod2(I) - base_b2
                require((difference == 0) == good, "boundary-rank disagreement")
                if good:
                    cert = collapse_certificate(I, m)
                    replay(I, K0, cert)
                    stats["admissible"] += 1
                    stats["collapse_pairs"] += len(cert)
                    record = cert
                    tag = "collapse"
                else:
                    tag, chain = obstruction(K, m)
                    check_sphere(I, chain)
                    stats[tag] += 1
                    record = sorted(chain.items())
                stats["cases"] += 1
                digest.update(json.dumps([n, sorted(K), m, tag, record],
                                         separators=(",", ":")).encode() + b"\n")
        base_counts[str(n)] = count

    independent_failures = [
        (closure([(0, 1, 2), (0, 2, 3), (0, 1, 3)]), (2, 1, 1, 1),
         (False, True, True)),
        (closure([(0, 1, 2), (0, 1, 3)]), (2, 2, 1, 1),
         (True, False, True)),
        (closure([(0, 1, 2)]), (2, 2, 2), (True, True, False)),
    ]
    for K, m, expected in independent_failures:
        require(conditions(K, m) == expected, "conditions not independent")
        _, chain = obstruction(K, m)
        check_sphere(inflate(K, m), chain)
        require(b2_mod2(K) == 0, "control base has H2")

    # A nontrivial base H2 is allowed when no copies are added. Conversely,
    # a duplicated torus vertex has an explicit spherical obstruction.
    torus = closure([tuple(sorted((i, (i + a) % 7, (i + 3) % 7)))
                     for i in range(7) for a in (1, 2)])
    require(len([f for f in torus if len(f) == 3]) == 14, "torus fixture")
    require(b2_mod2(torus) == 1, "torus boundary rank")
    require(all(conditions(torus, (1,) * 7)), "identity rejected")
    _, torus_chain = obstruction(torus, (2, 1, 1, 1, 1, 1, 1))
    check_sphere(inflate(torus, (2, 1, 1, 1, 1, 1, 1)), torus_chain)

    # Restriction of the ambient sequence is checked on EVERY subcomplex
    # of these two admissible inflated disks, not just induced subcomplexes.
    restriction_counts = []
    fixtures = [(closure([(0, 1, 2)]), (3, 1, 1)),
                (closure([(0, 1, 2), (0, 1, 3)]), (2, 1, 1, 1))]
    for K, m in fixtures:
        require(all(conditions(K, m)), "bad restriction fixture")
        I, K0 = inflate(K, m), original(K)
        cert = collapse_certificate(I, m)
        number = 0
        for Y in subcomplexes(I):
            R = replay(Y, K0, cert, restricted=True)
            require(b2_mod2(R) == b2_mod2(Y), "restricted homology changed")
            number += 1
        restriction_counts.append(number)

    K, m = fixtures[0]
    I, K0 = inflate(K, m), original(K)
    cert = collapse_certificate(I, m)
    bad = list(cert)
    t, _ = bad[0]
    bad[0] = (t, tuple(sorted(((1, 0), (2, 0)))))
    rejected(lambda: replay(I, K0, bad))
    rejected(lambda: replay(I, K0, cert[:-1]))
    rejected(lambda: validate(K - {(0, 1)}, m))
    rejected(lambda: validate(K, (0, 1, 1)))
    rejected(lambda: validate(closure([(0, 1, 2, 3)]), (1, 1, 1, 1)))
    K, m, _ = independent_failures[2]
    I = inflate(K, m)
    _, chain = obstruction(K, m)
    bad_chain = dict(chain)
    del bad_chain[min(bad_chain)]
    rejected(lambda: check_sphere(I, bad_chain))
    bad_chain = dict(chain)
    bad_chain[min(bad_chain)] *= -1
    rejected(lambda: check_sphere(I, bad_chain))
    rejected(lambda: collapse_certificate(I, m))
    require(inflate(set(), ()) == set(), "empty complex")
    replay(set(), set(), [])

    return {
        "status": "VERIFIED",
        "scope": "finite validation, not a decision procedure for base asphericity",
        "base_complex_counts": base_counts,
        "enumeration": "all complexes on 1..4 labelled vertices, m in {1,2,3}; "
                       "all 2-complexes on 5 vertices with complete 1-skeleton, m in {1,2}",
        "counts": dict(sorted(stats.items())),
        "entrywise_certificate_sha256": digest.hexdigest(),
        "independent_condition_failures": 3,
        "all_subcomplex_restriction_counts": restriction_counts,
        "negative_controls": 8,
        "additional_controls": ["torus identity", "torus clone", "empty complex"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print evidence without expected comparison")
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["evidence_sha256"] = hashlib.sha256(payload).hexdigest()
    if not args.emit:
        expected = json.loads(Path(__file__).with_name("expected.json").read_text())
        require(result == expected, "evidence differs from expected.json")
    print(json.dumps(result, indent=2, sort_keys=True))

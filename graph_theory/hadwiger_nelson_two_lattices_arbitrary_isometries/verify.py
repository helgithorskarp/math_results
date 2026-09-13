#!/usr/bin/env python3
"""Exact finite checks accompanying the unbounded two-lattice proof.

Python 3.11+, standard library. This program reads no external graph and
uses no solver. The unbounded proof is in PROOF.md.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def norm(z):
    a, b = z
    return a*a + a*b + b*b


def sub(z, w):
    return tuple(a-b for a, b in zip(z, w))


def rotate(z):
    a, b = z
    return -b, a+b


def geometric_lemma():
    # PROOF.md proves this box contains every norm <= 4 lattice vector.
    vectors = {(a, b) for a in range(-4, 5) for b in range(-2, 3)
               if 0 < norm((a, b)) <= 4}
    representatives = [(1, 0), (1, 1), (2, 0)]
    centres = [[(0, 1), (1, -1)], [(1, 0), (0, 1)], [(1, 0)]]
    covered = set()
    for d, xs in zip(representatives, centres):
        for _ in range(6):
            require(d not in covered, "duplicate norm-orbit entry")
            covered.add(d)
            require(len(set(xs)) == len(xs), "duplicate circle intersection")
            for x in xs:
                require(norm(x) == norm(sub(x, d)) == 1,
                        "incorrect unit-circle intersection")
            require(len(xs) == (1 if norm(d) == 4 else 2),
                    "incorrect intersection multiplicity")
            d = rotate(d)
            xs = [rotate(x) for x in xs]
    require(covered == vectors, "incomplete small-norm classification")
    return {str(k): sum(norm(z) == k for z in vectors) for k in range(1, 5)}


def palette(left, right, cross):
    """Lemma 3; labels in cross are local to the two disjoint parts."""
    require(all(c in (0, 1, 2) for c in left+right), "invalid input class")
    require(len(set(cross)) == len(cross), "repeated cross edge")
    la, rb = {}, {}
    for a, b in cross:
        require(0 <= a < len(left) and 0 <= b < len(right), "bad endpoint")
        require(a not in la and b not in rb, "cross edges are not a matching")
        la[a], rb[b] = b, a
    ca = [None if r == 0 else r for r in left]
    cb = [None if r == 0 else r+2 for r in right]
    # Only fixed neighbour colours matter; flexible palettes are disjoint.
    for a, r in enumerate(left):
        if r == 0:
            forbidden = cb[la[a]] if a in la and right[la[a]] != 0 else None
            ca[a] = next(c for c in (3, 4) if c != forbidden)
    for b, r in enumerate(right):
        if r == 0:
            forbidden = ca[rb[b]] if b in rb and left[rb[b]] != 0 else None
            cb[b] = next(c for c in (1, 2) if c != forbidden)
    return ca+cb


def check_word(word, n, edges, k):
    require(len(word) == n, "colour-word length")
    require(all(isinstance(c, int) and 1 <= c <= k for c in word), "colour range")
    require(all(word[a] != word[b] for a, b in edges), "monochromatic edge")


def matchings(n):
    def visit(a, available, current):
        if a == n:
            yield tuple(current)
            return
        yield from visit(a+1, available, current)
        for b in sorted(available):
            yield from visit(a+1, available-{b}, current+[(a, b)])
    yield from visit(0, set(range(n)), [])


def palette_checks():
    classes = [0, 0, 1, 1, 2, 2]
    internal = [(a, b) for a, b in combinations(range(6), 2)
                if classes[a] != classes[b]]
    edges = internal+[(a+6, b+6) for a, b in internal]
    total = 0
    digest = sha256()
    for cross in matchings(6):
        word = palette(classes, classes, list(cross))
        check_word(word, 12, edges+[(a, b+6) for a, b in cross], 4)
        digest.update(bytes(word))
        total += 1
    return {"partial_matchings": total, "colour_stream_sha256": digest.hexdigest()}


def contact_checks():
    result = {"three_colourable_relations": 0, "obstructing_relations": 0}
    for mask in range(512):
        es = {(i, j) for i in range(3) for j in range(3) if mask & (1 << (3*i+j))}
        possible = any(all(i != p[j] for i, j in es) for p in permutations(range(3)))
        star = any(all((i, j) in es for j in range(3)) for i in range(3))
        star |= any(all((i, j) in es for i in range(3)) for j in range(3))
        square = any(all((i, j) in es for i in aa for j in bb)
                     for aa in combinations(range(3), 2)
                     for bb in combinations(range(3), 2))
        require(possible == (not (star or square)), "Hall characterization")
        result["three_colourable_relations" if possible else "obstructing_relations"] += 1
    return result


def coordinates(layer, a, b):
    """(x0,x1,y0,y1) means (x0+x1 sqrt33, y0 sqrt3+y1 sqrt11)."""
    if layer == 0:
        return F(a)+F(b, 2), F(0), F(b, 2), F(0)
    r, s = F(a)+F(b, 2)+F(1, 2), F(b, 2)+F(1, 6)
    return 5*r/6, -s/6, 5*s/6, r/6


def cartesian_norm(z):
    a, b, c, d = z
    return a*a+33*b*b+3*c*c+11*d*d, 2*a*b+2*c*d


def tensor_product(x, y):
    # Independent complex basis 1,u,v,uv, with u^2=-3 and v^2=-11.
    out = [F(0)]*4
    for i in range(4):
        for j in range(4):
            common = i & j
            factor = (-3 if common & 1 else 1)*(-11 if common & 2 else 1)
            out[i ^ j] += x[i]*y[j]*factor
    return out


def tensor_norm(z):
    a, b, c, d = z
    value = tensor_product([a, c, d, -b], [a, -c, -d, -b])
    require(value[1] == value[2] == 0, "nonreal norm")
    return value[0], -value[3]


def propagate(n, edges, residues):
    edge = {tuple(sorted(e)) for e in edges}
    tri = next(t for t in combinations(range(n), 3)
               if all(e in edge for e in combinations(t, 2)))
    known = {v: residues[v] for v in tri}
    steps = []
    while len(known) < n:
        step = next(((v, a, b) for v in range(n) if v not in known
                     for a, b in combinations(sorted(known), 2)
                     if all(tuple(sorted(e)) in edge for e in [(a,b),(a,v),(b,v)])), None)
        require(step is not None, "triangle propagation stuck")
        v, a, b = step
        require(known[a] != known[b], "invalid triangle colours")
        colour, = set(range(3))-{known[a], known[b]}
        require(colour == residues[v], "propagated residue mismatch")
        known[v] = colour
        steps.append(list(step))
    return {"anchor": list(tri), "forced_steps": steps}


def count_three(n, edges):
    # Literal complete backtracking in vertex order, with no symmetry pins.
    prior = [[] for _ in range(n)]
    for a, b in edges:
        prior[max(a, b)].append(min(a, b))
    word = [-1]*n
    def visit(v):
        if v == n:
            return 1
        forbidden = {word[u] for u in prior[v]}
        count = 0
        for c in range(3):
            if c not in forbidden:
                word[v] = c
                count += visit(v+1)
        word[v] = -1
        return count
    return visit(0)


def has_spindle(n, edges):
    adjacency = [set() for _ in range(n)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    # Two K4-e arms sharing only an apex, with a unit edge between the tips.
    for apex in range(n):
        arms = []
        for tip in range(n):
            if tip == apex:
                continue
            for a, b in combinations(sorted(adjacency[apex] & adjacency[tip]), 2):
                if b in adjacency[a]:
                    arms.append((tip, {tip, a, b}))
        for (t, a), (s, b) in combinations(arms, 2):
            if not a & b and s in adjacency[t]:
                return True
    return False


def witness():
    aa = [(a, b) for a in range(-1, 3) for b in range(-1, 3) if a+b <= 1]
    bb = [(a, b) for a in range(-1, 2) for b in range(-1, 2) if a+b <= 0]
    points = [coordinates(0, a, b) for a, b in aa]+[coordinates(1, a, b) for a, b in bb]
    require(len(points) == len(set(points)) == 16, "distinct point count")
    edges = []
    for i, j in combinations(range(16), 2):
        delta = sub(points[i], points[j])
        q = cartesian_norm(delta)
        require(q == tensor_norm(delta), "two exact norm routes disagree")
        require(q != (0, 0), "coinciding physical points")
        if q == (1, 0):
            edges.append((i, j))
    ea = [(i, j) for i, j in edges if j < 10]
    eb = [(i-10, j-10) for i, j in edges if i >= 10]
    cross = [(i, j-10) for i, j in edges if i < 10 <= j]
    require((len(ea), len(eb), len(cross)) == (18, 9, 3), "strict edge counts")
    ra, rb = [[(a-b) % 3 for a, b in p] for p in (aa, bb)]
    relation = sorted({(ra[i], rb[j]) for i, j in cross})
    require(relation == [(0,0), (0,1), (0,2)], "wrong sharpness contact star")
    pa, pb = propagate(10, ea, ra), propagate(6, eb, rb)
    ca, cb, cg = count_three(10, ea), count_three(6, eb), count_three(16, edges)
    require((ca, cb, cg) == (6, 6, 0), "three-colouring counts")
    word = palette(ra, rb, cross)
    check_word(word, 16, edges, 4)
    require(not has_spindle(16, edges), "unexpected Moser spindle")
    encoded = ''.join(f'{a} {b}\n' for a, b in edges).encode()
    return {"vertices": 16, "edges": 30, "exact_pair_checks": 120,
            "edge_sha256": sha256(encoded).hexdigest(),
            "cross_edges_in_local_labels": cross,
            "contact_residue_pairs": relation,
            "three_colourings_of_parts": [ca, cb], "three_colourings_of_union": cg,
            "four_colour_word": ''.join(map(str, word)), "moser_spindle_free": True,
            "triangle_propagation": [pa, pb]}


def rejection_controls():
    bad = [lambda: palette([0, 1], [0, 1], [(0,0),(0,1)]),
           lambda: palette([0, 1], [0, 1], [(0,0),(1,0)]),
           lambda: palette([3], [0], []),
           lambda: palette([0], [0], [(1,0)]),
           lambda: palette([0], [0], [(0,0),(0,0)]),
           lambda: check_word([1,1], 2, [(0,1)], 4),
           lambda: check_word([1], 2, [(0,1)], 4),
           lambda: check_word([1,5], 2, [(0,1)], 4)]
    rejected = 0
    for operation in bad:
        try:
            operation()
        except ValueError:
            rejected += 1
        else:
            raise ValueError("malformed-input control was accepted")
    # Positive control for the spindle detector, in its seven-vertex labels.
    spindle = [(0,1),(0,2),(1,2),(1,3),(2,3),
               (0,4),(0,5),(4,5),(4,6),(5,6),(3,6)]
    require(has_spindle(7, spindle), "spindle positive control failed")
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-expected', action='store_true')
    args = parser.parse_args()
    result = {"status": "PASS", "small_norm_orbit_counts": geometric_lemma(),
              "palette_check": palette_checks(), "contact_criterion": contact_checks(),
              "sharpness_witness": witness(), "malformed_inputs_rejected": rejection_controls()}
    # Normalize tuples to the JSON data model before comparing expected output.
    result = json.loads(json.dumps(result))
    if args.check_expected:
        expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
        require(result == expected, "expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

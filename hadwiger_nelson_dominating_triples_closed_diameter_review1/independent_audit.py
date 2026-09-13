#!/usr/bin/env python3
"""Independent exact audit of the closed diameter-three theorem.

This checker does not import the target programs or read their certificate.
It reconstructs the equality graph, tests the proof's normalized interface
cases, and derives the sharp Moser-spindle witness from its formulas.
"""

import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET_HASHES = {
    "PROOF.md": "0fac3929905904af84fce27a8b797ab5e050e96f9ef3434be330ad126f04acd9",
    "certificate.json": "150024ff330da42d030dfb41b931bad7bc2d612c269140c1f6f6fa88f7a103c1",
    "verify.py": "7ec923d7ea76be56406e4ecf7ceb98c05294606fbc5aeccd1a9bd60dc58c9dd0",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def proper_words(n, edges, colours):
    return [
        word
        for word in product(range(colours), repeat=n)
        if all(word[a] != word[b] for a, b in edges)
    ]


class ParityDSU:
    """Union-find for equations colour(x) xor colour(y) = parity."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.xor_to_parent = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            parent, parity = self.find(self.parent[x])
            self.xor_to_parent[x] ^= parity
            self.parent[x] = parent
        return self.parent[x], self.xor_to_parent[x]

    def add(self, x, y, parity):
        rx, px = self.find(x)
        ry, py = self.find(y)
        if rx == ry:
            return (px ^ py) == parity
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
            px, py = py, px
        self.parent[ry] = rx
        self.xor_to_parent[ry] = px ^ py ^ parity
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def boundary_audit():
    # (s,t) denotes (s/2, t*sqrt(3)/2). Squared distances have numerator
    # ds^2 + 3 dt^2 over 4, so all unit predicates are integer exact.
    roots = [(2, 0), (1, 1), (-1, 1), (-2, 0), (-1, -1), (1, -1)]
    points = roots + [(s + 6, t) for s, t in roots]

    def unit(p, q):
        return (p[0] - q[0]) ** 2 + 3 * (p[1] - q[1]) ** 2 == 4

    edges = [e for e in combinations(range(12), 2) if unit(points[e[0]], points[e[1]])]
    cross = [e for e in edges if e[0] < 6 <= e[1]]
    require(len(edges) == 13, "boundary edge count")
    require(cross == [(0, 9)], "the equality support must have one cross edge")

    dsu = ParityDSU(12)
    require(all(dsu.add(a, b, 1) for a, b in edges), "boundary graph is not bipartite")
    roots_seen = {dsu.find(v)[0] for v in range(12)}
    require(len(roots_seen) == 1, "boundary graph should be connected")
    words = proper_words(12, edges, 2)
    require(len(words) == 2, "connected boundary graph should have two bipartitions")

    # If the third centre is one unit from a leaf centre, it is an anchor on
    # that leaf C6 and the two circle intersections are its neighbours.
    unit_anchor_cases = 0
    for leaf in range(2):
        for anchor in range(6):
            v = 6 * leaf + anchor
            left = 6 * leaf + (anchor - 1) % 6
            right = 6 * leaf + (anchor + 1) % 6
            feasible = [w for w in words if w[v] == 0]
            require(feasible and all(w[left] == w[right] == 1 for w in feasible), "unit anchor")
            unit_anchor_cases += 1

    # One exceptional Mi is an edge on one leaf. The optional unit anchor is
    # on the other leaf. For every relative placement, a proper phase with
    # the anchor at 0 has exactly one usable (colour-1) exceptional endpoint.
    one_exception_cases = 0
    one_exception_phase_rows = 0
    for leaf in range(2):
        for base in range(6):
            exc_edge = (6 * leaf + base, 6 * leaf + (base + 1) % 6)
            for other_anchor in [-1] + list(range(6)):
                feasible = words
                if other_anchor >= 0:
                    anchor = 6 * (1 - leaf) + other_anchor
                    feasible = [w for w in words if w[anchor] == 0]
                require(feasible, "one-exception phase does not extend")
                require(
                    all(sum(w[x] == 1 for x in exc_edge) == 1 for w in feasible),
                    "exceptional edge lacks a unique leaf endpoint",
                )
                one_exception_cases += 1
                one_exception_phase_rows += len(feasible)

    # With two exceptions the proof may start from either global phase; every
    # exceptional edge supplies one leaf-colour-1 endpoint in that phase.
    two_exception_cases = 0
    two_exception_phase_rows = 0
    for base0 in range(6):
        edge0 = (base0, (base0 + 1) % 6)
        for base1 in range(6):
            edge1 = (6 + base1, 6 + (base1 + 1) % 6)
            require(
                all(
                    sum(w[x] == 1 for x in edge0) == 1
                    and sum(w[x] == 1 for x in edge1) == 1
                    for w in words
                ),
                "two-exception endpoint selection",
            )
            two_exception_cases += 1
            two_exception_phase_rows += len(words)

    # A same-colour prescription is compatible precisely at an even step.
    # Intersections of two unit circles at centre separation d obey
    # chord^2 = 4-d^2. The only positive d^2 from an odd step is 3.
    chord_squared = [0, 1, 3, 4, 3, 1]
    exceptional_d2 = sorted(
        {4 - chord_squared[step] for step in range(6) if step % 2 and 4 - chord_squared[step] > 0}
    )
    require(exceptional_d2 == [3], "unexpected positive exceptional separation")

    # Semantic parity controls: even-separated points may be prescribed alike;
    # adjacent (exceptional) points may not.
    even = ParityDSU(3)
    require(even.add(0, 1, 1) and even.add(1, 2, 1) and even.add(0, 2, 0), "even control")
    odd = ParityDSU(2)
    require(odd.add(0, 1, 1) and not odd.add(0, 1, 0), "odd control")

    # The source proof's zero-exception rule needs this harmless empty-set
    # convention when the centrally assigned Mi is empty.
    def opposite_common_or_free(values):
        if not values:
            return 0
        require(len(set(values)) == 1, "expected a common central colour")
        return 1 - values[0]

    require([opposite_common_or_free(v) for v in ([], [0], [1, 1])] == [0, 1, 0], "empty repair")

    # Negative control: a same-parity chord in a C6 creates an odd cycle.
    bad = ParityDSU(12)
    require(not all(bad.add(a, b, 1) for a, b in edges + [(0, 2)]), "odd-cycle control missed")

    return {
        "boundary_vertices": 12,
        "boundary_pair_distances": 66,
        "boundary_edges": len(edges),
        "boundary_cross_edges": len(cross),
        "boundary_components": len(roots_seen),
        "boundary_binary_words_checked": 2 ** 12,
        "boundary_bipartitions": len(words),
        "unit_anchor_cases": unit_anchor_cases,
        "one_exception_cases": one_exception_cases,
        "one_exception_phase_rows": one_exception_phase_rows,
        "two_exception_cases": two_exception_cases,
        "two_exception_phase_rows": two_exception_phase_rows,
        "orbit_chord_steps": len(chord_squared),
        "positive_exceptional_squared_separations": exceptional_d2,
        "empty_intersection_rule_repairs": 1,
        "parity_semantic_controls": 3,
    }


# A field element is a 4-tuple in the basis 1,sqrt(3),sqrt(11),sqrt(33).
RADICANDS = (1, 3, 11, 33)
ZERO = (F(0), F(0), F(0), F(0))
ONE = (F(1), F(0), F(0), F(0))


def r(value):
    return (F(value), F(0), F(0), F(0))


def qadd(x, y):
    return tuple(a + b for a, b in zip(x, y))


def qneg(x):
    return tuple(-a for a in x)


def qmul(x, y):
    out = [F(0)] * 4
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            common = i & j
            out[i ^ j] += a * b * RADICANDS[common]
    return tuple(out)


def cadd(z, w):
    return qadd(z[0], w[0]), qadd(z[1], w[1])


def cmul(z, w):
    return qadd(qmul(z[0], w[0]), qneg(qmul(z[1], w[1]))), qadd(
        qmul(z[0], w[1]), qmul(z[1], w[0])
    )


def csqdist(z, w):
    dx = qadd(z[0], qneg(w[0]))
    dy = qadd(z[1], qneg(w[1]))
    return qadd(qmul(dx, dx), qmul(dy, dy))


def k_colourable(n, edges, k):
    neighbours = [set() for _ in range(n)]
    for a, b in edges:
        neighbours[a].add(b)
        neighbours[b].add(a)
    colour = [-1] * n

    def visit(done):
        if done == n:
            return tuple(colour)
        uncoloured = [v for v in range(n) if colour[v] < 0]
        v = max(uncoloured, key=lambda x: (len({colour[y] for y in neighbours[x] if colour[y] >= 0}), len(neighbours[x])))
        forbidden = {colour[y] for y in neighbours[v] if colour[y] >= 0}
        for c in range(k):
            if c not in forbidden:
                colour[v] = c
                answer = visit(done + 1)
                if answer is not None:
                    return answer
                colour[v] = -1
        return None

    return visit(0)


def sharpness_audit():
    sqrt3 = (F(0), F(1), F(0), F(0))
    sqrt11 = (F(0), F(0), F(1), F(0))
    z0 = (ZERO, ZERO)
    u = (ONE, ZERO)
    v = (tuple(a / 2 for a in ONE), tuple(a / 2 for a in sqrt3))
    b = cadd(u, v)
    rho = (tuple(a / 6 for a in tuple(5 * t for t in ONE)), tuple(a / 6 for a in sqrt11))
    vertices = [z0, u, v, b, cmul(rho, u), cmul(rho, v), cmul(rho, b)]
    require(len(set(vertices)) == 7, "spindle vertices collide")
    distances = {e: csqdist(vertices[e[0]], vertices[e[1]]) for e in combinations(range(7), 2)}
    edges = [e for e, d2 in distances.items() if d2 == ONE]
    require(len(edges) == 11, "spindle edge count")

    colouring3 = k_colourable(7, edges, 3)
    colouring4 = k_colourable(7, edges, 4)
    require(colouring3 is None and colouring4 is not None, "spindle chromatic number")

    third = (r(3), ZERO)
    centres = [z0, third, b]
    require(csqdist(z0, third) == r(9), "equality pair is not distance three")
    require(len(set(centres)) == 3, "centres collide")
    support_members = 0
    for point in vertices:
        if point in centres or any(csqdist(point, c) == ONE for c in centres):
            support_members += 1
    require(support_members == 7, "spindle not contained in support")

    # Edge-criticality catches any silently omitted spindle edge: deletion of
    # each exact edge restores a three-colouring.
    edge_deletion_controls = 0
    for omitted in edges:
        require(k_colourable(7, [e for e in edges if e != omitted], 3) is not None, "edge deletion control")
        edge_deletion_controls += 1

    return {
        "sharpness_vertices": len(vertices),
        "sharpness_pair_distances": len(distances),
        "sharpness_edges": len(edges),
        "sharpness_support_members": support_members,
        "sharpness_chromatic_number": 4,
        "sharpness_edge_deletion_controls": edge_deletion_controls,
    }


def source_audit(target_dir):
    observed = {}
    for name, expected in TARGET_HASHES.items():
        path = target_dir / name
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected, f"target source mismatch: {name}")
        observed[name] = digest
    return {"target_files_hashed": len(observed), "target_sha256": observed}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=HERE.parent / "hadwiger_nelson_dominating_triples_closed_diameter",
    )
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    result = {"status": "PASS", **boundary_audit(), **sharpness_audit(), **source_audit(args.target_dir)}
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        require(result == expected, "result differs from EXPECTED.json")
    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(raw)
    print(raw, end="")


if __name__ == "__main__":
    main()

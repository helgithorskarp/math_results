"""Exact small geometry and hypothesis controls in a multiquadratic field."""
from fractions import Fraction as Q
from itertools import combinations, permutations
from hashlib import sha256
import json

# The basis monomial indexed by a mask is the product of its selected roots.
# Distinct square classes give a basis of Q(i,sqrt(3),sqrt(5),sqrt(11),sqrt(13)).
RAD = (-1, 3, 5, 11, 13)
E_BASIS = {0, 2 | 8, 1 | 2, 1 | 8}


def require(ok, message):
    if not ok:
        raise ValueError(message)


class A:
    def __init__(self, terms=0):
        if isinstance(terms, A):
            terms = terms.terms
        if not isinstance(terms, dict):
            terms = {0: Q(terms)}
        self.terms = {m: Q(c) for m, c in terms.items() if c}

    def __add__(self, other):
        out = self.terms.copy()
        for m, c in A(other).terms.items():
            out[m] = out.get(m, 0)+c
        return A(out)

    __radd__ = __add__

    def __neg__(self):
        return A({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + -A(other)

    def __rsub__(self, other):
        return A(other) + -self

    def __mul__(self, other):
        out = {}
        for m, c in self.terms.items():
            for n, d in A(other).terms.items():
                factor = 1
                for k, p in enumerate(RAD):
                    if (m & n) & (1 << k):
                        factor *= p
                out[m ^ n] = out.get(m ^ n, 0)+c*d*factor
        return A(out)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == A(other).terms

    def __hash__(self):
        return hash(tuple(sorted(self.terms.items())))

    def bar(self):
        return A({m: (-c if m & 1 else c) for m, c in self.terms.items()})

    def norm(self):
        return self*self.bar()

    def in_E(self):
        return set(self.terms) <= E_BASIS


def six_cycles(P, Z, cross, distinct=True):
    cross = set(cross)
    cycles = set()
    for fixed in combinations(range(len(P)), 3):
        for moving in combinations(range(len(Z)), 3):
            if distinct and len({P[i] for i in fixed} | {Z[j] for j in moving}) != 6:
                continue
            for perm in permutations(moving):
                edges = tuple(sorted((fixed[i], perm[j])
                                     for i in range(3) for j in range(3) if i != j))
                if all(e in cross for e in edges):
                    cycles.add(edges)
    return sorted(cycles)


def colour(n, edges):
    neighbours = [set() for _ in range(n)]
    for i, j in edges:
        neighbours[i].add(j)
        neighbours[j].add(i)
    colours = [-1]*n

    def extend(i):
        if i == n:
            return True
        banned = {colours[j] for j in neighbours[i]}
        for c in range(4):
            if c not in banned:
                colours[i] = c
                if extend(i+1):
                    return True
        colours[i] = -1
        return False

    require(extend(0), "small example has no four-colouring")
    require(all(colours[i] != colours[j] for i, j in edges), "improper colouring")
    return colours


def case(name, P, Qs, u, h, expected_cross, expected_cycles, reverse=False):
    require(u.norm() == 1, "isometry multiplier is not unit")
    require(all(p.in_E() for p in P+Qs), "source point outside E")
    Z = [h+u*(q.bar() if reverse else q) for q in Qs]
    cross = [(i, j) for i, p in enumerate(P) for j, z in enumerate(Z)
             if (p-z).norm() == 1]
    cycles = six_cycles(P, Z, cross)
    require(len(cross) == expected_cross, "unexpected cross edges: "+name)
    require(len(cycles) == expected_cycles, "unexpected six-cycles: "+name)
    preserves = u.in_E() and h.in_E()
    require(not cycles or preserves, "counterexample to the claimed theorem")
    points = list(dict.fromkeys(P+Z))
    edges = [(i, j) for i in range(len(points)) for j in range(i+1, len(points))
             if (points[i]-points[j]).norm() == 1]
    colours = colour(len(points), edges)
    return {"case": name, "source_sizes": [len(P), len(Qs)],
            "vertices": len(points), "pairs_checked": len(points)*(len(points)-1)//2,
            "strict_edges": len(edges), "cross_edges": cross,
            "physical_cross_six_cycles": len(cycles),
            "labelled_cross_six_cycles": len(six_cycles(P, Z, cross, False)),
            "field_preserving": preserves, "orientation_reversing": reverse,
            "colours": colours, "proper_four_colouring": True,
            "edge_sha256": sha256(''.join(f'{i},{j}\n' for i, j in edges).encode()).hexdigest()}


def main():
    alpha = A({3: 1})
    iroot5 = A({5: 1})
    root5, root13 = A({4: 1}), A({16: 1})
    omega, eta = (-1+alpha)*Q(1, 2), (1+alpha)*Q(1, 2)
    triangle = [A(1), omega, omega*omega]
    line = list(map(A, (Q(3, 7), Q(5, 7), Q(-8, 7))))
    zero_line = list(map(A, (-1, 0, 1)))
    u = (1-2*alpha)*root13*Q(1, 13)
    v = (2+iroot5)*Q(1, 3)
    require(v*v-Q(4, 3)*v+1 == 0 and not v.in_E(), "quadratic rotation control")
    rows = [
        case("regular_hexagon", triangle, triangle, eta, A(), 6, 1),
        case("connected_hexagonal_wheel", [A()]+triangle, [A()]+triangle,
             eta, A(), 12, 7),
        case("collinear_six_cycle", line, line, omega, A(), 6, 1),
        case("reflected_hexagon", triangle, triangle, eta, A(), 6, 1, True),
        case("external_translation_path", list(map(A, (0, Q(1, 2), 1))),
             list(map(A, (Q(-1, 4), Q(1, 4), Q(3, 4)))),
             A(1), alpha*root5*Q(1, 4), 5, 0),
        case("quadratic_rotation_path_through_centre",
             list(map(A, (0, Q(4, 3), Q(-8, 27)))),
             list(map(A, (1, Q(7, 9), Q(-95, 81)))), v, A(), 5, 0),
        case("external_rotation_four_cycle", [alpha*Q(1, 4), -alpha*Q(1, 4)],
             [(1+2*alpha)*Q(1, 4), -(1+2*alpha)*Q(1, 4)], u, A(), 4, 0),
        case("folded_labelled_cycle", zero_line, zero_line, omega, A(), 6, 0)
    ]
    require(rows[-1]['labelled_cross_six_cycles'] == 1 and rows[-1]['vertices'] == 5,
            "six-distinct-point rejection was not exercised")
    # Coincident midpoint pairs do not satisfy the shared-vertex lemma.
    z1, z2 = alpha*root5*Q(1, 4), root13*Q(1, 4)
    require(all((z1-p).norm() == 1 for p in (A(Q(1, 4)), A(Q(-1, 4)))),
            "first circle intersection control")
    require(all((z2-p).norm() == 1 for p in (alpha*Q(1, 4), -alpha*Q(1, 4))),
            "second circle intersection control")
    require((z1-z2).norm() == Q(7, 4), "centre separation is not rational")
    require(all(not z.in_E() for z in (root5, root13, root5*root13)),
            "quadratic fields were not distinct over E")
    require(all((A()-p).norm() == 1 for p in (A(-1), A(1))), "tangency control")
    require(not set(omega.terms) <= {0, 1}, "missing Q(i) hypothesis control")
    print(json.dumps({"examples": rows, "controls": {
        "coincident_midpoints_allow_distinct_quadratic_fields": True,
        "centre_squared_distance": "7/4", "tangent_centre_in_E": True,
        "Q_i_counterexample_to_dropping_sqrt_minus_three": True,
        "folded_cycle_rejected_as_not_six_distinct_points": True},
        "uniform_theorem_requires_PROOF_md": True}, indent=2))


if __name__ == '__main__':
    main()

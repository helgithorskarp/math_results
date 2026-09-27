#!/usr/bin/env python3
"""Exact algebra and finite controls for PROOF.md; Python 3.11+, stdlib only.

The universal polynomial check supports the completion identity. Rational
jets do not replace the ODE existence argument; the prism grid does not
replace the continuum distance-gain proof. No floats or external inputs.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json


class Poly:
    """Small sparse polynomial ring Q[a11,a12,a21,a22]."""
    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = value.terms.copy()
        elif isinstance(value, dict):
            self.terms = {k: F(v) for k, v in value.items() if v}
        else:
            self.terms = {(0, 0, 0, 0): F(value)} if value else {}

    def __add__(self, other):
        other = Poly(other)
        result = self.terms.copy()
        for k, v in other.terms.items():
            result[k] = result.get(k, F(0)) + v
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.terms.items()})

    def __sub__(self, other):
        return self + (-Poly(other))

    def __rsub__(self, other):
        return Poly(other) + (-self)

    def __mul__(self, other):
        other = Poly(other)
        result = {}
        for k, v in self.terms.items():
            for ell, w in other.terms.items():
                degree = tuple(x + y for x, y in zip(k, ell))
                result[degree] = result.get(degree, F(0)) + v * w
        return Poly(result)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == Poly(other).terms


def eye(n):
    return tuple(tuple(F(i == j) for j in range(n)) for i in range(n))


def tr(a):
    return tuple(zip(*a))


def madd(a, b):
    return tuple(tuple(x + y for x, y in zip(r, s)) for r, s in zip(a, b))


def scale(c, a):
    return tuple(tuple(c * x for x in r) for r in a)


def mm(a, b):
    return tuple(tuple(sum(x * y for x, y in zip(r, c)) for c in tr(b)) for r in a)


def mv(a, v):
    return tuple(sum(x * y for x, y in zip(r, v)) for r in a)


def va(a, b):
    return tuple(x + y for x, y in zip(a, b))


def vs(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm2(a):
    return dot(a, a)


def adj(a):
    return ((a[1][1], -a[0][1]), (-a[1][0], a[0][0]))


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv(a):
    assert det(a) != 0
    return scale(1 / det(a), adj(a))


def diag(a, b):
    return ((a, F(0)), (F(0), b))


def rotation(t):
    c, s = (1 - t*t) / (1 + t*t), 2*t / (1 + t*t)
    return ((c, -s), (s, c))


def polynomial_checks():
    variables = [Poly({tuple(int(i == j) for j in range(4)): 1}) for i in range(4)]
    a = (tuple(variables[:2]), tuple(variables[2:]))
    d = madd(eye(2), scale(-1, mm(tr(a), a)))
    p = madd(eye(2), scale(-1, mm(a, tr(a))))
    assert det(d) == det(p)
    left = madd(scale(det(d), eye(2)), mm(mm(a, adj(d)), tr(a)))
    assert left == adj(p)
    return {"ring": "Q[a11,a12,a21,a22]", "zero_polynomials": 5,
            "identities": ["det(I-A^T A)=det(I-A A^T)",
                           "det(D) I + A adj(D) A^T = adj(P), four entries"]}


def horizontal_jet_checks():
    zero22 = ((F(0), F(0)), (F(0), F(0)))
    choices = [(F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)),
               (F(8, 17), F(15, 17))]
    jets = [(((F(-1, 11), F(2, 9)), (F(1, 8), F(3, 10))), (F(1, 7), F(-2, 11))),
            (((F(2, 13), F(1, 6)), (F(-1, 5), F(1, 9))), (F(-3, 8), F(2, 9)))]
    points = [(F(0), F(0)), (F(1, 2), F(-1, 3)), (F(-2, 5), F(3, 7))]
    frames = jet_points = wrong_inverse = omitted_translation = 0
    xi, eta, hp = (F(2, 3), F(-1, 4)), F(5, 7), F(2, 5)
    for first, second, tu, tq, tw in product(
            choices, choices, (F(0), F(1, 2)), (F(1, 3), F(2, 3)),
            (F(1, 4), F(-1, 2))):
        c1, s1 = first
        c2, s2 = second
        urot, qrot, wrot = rotation(tu), rotation(tq), rotation(tw)
        a = mm(mm(urot, diag(c1, c2)), wrot)
        b = mm(mm(qrot, diag(s1, s2)), wrot)
        v = a + b
        d = madd(eye(2), scale(-1, mm(tr(a), a)))
        p = madd(eye(2), scale(-1, mm(a, tr(a))))
        assert mm(tr(b), b) == d
        assert mm(tr(v), v) == eye(2)
        assert madd(eye(2), mm(mm(a, inv(d)), tr(a))) == inv(p)
        frames += 1
        for ap, bp in jets:
            bprime = scale(-1, mm(mm(inv(tr(b)), tr(a)), ap))
            dprime = mv(scale(-1, mm(inv(tr(b)), tr(a))), bp)
            vp, ep = ap + bprime, bp + dprime
            assert mm(tr(v), vp) == zero22
            assert mv(tr(v), ep) == (0, 0)
            assert madd(mm(tr(bprime), b), mm(tr(b), bprime)) == scale(
                -1, madd(mm(tr(ap), a), mm(tr(a), ap)))
            bad_bprime = scale(-1, mm(mm(inv(b), tr(a)), ap))
            if mm(tr(v), ap + bad_bprime) != zero22:
                wrong_inverse += 1
            if mv(tr(v), bp + (F(0), F(0))) != (0, 0):
                omitted_translation += 1
            for x in points:
                w = va(mv(ap, x), bp)
                eprime = va(mv(vp, x), ep)
                pressure_speed = dot(w, mv(inv(p), w))
                assert mv(tr(v), eprime) == (0, 0)
                assert norm2(eprime) == pressure_speed
                displacement = mv(inv(d), mv(tr(a), w))
                shifted = vs(xi, tuple(eta * y for y in displacement))
                lhs = norm2(xi) + eta*eta - norm2(
                    va(mv(a, xi), tuple(eta * y for y in w))) - hp*hp*eta*eta
                rhs = dot(shifted, mv(d, shifted)) + (1-hp*hp-pressure_speed)*eta*eta
                assert lhs == rhs
                jet_points += 1
    assert wrong_inverse > 0 and omitted_translation > 0
    j = ((F(0), F(-1)), (F(1), F(0)))
    a, b = diag(F(3, 5), F(5, 13)), diag(F(4, 5), F(12, 13))
    ap = mm(a, j)
    naive_bp = madd(scale(-1, mm(j, b)), mm(b, j))
    naive_residual = madd(mm(tr(a), ap), mm(tr(b), naive_bp))
    assert naive_residual == scale(F(17, 65), j)
    return {"rational_frames": frames, "frame_jet_point_checks": jet_points,
            "wrong_inverse_instead_of_inverse_transpose_rejected": wrong_inverse,
            "omitted_translation_velocity_rejected": omitted_translation,
            "positive_square_root_gauge_residual": "(17/65) J, nonzero"}


def singular_boundary_checks():
    # A=diag(1,0), b'=(0,1/3), h'=2/3 is a singular-defect endpoint.
    a, w, hp = diag(F(1), F(0)), (F(0), F(1, 3)), F(2, 3)
    assert mv(tr(a), w) == (0, 0)
    assert 1 - hp*hp - norm2(w) == F(4, 9)
    for n in (2, 3, 5, 9):
        lam, root = F(n*n-1, n*n+1), F(2*n, n*n+1)
        assert lam*lam + root*root == 1
        ae = scale(lam, a)
        be = diag(root, F(1))
        pe = madd(eye(2), scale(-1, mm(ae, tr(ae))))
        we = tuple(lam * x for x in w)
        assert mm(tr(be), be) == madd(eye(2), scale(-1, mm(tr(ae), ae)))
        assert dot(we, mv(inv(pe), we)) <= 1 - hp*hp
    return {"unit_matrix_norm_endpoint": "A=diag(1,0), b'=(0,1/3), h'=2/3",
            "axial_block_slack": "4/9", "strict_approximants_checked": 4}


def transverse(x):
    u1, u2, z = x
    return (u1/4 + z*u2/8 + z*z/16, z*u1/16 + u2/5 + z/12)


def height(z):
    return -3*z/5 if z <= 0 else 4*z/5


def unfolded(z):
    return 3*z/5 if z <= 0 else 4*z/5


def example_matrix(z):
    return ((F(1, 4), z/8), (z/16, F(1, 5)))


def exact_time_nodes():
    nodes = []
    for m in (F(1, 2), F(13, 25), F(17, 32), F(11, 20), F(9, 16)):
        qm = (7 - 16*(1-m)**2)/(9 - 16*m*m)
        qp = m*qm + 1-m
        t = (1-qm*qm)/F(16, 25)
        assert 0 <= t <= 1 and qm > 0 and qp > 0
        assert qm*qm == 1-F(16, 25)*t
        assert qp*qp == 1-F(9, 25)*t
        nodes.append((t, qm, qp))
    assert len(set(t for t, _, _ in nodes)) == len(nodes)
    return nodes


def prism_checks():
    bound = sum([F(1, 16), F(1, 25), F(1, 64), F(1, 256),
                 F(1, 16), F(49, 2304), F(16, 25)])
    assert bound == F(24359, 28800) < 1
    aminus, aplus = example_matrix(F(-1)), example_matrix(F(1))
    commutator = madd(mm(aminus, aplus), scale(-1, mm(aplus, aminus)))
    assert commutator == ((0, F(1, 80)), (F(-1, 160), 0))
    a0 = example_matrix(F(0))
    assert mm(tr(a0), a0)[0][0] != mm(tr(a0), a0)[1][1]
    grams = []
    for z in (F(-1, 2), F(1, 2)):
        jacobian = ((F(1, 4), z/8, z/8), (z/16, F(1, 5), F(1, 12)),
                    (F(0), F(0), F(-3, 5) if z < 0 else F(4, 5)))
        grams.append(mm(tr(jacobian), jacobian))
    gram_commutator = madd(mm(grams[0], grams[1]), scale(-1, mm(grams[1], grams[0])))
    assert gram_commutator[0][1] == F(3913, 36864000)
    points = list(product((F(-1), F(0), F(1)), repeat=2))
    labels = [(u, v, z) for u, v in points
              for z in (F(-1), F(-1, 2), F(0), F(1, 2), F(1))]
    nodes = exact_time_nodes()
    fold_nodes = [(r*r/(1+r*r), r/(1+r*r))
                  for r in (F(0), F(1, 2), F(1), F(2))] + [(F(1), F(0))]
    pairs = first_phase = folding = 0
    min_bridge = None
    for x, y in combinations(labels, 2):
        old_transverse = norm2(vs(x[:2], y[:2]))
        new_transverse = norm2(vs(transverse(x), transverse(y)))
        dz, dh = x[2]-y[2], height(x[2])-height(y[2])
        assert new_transverse + dh*dh <= old_transverse + dz*dz
        lo, hi = sorted((x[2], y[2]))
        lm = max(F(0), min(hi, F(0))-lo)
        lp = hi-lo-lm
        omega_integral = F(4, 5)*lm + F(3, 5)*lp
        gain = new_transverse-old_transverse
        bridge_slack = omega_integral**2-gain
        assert bridge_slack >= 0
        min_bridge = bridge_slack if min_bridge is None else min(min_bridge, bridge_slack)
        for t, qm, qp in nodes:
            length = lm*qm + lp*qp
            cost = lm*F(16, 25)/qm + lp*F(9, 25)/qp
            assert length*cost >= omega_integral**2 >= gain
            distance2 = (1-t)*old_transverse+t*new_transverse+length*length
            assert distance2 <= old_transverse+dz*dz
            assert distance2 >= new_transverse+dh*dh
            first_phase += 1
        xx, yy = unfolded(x[2]), unfolded(y[2])
        gx, gy = height(x[2]), height(y[2])
        assert gx == abs(xx) and gy == abs(yy)
        assert (gx-gy)**2 <= (xx-yy)**2
        for s, root in fold_nodes:
            assert root*root == s*(1-s)
            dx = (1-s)*(xx-yy)+s*(gx-gy)
            dy = root*((xx-gx)-(yy-gy))
            assert dx*dx+dy*dy == (1-s)*(xx-yy)**2+s*(gx-gy)**2
            folding += 1
        pairs += 1
    # A direct linear height clock increases a pair distance at its endpoint.
    x, y = (F(0), F(0), F(-1)), (F(0), F(0), F(-1, 2))
    gain = norm2(vs(transverse(x), transverse(y)))
    dz, dh = x[2]-y[2], height(x[2])-height(y[2])
    bad_derivative = gain + 2*dh*(dh-dz)
    assert bad_derivative > 0
    return {"jacobian_frobenius_square_bound": str(bound),
            "global_contraction_slack": str(1-bound),
            "matrix_commutator_off_diagonal": ["1/80", "-1/160"],
            "jacobian_gram_commutator_entry_12": str(gram_commutator[0][1]),
            "labels": len(labels), "unordered_pairs": pairs,
            "first_phase_pair_time_controls": first_phase,
            "folding_pair_time_controls": folding,
            "minimum_sampled_bridge_slack": str(min_bridge),
            "time_nodes": [{"t": str(t), "q_minus": str(qm), "q_plus": str(qp)}
                           for t, qm, qp in nodes],
            "wrong_linear_height_clock_positive_derivative": str(bad_derivative)}


def main():
    if not __debug__:
        raise SystemExit("Run without -O: this exact checker uses assertions.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare with EXPECTED.json")
    args = parser.parse_args()
    result = {"status": "PASS", "arithmetic": "exact rational and sparse polynomial",
              "universal_identities": polynomial_checks(),
              "horizontal_completion": horizontal_jet_checks(),
              "singular_boundary": singular_boundary_checks(),
              "prism_example": prism_checks(),
              "trust_boundary": "Author algebra controls; continuum proof and ODE existence in PROOF.md; independent review pending"}
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["record_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    if args.check:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        assert result == expected, "Computed exact record differs from EXPECTED.json"
        print("PASS: exact record matches EXPECTED.json; sha256=" + result["record_sha256"])
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

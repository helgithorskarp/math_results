#!/usr/bin/env python3
"""Exact reference projection, scalar cutoff and trace-tail checks for PROOF.md."""
from fractions import Fraction as F
import json
import sys


def mul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b, factor=F(1)):
    return [[x+factor*y for x, y in zip(row, other)]
            for row, other in zip(a, b)]


def scale(a, factor):
    return [[x*factor for x in row] for row in a]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def poly(values):
    return tuple(F(x) for x in values)


def pmul(a, b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return tuple(out)


def padd(a, b, factor=F(1)):
    out = tuple((a[i] if i < len(a) else 0)+factor*(b[i] if i < len(b) else 0)
                for i in range(max(len(a), len(b))))
    while out and out[-1] == 0:
        out = out[:-1]
    return out


def deriv(a):
    return tuple(i*a[i] for i in range(1, len(a)))


checks = []


def equal(label, actual, expected):
    if actual != expected:
        raise ArithmeticError(label+": "+repr(actual)+" != "+repr(expected))
    checks.append(label)


def positive(label, value):
    if value <= 0:
        raise ArithmeticError(label)
    checks.append(label)


def main():
    n = 8
    sign = [F(1)]*4+[F(-1)]*4
    identity = [[F(i == j) for j in range(n)] for i in range(n)]
    zero = [[F(0) for _ in range(n)] for _ in range(n)]
    qe = [[F(1, 8) for _ in range(n)] for _ in range(n)]
    qs = [[sign[i]*sign[j]/8 for j in range(n)] for i in range(n)]
    p = add(identity, qe, -1)
    diag = [[sign[i] if i == j else F(0) for j in range(n)] for i in range(n)]
    l = mul(mul(p, diag), p)
    l2 = mul(l, l)
    equal("whole normalized reference square", l2, add(p, qs, -1))
    equal("whole reference cubic", mul(l2, l), l)
    equal("whole reference annihilates constant subspace", mul(l, qe), zero)
    equal("whole reference annihilates sign subspace", mul(l, qs), zero)
    proj = {"plus": scale(add(l2, l), F(1, 2)),
            "minus": scale(add(l2, l, -1), F(1, 2)),
            "zero": add(qe, qs)}
    eigen = {"plus": F(1), "minus": F(-1), "zero": F(0)}
    for name, a in proj.items():
        equal(name+" whole idempotence", mul(a, a), a)
        equal(name+" whole eigenvalue equation", mul(l, a), scale(a, eigen[name]))
        equal(name+" rank from projection trace", trace(a), 2 if name == "zero" else 3)
        equal(name+" whole symmetry", a, [list(x) for x in zip(*a)])
        for other, b in proj.items():
            if other != name:
                equal(name+" versus "+other+" whole orthogonality", mul(a, b), zero)
    equal("whole reference projector resolution", add(add(proj["plus"], proj["minus"]), proj["zero"]), identity)
    equal("constant mode rank", trace(qe), 1)
    equal("sign mode rank", trace(qs), 1)
    equal("whole constant/sign orthogonality", mul(qe, qs), zero)

    c = F(1, 8)
    sign_slack = padd(tuple(25*x for x in poly([c, -1])),
                      tuple(9*x for x in poly([c, 1])), -1)
    equal("whole squared sign-count gap", sign_slack, poly([2, -34]))
    equal("whole symmetric square-root product", pmul(poly([c, 1]), poly([c, -1])),
          poly([c*c, 0, -1]))
    positive("sign-count endpoint less than squared-magnitude floor", c-F(1, 17))
    positive("sign-count endpoint permits strict central separation", F(3, 32)-F(1, 17))
    positive("F derivative positive on entire sign interval", F(6, 55)-F(1, 17))
    qmax = F(1, 17)**2/(c-F(1, 17))
    equal("satellite q upper endpoint", qmax, F(136, 2601))
    positive("satellite numerator monotonic throughout feasible q range", F(6, 7)-qmax)
    equal("whole satellite q derivative numerator",
          padd(pmul(deriv(poly([0, 0, 1])), poly([c, -1])),
               pmul(poly([0, 0, 1]), deriv(poly([c, -1]))), -1),
          poly([0, F(1, 4), -1]))
    fn = poly([2*c, -2, -F(7, 6)])
    fd = pmul(poly([c, -1]), poly([c, -1]))
    # The exact derivative numerator is (c-t)*(1/4-55t/24).
    fder = padd(pmul(deriv(fn), fd), pmul(fn, deriv(fd)), -1)
    equal("whole angular derivative numerator", fder,
          pmul(poly([c, -1]), poly([F(1, 4), -F(55, 24)])))

    def bound(t):
        return 2/(c-t)-F(7, 6)*t*t/(c-t)**2

    low = F(1, 676)
    high = F(3, 112)
    equal("rational low-D square", F(1, 26)**2, low)
    positive("new small-D cutoff in proved sign interval", F(1, 17)-F(1, 26))
    equal("new small-D angular endpoint", bound(F(1, 26)), F(5560, 243))
    equal("new endpoint margin below23", 23-bound(F(1, 26)), F(29, 243))
    equal("new endpoint margin below47/2", F(47, 2)-bound(F(1, 26)), F(301, 486))
    equal("old small-D endpoint strengthened", bound(F(1, 27)), F(24400, 1083))
    equal("old endpoint new margin below47/2", F(47, 2)-bound(F(1, 27)), F(2101, 2166))
    positive("new domain strictly extends old odd-moment collar", low-F(1, 729))
    positive("remaining D band nonempty", high-low)
    equal("remaining E lower endpoint", F(3, 64)-high/8, F(39, 896))
    equal("remaining E upper endpoint", F(3, 64)-low/8, F(505, 10816))
    # New source combines the spectral collar with its proved trace tail.
    d = poly([0, 1])
    variance = poly([F(3, 224), F(1, 2)])
    centered = poly([-F(3, 28), 1])
    equal("whole centered trace Gram slack",
          padd(tuple(F(6, 7)*x for x in variance), pmul(centered, centered), -1),
          poly([0, F(9, 14), -1]))
    un, ud = poly([144, -224]), poly([3, 112])
    equal("whole trace-tail derivative numerator",
          padd(pmul(deriv(un), ud), pmul(un, deriv(ud)), -1), poly([-16800]))
    def tail(d):
        return (144-224*d)/(3+112*d)
    equal("trace-tail endpoint", tail(F(3, 112)), F(23))
    equal("credited sign moment D floor", F(13, 84)-F(1, 8), F(5, 168))
    equal("all-level sign angular consequence", tail(F(5, 168)), F(412, 19))
    positive("all-level sign consequence excludes threshold23", 23-tail(F(5, 168)))
    output = {
        "actual_agent": "six-sendov-2", "role": "researcher", "pass": 49,
        "coefficient_domain": "Q; exact8x8 rational reference matrices, Q[t] scalar polynomials",
        "complete_checks": len(checks), "checks": checks,
        "whole_reference_L": [[str(x) for x in row] for row in l],
        "whole_reference_L2": [[str(x) for x in row] for row in l2],
        "whole_reference_projectors": {name: [[str(x) for x in row] for row in a]
                                       for name, a in proj.items()},
        "whole_scalar_coefficients": {"sign_slack": list(map(str, sign_slack)),
                                      "angular_derivative_numerator": list(map(str, fder))},
        "new_small_D": str(low), "new_C_upper": "5560/243",
        "remaining_open_D_band": [str(low), str(high)],
        "remaining_open_E_band": ["39/896", "505/10816"],
        "odd_moment_hypothesis": False,
        "ordinary_unformalized_bridges": ["sign inequalities", "min-max spectral perturbation",
                                          "full grouped spectral masses/Cauchy", "angular definition/continuity"],
        "global_region_infeasibility_decision_or_peer_review": False,
    }
    json.dump(output, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

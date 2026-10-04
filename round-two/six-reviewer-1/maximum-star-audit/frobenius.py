"""Fresh simultaneous-coordinate Frobenius budget; exact original entries."""
import argparse
import hashlib
import json
from itertools import product
from math import comb, isqrt
from pathlib import Path
from arithmetic import require


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def coefficients(n, lo, hi):
    sizes = range(lo, hi+1)
    f = {a: sum(choose(n-a-1, b-1) for b in sizes) for a in sizes}
    h = {a: sum((b-1)*choose(n-a, b) for b in sizes) for a in sizes}
    u = sum(choose(n-2, a-1)*f[a] for a in sizes)
    v = sum(choose(n-1, a)*(a-1)*f[a] for a in sizes)
    w = sum(choose(n, a)*(a-1)*h[a] for a in sizes)
    ordered = sum(choose(n, a)*choose(n-a, b) for a in sizes for b in sizes)
    require(ordered % 2 == 0, "free involution parity")
    D = ordered//2
    pieces = [w*w, 2*n*v*v, n*(n-1)*u*u,
              2*sum(choose(n, a)*h[a]**2 for a in sizes),
              2*sum(choose(n, a)*(n-a)*f[a]**2 for a in sizes), 2*D]
    return {"f": f, "h": h, "u": u, "v": v, "w": w, "D": D,
            "pieces": pieces, "B": sum(pieces)}


def literal(n, lo, hi, damage=None):
    """Build every original entry by sparse endpoint outer products, not formulas."""
    d = [x for x in range(1 << n) if x.bit_count() <= n-2]
    V = [x for x in d if lo <= x.bit_count() <= hi]
    pos = {x: i for i, x in enumerate(d)}
    edges = [(x, y) for i, x in enumerate(V) for y in V[i+1:] if not x & y]
    columns = {x: [(pos[0], x.bit_count()-1)]+[(pos[1 << i], -1) for i in range(n) if x & (1 << i)]+[(pos[x], 1)] for x in V}
    N = len(d)

    def matrix(signs):
        P = [[0]*N for _ in d]
        for (x, y), theta in zip(edges, signs):
            for i, a in columns[x]:
                for j, b in columns[y]:
                    P[i][j] += theta*a*b
                    P[j][i] += theta*a*b
        return P

    P = matrix([1]*len(edges))
    c = coefficients(n, lo, hi)
    require(c["D"] == len(edges), "literal all disjoint pair count")
    for i, x in enumerate(d):
        for j, y in enumerate(d):
            if not x and not y:
                expected = c["w"]
            elif not x and y.bit_count() == 1 or not y and x.bit_count() == 1:
                expected = -c["v"]
            elif x.bit_count() == y.bit_count() == 1:
                expected = c["u"] if x != y else 0
            elif not x and y in V or not y and x in V:
                expected = c["h"][(y or x).bit_count()]
            elif x.bit_count() == 1 and y in V or y.bit_count() == 1 and x in V:
                singleton, set_ = (x, y) if x.bit_count() == 1 else (y, x)
                expected = -c["f"][set_.bit_count()] if not singleton & set_ else 0
            elif x in V and y in V:
                expected = int(x != y and not x & y)
            else:
                expected = 0
            if damage == "drop_empty_square" and not x and not y:
                expected = 0
            if damage == "wrong_star_sign" and not x and y.bit_count() == 1:
                expected = -expected
            require(P[i][j] == expected, "all original Frobenius type entries")
    squared = sum(z*z for row in P for z in row)
    require(squared == c["B"], "full original sum of squared entries")
    if damage == "unordered_half":
        require(squared == c["B"]-c["D"], "ordered original positions count twice")
    row_sign = [-1 if x.bit_count() == 1 else 1 for x in d]
    require(all(row_sign[i]*row_sign[j]*P[i][j] >= 0 for i in range(N) for j in range(N)), "nonnegative row-sign lift")
    # Independently check every elementary basis for entrywise positivity after row flip.
    for x, y in edges:
        z = {}
        for i, a in columns[x]:
            for j, b in columns[y]:
                z[i, j] = z.get((i, j), 0)+a*b
                z[j, i] = z.get((j, i), 0)+a*b
        require(all(row_sign[i]*row_sign[j]*value >= 0 for (i, j), value in z.items()), "every basis entry nonnegative")
    controls = [[1]*len(edges), [-1]*len(edges),
                [(-1)**i for i in range(len(edges))],
                [((i*7) % 3)-1 for i in range(len(edges))]]
    if len(edges) <= 8:
        controls.extend(product((-1, 1), repeat=len(edges)))
    norms = []
    for signs in controls:
        actual = matrix(signs)
        norm = sum(z*z for row in actual for z in row)
        require(norm <= squared, "simultaneous box Frobenius domination")
        require(all(abs(actual[i][j]) <= abs(P[i][j]) for i in range(N) for j in range(N)), "entire coordinatewise domination")
        norms.append(norm)
    require(norms[0] == squared, "sharp simultaneous all-plus assignment")
    return {"n": n, "lo": lo, "hi": hi, "original_vertices": d, "V": V,
            "edges": edges, "P": P, "coefficients": c, "B": squared,
            "all_original_positions": N*N, "basis_count": len(edges),
            "control_squared_norms": norms}


def n28(damage=None):
    n, lo, hi = 28, 9, 19
    c = coefficients(n, lo, hi)
    # Independent global ordered-point moments of the three-part partitions.
    moments = [0, 0, 0, 0]
    for a in range(lo, hi+1):
        for b in range(lo, hi+1):
            count = choose(n, a)*choose(n-a, b)
            moments[0] += count
            moments[1] += count*a*b
            moments[2] += count*(a-1)*b
            moments[3] += count*(a-1)*(b-1)
    require(moments[1] % (n*(n-1)) == 0 and moments[2] % n == 0, "whole moment divisibility")
    require(c["u"] == moments[1]//(n*(n-1)) and c["v"] == moments[2]//n and c["w"] == moments[3], "independent three global moments")
    unused = sum(choose(n, unused)*sum(choose(n-unused, a) for a in range(lo, n-unused-lo+1))
                 for unused in range(n-2*lo+1))
    require(unused == moments[0] == 2*c["D"], "independent unused-point count")
    gamma = n*(n-1)*(2**(n-2)-n+1)+2*(2**n-2*n-2)
    gamma_literal = sum(choose(n, a)*(a*a-a+2) for a in range(2, n-1))
    require(gamma == gamma_literal, "entire Q metric trace")
    degrees = [sum(choose(n-a, b) for b in range(lo, hi+1)) for a in range(lo, hi+1)]
    delta = max(degrees)
    require(delta == degrees[0] == 354522 and all(degrees[i] >= degrees[i+1] for i in range(len(degrees)-1)), "greatest residual degree")
    B = c["B"]
    cap = isqrt(B)+(isqrt(B)**2 < B)
    if damage == "floor_sqrt":
        cap = isqrt(B)
    require((cap-1)**2 < B <= cap*cap, "certified upward integer square root")
    if damage == "underpay_radius":
        cap -= 1
        require(B <= cap*cap, "too-small Frobenius budget")
    q = sum(choose(n, a) for a in range(2, 9))
    N, s = 2**n-n-1, 2**(n-1)-n
    orbits = [(a, b) for a in range(lo, hi+1) for b in range(a, hi+1) if a+b <= n]
    require(len(orbits) == 36, "all unordered size orbits")
    require(27*cap < gamma*delta < 28*cap, "exact factor greater than27 and less than28")
    require(B == 433849844850403385325195747450 and cap == 658672790428149, "whole fresh n28 budget")
    return {"N": N, "s": s, "q": q, "D": c["D"], "slice_dimension": c["D"]-len(orbits),
            "original_lower_rank": N-n-q, "original_cap_rank": N-1,
            "gamma": gamma, "delta": delta, "degrees": degrees, "orbits": orbits,
            "budget": c, "global_moments": moments, "ceil_sqrt_B": cap,
            "old_radius_denominator": 400000000*gamma*delta,
            "new_radius_denominator": 400000000*cap,
            "empty_loop_single_middle_coordinate_factor": 2*(14-1)**2}


def coverage_gate(damage):
    # A retained singleton disjoint from every maximum-star point has r_B=0.
    # Its lifted empty entry is -1, so the stated nonnegative-column gate fails.
    r = 0
    covered = r >= 1
    require(not covered and r-1 < 0, "uncovered residual witness")
    if damage == "omit_coverage":
        require(covered, "new sharp-budget coverage premise is required")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--record")
    p.add_argument("--damage", choices=["drop_empty_square", "wrong_star_sign", "unordered_half",
                                        "floor_sqrt", "underpay_radius", "omit_coverage"])
    args = p.parse_args()
    coverage_gate(args.damage)
    cases = [literal(n, lo, hi, args.damage) for n, lo, hi in [(4, 2, 2), (5, 2, 3), (6, 2, 4), (7, 3, 4), (8, 3, 5), (9, 4, 5)]]
    record = {"literal_controls": cases, "n28": n28(args.damage), "uncovered_residual_gate": "not covered"}
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    summary = {"prototype_count": len(cases), "entire_original_positions": sum(x["all_original_positions"] for x in cases),
               "entire_basis_matrices": sum(x["basis_count"] for x in cases),
               "prototype_B": [x["B"] for x in cases],
               "record_bytes": len(payload), "record_sha256": hashlib.sha256(payload).hexdigest(),
               "n28": record["n28"]}
    if args.record:
        Path(args.record).write_bytes(payload)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()

"""Independent original-equation RREF and full-matrix controls. No author code."""
import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
from arithmetic import add, encode, eye, inverse, mm, psd, rank, require, solve, tr


def fixture(n, facets):
    d = sorted({b for a in facets for b in range(1 << n) if b & a == b})
    require(d[0] == 0 and all(1 << i in d for i in range(n)), "active downset")
    return d


def setup(n, d):
    N = len(d)
    sizes = [sum(bool(b & (1 << i)) for b in d) for i in range(n)]
    s = max(sizes)
    stars = [i for i in range(n) if sizes[i] == s]
    q = [b for b in d if b and b not in [1 << i for i in stars]]
    a = [[F((b & sum(1 << i for i in stars)).bit_count()-1) if x == 0
          else F(-bool(b & x)) if x in [1 << i for i in stars]
          else F(x == b) for b in q] for x in d]
    return N, s, stars, q, a


def original(n, d, selected, star_mode="maximum", raw=False):
    """Encode L directly on every original disjoint entry, before any decoder."""
    N, s, stars, q, a = setup(n, d)
    if star_mode == "all":
        stars = list(range(n))
    vars_ = [(i, j) for i, x in enumerate(d) for j, y in enumerate(d[i:], i) if not x & y]
    ix = {pair: k for k, pair in enumerate(vars_)}
    constant = [[F(s if i == j and x else 0) for j, y in enumerate(d)] for i, x in enumerate(d)]
    rows = []

    def equation(terms, rhs):
        row = [F(0)]*(len(vars_)+1)
        row[-1] = rhs
        for i, j, coefficient in terms:
            pair = tuple(sorted((i, j)))
            if pair in ix:
                row[ix[pair]] += coefficient
            else:
                row[-1] -= coefficient*constant[i][j]
        rows.append(row)

    for i in range(N):
        equation([(i, j, 1) for j in range(N)], N)
    for t in stars:
        js = [j for j, b in enumerate(d) if b & (1 << t)]
        for i in range(N):
            equation([(i, j, 1) for j in js], s)
    for x, y in selected:
        i, j = d.index(x), d.index(y)
        equation([(i, j, 1)], s)
        if not raw:
            for k in range(N):
                equation([(k, i, 1), (k, j, -1)], 0)
    base, null = solve(rows, len(vars_))

    def lift(v, affine=True):
        z = [r[:] for r in constant] if affine else [[F(0)]*N for _ in d]
        for (i, j), x in zip(vars_, v):
            z[i][j] = z[j][i] = x
        return z

    return lift(base), [lift(v, False) for v in null], rows, vars_


def decoder(n, d, selected, values=None, omit_complements=False):
    N, s, stars, q, a = setup(n, d)
    endpoints = {x for pair in selected for x in pair}
    v = [x for x in q if x not in endpoints]
    free = [(x, y) for i, x in enumerate(v) for y in v[i+1:] if not x & y]
    if omit_complements:
        free = [e for e in free if e[0] | e[1] != (1 << n)-1]
    t = [[F(s-1 if i == j else -1 if x & y else 0) for j, y in enumerate(q)] for i, x in enumerate(q)]
    for x, y in selected:
        for b in (x, y):
            j = q.index(b)
            for i, c in enumerate(q):
                t[i][j] = t[j][i] = F(s-1 if c in (x, y) else -1)
    for (x, y), z in zip(free, values or [0]*len(free)):
        i, j = q.index(x), q.index(y)
        t[i][j] = t[j][i] = F(z)
    l = add([[F(1)]*N for _ in d], mm(mm(a, t), tr(a))) if q else [[F(1)]*N for _ in d]
    return l, t, free


def system(name, n, d, selected=(), damage=None):
    N, s, stars, q, a = setup(n, d)
    base, null, rows, vars_ = original(n, d, selected, "all" if damage == "smaller_star" else "maximum")
    l, t, free = decoder(n, d, selected, omit_complements=damage == "omit_complements")
    require(len(null) == len(free), "full original affine dimension")
    records = []
    solutions = [base]+[add(base, v) for v in null]
    decoded = [l]+[decoder(n, d, selected, [int(i == j) for i in range(len(free))])[0] for j in range(len(free))]
    for L in solutions+decoded:
        recovered = [[L[d.index(x)][d.index(y)]-1 for y in q] for x in q]
        rebuilt = add([[F(1)]*N for _ in d], mm(mm(a, recovered), tr(a))) if q else [[F(1)]*N for _ in d]
        require(rebuilt == L, "entire original round trip")
        require(all(sum(r) == N for r in L), "actual empty row and all row sums")
        require(all(L[i][j] == (s if i == j else 0) for i, x in enumerate(d) for j, y in enumerate(d) if x & y), "full original support")
        require(all(sum(L[i][j] for j, b in enumerate(d) if b & (1 << k)) == s for k in stars for i in range(N)), "all maximum-star actions")
        if q:
            g = mm(tr(a), a)
            formula = [[F(i == j)+sum(bool(x & (1 << k))*bool(y & (1 << k)) for k in stars)
                        +(1-sum(bool(x & (1 << k)) for k in stars))*(1-sum(bool(y & (1 << k)) for k in stars))
                        for j, y in enumerate(q)] for i, x in enumerate(q)]
            if damage == "empty_metric":
                formula = [[z-(1-sum(bool(x & (1 << k)) for k in stars))*(1-sum(bool(y & (1 << k)) for k in stars))
                            for z, y in zip(r, q)] for r, x in zip(formula, q)]
            require(g == formula, "full metric including actual empty term")
            gi = inverse(g)
            u = [[F(bool(x & (1 << k)))-F(s, N) for k in stars] for x in d]
            pu = mm(mm(u, inverse(mm(tr(u), u))), tr(u))
            expected = add(add(eye(N), [[F(-1, N)]*N for _ in d]), mm(mm(a, gi), tr(a)), -1)
            require(pu == expected and mm(pu, pu) == pu, "entire original star projector")
            cap = add([[N*z for z in r] for r in eye(N)], L, -1)
            reduced = add([[N*z for z in r] for r in gi], recovered, -1)
            cap_decode = add([[N*z for z in r] for r in pu], mm(mm(a, reduced), tr(a)))
            require(cap == cap_decode, "entire original cap identity")
            require(rank(L) == 1+rank(recovered), "lower rank")
            require(rank(cap) == len(stars)+rank(reduced), "cap rank including forced stars")
            _, lower_null = solve([r+[F(0)] for r in recovered], len(q))
            _, upper_null = solve([r+[F(0)] for r in reduced], len(q))
            lower_vectors = tr(u)+[tr(mm(mm(a, gi), [[x] for x in v]))[0] for v in lower_null]
            upper_vectors = [[F(1)]*N]+[tr(mm(mm(a, gi), [[x] for x in v]))[0] for v in upper_null]
            require(all(all(sum(row[j]*v[j] for j in range(N)) == 0 for row in L) for v in lower_vectors), "every original lower kernel vector")
            require(all(all(sum(row[j]*v[j] for j in range(N)) == 0 for row in cap) for v in upper_vectors), "every original upper kernel vector")
            require(rank(lower_vectors) == N-rank(L) and rank(upper_vectors) == N-rank(cap), "entire original kernels spanned")
        for x, y in selected:
            i, j = d.index(x), d.index(y)
            require(L[i][j] == s and all(L[k][i] == L[k][j] for k in range(N)), "all saturated original columns")
            require([L[k][i] for k in range(N)] == [F(N-2*s if b == 0 else s if b in (x, y) else 0) for b in d], "entire saturated column formula")
        records.append(L)
    require(rank([[L[i][j]-l[i][j] for i, j in vars_] for L in solutions]) == len(free), "original solutions span decoded space")
    return {"name": name, "N": N, "s": s, "stars": stars, "Q": q, "selected": selected,
            "dimension": len(free), "original_equations": len(rows), "original_variables": len(vars_),
            "all_matrices": records, "matrix_count": len(records), "entries_checked": N*N*len(records)}


def controls(damage=None):
    cases = [
        ("one-point-s1", 1, [1], ()),
        ("three-point-s1", 3, [1, 2, 4], ()),
        ("cube-two-upper-boundary", 2, [3], ()),
        ("nonregular-path", 3, [3, 6], ()),
        ("path-retained-singleton-saturation", 3, [3, 6], ((1, 6),)),
        ("path-two-saturations", 3, [3, 6], ((1, 6), (4, 3))),
        ("path-isolated-point", 4, [3, 6, 8], ()),
        ("cycle-five", 5, [3, 6, 12, 24, 17], ()),
        ("near-cube-four", 4, [x for x in range(16) if x.bit_count() == 2], ()),
        ("near-cube-four-one-pair", 4, [x for x in range(16) if x.bit_count() == 2], ((3, 12),)),
        ("near-cube-four-all-pairs", 4, [x for x in range(16) if x.bit_count() == 2], ((3, 12), (5, 10), (9, 6))),
        ("near-cube-five", 5, [x for x in range(32) if x.bit_count() == 3], ()),
    ]
    data = [system(name, n, fixture(n, f), selected, damage if name in
                   {"nonregular-path", "near-cube-four"} else None) for name, n, f, selected in cases]
    d = fixture(4, [x for x in range(16) if x.bit_count() == 2])
    N, s, stars, q, a = setup(4, d)
    L, T, _ = decoder(4, d, (), [2, 2, 2])
    G = mm(tr(a), a)
    gi = inverse(G)
    require(psd(T) and psd(add([[N*z for z in r] for r in eye(len(q))], T, -1)), "literal naive cap PSD gates")
    S = add([[N*z for z in r] for r in gi], T, -1)
    energy = sum(sum(r) for r in S)
    require(energy == F(-12, 13) and not psd(S), "literal naive cap countercontrol")
    if damage == "naive_cap":
        require(psd(S), "naive cap substitution fails")
    raw_base, raw_null, _, _ = original(3, fixture(3, [3, 6]), ((1, 6),), raw=True)
    raw_gap = len(raw_null)-data[4]["dimension"]
    require(raw_gap > 0, "raw saturation values do not force affine column equality")
    if damage == "raw_saturation":
        require(raw_gap == 0, "PSD saturation bridge omitted")
    d2 = fixture(2, [3])
    L2, T2, _ = decoder(2, d2, ())
    require(psd(L2) and psd(add([[4*z for z in r] for r in eye(4)], L2, -1)), "cube-two both cones")
    unit_multiplicity = 4-rank(add([[4*z for z in r] for r in eye(4)], L2, -1))
    require(unit_multiplicity == 2, "upper degeneracy retained")
    if damage == "simple_unit_boundary":
        require(unit_multiplicity == 1, "false boundary simplicity")
    return {"systems": data, "raw_saturation_extra_dimension": raw_gap,
            "naive_cap": {"T": T, "G": G, "L": L, "actual_cap_energy": energy},
            "upper_boundary_unit_multiplicity": unit_multiplicity}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--record")
    p.add_argument("--damage", choices=["smaller_star", "omit_complements", "empty_metric", "naive_cap", "raw_saturation", "simple_unit_boundary"])
    args = p.parse_args()
    result = encode(controls(args.damage))
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    summary = {"system_count": len(result["systems"]), "matrix_count": sum(x["matrix_count"] for x in result["systems"]),
               "original_entries_checked": sum(x["entries_checked"] for x in result["systems"]),
               "dimensions": [x["dimension"] for x in result["systems"]],
               "record_bytes": len(payload), "record_sha256": hashlib.sha256(payload).hexdigest(),
               "raw_saturation_extra_dimension": result["raw_saturation_extra_dimension"],
               "naive_cap_energy": result["naive_cap"]["actual_cap_energy"],
               "upper_boundary_unit_multiplicity": result["upper_boundary_unit_multiplicity"]}
    if args.record:
        Path(args.record).write_bytes(payload)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact kernel audits and a rational maximal-rank Hoffman perturbation.

All arithmetic is integral or fractions.Fraction. The universal theorem is
written in KERNEL_TRADE_PROOF.md; this program checks stated finite inputs.
The two-STS9 fixture is a small, attributed public dependency, not a census.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
from math import comb
import argparse
import copy
import hashlib
import json


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def ordered(members):
    return sorted(set(members), key=lambda a: (a.bit_count(), a))


def mask(points):
    return sum(1 << i for i in points)


def digest(matrix):
    serial = [[str(F(x)) for x in row] for row in matrix]
    return hashlib.sha256(json.dumps(serial, separators=(",", ":")).encode()).hexdigest()


def psd_details(matrix):
    """Exact Schur certificate and a positive-eigenvalue lower bound.

    The selected original principal submatrix G is positive definite.
    Its LDL factors give 1/trace(G^{-1}); interlacing makes this a lower
    bound for the smallest positive eigenvalue of the original matrix.
    """
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "nonsquare PSD input")
    require(all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n)),
            "asymmetric PSD input")
    a = [[F(x) for x in row] for row in matrix]
    lower = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    indices, pivots = [], []
    for k in range(n):
        pivot = a[k][k]
        require(pivot >= 0, "negative Schur pivot")
        if pivot == 0:
            require(not any(a[k][j] for j in range(k+1, n)),
                    "zero pivot with nonzero residual row")
            continue
        indices.append(k)
        pivots.append(pivot)
        for i in range(k+1, n):
            lower[i][k] = a[i][k] / pivot
        for i in range(k+1, n):
            if lower[i][k]:
                for j in range(i, n):
                    a[i][j] -= lower[i][k] * a[k][j]
                    a[j][i] = a[i][j]
    rank = len(indices)
    if not rank:
        return {"rank": 0, "positive_lower_bound": None}
    inverse = [[F(int(i == j)) for j in range(rank)] for i in range(rank)]
    for i in range(rank):
        for j in range(i):
            inverse[i][j] = -sum(lower[indices[i]][indices[k]] * inverse[k][j]
                                  for k in range(j, i))
    trace_inverse = sum(sum(x*x for x in row) / pivot
                        for row, pivot in zip(inverse, pivots))
    require(trace_inverse > 0, "nonpositive inverse trace")
    return {"rank": rank, "positive_lower_bound": 1 / trace_inverse}


def vector_rank(vectors):
    if not vectors:
        return 0
    a = [[F(x) for x in row] for row in zip(*vectors)]
    row = 0
    for col in range(len(vectors)):
        pivot = next((k for k in range(row, len(a)) if a[k][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        value = a[row][col]
        a[row] = [x/value for x in a[row]]
        for k in range(row+1, len(a)):
            value = a[k][col]
            if value:
                a[k] = [x-value*y for x, y in zip(a[k], a[row])]
        row += 1
    return row


def largest_stars(members):
    active_mask = 0
    for a in members:
        active_mask |= a
    active = [i for i in range(active_mask.bit_length()) if active_mask >> i & 1]
    sizes = {i: sum(a >> i & 1 for a in members) for i in active}
    s = max(sizes.values())
    return active, s, [i for i in active if sizes[i] == s]


def check_definition(members, s, L):
    n = len(members)
    require(len(set(members)) == n and members[0] == 0, "bad member domain")
    included = set(members)
    require(all(a ^ (1 << i) in included for a in members
                for i in range(a.bit_length()) if a >> i & 1), "not a downset")
    require(len(L) == n and all(len(row) == n for row in L), "bad matrix shape")
    require(all(L[i][j] == L[j][i] for i in range(n) for j in range(n)),
            "matrix asymmetry")
    require(all(sum(row) == n for row in L), "wrong Hoffman row sum")
    require(all(L[i][j] == (s if i == j else 0)
                for i, a in enumerate(members) for j, b in enumerate(members) if a & b),
            "wrong supported diagonal or intersection entry")
    active, actual_s, stars = largest_stars(members)
    require(actual_s == s and 0 < 2*s < n, "wrong star or half-density boundary")
    vectors = [[n*int(bool(a >> i & 1))-s for a in members] for i in stars]
    require(all(sum(x*y for x, y in zip(row, v)) == 0
                for row in L for v in vectors), "star kernel equation failed")
    require(vector_rank(vectors) == len(stars), "star vectors dependent")
    return active, stars, vectors


def lift(core):
    sums = [sum(row) for row in core]
    return [[1+sum(sums)] + [1-x for x in sums]] + [
        [1-sums[i]] + [1+x for x in row] for i, row in enumerate(core)]


def trade(members, active):
    n = len(active)
    require(n >= 4, "trade needs at least four active points")
    require(all(mask(p) in members for p in combinations(active, 2)),
            "trade requires the full two-skeleton")
    delta = []
    for a in members[1:]:
        row = []
        for b in members[1:]:
            sizes = sorted((a.bit_count(), b.bit_count()))
            value = 0
            if not a & b:
                if sizes == [1, 1]:
                    value = (n-2)*(n-3)
                elif sizes == [1, 2]:
                    value = -(n-3)
                elif sizes == [2, 2]:
                    value = 1
            row.append(F(value))
        delta.append(row)
    total = F(n*(n-1)*(n-2)*(n-3), 4)
    bound = F(3*(n-1)*(n-2)*(n-3), 2)
    require(sum(map(sum, delta)) == total, "trade total differs")
    require(max(sum(abs(x) for x in row) for row in delta) == bound,
            "trade absolute-row bound differs")
    require(all(sum(row[j] for j, b in enumerate(members[1:]) if b >> i & 1) == 0
                for row in delta for i in active), "trade failed a coordinate-star kernel")
    return delta, total, bound


def outside_singletons_trade(members, active, stars):
    """An allowed two-entry trade outside every largest coordinate star."""
    outside = [i for i in active if i not in stars]
    require(len(outside) >= 2, "singleton trade needs two smaller-star coordinates")
    indices = [members[1:].index(1 << i) for i in outside[:2]]
    delta = [[F(0) for _ in members[1:]] for _ in members[1:]]
    a, b = indices
    delta[a][b] = delta[b][a] = F(1)
    require(all(sum(row[j] for j, vertex in enumerate(members[1:]) if vertex >> i & 1) == 0
                for row in delta for i in stars), "singleton trade failed a largest star")
    require(sum(map(sum, delta)) == 2 and max(sum(abs(x) for x in row) for row in delta) == 1,
            "singleton trade bounds differ")
    require(all(not delta[i][j] or not members[i+1] & members[j+1]
                for i in range(len(delta)) for j in range(len(delta))),
            "singleton trade changed an intersecting entry")
    return delta, F(2), F(1)


def audit_case(tag, members, s, L, perturb):
    active, stars, vectors = check_definition(members, s, L)
    n, r, m = len(members), len(stars), len(members)-1
    require(all(x == 1 for x in L[0]), "base empty column is not all ones")
    v0 = [n*int(i == 0)-1 for i in range(n)]
    require(all(sum(x*y for x, y in zip(row, v0)) == 0 for row in L),
            "empty-centered vector not in base kernel")
    require(vector_rank(vectors+[v0]) == r+1, "base kernel directions dependent")
    core = [[L[i][j]-1 for j in range(1, n)] for i in range(1, n)]
    require(all(sum(row) == 0 for row in core), "base core is not centered")
    upper = [[F(n*int(i == j)-1)-core[i][j] for j in range(m)] for i in range(m)]
    lower_data, upper_data = psd_details(core), psd_details(upper)
    require(lower_data["rank"] == n-r-2 and upper_data["rank"] == m,
            "base PSD ranks do not give the stated kernel")
    result = {"case": tag, "N": n, "s": s, "largest_star_count": r,
              "base_H_PSD_rank": 1+lower_data["rank"], "upper_rank": upper_data["rank"],
              "base_H_PSD_sha256": digest(L), "kernel_basis_rank": r+1,
              "maximum_family_count_by_written_lemma": 4 if set(members) == set(range(7)) else r}
    if not perturb:
        return result
    if perturb == "outside-singletons":
        delta, total, bound = outside_singletons_trade(members, active, stars)
        trade_kind = "two smaller-star singletons"
    else:
        delta, total, bound = trade(members, active)
        trade_kind = "full two-skeleton disjoint-pair trade"
    alpha, beta = lower_data["positive_lower_bound"], upper_data["positive_lower_bound"]
    allowed_epsilon = min(F(1), alpha/(4*bound), beta/(4*bound),
                          total*alpha/(8*m*bound*bound))
    # Round downward exactly to a reciprocal integer, keeping entries small.
    denominator = (allowed_epsilon.denominator+allowed_epsilon.numerator-1)//allowed_epsilon.numerator
    epsilon = F(1, denominator)
    require(0 < epsilon <= allowed_epsilon, "reciprocal rounding increased epsilon")
    require(epsilon > 0 and epsilon*bound <= alpha/4
            and epsilon*bound <= beta/4
            and epsilon*8*m*bound*bound <= total*alpha, "invalid exact perturbation bound")
    refined = [[core[i][j]+epsilon*delta[i][j] for j in range(m)] for i in range(m)]
    refined_upper = [[upper[i][j]-epsilon*delta[i][j] for j in range(m)] for i in range(m)]
    new_L = lift(refined)
    check_definition(members, s, new_L)
    require(new_L[0][0] == 1+epsilon*total and new_L[0][0] > 1,
            "missing empty-direction lift")
    new_lower, new_upper = psd_details(refined), psd_details(refined_upper)
    require(new_lower["rank"] == n-r-1 and new_upper["rank"] == m,
            "refined matrices fail maximal-rank capped bounds")
    result.update({"alpha": str(alpha), "beta": str(beta), "epsilon": str(epsilon),
                   "trade_kind": trade_kind,
                   "trade_total": str(total), "trade_norm_bound": str(bound),
                   "refined_H_PSD_rank": 1+new_lower["rank"],
                   "refined_upper_rank": new_upper["rank"],
                   "refined_empty_L_entry": str(new_L[0][0]),
                   "refined_H_PSD_sha256": digest(new_L)})
    return result


def uniform_two(n):
    members = ordered([0]+[1 << i for i in range(n)] +
                      [mask(p) for p in combinations(range(n), 2)])
    L = []
    for a in members:
        row = []
        for b in members:
            if not a or not b:
                value = F(1)
            elif a & b:
                value = F(n if a == b else 0)
            elif a.bit_count() == b.bit_count() == 1:
                value = F(0)
            else:
                value = F(n, n-2)
            row.append(value)
        L.append(row)
    return members, n, L


def friendship(k):
    center = 1 << (2*k)
    members = ordered([0, center]+[1 << i for i in range(2*k)] +
                      [center | (1 << i) for i in range(2*k)] +
                      [mask((2*j, 2*j+1)) for j in range(k)])
    def kind(a):
        if a == center:
            return "a", None
        if a.bit_count() == 1:
            return "c", (a.bit_length()-1)//2
        if a & center:
            return "b", ((a ^ center).bit_length()-1)//2
        return "d", ((a & -a).bit_length()-1)//2
    s = 2*k+1
    L = []
    for a in members:
        row = []
        for b in members:
            if not a or not b:
                value = F(1)
            elif a & b:
                value = F(s if a == b else 0)
            else:
                ta, ja = kind(a); tb, jb = kind(b); types = {ta, tb}
                if "a" in types:
                    value = F(1)
                elif "b" in types:
                    value = F(0) if ja == jb else F(k, k-1)
                elif ta == tb == "c":
                    value = F(k-1) if ja == jb else F(0)
                elif types == {"c", "d"}:
                    value = F(0)
                else:
                    value = F(1)
            row.append(value)
        L.append(row)
    return members, s, L


def two_centers(t):
    """Credited centered K_2 joined to t independent leaves; t>=2."""
    require(t >= 2, "two-center audit starts beyond the triangle boundary")
    leaves = [1 << i for i in range(2, t+2)]
    members = ordered([0,1,2,3]+leaves+[c|a for c in leaves for a in (1,2)])
    core = []
    for a in members[1:]:
        row = []
        for b in members[1:]:
            if a == b:
                value = F(t+1)
            elif a & b:
                value = F(-1)
            elif a.bit_count() == b.bit_count() == 1:
                centers = int(a in (1,2))+int(b in (1,2))
                value = F(-1) if centers == 2 else F(-1,t) if centers == 1 else F(-t-1,t)
            elif a.bit_count() == b.bit_count() == 2:
                value = F(2,t)
            else:
                single, pair = (a,b) if a.bit_count() == 1 else (b,a)
                value = F(2,t) if single in (1,2) else F(t+1,t) if pair == 3 else F(0)
            row.append(value)
        core.append(row)
    return members, t+2, lift(core)


def sts_blocks(v):
    if v == 7:
        return sorted({mask((a-1, b-1, (a ^ b)-1))
                       for a, b in combinations(range(1, 8), 2)})
    if v == 9:
        points = list(product(range(3), repeat=2)); index = {p:i for i,p in enumerate(points)}
        return sorted({mask((index[a], index[b],
                             index[((-a[0]-b[0]) % 3, (-a[1]-b[1]) % 3)]))
                       for a, b in combinations(points, 2)})
    if v == 13:
        return sorted({mask((x+t) % 13 for x in base)
                       for base in ((0, 1, 4), (0, 2, 7)) for t in range(13)})
    raise ValueError("only explicit validation orders 7,9,13 are generated")


def check_sts(v, blocks):
    require(len(blocks) == len(set(blocks)) == v*(v-1)//6, "wrong STS block count")
    require(all(a.bit_count() == 3 and 0 < a < 1 << v for a in blocks), "bad triple")
    require(all(sum(a & mask(p) == mask(p) for a in blocks) == 1
                for p in combinations(range(v), 2)), "STS pair coverage failed")


def sts(v):
    blocks = sts_blocks(v); check_sts(v, blocks); included = set(blocks)
    members = ordered([0]+[1 << i for i in range(v)] +
                      [mask(p) for p in combinations(range(v), 2)]+blocks)
    s = (3*v-1)//2
    h, w, beta = F(v+3, v-3), 1+F(v+3, (v-3)*(v-2)), F(-5, v-2)
    L = []
    for a in members:
        row = []
        for b in members:
            sizes = sorted((a.bit_count(), b.bit_count()))
            if not a or not b:
                value = F(1)
            elif a & b:
                value = F(s if a == b else 0)
            elif sizes == [1, 1]:
                value = F(0)
            elif sizes == [1, 2]:
                value = beta if a | b in included else w
            elif sizes == [2, 2]:
                value = w
            elif sizes == [3, 3]:
                value = F(1)
            else:
                value = h
            row.append(value)
        L.append(row)
    return members, s, L


def two_sts9(fixture):
    first = fixture["first_blocks"]
    check_sts(9, first)
    for case in fixture["cases"]:
        second = case["second_blocks"]; check_sts(9, second)
        require(not set(first) & set(second), "systems overlap")
        members = ordered([0]+[1 << i for i in range(9)] +
                          [mask(p) for p in combinations(range(9), 2)]+first+second)
        group = [tuple(p) for p in case["automorphism_subgroup"]]
        require(group and len(set(group)) == len(group), "repeated subgroup element")
        require(tuple(range(9)) in group, "subgroup lacks identity")
        require(all(sorted(p) == list(range(9)) for p in group), "not a permutation")
        require(all(tuple(p[q[i]] for i in range(9)) in group for p in group for q in group),
                "subgroup not closed")
        def moved(a, p):
            return sum(1 << p[i] for i in range(9) if a >> i & 1)
        maps = [{a:moved(a, p) for a in members} for p in group]
        require(all(set(mp.values()) == set(members) for mp in maps), "invalid automorphism")
        entries = {}
        for a, b, weight in case["orbit_entries"]:
            require(a in members and b in members and a <= b and not a & b,
                    "invalid orbit representative")
            orbit = {tuple(sorted((mp[a], mp[b]))) for mp in maps}
            require(not set(entries) & orbit, "overlapping seed orbits")
            entries.update({pair:F(weight) for pair in orbit})
        allowed = {tuple(sorted((a,b))) for i,a in enumerate(members)
                   for b in members[i:] if not a & b}
        require(set(entries) == allowed, "incomplete disjoint-pair table")
        L = [[F(17 if a == b else 0) if a & b else entries[tuple(sorted((a,b)))]
              for b in members] for a in members]
        yield members, 17, L


def maximum_families(members):
    nonempty = [a for a in members if a]
    maximum, families = 0, []
    for word in range(1 << len(nonempty)):
        chosen = [a for i,a in enumerate(nonempty) if word >> i & 1]
        if len(chosen) < maximum or any(not a & b for a,b in combinations(chosen, 2)):
            continue
        if len(chosen) > maximum:
            maximum, families = len(chosen), []
        families.append(chosen)
    return maximum, families


def controls():
    for matrix in ([[F(-1)]], [[F(0),F(1)],[F(1),F(0)]]):
        try:
            psd_details(matrix)
        except AssertionError:
            pass
        else:
            raise AssertionError("indefinite control accepted")
    require(psd_details([[1,0],[0,0]])["rank"] == 1, "singular PSD rank failed")
    require(psd_details([[2,1],[1,2]])["positive_lower_bound"] == F(3,4),
            "inverse-trace bound failed")
    members, s, L = uniform_two(3)
    maximum, families = maximum_families(members)
    expected = sorted([[a for a in members if a >> i & 1] for i in range(3)] + [[3,5,6]])
    require(maximum == s == 3 and sorted(families) == expected,
            "triangle exception classification failed")
    additive = 0
    for a,b,c,d in product((0,1), repeat=4):
        if a+d == b+c:
            require((a == b and c == d) or (a == c and b == d),
                    "additive Boolean rectangle depends on two variables")
            additive += 1
    require(additive == 6, "wrong additive rectangle count")
    majority = [a for a in range(8) if a.bit_count() >= 2]
    cube_max, cube_families = maximum_families(list(range(8)))
    require(cube_max == 4 and majority in cube_families
            and all(majority != [a for a in range(8) if a >> i & 1] for i in range(3)),
            "half-density boundary counterexample failed")
    damaged = copy.deepcopy(L)
    damaged[0][1] += 1; damaged[1][0] += 1
    try:
        check_definition(members,s,damaged)
    except AssertionError:
        pass
    else:
        raise AssertionError("damaged matrix accepted")
    return {"indefinite_controls_rejected":2, "damaged_matrix_rejected":True,
            "triangle_maximum_families":families, "additive_Boolean_rectangles":additive,
            "three_cube_half_density_noncylinder":majority}


def nine_point_boundary_checks():
    """Two attributed nonstar families; conditional ranks, not H feasibility."""
    inside, outside = tuple(range(3)), tuple(range(3,9))
    cross = [mask((*p, q)) for p in combinations(inside,2) for q in outside]
    all_outside = [mask(p) for p in combinations(outside,3)]
    removed = {mask(outside[:3]), mask(outside[3:])}
    records = []
    for include_inside in (0,1):
        triples = cross+([a for a in all_outside if a not in removed]
                         if not include_inside else all_outside+[mask(inside)])
        members = ordered([0]+[1 << i for i in range(9)]+
                          [mask(p) for p in combinations(range(9),2)]+triples)
        active, s, stars = largest_stars(members)
        family = [mask(p) for p in combinations(inside,2)]+cross+([mask(inside)] if include_inside else [])
        n = len(members)
        require(stars == active == list(range(9)) and s == 21+include_inside,
                "boundary stars differ")
        require(n == 82+3*include_inside and len(family) == s and
                all(a & b for a,b in combinations(family,2)), "boundary intersection differs")
        require(not any(all(a >> i & 1 for a in family) for i in active),
                "boundary family has a common coordinate")
        degree = [sum(a >> i & 1 for a in triples) for i in active]
        require(degree == [12+include_inside]*9, "boundary regularity differs")
        zstars = [[n*int(bool(a >> i & 1))-s for a in members] for i in stars]
        zempty = [n*int(i == 0)-1 for i in range(n)]
        zfamily = [n*int(a in family)-s for a in members]
        require(vector_rank(zstars+[zfamily]) == 10 and
                vector_rank(zstars+[zempty,zfamily]) == 11, "boundary kernel independence differs")
        delta, total, bound = trade(members,active)
        indicator = [int(a in family) for a in members[1:]]
        image = [sum(x*y for x,y in zip(row,indicator)) for row in delta]
        quadratic = sum(x*y for x,y in zip(indicator,image))
        require(quadratic == 0 and any(image), "missing exact trade obstruction")
        records.append({"inside_triple_present":bool(include_inside), "N":n, "s":s,
                        "triple_degree":degree[0], "triples":len(triples),
                        "family_masks":sorted(family), "centered_kernel_basis_rank":11,
                        "any_H_rank_upper_bound":n-10, "centered_H_rank_upper_bound":n-11,
                        "trade_quadratic_form":str(quadratic),
                        "trade_image_squared_norm":str(sum(x*x for x in image)),
                        "trade_total":str(total),"trade_norm_bound":str(bound)})
    return {"agent":"six-downset-3","role":"researcher",
            "scope":"Two attributed nine-point examples; conditional rank and trade obstructions, no H matrix or completeness claim.",
            "cases":records}


def run(fixture_path):
    cases = []
    for n in range(3,9):
        cases.append(audit_case("uniform-two-"+str(n), *uniform_two(n), perturb=n>=4))
    for k in range(2,6):
        cases.append(audit_case("friendship-"+str(k), *friendship(k), perturb="outside-singletons"))
    for t in range(2,6):
        cases.append(audit_case("two-centers-"+str(t), *two_centers(t), perturb="outside-singletons"))
    for v in (7,9,13):
        cases.append(audit_case("STS-"+str(v), *sts(v), perturb=True))
    fixture = json.loads(fixture_path.read_text())
    for i,args in enumerate(two_sts9(fixture)):
        cases.append(audit_case("two-STS9-"+str(i+1), *args, perturb=True))
    return {"agent":"six-downset-3","role":"researcher",
            "claim_status":"finite exact audits of written universal trade and kernel-equality theorems",
            "two_STS9_public_fixture_sha256":hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
            "cases":cases,"controls":controls()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--two-sts9",type=Path,
        default=Path(__file__).resolve().parent.parent/"spectral_downsets_steiner_triples"/"two9_certificates.json")
    parser.add_argument("--check",type=Path)
    parser.add_argument("--boundaries-only",action="store_true",
                        help="check only the two attributed nine-point rank/trade boundaries")
    args = parser.parse_args()
    result = nine_point_boundary_checks() if args.boundaries_only else run(args.two_sts9)
    if args.check:
        require(result == json.loads(args.check.read_text()), "saved kernel-trade results differ")
    print(json.dumps(result,indent=2,sort_keys=True))

"""Exact finite separation, dual identities, repaired blocks and controls.

Author six-downset-2, researcher. Same-author independent arithmetic and
decoding checks; independent peer review and formalization are unclaimed.
"""
import argparse
import copy
from fractions import Fraction as Q
import hashlib
import itertools
import json
from math import comb, isqrt
from pathlib import Path
from exact import bareiss_rank, both, schur_rank
from model import affine, blocks, choose, original, parameters, require

ROOT = Path(__file__).resolve().parent


def rational_strings(values):
    require(all(type(v) is str for v in values), "Rational strings required")
    return [Q(v) for v in values]


def digest(matrix):
    raw = json.dumps([[str(v) for v in row] for row in matrix],
                     separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def closed_complete(n, meta, values):
    """Independent direct two-row completion, without using RREF."""
    r, N, s = parameters(n)
    beta = [[Q(0)]*(r+1) for _ in range(r+1)]
    require(len(values) == len(meta["free_pairs"]), "Closed free-value count")
    for (a, b), value in zip(meta["free_pairs"], values):
        require(a >= 3 and b >= 3, "Closed decoder free face")
        beta[a][b] = beta[b][a] = value
    for a in range(3, r+1):
        b = n-a
        total = sum(beta[a][k]*choose(b, k) for k in range(3, r+1))
        star = sum(beta[a][k]*choose(b-1, k-1) for k in range(3, r+1))
        v = Q(b*(s-star)-(N-1-s-total), comb(b, 2))
        u = s-star-(b-1)*v
        beta[2][a] = beta[a][2] = v
        beta[1][a] = beta[a][1] = u
    total = sum(beta[2][a]*choose(n-2, a) for a in range(3, r+1))
    star = sum(beta[2][a]*choose(n-3, a-1) for a in range(3, r+1))
    beta[2][2] = Q((n-2)*(s-star)-(N-1-s-total), comb(n-2, 2))
    beta[1][2] = beta[2][1] = s-star-(n-3)*beta[2][2]
    beta[1][1] = s-sum(beta[1][a]*choose(n-2, a-1) for a in range(2, r+1))
    for a in range(1, r+1):
        require(sum(beta[a][b]*choose(n-a, b) for b in range(1, r+1)) == N-1-s,
                "Closed center residual")
        require(sum(beta[a][b]*choose(n-a-1, b-1) for b in range(1, r+1)) == s,
                "Direct excluding-point star residual")
    return beta


def decoded(n, meta, recover, values):
    beta = recover(values)
    require(beta == closed_complete(n, meta, values), "Independent completion agreement")
    return beta


def projection_gram(g, aa, j):
    d = len(g)
    if j >= 2:
        return [[Q(g[i]*int(i == k)) for k in range(d)] for i in range(d)]
    if j == 1:
        return [[Q(g[i]*int(i == k))-Q(g[i]*g[k], sum(g))
                 for k in range(d)] for i in range(d)]
    M = [[sum(g[a]*aa[a]**(i+k) for a in range(d)) for k in range(2)] for i in range(2)]
    det = M[0][0]*M[1][1]-M[0][1]**2
    require(det > 0, "Positive constant/cardinality moment determinant")
    Mi = [[Q(M[1][1], det), Q(-M[0][1], det)],
          [Q(-M[0][1], det), Q(M[0][0], det)]]
    return [[Q(g[i]*int(i == k))-g[i]*g[k]*sum(
        aa[i]**a*Mi[a][b]*aa[k]**b for a in range(2) for b in range(2))
        for k in range(d)] for i in range(d)]


def seed_fixture(doc):
    require(doc["n"] == 16 and doc["r"] == 14 and doc["N"] == 65519
            and doc["s"] == 32752, "Fixed sixteen-point seed domain")
    meta, recover = affine(16)
    require(doc["free_pairs"] == [list(v) for v in meta["free_pairs"]], "Free-pair census")
    require(doc["repair_endpoint"] == "1/22568", "Stated finite repair endpoint")
    require(doc["common_denominator"] == 1000000, "Declared common denominator")
    values = rational_strings(doc["free_values"])
    require(all(v.denominator <= 1000000 and 1000000 % v.denominator == 0 for v in values),
            "Compact common-denominator seed")
    return meta, decoded(16, meta, recover, values)


def seed_checks(doc):
    meta, beta = seed_fixture(doc)
    N, s, n = meta["N"], meta["s"], 16
    tstar = Q(doc["repair_endpoint"])
    records = []
    for t in (Q(0), tstar/2, tstar):
        rank_total, order_total, details = 0, 0, []
        for j, aa, g, K, U in blocks(n, beta, t):
            d = len(aa)
            require(all(v > 0 for v in g), "Positive complete-sector metric")
            require(j or all(sum(K[i][k]*aa[k] for k in range(d)) == 0 for i in range(d)),
                    "Degree-zero cardinality kernel")
            if j == 1 or j == 0 and not t:
                require(all(sum(row) == 0 for row in K), "Forced seed/point block kernel")
            expected = d-(2 if j == 0 and not t else 1 if j in (0, 1) else 0)
            lower = [[g[i]*v for v in row] for i, row in enumerate(K)]
            both(lower, expected)
            if not t:
                P = projection_gram(g, aa, j)
                both([[lower[i][k]-P[i][k] for k in range(d)] for i in range(d)])
            floor = Q(1, 4) if not t else Q(1, 8)
            upper = [[g[i]*(v-floor*int(i == k)) for k, v in enumerate(row)]
                     for i, row in enumerate(U)]
            both(upper)
            mult = comb(n, j)-(comb(n, j-1) if j else 0)
            rank_total += mult*expected
            order_total += mult*d
            details.append([j, d, mult, expected, digest(lower), digest(upper)])
        require(order_total == N-1 and rank_total == N-n-(2 if not t else 1),
                "Complete weighted original dimension and rank")
        records.append({"t": str(t), "complete_blocks": len(details),
            "full_lower_rank": rank_total+1, "full_upper_rank": N-1,
            "upper_nonzero_floor": str(floor), "block_data": details})
    return {"n": n, "r": 14, "N": N, "s": s, "affine_rank": meta["affine_rank"],
            "free_coordinates": len(meta["free_pairs"]), "seed_projected_lower_floor": "1",
            "parameters": records}


def upper_forms(n, beta):
    """Direct necessity forms: constants and one zero-sum point vector."""
    r, N, s = parameters(n)
    out = []
    for j in (0, 1):
        aa = list(range(1, r+1))
        g = [comb(n, a) if j == 0 else comb(n-2, a-1) for a in aa]
        scale = [isqrt(v) for v in g]
        A = [[Q(g[i], scale[i]*scale[k])*(
            (N-s)*int(i == k)+(-1)**(j+1)*beta[a][b]*choose(n-a-j, b-j))
            for k, b in enumerate(aa)] for i, a in enumerate(aa)]
        require(all(A[i][k] == A[k][i] for i in range(r) for k in range(r)),
                "Direct upper-form symmetry")
        out.append((scale, A))
    return out


def check_dual(doc):
    require(doc["n"] == 16 and doc["r"] == 14, "Fixed dual domain")
    meta, recover = affine(16)
    comp = [p for p in meta["free_pairs"] if sum(p) == 16]
    require(doc["comp_pairs"] == [list(p) for p in comp] and len(comp) == 6,
            "All six complement coordinates")
    require(len(doc["Y"]) == 2 and all(len(A) == 14 and all(len(row) == 14 for row in A)
                                     for A in doc["Y"]), "Dual dimensions")
    Y = [[rational_strings(row) for row in A] for A in doc["Y"]]
    floor = Q(doc["positive_definite_floor"])
    require(floor == Q(1, 1000000), "Dual floor convention")
    for A in Y:
        both(A, 14)
        both([[v-floor*int(i == k) for k, v in enumerate(row)] for i, row in enumerate(A)], 14)
    require(sum(Y[j][i][i] for j in range(2) for i in range(14)) == 1,
            "Dual trace normalization")

    def table(deltas):
        values = [Q(meta["s"])-deltas[comp.index(p)] if p in comp else Q(0)
                  for p in meta["free_pairs"]]
        return decoded(16, meta, recover, values)

    base_beta = table([Q(0)]*6)
    base = upper_forms(16, base_beta)
    require(doc["scales"] == [v[0] for v in base], "Rational metric scales")
    for j, aa, g, K, U in blocks(16, base_beta)[:2]:
        scale, direct = base[j]
        require(direct == [[Q(g[i]*v, scale[i]*scale[k]) for k, v in enumerate(row)]
                           for i, row in enumerate(U)], "Independent direct upper decoding")
    coefficients = []
    for k in range(6):
        d = [Q(0)]*6
        d[k] = Q(1)
        forms = upper_forms(16, table(d))
        value = sum(Y[j][i][l]*(forms[j][1][i][l]-base[j][1][i][l])
                    for j in range(2) for i in range(14) for l in range(14))
        require(value == 0, "Exact cancellation of an arbitrary complement weight")
        coefficients.append(str(value))
    constant = sum(Y[j][i][l]*base[j][1][i][l]
                   for j in range(2) for i in range(14) for l in range(14))
    require(constant == Q(doc["dual_constant"]) and constant < Q(-1, 4),
            "Strict negative dual constant")
    return {"orders": [14, 14], "positive_definite_floor": str(floor),
        "free_complements": 6, "zero_coefficients": coefficients,
        "constant": str(constant), "constant_below": "-1/4",
        "Y_hashes": [digest(A) for A in Y]}


def check_original(n, C, L, F):
    r, N, s = parameters(n)
    require(len(L) == N and all(sum(row) == N for row in L), "Original rows/empty loop")
    for i, A in enumerate([0]+F):
        for k, B in enumerate([0]+F):
            require(L[i][k] == L[k][i], "Original symmetry")
            if A & B:
                require(L[i][k] == s*int(i == k), "Original intersecting support")
    for point in range(n):
        x = [int(bool(A & (1 << point))) for A in F]
        require(sum(x) == s and all(sum(v*x[k] for k, v in enumerate(row)) == 0 for row in C),
                "Original exact star kernel")


def literal_baseline():
    n = 6
    meta, recover = affine(n)
    beta = decoded(n, meta, recover, [Q(24)])
    require([list(p) for p in meta["free_pairs"]] == [[3, 3]], "Published rank-four baseline coordinate")
    records = []
    for t in (Q(0), Q(1, 528)):
        F, C, L = original(n, beta, t)
        check_original(n, C, L, F)
        N = meta["N"]
        lower_rank = N-n-(not t)
        both(L, lower_rank)
        upper = [[Q(N*int(i == k))-v-Q(1, 8)*(int(i == k)-Q(1, N))
                  for k, v in enumerate(row)] for i, row in enumerate(L)]
        both(upper, N-1)
        columns = 0
        for j, aa, g, K, U in blocks(n, beta, t)[:2]:
            for bindex, b in enumerate(aa):
                vector = [Q(int(A.bit_count() == b))*(
                    1 if j == 0 else int(bool(A & 1))-int(bool(A & 2))) for A in F]
                image = [sum(v*vector[k] for k, v in enumerate(row)) for row in C]
                predicted = [K[aa.index(A.bit_count())][bindex]*(
                    1 if j == 0 else int(bool(A & 1))-int(bool(A & 2))) for A in F]
                require(image == predicted, "Definition-level constant/point action")
                columns += 1
        records.append({"t": str(t), "N": N, "lower_rank": int(lower_rank),
                        "upper_gap_rank": N-1, "action_columns": columns,
                        "full_L_sha256": digest(L)})
    return records


def determinant_small(A):
    d = len(A)
    total = 0
    for permutation in itertools.permutations(range(d)):
        sign = (-1)**sum(permutation[i] > permutation[k] for i in range(d) for k in range(i+1, d))
        value = sign
        for i in range(d):
            value *= A[i][permutation[i]]
        total += value
    return total


def rejected(operation):
    try:
        operation()
    except ValueError:
        return True
    return False


def arithmetic_audit():
    positive = 0
    for values in itertools.product((-1, 0, 1), repeat=6):
        A = [[0]*3 for _ in range(3)]
        for (i, k), v in zip(((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)), values):
            A[i][k] = A[k][i] = v
        criterion = all(determinant_small([[A[i][k] for k in subset] for i in subset]) >= 0
                        for size in (1, 2, 3) for subset in itertools.combinations(range(3), size))
        outcomes = [not rejected(lambda method=method: method(A))
                    for method in (bareiss_rank, schur_rank)]
        require(outcomes == [criterion, criterion], "Separate all-principal-minor PSD audits")
        positive += criterion
    require(positive == 24, "Ternary audit count")
    return {"all_symmetric_ternary_3x3": 729, "PSD": positive}


def controls(seed, dual):
    wrong = copy.deepcopy(seed)
    wrong["free_values"].pop()
    require(rejected(lambda: seed_fixture(wrong)), "Missing seed control")
    cases = ["missing seed coordinate"]
    wrong = copy.deepcopy(seed)
    wrong["free_values"][0] = 0.5
    require(rejected(lambda: seed_fixture(wrong)), "Float seed control")
    cases.append("floating seed coordinate")
    wrong = copy.deepcopy(seed)
    wrong["free_values"][0] = "1000000000"
    require(rejected(lambda: seed_checks(wrong)), "False lower certificate control")
    cases.append("damaged lower seed")
    wrong = copy.deepcopy(dual)
    wrong["Y"][0][0][0] = "-1"
    require(rejected(lambda: check_dual(wrong)), "False dual PSD control")
    cases.append("negative dual diagonal")
    wrong = copy.deepcopy(dual)
    value = str(Q(wrong["Y"][0][0][1])+Q(1, 10000))
    wrong["Y"][0][0][1] = wrong["Y"][0][1][0] = value
    require(rejected(lambda: check_dual(wrong)), "Changed dual identity control")
    cases.append("changed dual off-diagonal")
    wrong = copy.deepcopy(dual)
    wrong["dual_constant"] = "1"
    require(rejected(lambda: check_dual(wrong)), "False dual constant control")
    cases.append("false declared dual constant")
    meta, recover = affine(6)
    beta = recover([Q(24)])
    F, C, L = original(6, beta)
    L[0][0] += 1
    require(rejected(lambda: check_original(6, C, L, F)), "Empty-loop corruption control")
    cases.append("changed original empty loop")
    require(rejected(lambda: original(16, seed_fixture(seed)[1])), "Full-size allocation guard")
    cases.append("forbidden large literal allocation")
    return cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    seed = json.loads((ROOT/"seed.json").read_text())
    dual = json.loads((ROOT/"dual.json").read_text())
    result = {"agent": "six-downset-2", "role": "researcher",
        "status": "Exact finite proof checks; ordinary bridges unformalized; independent review unclaimed",
        "seed": seed_checks(seed), "dual": check_dual(dual),
        "literal_published_rank_four_baseline": literal_baseline(),
        "arithmetic_audit": arithmetic_audit(), "rejected_controls": controls(seed, dual),
        "seed_sha256": hashlib.sha256((ROOT/"seed.json").read_bytes()).hexdigest(),
        "dual_sha256": hashlib.sha256((ROOT/"dual.json").read_bytes()).hexdigest(),
        "no_literal_n16_matrix": True, "arithmetic": "integers and fractions.Fraction"}
    body = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.check:
        require(body == args.check.read_text(), "Frozen expected result mismatch")
    if args.output:
        args.output.write_text(body)
    print(json.dumps({"ok": True, "result_sha256": hashlib.sha256(body.encode()).hexdigest(),
        "complete_n16_blocks": 27, "dual_blocks": 2, "literal_order": 57,
        "controls": len(result["rejected_controls"])}))


if __name__ == "__main__":
    main()

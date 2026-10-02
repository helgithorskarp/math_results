"""Exact finite controls for an ordinary all-n reduction theorem.

six-downset-2, researcher. No finite coverage or numerical solver is the
universal proof. The two full seeds are credited9556/9592 validation only.
"""
import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from math import comb
from pathlib import Path

import exact
import model
from reduction import (complete_stars, dimensions, domain, need, parent,
                       quotient, supported, table, transfer, validate)

ROOT = Path(__file__).resolve().parent


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"),
                                    default=str).encode()).hexdigest()


def reference_agreement(n, beta):
    positions = 0
    for j, aa, g, K, U in model.blocks(n, beta):
        need((aa, g, K, U) == quotient(n, j, beta),
             "Every complete entry agrees with unchanged prior model")
        for matrix in [K, U]:
            need(all(g[i]*matrix[i][t] == g[t]*matrix[t][i]
                     for i in range(len(g)) for t in range(len(g))),
                 "Entire physical form is symmetric")
        positions += 2*len(g)**2
    return positions


def basis_controls():
    """Entire rational coordinate bases at each stated finite (n,k)."""
    records = []
    for n in range(6, 15):
        d = n//2
        for k in sorted({1, 2, 3, d, n-2}):
            data = dimensions(n, k)
            active = [p for p in supported(n) if min(p) <= k or sum(p) == n]
            z = table(n)
            zero = transfer(n, k, z)
            positions = zero["positions"]
            for a, b in active:
                beta = table(n)
                beta[a][b] = beta[b][a] = Q(1)
                positions += transfer(n, k, beta)["positions"]
            # A signed mixture controls actual rational arithmetic, not just bits.
            mix = table(n)
            for i, (a, b) in enumerate(active):
                mix[a][b] = mix[b][a] = Q((-1)**i*(i+1), 2*i+3)
            positions += transfer(n, k, mix)["positions"]
            reference = reference_agreement(n, mix)
            records.append({"n": n, "k": k, "q": data["q"],
                            "supported_active_basis_vectors": len(active),
                            "transfer_positions": positions,
                            "complete_reference_positions": reference,
                            "omitted_degree_parent_order": zero["omitted_degree_parent_order"],
                            "middle_parities": zero["middle_parities"]})
    return records


def fixture_checks():
    records = []
    fixtures = json.loads((ROOT/"fixtures.json").read_text())
    need([(z["n"], z["proper_support_cutoff"], z["upper_floor"]) for z in fixtures]
         == [(24, 6, "1/64"), (32, 8, "1/1024")], "Two unchanged defining fixtures")
    for z in fixtures:
        n, k = z["n"], z["proper_support_cutoff"]
        r, N, s, d, q = domain(n, k)
        eps = Q(z["upper_floor"])
        beta = complete_stars(n, [Q(v) for v in z["free_values"]])
        validate(n, k, beta)
        direct_positions = reference_agreement(n, beta)
        identity = transfer(n, k, beta)
        sector_data = []
        dimension, rank = 0, 0
        for j in range(d+1):
            aa, g, K, U = quotient(n, j, beta)
            order = len(aa)
            lower = [[g[i]*v for v in row] for i, row in enumerate(K)]
            upper = [[g[i]*(v-eps*int(i == t)) for t, v in enumerate(row)]
                     for i, row in enumerate(U)]
            expected_rank = order-int(j <= 1)
            exact.both(lower, expected_rank)
            exact.both(upper, order)
            if j <= 1:
                kernel = aa if j == 0 else [1]*order
                need(all(sum(K[i][t]*kernel[t] for t in range(order)) == 0
                         for i in range(order)), "Exactly required point-star kernels")
            mult = comb(n, j)-(comb(n, j-1) if j else 0)
            dimension += mult*order
            rank += mult*expected_rank
            sector_data.append([j, order, digest(lower), digest(upper)])
        need(dimension == N-1 and rank == N-n-1, "Whole dimensions and greatest ranks")
        # The derived automatic omitted cap floor uses ONLY lower positivity.
        auto_positions = 0
        for j in range(min(k, d)+1, d+1):
            aa, g, K, U = quotient(n, j, beta)
            floor = [[g[i]*(v-Q(n-1)*int(i == t)) for t, v in enumerate(row)]
                     for i, row in enumerate(U)]
            exact.both(floor)
            auto_positions += len(aa)**2
        records.append({"credited": 9556 if n == 24 else 9592,
                        "dimensions": dimensions(n, k), "upper_floor": str(eps),
                        "complete_reference_positions": direct_positions,
                        "transfer": identity, "full_forms_checked": 2*(d+1),
                        "automatic_upper_floor": n-1,
                        "automatic_upper_floor_positions": auto_positions,
                        "whole_lower_rank": rank+1,
                        "complete_forms_sha256": digest(sector_data)})
    return records


def ordinary_control():
    """Credited8106 all-n reference instantiated at an odd order; cap fails."""
    n, k = 11, 1
    r, N, s, d, q = domain(n, k)
    free = [p for p in supported(n) if p[0] >= 2]
    beta = complete_stars(n, [Q(s-1 if sum(p) == n else 0) for p in free])
    validate(n, k, beta)
    need(beta[1][1] == s-(2**(n-2)-2)
         and all(beta[1][a] == 1 for a in range(2, r+1)), "Ordinary8106 reference")
    identity = transfer(n, k, beta)
    rank = 0
    for j in range(d+1):
        aa, g, K, U = quotient(n, j, beta)
        expected = len(aa)-int(j <= 1)
        exact.both([[g[i]*v for v in row] for i, row in enumerate(K)], expected)
        rank += (comb(n, j)-(comb(n, j-1) if j else 0))*expected
        if j > k:
            exact.both([[g[i]*(v-Q(n-1)*int(i == t)) for t, v in enumerate(row)]
                        for i, row in enumerate(U)])
    aa, g, K, U = quotient(n, 0, beta)
    need(U[0][0] < 0 and rank+1 == N-n,
         "Full degree-zero cap still necessary; ordinary greatest lower rank")
    return {"credited": 8106, "n": n, "k": k, "q": q,
            "transfer": identity, "upper0_diagonal": str(U[0][0]),
            "ordinary_lower_rank": rank+1, "not_a_capped_seed": True}


def rejected(job):
    try:
        job()
    except (ValueError, TypeError, IndexError, ZeroDivisionError):
        return True
    return False


def controls():
    cases = []
    for name, job in [
        ("n below domain", lambda: domain(5, 1)),
        ("noninteger order", lambda: domain(8.0, 1)),
        ("cutoff zero", lambda: domain(8, 0)),
        ("cutoff outside layers", lambda: domain(8, 7)),
        ("negative binomial upper", lambda: quotient(8, 5, table(8))),
        ("missing row", lambda: transfer(8, 1, table(8)[:-1]))]:
        need(rejected(job), "Reject "+name)
        cases.append(name)
    for name, n, k, a, b, value in [
        ("floating coordinate", 8, 1, 4, 4, 0.5),
        ("asymmetric coordinate", 9, 1, 3, 6, Q(1)),
        ("unsupported coordinate", 8, 1, 5, 5, Q(1)),
        ("forbidden proper coordinate", 10, 2, 3, 3, Q(1))]:
        z = table(n);z[a][b] = value
        if name != "asymmetric coordinate":
            z[b][a] = value
        need(rejected(lambda: transfer(n, k, z)), "Reject "+name)
        cases.append(name)
    # Sign/parity controls are direct counterexamples to the damaged identity.
    for name, n, j, a, b in [
        ("odd order sign omitted", 9, 3, 3, 6),
        ("even middle wrong parity", 10, 5, 5, 5)]:
        beta = table(n);beta[a][b] = beta[b][a] = Q(1)
        aa, g, K, U = quotient(n, j, beta)
        bb, gg, low, low_u = quotient(n, 2, beta)
        need(K[aa.index(a)][aa.index(b)] != low[bb.index(a)][bb.index(b)],
             "Damaged parent identity differs exactly")
        cases.append(name)
    # Positive low2 alone does not bound the other even middle parity.
    n = 10;r, N, s, d, q = domain(n, 1)
    beta = table(n);beta[5][5] = Q(2*s)
    aa, g, K, U = quotient(n, 2, beta)
    exact.both([[g[i]*v for v in row] for i, row in enumerate(K)])
    aa, g, K, U = quotient(n, 3, beta)
    need(K[aa.index(5)][aa.index(5)] == -s,
         "Third degree catches opposite middle parity")
    need(rejected(lambda: exact.both([[g[i]*v for v in row]
                                     for i, row in enumerate(K)])),
         "Actual opposite middle form is indefinite")
    cases.append("missing even third-degree middle inequality")
    need(rejected(lambda: exact.both([[Q(1), Q(2)], [Q(2), Q(1)]])),
         "Independent PSD engines reject an indefinite form")
    cases.append("indefinite form")
    return cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    record = {"agent": "six-downset-2", "role": "researcher",
              "status": "Finite exact controls; all-n ordinary proof unformalized",
              "coordinate_basis_controls": basis_controls(),
              "credited_full_fixtures": fixture_checks(),
              "credited_ordinary_odd_control": ordinary_control(),
              "dimensions_n40_S10": dimensions(40, 10),
              "semantic_damage_controls": controls()}
    if args.check:
        need(json.loads(args.check.read_text()) == record, "Whole deterministic record match")
    if args.output:
        args.output.write_text(json.dumps(record, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"ok": True, "record_sha256": digest(record),
                      "basis_cases": len(record["coordinate_basis_controls"]),
                      "full_prior_forms": sum(z["full_forms_checked"]
                                              for z in record["credited_full_fixtures"]),
                      "controls": len(record["semantic_damage_controls"])}))


if __name__ == "__main__":
    main()

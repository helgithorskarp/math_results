"""Exact author controls. Every check remains active under python -O."""
import argparse
import hashlib
import json
from pathlib import Path

from budget import (covering_hypotheses, definition_budget, divisors,
                    p3_budget, pq_budget, physical_capacity, prime, radical, require)

HERE = Path(__file__).resolve().parent
COVER_SHA256 = "f3b7ab8112f2fdba3ab32ea992f2380c43c404e8b54c8abdd71c839a9f5424e3"


def identity_controls():
    evidence = []
    families = [("pq", p, q) for p, q in [(2, 3), (3, 5), (5, 7)]]
    families += [("p3", p, None) for p in [2, 3]]
    for kind, p, q in families:
        C = p*q if kind == "pq" else p**3
        periods = (1, p, q, C) if kind == "pq" else (1, p, p*p, C)
        point_weight = ((q if kind == "pq" else p*p) + 1) // 2
        fixtures = [("zero", [[0]*C]), ("constant", [[1]*C]),
                    ("single_point", [[int(z == C-1) for z in range(C)]]),
                    ("three_labels", [[(17*t + 11*z + z*z + 3) % 8 for z in range(C)] for t in range(3)]),
                    ("two_pairs", [[int(z % p == 0) for z in range(C)],
                                   [point_weight * int(z == 1) for z in range(C)]])]
        for name, weights in fixtures:
            closed = pq_budget(p, q, weights, True) if kind == "pq" else p3_budget(p, weights, True)
            direct = definition_budget(periods, weights, True)
            for key in ["budget", "all_one_group", "phase_table_sha256", "table"]:
                require(closed[key] == direct[key], f"Identity mismatch: {kind,p,q,name,key}")
            if name == "two_pairs":
                require(closed["two_pairs"] > closed["all_one_group"], "Independent-label term is essential")
            if name == "constant":
                require(closed["all_one_group"] > closed["two_pairs"], "All-one term is essential")
            evidence.append({"kind": kind, "p": p, "q": q, "fixture": name,
                             **{k: v for k, v in closed.items() if k != "table"},
                             "phase_partition_rows": direct["phase_partition_rows"]})
    return evidence


def local_period_controls():
    footprints = 0
    for B in [4, 12, 18, 36, 72]:
        rho, T = radical(B), B // radical(B)
        for m in divisors(B)[:-1]:
            ell = next(p for p in divisors(rho) if prime(p) and (B // p) % m == 0)
            for q in range(T):
                for a in range(m):
                    row = [int((q + T*j) % m == a) for j in range(rho)]
                    require(all(row[j] == row[(j + rho//ell) % rho] for j in range(rho)),
                            "False proper local-period assertion")
                    footprints += 1
    return footprints


def genuine_controls():
    cover = [(2, 0), (3, 0), (4, 1), (6, 1), (12, 11)]
    records = []
    for N, B, b, periods in [(60, 4, 2, (1, 3, 5, 15)), (216, 8, 4, (1, 3, 9, 27))]:
        Q = b * periods[-1]
        for shift in range(3):
            actual = [(n, (a+shift) % n) for n, a in cover]
            require(all(any(x % n == a for n, a in actual) for x in range(N)), "Invalid positive covering")
            anchors = actual[:2]
            for case in range(3):
                u = [0 if any(x % n == a for n, a in anchors) else (x*x + 3*x + 5*case + shift) % 7
                     for x in range(N)]
                base = [0 if any(r % n == a for n, a in anchors) else (r*r + 7*r + case + 2) % 11
                        for r in range(Q)]
                result = physical_capacity(N, B, b, periods, anchors, u, base, 2)
                require(result["gap"] <= 0, "False exclusion of a genuine covering")
                if case == 0:
                    ordinary = physical_capacity(N, B, b, periods, anchors, u, [0]*Q, 2)
                    require(ordinary["mixed_capacity"] == ordinary["ordinary_capacity"], "v=0 must recover ordinary bound")
                records.append({"shift": shift, "case": case, **result})
    return records


def strengthening_controls():
    records = []
    for N, B, b in [(10080, 288, 48), (15120, 432, 72)]:
        Q = b * 35
        u = [int(x == 1) for x in range(N)]
        base = [int(x % 8 != 0) for x in range(Q)]
        result = physical_capacity(N, B, b, (1, 5, 7, 35), [(8, 0)], u, base)
        require(result["capacity_saving"] == 23 and result["gap"] < 0, "Incorrect strengthening fixture")
        require(result["partition_budget"] == 25, "Incorrect physical block budget")
        require(u[1] + base[1] != u[Q+1] + base[1], "Total fixture is already Q-periodic")
        records.append(result)
    return records


def malformed_controls():
    calls = [lambda: pq_budget(4, 7, [[0]*28]), lambda: pq_budget(3, 3, [[0]*9]),
             lambda: pq_budget(3, 5, [[-1]*15]), lambda: pq_budget(3, 5, [[True]*15]),
             lambda: pq_budget(3, 5, [[0]*14]), lambda: p3_budget(4, [[0]*64]),
             lambda: p3_budget(3, []), lambda: definition_budget((1, 3, 5, 35), [[0]*35])]
    bad_parameters = [(180, 12, 2, 15, [], 2), (60, 4, 4, 15, [], 2),
                      (60, 4, 2, 15, [(2, 2)], 2), (60, 4, 2, 15, [(2, 0), (2, 1)], 2),
                      (60, 4, 2, 15, [(4, 1)], 2), (60, 4, 2, 15, [(7, 0)], 2),
                      (60, 4, 2, 15, [], 8), (60, 4, True, 15, [], 2)]
    calls += [lambda args=args: covering_hypotheses(*args) for args in bad_parameters]
    for u in [[-1]*60, [True]*60, [0]*59, [int(x == 0) for x in range(60)]]:
        calls.append(lambda u=u: physical_capacity(60, 4, 2, (1, 3, 5, 15), [(2, 0)], u, [0]*30, 2))
    rejected = 0
    for call in calls:
        try:
            call()
        except ValueError:
            rejected += 1
        else:
            raise ValueError("Malformed input accepted")
    return rejected


def published_cover_control(path):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == COVER_SHA256, "External covering digest mismatch")
    source = json.loads(raw)
    require(source["lcm"] == 20160 and source["format_version"] == 1, "External covering format")
    cover = [(n, a) for a, n in source["congruences"]]
    require(len(cover) == len({n for n, a in cover}) == 77 and min(n for n, a in cover) == 8,
            "External distinctness/minimum")
    from math import gcd, lcm
    require(lcm(*(n for n, a in cover)) == 20160, "External actual LCM")
    require(all(0 <= a < n and 20160 % n == 0 for n, a in cover), "External phase/modulus")
    require(all(any(x % n == a for n, a in cover) for x in range(20160)), "External covering fails")
    N, B, b, C = 20160, 576, 96, 35
    Q = b*C
    anchors = cover[:3]
    base = [0 if any(r % gcd(n, Q) == a % gcd(n, Q) for n, a in anchors)
            else 1 + (r % C) % 3 for r in range(Q)]
    available = [x for x in range(N) if not any(x % n == a for n, a in anchors)]
    u = [0]*N
    for j, x in enumerate(available[:10]):
        u[x] = j+1
    result = physical_capacity(N, B, b, (1, 5, 7, 35), anchors, u, base)
    require(result["gap"] <= 0, "Mixed inequality excludes the published covering")
    return {"external_sha256": COVER_SHA256, "classes": len(cover), "minimum": 8,
            "actual_lcm": 20160, "prefix": [[n, a] for n, a in anchors], **result}


def run(cover_path):
    identities = identity_controls()
    genuine = genuine_controls()
    return {"author": "six-covering-2", "role": "researcher", "all_passed": True,
            "scope": "Mixed-weight and four-resource budget controls; no new numerical L_min(8) bound",
            "identity_fixtures": identities,
            "phase_partition_rows_checked": sum(r["phase_partition_rows"] for r in identities),
            "all_one_phase_table_rows_compared": sum(r["phase_table_rows"] for r in identities),
            "proper_local_period_footprints_checked": local_period_controls(),
            "malformed_inputs_rejected": malformed_controls(), "genuine_cover_weight_cases": genuine,
            "nonperiodic_strengthening": strengthening_controls(),
            "published_20160_positive_control": published_cover_control(cover_path)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cover", type=Path, default=HERE.parent / "distinct_covering_min8_20160" / "cover.json")
    args = parser.parse_args()
    result = run(args.cover)
    expected = json.loads((HERE / "expected.json").read_text())
    require(result == expected, "Fresh exact result differs from expected evidence")
    print(json.dumps({"all_passed": True,
                      "phase_partition_rows_checked": result["phase_partition_rows_checked"],
                      "all_one_phase_table_rows_compared": result["all_one_phase_table_rows_compared"],
                      "genuine_cover_weight_cases": len(result["genuine_cover_weight_cases"]),
                      "nonperiodic_capacity_savings": [r["capacity_saving"] for r in result["nonperiodic_strengthening"]],
                      "published_20160_cover_checked": True, "scope": result["scope"]}), flush=True)

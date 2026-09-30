"""Independent exact review by six-reviewer-5; no target code imports."""
from hashlib import sha256
from itertools import product
from math import gcd, prod
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def radical(n):
    return prod(p for p in divisors(n)[1:]
                if all(p % d for d in range(2, p)))


def coset_tables(columns, C):
    # Direct arithmetic-progressions, rather than residue-bin accumulation.
    return {d: [[sum(column[a::d]) for a in range(d)]
                for column in columns] for d in divisors(C)[1:]}


def budgets(columns, C, p, q):
    require(p != q and C % p == C % q == 0, "Two distinct cofactor divisors required")
    tables = coset_tables(columns, C)
    H = {d: [max(row) for row in rows] for d, rows in tables.items()}
    M = {d: max(row) for d, row in H.items()}
    old, corrected, pair_cases = [], [], []
    for t, column in enumerate(columns):
        # Four possibilities for whether each designated resource shares
        # the block of the coarsest top class. Both-in retains the overlap.
        both = max(2 * tables[p][t][a] + 2 * tables[q][t][r]
                   - sum(column[z] for z in range(a, C, p) if z % q == r)
                   for a in range(p) for r in range(q))
        cases = [M[p] + M[q], 2 * H[p][t] + M[q],
                 M[p] + 2 * H[q][t], both]
        old.append(sum(max(M[d], 2 * H[d][t]) for d in H))
        corrected.append(max(cases) + sum(max(M[d], 2 * H[d][t])
                                         for d in H if d not in (p, q)))
        require(corrected[-1] <= old[-1], "Pair correction exceeds old relaxation")
        pair_cases.append(cases)
    return {"H": H, "M": M, "old_by_label": old,
            "pair_by_label": corrected, "pair_cases_by_label": pair_cases,
            "G": max(old), "G_pair": max(corrected)}


def check_certificate():
    raw = (HERE / "input.json").read_bytes()
    require(sha256(raw).hexdigest() ==
            "bf4d3deb56fa173a875a816aef6831a6aebff54b8bfdb441898137a5b96e1b96",
            "Target certificate bytes changed")
    c = json.loads(raw)
    N, B, C, b, Q = (c[k] for k in ("N", "B", "C", "b", "weight_period"))
    require((N, B, C, b, Q) == (43200, 64, 675, 16, 720), "Unexpected target")
    require(gcd(B, C) == 1 and (B // radical(B)) % b == 0,
            "Primitive-block hypotheses")
    require(N == B * C and N % Q == (b * C) % Q == 0, "Weight periods")
    axes = c["axes"]
    require(prod(axes) == Q and all(gcd(a, r) == 1 for i, a in enumerate(axes)
                                   for r in axes[:i]), "Invalid CRT axes")
    for box in c["boxes"]:
        require(len(box) == 4 and type(box[-1]) is int and box[-1] > 0,
                "Malformed box")
        require(all(type(mask) is int and 0 < mask < 2 ** axis
                    for mask, axis in zip(box[:-1], axes)), "Invalid mask")
    # Decode by literal ordinary residues. No CRT inverse or author decoder.
    base = []
    for x in range(Q):
        hits = [box[-1] for box in c["boxes"]
                if all((mask // 2 ** (x % axis)) % 2
                       for mask, axis in zip(box[:-1], axes))]
        require(len(hits) <= 1, "Overlapping certificate boxes")
        base.append(sum(hits))
    require(digest(base) == c["base_weight_sha256"], "Base weight hash")
    weight = [base[x % Q] for x in range(N)]
    anchors = [(8, 0), (9, 0), (10, 5), (12, 9), (15, 10)]
    require(c["anchors"] == [list(row) for row in anchors], "Target prefix changed")
    require(all(sum(weight[a::n]) == 0 for n, a in anchors), "Weight meets prefix")
    resources = [n for n in divisors(N) if n >= 8 and n not in dict(anchors)]
    top = {B * d for d in divisors(C)}
    require(top <= set(resources), "Top resource unavailable")
    # Every actual phase of every resource, directly as a finite progression.
    phases = {n: [sum(weight[a::n]) for a in range(n)] for n in resources}
    capacities = {n: max(sums) for n, sums in phases.items()}
    require(digest(capacities) ==
            "5721cf3e89319fdd43cf53606fdfd6efd0922fc91ca19c9846613406dad32c1c",
            "All 73 actual maxima differ from the target's pinned digest")
    # Populate columns by all b*C ordinary residues, without CRT inversion.
    columns = [[None] * C for _ in range(b)]
    for x in range(b * C):
        t, z = x % b, x % C
        require(columns[t][z] is None, "CRT coordinate repeated")
        columns[t][z] = base[x % Q]
    require(all(v is not None for col in columns for v in col), "Missing CRT coordinate")
    tables = coset_tables(columns, C)
    phase_checks = 0
    for d in divisors(C)[1:]:
        for a, total in enumerate(phases[B * d]):
            require(total == tables[d][a % b][a % d], "Physical top phase mismatch")
            phase_checks += 1
    result = budgets(columns, C, 3, 5)
    outside = sum(capacities[n] for n in resources if n not in top)
    demand = sum(weight)
    require((demand, outside, result["G"], result["G_pair"]) ==
            (597000, 573780, 23150, 22295), "Certificate totals")
    require(demand - outside - result["G_pair"] == 925, "Strengthened gap")
    ordinary = sum(capacities.values())
    fibre = ordinary - capacities[1728] + capacities[8640] + capacities[N]
    require((ordinary, fibre) == (597430, 597075), "Same-vector comparison")
    return {"input_sha256": sha256(raw).hexdigest(), "base_weight_sha256": digest(base),
            "physical_demand": demand, "outside_capacity": outside,
            "ordinary_capacity": ordinary, "old_fibre_capacity": fibre,
            "original_capacity": outside + result["G"], "original_gap": 70,
            "pair_capacity": outside + result["G_pair"], "pair_gap": 925,
            "resource_count": len(resources), "outside_resource_count": len(resources) - len(top),
            "all_phase_checks": sum(resources), "top_phase_identity_checks": phase_checks,
            "actual_phase_maxima": capacities, "budget": result}


def small_complete_controls():
    # B=4, C=15, b=T=2. All actual block-label and cofactor-phase tuples.
    C, b = 15, 2
    ds = divisors(C)
    outputs = []
    for seed in range(3):
        columns = [[0 if seed == 0 else (z * z + 7 * t + 3 * seed) % 6
                    for z in range(C)] for t in range(b)]
        bounds = budgets(columns, C, 3, 5)
        maximum, tuples = 0, 0
        for labels in product(range(b), repeat=len(ds)):
            for residues in product(*(range(d) for d in ds)):
                charge = 0
                for label in range(b):
                    for z in range(C):
                        k = sum(labels[i] == label and z % d == residues[i]
                                for i, d in enumerate(ds))
                        if k >= 2:
                            charge += k * columns[label][z]
                maximum = max(maximum, charge)
                tuples += 1
        require(maximum <= bounds["G_pair"] <= bounds["G"], "Finite charge control")
        outputs.append({"seed": seed, "complete_actual_charge_maximum": maximum,
                        "G_pair": bounds["G_pair"], "G": bounds["G"], "tuples": tuples})
    return outputs


def essential_period_counterexample():
    # A genuine cover, lifting the classical 12-period minimum-two example.
    N, B, C, b = 60, 12, 5, 12
    prescribed = [(2, 0), (3, 0), (4, 1), (6, 1)]
    cover = prescribed + [(12, 11)]
    require(all(any(x % n == a for n, a in cover) for x in range(N)), "Positive cover")
    weight = [int(x % B == 11) for x in range(N)]
    require(all(sum(weight[a::n]) == 0 for n, a in prescribed), "Supported counterexample")
    columns = [[int(t == 11)] * C for t in range(b)]
    H5 = [max(col) for col in columns]
    G = max(max(max(H5), 2 * h) for h in H5)
    require(gcd(B, C) == 1 and (B // radical(B)) % b != 0, "Exactly failed period condition")
    require((sum(weight), G) == (5, 2), "Counterexample arithmetic")
    return {"N": N, "B": B, "C": C, "b": b, "T": B // radical(B),
            "prescribed": prescribed, "completion": [(12, 11)], "R": [12, 60],
            "demand": sum(weight), "outside_capacity": 0, "invalid_G": G,
            "conclusion": "Dropping b|T would falsely exclude this genuine covering"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true")
    args = parser.parse_args()
    result = {"reviewer": "six-reviewer-5", "role": "reviewer",
              "scope": "Independent fixed-prefix certificate and proved pair correction",
              "certificate": check_certificate(), "complete_controls": small_complete_controls(),
              "essential_period_counterexample": essential_period_counterexample()}
    rendered = json.dumps(result, indent=2) + "\n"
    if args.record:
        (HERE / "expected.json").write_text(rendered)
    else:
        require(json.loads((HERE / "expected.json").read_text()) == json.loads(rendered),
                "Independent evidence changed")
    print(rendered, end="")


if __name__ == "__main__":
    main()

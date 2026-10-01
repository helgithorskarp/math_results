"""Exact evidence for a prescribed-prefix LCM optimum; Python 3.11+ stdlib.
Actual author six-covering-1, researcher. See proof.md for the reduction.
"""
import argparse
from collections import Counter
import copy
import hashlib
import json
import math
from pathlib import Path
import struct


def require(ok, message):
    if not ok:
        raise ValueError(message)


def integer(x):
    return type(x) is int


def validate_fixed(rows, period):
    require(isinstance(rows, list) and bool(rows), "missing fixed classes")
    require(all(isinstance(row, list) and len(row) == 2
                and all(integer(x) for x in row) for row in rows), "malformed fixed classes")
    require(all(8 <= m <= period and period % m == 0 and 0 <= a < m for a, m in rows),
            "ineligible fixed class")
    require([m for a, m in rows] == sorted({m for a, m in rows}), "duplicate or unsorted fixed modulus")
    require([m for a, m in rows] == [m for m in range(8, 80) if period % m == 0],
            "wrong prescribed modulus set")
    require(min(m for a, m in rows) == 8 and math.lcm(*(m for a, m in rows)) == period,
            "wrong prefix minimum or LCM")


def pair_values(weight, period, m, n):
    hm = [0] * m
    hn = [0] * n
    overlap = {}
    for x, w in enumerate(weight):
        hm[x % m] += w
        hn[x % n] += w
        if w:
            k = (x % m, x % n)
            overlap[k] = overlap.get(k, 0) + w
    return [hm[a] + hn[b] - overlap.get((a, b), 0)
            for a in range(m) for b in range(n)]


def pair_digest(values):
    h = hashlib.sha256()
    for v in values:
        require(0 <= v < 2**64, "pair digest range")
        h.update(struct.pack("<Q", v))
    return h.hexdigest()


def certificate_check(data):
    require(integer(data.get("schema")) and data.get("schema") == 1
            and integer(data.get("period")) and data.get("period") == 15120, "wrong integer scope")
    period = data["period"]
    fixed = data["fixed"]
    validate_fixed(fixed, period)
    covered = bytearray(period)
    for a, m in fixed:
        for x in range(a, period, m):
            covered[x] = 1
    residual = [x for x in range(period) if not covered[x]]
    weights = data["weights"]
    require(isinstance(weights, list) and bool(weights), "empty weights")
    require(all(isinstance(row, list) and len(row) == 2 and all(integer(v) for v in row)
                and 0 <= row[0] < period and row[1] > 0 for row in weights), "bad weight row")
    require([x for x, w in weights] == sorted({x for x, w in weights}), "duplicate or unsorted weight point")
    require(all(not covered[x] for x, w in weights), "weight on a fixed-covered point")
    weight = [0] * period
    for x, w in weights:
        weight[x] = w
    used = {m for a, m in fixed}
    free = [m for m in range(8, period + 1) if period % m == 0 and m not in used]
    pair = data["pair"]
    require(pair == [112, 144] and set(pair) <= set(free), "wrong free resource pair")
    caps = {}
    for m in free:
        h = [0] * m
        for x, w in weights:
            h[x % m] += w
        caps[m] = max(h)
    values = pair_values(weight, period, *pair)
    demand = sum(weight)
    individual = sum(caps.values())
    joint = max(values)
    capacity = sum(v for m, v in caps.items() if m not in pair) + joint
    gap = demand - capacity
    require(gap > 0, "no strict paired bound")
    return dict(period=period, fixed_classes=len(fixed), fixed_lcm=math.lcm(*(m for a, m in fixed)),
                residual_points=len(residual), free_resources=len(free), weight_support=len(weights),
                maximum_weight=max(weight), demand=demand, individual_capacity=individual,
                pair=pair, pair_phases=len(values), individual_pair_capacity=sum(caps[m] for m in pair),
                joint_pair_capacity=joint, grouped_capacity=capacity, strict_gap=gap,
                minimum_holes=(gap + max(weight) - 1) // max(weight),
                resource_capacities=[[m, caps[m]] for m in free],
                all_pair_values_sha256=pair_digest(values))


def fractional_check(data, fixed):
    require(integer(data.get("schema")) and data.get("schema") == 1
            and integer(data.get("period")) and data.get("period") == 15120 and data.get("fixed") == fixed,
            "wrong fractional scope")
    validate_fixed(data["fixed"], data["period"])
    period = data["period"]
    denominator = data["denominator"]
    require(integer(denominator) and denominator > 0, "bad fractional denominator")
    free = {m for m in range(8, period + 1) if period % m == 0} - {m for a, m in fixed}
    rows = data["phase_masses"]
    require(isinstance(rows, list) and bool(rows), "no fractional phases")
    require(all(isinstance(row, list) and len(row) == 3 and all(integer(v) for v in row)
                and row[0] in free and 0 <= row[1] < row[0] and 0 < row[2] <= denominator
                for row in rows), "invalid fractional phase")
    require(len({(m, a) for m, a, v in rows}) == len(rows), "duplicate fractional phase")
    budgets = {m: 0 for m in sorted(free)}
    mass = [0] * period
    for m, a, v in rows:
        budgets[m] += v
        for x in range(a, period, m):
            mass[x] += v
    require(max(budgets.values()) <= denominator, "fractional resource overused")
    covered = bytearray(period)
    for a, m in fixed:
        for x in range(a, period, m):
            covered[x] = 1
    residual = [x for x in range(period) if not covered[x]]
    minimum = min(mass[x] for x in residual)
    require(minimum >= denominator, "fractional residual uncovered")
    return dict(denominator=denominator, phase_rows=len(rows), residual_points=len(residual),
                minimum_residual_mass=minimum, maximum_resource_mass=max(budgets.values()),
                resource_budgets=[[m, budgets[m]] for m in sorted(free)],
                residual_masses_sha256=pair_digest([mass[x] for x in residual]))


def cover_check(data, fixed):
    require(integer(data.get("schema")) and data.get("schema") == 1
            and integer(data.get("lcm")) and data.get("lcm") == 30240, "wrong upper scope")
    rows = data["congruences"]
    require(isinstance(rows, list) and bool(rows), "empty upper cover")
    require(all(isinstance(row, list) and len(row) == 2 and all(integer(v) for v in row)
                and 8 <= row[1] <= 30240 and 30240 % row[1] == 0 and 0 <= row[0] < row[1]
                for row in rows), "malformed upper class")
    require([m for a, m in rows] == sorted({m for a, m in rows}), "duplicate upper modulus")
    require(min(m for a, m in rows) == 8 and math.lcm(*(m for a, m in rows)) == 30240,
            "upper minimum or LCM is wrong")
    require(set(map(tuple, fixed)) <= set(map(tuple, rows)), "upper does not retain the prefix")
    counts = [0] * 30240
    for a, m in rows:
        for x in range(a, 30240, m):
            counts[x] += 1
    require(min(counts) > 0, "upper has holes")
    private = [[m, sum(counts[x] == 1 for x in range(a, 30240, m))] for a, m in rows]
    return dict(lcm=30240, minimum_exactly=8, classes=len(rows), retained_classes=len(fixed),
                holes=counts.count(0), multiplicities=[[k, v] for k, v in sorted(Counter(counts).items())],
                multiplicities_sha256=hashlib.sha256(bytes(counts)).hexdigest(),
                private_point_counts=private)


def mathematical_check(certificate, fractional, cover):
    return dict(status="EXACT_PRESCRIBED_PREFIX_LCM_30240", certificate=certificate_check(certificate),
                fractional=fractional_check(fractional, certificate["fixed"]),
                upper=cover_check(cover, certificate["fixed"]))


def controls(certificate, fractional, cover):
    # Direct finite union oracle checks compatible, incompatible and dividing pairs.
    union_cases = 0
    for period in (6, 12, 24):
        weight = [0 if x % 5 == 0 else x + 1 for x in range(period)]
        moduli = [m for m in range(2, period + 1) if period % m == 0]
        for m in moduli:
            for n in moduli:
                literal = [sum(weight[x] for x in range(period) if x % m == a or x % n == b)
                           for a in range(m) for b in range(n)]
                require(pair_values(weight, period, m, n) == literal, "small union mismatch")
                union_cases += len(literal)
    invalid = []
    def add(which, change):
        data = copy.deepcopy([certificate, fractional, cover]);change(data[which]);invalid.append(data)
    add(0, lambda d: d.update(period=10080))
    add(0, lambda d: d["fixed"].append(d["fixed"][0]))
    add(0, lambda d: d["weights"].append(d["weights"][0]))
    add(0, lambda d: d["weights"][0].__setitem__(1, -1))
    add(0, lambda d: d["weights"][0].__setitem__(1, True))
    add(0, lambda d: d.update(weights=[[certificate["fixed"][0][0], 1]]))
    add(0, lambda d: d.update(pair=[112, 112]))
    add(1, lambda d: d.update(denominator=0))
    add(1, lambda d: d["phase_masses"].append(d["phase_masses"][0]))
    add(1, lambda d: d["phase_masses"][0].__setitem__(0, 8))
    add(1, lambda d: d["phase_masses"][0].__setitem__(2, d["denominator"] + 1))
    add(1, lambda d: d.update(phase_masses=[]))
    add(2, lambda d: d["congruences"].pop(0))
    add(2, lambda d: d["congruences"].append(d["congruences"][0]))
    add(2, lambda d: d["congruences"][0].__setitem__(0, 0))
    private_m = next(m for m, count in cover_check(cover, certificate["fixed"])["private_point_counts"]
                     if count and m not in {m for a, m in certificate["fixed"]})
    add(2, lambda d: d.update(congruences=[r for r in d["congruences"] if r[1] != private_m]))
    for data in invalid:
        try:
            mathematical_check(*data)
        except ValueError:
            continue
        raise ValueError("invalid evidence accepted")
    return dict(small_union_phase_cases=union_cases, malformed_evidence_rejected=len(invalid))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    names = ["certificate.json", "fractional.json", "cover.json"]
    data = [json.loads((root / n).read_text()) for n in names]
    result = mathematical_check(*data)
    expected = dict(summary=result, hashes={n: hashlib.sha256((root / n).read_bytes()).hexdigest() for n in names},
                    controls=controls(*data))
    if args.write_expected:
        (root / "expected.json").write_text(json.dumps(expected, indent=2) + "\n")
    else:
        require(expected == json.loads((root / "expected.json").read_text()), "expected evidence mismatch")
    print(json.dumps(dict(status=result["status"], integer_gap=result["certificate"]["strict_gap"],
                          guaranteed_holes=result["certificate"]["minimum_holes"],
                          fractional_minimum=result["fractional"]["minimum_residual_mass"],
                          upper_classes=result["upper"]["classes"], upper_lcm=result["upper"]["lcm"],
                          controls=expected["controls"]), sort_keys=True))


if __name__ == "__main__":
    main()

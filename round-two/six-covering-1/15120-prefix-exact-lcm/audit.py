"""Separate physical audit; imports no discovery or main checker code."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(values):
    h = hashlib.sha256()
    for v in values:
        require(type(v) is int and 0 <= v < 2**64, "invalid digest value")
        h.update(struct.pack("<Q", v))
    return h.hexdigest()


def main():
    root = Path(__file__).resolve().parent
    expected = json.loads((root / "expected.json").read_text())
    data = {}
    for name in ("certificate.json", "fractional.json", "cover.json"):
        payload = (root / name).read_bytes()
        require(hashlib.sha256(payload).hexdigest() == expected["hashes"][name], "input hash changed")
        data[name] = json.loads(payload)
    cert, frac, cover = (data[name] for name in ("certificate.json", "fractional.json", "cover.json"))
    N = 15120
    fixed = cert["fixed"]
    require([m for a, m in fixed] == [m for m in range(8, 80) if N % m == 0], "bad prefix labels")
    require(all(m in {label for a, label in fixed} for m in (16, 27, 35)), "missing LCM witnesses")
    prefix_lcm = 16 * 27 * 35  # coprime fixed moduli; every other fixed modulus divides this product
    residual = [x for x in range(N) if not any(x % m == a for a, m in fixed)]
    require(all(type(x) is int and type(w) is int and w > 0 and x in residual
                for x, w in cert["weights"]), "bad weight support")
    require(len({x for x, w in cert["weights"]}) == len(cert["weights"]), "repeated weight coordinate")
    f = [0] * N
    for x, w in cert["weights"]:
        f[x] = w
    free = [m for m in range(8, N + 1) if N % m == 0 and m not in {m for a, m in fixed}]
    caps = {m: max(sum(f[x] for x in range(a, N, m)) for a in range(m)) for m in free}
    require(cert["pair"] == [112, 144], "wrong pair")
    # Rebuild every actual union by literal progressions. No intersection
    # histogram, CRT compatibility test or production pair formula is used.
    values = []
    for a in range(112):
        left = sum(f[x] for x in range(a, N, 112))
        for b in range(144):
            values.append(left + sum(f[x] for x in range(b, N, 144) if x % 112 != a))
    demand = sum(f)
    joint = max(values)
    capacity = sum(v for m, v in caps.items() if m not in (112, 144)) + joint
    certificate = dict(period=N, fixed_classes=len(fixed), fixed_lcm=prefix_lcm,
                       residual_points=len(residual), free_resources=len(free), weight_support=len(cert["weights"]),
                       maximum_weight=max(f), demand=demand, individual_capacity=sum(caps.values()),
                       pair=[112, 144], pair_phases=len(values), individual_pair_capacity=caps[112] + caps[144],
                       joint_pair_capacity=joint, grouped_capacity=capacity, strict_gap=demand-capacity,
                       minimum_holes=(demand-capacity+max(f)-1)//max(f),
                       resource_capacities=[[m, caps[m]] for m in free], all_pair_values_sha256=digest(values))
    require(demand > capacity, "no strict integer exclusion")
    require(certificate == expected["summary"]["certificate"], "integer manifest differs")

    # Literal predicates instead of distributing each phase along a progression.
    require(frac["fixed"] == fixed and frac["period"] == N, "fractional prefix differs")
    den = frac["denominator"]
    require(type(den) is int and den > 0, "invalid denominator")
    phase_rows = frac["phase_masses"]
    require(all(type(m) is int and type(a) is int and type(v) is int and m in free
                and 0 <= a < m and v > 0 for m, a, v in phase_rows), "invalid fractional class")
    require(len({(m, a) for m, a, v in phase_rows}) == len(phase_rows), "fractional phase repeated")
    budgets = {m: sum(v for label, a, v in phase_rows if label == m) for m in free}
    masses = [sum(v for m, a, v in phase_rows if x % m == a) for x in residual]
    require(max(budgets.values()) <= den and min(masses) >= den, "fractional cover invalid")
    fractional = dict(denominator=den, phase_rows=len(phase_rows), residual_points=len(residual),
                      minimum_residual_mass=min(masses), maximum_resource_mass=max(budgets.values()),
                      resource_budgets=[[m, budgets[m]] for m in free], residual_masses_sha256=digest(masses))
    require(fractional == expected["summary"]["fractional"], "fractional manifest differs")

    # Find the LCM from prime-exponent maxima instead of repeated gcd/lcm.
    rows = cover["congruences"]
    require(set(map(tuple, fixed)) <= set(map(tuple, rows)), "prefix not retained")
    require(min(m for a, m in rows) == 8 and len({m for a, m in rows}) == len(rows), "bad distinct upper moduli")
    exponents = {}
    for a, m in rows:
        require(type(a) is int and type(m) is int and 0 <= a < m, "bad upper phase")
        rest = m
        p = 2
        while p * p <= rest:
            e = 0
            while rest % p == 0:
                rest //= p
                e += 1
            if e:
                exponents[p] = max(exponents.get(p, 0), e)
            p += 1
        if rest > 1:
            exponents[rest] = max(exponents.get(rest, 0), 1)
    actual = 1
    for p, e in exponents.items():
        actual *= p**e
    require(actual == 30240 and cover["lcm"] == actual, "wrong actual upper LCM")
    counts = []
    private = {m: 0 for a, m in rows}
    for x in range(actual):
        hit = [m for a, m in rows if x % m == a]
        require(bool(hit), "upper has a literal hole")
        counts.append(len(hit))
        if len(hit) == 1:
            private[hit[0]] += 1
    upper = dict(lcm=actual, minimum_exactly=8, classes=len(rows), retained_classes=len(fixed), holes=counts.count(0),
                 multiplicities=[[k, v] for k, v in sorted(Counter(counts).items())],
                 multiplicities_sha256=hashlib.sha256(bytes(counts)).hexdigest(),
                 private_point_counts=[[m, private[m]] for a, m in rows])
    require(upper == expected["summary"]["upper"], "upper manifest differs")
    print(json.dumps(dict(status="SEPARATE_PHYSICAL_AUDIT_PASSED", pair_phases=len(values),
                          strict_gap=demand-capacity, fractional_points=len(residual),
                          upper_residues=actual, upper_classes=len(rows)), sort_keys=True))


if __name__ == "__main__":
    main()

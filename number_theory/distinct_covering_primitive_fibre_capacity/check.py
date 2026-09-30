"""Two exact conditional period43200 exclusions; no solver or tree premise.

six-covering-3, researcher. Every unused actual divisor capacity is computed
on the physical period. The reusable lemmas are proved in proof.md.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import gcd, lcm
from pathlib import Path
from time import monotonic
import argparse
import json

HERE = Path(__file__).resolve().parent
N = 43200
DIVISORS = tuple(n for n in range(8, N+1) if N % n == 0)


def progression_maximum(values, modulus):
    upper = len(values)//modulus*max(values)
    best = 0
    for a in range(modulus):
        best = max(best, sum(values[a::modulus]))
        if best == upper:
            break
    return best


def decode(Q, axes, boxes):
    if Q != 720 or axes != [16, 9, 5]:
        raise ValueError("wrong required weight period")
    result = {}
    for box in boxes:
        if len(box) != 4 or any(type(v) is not int for v in box) or box[3] <= 0:
            raise ValueError("invalid integer box")
        coordinates = []
        for mask, axis in zip(box[:3], axes):
            if not 0 < mask < 1 << axis:
                raise ValueError("invalid coordinate mask")
            coordinates.append([a for a in range(axis) if mask >> a & 1])
        for point in product(*coordinates):
            x = sum(a*(Q//axis)*pow(Q//axis, -1, axis)
                    for a, axis in zip(point, axes)) % Q
            if x in result:
                raise ValueError("boxes overlap")
            result[x] = box[3]
    if not result:
        raise ValueError("zero weight")
    return [result.get(x, 0) for x in range(Q)]


def check_case(anchors, Q, base, model):
    if (N % Q or len(base) != Q or any(type(w) is not int or w < 0 for w in base)
            or len(anchors) != len({m for m, a in anchors})
            or any(m not in DIVISORS or type(a) is not int or not 0 <= a < m
                   for m, a in anchors)):
        raise ValueError("invalid period, weights or distinct placed congruences")
    weights = [base[x % Q] for x in range(N)]
    if not any(weights) or any(weights[x] and any(x % m == a for m, a in anchors)
                              for x in range(N)):
        raise ValueError("positive weight on a placed class, or zero demand")
    remaining = tuple(n for n in DIVISORS if n not in {m for m, a in anchors})
    capacities = {n: progression_maximum(weights, n) for n in remaining}
    demand, ordinary = sum(weights), sum(capacities.values())
    if model == "omit-N":
        if Q >= N or tuple(n for n in remaining if lcm(Q, n) == N) != (N,):
            raise ValueError("singleton primitive-period hypothesis fails")
        corrected = ordinary-capacities[N]
    elif model == "fibre":
        B, b, p = 1728, 144, 5
        if Q not in (720, 3600) or not {B, B*p, N} <= set(remaining):
            raise ValueError("invalid fibre resources")
        if any(lcm(b, gcd(B, n)) == B for n in remaining if n % B):
            raise ValueError("a nontop fibre term has full period")
        # The fine b*p^2 version or its exact fivefold lift from Q720.
        corrected = ordinary-capacities[B]+capacities[B*p]+capacities[N]
    else:
        raise ValueError("unrecognised necessary-capacity inequality")
    if corrected >= demand:
        raise ValueError("the strict corrected inequality does not exclude completion")
    if ordinary < demand:
        raise ValueError("this evidence is meant to demonstrate an essential refinement")
    return {"N": N, "Q": Q, "placed": anchors, "model": model,
            "eligible_divisors": len(DIVISORS), "actual_unused_divisors": len(remaining),
            "base_demand": sum(base), "physical_demand": demand,
            "ordinary_physical_capacity": ordinary,
            "corrected_physical_capacity": corrected, "strict_physical_gap": demand-corrected,
            "maximum_point_weight": max(base),
            "individual_actual_capacities": capacities}


def evidence():
    uniform_anchors = ((8, 0), (9, 0), (10, 5), (12, 1),
                       (15, 11), (16, 2), (18, 1), (20, 6))
    base = [int(all(x % m != a for m, a in uniform_anchors)) for x in range(720)]
    uniform = check_case(uniform_anchors, 720, base, "fibre")
    path = HERE/"weighted_example.json"
    data = json.loads(path.read_text())
    if data["format_version"] != 1 or data["N"] != N or data["model"] != "omit-N":
        raise ValueError("required weighted example header changed")
    weighted = check_case(tuple(map(tuple, data["anchors"])), data["Q"],
                          decode(data["Q"], data["axes"], data["boxes"]), "omit-N")
    return {"agent": "six-covering-3", "role": "researcher",
            "scope": "two fixed-prefix completion exclusions; period43200 root remains unresolved",
            "uniform_fibre_case": uniform, "weighted_singleton_case": weighted,
            "weighted_file_sha256": sha256(path.read_bytes()).hexdigest(),
            "root_exclusion": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", type=Path)
    parser.add_argument("--expected", type=Path, default=HERE/"expected.json")
    args = parser.parse_args()
    start = monotonic()
    result = evidence()
    # JSON round-trip normalises integer dictionary keys and tuples.
    result = json.loads(json.dumps(result))
    if args.write:
        args.write.write_text(json.dumps(result, indent=2)+"\n")
    elif result != json.loads(args.expected.read_text()):
        raise ValueError("checked evidence differs from expected manifest")
    for name in ("uniform_fibre_case", "weighted_singleton_case"):
        r = result[name]
        print(name, "demand", r["physical_demand"], "ordinary",
              r["ordinary_physical_capacity"], "corrected",
              r["corrected_physical_capacity"], "gap", r["strict_physical_gap"])
    print("Every actual unused-divisor maximum checked; both fixed prefixes excluded.")
    print("The period43200 root remains unresolved.")
    print("Elapsed seconds:", monotonic()-start)


if __name__ == "__main__":
    main()

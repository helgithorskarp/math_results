"""Literal prefix adapter for the C35 budget, including every outside capacity.

Author six-covering-3, researcher. Published fixture provenance is in README.md.
The default projected-uniform vector is a control, not an exclusion claim.
"""

import argparse
import hashlib
import json
from pathlib import Path

from budget import divisors, require
from reproduce import run


def prepare(fixture, b=48, vectors=None):
    N = fixture["period"]
    require(type(N) is int and N % 35 == 0, "C35 period required")
    B, C = N // 35, 35
    require(B % 6 == 0 and b >= 1 and (B // 6) % b == 0, "invalid block period")
    anchors = tuple(tuple(pair) for pair in fixture["anchors"])
    require(len({n for n, _ in anchors}) == len(anchors), "repeated prescribed modulus")
    require(all(type(n) is int and type(a) is int and n >= 8 and N % n == 0 and 0 <= a < n
                for n, a in anchors), "invalid prescribed class")
    require(fixture["minimum"] == 8 and any(n == 8 for n, _ in anchors), "exactly-eight anchor required")
    residual = [int(not any(x % n == a for n, a in anchors)) for x in range(N)]
    encoded = sum(bit << x for x, bit in enumerate(residual))
    require(int(fixture["residual_hex"], 16) == encoded, "literal residual bitset mismatch")
    require(sum(residual) == fixture["residual_count"], "literal residual count mismatch")
    available = tuple(n for n in divisors(N) if n >= 8 and n not in {m for m, _ in anchors})
    require(tuple(fixture["available_moduli"]) == available, "incomplete actual resource set")
    tops = tuple(B * d for d in (1, 5, 7, 35))
    require(tuple(fixture["four_top_resources"]) == tops, "top resource mismatch")
    prescribed_top = {str(n): a for n, a in anchors if n in tops}
    require(fixture["prescribed_top_phases"] == prescribed_top, "prescribed top map mismatch")
    fixed = {n // B: (a % B, a % (n // B)) for n, a in anchors if n in tops}
    Q = b * C
    if vectors is None:
        ux = residual
        eta = [sum(residual[x] for x in range(y, N, Q)) for y in range(Q)]
    else:
        ux, eta = vectors["u"], vectors["v"]
    require(len(ux) == N and len(eta) == Q, "wrong physical vector dimensions")
    require(all(type(w) is int and 0 <= w <= 1000000000 for w in (*ux, *eta)), "invalid integer vector")
    require(all(residual[x] or ux[x] == 0 for x in range(N)), "u positive on a known class")
    u = [[0] * C for _ in range(B)]
    v = [[0] * C for _ in range(b)]
    for x, weight in enumerate(ux):
        u[x % B][x % C] = weight
    for y, weight in enumerate(eta):
        v[y % b][y % C] = weight
    return B, C, anchors, available, tops, fixed, ux, eta, u, v


def capacity(weights, n):
    hist = [0] * n
    for x, weight in enumerate(weights):
        hist[x % n] += weight
    return max(hist)


def evaluate(fixture, exe, b=48, vectors=None):
    B, C, anchors, available, tops, fixed, ux, eta, u, v = prepare(fixture, b, vectors)
    N, Q = B * C, b * C
    mixed = [ux[x] + eta[x % Q] for x in range(N)]
    known_costs = {str(n): sum(eta[x % Q] for x in range(a, N, n))
                   for n, a in anchors if n not in tops}
    outside = {str(n): capacity(mixed, n) for n in available if n not in tops}
    ordinary = {str(n): capacity(ux, n) for n in available}
    top = run(exe, B, b, u, v, fixed)
    demand = sum(mixed)
    lhs = demand - sum(known_costs.values())
    rhs = sum(outside.values()) + top["value"]
    return {"period": N, "b": b, "v_period": Q, "residual_count": fixture["residual_count"],
            "positive_u_residues": sum(int(w > 0) for w in ux),
            "known_outside_costs": known_costs, "mixed_demand": demand,
            "effective_demand": lhs, "outside_capacities": outside,
            "outside_capacity_total": sum(outside.values()), "top": top,
            "total_capacity": rhs, "strict_gap": lhs - rhs,
            "ordinary_demand": sum(ux), "ordinary_capacity": sum(ordinary.values()),
            "scope": "necessary bound for this vector; default control is not a root exclusion"}


def malformed_controls(fixture):
    cases = []
    for field in ("residual_count", "residual_hex", "available_moduli", "four_top_resources",
                  "prescribed_top_phases"):
        changed = dict(fixture)
        changed[field] = ({"residual_count": 0, "residual_hex": "0", "available_moduli": [],
                           "four_top_resources": [], "prescribed_top_phases": {"288": 0}})[field]
        cases.append(changed)
    for changed in cases:
        try:
            prepare(changed)
        except ValueError:
            continue
        raise RuntimeError("malformed application fixture accepted")
    return len(cases)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--optimizer", type=Path, required=True)
    parser.add_argument("--b", type=int, default=48)
    parser.add_argument("--vectors", type=Path, help="JSON physical u[N], periodic v[35*b]")
    args = parser.parse_args()
    data = args.fixture.read_bytes()
    fixture = json.loads(data)
    vectors = None if args.vectors is None else json.loads(args.vectors.read_text())
    result = evaluate(fixture, args.optimizer.resolve(), args.b, vectors)
    result["fixture_sha256"] = hashlib.sha256(data).hexdigest()
    if vectors is None and args.b == 48:
        result["rejected_fixtures"] = malformed_controls(fixture)
        expected = Path(__file__).with_name("expected-application.json")
        if expected.exists() and result != json.loads(expected.read_text()):
            raise RuntimeError("published application control mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

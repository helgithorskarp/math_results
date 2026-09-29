"""Deterministic construction and exact gcd-based extension capacities."""
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def divisors(n):
    small = [d for d in range(1, math.isqrt(n) + 1) if n % d == 0]
    return sorted(set(small + [n // d for d in small]))


def counts_by_progressions(pairs, period):
    counts = [0] * period
    for a, m in pairs:
        if not 0 <= a < m or period % m:
            raise ValueError("Noncanonical residue or modulus outside period")
        for x in range(a, period, m):
            counts[x] += 1
    return counts


def refine(pairs, p, c):
    period = math.lcm(*(m for a, m in pairs))
    if p < 2 or any(p % d == 0 for d in range(2, math.isqrt(p) + 1)):
        raise ValueError("p must be prime")
    if period % p or period // p % p == 0:
        raise ValueError("The original LCM must have p-adic valuation one")
    if (c, p) not in pairs:
        raise ValueError("Missing designated congruence")
    if len({m for a, m in pairs}) != len(pairs):
        raise ValueError("Repeated original modulus")
    if not all(counts_by_progressions(pairs, period)):
        raise ValueError("The original system is not a covering")
    result = [(a, m) for a, m in pairs if m != p]
    for a, m in pairs:
        if m % p == 0:
            d = m // p
            residue = c + p * (a % p)
            if d > 1:
                residue += p*p * ((a-residue) * pow(p*p, -1, d) % d)
            result.append((residue, p*p*d))
    return sorted(result, key=lambda x: x[1])


def build():
    seed = json.loads((ROOT / "seed_m7.json").read_text())["congruences"]
    pairs = [tuple(pair) for pair in seed]
    assert len(pairs) == 66
    assert [m for a, m in pairs] == [d for d in divisors(10080) if d >= 7]
    fixed = [pair for pair in pairs if pair[1] != 7]
    assert math.lcm(*(m for a, m in fixed)) == 10080
    coverage = counts_by_progressions(fixed, 10080)
    holes = [h for h, n in enumerate(coverage) if n == 0]
    assert len(holes) == 252
    witness = {
        "minimum_modulus": 8,
        "lcm": 70560,
        "construction": "Prime-digit refinement at p=7, c=6",
        "congruences": [list(pair) for pair in refine(pairs, 7, 6)],
    }
    rows = []
    for t in range(1, 7):
        L = t * 10080
        mods = [d for d in divisors(L) if d >= 8 and 10080 % d != 0]
        details = []
        for d in mods:
            g = math.gcd(10080, d)
            w = max(Counter(h % g for h in holes).values())
            assert t*g % d == 0
            details.append([d, g, w, t*g // d * w])
        row = {"multiplier": t, "lcm": L, "hole_count": t*len(holes),
               "new_moduli": len(mods),
               "capacity_sum": sum(entry[3] for entry in details),
               "capacities_d_g_w_C": details}
        assert row["capacity_sum"] < row["hole_count"]
        rows.append(row)
    return witness, {"base_lcm": 10080, "base_holes": 252, "rows": rows}


if __name__ == "__main__":
    cover, manifest = build()
    assert cover == json.loads((ROOT / "cover_m8.json").read_text())
    assert manifest == json.loads((ROOT / "capacity_manifest.json").read_text())
    print(json.dumps({"construction": "matched", "classes": len(cover["congruences"]),
                      "lcm": cover["lcm"], "minimum_modulus": cover["minimum_modulus"],
                      "capacity_sums": [r["capacity_sum"] for r in manifest["rows"]]},
                     sort_keys=True))

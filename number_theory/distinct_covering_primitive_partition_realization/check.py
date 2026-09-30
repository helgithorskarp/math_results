"""Definition-level controls; six-covering-3, researcher.

Enumerate every cofactor phase and every b-phase block label for eight small
fixed weights. Independently count useful physical top-class masses at the
realized CRT phases. These controls supplement the general written proofs.
"""
from hashlib import sha256
from itertools import product
from math import gcd
from pathlib import Path
from time import monotonic
import argparse
import json

import partition as model

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def vector(W, p, c):
    b = len(W[0])
    Q = b*p**c
    require(gcd(b, p) == 1, "CRT axes must be coprime")
    return [W[x % (p**c)][x % b] for x in range(Q)]


def coarse_maximum(W, p, c):
    """Raw labels and raw cofactor phases; no set-partition reduction."""
    b, P = len(W[0]), p**c
    best, count = -1, 0
    for phases in product(*(range(p**j) for j in range(c + 1))):
        footprints = [tuple(z for z in range(P) if z % (p**j) == r)
                      for j, r in enumerate(phases)]
        for labels in product(range(b), repeat=c + 1):
            count += 1
            populations = [[0]*P for _ in range(b)]
            for j, phase_footprint in enumerate(footprints):
                for z in phase_footprint:
                    populations[labels[j]][z] += 1
            value = sum(k*W[z][t] for t, row in enumerate(populations)
                        for z, k in enumerate(row) if k >= 2)
            best = max(best, value)
    return best, count


def physical_useful(B, p, c, W, classes):
    """Literal actual congruence progressions at the full physical period."""
    N = B*p**c
    # Trial division independent of the model's radical helper.
    prime_factors = [q for q in range(2, B + 1) if B % q == 0
                     and all(q % d for d in range(2, q))]
    rho = 1
    for q in prime_factors:
        rho *= q
    T = B//rho
    v = vector(W, p, c)
    Q = len(v)
    total = 0
    for n, a in classes:
        for x in range(a, N, n):
            active = sum(a2 % T == a % T and x % (n2//B) == a2 % (n2//B)
                         for n2, a2 in classes)
            if active >= 2:
                total += v[x % Q]
    return total


def genuine_cover_controls():
    cases, maxima_checks = 0, 0
    original = [(2, 0), (3, 0), (4, 1), (6, 1), (12, 11)]
    for B, p, b in [(9, 2, 3), (20, 3, 2)]:
        c, N = 3, B*p**3
        require(N % 12 == 0, "Positive control period")
        top = [(B*p**j, (7*j + 1) % (B*p**j)) for j in range(4)]
        classes = original + top
        require(len({n for n, a in classes}) == len(classes), "Positive moduli distinct")
        require(all(any(x % n == a for n, a in classes) for x in range(N)), "Positive cover")
        for seed in range(9):
            W = [[(z*13 + t*7 + z*t*3 + seed) % 7 for t in range(b)]
                 for z in range(p**3)]
            H = model.cube_budget(W, p)["F3"]
            v = vector(W, p, c)
            demand = (N//len(v))*sum(v)
            outside = 0
            for n, a in original:
                outside += max(sum(v[x % len(v)] for x in range(r, N, n))
                               for r in range(n))
                maxima_checks += 1
            require(demand <= outside + H, "Genuine cover violates necessary budget")
            cases += 1
    return cases, maxima_checks


def run(seconds):
    start = monotonic()
    rows = []
    for c, p, b in [(1, 2, 3), (2, 2, 3), (3, 2, 3), (4, 2, 3), (3, 3, 1)]:
        W = [[(13*z + 7*t + 3*z*t + c) % 7 for t in range(b)] for z in range(p**c)]
        rows.append((f"pattern-c{c}-p{p}-b{b}", c, p, b, W, 9 if p == 2 else 20))
    strict = [[0, 0] for _ in range(27)]
    for z in range(0, 27, 3):
        strict[z][0] = 1
    strict[1][1] = 4
    rows.extend([
        ("strict-pair", 3, 3, 2, strict, 20),
        ("uniform", 3, 3, 2, [[1, 1] for _ in range(27)], 20),
        ("zero-component", 3, 3, 2, [[0, 0] for _ in range(27)], 20),
    ])
    results, configurations = [], 0
    for name, c, p, b, W, B in rows:
        if monotonic() - start > seconds:
            raise RuntimeError("Incomplete control enumeration: time bound reached")
        F, witness = model.general_budget(W, p, c)
        raw, count = coarse_maximum(W, p, c)
        require(F == raw, "Partition maximum differs from raw block-label maximum")
        realization = model.realize(B, p, c, W, witness)
        physical = physical_useful(B, p, c, W, realization["classes"])
        require(physical == F, "Actual CRT realization missed maximum")
        entry = {"case": name, "p": p, "c": c, "b": b, "B": B,
                 "F": F, "raw_useful_maximum": raw, "physical_useful_mass": physical,
                 "raw_phase_label_tuples": count,
                 "partitions": len(tuple(model.partitions(c + 1))),
                 "weight_sha256": sha256(json.dumps(W, separators=(",", ":")).encode()).hexdigest()}
        if c == 3:
            cube = model.cube_budget(W, p)
            require(cube["F3"] == F, "Closed cube formula differs from partition definition")
            entry["cube"] = cube
        if name == "strict-pair":
            require(F == 26 and entry["cube"]["K3"] == 22
                    and entry["cube"]["pair_budget"] == 26, "Strict pair fixture")
            # Explicit physical top phases attaining the pair mode.
            explicit = [[20, 0], [60, 0], [180, 1], [540, 1]]
            require(physical_useful(20, 3, 3, W, explicit) == 26, "Literal pair fixture")
        results.append(entry)
        configurations += count
    covers, maximum_checks = genuine_cover_controls()
    rejected = 0
    invalid = [([[1]], 4, 1), ([[1], [-1]], 2, 1), ([[1], [1.0]], 2, 1),
               ([[1], [1, 2]], 2, 1), ([[1], [1]], 2, 0)]
    for W, p, c in invalid:
        try:
            model.general_budget(W, p, c)
        except ValueError:
            rejected += 1
    require(rejected == len(invalid), "Invalid component accepted")
    invalid_realizations = [(6, 2, 1), (20, 3, 3)]
    for B, p, b in invalid_realizations:
        W = [[1]*b for _ in range(p**3)]
        F, witness = model.general_budget(W, p, 3)
        try:
            model.realize(B, p, 3, W, witness)
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError("Invalid physical hypotheses accepted")
    require(monotonic() - start <= seconds, "Incomplete controls: time bound reached")
    evidence = {
        "agent": "six-covering-3", "role": "researcher",
        "scope": "finite controls for written general realization and cube-budget proofs",
        "cases": results, "raw_phase_label_tuples": configurations,
        "genuine_cover_weight_checks": covers, "literal_outside_maxima_checks": maximum_checks,
        "malformed_hypotheses_rejected": rejected,
        "full43200_exclusion": False, "global_numeric_bound_improved": False,
    }
    return evidence, monotonic() - start


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--seconds", type=float, default=20)
    args = parser.parse_args()
    if not 0 < args.seconds <= 20:
        raise ValueError("Existing control budget: at most20 seconds")
    evidence, elapsed = run(args.seconds)
    expected = HERE / "expected.json"
    if args.write:
        expected.write_text(json.dumps(evidence, indent=2) + "\n")
    else:
        require(evidence == json.loads(expected.read_text()), "Evidence manifest differs")
    print(f"{evidence['raw_phase_label_tuples']} complete raw phase/label tuples; "
          f"{evidence['genuine_cover_weight_checks']} true-cover weights passed.")
    print("Strict pair mode26>K3=22; every tested partition maximum physically attained.")
    print("No full43200 exclusion or numerical-bound improvement.")
    print(f"Elapsed seconds: {elapsed:.6f}")


if __name__ == "__main__":
    main()

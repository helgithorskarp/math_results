"""Exact local, cover, profile, DP and known-mask quotient controls.

Author six-covering-3, researcher. Integer arithmetic, explicit exceptions.
The universal claim follows from proof.md, not these sampled controls.
"""

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
from random import Random
import subprocess
import sys

from transport import (CHARGE, DELTA, MASS, actual_value, balanced_vertices, coefficient_row, encode,
                       exact_budget, known_data, literal_charge, profile35,
                       old_encode, profile_charge35, require, run, sharp_nonnegative)
from budget import divisors, exact_budget as old_exact_budget

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mixed-outside-groups"))
from groups import PairBudgets, fractional_pairs
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cofactor-orbits"))
from check_orbits import canonical_pair, permutation_to_pair


def additive(f):
    def at(e, col):
        return f[next(j for j in range(6) if j % 2 == e and j % 3 == col)]
    return all(at(0, c) - at(1, c) == at(0, 0) - at(1, 0) for c in range(3))


def local_controls():
    vertices = balanced_vertices()
    increments = monotonicity = comparisons = 0
    for a in range(64):
        mass = max(sum(w[j] for j in range(6) if a & (1 << j)) for w in vertices)
        require(mass == MASS[a] == 2 * a.bit_count() - CHARGE[a], "dual mass formula fails")
        cols0 = {j % 3 for j in range(6) if j % 2 == 0 and a & (1 << j)}
        cols1 = {j % 3 for j in range(6) if j % 2 == 1 and a & (1 << j)}
        require(mass == min(2 * len(cols0 | cols1), 3 + 2 * len(cols1),
                            3 + 2 * len(cols0), 6), "elementary four-cover cost formula fails")
        f = sharp_nonnegative(a)
        require(additive(f) and sum(f) == mass and all(f[j] >= bool(a & (1 << j)) for j in range(6)),
                "sharp nonnegative additive witness fails")
        for h in range(64):
            require(DELTA[a][h] == mass - MASS[a & ~h] and DELTA[a][h] >= 0,
                    "wrong or negative residual deletion increment")
            for j in range(6):
                require(DELTA[a][h | (1 << j)] >= DELTA[a][h], "increment not monotone")
                monotonicity += 1
            increments += 1
    for coefficients in product(range(3), repeat=5):
        k = [coefficients[j % 2] + coefficients[2 + j % 3] for j in range(6)]
        u = sum(1 << j for j in range(6) if k[j] == 0)
        s = sum(k)
        require(6 - s - MASS[u] <= 0, "known baseline is positive")
        for h in range(64):
            a = u & ~h
            f = [g + kk - 1 for g, kk in zip(sharp_nonnegative(a), k)]
            require(additive(f) and all(f[j] >= (-1 if h & (1 << j) else 0) for j in range(6)),
                    "comparison signed-function construction fails")
            require(6 - s - MASS[a] <= CHARGE[h], "new absolute charge exceeds old kappa")
            comparisons += 1
    # Known even row and column0: S=5, residual {1,5}, M=3.
    k = [int(j % 2 == 0) + int(j % 3 == 0) for j in range(6)]
    u = sum(1 << j for j in range(6) if not k[j])
    h = u & -u
    require(u.bit_count() == 2 and MASS[u] == 3 and DELTA[u][h] == 1 and CHARGE[h] == 0,
            "row/column overlap mechanism changed")
    return {"sharp_local_shapes": 64, "deletion_increments": increments,
            "monotonicity_checks": monotonicity, "known_function_comparisons": comparisons,
            "overlap_example": {"known_count_mass": sum(k), "residual_mask": u,
                                "transport_mass": MASS[u], "singleton_increment": DELTA[u][h]}}


def profile_controls():
    rng = Random(20261001037)
    profiles = []
    for i in range(3):
        masks = [rng.randrange(64) for _ in range(35)]
        weights = [rng.randrange(11) for _ in range(35)]
        profiles.append((masks, weights))
    count = 0
    digest = hashlib.sha256()
    for masks, weights in profiles:
        table = profile35(weights, masks)
        for rs in ((0, 0, 0, 0), (0, 1, 2, 13), (0, 4, 6, 34)):
            for subset in range(16):
                members = [i for i in range(4) if subset & (1 << i)]
                for selected in product(range(6), repeat=len(members)):
                    js = [0] * 4
                    for i, j in zip(members, selected):
                        js[i] = j
                    literal = literal_charge(35, (1, 5, 7, 35), rs, subset, js, weights, masks)
                    profile = profile_charge35(rs, subset, js, table)
                    require(profile == literal, "C35 profile differs from literal distinct point set")
                    digest.update(f"{literal}\n".encode())
                    count += 1
    return {"profile_literal_comparisons": count, "profile_values_sha256": digest.hexdigest()}


def reference_controls():
    rng = Random(20261001038)
    count = tuples = 0
    for B, C in ((6, 1), (12, 1), (18, 1), (6, 5), (12, 5), (6, 7)):
        b = B // 6
        ds = (1,) if C == 1 else (1, C)
        for repetition in range(2):
            u = [[rng.randrange(7) for _ in range(C)] for _ in range(B)]
            v = [[rng.randrange(5) for _ in range(C)] for _ in range(b)]
            masks = [[rng.randrange(64) for _ in range(C)] for _ in range(b)]
            fixed = {} if repetition == 0 else {ds[-1]: (B - 1, C - 1)}
            if fixed:
                u[B - 1] = [0] * C
            choices = [((fixed[d],) if d in fixed else tuple(product(range(B), range(d)))) for d in ds]
            best = None
            for phases in product(*choices):
                value = actual_value(B, C, b, u, v, masks, phases)
                best = value if best is None else max(best, value)
                tuples += 1
            require(exact_budget(B, C, b, u, v, masks, fixed) == best,
                    "actual-label DP differs from complete physical top-phase enumeration")
            count += 1
    return {"reference_dp_controls": count, "literal_complete_top_tuples": tuples}


def known_mask_controls():
    rng = Random(20261001041)
    cases = proper_blocks = 0
    for B, C in ((6, 1), (12, 1), (6, 5), (12, 5), (6, 7), (6, 35), (288, 35), (432, 35)):
        N, T = B * C, B // 6
        anchors = [(n, rng.randrange(n)) for n in divisors(N)[::3]]
        # Always include an actual known top, which must be excluded from U.
        if B not in dict(anchors):
            anchors.append((B, rng.randrange(B)))
        masks, counts = known_data(B, C, anchors)
        wanted_masks = [[63] * C for _ in range(T)]
        wanted_counts = [[0] * C for _ in range(T)]
        proper = [(n, a) for n, a in anchors if n % B != 0]
        for x in range(N):
            q, j, z = x % B % T, x % B // T, x % C
            k = sum(x % n == a for n, a in proper)
            wanted_counts[q][z] += k
            if k:
                wanted_masks[q][z] &= ~(1 << j)
        require(masks == wanted_masks and counts == wanted_counts,
                "known masks differ from independent physical-residue scan")
        for n, a in proper:
            blocks = [[[0] * 6 for _ in range(C)] for _ in range(T)]
            for x in range(a, N, n):
                blocks[x % B % T][x % C][x % B // T] = 1
            require(all(additive(f) for row in blocks for f in row), "known outside indicator not additive")
            proper_blocks += T * C
        cases += 1
    return {"literal_known_mask_controls": cases, "proper_known_indicator_blocks": proper_blocks}


def cover_controls():
    base = ((2, 0), (3, 0), (4, 1), (6, 5), (12, 7))
    rng = Random(20261001039)
    count = fractional = positive_known = negative_old = improvements = 0
    for N in (12, 24):
        T = N // 6
        require(all(any(x % n == a for n, a in base) for x in range(N)), "bad cover control")
        for mask in range(32):
            known = tuple(pair for i, pair in enumerate(base) if mask & (1 << i))
            outside = [n for n in range(2, N) if N % n == 0 and n not in dict(known)]
            actual = dict(base)
            for n in (*outside, N):
                actual.setdefault(n, rng.randrange(n))
            residual_masks, multiplicities = known_data(N, 1, known)
            fixed = {1: (dict(known)[N], 0)} if N in dict(known) else {}
            for repetition in range(4):
                ux = [rng.randrange(8) if not any(x % n == a for n, a in known) else 0 for x in range(N)]
                eta = [rng.randrange(7) + 1 for _ in range(T)]
                vx = [eta[x % T] for x in range(N)]
                u, v = [[x] for x in ux], [[x] for x in eta]
                edges = []
                if len(outside) >= 3:
                    edges = [(*sorted((outside[i], outside[(i + 1) % len(outside)])), 1)
                             for i in range(len(outside))]
                elif len(outside) == 2:
                    edges = [(*outside, 1 + repetition % 2)]
                calc = PairBudgets(ux, vx, N if repetition % 2 else None)
                groups = fractional_pairs(calc, outside, edges)
                scale = groups["scale"]
                demand = sum(ux) + sum(MASS[residual_masks[q][0]] * eta[q] for q in range(T))
                old_demand = sum(ux) + sum((6 - multiplicities[q][0]) * eta[q] for q in range(T))
                new_top = exact_budget(N, 1, T, u, v, residual_masks, fixed)
                old_top = old_exact_budget(N, 1, T, u, v, fixed)
                require(scale * demand <= groups["outside_numerator"] + scale * new_top,
                        "new necessary group budget rejects a genuine cover")
                require(demand - new_top >= old_demand - old_top, "old comparison fails on genuine cover")
                actual_rhs = scale * actual_value(N, 1, T, u, v, residual_masks, ((actual[N], 0),))
                for n in outside:
                    actual_rhs += groups["singleton_remainders"][str(n)] * sum(
                        ux[x] + vx[x] for x in range(actual[n], N, n))
                for pair in groups["pairs"]:
                    m, n = pair["resources"]
                    union_v = pair["v_mode"] == "union"
                    value = sum(ux[x] * int(x % m == actual[m] or x % n == actual[n])
                                + vx[x] * (int(x % m == actual[m] or x % n == actual[n]) if union_v else
                                           int(x % m == actual[m]) + int(x % n == actual[n])) for x in range(N))
                    actual_rhs += pair["numerator"] * value
                require(scale * demand <= actual_rhs, "actual grouped covering inequality fails")
                count += 1
                fractional += any(pair["numerator"] == 1 for pair in groups["pairs"])
                positive_known += bool(known)
                negative_old += old_demand < 0
                improvements += demand - new_top > old_demand - old_top
    return {"genuine_cover_cases": count, "fractional_cover_cases": fractional,
            "positive_known_v_cases": positive_known, "negative_old_effective_demands": negative_old,
            "strict_same_vector_improvements_on_covers": improvements,
            "ambient24_actual_cover_lcm": 12}


def classes(p, u, v, masks, fixed):
    locked = {r % p for d, (_, r) in fixed.items() if d % p == 0}
    other = 7 if p == 5 else 5
    result, lookup = [], {}
    for a in range(p):
        zs = [next(z for z in range(35) if z % p == a and z % other == h) for h in range(other)]
        signature = ("fixed", a) if a in locked else (
            "free", tuple(row[z] for matrix in (u, v, masks) for row in matrix for z in zs))
        if signature not in lookup:
            lookup[signature] = len(result)
            result.append([])
        result[lookup[signature]].append(a)
    return result


def orbit_audit(B, b, u, v, masks, fixed, scores):
    c5, c7 = classes(5, u, v, masks, fixed), classes(7, u, v, masks, fixed)
    choices = [(fixed[d][1],) if d in fixed else range(d) for d in (5, 7, 35)]
    reps = set()
    count = transports = 0
    for r5, r7, s in product(*choices):
        a5, s5 = canonical_pair(r5, s % 5, c5)
        a7, s7 = canonical_pair(r7, s % 7, c7)
        ss = next(z for z in range(35) if z % 5 == s5 and z % 7 == s7)
        reps.add((a5, a7, ss))
        require(all(d not in fixed or r == fixed[d][1] for d, r in zip((5, 7, 35), (a5, a7, ss))),
                "known-mask quotient changes fixed phase")
        if scores:
            p5 = permutation_to_pair(r5, s % 5, a5, s5, c5)
            p7 = permutation_to_pair(r7, s % 7, a7, s7, c7)
            zmap = [next(y for y in range(35) if y % 5 == p5[z % 5] and y % 7 == p7[z % 7])
                    for z in range(35)]
            require(all(row[z] == row[zmap[z]] for matrix in (u, v, masks) for row in matrix for z in range(35)),
                    "transport changes weights or known residual masks")
            ts = [fixed[d][0] if d in fixed else (3 * i + 7 * count) % B for i, d in enumerate((1, 5, 7, 35))]
            before, after = tuple(zip(ts, (0, r5, r7, s))), tuple(zip(ts, (0, a5, a7, ss)))
            require(actual_value(B, 35, b, u, v, masks, before) == actual_value(B, 35, b, u, v, masks, after),
                    "literal known-residual score changes under quotient")
            transports += 1
        count += 1
    return c5, c7, count, len(reps), transports


def cpp_controls(exe, old_exe, small):
    rng = Random(20261001040)
    cases = []
    inputs = []
    for i in range(8):
        B = (6, 12, 18)[i % 3]
        b = B // 6
        p5, p7 = [0, 1, 1, 1, 1], [1, 0, 1, 1, 1, 1, 1]
        def matrix(height, maximum):
            layers = [[[rng.randrange(maximum) for _ in range(2)] for _ in range(2)] for _ in range(height)]
            return [[layers[q][p5[z % 5]][p7[z % 7]] for z in range(35)] for q in range(height)]
        u, v, masks = matrix(B, 11), matrix(b, 7), matrix(b, 64)
        fixed = ({}, {5: (2, 2)}, {35: (4, 17)}, {5: (1, 0), 7: (2, 6), 35: (3, 14)})[i % 4]
        for t, _ in fixed.values():
            u[t] = [0] * 35
        inputs.append((f"structured{i}", B, b, u, v, masks, fixed))
    inputs.extend([
        ("uniform_masks", 6, 1, [[0] * 35 for _ in range(6)], [[1] * 35], [[63] * 35], {}),
        ("masks_only_break_symmetry", 6, 1, [[0] * 35 for _ in range(6)], [[1] * 35],
         [[z % 5 + 5 * (z % 7) for z in range(35)]], {}),
        ("empty_residual", 6, 1, [[rng.randrange(7) for _ in range(35)] for _ in range(6)],
         [[4] * 35], [[0] * 35], {}),
        ("old_recovered", 12, 2, [[rng.randrange(7) for _ in range(35)] for _ in range(12)],
         [[rng.randrange(8) for _ in range(35)] for _ in range(2)], [[63] * 35 for _ in range(2)], {})])
    if not small:
        for B in (288, 432):
            b = B // 6
            u = [[10 if t in (0, B // 2) else 0 for _ in range(35)] for t in range(B)]
            v = [[int(q == 0 and z == 0) for z in range(35)] for q in range(b)]
            masks = [[10 if q == 0 and z == 0 else 63 for z in range(35)] for q in range(b)]
            inputs.append((f"actual_label{B}", B, b, u, v, masks, {}))
    for label, B, b, u, v, masks, fixed in inputs:
        c5, c7, n, r, transports = orbit_audit(B, b, u, v, masks, fixed, label in ("structured0", "masks_only_break_symmetry"))
        full = run(exe, B, b, u, v, masks, fixed, False)
        reduced = run(exe, B, b, u, v, masks, fixed, True)
        for result in (full, reduced):
            cu, cv = coefficient_row(B, 35, b, masks, [(t, r) for _, t, r in result["phases"]])
            require(sum(cu[t][z] * u[t][z] for t in range(B) for z in range(35))
                    + sum(cv[q][z] * v[q][z] for q in range(b) for z in range(35)) == result["value"],
                    "unfolded coefficient row differs from literal witness value")
        require(full["value"] == reduced["value"], "full and known-mask quotient maxima differ")
        require(full["cofactor_tuples"] == n == reduced["complete_cofactor_tuples"]
                and reduced["cofactor_tuples"] == r, "quotient counts differ")
        require((reduced["classes5"], reduced["classes7"]) == (c5, c7), "signature partitions differ")
        require(full["local_candidate_visits"] * r == reduced["local_candidate_visits"] * n,
                "actual-label visit counts differ")
        if label == "uniform_masks":
            require(r == 4, "uniform cofactor quotient is incomplete")
        if label == "masks_only_break_symmetry":
            require(r == 1225, "weight-only quotient wrongly retained for changed charge")
        reference = None
        if len(fixed) == 3:
            reference = exact_budget(B, 35, b, u, v, masks, fixed)
            require(reference == full["value"], "C++ profile DP differs from literal Python DP")
        if label in ("old_recovered", "uniform_masks"):
            p = subprocess.run([str(old_exe), "--orbits"], input=old_encode(B, b, u, v, fixed),
                               text=True, capture_output=True, check=True, timeout=50)
            require(json.loads(p.stdout)["value"] == full["value"], "U=all fails to recover old kappa budget")
        cases.append({"label": label, "B": B, "b": b, "value": full["value"],
                      "full_tuples": n, "quotient_tuples": r, "literal_score_transports": transports,
                      "literal_python_dp": reference})
    return cases


def rejection_controls(exe):
    valid = encode(6, 1, [[0] * 35 for _ in range(6)], [[1] * 35], [[63] * 35], {})
    tokens = valid.split()
    cases = [(valid, ["--invalid"]), (valid, ["--orbits", "extra"]), (" ".join(tokens[:-35]), []),
             (valid + " 1", []), (" ".join(tokens[:-1] + ["64"]), []),
             (" ".join(tokens[:-1] + ["-1"]), []), (" ".join(["30"] + tokens[1:]), []),
             (" ".join(tokens[:1] + ["2"] + tokens[2:]), []),
             (" ".join(tokens[:10] + ["1000000001"] + tokens[11:]), [])]
    for text, flags in cases:
        p = subprocess.run([str(exe), *flags], input=text, text=True, capture_output=True, timeout=5)
        require(p.returncode != 0, "invalid optimizer input accepted")
    bad = [lambda: known_data(30, 1, ()), lambda: known_data(6, 5, ((7, 0),)),
           lambda: known_data(6, 5, ((2, 0), (2, 1))), lambda: known_data(6, 5, ((5, 5),)),
           lambda: exact_budget(6, 1, 1, [[0] for _ in range(6)], [[0]], [[64]]),
           lambda: exact_budget(6, 1, 1, [[0] for _ in range(6)], [[0]], [[True]])]
    for f in bad:
        try:
            f()
        except ValueError:
            continue
        raise RuntimeError("invalid Python mathematical input accepted")
    return len(cases) + len(bad)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--optimizer", type=Path, required=True)
    parser.add_argument("--old-optimizer", type=Path, required=True)
    parser.add_argument("--small", action="store_true")
    args = parser.parse_args()
    result = {**local_controls(), **profile_controls(), **reference_controls(), **known_mask_controls(), **cover_controls(),
              "cpp_cases": cpp_controls(args.optimizer.resolve(), args.old_optimizer.resolve(), args.small),
              "rejected_inputs": rejection_controls(args.optimizer.resolve())}
    expected = Path(__file__).with_name("expected-small.json" if args.small else "expected.json")
    if expected.exists():
        require(result == json.loads(expected.read_text()), "published check output differs")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

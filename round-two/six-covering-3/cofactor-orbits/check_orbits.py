"""Exact author checks for the C35 coordinate-fiber quotient.

Author six-covering-3, researcher. Complete enumeration remains a control.
The proof, not a sampled equality, supplies the universal quotient theorem.
"""

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
from random import Random
import subprocess
import sys
from time import monotonic

prior = Path(__file__).resolve().parent.parent / "four-top-block-dp"
sys.path.insert(0, str(prior))
from budget import actual_value, require
from reproduce import encode, reject_controls


def classes(p, u, v, fixed):
    locked = {r % p for d, (_, r) in fixed.items() if d % p == 0}
    other = 7 if p == 5 else 5
    result, by_signature = [], {}
    for a in range(p):
        zs = [next(z for z in range(35) if z % p == a and z % other == h)
              for h in range(other)]
        signature = ("fixed", a) if a in locked else (
            "free", tuple(row[z] for matrix in (u, v) for row in matrix for z in zs))
        if signature not in by_signature:
            by_signature[signature] = len(result)
            result.append([])
        result[by_signature[signature]].append(a)
    return result


def canonical_pair(a, b, partition):
    ca = next(c for c in partition if a in c)
    cb = next(c for c in partition if b in c)
    if ca != cb:
        return ca[0], cb[0]
    return (ca[0], ca[0]) if a == b else (ca[0], ca[1])


def permutation_to_pair(a, b, target_a, target_b, partition):
    perm = [None] * sum(map(len, partition))
    perm[a], perm[b] = target_a, target_b
    require(a != b or target_a == target_b, "invalid equal-pair transport")
    for c in partition:
        remain_source = [x for x in c if perm[x] is None]
        remain_target = [x for x in c if x not in {perm[y] for y in c}]
        for x, y in zip(remain_source, remain_target):
            perm[x] = y
    require(sorted(perm) == list(range(len(perm))), "transport is not a permutation")
    return perm


def audit_quotient(B, b, u, v, fixed, inspect_scores=False):
    c5, c7 = classes(5, u, v, fixed), classes(7, u, v, fixed)
    choices = [(fixed[d][1],) if d in fixed else range(d) for d in (5, 7, 35)]
    representatives = set()
    tuples = transports = 0
    digest = hashlib.sha256()
    for r5, r7, s in product(*choices):
        a5, s5 = canonical_pair(r5, s % 5, c5)
        a7, s7 = canonical_pair(r7, s % 7, c7)
        target_s = next(z for z in range(35) if z % 5 == s5 and z % 7 == s7)
        target = (a5, a7, target_s)
        require(all(d not in fixed or rr == fixed[d][1]
                    for d, rr in zip((5, 7, 35), target)), "representative violates fixed phase")
        representatives.add(target)
        perm5 = permutation_to_pair(r5, s % 5, a5, s5, c5)
        perm7 = permutation_to_pair(r7, s % 7, a7, s7, c7)
        for d, (_, r) in fixed.items():
            if d % 5 == 0:
                require(perm5[r % 5] == r % 5, "transport changes prescribed5 coordinate")
            if d % 7 == 0:
                require(perm7[r % 7] == r % 7, "transport changes prescribed7 coordinate")
        zmap = [next(y for y in range(35)
                     if y % 5 == perm5[z % 5] and y % 7 == perm7[z % 7]) for z in range(35)]
        if inspect_scores:
            for matrix in (u, v):
                require(all(row[z] == row[zmap[z]] for row in matrix for z in range(35)),
                        "literal weight transport changes input")
            ts = [fixed[d][0] if d in fixed else (7 * tuples + 3 * i) % B
                  for i, d in enumerate((1, 5, 7, 35))]
            before = tuple(zip(ts, (0, r5, r7, s)))
            after = tuple(zip(ts, (0, a5, a7, target_s)))
            require(actual_value(B, 35, b, u, v, before) ==
                    actual_value(B, 35, b, u, v, after), "literal budget transport changes score")
            transports += 1
        digest.update(f"{r5},{r7},{s}:{a5},{a7},{target_s}\n".encode())
        tuples += 1
    return c5, c7, tuples, len(representatives), transports, digest.hexdigest()


def run(exe, B, b, u, v, fixed, quotient):
    args = [str(exe)] + (["--orbits"] if quotient else [])
    completed = subprocess.run(args, input=encode(B, b, u, v, fixed), text=True,
                               capture_output=True, timeout=50, check=True)
    result = json.loads(completed.stdout)
    phases = []
    require((result["B"], result["C"], result["b"]) == (B, 35, b), "metadata mismatch")
    require(len(result["phases"]) == 4, "incomplete phase witness")
    for d, triple in zip((1, 5, 7, 35), result["phases"]):
        dd, t, r = triple
        require(dd == d and 0 <= t < B and 0 <= r < d, "invalid phase witness")
        require(d not in fixed or (t, r) == fixed[d], "prescribed phase changed")
        phases.append((t, r))
    require(actual_value(B, 35, b, u, v, phases) == result["value"], "literal witness score mismatch")
    return result


def compare(exe, B, b, u, v, fixed, label, inspect_scores=False, original=None):
    c5, c7, full_count, count, transports, digest = audit_quotient(
        B, b, u, v, fixed, inspect_scores)
    full = run(exe, B, b, u, v, fixed, False)
    reduced = run(exe, B, b, u, v, fixed, True)
    require(full["value"] == reduced["value"], "quotient differs from complete maximum")
    require(full["cofactor_tuples"] == full_count == reduced["complete_cofactor_tuples"],
            "full cofactor count mismatch")
    require(reduced["cofactor_tuples"] == count, "quotient representative count mismatch")
    require((reduced["classes5"], reduced["classes7"]) == (c5, c7), "signature partition mismatch")
    require(full["local_candidate_visits"] * count ==
            reduced["local_candidate_visits"] * full_count, "local visit reduction mismatch")
    if original:
        old = run(original, B, b, u, v, fixed, False)
        require(old == full, "default mode differs from original published optimizer")
    return {"label": label, "B": B, "b": b, "fixed": {str(k): list(x) for k, x in fixed.items()},
            "value": full["value"], "full_tuples": full_count, "quotient_tuples": count,
            "full_local_visits": full["local_candidate_visits"],
            "quotient_local_visits": reduced["local_candidate_visits"],
            "classes5": c5, "classes7": c7, "literal_score_transports": transports,
            "cofactor_transport_sha256": digest}


def controls(exe, original, small):
    rng = Random(20261001031)
    cases = []
    for i in range(10):
        B, b = ((6, 1), (12, 2), (18, 3))[i % 3]
        p5 = [0, 1, 1, 2, 2] if i % 3 == 0 else [0, 1, 1, 1, 1]
        p7 = [0, 0, 1, 1, 2, 2, 2] if i % 3 == 0 else [1, 0, 1, 1, 1, 1, 1]
        cats = max(p5) + 1, max(p7) + 1
        def matrix(h):
            layers = [[[rng.randrange(12) for _ in range(cats[1])] for _ in range(cats[0])]
                      for _ in range(h)]
            return [[layers[t][p5[z % 5]][p7[z % 7]] for z in range(35)] for t in range(h)]
        u, v = matrix(B), matrix(b)
        fixed = ({}, {5: (2 % B, 2)}, {7: (3 % B, 4)}, {35: (5 % B, 17)},
                 {5: (1, 0), 7: (2, 6), 35: (3, 14)})[i % 5]
        for t, _ in fixed.values():
            u[t] = [0] * 35
        cases.append(compare(exe, B, b, u, v, fixed, f"structured{i}",
                             inspect_scores=i in (0, 4), original=original if i == 0 else None))
    for i, (u, v) in enumerate((
            ([[0] * 35 for _ in range(6)], [[0] * 35]),
            ([[rng.randrange(1000) for _ in range(35)] for _ in range(6)], [[0] * 35]),
            ([[0] * 35 for _ in range(6)], [[rng.randrange(1000) for _ in range(35)]]))):
        cases.append(compare(exe, 6, 1, u, v, {}, f"fallback{i}"))
    require(cases[-3]["quotient_tuples"] == 4, "uniform full-symmetry quotient mismatch")
    require(all(c["quotient_tuples"] == 1225 for c in cases[-2:]), "asymmetric fallback lost tuples")
    if not small:
        # Literal current research handoff; the complete prefix adapter checks
        # all known classes, actual bitset, all unused resources and fixed tops.
        from application import prepare
        fixture_path = Path(__file__).resolve().parent.parent / "mixed-outside-groups" / "input.json"
        fixture = json.loads(fixture_path.read_text())
        B, _, _, _, _, fixed, _, _, u, v = prepare(fixture, 48)
        cases.append(compare(exe, B, 48, u, v, fixed, "literal10080", original=original))
        require(cases[-1]["quotient_tuples"] == 25 and cases[-1]["value"] == 174,
                "current handoff quotient mismatch")
        for B in (288, 432):
            b = B // 6
            u = [[10 if t in (0, B // 2) else 0 for _ in range(35)] for t in range(B)]
            v = [[int(q == 0 and z == 0) for z in range(35)] for q in range(b)]
            cases.append(compare(exe, B, b, u, v, {}, f"label{B}"))
            require(cases[-1]["value"] == 482 and cases[-1]["quotient_tuples"] == 25,
                    "actual-label benchmark mismatch")
    return cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--optimizer", type=Path, required=True)
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--small", action="store_true")
    args = parser.parse_args()
    exe = args.optimizer.resolve()
    original = args.original.resolve() if args.original else None
    t = monotonic()
    cases = controls(exe, original, args.small)
    rejects = reject_controls(exe)
    text = encode(6, 1, [[0] * 35 for _ in range(6)], [[0] * 35], {})
    for flags in (("--unknown",), ("--orbits", "extra")):
        p = subprocess.run([str(exe), *flags], input=text, text=True, capture_output=True, timeout=5)
        require(p.returncode != 0, "unknown command arguments accepted")
        rejects += 1
    result = {"cases": cases, "rejected_inputs": rejects,
              "original_default_comparisons": (1 if args.small else 2) if original else 0}
    expected = Path(__file__).with_name("expected-small.json" if args.small else "expected.json")
    if expected.exists():
        require(result == json.loads(expected.read_text()), "published orbit output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps({"seconds": round(monotonic() - t, 3)}), file=sys.stderr)


if __name__ == "__main__":
    main()

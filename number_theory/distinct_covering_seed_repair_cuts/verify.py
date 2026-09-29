"""Direct-period capacity replay and direct-coset checking of sufficient cuts."""
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
B = 10080


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify_certificate(certificate):
    seed = json.loads((ROOT / "seed_m7.json").read_text())["congruences"]
    require(all(type(a) is int and type(m) is int and m >= 7 and 0 <= a < m for a, m in seed), "Invalid seed")
    retained = [(a, m) for a, m in seed if m != 7]
    used = {m for a, m in retained}
    require(len(seed) == 66 and len({m for a, m in seed}) == 66, "Incorrect seed size or repeated modulus")
    require(min(m for a, m in seed) == 7 and math.lcm(*(m for a, m in seed)) == B, "Incorrect seed period")
    require(all(any(x % m == a for a, m in seed) for x in range(B)), "The seed does not cover")
    require(used == {d for d in range(8, B+1) if B % d == 0}, "The retained moduli do not exhaust the eligible divisors")
    require(certificate["format_version"] == 1 and certificate["base_lcm"] == B, "Incorrect certificate metadata")
    require(set(certificate["tower_cases"]) == {"3", "4"}, "Incorrect tower scope")
    rows = certificate["capacity_rows_m_t_holes_C"]
    require(len(rows) == 65*4, "Incomplete capacity enumeration")
    capacity = {(m, t): (holes, C) for m, t, holes, C in rows}
    require(len(capacity) == len(rows), "Repeated capacity row")
    require(set(capacity) == {(m, t) for m in used for t in range(1, 5)}, "Incorrect capacity domain")
    survivors = {t: [] for t in range(1, 5)}
    for m in sorted(used):
        fixed = [(a, n) for a, n in retained if n != m]
        require(math.lcm(*(n for a, n in fixed)) == B, "A retained 64-class LCM is not 10080")
        # Mark the actual progressions; the generator instead subtracts predicate counts.
        covered = bytearray(B)
        for a, n in fixed:
            for x in range(a, B, n):
                covered[x] = 1
        H = [x for x in range(B) if not covered[x]]
        fixed_moduli = {n for a, n in fixed}
        for t in range(1, 5):
            L = t*B
            # Literal divisibility scan and literal full-period hole counts.
            available = [d for d in range(8, L+1) if L % d == 0 and d not in fixed_moduli]
            lifted = [x + k*B for k in range(t) for x in H]
            C = sum(max(Counter(x % d for x in lifted).values()) for d in available)
            require(capacity[(m, t)] == (len(lifted), C), "Capacity value differs from direct replay")
            if C >= len(lifted):
                survivors[t].append(m)
    require(not survivors[1] and not survivors[2], "An early period remains unexcluded")
    # Independently form predicate counts for checking the completed fixed phases.
    count = [sum(x % m == a for a, m in retained) for x in range(B)]
    old_residue = {m: a for a, m in retained}
    summaries = []
    for t, p, s, h in [(3, 3, 2, 1), (4, 2, 5, 2)]:
        q, M = p**s, B//p**s
        D = [d for d in range(1, M+1) if M % d == 0]
        copies = p**h
        W = sum(p**(h-j) for j in range(1, h+1))
        cases = certificate["tower_cases"][str(t)]
        expected = {(m, a) for m in survivors[t] for a in range(m)}
        require(len(cases) == len(expected) and {(r[0], r[1]) for r in cases} == expected, "Incomplete phase enumeration")
        minima = {m: None for m in survivors[t]}
        for m, a, N, A, type_count, bound in cases:
            fixed_moduli = used
            actual_new = [d for d in range(8, t*B+1) if t*B % d == 0 and d not in fixed_moduli]
            require(actual_new == sorted(p**(s+j)*d for j in range(1, h+1) for d in D), "Incorrect new-modulus reduction")
            holes = [x for x in range(B)
                     if count[x] - int(x % m == old_residue[m]) + int(x % m == a) == 0]
            groups = {r: [x % M for x in holes if x % q == r] for r in sorted({x % q for x in holes})}
            require(N == copies*len(groups), "Incorrect number of nonempty children")
            require(len(set(A)) == len(A) and all(r in groups for r in A), "Invalid selected parent set")
            # Check every eligible coset directly. No gcd formula or cut optimization.
            T = [d for d in D if any(len({x % d for x in groups[r]}) == 1 for r in A)]
            computed = N + copies*len(A) - W*len(T)
            require(type_count == len(T) and bound == computed and bound > W*len(D), "The recorded resource cut is not strict")
            minima[m] = bound if minima[m] is None else min(minima[m], bound)
        summaries.append({"multiplier": t, "period": t*B, "phase_cases": len(cases),
                          "resource": W*len(D), "minimum_bounds_by_freed_modulus": minima})
    return {"agent": "six-covering-1", "role": "researcher", "retained_seed_classes": 65,
            "required_fixed_classes": 64, "capacity_rows_checked": len(rows),
            "capacity_survivors": survivors, "tower_exclusions": summaries,
            "local_lcm_lower_bound": 50400}


if __name__ == "__main__":
    certificate = json.loads((ROOT / "certificate.json").read_text())
    result = verify_certificate(certificate)
    expected = json.loads((ROOT / "expected.json").read_text())
    require(json.loads(json.dumps(result)) == expected, "Unexpected summary")
    print(json.dumps(result, sort_keys=True))
    print("CERTIFICATE VERIFIED", hashlib.sha256((ROOT / "certificate.json").read_bytes()).hexdigest())

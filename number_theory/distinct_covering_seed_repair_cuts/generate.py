"""Generate compact sufficient cuts; verification does not import this module."""
import itertools
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
B = 10080


def divisors(n):
    small = [d for d in range(1, math.isqrt(n) + 1) if n % d == 0]
    return sorted(set(small + [n // d for d in small]))


def generate():
    seed = json.loads((ROOT / "seed_m7.json").read_text())["congruences"]
    retained = [(a, m) for a, m in seed if m != 7]
    count = [sum(x % m == a for a, m in retained) for x in range(B)]
    used = {m for a, m in retained}
    capacity_rows = []
    survivors = {t: [] for t in range(1, 5)}
    for old_a, m in retained:
        H = [x for x in range(B) if count[x] - int(x % m == old_a) == 0]
        weights = {g: max(Counter(x % g for x in H).values()) for g in divisors(B)}
        for t in range(1, 5):
            available = [d for d in divisors(t*B) if d >= 8 and (d not in used or d == m)]
            total = sum((t*math.gcd(B, d)//d)*weights[math.gcd(B, d)] for d in available)
            capacity_rows.append([m, t, t*len(H), total])
            if total >= t*len(H):
                survivors[t].append(m)
    certificate = {"format_version": 1, "base_lcm": B,
                   "capacity_rows_m_t_holes_C": capacity_rows, "tower_cases": {}}
    for t, p, s, h in [(3, 3, 2, 1), (4, 2, 5, 2)]:
        q = p**s
        M = B//q
        D = divisors(M)
        copies = p**h
        W = sum(p**(h-j) for j in range(1, h+1))
        cases = []
        for m in survivors[t]:
            old_a = next(a for a, n in retained if n == m)
            for a in range(m):
                H = [x for x in range(B)
                     if count[x] - int(x % m == old_a) + int(x % m == a) == 0]
                parents = []
                for r in sorted({x % q for x in H}):
                    U = [x % M for x in H if x % q == r]
                    g = math.gcd(M, *(z-U[0] for z in U))
                    parents.append((r, g))
                N = copies*len(parents)
                best = (N, [], 0)
                if len(parents) <= 9:
                    for k in range(1, len(parents)+1):
                        for A in itertools.combinations(parents, k):
                            T = [d for d in D if any(g % d == 0 for r, g in A)]
                            bound = N + copies*k - W*len(T)
                            if bound > best[0]:
                                best = (bound, [r for r, g in A], len(T))
                bound, A, types = best
                if bound <= W*len(D):
                    raise ValueError("This case has no sufficient cut")
                cases.append([m, a, N, A, types, bound])
        certificate["tower_cases"][str(t)] = cases
    return certificate


if __name__ == "__main__":
    certificate = generate()
    (ROOT / "certificate.json").write_text(json.dumps(certificate, separators=(",", ":")) + "\n")
    print(json.dumps({"capacity_rows": len(certificate["capacity_rows_m_t_holes_C"]),
                      "tower_cases": {t: len(rows) for t, rows in certificate["tower_cases"].items()}}, sort_keys=True))

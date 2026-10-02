#!/usr/bin/env python3
"""Independent row-by-row exact-cover census; no pair join or quotient map."""
from itertools import combinations, combinations_with_replacement, permutations, product
from collections import Counter
import hashlib, json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


GROUND = tuple(combinations(range(5), 2))
POS = {p: i for i, p in enumerate(GROUND)}
PAIRS = tuple(combinations(range(10), 2))
RED = tuple((i, j) for i, j in PAIRS if not set(GROUND[i]) & set(GROUND[j]))
BLUE = tuple(p for p in PAIRS if p not in RED)
N = tuple(sum(1 << j for j in range(10) if (min(i, j), max(i, j)) in RED) for i in range(10))
STARS = tuple(sum(1 << i for i, p in enumerate(GROUND) if t in p) for t in range(5))
LOW = tuple(z for z in range(1024) if 5 <= z.bit_count() <= 7)
FULL = {k: tuple(z for z in range(1024) if z.bit_count() == k and all((N[i] & (1023 ^ z)).bit_count() <= 1 for i in range(10) if not z >> i & 1)) for k in (5, 6)}
REDMASK = tuple(sum(1 << t for t, (i, j) in enumerate(RED) if z >> i & z >> j & 1) for z in range(1024))
BLUEMASK = tuple(sum(1 << t for t, (i, j) in enumerate(BLUE) if z >> i & z >> j & 1) for z in range(1024))
MAPS = tuple((p, tuple(POS[tuple(sorted((p[a], p[b])))] for a, b in GROUND)) for p in permutations(range(5)))


def move(z, im):
    return sum(1 << im[i] for i in range(10) if z >> i & 1)


def key_orbit(key):
    lo, hi, mu = key
    answer = set()
    for p, im in MAPS:
        m = [0] * 5
        for t, n in enumerate(mu):
            m[p[t]] = n
        answer.add((tuple(sorted(move(z, im) for z in lo)), tuple(sorted(move(z, im) for z in hi)), tuple(m)))
    return answer


def full_cohorts():
    choices = {()} | {(z,) for k in (5, 6) for z in FULL[k]} | {tuple(h) for h in combinations_with_replacement(FULL[5], 2) if not REDMASK[h[0]] & REDMASK[h[1]]}
    cohorts = []
    remain = set(choices)
    while remain:
        h = min(remain)
        orbit = {tuple(sorted(move(z, im) for z in h)) for p, im in MAPS}
        need(orbit <= remain, "full-large orbits overlap or escape complete domain")
        cohorts.append((h, len(orbit)))
        remain -= orbit
    need(sum(n for h, n in cohorts) == len(choices), "full-large coverage")
    return cohorts


# Bit sets index candidate *rows*, not ground incidence coordinates.
ALL = (1 << len(LOW)) - 1
CONTAIN = tuple(sum(1 << a for a, z in enumerate(LOW) if z >> i & 1) for i in range(10))
EDGE = tuple(sum(1 << a for a, z in enumerate(LOW) if REDMASK[z] >> i & 1) for i in range(15))
BPAIR = tuple(sum(1 << a for a, z in enumerate(LOW) if BLUEMASK[z] >> i & 1) for i in range(30))
SIZE = {k: sum(1 << a for a, z in enumerate(LOW) if z.bit_count() == k) for k in (5, 6, 7)}
INDEX = {z: a for a, z in enumerate(LOW)}


def bit_indices(bits):
    while bits:
        b = bits & -bits
        yield b.bit_length() - 1
        bits ^= b


def one_cohort(highs, multiplicity_cap=2):
    """Enumerate mu explicitly and choose one ordered low row at a time.

    Residual columns are unary threshold bitplanes. Every recursion step exhausts
    all candidate rows satisfying necessary capacity and completion constraints.
    With one row left, the ten residual columns determine that row uniquely.
    """
    found = set()
    stats = Counter()
    hr = 0
    for z in highs:
        need(not hr & REDMASK[z], "full-large red repetition")
        hr |= REDMASK[z]
    initial_allowed = ALL
    for t in bit_indices(hr):
        initial_allowed &= ~EDGE[t]
    need(multiplicity_cap in (2, 3), "supported multiplicity cap")
    for mu in product(range(multiplicity_cap+1), repeat=5):
        if sum(mu) != 7 - len(highs):
            continue
        rows = list(highs) + [s for s, n in zip(STARS, mu) for _ in range(n)]
        residual = tuple(5 - sum(z >> i & 1 for z in rows) for i in range(10))
        if any(r < 0 or r > 4 for r in residual):
            continue
        bcounts = tuple(sum(z >> i & z >> j & 1 for z in rows) for i, j in BLUE)
        if any(c > 3 for c in bcounts):
            continue
        stats["full_choices"] += 1
        planes = tuple(sum(1 << i for i, r in enumerate(residual) if r >= t) for t in (1, 2, 3, 4))

        def visit(chosen, remaining, allowed, bc):
            stats["row_nodes_" + str(len(chosen))] += 1
            left = 4 - len(chosen)
            if left == 1:
                if remaining[1]:
                    return
                z = remaining[0]
                a = INDEX.get(z)
                if a is None or not allowed >> a & 1:
                    return
                if any(bc[t] + (BLUEMASK[z] >> t & 1) > 3 for t in range(30)):
                    return
                key = (tuple(chosen + [z]), tuple(highs), tuple(mu))
                need(key not in found, "repeated row-by-row solution")
                found.add(key)
                return
            forced = remaining[left - 1]
            forbid = 1023 ^ remaining[0]
            pool = allowed
            for i in bit_indices(forced):
                pool &= CONTAIN[i]
            for i in bit_indices(forbid):
                pool &= ~CONTAIN[i]
            total = sum(x.bit_count() for x in remaining)
            sizebits = 0
            for k in (5, 6, 7):
                if 5 * (left - 1) <= total - k <= 7 * (left - 1):
                    sizebits |= SIZE[k]
            pool &= sizebits
            for t, c in enumerate(bc):
                if c == 3:
                    pool &= ~BPAIR[t]
            for a in bit_indices(pool):
                z = LOW[a]
                after = tuple((remaining[t] & ~z) | ((remaining[t + 1] if t < 3 else 0) & z) for t in range(4))
                next_allowed = allowed & (ALL ^ ((1 << a) - 1))
                for t in bit_indices(REDMASK[z]):
                    next_allowed &= ~EDGE[t]
                next_bc = tuple(c + (BLUEMASK[z] >> t & 1) for t, c in enumerate(bc))
                visit(chosen + [z], after, next_allowed, next_bc)

        visit([], planes, initial_allowed, bcounts)
    return found, dict(sorted(stats.items()))


def census(multiplicity_cap=2):
    keys = set()
    info = []
    for h, n in full_cohorts():
        found, stats = one_cohort(h, multiplicity_cap)
        expanded = set()
        for key in found:
            expanded.update(key_orbit(key))
        need(not keys & expanded, "overlapping full-cohort incidence keys")
        keys.update(expanded)
        info.append({"highs": h, "high_orbit": n, "canonical_keys": len(found), "raw_keys": len(expanded), "search": stats})
    return keys, info


if __name__ == "__main__":
    import argparse, time
    p = argparse.ArgumentParser()
    p.add_argument("--cohort", type=int)
    p.add_argument("--multiplicity-cap", type=int, default=2)
    args = p.parse_args()
    start = time.monotonic()
    if args.cohort is not None:
        h, n = full_cohorts()[args.cohort]
        keys, info = one_cohort(h, args.multiplicity_cap)
        print(json.dumps({"highs": h, "keys": len(keys), "hash": digest(sorted(keys)), "stats": info, "seconds": time.monotonic()-start}, indent=2))
    else:
        keys, info = census(args.multiplicity_cap)
        print(json.dumps({"records": len(keys), "hash": digest(sorted(keys)), "cohorts": info, "seconds": time.monotonic()-start}, indent=2))

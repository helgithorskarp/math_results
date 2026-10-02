#!/usr/bin/env python3
"""Exact row enumeration for the stated Case-II leaf sector; Python stdlib."""
from collections import Counter
from itertools import combinations, product
from math import comb
import hashlib
import json
import sys
import time

CYCLE = ((0, 4), (4, 3), (3, 1), (1, 2), (2, 5), (5, 0))
OWN = (40, 20)
MINIMUM = (2, 2, 1, 1, 1, 1)


def masks(n):
    return tuple(sum(1 << i for i in row) for row in combinations(range(6), n))


def frame(lows, columns, special, beta):
    red = [0] * 16

    def edge(i, j):
        red[i] |= 1 << j
        red[j] |= 1 << i

    for z in (1, 2, *range(3, 11)):
        edge(0, z)
    for z in (2, 11, 12):
        edge(1, z)
    for z in range(9, 16):
        edge(2, z)
    for i, j in CYCLE:
        edge(3 + i, 3 + j)
    for s in range(2):
        for i in range(6):
            if OWN[s] & (1 << i):
                edge(9 + s, 3 + i)
            if special[s] & (1 << i):
                edge(11 + s, 3 + i)
    for i in range(8):
        for t in range(3):
            if columns[i] & (1 << t):
                edge(3 + i, 13 + t)
    for s in range(2):
        for t in range(3):
            if (5, 3)[s] & (1 << t):
                edge(11 + s, 13 + t)
    degrees = (10, 10, 9, *([10] * 8), 10-lows[3], 10-lows[4],
               *(10-lows[t] for t in range(3)))
    outside = (0, 6, 0, *(3+b for b in beta), 4, 4, 2, 2, 2, 3, 3)
    if tuple(red[i].bit_count()+outside[i] for i in range(16)) != degrees:
        raise ValueError("actual tagged degree mismatch")
    if sum(beta) != 1+sum(lows):
        raise ValueError("ordinary block edge budget mismatch")
    for i, j in combinations(range(16), 2):
        lower = (red[i] & red[j]).bit_count() + max(0, outside[i]+outside[j]-6)
        cap = 3 if red[i] & (1 << j) else degrees[i]+degrees[j]-14
        if lower > cap:
            return False
    return True


def close(domain):
    """Symbolic overlap caps; enumerate every labeled SX pair on six points."""
    fours, threes = masks(4), masks(3)
    sx_pairs = tuple((a, b) for a, b in product(fours, repeat=2)
                     if (a & b).bit_count() == 2)
    if len(sx_pairs) != 90:
        raise ValueError("six-point SX coverage")
    finish = Counter()
    frames = pairs = 0
    for lows, c, _, _, _ in domain:
        rows = tuple(sum(((c[i] >> t) & 1) << i for i in range(6))
                     for t in range(3))
        overlap = tuple(tuple((row & own).bit_count() for own in OWN)
                        for row in rows[1:])
        if any(min(p) > 0 for p in overlap):
            finish["union_obstruction"] += 1
        else:
            if lows[1:3] != (0, 0):
                raise ValueError("remaining T endpoints must have degree ten")
            if any(row.bit_count() != 3 or row & 3 != 3 for row in rows[1:]):
                raise ValueError("remaining T ordinary-X rows")
            if any(sorted(p) != [0, 1] for p in overlap):
                raise ValueError("remaining own-SX overlaps")
            finish["two_T_three_sets_obstruction"] += 1
        common_known = 3 + (rows[1] & rows[2]).bit_count()
        cap = 6-lows[1]-lows[2]
        for a, b in sx_pairs:
            frames += 1
            choices = []
            for p in overlap:
                choices.append(tuple(z for z in threes
                    if 1+p[0]+(z & a).bit_count() <= 3
                    and 1+p[1]+(z & b).bit_count() <= 3))
            for z1, z2 in product(*choices):
                if common_known+(z1 & z2).bit_count() <= cap:
                    pairs += 1
    if pairs:
        raise ValueError("Y completion survives the selected mixed spines")
    return {"union_obstruction": finish["union_obstruction"],
            "two_T_three_sets_obstruction": finish["two_T_three_sets_obstruction"],
            "labeled_SX_Y_frames": frames, "compatible_T_Y_row_pairs": pairs}


def derive():
    start = time.monotonic()
    pools = {n: masks(n) for n in range(2, 6)}
    domain = []
    flags = tuple(l for l in product(range(2), repeat=5) if sum(l) <= 3)
    for lows in flags:
        for rows in product(pools[5-lows[0]], pools[3-lows[1]], pools[3-lows[2]]):
            c = tuple(sum(int(bool(rows[t] & (1 << i))) << t for t in range(3))
                      for i in range(6)) + (6, 6)
            k = tuple(c[i].bit_count()-MINIMUM[i] for i in range(6))
            if min(k) < 0:
                continue
            if sum(k) != 3-sum(lows[:3]):
                raise ValueError("T row budget mismatch")
            if any((c[i] & c[j]).bit_count() > min(2, k[i]+k[j]) for i, j in CYCLE):
                continue
            if any((6 & c[i]).bit_count() > min(2, 1+k[i])
                   for s in range(2) for i in range(6) if OWN[s] & (1 << i)):
                continue
            for special in product(pools[4-lows[3]], pools[4-lows[4]]):
                beta = tuple(2-k[i]-sum(int(bool(row & (1 << i))) for row in special)
                             for i in range(6))
                if min(beta) < 0 or max(beta) > 2:
                    continue
                if frame(lows, c, special, beta):
                    domain.append((lows, c, special[0], special[1], beta))
        if time.monotonic()-start > 30:
            raise RuntimeError("30-second guard: incomplete computation proves no exclusion")
    domain.sort()
    if any(item[0][0] != 1 for item in domain):
        raise ValueError("T0 degree-nine refinement fails")
    counts = Counter(item[0] for item in domain)
    tag_coverage = [{"low_T0_T1_T2_SY0_SY1": lows,
                     "ordinary_Y_low_count": 3-sum(lows),
                     "labeled_ordinary_Y_choices": comb(6, 3-sum(lows)),
                     "X_interfaces": counts[lows]} for lows in flags]
    finish = close(domain)
    if time.monotonic()-start > 30:
        raise RuntimeError("30-second guard: incomplete finish proves no exclusion")
    return {"schema": 1, "agent": "six-books-1", "role": "researcher",
            "scope": "specified one-nine leaf; red degrees 9^4,10^18; both SX omit T0",
            "flag_words": len(flags),
            "labeled_actual_low_placements": sum(x["labeled_ordinary_Y_choices"] for x in tag_coverage),
            "tag_coverage": tag_coverage, "X_interface_count": len(domain),
            "X_domain_sha256": hashlib.sha256(json.dumps(domain, separators=(",", ":")).encode()).hexdigest(),
            "X_domain": domain, "every_X_interface_has_T0_degree9": True,
            "finish": finish}


if __name__ == "__main__":
    json.dump(derive(), sys.stdout, separators=(",", ":"))
    print()

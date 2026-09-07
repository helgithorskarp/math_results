"""Two complete F27 cut branches and streamed Ramsey CNF statistics.

No SAT invocation. Every unpinned physical pair remains an independent bit.
Compatible-clique enumeration constructs clauses; check_branches.py instead
inspects every physical five-set and both colors.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations

A = list(range(2, 12)) + [27, 28]
B = list(range(12, 22)) + [29, 30]


def frame():
    pins = {(0, 1): 1}
    for base in (2, 7, 12, 17, 22):
        for i, j in combinations(range(5), 2):
            pins[base + i, base + j] = int(j - i in (1, 4))
    for u in (0, 1):
        for v in range(2, 7):
            pins[u, v] = 1
    return pins


def compatible_fives(adjacency, candidates, chosen=()):
    if len(chosen) == 5:
        yield chosen
    else:
        while candidates.bit_count() >= 5 - len(chosen):
            bit = candidates & -candidates
            candidates ^= bit
            u = bit.bit_length() - 1
            yield from compatible_fives(adjacency, candidates & adjacency[u], chosen + (u,))


def certificate():
    pairs = list(combinations(range(43), 2))
    pins = frame()
    numbers = {e: i + 1 for i, e in enumerate(e for e in pairs if e not in pins)}
    cross = sorted(tuple(sorted((a, b))) for a in A for b in B)
    if len(set(cross)) != 144 or any(e in pins for e in cross):
        raise ValueError("cross branch conflicts with F27")
    rows = []
    for cross_color in (0, 1):
        fixed = pins | dict.fromkeys(cross, cross_color)
        histogram = Counter()
        counts = Counter()
        stream = sha256()
        byte_count = 0
        for color in (1, 0):
            adjacency = [0] * 43
            for u, v in pairs:
                if fixed.get((u, v), color) == color:
                    adjacency[u] |= 1 << v
                    adjacency[v] |= 1 << u
            for vs in compatible_fives(adjacency, (1 << 43) - 1):
                clause = [(-1 if color else 1) * numbers[e]
                          for e in combinations(vs, 2) if e not in fixed]
                line = (" ".join(map(str, clause)) + (" " if clause else "") + "0\n").encode()
                stream.update(line)
                byte_count += len(line)
                histogram[len(clause)] += 1
                counts[color] += 1
        rows.append({"cross_color": cross_color, "fixed_pairs": len(fixed),
                     "free_physical_pairs": 903 - len(fixed),
                     "ramsey_clauses": sum(counts.values()),
                     "red_clauses": counts[1], "blue_clauses": counts[0],
                     "length_histogram": {str(k): v for k, v in sorted(histogram.items())},
                     "literal_body_bytes": byte_count, "literal_body_sha256": stream.hexdigest(),
                     "cut_nogood_in_F27_variables": [(1 if cross_color == 0 else -1) * numbers[e] for e in cross]})
    return {"n": 43, "frame_pins": [[u, v, c] for (u, v), c in sorted(pins.items())],
            "frame_free_variables": len(numbers), "a": A, "b": B,
            "separator": sorted(set(range(43)) - set(A) - set(B)), "branches": rows}

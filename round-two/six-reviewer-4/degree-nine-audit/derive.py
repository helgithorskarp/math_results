"""Algebraic histogram producer; independent of the author and of verify.py.

Only necessary four-corner incidences are enumerated, never host colorings.
"""
from itertools import combinations, product
import json

PAIRS = tuple(combinations(range(4), 2))
EDGES = {(0, 1), (1, 2), (2, 3), (0, 3)}
H = (3, 3, 2, 3)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def record(delta_position, collision, counts):
    return {"deficient_corner": delta_position,
            "shared_extra_pair": list(collision) if collision else [],
            "blue_word_counts": [[w, c] for w, c in enumerate(counts) if c]}


def enumerate_near():
    result = []
    for dpos in range(4):
        delta = [int(i == dpos) for i in range(4)]
        margins = [H[i] + 3 + delta[i] for i in range(4)]
        for collision in (None, (0, 1), (0, 3), (1, 3)):
            common = [int(ij not in EDGES) * 2 + int(ij == collision)
                      for ij in PAIRS]
            caps = [(H[i] + H[j] - 4 + delta[i] + delta[j] if (i, j) in EDGES
                     else H[i] + H[j] - 1) - c
                    for (i, j), c in zip(PAIRS, common)]
            # The proved slack identity and sum r=24 leave either all pairs,
            # or one singleton, one triple, and ten pairs.
            higher_rows = [(None, None)] + list(product(range(4), (7, 11, 13, 14)))
            for single, triple in higher_rows:
                counts = [0] * 16
                if single is not None:
                    counts[1 << single] = counts[triple] = 1
                resid = [margins[i] - sum(counts[w] for w in range(16) if w >> i & 1)
                         for i in range(4)]
                twice_k = sum(resid[:3]) - resid[3]
                if twice_k % 2:
                    continue
                for x01, x02 in product(range(13), repeat=2):
                    x03 = resid[0] - x01 - x02
                    x12 = twice_k // 2 - x01 - x02
                    x13 = resid[1] - x01 - x12
                    x23 = resid[2] - x02 - x12
                    vals = (x01, x02, x03, x12, x13, x23)
                    if min(vals) < 0:
                        continue
                    cc = counts[:]
                    for (i, j), value in zip(PAIRS, vals):
                        cc[(1 << i) | (1 << j)] = value
                    if sum(cc) != 12:
                        continue
                    joints = [sum(cc[w] for w in range(16) if w >> i & 1 and w >> j & 1)
                              for i, j in PAIRS]
                    if all(value <= cap for value, cap in zip(joints, caps)):
                        result.append(record(dpos, collision, cc))
    require(len(result) == 13, "unexpected near-equality count")
    result.sort(key=lambda r: (r["deficient_corner"], r["shared_extra_pair"], r["blue_word_counts"]))
    return result


def enumerate_equal():
    profiles = []
    for deficient_local in range(4):
        h = [2 if i == deficient_local else 3 for i in range(4)]
        pair_counts = [(h[i] + h[j] - 4 if ij in EDGES else h[i] + h[j] - 3)
                       for ij in PAIRS for i, j in [ij]]
        counts = [0] * 16
        for (i, j), value in zip(PAIRS, pair_counts):
            counts[(1 << i) | (1 << j)] = value
        for i in range(4):
            counts[1 << i] = h[i] + 3 - sum(counts[w] for w in range(16) if w >> i & 1)
        require(min(counts) >= 0 and sum(counts) == 12, "equality histogram")
        profiles.append({"local_degree_two_corner": deficient_local,
                         "blue_word_counts": [[w, c] for w, c in enumerate(counts) if c]})
    return profiles


def leaf_words():
    groups = {"repeat_X": [], "repeat_Y": [], "cross": []}
    for omitted in product(range(3), repeat=4):
        if sorted(omitted.count(t) for t in range(3)) != [1, 1, 2]:
            continue
        word = sum((7 ^ (1 << t)) << (3 * i) for i, t in enumerate(omitted))
        repeated = next(t for t in range(3) if omitted.count(t) == 2)
        positions = [i for i, t in enumerate(omitted) if t == repeated]
        name = "repeat_X" if positions == [0, 1] else "repeat_Y" if positions == [2, 3] else "cross"
        groups[name].append(word)
    return {k: sorted(v) for k, v in groups.items()}


def produce():
    return {"equality_profiles": enumerate_equal(), "leaf_words": leaf_words(),
            "near_equality": enumerate_near(),
            "near_equality_counts_by_deficient_corner": [1, 4, 4, 4],
            "caseI_deficient_T_remaining_words": sorted([
                [[3, 2], [5, 2], [6, 2], [9, 2], [10, 2], [12, 2]],
                [[1, 1], [3, 1], [5, 2], [6, 2], [9, 1], [10, 2], [11, 1], [12, 2]]]),
            "row_cost_by_blue_rank": [1, 0, 0, 1, 3]}


if __name__ == "__main__":
    print(json.dumps(produce(), sort_keys=True, indent=2))

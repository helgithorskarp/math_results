#!/usr/bin/env python3
"""Independent histogram/row-subset and literal 22-point controls.

Imports no producer. Graph frames validate selected spines and identities;
unselected edges may violate books. They are not valid-host witnesses.
"""
from copy import deepcopy
from itertools import combinations, product
from pathlib import Path
import argparse
import json
import sys


def require(value, message):
    if not value:
        raise ValueError(message)


def blank():
    return [[False] * 22 for _ in range(22)]


def add(g, i, j):
    g[i][j] = g[j][i] = True


def pages(g, i, j, red):
    return sum(g[i][k] == red and g[j][k] == red
               for k in range(22) if k not in (i, j))


def equality_frame(q, word_counts):
    g = blank()
    for j in range(1, 10):
        add(g, 0, j)
    for i, j in ((1, 2), (2, 3), (3, 4), (4, 1)):
        add(g, i, j)
    for i in range(4):
        if i != q:
            add(g, i + 1, i + 5)
    b = 10
    for word, count in enumerate(word_counts):
        for _ in range(count):
            for i in range(4):
                if not (word & (1 << i)):
                    add(g, b, i + 1)
            b += 1
    require(b == 22, "twelve physical outside rows")
    return g


def cycle_records():
    pairs = tuple(combinations(range(4), 2))
    answer = []
    histograms_tested = 0
    for q in range(4):
        local_degrees = [2 if i == q else 3 for i in range(4)]
        margins = [h + 3 for h in local_degrees]
        caps = []
        for i, j in pairs:
            red = (j - i) in (1, 3)
            # Count the two opposite common neighbors in the literal cycle.
            common = sum((k - i) % 4 in (1, 3)
                         and (k - j) % 4 in (1, 3) for k in range(4))
            caps.append(local_degrees[i] + local_degrees[j]
                        + (5 if red else 8) - 9 - common)
        survivors = []
        for mult in product(*(range(c + 1) for c in caps)):
            histograms_tested += 1
            singles = [margins[i] - sum(n for p, n in zip(pairs, mult)
                                       if i in p) for i in range(4)]
            if min(singles) < 0 or sum(singles) + sum(mult) != 12:
                continue
            counts = [0] * 16
            for i, count in enumerate(singles):
                counts[1 << i] = count
            for (i, j), count in zip(pairs, mult):
                counts[(1 << i) | (1 << j)] = count
            survivors.append(counts)
        require(len(survivors) == 1, "unique equality incidence multiset")
        counts = survivors[0]
        g = equality_frame(q, counts)
        require(sum(g[0]) == 9 and all(sum(g[i]) == 10 for i in range(1, 5)),
                "physical equality root/corner degrees")
        for i, j in pairs:
            red = g[i + 1][j + 1]
            require(pages(g, i + 1, j + 1, red) == (3 if red else 6),
                    "all six physical colored spines saturated")
        actual_h = [sum(g[i + 1][j] for j in range(1, 10)) for i in range(4)]
        actual_margins = [sum(not g[i + 1][b] for b in range(10, 22))
                          for i in range(4)]
        actual_caps = [sum(not g[i + 1][b] and not g[j + 1][b]
                           for b in range(10, 22)) for i, j in pairs]
        actual_words = [0] * 16
        for b in range(10, 22):
            word = sum(int(not g[i + 1][b]) << i for i in range(4))
            actual_words[word] += 1
        opposite = (q + 2) % 4
        block = {b for b in range(10, 22) if g[opposite + 1][b]}
        p, r = (opposite + 1) % 4, (opposite + 3) % 4
        left = {b for b in block if g[p + 1][b]}
        right = {b for b in block if g[r + 1][b]}
        answer.append({"h": actual_h, "blue_margins": actual_margins,
                       "pair_caps": actual_caps, "blue_word_counts": actual_words,
                       "outside_red_block": [len(block), len(left), len(right),
                                             len(left & right)]})
    require(histograms_tested == 1728, "four complete 432-histogram domains")
    return answer


def weighted_identity_controls():
    # These varied frames are usually invalid hosts. Test exact identities and
    # equivalent page-cap inequalities, including signed negative deficits.
    trials = negative_deficit_frames = 0
    for d in range(4, 18):
        for seed in range(24):
            g = blank()
            for i in range(1, d + 1):
                add(g, 0, i)
            for i, j in ((1, 2), (2, 3), (3, 4), (4, 1)):
                add(g, i, j)
            if d > 4:
                for i in range(4):
                    if (seed >> i) & 1:
                        add(g, i + 1, 5 + ((seed + i) % (d - 4)))
            for b in range(d + 1, 22):
                word = ((b * 7 + seed * 3) ^ (b // 3)) % 16
                for i in range(4):
                    if not (word & (1 << i)):
                        add(g, b, i + 1)
            h = [sum(g[i + 1][j] for j in range(1, d + 1)) for i in range(4)]
            delta = [10 - sum(g[i + 1]) for i in range(4)]
            negative_deficit_frames += int(min(delta) < 0)
            misses = [{b for b in range(d + 1, 22) if not g[i + 1][b]}
                      for i in range(4)]
            require([len(w) for w in misses] ==
                    [h[i] + 12 - d + delta[i] for i in range(4)],
                    "signed blue-column margins")
            for i, j in combinations(range(4), 2):
                red = g[i + 1][j + 1]
                common = sum(g[i + 1][k] and g[j + 1][k]
                             for k in range(1, d + 1))
                joint = len(misses[i] & misses[j])
                physical = pages(g, i + 1, j + 1, red)
                if red:
                    formula = 1 + common + 21 - d - len(misses[i]) - len(misses[j]) + joint
                    cap = h[i] + h[j] + delta[i] + delta[j] + 5 - d - common
                else:
                    formula = d - 2 - h[i] - h[j] + common + joint
                    cap = h[i] + h[j] + 8 - d - common
                require(physical == formula, "physical colored-page identity")
                require((physical <= (3 if red else 6)) == (joint <= cap),
                        "equivalent joint-miss bound")
            trials += 1
    require(trials == 336 and negative_deficit_frames > 0,
            "general-root/signed-deficit identity coverage")
    return {"weighted_identity_frames": trials,
            "frames_with_negative_corner_deficit": negative_deficit_frames,
            "literal_cycle_spines": 24, "pair_histograms": 1728}


def leaf_frame(rows):
    # a=0,u=1,v=2,SX=3,4,SY=5,6,T=7..9; ordinary X=10..15,Y=16..21.
    g = blank()
    for j in range(1, 10):
        add(g, 0, j)
    add(g, 1, 2)
    for x in (3, 4, *range(10, 16)):
        add(g, 1, x)
    for y in (5, 6, *range(16, 22)):
        add(g, 2, y)
    for i, j in ((10, 14), (14, 13), (13, 11), (11, 12), (12, 15), (15, 10),
                 (3, 13), (3, 15), (4, 12), (4, 14),
                 (5, 16), (5, 17), (6, 18), (6, 19)):
        add(g, i, j)
    for t, row in enumerate(rows):
        for i in row:
            add(g, t + 7, i + 3)
    return g


def leaf_records():
    subsets = [frozenset(i for i in range(4) if word & (1 << i)) for word in range(16)]
    classes = {"X_repeat": [], "Y_repeat": [], "cross_repeat": []}
    splits = set()
    physical_cycles = 0
    for rows in product(subsets, repeat=3):
        if any(sum(i in row for row in rows) != 2 for i in range(4)):
            continue
        if sorted(map(len, rows)) != [2, 3, 3]:
            continue
        g = leaf_frame(rows)
        require([sum(g[i]) for i in (0, 1, 2)] == [9, 10, 10], "leaf root degrees")
        require([k for k in range(22) if g[1][k] and g[2][k]] == [0], "sole uv page")
        a = {i for i in range(22) if g[0][i]}
        t = next(i + 7 for i, row in enumerate(rows) if len(row) == 2)
        if g[t][5] and g[t][6]:
            name, corners = "X_repeat", (2, 5, t, 6)
        elif g[t][3] and g[t][4]:
            name, corners = "Y_repeat", (1, 3, t, 4)
        else:
            name, corners = "cross_repeat", None
        if corners:
            require([sum(g[c][k] for k in a) for c in corners] == [3, 3, 2, 3],
                    "distinguished leaf-cycle local degrees")
            require(all(g[corners[i]][corners[j]] == ((j - i) in (1, 3))
                        for i, j in combinations(range(4), 2)), "induced leaf cycle")
            physical_cycles += 1
        if name == "X_repeat":
            for tx, ty in ((5, 4), (4, 5)):
                frame = deepcopy(g)
                for x in range(10, 10 + tx):
                    add(frame, t, x)
                for y in range(16, 16 + ty - 2):
                    add(frame, t, y)
                require(sum(frame[t]) == sum(frame[2]) == 10, "full v,T split control")
                blue = pages(frame, 2, t, False)
                require(blue == 1 + ty, "literal full v--T blue identity")
                splits.add((tx, ty, blue))
        word = sum(int(g[s + 3][t0 + 7]) << (3 * s + t0)
                   for s in range(4) for t0 in range(3))
        classes[name].append(word)
    require(physical_cycles == 12 and sorted(map(len, classes.values())) == [6, 6, 24],
            "complete 36-core/12-cycle partition")
    sets = [[old for old in range(2, 8) if g[s][old + 8]] for s in (3, 4)]
    # The sets were read from the literal fixed leaf, with its original labels.
    return {"leaf_core_words": {k: sorted(v) for k, v in sorted(classes.items())},
            "leaf_core_counts": {k: len(v) for k, v in sorted(classes.items())},
            "leaf_X_special_ordinary_red_sets": sets,
            "leaf_X_special_ordinary_red_overlap": len(set(sets[0]) & set(sets[1])),
            "caseII_full_T_degree_splits": [list(t) for t in sorted(splits, reverse=True)]}


def validate(stored, actual):
    require(type(stored) is dict and stored.keys() == actual.keys(), "exact record fields")
    # JSON equality treats True like 1, so also require identical serialized types.
    require(json.dumps(stored, sort_keys=True) == json.dumps(actual, sort_keys=True),
            "complete typed mathematical record mismatch")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    actual = {"cycle_profiles": cycle_records(),
              "row_costs_by_blue_rank": [r * (r - 1) // 2 - r + 1 for r in range(5)],
              **leaf_records()}
    coverage = weighted_identity_controls()
    stored = json.loads((Path(__file__).parent / "EXPECTED.json").read_text())
    validate(stored, actual)
    if args.self_test:
        damages = []
        for key, index, value in (("pair_caps", 4, 2), ("blue_word_counts", 4, 0),
                                  ("outside_red_block", 3, 0), ("blue_word_counts", 4, True)):
            bad = deepcopy(stored); bad["cycle_profiles"][2][key][index] = value; damages.append(bad)
        bad = deepcopy(stored); bad["leaf_core_words"]["Y_repeat"].pop(); damages.append(bad)
        bad = deepcopy(stored); bad["leaf_core_counts"]["cross_repeat"] = 36; damages.append(bad)
        bad = deepcopy(stored); bad["leaf_X_special_ordinary_red_overlap"] = 1; damages.append(bad)
        bad = deepcopy(stored); bad["caseII_full_T_degree_splits"][0][2] = 6; damages.append(bad)
        for bad in damages:
            try:
                validate(bad, actual)
            except ValueError:
                continue
            raise ValueError("damaged record accepted")
        print(json.dumps({"damages_rejected": len(damages)}, sort_keys=True))
    else:
        print(json.dumps(actual, indent=2, sort_keys=True))
    print(json.dumps(coverage, sort_keys=True), file=sys.stderr)


if __name__ == "__main__":
    main()

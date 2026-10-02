"""Reconstruct every original mathematical field using only our own audit.

The optional original EXPECTED input is a comparator, not a search input.
"""
from itertools import combinations
import json
from pathlib import Path
import sys
from verify import audit_expected, counts_from_rows, graph, pages, require, strict_same


def reconstruct():
    own = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
    actual, _ = audit_expected(own, full_controls=False)
    pairs = tuple(combinations(range(4), 2))
    profiles = []
    for profile in actual["equality_profiles"]:
        pos = profile["local_degree_two_corner"]
        h = [2 if i == pos else 3 for i in range(4)]
        cc = counts_from_rows(profile["blue_word_counts"])
        margins = [sum(cc[w] for w in range(16) if w >> i & 1) for i in range(4)]
        joints = [sum(cc[w] for w in range(16) if w >> i & 1 and w >> j & 1) for i, j in pairs]
        opposite = (pos + 2) % 4
        block = [w for w in range(16) if not w >> opposite & 1]
        left, right = (opposite + 1) % 4, (opposite + 3) % 4
        sizes = [sum(cc[w] for w in block),
                 sum(cc[w] for w in block if not w >> left & 1),
                 sum(cc[w] for w in block if not w >> right & 1),
                 sum(cc[w] for w in block if not w >> left & 1 and not w >> right & 1)]
        profiles.append({"h": h, "blue_margins": margins, "pair_caps": joints,
                         "blue_word_counts": cc, "outside_red_block": sizes})
    groups = {"X_repeat": actual["leaf_words"]["repeat_X"],
              "Y_repeat": actual["leaf_words"]["repeat_Y"],
              "cross_repeat": actual["leaf_words"]["cross"]}
    fixed = graph(10, [(0, 1), (0, 8), (0, 9), (2, 6), (2, 7), (3, 4), (3, 5),
                       (4, 7), (4, 9), (5, 6), (5, 8), (6, 9), (7, 8)])
    red_sets = [[z for z in range(2, 8) if fixed[s][z]] for s in (8, 9)]
    splits = []
    for x in range(4, 9):
        y = 9 - x
        if y < 4:
            continue
        # Literal CaseII frame: a0,u1,v2,SX3,4,SY5,6,T7..9,
        # ordinary X10..15,Y16..21; t*=7 is blue to both SX.
        es = [(0, z) for z in range(1, 10)] + [(1, 2)]
        es += [(1, z) for z in (3, 4, *range(10, 16))]
        es += [(2, z) for z in (5, 6, *range(16, 22))]
        omitted = [0, 0, 1, 2]
        es += [(i + 3, t + 7) for i in range(4) for t in range(3) if omitted[i] != t]
        es += [(7, z) for z in range(10, 10 + x)]
        es += [(7, z) for z in range(16, 16 + y - 2)]
        g = graph(22, es)
        require(sum(g[2]) == sum(g[7]) == 10 and not g[2][7], "literal CaseII split degrees")
        splits.append([x, y, pages(g, 2, 7)])
    result = {"cycle_profiles": profiles, "row_costs_by_blue_rank": actual["row_cost_by_blue_rank"],
              "leaf_core_words": groups, "leaf_core_counts": {k: len(v) for k, v in groups.items()},
              "leaf_X_special_ordinary_red_sets": red_sets,
              "leaf_X_special_ordinary_red_overlap": len(set(red_sets[0]) & set(red_sets[1])),
              "caseII_full_T_degree_splits": sorted(splits, reverse=True)}
    if len(sys.argv) == 2:
        original = json.loads(Path(sys.argv[1]).read_text())
        require(strict_same(result, original), "entire typed original mathematical record mismatch")
    return result


if __name__ == "__main__":
    print(json.dumps(reconstruct(), sort_keys=True, indent=2))

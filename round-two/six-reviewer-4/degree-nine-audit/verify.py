"""Independent residual-margin search and literal colored-spine audit.

No import of derive.py or author executable. EXPECTED is only a comparator.
All failures are explicit and remain active under python -O.
"""
import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import random
import sys


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def pages(g, u, v):
    color = g[u][v]
    return sum(g[u][z] == color and g[v][z] == color
               for z in range(len(g)) if z != u and z != v)


def graph(n, edge_list):
    g = [[False] * n for _ in range(n)]
    for u, v in edge_list:
        require(u != v, "loop")
        g[u][v] = g[v][u] = True
    return g


def audit_identity(g, root, corners):
    n = len(g)
    a = [v for v in range(n) if g[root][v]]
    b = [v for v in range(n) if v != root and not g[root][v]]
    require(all(v in a for v in corners), "cycle outside red neighborhood")
    for i, j in combinations(range(4), 2):
        require(g[corners[i]][corners[j]] == ((i - j) % 4 in (1, 3)), "not induced C4")
    h = [sum(g[v][z] for z in a) for v in corners]
    deficit = [10 - sum(g[v]) for v in corners]
    ranks = Counter(sum(not g[z][v] for v in corners) for z in b)
    common_sum = sum(sum(g[corners[i]][z] and g[corners[j]][z] for z in a)
                     for i, j in combinations(range(4), 2))
    excess = common_sum - 4
    lam = sum((3 if g[corners[i]][corners[j]] else 6) - pages(g, corners[i], corners[j])
              for i, j in combinations(range(4), 2))
    left = 2 * sum(h) + sum(deficit) - 3 * len(a) + n - 17
    right = lam + excess + ranks[0] + ranks[3] + 3 * ranks[4]
    require(left == right and excess >= 0, "literal slack identity")
    for i, j in combinations(range(4), 2):
        v, w = corners[i], corners[j]
        common_a = sum(g[v][z] and g[w][z] for z in a)
        wi = sum(not g[v][z] for z in b)
        wj = sum(not g[w][z] for z in b)
        joint = sum(not g[v][z] and not g[w][z] for z in b)
        require(wi == h[i] + n - 10 - len(a) + deficit[i], "signed blue column")
        direct = (1 + common_a + len(b) - wi - wj + joint if g[v][w]
                  else len(a) - 2 - h[i] - h[j] + common_a + joint)
        require(direct == pages(g, v, w), "actual third-vertex page formula")
    return {"h": h, "deficits": deficit, "slack": left,
            "colored_spine_slack": lam, "common_neighbor_excess": excess,
            "row_rank_counts": [ranks[r] for r in range(5)]}


def physical_frame(h, delta, counts, collision=None):
    # root0, cyclic corners1..4, other root neighbors5..9, outside10..21.
    edges = [(0, v) for v in range(1, 10)]
    edges += [(1, 2), (2, 3), (3, 4), (1, 4)]
    extra = {}
    label = 5
    for i in range(4):
        if h[i] == 3:
            extra[i] = label
            label += 1
    if collision:
        extra[collision[1]] = extra[collision[0]]
    edges += [(i + 1, v) for i, v in extra.items()]
    outside = 10
    for word, count in enumerate(counts):
        for _ in range(count):
            edges += [(i + 1, outside) for i in range(4) if not word >> i & 1]
            outside += 1
    require(outside == 22, "outside count")
    g = graph(22, edges)
    info = audit_identity(g, 0, list(range(1, 5)))
    require(info["h"] == h and info["deficits"] == delta, "physical degree tags")
    require(all(pages(g, i + 1, j + 1) <= (3 if g[i + 1][j + 1] else 6)
                for i, j in combinations(range(4), 2)), "physical selected colored cap")
    p0_red = [z for z in range(10, 22) if g[1][z]]
    sets = [{z for z in p0_red if g[i + 1][z]} for i in (1, 3)]
    return info, [len(s) for s in sets], len(sets[0] & sets[1])


def residual_search(h, delta, collision=None):
    """All16 word multiplicities, using residual margins and exact row cost.

    No linear pair parametrization and no producer's singleton/triple split.
    Each nonnegative histogram occurs once. Every branch decreases the word
    index; all counts 0..remaining_rows are considered before exact pruning.
    """
    pairs = tuple(combinations(range(4), 2))
    cyc = {(0, 1), (1, 2), (2, 3), (0, 3)}
    margins = tuple(h[i] + 3 + delta[i] for i in range(4))
    common = [2 * int(ij not in cyc) + int(ij == collision) for ij in pairs]
    caps = tuple((h[i] + h[j] - 4 + delta[i] + delta[j] if ij in cyc
                  else h[i] + h[j] - 1) - c
                 for ij, c in zip(pairs, common) for i, j in [ij])
    budget = 2 * sum(h) + sum(delta) - 22 - int(collision is not None)
    words = sorted(range(16), key=lambda w: (-w.bit_count(), w))
    output = []
    counts = [0] * 16
    nodes = 0

    def visit(index, rows, col, joint, cost):
        nonlocal nodes
        nodes += 1
        if min(col) < 0 or max(col) > rows or min(joint) < 0 or cost < 0:
            return
        if not rows:
            if any(col):
                return
            output.append(counts[:])
            return
        if index == 16:
            return
        possible = words[index:]
        if sum(col) < rows * min(w.bit_count() for w in possible):
            return
        if sum(col) > rows * max(w.bit_count() for w in possible):
            return
        for i in range(4):
            if col[i] and not any(w >> i & 1 for w in possible):
                return
        word = words[index]
        bits = tuple(word >> i & 1 for i in range(4))
        joints = tuple(bits[i] * bits[j] for i, j in pairs)
        rank = sum(bits)
        row_cost = (rank - 1) * (rank - 2) // 2
        top = rows
        for bit, value in zip(bits, col):
            if bit:
                top = min(top, value)
        for bit, value in zip(joints, joint):
            if bit:
                top = min(top, value)
        if row_cost:
            top = min(top, cost // row_cost)
        for count in range(top + 1):
            counts[word] = count
            visit(index + 1, rows - count,
                  tuple(v - count * bit for v, bit in zip(col, bits)),
                  tuple(v - count * bit for v, bit in zip(joint, joints)),
                  cost - count * row_cost)
        counts[word] = 0

    visit(0, 12, margins, caps, budget)
    require(len({tuple(v) for v in output}) == len(output), "duplicate histogram")
    return sorted(output), nodes


def counts_from_rows(rows):
    counts = [0] * 16
    for word, count in rows:
        require(type(word) is int and type(count) is int and 0 <= word < 16 and count > 0,
                "word/count type or domain")
        require(counts[word] == 0, "duplicate word")
        counts[word] = count
    return counts


def independent_leaf_rows():
    groups = {"repeat_X": [], "repeat_Y": [], "cross": []}
    trials = 0
    cycles = 0
    for rows in product(range(16), repeat=3):
        trials += 1
        if any(sum(row >> i & 1 for row in rows) != 2 for i in range(4)):
            continue
        if sorted(row.bit_count() for row in rows) != [2, 3, 3]:
            continue
        omitted = [next(t for t, row in enumerate(rows) if not row >> i & 1)
                   for i in range(4)]
        repeat_t = next(t for t, row in enumerate(rows) if row.bit_count() == 2)
        positions = [i for i, t in enumerate(omitted) if t == repeat_t]
        group = "repeat_X" if positions == [0, 1] else "repeat_Y" if positions == [2, 3] else "cross"
        columns = [sum((row >> i & 1) << t for t, row in enumerate(rows)) for i in range(4)]
        groups[group].append(sum(col << (3 * i) for i, col in enumerate(columns)))
        if group != "cross":
            # N(a): roots0,1; X specials2,3; Y specials4,5; T6,7,8.
            e = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5)]
            e += [(i + 2, t + 6) for t, row in enumerate(rows) for i in range(4) if row >> i & 1]
            g = graph(9, e)
            block = [2, 3] if group == "repeat_Y" else [4, 5]
            root = 0 if group == "repeat_Y" else 1
            cyc = [root, block[0], repeat_t + 6, block[1]]
            require([sum(g[v]) for v in cyc] == [3, 3, 2, 3], "actual distinguished cycle degrees")
            require(all(g[cyc[i]][cyc[j]] == ((i - j) % 4 in (1, 3))
                        for i, j in combinations(range(4), 2)), "actual induced distinguished cycle")
            extra = [next(z for z in range(9) if g[v][z] and z not in cyc)
                     for v in (cyc[0], cyc[1], cyc[3])]
            require(len(set(extra)) == 3, "distinguished extras distinct")
            cycles += 1
    return {k: sorted(v) for k, v in groups.items()}, trials, cycles


def identity_controls():
    # Complete all six-point graphs, and each canonical rooted induced C4.
    pairs = tuple(combinations(range(6), 2))
    count = 0
    for mask in range(1 << len(pairs)):
        g = graph(6, [ij for bit, ij in enumerate(pairs) if mask >> bit & 1])
        for root in range(6):
            nbr = [v for v in range(6) if g[root][v]]
            for four in combinations(nbr, 4):
                deg = {v: sum(g[v][w] for w in four) for v in four}
                if any(d != 2 for d in deg.values()):
                    continue
                p0 = min(four)
                p1, p3 = sorted(v for v in four if g[p0][v])
                p2 = next(v for v in four if v not in (p0, p1, p3))
                audit_identity(g, root, [p0, p1, p2, p3])
                count += 1
    rng = random.Random(9197)
    signed = 0
    frames = 0
    for degree in range(4, 22):
        for _ in range(16):
            es = [(0, v) for v in range(1, degree + 1)]
            es += [(1, 2), (2, 3), (3, 4), (1, 4)]
            for i, j in combinations(range(1, 22), 2):
                if i <= 4 and j <= 4:
                    continue
                if rng.randrange(3):
                    es.append((i, j))
            info = audit_identity(graph(22, es), 0, [1, 2, 3, 4])
            signed += any(d < 0 for d in info["deficits"])
            frames += 1
    # Signed sum zero is weaker than every corner having degree ten. This
    # literal selected-spine frame has degrees11,10,9,10 and a different
    # saturated histogram. It is NOT a valid full-host counterexample.
    signed_counts = [0] * 16
    for word, value in ((1, 1), (3, 1), (5, 2), (6, 2), (9, 1), (10, 3), (12, 2)):
        signed_counts[word] = value
    signed_info, _, _ = physical_frame([3, 3, 2, 3], [-1, 0, 1, 0], signed_counts)
    require(signed_info["slack"] == signed_info["colored_spine_slack"] == 0,
            "signed zero-sum saturation control")
    return {"all_six_point_graphs": 32768, "rooted_induced_cycle_identity_checks": count,
            "varied_22_point_frames": frames, "negative_deficit_frames": signed,
            "signed_zero_sum_degree_control": [11, 10, 9, 10]}


def strict_same(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(strict_same(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(strict_same(a, b) for a, b in zip(left, right))
    return left == right


def audit_expected(expected, full_controls=True):
    actual_equal = []
    physical_spines = 0
    nodes = 0
    for pos in range(4):
        h = [2 if i == pos else 3 for i in range(4)]
        found, n = residual_search(h, [0] * 4)
        nodes += n
        require(len(found) == 1, "equality uniqueness")
        cc = found[0]
        info, _, _ = physical_frame(h, [0] * 4, cc)
        require(info["slack"] == info["colored_spine_slack"] == 0, "equality saturation")
        # Rotate the independently recovered histogram so the local two
        # corner is p2; p0 is then its opposite. No expected row is an input.
        shift = (pos - 2) % 4
        rotated = [0] * 16
        for word, count in enumerate(cc):
            new_word = sum(((word >> ((i + shift) % 4)) & 1) << i for i in range(4))
            rotated[new_word] += count
        _, sizes, overlap = physical_frame([3, 3, 2, 3], [0] * 4, rotated)
        require(sizes == [2, 2] and overlap == 1, "forced overlap")
        actual_equal.append({"local_degree_two_corner": pos,
                             "blue_word_counts": [[w, c] for w, c in enumerate(cc) if c]})
        physical_spines += 6
    near = []
    caseI = []
    by_corner = []
    for dpos in range(4):
        delta = [int(i == dpos) for i in range(4)]
        total = 0
        for collision in (None, (0, 1), (0, 3), (1, 3)):
            found, n = residual_search([3, 3, 2, 3], delta, collision)
            nodes += n
            total += len(found)
            for cc in found:
                info, sizes, overlap = physical_frame([3, 3, 2, 3], delta, cc, collision)
                require(info["slack"] == 1, "near-equality slack")
                physical_spines += 6
                rows = [[w, c] for w, c in enumerate(cc) if c]
                near.append({"deficient_corner": dpos,
                             "shared_extra_pair": list(collision) if collision else [],
                             "blue_word_counts": rows})
                if dpos == 2 and collision is None and overlap == 0:
                    require(sizes == [2, 2], "CaseI special red degrees")
                    caseI.append(rows)
        by_corner.append(total)
    near.sort(key=lambda r: (r["deficient_corner"], r["shared_extra_pair"], r["blue_word_counts"]))
    groups, leaf_trials, leaf_cycles = independent_leaf_rows()
    caseI.sort()
    # Fixed leaf literal adjacency, not imported expected data.
    fixed_edges = [(0, 1), (0, 8), (0, 9), (2, 6), (2, 7), (3, 4), (3, 5),
                   (4, 7), (4, 9), (5, 6), (5, 8), (6, 9), (7, 8)]
    fixed = graph(10, fixed_edges)
    sx = [{v for v in range(2, 8) if fixed[s][v]} for s in (8, 9)]
    require(len(fixed_edges) == 13 and sx == [{5, 7}, {4, 6}] and not sx[0] & sx[1], "fixed leaf overlap")
    actual = {"equality_profiles": actual_equal, "leaf_words": groups, "near_equality": near,
              "near_equality_counts_by_deficient_corner": by_corner,
              "caseI_deficient_T_remaining_words": caseI,
              "row_cost_by_blue_rank": [(r - 1) * (r - 2) // 2 for r in range(5)]}
    require(strict_same(actual, expected), "whole independent record mismatch")
    evidence = {"residual_search_nodes": nodes, "physical_selected_colored_spines": physical_spines,
                "leaf_row_trials": leaf_trials, "distinguished_leaf_cycles": leaf_cycles,
                "near_patterns": len(near), "same_block_T_degree9_patterns": len(caseI)}
    if full_controls:
        evidence.update(identity_controls())
    return actual, evidence


def self_test(expected):
    from copy import deepcopy
    damaged = []
    for mutate in (
        lambda z: z["equality_profiles"][0]["blue_word_counts"].pop(),
        lambda z: z["near_equality"].pop(),
        lambda z: z["near_equality"][0].update(deficient_corner=3),
        lambda z: z["near_equality"][0].update(shared_extra_pair=[0, 1]),
        lambda z: z["near_equality"][0]["blue_word_counts"][0].__setitem__(1, True),
        lambda z: z["leaf_words"]["cross"].pop(),
        lambda z: z["near_equality_counts_by_deficient_corner"].__setitem__(0, 2),
        lambda z: z["caseI_deficient_T_remaining_words"].pop(),
        lambda z: z["row_cost_by_blue_rank"].__setitem__(4, 2),
        lambda z: z.update(extra_key=1),
    ):
        z = deepcopy(expected)
        mutate(z)
        try:
            audit_expected(z, full_controls=False)
        except RuntimeError:
            damaged.append(True)
        else:
            raise RuntimeError("damaged certificate accepted")
    return {"damages_rejected": len(damaged)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
    if args.self_test:
        print(json.dumps(self_test(expected), sort_keys=True))
    else:
        actual, evidence = audit_expected(expected)
        print(json.dumps(evidence, sort_keys=True), file=sys.stderr)
        print(json.dumps(actual, sort_keys=True, indent=2))

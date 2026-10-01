"""Independent definition-level checks of the Book22 Petersen bridge.

Ordinary proofs in REVIEW.md establish the universal statements. These finite
checks neither enumerate Book22 hosts nor prove Hall's classification.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
from random import Random
from itertools import product

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def graph(order, edges):
    adjacency = [set() for _ in range(order)]
    for a, b in edges:
        require(0 <= a < order and 0 <= b < order and a != b, "bad edge")
        adjacency[a].add(b)
        adjacency[b].add(a)
    return adjacency


def validate(adjacency):
    n = len(adjacency)
    require(n == 10, "Moore graph needs ten vertices")
    require(all(len(s) == 3 for s in adjacency), "not cubic")
    require(all(i not in s and all(0 <= j < n for j in s)
                for i, s in enumerate(adjacency)), "bad vertex")
    require(all((j in adjacency[i]) == (i in adjacency[j])
                for i, j in combinations(range(n), 2)), "not symmetric")
    require(not any(adjacency[i] & adjacency[j]
                    for i, j in combinations(range(n), 2)
                    if j in adjacency[i]), "triangle")
    require(not any(len(adjacency[i] & adjacency[j]) >= 2
                    for i, j in combinations(range(n), 2)), "four-cycle")


def cycles4(adjacency):
    """Unordered induced cycle vertex sets; used on triangle-free inputs."""
    return [points for points in combinations(range(len(adjacency)), 4)
            if all(len(adjacency[i].intersection(points)) == 2 for i in points)]


def isomorphism(left, right):
    require(len(left) == len(right), "different orders")
    assignment = {}
    used = set()

    def search():
        if len(assignment) == len(left):
            return assignment.copy()
        available = [v for v in range(len(left)) if v not in assignment]
        a = max(available, key=lambda v: (len(left[v].intersection(assignment)), -v))
        for b in range(len(right)):
            if b in used or len(left[a]) != len(right[b]):
                continue
            if any((x in left[a]) != (y in right[b]) for x, y in assignment.items()):
                continue
            assignment[a] = b
            used.add(b)
            answer = search()
            if answer is not None:
                return answer
            used.remove(b)
            del assignment[a]
        return None

    result = search()
    require(result is not None, "not Petersen")
    require(len(set(result.values())) == len(left)
            and all({result[j] for j in left[i]} == right[result[i]]
                    for i in range(len(left))), "false isomorphism")
    return [result[i] for i in range(len(left))]


def kneser5():
    pairs = list(combinations(range(5), 2))
    return graph(10, [(i, j) for i, j in combinations(range(10), 2)
                      if set(pairs[i]).isdisjoint(pairs[j])])


def moore():
    """All sixty possible residual six-cycles in the normalized Moore proof."""
    reference = kneser5()
    validate(reference)
    base = [(0, i) for i in (1, 2, 3)]
    base += [(i, j) for i, pair in enumerate(((4, 5), (6, 7), (8, 9)), 1)
             for j in pair]
    examined = 0
    survivors = []
    for tail in permutations(range(5, 10)):
        if tail[0] > tail[-1]:
            continue
        cycle = (4,) + tail
        candidate = graph(10, base + list(zip(cycle, cycle[1:] + cycle[:1])))
        examined += 1
        try:
            validate(candidate)
        except ValueError:
            continue
        mapping = isomorphism(candidate, reference)
        survivors.append({"cycle": list(cycle), "map_to_kneser5": mapping})
        # Literal BFS layer reconstruction at every possible root.
        for root in range(10):
            branch = candidate[root]
            leaves = [candidate[x] - {root} for x in branch]
            require(len(set.union(*leaves)) == 6
                    and sum(map(len, leaves)) == 6, "overlapping second layer")
            remaining = set(range(10)) - {root} - branch
            require(remaining == set.union(*leaves), "missing second layer")
            require(all(len(candidate[x] & remaining) == 2 for x in remaining),
                    "residual layer not two-regular")
            for pair in leaves:
                a, b = pair
                require(b not in candidate[a]
                        and not ((candidate[a] & candidate[b]) & remaining),
                        "branch pair is not opposite")
    require(examined == 60 and len(survivors) == 4, "incomplete Moore cycle list")
    return {"six_cycles_examined": examined, "survivors": survivors,
            "literal_root_checks": 10 * len(survivors)}


def column_dp(target):
    """Eleven binary rows, exact individual column counts, literal pair costs."""
    states = {(0, 0, 0, 0): (0, [])}
    for _ in range(11):
        following = {}
        for counts, (cost, witness) in states.items():
            for mask in range(16):
                bits = tuple((mask >> i) & 1 for i in range(4))
                new = tuple(a + b for a, b in zip(counts, bits))
                if any(a > b for a, b in zip(new, target)):
                    continue
                pair_cost = sum(bits[i] and bits[j]
                                for i, j in combinations(range(4), 2))
                candidate = cost + pair_cost
                if new not in following or candidate < following[new][0]:
                    following[new] = (candidate, witness + [mask])
        states = following
    optimum, witness = states[target]
    columns = [{r for r, mask in enumerate(witness) if mask >> i & 1}
               for i in range(4)]
    require(tuple(map(len, columns)) == target, "false column margins")
    require(sum(len(a & b) for a, b in combinations(columns, 2)) == optimum,
            "false packing cost")
    return {"target": list(target), "minimum": optimum, "rows": witness}


def clique_dp():
    """All eighteen outside attachments, with six separate page budgets one."""
    pairs = list(combinations(range(4), 2))
    states = {0: 0}
    for _ in range(18):
        new = {}
        for consumed, score in states.items():
            for row in range(16):
                budget = sum(1 << k for k, (i, j) in enumerate(pairs)
                             if row >> i & 1 and row >> j & 1)
                if consumed & budget:
                    continue
                key = consumed | budget
                new[key] = max(new.get(key, -1), score + row.bit_count())
        states = new
    require(max(states.values()) == 24, "K4 degree-sum bound failed")
    return {"outside_rows": 18, "individual_pair_caps": 1,
            "maximum_external_incidence": 24, "degree_sum_bound": 36}


def identities():
    """Literal common-neighbor sets versus degree-dependent identities."""
    rng = Random(8692)
    checked = 0
    for trial in range(128):
        # These deliberately unrestricted hosts need not satisfy book caps.
        edges = [(0, i) for i in range(1, 11)]
        edges += [(i, j) for i, j in combinations(range(1, 22), 2)
                  if rng.randrange(7) < trial % 6 + 1]
        red = graph(22, edges)
        blue = [set(range(22)) - s - {i} for i, s in enumerate(red)]
        a = red[0]
        b = blue[0]
        require(len(a) == 10 and len(b) == 11, "bad root")
        h = {i: len(red[i] & a) for i in a}
        deficit = {i: 10 - len(red[i]) for i in a}
        miss = {i: blue[i] & b for i in a}
        for i in a:
            require(len(miss[i]) == 2 + h[i] + deficit[i], "miss column size")
        for i, j in combinations(sorted(a), 2):
            common = len(red[i] & red[j] & a)
            shared = len(miss[i] & miss[j])
            if j in red[i]:
                formula = 8 - h[i] - h[j] - deficit[i] - deficit[j] + common + shared
                require(len(red[i] & red[j]) == formula, "red page identity")
            else:
                formula = 8 - h[i] - h[j] + common + shared
                require(len(blue[i] & blue[j]) == formula, "blue page identity")
            checked += 1
    return {"seed": 8692, "arbitrary_hosts": 128, "pair_identities": checked}


def weighted_bounds():
    checked = 0
    for h in product4(range(4)):
        total = sum(h)
        for deficit in product4(range(3)):
            d = sum(deficit)
            lower = total + d - 3
            caps = sum(h[i] + h[j] + deficit[i] + deficit[j] - 5
                       for i, j in ((0, 1), (1, 2), (2, 3), (3, 0)))
            caps += h[0] + h[2] - 4 + h[1] + h[3] - 4
            require(caps == 3 * total + 2 * d - 28, "weighted cap summation")
            require((lower > caps) == (2 * total + d < 25),
                    "weighted four-cycle threshold")
            checked += 1
    return {"arithmetic_states": checked, "necessary_threshold": 25}


def deficit_one_rows():
    """Exact row multisets after the proved equality excludes sizes 0,3,4."""
    pairs = list(combinations(range(4), 2))
    caps = (2, 2, 2, 1, 2, 1)
    margins = (6, 5, 5, 5)
    solutions = []
    visited = 0
    for pair_counts in product(*(range(c + 1) for c in caps)):
        visited += 1
        used = [0] * 4
        rows = []
        for (i, j), count in zip(pairs, pair_counts):
            used[i] += count
            used[j] += count
            rows += [(1 << i) | (1 << j)] * count
        singles = [a - b for a, b in zip(margins, used)]
        if any(s < 0 for s in singles):
            continue
        rows += [1 << i for i, s in enumerate(singles) for _ in range(s)]
        if len(rows) != 11:
            continue
        columns = [{r for r, row in enumerate(rows) if row >> i & 1}
                   for i in range(4)]
        require(tuple(map(len, columns)) == margins, "deficit-one margins")
        require(tuple(len(columns[i] & columns[j]) for i, j in pairs) == caps,
                "deficit-one capacities not forced")
        require(singles == [0, 0, 1, 0], "wrong singleton column")
        solutions.append({"pair_counts": list(pair_counts), "singles": singles,
                          "rows": sorted(rows)})
    require(visited == 324 and len(solutions) == 1, "deficit-one coverage")
    return {"pair_histograms_examined": visited, "solutions": solutions,
            "margins": list(margins), "caps": list(caps)}


def product4(values):
    for a in values:
        for b in values:
            for c in values:
                for d in values:
                    yield a, b, c, d


def decode_g6(line):
    require(len(line) == 9 and line[0] == "I", "bad graph6 order")
    payload = 0
    for character in line[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, "bad graph6 digit")
        payload = (payload << 6) | value
    require(payload & 7 == 0, "bad graph6 padding")
    edges = []
    bit = 47
    for j in range(1, 10):
        for i in range(j):
            if payload >> bit & 1:
                edges.append((i, j))
            bit -= 1
    return graph(10, edges)


def primary_checks():
    lines = (HERE / "PRIMARY.g6").read_text().splitlines()
    result = []
    for line in lines:
        adjacency = decode_g6(line)
        require(all(len(s) == 3 for s in adjacency), "noncubic primary fixture")
        require(not any(adjacency[i] & adjacency[j]
                        for i, j in combinations(range(10), 2)
                        if j in adjacency[i]), "primary triangle")
        cycles = cycles4(adjacency)
        capacities = []
        for points in cycles:
            cost = sum((1 if j in adjacency[i] else 4) -
                       len(adjacency[i] & adjacency[j])
                       for i, j in combinations(points, 2))
            require(cost <= 8, "four-cycle cap exceeds eight")
            capacities.append(cost)
        if not cycles:
            validate(adjacency)
            isomorphism(adjacency, kneser5())
        result.append({"graph6": line, "four_cycles": len(cycles),
                       "capacity_histogram": dict(sorted(Counter(capacities).items()))})
    require(sorted(x["four_cycles"] for x in result) == [0, 2, 3, 5, 5, 6],
            "primary fixture comparison")
    # Baseline matrix uses 0 for red and 1 for blue, excluding the diagonal.
    raw = (HERE / "PRIMARY21.txt").read_text().split("\n\n", 1)[0]
    matrix = json.loads(raw)
    require(len(matrix) == 21 and all(len(r) == 21 for r in matrix),
            "bad primary21 order")
    require(all(matrix[i][j] in (0, 1) and matrix[i][j] == matrix[j][i]
                for i, j in combinations(range(21), 2)), "bad primary21 adjacency")
    baseline = {}
    for label, color in [("red", 0), ("blue", 1)]:
        adjacency = [{j for j in range(21) if j != i and matrix[i][j] == color}
                     for i in range(21)]
        edges = [(i, j) for i, j in combinations(range(21), 2)
                 if j in adjacency[i]]
        baseline[label] = {"edges": len(edges), "max_pages":
                           max(len(adjacency[i] & adjacency[j]) for i, j in edges)}
    require(baseline == {"red": {"edges": 93, "max_pages": 3},
                         "blue": {"edges": 117, "max_pages": 6}}, "primary21 mismatch")
    return {"cubic_fixtures": result, "known21": baseline}


def controls():
    reference = kneser5()
    damaged = []
    bad = [s.copy() for s in reference]
    i, j = next((i, j) for i, j in combinations(range(10), 2) if j in reference[i])
    bad[i].remove(j)
    damaged.append(("missing edge", lambda: validate(bad)))
    damaged.append(("wrong order", lambda: validate(reference[:-1])))
    triangle = graph(10, list(combinations(range(4), 2)) +
                     list(combinations((4, 5, 6), 2)) +
                     list(combinations((7, 8, 9), 2)) + [(4, 7), (5, 8), (6, 9)])
    damaged.append(("triangle graph", lambda: validate(triangle)))
    prism = graph(10, [(i, (i + 1) % 5) for i in range(5)] +
                  [(i + 5, (i + 1) % 5 + 5) for i in range(5)] +
                  [(i, i + 5) for i in range(5)])
    damaged.append(("four-cycle graph", lambda: validate(prism)))
    damaged.append(("wrong graph6 order", lambda: decode_g6("H" + "?" * 8)))
    damaged.append(("nonzero graph6 padding", lambda: decode_g6("I" + "?" * 7 + "@")))
    rejected = []
    for name, call in damaged:
        try:
            call()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("control accepted: " + name)
    t = Fraction(3, 2)
    require(t * (t - 1) / 2 - t + 1 < 0, "integer-domain control")
    # A red-only relaxation falsifies both the density conclusion and the
    # idea that one Petersen neighborhood suffices for global Hall.
    pairs = list(combinations(range(7), 2))
    red = graph(22, [(i, j) for i, j in combinations(range(21), 2)
                     if set(pairs[i]).isdisjoint(pairs[j])])
    blue = [set(range(22)) - s - {i} for i, s in enumerate(red)]
    edge_count = sum(map(len, red)) // 2
    red_pages = max(len(red[i] & red[j])
                    for i, j in combinations(range(22), 2) if j in red[i])
    blue_pages = max(len(blue[i] & blue[j])
                     for i, j in combinations(range(22), 2) if j in blue[i])
    a = red[0]
    local_edges = sum(len(red[i] & a) for i in a) // 2
    b = blue[0]
    outside_edges = sum(len(red[i] & b) for i in b) // 2
    require(len(a) == 10 and all(len(red[i]) == 10 for i in a),
            "red-only fixture lost degree hypothesis")
    require(edge_count == 105 and red_pages == 3 and blue_pages == 10
            and local_edges == 15 and outside_edges == 20, "red-only fixture")
    require(outside_edges == edge_count + local_edges - 100,
            "literal healthy-root edge identity")
    return {"rejected_graphs_or_encodings": rejected,
            "integer_domain_essential": True,
            "red_only_relaxation": {"host_edges": edge_count,
                                    "red_max_pages": red_pages,
                                    "blue_max_pages": blue_pages,
                                    "local_edges": local_edges,
                                    "outside_edges": outside_edges}}


def run():
    exact = column_dp((5, 5, 5, 5))
    boundary = column_dp((5, 5, 5, 4))
    require(exact["minimum"] == 9 and boundary["minimum"] == 8,
            "nineteen/twenty incidence boundary")
    return {"agent": "six-reviewer-2", "role": "independent mathematical reviewer",
            "status": "COMPLETE", "column_dp": [exact, boundary],
            "clique_dp": clique_dp(), "moore": moore(),
            "literal_identities": identities(), "weighted_bounds": weighted_bounds(),
            "deficit_one_rows": deficit_one_rows(),
            "primary": primary_checks(), "controls": controls()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = run()
    raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    if args.check:
        require(raw == args.check.read_bytes(), "expected bytes differ")
        print(json.dumps({"status": "PASS", "sha256": sha256(raw).hexdigest(),
                          "literal_pairs": result["literal_identities"]["pair_identities"],
                          "weighted_states": result["weighted_bounds"]["arithmetic_states"],
                          "moore_cycles": result["moore"]["six_cycles_examined"],
                          "damaged_inputs_rejected": len(result["controls"]["rejected_graphs_or_encodings"])}))
    else:
        print(raw.decode(), end="")

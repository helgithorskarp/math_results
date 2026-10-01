#!/usr/bin/env python3
"""Exact finite controls for the ordinary proof; no valid-host enumeration."""
import hashlib
import itertools as it
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise ValueError(message)


def masks(n, edges):
    out = [0] * n
    for a, b in edges:
        require(a != b and not (out[a] >> b & 1), "simple edge")
        out[a] |= 1 << b
        out[b] |= 1 << a
    return out


def graph_data(rows):
    n = len(rows)
    blue = [((1 << n) - 1) ^ row ^ (1 << i) for i, row in enumerate(rows)]
    require(all(not (row >> i & 1) for i, row in enumerate(rows)), "loop")
    require(all((rows[i] >> j & 1) == (rows[j] >> i & 1)
                for i in range(n) for j in range(n)), "symmetry")
    red_max = blue_max = 0
    for i in range(n):
        for j in range(i + 1, n):
            if rows[i] >> j & 1:
                red_max = max(red_max, (rows[i] & rows[j]).bit_count())
            else:
                blue_max = max(blue_max, (blue[i] & blue[j]).bit_count())
    degrees = [x.bit_count() for x in rows]
    return {"edges": sum(degrees) // 2,
            "degree_histogram": [[d, degrees.count(d)] for d in sorted(set(degrees))],
            "red_max": red_max, "blue_max": blue_max}


def petersen():
    points = list(it.combinations(range(5), 2))
    edges = [(i, j) for i, a in enumerate(points) for j in range(i + 1, 10)
             if set(a).isdisjoint(points[j])]
    return masks(10, edges)


def four_sets(p):
    return [sum(1 << i for i in a) for a in it.combinations(range(10), 4)
            if all(not (p[i] >> j & 1) for i, j in it.combinations(a, 2))]


def pairings(points):
    if not points:
        yield []
        return
    a = points[0]
    for b in points[1:]:
        for rest in pairings([x for x in points[1:] if x != b]):
            yield [(a, b)] + rest


def leaf_graph(cycle, matching):
    edges = [(0, i) for i in range(1, 4)]
    for parent, (a, b) in enumerate(matching, 1):
        edges.extend([(parent, a + 4), (parent, b + 4)])
    edges.extend((a + 4, a + 5) for a in range(5))
    if cycle:
        edges.append((4, 9))
    return masks(10, edges)


def iso(source, target):
    order = sorted(range(10), key=lambda i: (-source[i].bit_count(), i))
    mapping = {}

    def visit(t):
        if t == 10:
            return [mapping[i] for i in range(10)]
        i = order[t]
        for j in range(10):
            if j in mapping.values() or source[i].bit_count() != target[j].bit_count():
                continue
            if any((source[i] >> k & 1) != (target[j] >> l & 1)
                   for k, l in mapping.items()):
                continue
            mapping[i] = j
            answer = visit(t + 1)
            if answer is not None:
                return answer
            del mapping[i]
        return None

    answer = visit(0)
    require(answer is not None, "isomorphism")
    return answer


def leaf_census():
    pairs = list(it.combinations(range(6), 2))
    counts = []
    for degrees, nedges in [([2] * 6, 6), ([1, 2, 2, 2, 2, 1], 5)]:
        found = []
        for selected in it.combinations(pairs, nedges):
            g = masks(6, selected)
            if [x.bit_count() for x in g] != degrees:
                continue
            if any((g[i] & g[j]).bit_count() >= 2 for i, j in pairs):
                continue
            if any(g[i] >> j & 1 and g[i] & g[j] for i, j in pairs):
                continue
            found.append(g)
        counts.append(len(found))
    require(counts == [60, 24], "six-leaf census")
    return {"cycle_degree_graphs": counts[0], "path_degree_graphs": counts[1]}


def control(name, local, words, deficits):
    desired = [word.bit_count() - d for word, d in zip(words, deficits)]
    require(desired[0] in [6, 8] and desired[1:] == [4] * 10, "control B degrees")
    # Four-regular ten-cycle with steps1,2; split a matching to attach point0.
    bedges = {tuple(sorted((1 + i, 1 + (i + step) % 10)))
              for i in range(10) for step in [1, 2]}
    for a in range(0, desired[0], 2):
        bedges.remove((1 + a, 2 + a))
        bedges.update([(0, 1 + a), (0, 2 + a)])
    outside = masks(11, sorted(bedges))
    require([x.bit_count() for x in outside] == desired, "outside control degrees")
    edges = [(0, i + 1) for i in range(10)]
    edges += [(i + 1, j + 1) for i in range(10) for j in range(i + 1, 10)
              if local[i] >> j & 1]
    edges += [(i + 1, b + 11) for b, z in enumerate(words) for i in range(10)
              if not (z >> i & 1)]
    edges += [(b + 11, c + 11) for b in range(11) for c in range(b + 1, 11)
              if outside[b] >> c & 1]
    host = masks(22, edges)
    require([host[i].bit_count() for i in range(11)] == [10] * 11, "full root")
    require([10 - host[b + 11].bit_count() for b in range(11)] == deficits,
            "outside deficiencies")
    h = [row.bit_count() for row in local]
    f = [[0] * 10 for _ in range(10)]
    s0 = [[0] * 10 for _ in range(10)]
    gram = [[sum((z >> i & 1) * (z >> j & 1) for z in words)
             for j in range(10)] for i in range(10)]
    blue = [((1 << 22) - 1) ^ row ^ (1 << i) for i, row in enumerate(host)]
    for i in range(10):
        for j in range(10):
            if i == j:
                s0[i][j] = h[i] + 2
            else:
                red = local[i] >> j & 1
                pages = (host[i + 1] & host[j + 1]).bit_count() if red else (
                    blue[i + 1] & blue[j + 1]).bit_count()
                f[i][j] = (3 if red else 6) - pages
                s0[i][j] = h[i] + h[j] - (5 if red else 2) - (
                    local[i] & local[j]).bit_count()
            require(gram[i][j] == s0[i][j] - f[i][j], "signed local Gram")
    for i in range(10):
        u = sum(z.bit_count() - 4 for z in words if z >> i & 1)
        require(sum(f[i]) == 3 * h[i] + sum(h) - 24
                - sum(h[j] for j in range(10) if local[i] >> j & 1) - u,
                "signed defect margin")
    require(all(x >= 0 for row in f for x in row), "control local nonnegative capacity")
    k = [[4 * (i == j) + 3 - 3 * (petersen()[i] >> j & 1)
          - (petersen()[i] & petersen()[j]).bit_count()
          for j in range(10)] for i in range(10)]
    if words[0].bit_count() == 10:
        require(all(x == 0 for row in f for x in row), "ten-row capacity zero")
        residual = [[gram[i][j] - 1 for j in range(10)] for i in range(10)]
        require(residual == k, "ten-row contraction")
    elif words[0].bit_count() == 9:
        q = next(z for z in words if z.bit_count() == 5)
        a = next(i for i in range(10) if not (words[0] >> i & 1))
        require(q >> a & 1, "nine-row star center")
        r = q ^ (1 << a)
        z = words[0]
        for i in range(10):
            for j in range(10):
                require((z >> i & 1) * (z >> j & 1) + (q >> i & 1) * (q >> j & 1)
                        + f[i][j] == 1 + (r >> i & 1) * (r >> j & 1),
                        "nine-row rank-one identity")
                residual = gram[i][j] - (z >> i & 1) * (z >> j & 1)
                residual -= (q >> i & 1) * (q >> j & 1)
                require(k[i][j] == residual + (r >> i & 1) * (r >> j & 1),
                        "nine-row contraction")
    else:
        z = words[0]
        for i in range(10):
            for j in range(10):
                require(gram[i][j] - (z >> i & 1) * (z >> j & 1) == k[i][j],
                        "eight-row edge-deleted contraction")
    # Whole graph near-regular identity, including diagonal and degree corrections.
    d = [10 - row.bit_count() for row in host]
    for i in range(22):
        for j in range(22):
            adj = host[i] >> j & 1
            lhs = (host[i] & host[j]).bit_count() + 3 * adj
            cap = 0 if i == j else (3 - (host[i] & host[j]).bit_count() if adj
                  else 6 - (blue[i] & blue[j]).bit_count())
            rhs = 4 * (i == j) + 6 - d[i] - d[j] + d[i] * (i == j)
            rhs += (d[i] + d[j]) * adj - cap
            require(lhs == rhs, "whole signed identity")
    equal = next((a, b) for a, b in it.combinations(range(1, 11), 2)
                 if words[a] == words[b] and words[a].bit_count() == 4
                 and outside[0] >> a & 1 and outside[0] >> b & 1)
    a, b = equal
    require(not (outside[a] >> b & 1), "equal row blue spine")
    pages = blue[a + 11] & blue[b + 11]
    require(pages.bit_count() >= 7, "literal forbidden blue book")
    return {"name": name, "local": local, "miss_rows": words,
            "deficits": deficits, "outside": outside, "host": host,
            "summary": graph_data(host), "book_spine": [a + 11, b + 11],
            "book_pages": [i for i in range(22) if pages >> i & 1],
            "local_identity_entries": 100, "whole_identity_entries": 484}


def compute():
    profiles = []
    for n0 in range(2):
        for n2 in range(11 - n0):
            n3 = 10 - n0 - n2
            h = 2 * n2 + 3 * n3
            if 26 <= h <= 30 and h % 2 == 0:
                profiles.append([n0, n2, n3])
    require(sorted(profiles) == [[0, 0, 10], [0, 2, 8], [0, 4, 6], [1, 1, 8]],
            "profiles")
    cycles = []
    for degrees in it.product([2, 3], repeat=4):
        total = sum(degrees)
        lo = total - 3
        hi = 3 * total - 28
        require(hi < lo, "C4 gap")
        cycles.append({"degrees": list(degrees), "lower": lo, "upper": hi})
    # Separate integer DP validates the packing minimum for each total.
    dp = {0: 0}
    for _ in range(11):
        new = {}
        for amount, cost in dp.items():
            for t in range(5):
                new[amount + t] = min(new.get(amount + t, 10**9), cost + t * (t - 1) // 2)
        dp = new
    packing = [[h, dp[h + 8]] for h in range(8, 13)]
    path = [q for q in pairings(list(range(6))) if all(abs(a - b) >= 3 for a, b in q)]
    cycle = [q for q in pairings(list(range(6)))
             if all(min(abs(a - b), 6 - abs(a - b)) >= 3 for a, b in q)]
    require(len(path) == len(cycle) == 1, "leaf pairing")
    p = petersen()
    for i in range(10):
        for j in range(10):
            require((p[i] & p[j]).bit_count() + (p[i] >> j & 1)
                    == 2 * (i == j) + 1, "Petersen relation")
    sets = four_sets(p)
    require(len(sets) == 5, "independent four sets")
    deleted = [*p]
    edge = next((i, j) for i in range(10) for j in range(i + 1, 10) if p[i] >> j & 1)
    x, y = edge
    deleted[x] ^= 1 << y
    deleted[y] ^= 1 << x
    leaf_full = leaf_graph(True, cycle[0])
    leaf_deleted = leaf_graph(False, path[0])
    a = 0
    r = next(z for z in sets if not (z >> a & 1))
    nine_rows = sets * 2
    q_position = nine_rows.index(r)
    nine_rows[q_position] |= 1 << a
    nine_deficits = [1] + [0] * 10
    nine_deficits[q_position + 1] = 1
    controls = [
        control("ten-row-one-degree-eight", p, [1023] + sets * 2, [2] + [0] * 10),
        control("nine-row-two-degree-nine", p, [1023 ^ (1 << a)] + nine_rows, nine_deficits),
        control("edge-deleted-eight-row-degree-eight", deleted,
                [1023 ^ (1 << x) ^ (1 << y)] + sets * 2, [2] + [0] * 10),
    ]
    baseline = [sum((ch == "1") << j for j, ch in enumerate(line))
                for line in (HERE / "baseline21.rows").read_text().splitlines()]
    require(len(baseline) == 21, "baseline order")
    b = graph_data(baseline)
    require(b == {"edges": 93, "degree_histogram": [[8, 4], [9, 16], [10, 1]],
                  "red_max": 3, "blue_max": 6}, "primary baseline")
    return {"schema": 1, "agent": "six-books-1", "role": "researcher",
            "profiles": profiles, "cycle_degree_checks": cycles,
            "packing_minima": packing, "low_overlap_union_lower": [[r, 11 + r] for r in [1, 2]],
            "path_pairings": [[[a, b] for a, b in q] for q in path],
            "cycle_pairings": [[[a, b] for a, b in q] for q in cycle],
            "leaf_census": leaf_census(),
            "petersen": p,
            "deleted_edge": list(edge), "deleted_petersen": deleted,
            "leaf_full_isomorphism": iso(leaf_full, p),
            "leaf_deleted_isomorphism": iso(leaf_deleted, deleted),
            "independent_four_sets": sets, "controls": controls, "baseline": b}


if __name__ == "__main__":
    result = compute()
    if "--write" in sys.argv:
        (HERE / "expected.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        require(result == json.loads((HERE / "expected.json").read_text()), "expected data")
    print(json.dumps({"status": "PASS", "controls": len(result["controls"]),
                      "expected_sha256": hashlib.sha256((HERE / "expected.json").read_bytes()).hexdigest()}))

"""Independent literal audit of the interval-tail repair and Ramsey witnesses."""

import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "additive_combinatorics/schur6_interval_tail_trades"
N = 537


def segment(a, b):
    return set(range(a, b + 1))


def triples(points):
    points = set(points)
    for z in sorted(points):
        for x in range(1, z // 2 + 1):
            y = z - x
            if x in points and y in points:
                yield x, y, z


def main():
    data = json.loads((SOURCE / "data.json").read_text())
    B = [int(c) for c in data["base160"]]
    assert len(B) == 160 and set(B) == set(range(1, 6))
    assert all(len({B[x - 1], B[y - 1], B[z - 1]}) > 1
               for x, y, z in triples(range(1, 161)))
    U = segment(1, 77)
    V = segment(155, 304)
    W = segment(305, 459)
    T0 = segment(78, 154) | segment(460, N)
    assert U | V | W == segment(1, N) - T0
    seed = {d: B[d - 1] for d in U}
    seed.update({154 + i: B[i - 1] for i in range(1, 151)})
    assert ''.join(str(seed[x]) for x in sorted(U)) == data["u"]
    assert ''.join(str(seed[x]) for x in sorted(V)) == data["v"]
    assert all(len({seed[x], seed[y], seed[z]}) > 1
               for x, y, z in triples(U | V))

    labels = {x: "U" if x in U else "V" if x in V else "W"
              for x in U | V | W}
    row_count = Counter(''.join(labels[x] for x in row)
                        for row in triples(U | V | W))
    assert row_count == {"UUU": 1482, "UVV": 8547, "UVW": 3003,
                         "UWW": 8932, "VVW": 5700}
    assert sum(row_count.values()) == 27664

    holes = set(data["empty_points"])
    assert holes == {312, 313, 315, 322, 326, 327, 332, 334, 335, 336,
                     340, 341, 342, 347, 348}
    list_hist = []
    for delta in (0, 1):
        fixed = {x: c for x, c in seed.items() if not delta or x != 155}
        lists = {z: set(range(1, 6)) for z in W}
        for x, y, z in triples(U | V | W):
            if z in W and x in fixed and y in fixed and fixed[x] == fixed[y]:
                lists[z].discard(fixed[x])
        assert {z for z in W if not lists[z]} == holes
        list_hist.append(dict(sorted(Counter(map(len, lists.values())).items())))
    assert list_hist == [{0: 15, 1: 76, 2: 46, 3: 14, 4: 4}] * 2
    for colour, pair in enumerate(data["obstruction312"], 1):
        assert sum(pair) == 312 and seed[pair[0]] == seed[pair[1]] == colour

    graph_edges = []
    for delta in (0, 1):
        old = segment(78, 154 + delta) | segment(460, 537)
        assert not any(triples(old))
        m = 43 + delta
        low = [112 + i for i in range(m)]
        high = [460 + i for i in range(m)]
        for Q in (holes, segment(312, 348)):
            assert not any(triples(Q))
            edges = {(l, l + q) for l in low for q in Q if l + q in high}
            literal = []
            for row in triples(old | Q):
                q = set(row) & Q
                endpoints = set(row) & old
                assert len(q) == 1 and len(endpoints) == 2
                literal.append(tuple(sorted(endpoints)))
            assert edges == set(literal)
            assert len(edges) == (395 if not delta and len(Q) == 15 else
                                  925 if not delta else 410 if len(Q) == 15 else 962)
            assert {(low[i], high[i]) for i in range(m)} <= edges
            assert {(low[i + 1], high[i]) for i in range(m - 1)} <= edges
            assert all((h - 460) <= (l - 112) for l, h in edges)
            for t in range(m + 1):
                C = set(high[:t]) | set(low[t:])
                assert len(C) == m and all(l in C or h in C for l, h in edges)
                reserved = (old - C) | Q
                assert not any(triples(reserved))
                assert len(reserved) == (127 if len(Q) == 15 else 149)
            graph_edges.append(len(edges))
    assert graph_edges == [395, 925, 410, 962]

    # For a minimum cover, each matching edge contributes exactly one chosen
    # endpoint. The chain edges forbid an unchosen low endpoint immediately
    # after an unchosen high endpoint, so only upper-prefix choices survive.
    for m in range(1, 11):
        choices = {bits for bits in product((0, 1), repeat=m)
                   if all(not(bits[i + 1] == 1 and bits[i] == 0)
                          for i in range(m - 1))}
        assert choices == {(1,) * t + (0,) * (m - t) for t in range(m + 1)}

    total_pairs = 0
    sizes = []
    for t in range(45):
        T = segment(78, 111 + t) | segment(312, 348) | segment(460 + t, 537)
        assert len(T) == 149 and not any(triples(T))
        p = (112 + t) // 2
        r = 112 + t - p
        s = min(78, 126 - 2 * t)
        b = 111 + t
        A = (segment(0, p - 1) | segment(b + p, b + p + s - 1) |
             segment(348 + p, 347 + p + r))
        expected_size = 190 + t if t <= 24 else 238 - t
        assert len(A) == expected_size and max(A) <= 537
        assert all(1 <= y - x <= 537 and y - x not in T
                   for x, y in combinations(sorted(A), 2))
        total_pairs += len(A) * (len(A) - 1) // 2
        sizes.append(len(A))
    assert total_pairs == 920595 and min(sizes) == 190 and max(sizes) == 214
    print(f"PASS base160=yes target_rows={sum(row_count.values())} "
          f"empty_lists={len(holes)} deletion_edges={graph_edges} "
          f"minimum_repairs=44+45 witness_sizes={min(sizes)}..{max(sizes)} "
          f"witness_pairs={total_pairs} exact_differences=yes")


if __name__ == "__main__":
    main()

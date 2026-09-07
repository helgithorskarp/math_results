"""Finite arithmetic, exhaustive small matrices, and physical consumer controls."""
import copy
import json
import random
import sys
from collections import Counter
from itertools import combinations, product

import extract
import model
import verify


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def gaussian_binomial(n, k):
    # Independent recurrence for the number of k-dimensional binary subspaces.
    table = [[0] * (n + 1) for _ in range(n + 1)]
    table[0][0] = 1
    for i in range(1, n + 1):
        table[i][0] = 1
        for j in range(1, i + 1):
            table[i][j] = table[i - 1][j - 1] + (2**j) * table[i - 1][j]
    return table[n][k]


def count_by_row_space(m, n, k):
    answer = gaussian_binomial(n, k)
    for i in range(k):
        answer *= 2**m - 2**i
    return answer


def small_matrices():
    cases = 0
    histograms = {}
    for m in range(1, 5):
        for n in range(1, 5):
            hist = Counter()
            for word in range(1 << (m * n)):
                rows = [(word >> (i * n)) & ((1 << n) - 1) for i in range(m)]
                dense = [[(word >> (i * n + j)) & 1 for j in range(n)] for i in range(m)]
                r = verify.rank(dense)
                check(len(extract.basis(rows)) == r, "binary/dense rank disagreement")
                hist[r] += 1
                cases += 1
            expected = [model.matrix_count(m, n, k) for k in range(min(m, n) + 1)]
            independent = [count_by_row_space(m, n, k) for k in range(min(m, n) + 1)]
            check([hist[k] for k in range(len(expected))] == expected == independent, "matrix enumeration/count")
            histograms[f"{m}x{n}"] = expected
    # Complete 4x2 times 2x4 map, including the degenerate factors.
    fibers = Counter()
    for uword in range(256):
        u = [(uword >> (2 * i)) & 3 for i in range(4)]
        for vword in range(256):
            v = [(vword >> (2 * j)) & 3 for j in range(4)]
            word = sum(((u[i] & v[j]).bit_count() % 2) << (4 * i + j)
                       for i in range(4) for j in range(4))
            fibers[word] += 1
    by_rank = Counter()
    fiber_counts = {r: Counter() for r in range(3)}
    for word in range(65536):
        r = verify.rank([[(word >> (4 * i + j)) & 1 for j in range(4)] for i in range(4)])
        check((word in fibers) == (r <= 2), "factor map coverage")
        if r <= 2:
            by_rank[r] += 1
            fiber_counts[r][fibers[word]] += 1
        if r == 2:
            check(fibers[word] == 6, "full-rank GL(2,2) fiber")
    return {"exhaustive_matrices": cases, "histograms": histograms,
            "4x4_factor_words": 65536, "4x4_distinct_images": sum(by_rank.values()),
            "4x4_fiber_sizes_by_rank": {str(r): dict(sorted(c.items())) for r, c in fiber_counts.items()}}


def signatures_and_ramsey6():
    for x, y in product(range(2), repeat=2):
        check(x + y == 2 * x * y + int(x != y), "pair identity")
    for x, y, z in product(range(2), repeat=3):
        uniform = int(x == y == z)
        check(x * y + x * z + (1 - y) * (1 - z) == uniform + x, "mixed triple identity")
        check(x + y + z <= 3 * int(x == y == z == 1) + 2 * (1 - uniform), "triangle contact cap")
    graphs = 0
    comparisons = 0
    six_good = 0
    for n in range(1, 7):
        pairs = list(combinations(range(n), 2))
        for word in range(1 << len(pairs)):
            g = [[0] * n for _ in range(n)]
            adj = [0] * n
            for i, (u, v) in enumerate(pairs):
                g[u][v] = g[v][u] = (word >> i) & 1
                if g[u][v]:
                    adj[u] |= 1 << v
                    adj[v] |= 1 << u
            mono_triangle = False
            for color in (0, 1):
                colored = adj if color else [((1 << n) - 1) ^ row ^ (1 << i) for i, row in enumerate(adj)]
                for size in (3, 5):
                    literal = next((list(q) for q in combinations(range(n), size)
                                    if all(g[u][v] == color for u, v in combinations(q, 2))), None)
                    found = extract.clique(colored, (1 << n) - 1, size)
                    check(found == literal, "physical clique DFS versus literal enumeration")
                    comparisons += 1
                    if size == 3 and literal is not None:
                        mono_triangle = True
            if n == 6:
                check(mono_triangle, "R(3,3)<=6 check")
                six_good += 1
            graphs += 1
    return {"pair_signatures": 4, "triple_signatures": 8,
            "all_labeled_graphs_through_6": graphs,
            "literal_clique_comparisons": comparisons, "six_vertex_R33_checks": six_good}


def pack(matrix, cut, color):
    word = sum(matrix[u][v] << i for i, (u, v) in enumerate(combinations(range(43), 2)))
    return {"n": 43, "red_hex": format(word, "0226x"), "cut": sorted(cut), "rank_color": color}


def permute(data, permutation):
    g, _, _ = verify.graph(data)
    h = [[0] * 43 for _ in range(43)]
    for u, v in combinations(range(43), 2):
        h[permutation[u]][permutation[v]] = h[permutation[v]][permutation[u]] = g[u][v]
    return pack(h, [permutation[v] for v in data["cut"]], data["rank_color"])


def consumers():
    rng = random.Random(2026090703)
    statuses = Counter()
    ranks = Counter()
    physical_checks = 0
    saved = None
    for color in ("red", "blue"):
        for k in range(48):
            # First two cases include the zero and all-one cross matrices.
            u = [0] * 20 if k == 0 else [1] * 20 if k == 1 else [rng.randrange(4) for _ in range(20)]
            v = [1] * 23 if k < 2 else [rng.randrange(4) for _ in range(23)]
            internal = rng.getrandbits(382)
            data = model.family(u, v, internal, color)
            dense, a, b = verify.graph(data)
            # Independently reconstruct every fixed and free physical pair.
            independent_pins = {}
            for start in (2, 7, 12, 17, 22):
                for x, y in combinations(range(start, start + 5), 2):
                    independent_pins[x, y] = int(((y - x) % 5 == 1) or ((x - y) % 5 == 1))
            independent_pins[0, 1] = 1
            independent_pins.update({(x, y): 1 for x in (0, 1) for y in range(2, 7)})
            internal_index = 0
            for x, y in combinations(range(43), 2):
                if (x, y) in independent_pins:
                    expected = independent_pins[x, y]
                elif (x in a) != (y in a):
                    row, col = (x, y) if x in a else (y, x)
                    ui, vj = u[a.index(row)], v[b.index(col)]
                    expected = ((ui % 2) * (vj % 2) + (ui // 2) * (vj // 2)) % 2
                    expected ^= int(color == "blue")
                else:
                    expected = (internal >> internal_index) & 1
                    internal_index += 1
                check(dense[x][y] == expected, "F27 physical map")
                physical_checks += 1
            check(internal_index == 382, "internal parameter count")
            if saved is None and color == "red" and k == 2:
                saved = data
            for permuted in (False, True):
                item = data
                if permuted:
                    permutation = list(range(43))
                    rng.shuffle(permutation)
                    item = permute(data, permutation)
                    item["cut"] = [v for v in range(43) if v not in item["cut"]]
                cert = extract.extract(item)
                statuses[verify.verify(item, cert)] += 1
                ranks[cert["rank"]] += 1
                check(cert["status"] == "EXCLUDED_WITH_PHYSICAL_WITNESS", "complete family gate")
    # Cover each smaller-side profile gate and both color orientations.
    for a in range(1, 22):
        for color in ("red", "blue"):
            allowed = model.lower_bound(a) - 1
            u = [rng.randrange(1 << allowed) for _ in range(a)]
            v = [rng.randrange(1 << allowed) for _ in range(43 - a)]
            g = [[0] * 43 for _ in range(43)]
            for x, y in combinations(range(43), 2):
                bit = rng.randrange(2)
                if x < a <= y:
                    bit = (u[x] & v[y - a]).bit_count() % 2
                    bit ^= int(color == "blue")
                g[x][y] = g[y][x] = bit
            item = pack(g, list(range(a)), color)
            cert = extract.extract(item)
            statuses[verify.verify(item, cert)] += 1
            check(cert["status"] == "EXCLUDED_WITH_PHYSICAL_WITNESS", "profile consumer")
    # Deliberately bad graphs of full cut rank: outside means only outside this gate.
    for color in ("red", "blue"):
        g = [[0] * 43 for _ in range(43)]
        for x in range(20):
            for j in range(23):
                g[x][20 + j] = g[20 + j][x] = int(x == j) ^ int(color == "blue")
        item = pack(g, list(range(20)), color)
        cert = extract.extract(item)
        statuses[verify.verify(item, cert)] += 1
        check(cert["status"] == "OUTSIDE_CUT_RANK_GATE" and cert["rank"] == 20, "outside guard")
    check(saved is not None, "saved fixture")
    cert = extract.extract(saved)
    bad_inputs = []
    for field, value in (("n", 42), ("n", True), ("red_hex", "0"), ("red_hex", "f" * 226),
                         ("red_hex", saved["red_hex"].upper()), ("cut", []), ("cut", [0, 0]),
                         ("cut", [43]), ("cut", [True]), ("rank_color", "green")):
        item = copy.deepcopy(saved)
        item[field] = value
        bad_inputs.append(item)
    bad_inputs.append(dict(saved, hidden=1))
    for item in bad_inputs:
        for fn in (extract.parse, verify.graph):
            try:
                fn(item)
            except (ValueError, TypeError):
                pass
            else:
                raise RuntimeError("malformed input accepted")
    bad_certs = []
    for field, value in (("input_sha256", "0" * 64), ("rank", cert["rank"] + 1),
                         ("rank_lower_bound", 0), ("cut", [0]), ("rank_color", "blue"),
                         ("row_basis_hex", []), ("status", "OUTSIDE_CUT_RANK_GATE"),
                         ("witness", [0] * 5), ("witness_color", "green")):
        item = copy.deepcopy(cert)
        item[field] = value
        bad_certs.append(item)
    wrong_color = copy.deepcopy(cert)
    wrong_color["witness_color"] = "red" if cert["witness_color"] == "blue" else "blue"
    bad_certs.append(wrong_color)
    wrong_basis = copy.deepcopy(cert)
    wrong_basis["row_basis_hex"][0] = "0x0"
    bad_certs.append(wrong_basis)
    for item in bad_certs:
        try:
            verify.verify(saved, item)
        except (ValueError, TypeError):
            pass
        else:
            raise RuntimeError("corrupt certificate accepted")
    return {"F27_parameter_graphs": 96, "F27_with_permuted_complement_cuts": 192,
            "F27_physical_pair_checks": physical_checks, "F27_rank_histogram": dict(sorted(ranks.items())),
            "profile_graphs": 42, "statuses": dict(sorted(statuses.items())),
            "malformed_input_rejections_each_parser": len(bad_inputs),
            "corrupt_certificate_rejections": len(bad_certs)}, saved, cert


def run():
    summary = model.report()
    for row in summary["profile"]:
        a, lower = row["smaller_side"], row["rank_lower_bound"]
        for r in range(6):
            check(model.capacity(a, r) == verify.slot_bound(a, r), "slot capacity")
        check(all(verify.slot_bound(a, r) < a for r in range(lower)), "profile exclusion")
        check(verify.slot_bound(a, lower) >= a, "first unexcluded rank")
    check([r["rank_lower_bound"] for r in summary["profile"]] ==
          [1, 2, 2, 3, 3, 3, 3, 4, 4, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 3, 3], "profile transcription")
    triples = [t for t in product(range(1, 22), repeat=3) if sum(t) == 43]
    check(triples and all(15 <= max(t) <= 21 for t in triples), "centroid arithmetic")
    for k in range(3):
        check(count_by_row_space(20, 23, k) == summary["F27"]["distinct_cross_matrices_by_rank"][k], "target matrix count")
    controls, fixture, certificate = consumers()
    return {"status": "CHECKED_GLOBAL_CUT_RANK_REDUCTION", "capacity_cells": 126,
            "centroid_component_triples": len(triples), "small_matrices": small_matrices(),
            "physical_identities": signatures_and_ramsey6(), "consumer_controls": controls}, fixture, certificate


if __name__ == "__main__":
    result, fixture, certificate = run()
    output = {"audit": result, "fixture": fixture, "certificate": certificate} if sys.argv[1:] == ["--bundle"] else result
    print(json.dumps(output, indent=2, sort_keys=True))

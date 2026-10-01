"""Separate exact checker; imports no author generator or helper module.

Actual author six-books-1, researcher. Uses cycle complements, a K4-edge
bijection, set intersections, and literal full-graph page definitions.
This does not formalize the written proof or enumerate valid Ramsey hosts.
"""
from collections import Counter
from copy import deepcopy
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def fingerprint(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def points(code, n):
    return {i for i in range(n) if code & (1 << i)}


def encode_rows(rows, width):
    return sum(sum(1 << j for j in row) << (width * i) for i, row in enumerate(rows))


def graph(rows):
    n = len(rows)
    require(all(len(row) == n and set(row) <= {"0", "1"} for row in rows), "graph row format")
    ns = [{j for j, c in enumerate(row) if c == "1"} for row in rows]
    require(all(i not in ns[i] and all((j in ns[i]) == (i in ns[j]) for j in range(n))
                for i in range(n)), "simple graph")
    return ns


def matrix_graph(p):
    require(len(p) == 10 and all(len(r) == 10 and set(r) <= {0, 1} for r in p), "matrix format")
    return graph(["".join(map(str, row)) for row in p])


def page_set(ns, i, j):
    if j in ns[i]:
        return ns[i] & ns[j]
    return set(range(len(ns))) - (ns[i] | ns[j] | {i, j})


def cycle_bipartite_codes():
    # A 2-regular simple bipartite complement on 5+5 has C10, or C4+C6.
    cycles10 = Counter()
    for o_tail in permutations(range(1, 5)):
        o = (0,) + o_tail
        for ii in permutations(range(5)):
            zeros = [set() for _ in range(5)]
            for t in range(5):
                zeros[ii[t]].update((o[t], o[(t + 1) % 5]))
            rows = [set(range(5)) - zero for zero in zeros]
            cycles10[encode_rows(rows, 5)] += 1
    require(len(cycles10) == 1440 and set(cycles10.values()) == {2}, "C10 multiplicity")
    split = set()
    for oi in combinations(range(5), 2):
        for ii in combinations(range(5), 2):
            o_rest = sorted(set(range(5)) - set(oi))
            i_rest = sorted(set(range(5)) - set(ii))
            for matching in permutations(o_rest):
                zeros = [set(oi) if i in ii else set() for i in range(5)]
                for i, omitted in zip(i_rest, matching):
                    zeros[i] = set(o_rest) - {omitted}
                split.add(encode_rows([set(range(5)) - s for s in zeros], 5))
    require(len(split) == 600 and not (split & cycles10.keys()), "C4+C6 coverage")
    return sorted(set(cycles10) | split)


def check_triples(expected):
    # Each of the six outside labels is independently assigned a K4 edge.
    edges = list(combinations(range(4), 2))
    profiles = []
    for assignment in permutations(edges):
        rows = [{j for j, edge in enumerate(assignment) if i in edge} for i in range(4)]
        require(all(len(s) == 3 for s in rows), "K4 incidence triples")
        require(all(len(rows[i] & rows[j]) == 1 for i, j in combinations(range(4), 2)), "cut common neighbor")
        profiles.append(encode_rows(rows, 6))
    require(sorted(profiles) == expected["labeled_profiles"], "every labeled triple record")
    triples5 = [points(m, 5) for m in range(32) if m.bit_count() == 3]
    feasible5 = 0
    for a in triples5:
        for b in triples5:
            for c in triples5:
                if max(len(a & b), len(a & c), len(b & c)) <= 1:
                    feasible5 += 1
    require(feasible5 == expected["feasible_five_point_triples"] == 0, "five-point triple impossibility")
    triples6 = [points(m, 6) for m in range(64) if m.bit_count() == 3]
    pair_count = sum(len(a & b) <= 1 for a in triples6 for b in triples6)
    triple_count = 0
    for a, b, c in combinations(triples6, 3):
        if max(len(a & b), len(a & c), len(b & c)) <= 1:
            require(a | b | c == set(range(6)), "six-point union")
            triple_count += 1
    require(pair_count == expected["six_point_pair_records"], "all pair records")
    require(triple_count == expected["six_point_triple_records"], "all triple records")
    require(expected["four_triple_systems"] == len(profiles) // 24 == 30, "unordered four-triple count")
    require(expected["five_point_ordered_triples"] == len(triples5) ** 3, "five-triple coverage")


def check_packing(expected):
    fours = [m for m in range(256) if m.bit_count() == 4]
    fives = [m for m in range(256) if m.bit_count() == 5]
    sixes = [m for m in range(256) if m.bit_count() == 6]
    trials = 0
    for c in fours:
        d = 255 ^ c
        for k, rows in ((5, fives), (6, sixes)):
            for q in rows:
                require((q & c).bit_count() > k - 4 or (q & d).bit_count() > k - 4,
                        "contained repeated row")
                trials += 1
    nested = [(u, w) for u in fives for w in fives if (u & w).bit_count() <= 2]
    for u, w in nested:
        require(u | w == 255, "nested covering")
        for c in fours:
            require((c & u).bit_count() > 1 or (c & w).bit_count() > 1, "nested-four packing")
    require(expected == {"repeated_containment_trials": trials,
                         "nested_five_pairs": len(nested), "nested_four_trials": len(nested) * len(fours)},
            "packing coverage counts")


def pair_caps(ns, large_rows):
    h = [len(s) for s in ns]
    return [[(h[i] + 2 if i == j else h[i] + h[j] - (5 if j in ns[i] else 2) - len(ns[i] & ns[j]))
             - sum(i in s and j in s for s in large_rows) for j in range(10)] for i in range(10)]


WORDS4 = [(m, points(m, 10)) for m in range(1024) if m.bit_count() == 4]
WORDS5 = [(m, points(m, 10)) for m in range(1024) if m.bit_count() == 5]


def allowed(cap, row):
    return all(cap[a][b] > 0 for a, b in combinations(sorted(row), 2))


def check_bipartite_words(codes, expected):
    records = []
    i_set, w = set(range(5)), {5, 6}
    z = set(range(10)) - w
    for code in codes:
        rows = [points((code >> (5 * i)) & 31, 5) for i in range(5)]
        ns = [set() for _ in range(10)]
        for i, neighbors in enumerate(rows):
            for o in neighbors:
                ns[i].add(o + 5)
                ns[o + 5].add(i)
        require(all(len(s) == 3 for s in ns), "bipartite margins")
        cap = pair_caps(ns, [z, i_set | {5}])
        negative = any(v < 0 for row in cap for v in row)
        words = []
        if not negative:
            for word, row in WORDS4:
                if allowed(cap, row):
                    require(len(row & i_set) <= 1, "one-W word count")
                    words.append(word)
        five_hist = Counter()
        base = pair_caps(ns, [z, i_set])
        if not any(v < 0 for row in base for v in row):
            for _, row in WORDS5:
                if allowed(base, row):
                    s = len(row & i_set)
                    require(s <= 2, "five overlap")
                    five_hist[s] += 1
        w_cap = 4 - len(ns[5] & ns[6])
        require(w_cap <= 3, "blue W bound")
        require(all(15 - s > 8 + w_cap for s in five_hist), "incidence gap")
        records.append([code, negative, words, [[s, n] for s, n in sorted(five_hist.items())], w_cap])
    actual = {"records_sha256": fingerprint(records), "pair_capacity_entries": 100 * len(codes),
              "negative_six_row_controls": sum(row[1] for row in records),
              "nonnegative_six_row_controls": sum(not row[1] for row in records),
              "admissible_four_word_counts": {str(k): v for k, v in sorted(Counter(len(row[2]) for row in records).items())},
              "second_five_row_records": sum(sum(n for _, n in row[3]) for row in records)}
    require(actual == expected, "all reconstructed word/capacity records")


def check_petersen(record):
    ns = matrix_graph(record["P"])
    require(all(len(s) == 3 for s in ns), "cut model cubic")
    require(all(len(ns[i] & ns[j]) == (0 if j in ns[i] else 1)
                for i, j in combinations(range(10), 2)), "cut model pair relation")
    independent = [s for _, s in WORDS4 if all(not (ns[i] & s) for i in s)]
    require(len(independent) == 5, "cut independent fours")
    i_set = set(record["I"])
    require(i_set in independent, "distinguished independent cut")
    o_set = set(range(10)) - i_set
    # Independently decode the subdivision of K4 and complementary matching.
    outside_labels = {o: ns[o] & i_set for o in o_set}
    require(set(map(frozenset, outside_labels.values())) == set(map(frozenset, combinations(i_set, 2))),
            "six distinct K4 edge labels")
    for o in o_set:
        partner, = ns[o] & o_set
        require(outside_labels[partner] == i_set - outside_labels[o], "complementary matching")
    actual = []
    for w_tuple in combinations(sorted(o_set), 2):
        w = set(w_tuple)
        cap = pair_caps(ns, [set(range(10)) - w, i_set | w])
        require(all(v >= 0 for row in cap for v in row), "cut pair capacities")
        words = []
        for m, s in WORDS4:
            if allowed(cap, s):
                require(len(s & i_set) in (0, 1, 4), "two-W intersection sizes")
                if len(s & i_set) == 1:
                    require(s in independent, "one-I independent row")
                words.append(m)
        actual.append({"W": sorted(w), "red_W": w_tuple[1] in ns[w_tuple[0]], "four_words": words})
    require(actual == record["word_records"], "every marked Petersen word record")


def check_literal_control(control, p_plus_matrix):
    host = graph(control["graph_rows"])
    require(len(host) == 22 and all(len(s) == 10 for s in host), "control regularity")
    require(host[0] == set(range(1, 11)), "control root split")
    p = matrix_graph(control["P"])
    pp = matrix_graph(p_plus_matrix)
    x, y = control["low_pair"]
    require(x != y and pp[x] == p[x] | {y} and pp[y] == p[y] | {x}, "added low edge")
    require(all(pp[i] == p[i] for i in range(10) if i not in (x, y)), "other local edges")
    require(not (p[x] & p[y]) and len(p[x]) == len(p[y]) == 2, "disjoint low neighborhoods")
    require(all((j + 1 in host[i + 1]) == (j in p[i]) for i in range(10) for j in range(10)),
            "literal local graph")
    miss = [{i for i in range(10) if i + 1 not in host[b]} for b in range(11, 22)]
    require([sorted(s) for s in miss] == control["miss_sets"], "literal miss rows")
    require(miss[0] == set(range(10)) - {x, y} and all(len(s) == 4 for s in miss[1:]), "control row pattern")
    require(all(sum(i in s for s in miss) == len(p[i]) + 2 for i in range(10)), "column margins")
    f = [[0] * 10 for _ in range(10)]
    for i, j in combinations(range(10), 2):
        f[i][j] = f[j][i] = (3 if j in p[i] else 6) - len(page_set(host, i + 1, j + 1))
    require(f == control["F"] and all(v >= 0 for row in f for v in row), "literal F matrix")
    for i in range(10):
        for j in range(10):
            e_ij = int({i, j} == {x, y} and i != j)
            pe_ij = int(j == x and y in p[i]) + int(j == y and x in p[i])
            ep_ij = int(i == x and j in p[y]) + int(i == y and j in p[x])
            require(f[i][j] == 2 * e_ij + pe_ij + ep_ij, "F=2E+PE+EP entries")
            k = 4 * (i == j) + 3 - 3 * (j in pp[i]) - len(pp[i] & pp[j])
            require(control["K"][i][j] == k == sum(i in s and j in s for s in miss[1:]),
                    "all contracted K Gram entries")
            s0 = len(p[i]) + 2 if i == j else len(p[i]) + len(p[j]) - (5 if j in p[i] else 2) - len(p[i] & p[j])
            require(sum(i in s and j in s for s in miss) + f[i][j] == s0, "full Gram entries")
        t = sum(len(s) - 4 for s in miss if i in s)
        require(sum(f[i]) == 3 * len(p[i]) + sum(map(len, p)) - 24 - sum(len(p[j]) for j in p[i]) - t,
                "general row margins")
    c, d = control["repeated_pair"]
    require(c != d and c in host[11] and d in host[11], "repeated red neighbors")
    require(miss[c - 11] == miss[d - 11] and len(miss[c - 11]) == 4, "equal four rows")
    require(control["spine_color"] == ("red" if d in host[c] else "blue"), "literal spine color")
    actual_pages = sorted(page_set(host, c, d))
    require(actual_pages == control["literal_pages"] and len(actual_pages) > (3 if d in host[c] else 6),
            "literal forbidden book")
    # The signed whole-graph identity holds even on this invalid control.
    for i in range(22):
        for j in range(22):
            if i == j:
                require(len(host[i]) == 4 + 6, "whole-graph diagonal")
            else:
                deficit = (3 if j in host[i] else 6) - len(page_set(host, i, j))
                require(len(host[i] & host[j]) + 3 * (j in host[i]) == 6 - deficit,
                        "whole-graph signed deficit identity")
        margin = sum((3 if j in host[i] else 6) - len(page_set(host, i, j))
                     for j in range(22) if i != j)
        require(margin == 6, "whole-graph signed deficit margins")


def mutation_controls(control, p):
    bad = []
    for key in ("F", "K"):
        c = deepcopy(control)
        c[key][0][1] += 1
        bad.append(c)
    c = deepcopy(control)
    c["graph_rows"][0] = "1" + c["graph_rows"][0][1:]
    bad.append(c)
    c = deepcopy(control)
    c["miss_sets"][1] = c["miss_sets"][1][1:]
    bad.append(c)
    c = deepcopy(control)
    c["literal_pages"] = c["literal_pages"][:-1]
    bad.append(c)
    c = deepcopy(control)
    c["repeated_pair"] = [11, 12]
    bad.append(c)
    c = deepcopy(control)
    c["spine_color"] = "blue" if c["spine_color"] == "red" else "red"
    bad.append(c)
    for c in bad:
        try:
            check_literal_control(c, p)
        except ValueError:
            continue
        raise ValueError("forged control accepted")
    return len(bad)


def check_baseline(expected):
    raw = (HERE / "baseline21.rows").read_bytes()
    ns = graph(raw.decode().splitlines())
    require(len(ns) == 21, "baseline order")
    maxima = [max(len(page_set(ns, i, j)) for i, j in combinations(range(21), 2)
                  if (j in ns[i]) == red) for red in (True, False)]
    actual = {"order": len(ns), "red_edges": sum(map(len, ns)) // 2,
              "degrees": {str(k): v for k, v in sorted(Counter(map(len, ns)).items())},
              "page_maxima": maxima, "rows_sha256": hashlib.sha256(raw).hexdigest()}
    require(actual == expected and maxima == [3, 6], "primary witness")


def main():
    raw = (HERE / "expected.json").read_bytes()
    record = json.loads(raw)
    check_baseline(record["baseline"])
    check_triples(record["triple_controls"])
    check_packing(record["packing_controls"])
    codes = cycle_bipartite_codes()
    require(codes == record["bipartite_codes"], "every cubic bipartite matrix")
    check_bipartite_words(codes, record["bipartite_controls"])
    check_petersen(record["petersen_control"])
    check_literal_control(record["contraction_control"], record["petersen_control"]["P"])
    rejected = mutation_controls(record["contraction_control"], record["petersen_control"]["P"])
    print(json.dumps({"status": "PASS", "bipartite_matrices": len(codes),
                      "labeled_triple_profiles": 720, "rejected_forged_controls": rejected,
                      "literal_pair_checks": 231, "expected_sha256": hashlib.sha256(raw).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()

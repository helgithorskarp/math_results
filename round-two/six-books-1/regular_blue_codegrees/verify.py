"""Separate definition-level checks; imports no generator or helper code.

Actual author six-books-1, researcher. Written spectral/coverage arguments
are not formalized by this program. It checks all compact literal data.
"""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def graph(rows):
    n = len(rows)
    require(all(len(row) == n and set(row) <= {"0", "1"} for row in rows), "graph format")
    ns = [{j for j, value in enumerate(row) if value == "1"} for row in rows]
    require(all(i not in ns[i] and all((j in ns[i]) == (i in ns[j])
                for j in range(n)) for i in range(n)), "simple graph")
    return ns


def standard_petersen():
    ns = [set() for _ in range(10)]
    for i in range(5):
        for a, b in ((i, (i + 1) % 5), (i, i + 5), (i + 5, (i + 2) % 5 + 5)):
            ns[a].add(b)
            ns[b].add(a)
    return ns


def explicit_isomorphism(source, target):
    mapping = {}
    used = set()

    def visit():
        if len(mapping) == 10:
            return [mapping[i] for i in range(10)]
        i = max((i for i in range(10) if i not in mapping),
                key=lambda i: (len(source[i] & mapping.keys()), -i))
        for j in range(10):
            if j in used or any((k in source[i]) != (mapping[k] in target[j]) for k in mapping):
                continue
            mapping[i] = j
            used.add(j)
            answer = visit()
            if answer is not None:
                return answer
            used.remove(j)
            del mapping[i]
        return None

    answer = visit()
    require(answer is not None, "control graphs not isomorphic")
    require(all((j in source[i]) == (answer[j] in target[answer[i]])
                for i in range(10) for j in range(10)), "entrywise isomorphism")
    return answer


def fours(ns):
    result = []
    for mask in range(1 << 10):
        if mask.bit_count() != 4:
            continue
        s = {i for i in range(10) if mask >> i & 1}
        if all(not (ns[i] & s) for i in s):
            result.append(sorted(s))
    return sorted(result)


def operate(ns, v):
    return [sum(v[j] for j in ns[i]) for i in range(10)]


def k_operator(ns, v):
    pv = operate(ns, v)
    ppv = operate(ns, pv)
    return [4 * v[i] + 3 * sum(v) - 3 * pv[i] - ppv[i] for i in range(10)]


def pages(ns, i, j):
    if j in ns[i]:
        return ns[i] & ns[j]
    return set(range(len(ns))) - (ns[i] | ns[j] | {i, j})


def check_incidence_identities(ns):
    n = len(ns)
    triangle_count = clique_count = 0
    for tri in combinations(range(n), 3):
        if not all(j in ns[i] for i, j in combinations(tri, 2)):
            continue
        outside = [len(ns[w] & set(tri)) for w in range(n) if w not in tri]
        defect = sum(3 - len(ns[i] & ns[j]) for i, j in combinations(tri, 2))
        require(sum(len(ns[i]) for i in tri) == n + 9 - defect - outside.count(0) - outside.count(3),
                "signed triangle identity")
        triangle_count += 1
    for quad in combinations(range(n), 4):
        if not all(j in ns[i] for i, j in combinations(quad, 2)):
            continue
        defect = sum(3 - len(ns[i] & ns[j]) for i, j in combinations(quad, 2))
        penalty = sum((k - 1) * (k - 2) // 2
                      for w in range(n) if w not in quad for k in [len(ns[w] & set(quad))])
        require(sum(len(ns[i]) for i in quad) == n + 14 - defect - penalty,
                "signed clique identity")
        clique_count += 1
    return triangle_count, clique_count


def verify_record(record):
    p = record["P"]
    require(len(p) == 10 and all(len(row) == 10 and set(row) <= {0, 1} for row in p), "P format")
    local = graph(["".join(map(str, row)) for row in p])
    require(all(len(s) == 3 for s in local), "P cubic")
    require(all(len(local[i] & local[j]) == (0 if j in local[i] else 1)
                for i, j in combinations(range(10), 2)), "Moore pair relation")
    mapping = explicit_isomorphism(standard_petersen(), local)
    mapped_fours = sorted(sorted(mapping[i] for i in s) for s in fours(standard_petersen()))
    require(fours(local) == mapped_fours == record["independent_four_sets"], "full four-set comparison")
    require(len(mapped_fours) == 5, "four-set count")
    for i in range(10):
        y = set(range(10)) - (local[i] | {i})
        require(len(y) == 6 and all(len(local[j] & y) == 2 for j in y), "six-point complement cycle")
        triples = [s for s in combinations(sorted(y), 3)
                   if all(b not in local[a] for a, b in combinations(s, 2))]
        require(len(triples) == 2, "C6 independent triples")
    k_columns = [k_operator(local, [int(i == j) for i in range(10)]) for j in range(10)]
    k = [[k_columns[j][i] for j in range(10)] for i in range(10)]
    require(k == record["K"], "all K entries")
    require(k == [[2 * int(i == j) + 2 - 2 * int(j in local[i]) for j in range(10)]
                  for i in range(10)], "forced K simplification")
    control_pair_checks = 0
    identity_counts = [0, 0]
    for control in record["controls"]:
        ns = graph(control["graph_rows"])
        require(len(ns) == 22 and all(len(s) == 10 for s in ns), "host control regularity")
        require(ns[0] == set(range(1, 11)), "host root split")
        require(all((j + 1 in ns[i + 1]) == (j in local[i]) for i in range(10) for j in range(10)),
                "literal host local P")
        miss = [{i for i in range(10) if i + 1 not in ns[b]} for b in range(11, 22)]
        require([sorted(s) for s in miss] == control["miss_sets"], "literal miss sets")
        require(len(miss[0]) == control["large_row_size"], "large row size")
        require(all(sum(i in s for s in miss) == 5 for i in range(10)), "column margin")
        f = [[0] * 10 for _ in range(10)]
        for i, j in combinations(range(10), 2):
            f[i][j] = f[j][i] = (3 if j in local[i] else 6) - len(pages(ns, i + 1, j + 1))
        require(f == control["defect_matrix"], "all literal defect entries")
        require(all(x >= 0 for row in f for x in row), "defect nonnegativity")
        for i in range(10):
            for j in range(10):
                s = sum(i in row and j in row for row in miss)
                require(s + f[i][j] == k[i][j] + 1, "all miss Gram entries")
            t = sum(len(row) - 4 for row in miss if i in row)
            require(sum(f[i]) == 6 - t, "row defect margin")
        if len(miss[0]) == 10:
            four_rows = miss[1:]
        else:
            require(len(miss[0]) == 9 and len(miss[1]) == 5, "size9 pattern")
            omitted, = set(range(10)) - miss[0]
            require(omitted in miss[1], "forced five-row containment")
            extra = miss[1] - {omitted}
            for i in range(10):
                for j in range(10):
                    require(int(i in miss[0] and j in miss[0]) + int(i in miss[1] and j in miss[1]) + f[i][j]
                            == 1 + int(i in extra and j in extra), "all star cancellation entries")
            four_rows = miss[2:] + [extra]
        require(len(four_rows) == 10 and all(len(s) == 4 for s in four_rows), "converted four-row domain")
        require(all(not (local[i] & s) for s in four_rows for i in s), "independent converted rows")
        require(all(sum(i in s and j in s for s in four_rows) == k[i][j]
                    for i in range(10) for j in range(10)), "all converted Gram entries")
        c, d = control["repeated_pair"]
        require(c != d and c in ns[11] and d in ns[11], "repeated pair red to large row")
        require(miss[c - 11] == miss[d - 11] and len(miss[c - 11]) == 4, "repeated size4 support")
        actual = sorted(pages(ns, c, d))
        require(actual == control["literal_pages"], "literal forbidden pages")
        require(control["spine_color"] == ("red" if d in ns[c] else "blue"), "literal spine color")
        require(len(actual) > (3 if d in ns[c] else 6), "forbidden book")
        for i, j in combinations(range(22), 2):
            red_common = len(ns[i] & ns[j])
            blue_common = len(set(range(22)) - (ns[i] | ns[j] | {i, j}))
            require(blue_common == red_common + (2 if j in ns[i] else 0), "regular color codegrees")
            control_pair_checks += 1
        counts = check_incidence_identities(ns)
        identity_counts = [a + b for a, b in zip(identity_counts, counts)]
    for entry in record["negative_forms"]:
        ns = graph(entry["graph_rows"])
        require(len(ns) == 10 and all(len(s) == 3 for s in ns), "negative control cubic")
        require(all(not (ns[i] & ns[j]) for i in range(10) for j in ns[i]), "negative control triangle-free")
        v = entry["vector"]
        require(len(v) == 10 and sum(v) == 0 and all(isinstance(x, int) for x in v), "integer test form")
        kv = k_operator(ns, v)
        value = sum(a * b for a, b in zip(v, kv))
        require(value == entry["value"] and value < 0, "literal negative form")
    raw = (HERE / "baseline21.rows").read_bytes()
    ns = graph(raw.decode().splitlines())
    require(len(ns) == 21, "baseline order")
    maxima = [0, 0]
    degrees = {}
    for s in ns:
        key = str(len(s))
        degrees[key] = degrees.get(key, 0) + 1
    for i, j in combinations(range(21), 2):
        color = 0 if j in ns[i] else 1
        maxima[color] = max(maxima[color], len(pages(ns, i, j)))
    base = {"order": 21, "red_edges": sum(map(len, ns)) // 2, "degrees": degrees,
            "red_blue_page_maxima": maxima, "rows_sha256": hashlib.sha256(raw).hexdigest()}
    require(base == record["baseline"] and maxima == [3, 6], "baseline full check")
    counts = check_incidence_identities(ns)
    identity_counts = [a + b for a, b in zip(identity_counts, counts)]
    return {"control_pair_checks": control_pair_checks,
            "signed_triangle_identities": identity_counts[0],
            "signed_clique_identities": identity_counts[1],
            "explicit_petersen_isomorphism": mapping}


def main():
    raw = (HERE / "expected.json").read_bytes()
    record = json.loads(raw)
    summary = verify_record(record)
    mutations = []
    bad = deepcopy(record); bad["K"][0][1] += 1; mutations.append(bad)
    bad = deepcopy(record); bad["independent_four_sets"].pop(); mutations.append(bad)
    bad = deepcopy(record); bad["controls"][1]["defect_matrix"][0][1] += 1; mutations.append(bad)
    bad = deepcopy(record); bad["controls"][0]["literal_pages"].pop(); mutations.append(bad)
    bad = deepcopy(record); bad["controls"][1]["miss_sets"][0].pop(); mutations.append(bad)
    bad = deepcopy(record); bad["negative_forms"][0]["value"] = 0; mutations.append(bad)
    bad = deepcopy(record); bad["baseline"]["red_edges"] = 94; mutations.append(bad)
    for bad in mutations:
        try:
            verify_record(bad)
        except ValueError:
            continue
        raise ValueError("forged record accepted")
    print(json.dumps({"status": "PASS", "independent_four_sets": 5,
                      "rejected_forged_records": len(mutations), **summary,
                      "expected_sha256": hashlib.sha256(raw).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()

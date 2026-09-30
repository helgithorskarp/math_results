"""Independent exact free-involution audit; six-reviewer-1, reviewer.

CPython 3.11+, standard library. No author executable is imported.
The written proof establishes the theorem; these checks validate its bridges.
"""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n"


def mm(a, b):
    need(bool(a) and bool(b) and len(a[0]) == len(b), "matrix dimensions")
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def tr(a):
    return [list(x) for x in zip(*a)]


def minus(a, b):
    return [[x-y for x, y in zip(r, s)] for r, s in zip(a, b)]


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def sign_vector(mask, n=6):
    return tuple(1 if mask >> i & 1 else -1 for i in range(n))


def lift(q, types, inside):
    pairs = list(combinations(range(q), 2))
    need(len(types) == len(pairs) and len(inside) == q, "lift dimensions")
    need(all(x in (-1, 0, 1, 2) for x in types), "cross type")
    need(all(x in (0, 1) for x in inside), "inside type")
    red = [0] * (2*q)
    w, s = [[0]*q for _ in range(q)], [[0]*q for _ in range(q)]
    def edge(i, j):
        red[i] |= 1 << j
        red[j] |= 1 << i
    for i, flag in enumerate(inside):
        if flag:
            edge(2*i, 2*i+1)
    for (i, j), kind in zip(pairs, types):
        # -1 uniformly blue, 2 uniformly red, 1 parallel, 0 crossed.
        w[i][j] = w[j][i] = 1 if kind == 2 else -1 if kind == -1 else 0
        s[i][j] = s[j][i] = 1 if kind == 1 else -1 if kind == 0 else 0
        for u, v in product(range(2), repeat=2):
            if kind == 2 or (kind == 1 and u == v) or (kind == 0 and u != v):
                edge(2*i+u, 2*j+v)
    return red, w, s


def literal_controls():
    graphs = matching = uniform = inside_checks = 0
    for q in (3, 4):
        pairs = list(combinations(range(q), 2))
        full = (1 << (2*q)) - 1
        for types in product((-1, 0, 1, 2), repeat=len(pairs)):
            for inside in product((0, 1), repeat=q):
                red, w, s = lift(q, types, inside)
                blue = [full ^ (row | (1 << i)) for i, row in enumerate(red)]
                w2, s2 = mm(w, w), mm(s, s)
                u = [sum(row) for row in w]
                for i in range(q):
                    color = red if inside[i] else blue
                    pages = (color[2*i] & color[2*i+1]).bit_count()
                    want = 2*sum(w[i][j] == (1 if inside[i] else -1) for j in range(q))
                    need(pages == want, "inside spine identity")
                    inside_checks += 1
                for (i, j), kind in zip(pairs, types):
                    if kind in (0, 1):
                        numerator_r = q-2+u[i]+u[j]+w2[i][j]+s[i][j]*s2[i][j]
                        numerator_b = q-2-u[i]-u[j]+w2[i][j]-s[i][j]*s2[i][j]
                        need(numerator_r % 2 == numerator_b % 2 == 0, "matching parity")
                        for v in (0, 1):
                            rj = 2*j+(v if kind == 1 else 1-v)
                            bj = 2*j+(1-v if kind == 1 else v)
                            need((red[2*i+v] & red[rj]).bit_count() == numerator_r//2,
                                 "literal red matching")
                            need((blue[2*i+v] & blue[bj]).bit_count() == numerator_b//2,
                                 "literal blue matching")
                            matching += 2
                    else:
                        color = red if kind == 2 else blue
                        values = [(color[2*i] & color[2*j+v]).bit_count() for v in (0, 1)]
                        outside = sum((1+w[i][k])*(1+w[j][k]) if kind == 2
                                      else (1-w[i][k])*(1-w[j][k])
                                      for k in range(q) if k not in (i, j))
                        total = outside + 2*(inside[i]+inside[j] if kind == 2
                                                else 2-inside[i]-inside[j])
                        need(sum(values) == total and values[0]-values[1] == s2[i][j],
                             "literal uniform sum/difference")
                        uniform += 1
                graphs += 1
    return {"lifted_graphs": graphs, "matching_spines": matching,
            "uniform_sum_and_difference": uniform, "inside_spines": inside_checks}


FORMS = {
    "two_adjacent": ((0, 1), (0, 2)),
    "two_disjoint": ((0, 1), (2, 3)),
    "3k2": ((0, 1), (2, 3), (4, 5)),
    "p3k2": ((0, 1), (1, 2), (3, 4)),
    "p4": ((0, 1), (1, 2), (2, 3)),
    "star": ((0, 1), (0, 2), (0, 3)),
    "triangle": ((0, 1), (0, 2), (1, 2)),
}


def neighbors(edges, n=11):
    out = [set() for _ in range(n)]
    for i, j in edges:
        need(0 <= i < j < n, "edge normalization")
        out[i].add(j); out[j].add(i)
    return out


def census():
    n = 11
    pairs = list(combinations(range(n), 2))
    ids = {pair: i for i, pair in enumerate(pairs)}
    stats, records, expanded = [], [], []
    for name, red_edges in FORMS.items():
        red = neighbors(red_edges)
        choices = [edge for edge in pairs if edge not in red_edges]
        count = neighbor_pass = matching_pass = assignments = 0
        for blue_edges in combinations(choices, 6-len(red_edges)):
            count += 1
            blue = neighbors(blue_edges)
            if any(len(blue[i] | blue[j]) < 3 for i, j in red_edges):
                continue
            neighbor_pass += 1
            known = [red[i] | blue[i] for i in range(n)]
            u = [len(red[i])-len(blue[i]) for i in range(n)]
            good = True
            for i, j in pairs:
                if j in known[i]:
                    continue
                w2 = (len(red[i] & red[j])+len(blue[i] & blue[j])
                      -len(red[i] & blue[j])-len(blue[i] & red[j]))
                remaining = n-2-len(known[i] | known[j])
                lo, hi = -3-u[i]-u[j]+w2, -3-u[i]-u[j]-w2
                # Every unassigned signed product is +/-1. Check parity as well.
                if not any(lo <= z <= hi for z in range(-remaining, remaining+1, 2)):
                    good = False
                    break
            if not good:
                continue
            matching_pass += 1
            budgets = []
            for is_red, edges in ((True, red_edges), (False, blue_edges)):
                for i, j in edges:
                    total = 0
                    for k in range(n):
                        if k not in (i, j):
                            a = 2 if k in red[i] else 0 if k in blue[i] else 1
                            b = 2 if k in red[j] else 0 if k in blue[j] else 1
                            total += a*b if is_red else (2-a)*(2-b)
                    budgets.append((i, j, is_red, total))
            flags = []
            for word in range(1 << n):
                if any(2*len(red[i] if word >> i & 1 else blue[i]) >
                       (3 if word >> i & 1 else 6) for i in range(n)):
                    continue
                good = True
                for i, j, is_red, total in budgets:
                    inside = (word >> i & 1)+(word >> j & 1)
                    if total+2*(inside if is_red else 2-inside) > (6 if is_red else 12):
                        good = False
                        break
                if good:
                    flags.append(word)
            if flags:
                active = sorted({v for edge in red_edges+blue_edges for v in edge})
                free = [i for i in range(n) if i not in active]
                fixed = flags[0] & sum(1 << i for i in active)
                predicted = sorted(fixed | sum(1 << i for j, i in enumerate(free) if mask >> j & 1)
                                   for mask in range(1 << len(free)))
                need(flags == predicted, "active colors not uniquely determined")
                word = sum(1 << ids[edge] for edge in blue_edges)
                records.append({"red_form": name, "blue_edges": [list(e) for e in blue_edges],
                                "fixed_red_inside_mask": fixed, "free_inside_orbits": free,
                                "flag_count": len(flags)})
                expanded.append({"red_form": name, "blue_mask": word, "flags": flags})
                assignments += len(flags)
        need(count == comb(len(choices), 6-len(red_edges)), "incomplete combinations")
        stats.append({"red_form": name, "patterns": count, "three_blue_indices_pass": neighbor_pass,
                      "matching_relaxation_pass": matching_pass,
                      "survivors": sum(r["red_form"] == name for r in records),
                      "inside_assignments": assignments})
    expected = []
    for k, l in combinations(range(3, 11), 2):
        blues = tuple(sorted(((0, k), (0, l), (1, 2), (k, l))))
        free = [i for i in range(11) if i not in (0, 1, 2, k, l)]
        expected.append({"red_form": "two_adjacent", "blue_edges": [list(e) for e in blues],
                         "fixed_red_inside_mask": (1 << k) | (1 << l),
                         "free_inside_orbits": free, "flag_count": 64})
    for bridges in (((0, 2), (1, 3)), ((0, 3), (1, 2))):
        for first in (0, 1):
            partner = next(j for i, j in bridges if i == first)
            other = 5-partner
            for k in range(4, 11):
                blues = tuple(sorted(bridges+((first, k), (other, k))))
                expected.append({"red_form": "two_disjoint", "blue_edges": [list(e) for e in blues],
                                 "fixed_red_inside_mask": 1 << k,
                                 "free_inside_orbits": [i for i in range(11) if i not in (0, 1, 2, 3, k)],
                                 "flag_count": 64})
    key = lambda r: (r["red_form"], r["blue_edges"])
    need(sorted(records, key=key) == sorted(expected, key=key), "case coverage differs from analytic A/B")
    expanded.sort(key=lambda r: (r["red_form"], r["blue_mask"]))
    return {"forms": stats, "patterns": sum(x["patterns"] for x in stats),
            "survivors": records, "inside_assignments": sum(x["inside_assignments"] for x in stats),
            "expanded_records_sha256": hashlib.sha256(canonical(expanded).encode()).hexdigest()}, expanded


def no_red_blocks():
    partitions = []
    for n3 in range(4):
        for n2 in range(6):
            n1 = 11-3*n3-2*n2
            if n1 < 0:
                continue
            reason = ("singleton/triple square gap" if n1 and n3 else
                      "two-clique difference: 24 not divisible by16" if n1 and n2 else
                      "two-clique sum: 40 not divisible by16" if n3 and n2 else
                      "singleton eigenvalue multiplicity55/7")
            need(n1 or (n2 and n3), "missing partition case")
            partitions.append([n1, n2, n3, reason])
    scalar_pairs, triple_pairs = set(), set()
    for h in range(-9, 10):
        k = [[37, 4*h], [4*h, 37]]
        for row in product((-2, 2), repeat=2):
            if mm([row], k) == [[49*x for x in row]]:
                scalar_pairs.add(h)
        for values in product((-2, 2), repeat=6):
            cross = [list(values[:3]), list(values[3:])]
            if mm(k, cross) == [[33*x for x in row] for row in cross]:
                triple_pairs.add(h)
    need(scalar_pairs == {-3, 3} and triple_pairs == {-1, 1}, "clique commutation")
    for h in (1, 3):
        k = [[37, 4*h], [4*h, 37]]
        intertwiners = []
        for values in product((-2, 2), repeat=4):
            x = [list(values[:2]), list(values[2:])]
            if mm(k, x) == mm(x, k):
                intertwiners.append(x)
        need(len(intertwiners) == 4 and all(x[0][0] == x[1][1] and x[0][1] == x[1][0]
                                             for x in intertwiners), "two-clique cross blocks")
    need((25-1) % 16 and (41-1) % 16 and 55 % 7, "integrality obstruction")
    return {"partitions": partitions, "singleton_two_h": sorted(scalar_pairs),
            "triple_two_h": sorted(triple_pairs)}


def blue_three():
    cases, total = [], 0
    for name in ("3k2", "p3k2", "p4", "star", "triangle"):
        d_edges = FORMS[name]
        d = neighbors(d_edges)
        candidates = [edge for edge in combinations(range(11), 2)
                      if edge not in d_edges and all(i in edge or j in edge for i, j in d_edges)
                      and len(d[edge[0]] | d[edge[1]]) >= 3]
        rejected = 0
        for mask in range(1, 1 << len(candidates)):
            red_edges = [edge for i, edge in enumerate(candidates) if mask >> i & 1]
            r = neighbors(red_edges)
            witness = [(i, j) for i, j in combinations(range(11), 2)
                       if j not in r[i] | d[i] and not r[i] and not r[j] and d[i] & d[j]]
            need(witness, "three-blue pattern needs an additional obstruction")
            rejected += 1
        cases.append({"blue_form": name, "possible_red_uniform_pairs": [list(e) for e in candidates],
                      "nonempty_red_subsets_rejected": rejected})
        total += rejected
    need(total == 130, "three-blue case coverage")
    return {"cases": cases, "nonempty_red_subsets_rejected": total,
            "seven_pair_color_splits": [[2, 5], [3, 4]]}


def vector_obstructions():
    vectors = {mask: sign_vector(mask) for mask in range(64)}
    balanced = [mask for mask in vectors if mask.bit_count() == 3]
    low = [mask for mask in vectors if mask.bit_count() == 2]
    adjacent = {a: [b for b in balanced if dot(vectors[a], vectors[b]) == -2] for a in balanced}
    ga = [[8, -8], [-8, 8]]
    ta = [[-3, -2], [-2, -1]]
    ca = minus(mm(ta, ga), mm(ga, tr(ta)))
    need(ca == [[0, 16], [-16, 0]], "shape A symmetry defect")
    count_a = 0
    for i in balanced:
        for j in adjacent[i]:
            for k in set(adjacent[i]) & set(adjacent[j]):
                for l in set(adjacent[i]) & set(adjacent[j]) & set(adjacent[k]):
                    rows = [vectors[x] for x in (i, j, k, l)]
                    p = [x+y for x, y in zip(rows[0], rows[1])]
                    q = [x+y for x, y in zip(rows[2], rows[3])]
                    need(mm([p, q], tr([p, q])) == ga, "shape A Gram")
                    count_a += 1
    gb = [[6, -2, -2], [-2, 6, -2], [-2, -2, 6]]
    tb = [[-1, -1, -1], [-1, -3, -1], [-1, -1, -3]]
    cb = minus(mm(tb, gb), mm(gb, tr(tb)))
    need(cb == [[0, -4, -4], [4, 0, 0], [4, 0, 0]], "shape B symmetry defect")
    count_b = 0
    example = None
    for i in balanced:
        for j in adjacent[i]:
            compatible = [x for x in low if dot(vectors[x], vectors[i]) == dot(vectors[x], vectors[j]) == 0]
            for k, l in product(compatible, repeat=2):
                if dot(vectors[k], vectors[l]) != -2:
                    continue
                rows = [[1]*6, vectors[k], vectors[l]]
                need(mm(rows, tr(rows)) == gb, "shape B Gram")
                example = rows
                count_b += 1
    need(count_a == 720 and count_b == 2160, "normalized row coverage")
    # Solve G M + M G = 2T exactly; C0=F^T M F minimizes the symmetric relaxation.
    p = [[F(1, 3)]*3 for _ in range(3)]
    q = [[F(int(i == j))-p[i][j] for j in range(3)] for i in range(3)]
    ptp, qtq, ptq, qtp = mm(mm(p, tb), p), mm(mm(q, tb), q), mm(mm(p, tb), q), mm(mm(q, tb), p)
    m = [[ptp[i][j]/2+qtq[i][j]/8+(ptq[i][j]+qtp[i][j])/5 for j in range(3)] for i in range(3)]
    need([[x+y for x, y in zip(a, b)] for a, b in zip(mm(gb, m), mm(m, gb))] == [[2*x for x in row] for row in tb],
         "symmetric least-squares normal equation")
    c0 = mm(mm(tr(example), m), example)
    error = minus(mm(example, c0), mm(tb, example))
    need(c0 == tr(c0) and sum(x*x for row in error for x in row) == F(16, 5), "sharp B residual")
    stationarity = mm(tr(example), error)
    need(stationarity == [[-x for x in row] for row in tr(stationarity)], "residual stationarity")
    return {"A_normalized_row_tuples": count_a, "B_normalized_row_tuples": count_b,
            "A_TG_minus_GTt": ca, "B_TG_minus_GTt": cb,
            "A_sharp_squared_residual_any_linear_C": "16",
            "B_sharp_squared_residual_symmetric_C": "16/5",
            "B_minimizer_coefficient_M": [[str(x) for x in row] for row in m]}


def compare_records(expanded, other):
    need(isinstance(other, list) and len(other) == len(expanded), "author record count")
    def index(records):
        out = {}
        for r in records:
            need(set(r) == {"red_form", "blue_mask", "flags"}, "record schema")
            need(isinstance(r["blue_mask"], int) and isinstance(r["flags"], list), "record types")
            key = (r["red_form"], r["blue_mask"])
            need(key not in out and r["flags"] == sorted(set(r["flags"])), "duplicate/noncanonical record")
            out[key] = r["flags"]
        return out
    need(index(expanded) == index(other), "entrywise survivor/flag mismatch")


def controls(expanded):
    import copy
    bad = []
    missing = copy.deepcopy(expanded); missing.pop(); bad.append(missing)
    flag = copy.deepcopy(expanded); flag[0]["flags"].pop(); bad.append(flag)
    pair = copy.deepcopy(expanded); pair[0]["blue_mask"] ^= 1; bad.append(pair)
    tag = copy.deepcopy(expanded); tag[0]["red_form"] = "star"; bad.append(tag)
    for item in bad:
        try:
            compare_records(expanded, item)
        except ValueError:
            continue
        raise ValueError("corrupted record accepted")
    return len(bad)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--compare-author-records", type=Path)
    args = parser.parse_args()
    local = literal_controls()
    finite, expanded = census()
    result = {"agent": "six-reviewer-1", "role": "independent mathematical reviewer",
              "literal_controls": local, "reduced_complete_census": finite,
              "no_red_clique_checks": no_red_blocks(), "blue_minimum_four": blue_three(),
              "gram_obstructions": vector_obstructions(), "corrupted_record_rejections": controls(expanded),
              "full_graph_or_matching_signing_enumeration": False}
    if args.compare_author_records:
        other = [json.loads(line) for line in args.compare_author_records.read_text().splitlines() if line.strip()]
        compare_records(expanded, other)
    if args.check:
        need(json.loads(args.check.read_text()) == result, "expected output mismatch")
    print(canonical(result), end="")


if __name__ == "__main__":
    main()

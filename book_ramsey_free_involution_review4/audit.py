"""Independent exact audit by six-reviewer-4, independent mathematical reviewer.

No campaign executable imports. Standard library only. Scratch is mandatory
and must be outside this contribution. C++ and Python run sequentially.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, permutations, product
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
N = 11
PAIRS = tuple(combinations(range(N), 2))
CORES = {
    "A": ([(0, 1), (0, 2)], [(0, 3), (0, 4), (1, 2), (3, 4)]),
    "B": ([(0, 1), (2, 3)], [(0, 2), (0, 4), (1, 3), (3, 4)]),
    "X": ([(0, 1), (2, 3)], [(0, 2), (0, 3), (1, 2), (1, 4), (3, 4)]),
}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def rows(red, blue):
    r, b = [0]*N, [0]*N
    for links, matrix in ((red, r), (blue, b)):
        for i, j in links:
            matrix[i] |= 1 << j
            matrix[j] |= 1 << i
    return r, b


def admissible_flags(red, blue):
    """Literal uniform-spine capacities plus inside-orbit spine capacities.

    Only active variables are enumerated; isolated quotient vertices are
    unconstrained here and all their assignments are added explicitly.
    """
    r, b = rows(red, blue)
    active = sorted({v for edge in red+blue for v in edge})
    passive = sorted(set(range(N))-set(active))
    rules = []
    for color, links in ((1, red), (0, blue)):
        for i, j in links:
            ni = r[i] if color else b[i]
            nj = r[j] if color else b[j]
            opposite_i = b[i] if color else r[i]
            opposite_j = b[j] if color else r[j]
            outside = 0
            for k in range(N):
                if k == i or k == j:
                    continue
                di = 2 if ni >> k & 1 else 0 if opposite_i >> k & 1 else 1
                dj = 2 if nj >> k & 1 else 0 if opposite_j >> k & 1 else 1
                outside += di*dj
            rules.append((i, j, color, outside))
    accepted = []
    for values in product((0, 1), repeat=len(active)):
        eps = dict(zip(active, values))
        if any((eps[i] and 2*r[i].bit_count() > 3) or
               (not eps[i] and 2*b[i].bit_count() > 6) for i in active):
            continue
        if any(outside+2*(eps[i]+eps[j] if color else 2-eps[i]-eps[j])
               > (6 if color else 12) for i, j, color, outside in rules):
            continue
        word = sum(eps[i] << i for i in active)
        for extras in product((0, 1), repeat=len(passive)):
            accepted.append(word+sum(value << i for i, value in zip(passive, extras)))
    return sorted(accepted)


def reference_census(adjacent):
    """Set cuts and signed intersections; no matrix multiplication.

    itertools gives all five-subsets independently of the C++ successor
    implementation. Every accepted inside-color word is returned.
    """
    red = [(0, 1), (0, 2)] if adjacent else [(0, 1), (2, 3)]
    available = [e for e in PAIRS if e not in red]
    r, _ = rows(red, [])
    cuts = []
    for i, j in red:
        edge_masks = []
        for k, l in available:
            mask = 0
            if k in (i, j):
                mask |= 1 << l
            if l in (i, j):
                mask |= 1 << k
            edge_masks.append(mask)
        cuts.append(edge_masks)
    first, second = cuts
    counts = Counter()
    records = {}
    for a, b, c, d, e in combinations(range(len(available)), 5):
        counts["all_patterns"] += 1
        if (first[a] | first[b] | first[c] | first[d] | first[e]).bit_count() < 3:
            continue
        if (second[a] | second[b] | second[c] | second[d] | second[e]).bit_count() < 3:
            continue
        counts["blue_cover_pass"] += 1
        blue = [available[k] for k in (a, b, c, d, e)]
        _, nb = rows([], blue)
        if any((r[i] & r[j]).bit_count()+(nb[i] & nb[j]).bit_count()
               > (r[i] & nb[j]).bit_count()+(nb[i] & r[j]).bit_count()
               for i, j in PAIRS if not ((r[i] | nb[i]) >> j & 1)):
            continue
        counts["matching_square_pass"] += 1
        flags = admissible_flags(red, blue)
        if flags:
            records[tuple(blue)] = flags
    counts["survivor_patterns"] = len(records)
    counts["survivor_flags"] = sum(map(len, records.values()))
    return dict(counts), records


def template_records(adjacent):
    """All labelled images of the three stated shapes, with literal flags."""
    base_red = [(0, 1), (0, 2)] if adjacent else [(0, 1), (2, 3)]
    m = 3 if adjacent else 4
    templates = [("A+blue", CORES["A"][0], CORES["A"][1]+[(5, 6)])] if adjacent else [
        ("B+blue", CORES["B"][0], CORES["B"][1]+[(5, 6)]),
        ("X", CORES["X"][0], CORES["X"][1])]
    result, class_sizes = {}, {}
    for name, red, blue in templates:
        active_outside = sorted({v for edge in blue for v in edge if v >= m})
        images = {}
        for perm in permutations(range(m)):
            mapped_red = sorted(tuple(sorted((perm[i], perm[j]))) for i, j in red)
            if mapped_red != base_red:
                continue
            for outside in permutations(range(m, N), len(active_outside)):
                mapping = dict(enumerate(perm))
                mapping.update(zip(active_outside, outside))
                image = tuple(sorted(tuple(sorted((mapping[i], mapping[j]))) for i, j in blue))
                if image not in images:
                    images[image] = admissible_flags(base_red, list(image))
        require(not (set(images) & set(result)), "templates must be disjoint")
        result.update(images)
        class_sizes[name] = {"patterns": len(images),
                             "flags": sum(map(len, images.values()))}
    return result, class_sizes


def formula_checks(base=1, inside=2):
    """All 512 six-vertex lifts, compared with literal common-page sets."""
    checks = 0
    links = [(0, 1), (0, 2), (1, 2)]
    types = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for choices in product(types, repeat=3):
        w, s = [[0]*3 for _ in range(3)], [[0]*3 for _ in range(3)]
        for (i, j), (wij, sij) in zip(links, choices):
            w[i][j] = w[j][i] = wij
            s[i][j] = s[j][i] = sij
        for eps in product((0, 1), repeat=3):
            graph = [set() for _ in range(6)]
            for i in range(3):
                if eps[i]:
                    graph[2*i].add(2*i+1); graph[2*i+1].add(2*i)
            for (i, j), (wij, sij) in zip(links, choices):
                for x, y in product((0, 1), repeat=2):
                    red = wij == 1 or (wij == 0 and sij == (1 if x == y else -1))
                    if red:
                        graph[2*i+x].add(2*j+y); graph[2*j+y].add(2*i+x)
            blue_graph = [set(range(6))-{i}-graph[i] for i in range(6)]
            u = list(map(sum, w))
            for i in range(3):
                require(len(graph[2*i]) == 2+u[i]+eps[i], "red degree identity")
                checks += 1
            for i, j in links:
                color = 1 if w[i][j] == 1 else 0
                if not w[i][j]:
                    w2 = sum(w[i][k]*w[j][k] for k in range(3))
                    s2 = sum(s[i][k]*s[j][k] for k in range(3))
                    for x, y in product((0, 1), repeat=2):
                        red = y in {v % 2 for v in graph[2*i+x] if v//2 == j}
                        pages = len((graph if red else blue_graph)[2*i+x] &
                                    (graph if red else blue_graph)[2*j+y])
                        numerator = base+(u[i]+u[j] if red else -u[i]-u[j])+w2
                        numerator += s[i][j]*s2 if red else -s[i][j]*s2
                        require(numerator == 2*pages, "matching page identity")
                        checks += 1
                else:
                    neighborhood = graph if color else blue_graph
                    pages = [len(neighborhood[2*i] & neighborhood[2*j+y]) for y in (0, 1)]
                    other = 3-i-j
                    expected = (1+w[i][j]*w[i][other])*(1+w[i][j]*w[j][other])
                    expected += inside*(eps[i]+eps[j] if color else 2-eps[i]-eps[j])
                    require(sum(pages) == expected, "uniform combined page identity")
                    require(pages[0]-pages[1] == sum(s[i][k]*s[j][k] for k in range(3)),
                            "uniform difference identity")
                    checks += 2
    return checks


def linear_checks():
    vectors = [tuple(1 if i in pos else -1 for i in range(6))
               for pos in combinations(range(6), 3)]
    require(all(dot(a, b) % 4 == 2 for a, b in product(vectors, repeat=2)),
            "balanced-six parity")
    a_cases = 0
    for p1, p2 in product(vectors, repeat=2):
        if dot(p1, p2) != -2:
            continue
        candidates = [v for v in vectors if dot(v, p1) == dot(v, p2) == -2]
        for q1, q2 in product(candidates, repeat=2):
            if dot(q1, q2) != -2:
                continue
            p, q = tuple(x+y for x, y in zip(p1, p2)), tuple(x+y for x, y in zip(q1, q2))
            require(all(x+y == 0 for x, y in zip(p, q)), "A zero sum")
            require(dot(p, p) == 8, "A nonzero sum")
            a_cases += 1
    a = (1,)*6
    twoplus = [tuple(1 if i in pos else -1 for i in range(6))
               for pos in combinations(range(6), 2)]
    b_cases = 0
    for r1, r2 in product(twoplus, repeat=2):
        if dot(r1, r2) != -2:
            continue
        ta = tuple(-x-y-z for x, y, z in zip(a, r1, r2))
        tr1 = tuple(-x-3*y-z for x, y, z in zip(a, r1, r2))
        require(dot(ta, r1) == -2 and dot(a, tr1) == 2, "B symmetry margin4")
        b_cases += 1
    # Squared-trace check of the author's larger invariant-space argument.
    m = [[-1, -1, -1], [-1, -3, -1], [-1, -1, -3]]
    k = [[-2, -1], [-1, -2]]
    squared_trace = sum(sum(x[i][j]*x[j][i] for j in range(len(x)))
                        for x in (m, k) for i in range(len(x)))
    require(squared_trace == 35 > 6*5, "Frobenius shortage5")
    return {"balanced_vectors": len(vectors), "shape_A_vector_tuples": a_cases,
            "shape_B_pair_tuples": b_cases, "shape_B_paired_inner_products": [-2, 2],
            "shape_B_squared_trace": squared_trace, "six_sign_matrix_squared_trace": 30,
            "shape_X_balanced_orthogonality_possible": False}


def compare_records(observed, expected):
    require(observed == expected, "complete survivor/flag entries differ")


def rejected(action):
    try:
        action()
    except RuntimeError:
        return True
    raise RuntimeError("corruption was accepted")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--write-expected", action="store_true")
    args = parser.parse_args()
    scratch = args.scratch.resolve()
    require(scratch != HERE and HERE not in scratch.parents, "external scratch required")
    scratch.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                 "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        env[name] = "1"
    start = time.monotonic()
    p = subprocess.run(["g++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Wpedantic",
                        str(HERE/"census.cpp"), "-o", str(scratch/"census")],
                       capture_output=True, text=True, timeout=60, env=env)
    require(p.returncode == 0 and not p.stderr, "warning-free C++ build required: "+p.stderr)
    p = subprocess.run([str(scratch/"census")], capture_output=True, text=True, timeout=60, env=env)
    require(p.returncode == 0, "census did not complete")
    (scratch/"census.jsonl").write_text(p.stdout)
    cpp_records, cpp_counts = {0: {}, 1: {}}, {}
    for line in p.stdout.splitlines():
        entry = json.loads(line)
        adjacent = entry["adjacent_red"]
        if entry.get("record"):
            blue = tuple(tuple(e) for e in entry["blue"])
            require(blue not in cpp_records[adjacent], "duplicate C++ record")
            cpp_records[adjacent][blue] = entry["flags"]
        else:
            require(entry["complete"], "incomplete C++ case")
            cpp_counts[adjacent] = {k: v for k, v in entry.items()
                                    if k not in ("adjacent_red", "complete")}
    summary, all_records = {}, {}
    for adjacent in (0, 1):
        counts, reference = reference_census(adjacent)
        templates, classes = template_records(adjacent)
        require(counts == cpp_counts[adjacent], "every C++/Python case count differs")
        compare_records(cpp_records[adjacent], reference)
        compare_records(reference, templates)
        serial = [[list(map(list, blue)), flags] for blue, flags in sorted(reference.items())]
        summary[str(adjacent)] = {"counts": counts, "classes": classes,
                                  "entry_sha256": digest(serial)}
        all_records[adjacent] = reference
    identities = formula_checks()
    linear = linear_checks()
    first = all_records[0]
    truncated = dict(first); truncated.pop(next(iter(truncated)))
    corrupted = {k: list(v) for k, v in first.items()}; corrupted[next(iter(corrupted))][0] ^= 1
    controls = [rejected(lambda: formula_checks(base=0)),
                rejected(lambda: formula_checks(inside=1)),
                rejected(lambda: compare_records(truncated, first)),
                rejected(lambda: compare_records(corrupted, first))]
    result = {"agent": "six-reviewer-4", "role": "independent mathematical reviewer",
              "complete": True, "formula_identity_comparisons": identities,
              "linear_checks": linear, "seven_uniform_two_red": summary,
              "every_survivor_and_flag_entry_compared": True,
              "corruption_controls_rejected": len(controls),
              "uses_degree_bound_or_peer_executable": False,
              "full_matching_signing_enumeration": False,
              "full_order22_coloring_enumeration": False}
    expected = HERE/"EXPECTED.json"
    if args.write_expected:
        expected.write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")
    else:
        require(result == json.loads(expected.read_text()), "expected evidence differs")
    receipt = {"status": "passed", "expected_sha256": hashlib.sha256(expected.read_bytes()).hexdigest(),
               "wall_seconds": time.monotonic()-start, "python": sys.version.split()[0],
               "peak_child_rss_kib_linux": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               "peak_self_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (scratch/"validation.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()

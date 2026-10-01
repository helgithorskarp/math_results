#!/usr/bin/env python3
"""Independent root-degree census and literal KG(7,2) page audit.

No imports from the author's programs. All decisions use exact integers
and explicit guards, including under python -O.
"""
import argparse
from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path
import time

ROOTS = tuple(range(7))
EDGES = tuple(combinations(ROOTS, 2))
VERTICES = tuple(frozenset(e) for e in EDGES)
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}
WHOLE = (1 << 21) - 1


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encoded(edges):
    return sum(1 << EDGE_INDEX[tuple(sorted(e))] for e in edges)


def normalized(mask):
    return mask ^ WHOLE if mask & 1 else mask


def templates():
    yield "empty", 0
    for m in (3, 4, 5, 6):
        for support in combinations(ROOTS, m):
            yield "K%d" % m, encoded(combinations(support, 2))
    for u, h in ((2, 3), (2, 4), (3, 3)):
        for support in combinations(ROOTS, u + h):
            for universal in combinations(support, u):
                leaves = set(support) - set(universal)
                edges = list(combinations(universal, 2))
                edges += [(x, y) for x in universal for y in leaves]
                yield "J%d_%d" % (u, h), encoded(edges)


def degree_domain():
    """All 2^20 cuts omitting 01, traversed in Gray order.

    Maintain root adjacency/degrees by one-edge changes. Condition D at
    root v is min{d(a): va in F} >= max{d(b): vb outside F}+2, whenever
    both sets are nonempty. This does not compute any switched codegree.
    """
    adjacency = [0] * 7
    degree = [0] * 7
    survivors = []
    previous_gray = 0
    scanned = 0
    for assignment in range(1 << 20):
        gray = assignment ^ (assignment >> 1)
        if assignment:
            changed = (gray ^ previous_gray).bit_length()
            a, b = EDGES[changed]
            delta = -1 if adjacency[a] & (1 << b) else 1
            adjacency[a] ^= 1 << b
            adjacency[b] ^= 1 << a
            degree[a] += delta
            degree[b] += delta
        previous_gray = gray
        scanned += 1
        good = True
        for v in ROOTS:
            if degree[v] in (0, 6):
                continue
            low_neighbor, high_non_neighbor = 7, -1
            for w in ROOTS:
                if w == v:
                    continue
                if adjacency[v] & (1 << w):
                    low_neighbor = min(low_neighbor, degree[w])
                else:
                    high_non_neighbor = max(high_non_neighbor, degree[w])
            if low_neighbor < high_non_neighbor + 2:
                good = False
                break
        if good:
            cut = gray << 1
            require(not cut & 1, "normalization failed")
            require(all(adjacency[v].bit_count() == degree[v] for v in ROOTS),
                    "incremental degree drift")
            survivors.append(cut)
    require(scanned == 1048576, "incomplete Gray domain")
    require(len(set(survivors)) == len(survivors), "duplicate Gray survivor")
    return scanned, set(survivors)


def red(cut, i, j):
    require(i != j, "diagonal is not a spine")
    return VERTICES[i].isdisjoint(VERTICES[j]) != (
        bool(cut & (1 << i)) != bool(cut & (1 << j)))


def page_histogram(adjacency):
    n = len(adjacency)
    blue = [set(range(n)) - adjacency[i] - {i} for i in range(n)]
    hist = {"red": Counter(), "blue": Counter()}
    for i, j in combinations(range(n), 2):
        color = "red" if j in adjacency[i] else "blue"
        rows = adjacency if color == "red" else blue
        hist[color][len(rows[i] & rows[j])] += 1
    require(sum(map(sum, (hist["red"].values(), hist["blue"].values()))) == n * (n - 1) // 2,
            "missing spine")
    return {color: dict(sorted(counts.items())) for color, counts in hist.items()}


def literal_pages(cut):
    adjacency = [{j for j in range(21) if j != i and red(cut, i, j)}
                 for i in range(21)]
    return page_histogram(adjacency)


def attachment_audit():
    """Construct every intersecting two-set family: stars or triangles.

    Written proof supplies equivalence to red-B4-free attachments;
    computation tests every resulting whole 22-vertex coloring.
    """
    families = set()
    for a in ROOTS:
        star = [i for i, e in enumerate(EDGES) if a in e]
        for bits in range(64):
            families.add(frozenset(star[i] for i in range(6) if bits & (1 << i)))
    for triple in combinations(ROOTS, 3):
        families.add(frozenset(EDGE_INDEX[e] for e in combinations(triple, 2)))
    require(len(families) == 456, "intersecting-family count differs")
    counts = Counter()
    equalities = []
    for family in sorted(families, key=lambda s: tuple(sorted(s))):
        require(all(not VERTICES[i].isdisjoint(VERTICES[j])
                    for i, j in combinations(family, 2)), "nonintersecting attachment")
        adjacency = [{j for j in range(21) if j != i and red(0, i, j)}
                     for i in range(21)]
        for i in family:
            adjacency[i].add(21)
        adjacency.append(set(family))
        hist = page_histogram(adjacency)
        require(max(hist["red"]) == 3, "intersecting attachment creates red B4")
        blue_max = max(hist["blue"])
        counts[str(blue_max)] += 1
        if blue_max == 8:
            equalities.append(sum(1 << i for i in family))
        if len(family) == 6:
            require(blue_max == 8, "full star not sharp eight")
        elif len(family) == 5:
            require(blue_max == 9, "five-edge star not sharp nine")
        else:
            require(blue_max == 10, "remaining family not ten")
    require(dict(counts) == {"8": 7, "9": 42, "10": 407}, "attachment histogram differs")
    return {"intersecting_red_neighbor_families": 456,
            "maximum_blue_pages_histogram": dict(sorted(counts.items(), key=lambda x: int(x[0]))),
            "eight_page_full_star_families": sorted(equalities)}


def check_local_identity(cut):
    degree = [sum(bool(cut & (1 << i)) for i, e in enumerate(EDGES) if v in e)
              for v in ROOTS]
    controls = 0
    for v in ROOTS:
        others = [x for x in ROOTS if x != v]
        for a in others:
            i = EDGE_INDEX[tuple(sorted((v, a)))]
            if not cut & (1 << i):
                continue
            for b in others:
                if a == b:
                    continue
                j = EDGE_INDEX[tuple(sorted((v, b)))]
                if cut & (1 << j):
                    continue
                pages = [k for k in range(21) if k not in (i, j)
                         and red(cut, i, k) and red(cut, j, k)]
                require(red(cut, i, j), "mixed intersecting spine not red")
                require(len(pages) == 5 + degree[b] - degree[a],
                        "local degree identity fails")
                controls += 1
    return controls


def audit(run_domain=True):
    classified = {}
    for kind, mask in templates():
        key = normalized(mask)
        require(key not in classified, "root templates overlap modulo complement")
        classified[key] = kind
    counts = dict(sorted(Counter(classified.values()).items()))
    require(counts == {"J2_3": 210, "J2_4": 105, "J3_3": 140,
                       "K3": 35, "K4": 35, "K5": 21, "K6": 7, "empty": 1},
            "labeled template count differs")
    scanned = None
    if run_domain:
        scanned, survivors = degree_domain()
        require(survivors == set(classified), "analytic D coverage disagrees with sweep")
    profiles = {}
    records = []
    local_checks = 0
    for cut, kind in sorted(classified.items()):
        local_checks += check_local_identity(cut)
        histogram = literal_pages(cut)
        require(histogram == literal_pages(cut ^ WHOLE), "cut-complement mismatch")
        if kind in profiles:
            require(profiles[kind] == histogram, "root label changes page profile")
        else:
            profiles[kind] = histogram
        rmax, bmax = max(histogram["red"]), max(histogram["blue"])
        if rmax < 4:
            records.append([cut, rmax, bmax])
            require(kind not in ("K3", "J2_3"), "red obstruction failed")
        else:
            require(kind in ("K3", "J2_3"), "additional red obstruction")
    require(len(records) == 309, "red-free classification count differs")
    equality = [cut for cut, _, blue_max in records if blue_max == 10]
    stars = [normalized(encoded((a, x) for x in ROOTS if x != a)) for a in ROOTS]
    require(sorted(equality) == sorted(stars), "ten-page equality is not exactly stars")
    record_sha256 = hashlib.sha256(json.dumps(records, separators=(",", ":"))
                                   .encode("ascii")).hexdigest()
    output = {
        "reviewer": "six-reviewer-2", "role": "independent mathematical reviewer",
        "degree_cuts_scanned": scanned, "degree_condition_cuts": len(classified),
        "template_counts": counts, "local_identity_checks": local_checks,
        "profiles": profiles, "red_B4_free_cuts": len(records),
        "maximum_blue_pages_histogram": dict(sorted(Counter(str(r[2]) for r in records)
                                                     .items(), key=lambda x: int(x[0]))),
        "record_sha256": record_sha256, "ten_page_star_cuts": sorted(equality),
        "unswitched_attachment": attachment_audit(),
    }
    # JSON object keys are strings; normalize before expected-file equality.
    return json.loads(json.dumps(output)), records


def compare_author(records, path):
    candidate = json.loads(path.read_text())
    require(candidate["cuts_scanned"] == 1048576, "author coverage summary damaged")
    require(candidate["records"] == records, "author records differ entrywise")
    require(candidate["red_B4_free_cuts"] == len(records), "author survivor count differs")
    digest = hashlib.sha256(json.dumps(records, separators=(",", ":"))
                            .encode("ascii")).hexdigest()
    require(candidate["record_sha256"] == digest, "author record digest differs")
    histogram = dict(sorted(Counter(str(r[2]) for r in records).items(),
                            key=lambda x: int(x[0])))
    require(candidate["maximum_blue_pages_histogram"] == histogram,
            "author histogram differs")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--records", type=Path)
    parser.add_argument("--author-records", type=Path)
    parser.add_argument("--skip-domain", action="store_true",
                        help="fixture-only run; never report as full degree census")
    args = parser.parse_args()
    started = time.monotonic()
    output, records = audit(not args.skip_domain)
    if args.author_records:
        compare_author(records, args.author_records)
    if not args.skip_domain:
        expected_path = Path(__file__).with_name("EXPECTED.json")
        if expected_path.exists():
            require(output == json.loads(expected_path.read_text()), "expected output differs")
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    if args.records:
        args.records.write_text(json.dumps(records, separators=(",", ":")) + "\n")
    print(rendered, end="")
    print("elapsed_seconds=%.3f" % (time.monotonic() - started))


if __name__ == "__main__":
    main()

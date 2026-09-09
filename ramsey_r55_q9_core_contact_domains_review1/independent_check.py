#!/usr/bin/env python3
"""Independent audit of h4059 contact counts, arithmetic, and physical output.

The reviewer C++ census enumerates ordered row triples directly.  It neither
uses the target's row-multiset weights nor its labelled-column DFS.  This
Python layer imports no target module and checks the target replay only as
files and physical graph records.
"""
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path
import argparse
import hashlib
import json
import re
import struct
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "ramsey_r55_q9_core_contact_domains"
PARENT = ROOT / "ramsey_r55_packing_augmentation"
PAIR43 = list(combinations(range(43), 2))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse_graph6(line):
    require(type(line) is bytes and len(line) == 5 and line[0] == 70, "graph6 shape")
    require(all(63 <= byte <= 126 for byte in line), "graph6 character")
    bits = [((byte - 63) >> shift) & 1 for byte in line[1:] for shift in range(5, -1, -1)]
    require(bits[21:] == [0, 0, 0], "graph6 padding")
    rows = [0] * 7
    position = 0
    for v in range(1, 7):
        for u in range(v):
            if bits[position]:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
            position += 1
    for vertices in combinations(range(7), 4):
        colors = {((rows[u] >> v) & 1) for u, v in combinations(vertices, 2)}
        require(colors == {0, 1}, "catalogue core is not Ramsey(4,4)")
    return rows


def load_cores(cache):
    raw = (Path(cache) / "r44_7.g6").read_bytes()
    require(len(raw) == 2172, "catalogue byte count")
    require(hashlib.sha256(raw).hexdigest() == "6a3da7f0687c392420f190db0643b5c5b7ecb1a3c5ed098c7d96200185a5f010",
            "catalogue digest")
    lines = raw.splitlines()
    require(len(lines) == len(set(lines)) == 362, "catalogue records")
    return [parse_graph6(line) for line in lines]


def graph_word(rows):
    return sum(((rows[u] >> v) & 1) << k for k, (u, v) in enumerate(combinations(range(7), 2)))


def permuted_complement_word(rows, permutation):
    return sum((1 ^ ((rows[permutation[u]] >> permutation[v]) & 1)) << k
               for k, (u, v) in enumerate(combinations(range(7), 2)))


def read_counts(path, columns):
    records = [list(map(int, line.split())) for line in Path(path).read_text().splitlines()]
    require(len(records) == 362, "count record total")
    require(all(len(row) == columns and row[0] == i for i, row in enumerate(records)), "count record shape")
    return records


def verify_target_manifest():
    manifest = json.loads((TARGET / "MANIFEST.json").read_text())
    require(set(manifest) == {path.name for path in TARGET.iterdir() if path.is_file() and path.name != "MANIFEST.json"},
            "target manifest coverage")
    for name, digest in manifest.items():
        require(sha256(TARGET / name) == digest, "target manifest mismatch: " + name)
    return hashlib.sha256((TARGET / "MANIFEST.json").read_bytes()).hexdigest()


def run_ordered_census(cache, out):
    executable = out / "ordered_rows"
    counts = out / "ordered_rows.tsv"
    build = ["g++", "-std=c++20", "-O3", "-Wall", "-Wextra", "-Wpedantic",
             str(HERE / "ordered_rows.cpp"), "-o", str(executable)]
    completed = subprocess.run(build, text=True, capture_output=True)
    require(completed.returncode == 0 and not completed.stdout and not completed.stderr, "reviewer census build")
    completed = subprocess.run([str(executable), str(Path(cache) / "r44_7.g6"), str(counts)],
                               text=True, capture_output=True)
    require(completed.returncode == 0 and not completed.stderr, "reviewer census run")
    receipt = json.loads(completed.stdout)
    require(receipt["status"] == "ORDERED_ROW_CENSUS_COMPLETE" and receipt["records"] == 362,
            "reviewer census receipt")
    return counts, receipt


def complement_audit(cores, rows):
    words = {graph_word(core): i for i, core in enumerate(cores)}
    require(len(words) == 362, "literal catalogue duplicate")
    involutions = 0
    for i, record in enumerate(rows):
        _, plain, joint, destination, packed = record
        require(0 < joint <= plain <= 15 ** 7, "contact count bounds")
        permutation = [(packed >> (3 * k)) & 7 for k in range(7)]
        require(sorted(permutation) == list(range(7)), "complement permutation")
        require(words.get(permuted_complement_word(cores[i], permutation)) == destination,
                "complement certificate")
        require(rows[destination][1] > 0, "blue contact domain")
        reverse = rows[destination][3]
        involutions += reverse == i
    require(involutions == 362, "complement destination is not involutive")
    return {"edge_identities": 362 * 21, "involutive_destinations": involutions}


def parent_and_global_audit(rows, target_expected):
    parent = json.loads((PARENT / "EXPECTED.json").read_text())
    require(len(parent["classes"]) == 18, "parent class count")
    before = after = q9_before = q9_after = 0
    affected = 0
    maximum = Fraction(0)
    minimum = Fraction(1)
    q9_classes = []
    for entry in parent["classes"]:
        q, r, core_count = entry["q"], entry["r"], entry["core_count"]
        a, b = r - 1, q - r
        matrix = (comb(1998 + a - 1, a) * comb(1931 + b - 1, b)
                  * 37823 ** (comb(a, 2) + comb(b, 2)) * 35714 ** (a * b))
        old_per_task = matrix * 15 ** (q * (43 - 4 * q))
        require(old_per_task == entry["per_task"], "parent physical factorization")
        old_retained = entry["retained_per_task"]
        require(old_retained <= old_per_task, "parent retained bound")
        class_before = core_count * old_retained
        before += class_before
        if q == 9:
            require(core_count == 362, "q9 catalogue multiplicity")
            require(old_retained == matrix * (50151 * 15 ** 3) ** r * (15 ** 7) ** b,
                    "q9 h4035 factorization")
            local = [matrix * record[2] ** r * rows[record[3]][1] ** b for record in rows]
            require(all(0 < value < old_retained for value in local), "q9 strict positive reduction")
            class_after = sum(local)
            fractions = [Fraction(value, old_retained) for value in local]
            minimum = min(minimum, min(fractions))
            maximum = max(maximum, max(fractions))
            q9_before += class_before
            q9_after += class_after
            affected += core_count
            q9_classes.append({"r": r, "before": class_before, "after": class_after})
        else:
            class_after = class_before
        after += class_after
    require(before == parent["new_carrier"], "parent carrier total")
    removed = Fraction(before - after, before)
    q9_removed = Fraction(q9_before - q9_after, q9_before)
    census = target_expected["census"]
    require((before, after, q9_before, q9_after) ==
            (census["before"], census["after"], census["q9_before"], census["q9_after"]),
            "target aggregate mismatch")
    require(removed == Fraction(**census["removed_fraction"]), "target global fraction")
    require(q9_removed == Fraction(**census["q9_removed_fraction"]), "target q9 fraction")
    require(maximum == Fraction(**census["maximum_task_retained"]), "target maximum task fraction")
    require(2 * after <= before and affected == 1810, "declared global gate")
    return {
        "before": before,
        "after": after,
        "affected_tasks": affected,
        "q9_before": q9_before,
        "q9_after": q9_after,
        "removed_numerator": removed.numerator,
        "removed_denominator": removed.denominator,
        "q9_removed_numerator": q9_removed.numerator,
        "q9_removed_denominator": q9_removed.denominator,
        "minimum_task_retained_numerator": minimum.numerator,
        "minimum_task_retained_denominator": minimum.denominator,
        "maximum_task_retained_numerator": maximum.numerator,
        "maximum_task_retained_denominator": maximum.denominator,
        "q9_classes": q9_classes,
    }


def decode_physical(obj):
    require(type(obj) is dict and obj.get("n") == 43, "physical order")
    text = obj.get("red_hex")
    require(type(text) is str and re.fullmatch(r"[0-9a-f]{226}", text), "physical word syntax")
    word = int(text, 16)
    require(word < 1 << 903, "physical word padding")
    rows = [0] * 43
    for k, (u, v) in enumerate(PAIR43):
        if (word >> k) & 1:
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return rows


def color(rows, u, v):
    return (rows[u] >> v) & 1


def monochromatic(rows, vertices, wanted):
    return all(color(rows, u, v) == wanted for u, v in combinations(vertices, 2))


def first_monochromatic_five(rows, vertices):
    for chosen in combinations(vertices, 5):
        for wanted in (0, 1):
            if monochromatic(rows, chosen, wanted):
                return chosen, wanted
    return None


def has_global_monochromatic_five(rows):
    """Exact bitset clique search; used only to establish fixture non-targets."""
    for wanted in (0, 1):
        neighbors = []
        for u in range(43):
            mask = 0
            for v in range(43):
                if u != v and color(rows, u, v) == wanted:
                    mask |= 1 << v
            neighbors.append(mask)

        def visit(depth, allowed):
            if depth == 5:
                return True
            needed = 5 - depth
            while allowed.bit_count() >= needed:
                bit = allowed & -allowed
                allowed -= bit
                vertex = bit.bit_length() - 1
                if visit(depth + 1, allowed & neighbors[vertex]):
                    return True
            return False

        if visit(0, (1 << 43) - 1):
            return True
    return False


def selected_matching(core):
    available = set(range(7))
    answer = []
    for u, v in combinations(range(7), 2):
        if u in available and v in available and ((core[u] >> v) & 1):
            answer.append((36 + u, 36 + v))
            available.remove(u)
            available.remove(v)
    require(len(answer) >= 2, "selected matching")
    return answer[:2]


def task_size(r, core_index, counts):
    a, b = r - 1, 9 - r
    matrix = (comb(1998 + a - 1, a) * comb(1931 + b - 1, b)
              * 37823 ** (comb(a, 2) + comb(b, 2)) * 35714 ** (a * b))
    return matrix * counts[core_index][2] ** r * counts[counts[core_index][3]][1] ** b


def physical_audit(cache, replay, cores, counts, expected):
    stream = Path(replay) / "normal-physical" / "physical.jsonl"
    require(stream.is_file(), "target physical stream missing")
    digest = hashlib.sha256(stream.read_bytes()).hexdigest()
    require(digest == expected["physical"]["physical_sha256"], "target physical stream digest")
    seen = {}
    five_sets = 0
    global_defects = 0
    for line in stream.read_text().splitlines():
        item = json.loads(line)
        match = re.fullmatch(r"bo1-q9-r([5-9])-c([0-9]{6})", item["task"])
        require(match is not None, "physical task syntax")
        r, core_index = map(int, match.groups())
        require(0 <= core_index < 362, "physical core index")
        size = task_size(r, core_index, counts)
        require(item["code"] in (0, size // 2, size - 1), "physical test index")
        key = item["task"]
        seen.setdefault(key, set()).add(item["code"])
        rows = decode_physical(item["graph"])
        core = cores[core_index]
        for u, v in combinations(range(7), 2):
            require(color(rows, 36 + u, 36 + v) == ((core[u] >> v) & 1), "fixed physical core")
        for block in range(9):
            vertices = range(4 * block, 4 * block + 4)
            require(all(color(rows, u, v) == int(block < r) for u, v in combinations(vertices, 2)),
                    "fixed physical block")
        root_words = []
        for block in range(1, 9):
            signatures = [sum(color(rows, u, 4 * block + v) << u for u in range(4)) for v in range(4)]
            require(signatures == sorted(signatures, reverse=True), "root column order")
            root_words.append(sum(color(rows, u, 4 * block + v) << (4 * u + v)
                                  for u in range(4) for v in range(4)))
        require(root_words[:r - 1] == sorted(root_words[:r - 1], reverse=True), "red block order")
        require(root_words[r - 1:] == sorted(root_words[r - 1:], reverse=True), "blue block order")
        for first, second in combinations(range(9), 2):
            vertices = list(range(4 * first, 4 * first + 4)) + list(range(4 * second, 4 * second + 4))
            require(first_monochromatic_five(rows, vertices) is None, "block-pair Ramsey domain")
            five_sets += comb(8, 5)
        edge, other = selected_matching(core)
        for block in range(9):
            vertices = list(range(4 * block, 4 * block + 4)) + list(range(36, 43))
            require(first_monochromatic_five(rows, vertices) is None, "block-core contact domain")
            five_sets += comb(11, 5)
            if block < r:
                base = list(range(4 * block, 4 * block + 4))
                for chosen in combinations(base, 2):
                    remainder = [v for v in base if v not in chosen]
                    augmentation = (all(color(rows, u, v) for u in chosen for v in edge)
                                    and all(color(rows, u, v) for u in remainder for v in other))
                    require(not augmentation, "selected augmentation retained")
        if has_global_monochromatic_five(rows):
            global_defects += 1
    require(len(seen) == 1810 and all(len(values) == 3 for values in seen.values()), "physical task coverage")
    require(five_sets == 33524820, "physical literal five-set count")
    require(global_defects == 5430, "fixture non-target defects")
    return {
        "records": 5430,
        "tasks": len(seen),
        "literal_local_five_sets": five_sets,
        "records_with_global_defect": global_defects,
        "stream_sha256": digest,
    }


def small_cube_audit():
    cases = assignments = 0
    for n in range(4):
        for word in range(1 << (n * (n - 1) // 2)):
            core_edges = {(u, v): (word >> k) & 1 for k, (u, v) in enumerate(combinations(range(n), 2))}
            for columns in product(range(16), repeat=n):
                assignments += 1
                valid = all(column != 15 for column in columns)
                if valid:
                    for vertices in combinations(range(n), 2):
                        if core_edges[vertices]:
                            valid &= (columns[vertices[0]] & columns[vertices[1]]).bit_count() <= 2
                    for vertices in combinations(range(n), 3):
                        if all(core_edges[edge] for edge in combinations(vertices, 2)):
                            valid &= (columns[vertices[0]] & columns[vertices[1]] & columns[vertices[2]]).bit_count() <= 1
                # Cross-check by literal five-sets in the induced red-block/core graph.
                matrix = [[0] * (4 + n) for _ in range(4 + n)]
                for u, v in combinations(range(4), 2): matrix[u][v] = matrix[v][u] = 1
                for (u, v), value in core_edges.items(): matrix[4 + u][4 + v] = matrix[4 + v][4 + u] = value
                for v, column in enumerate(columns):
                    for u in range(4): matrix[u][4 + v] = matrix[4 + v][u] = (column >> u) & 1
                literal = not any(len({matrix[u][v] for u, v in combinations(chosen, 2)}) == 1
                                  for chosen in combinations(range(4 + n), 5))
                require(valid == literal, "small-cube contact theorem")
            cases += 1
    # Two four-vertex cores exercise the selected matching and its packing
    # exclusion.  This check derives the event once from common-neighbour
    # masks and once from the literal two-K4 definition.
    for word in (33, 47):
        core_edges = {(u, v): (word >> k) & 1 for k, (u, v) in enumerate(combinations(range(4), 2))}
        available = set(range(4))
        matching = []
        for u, v in combinations(range(4), 2):
            if core_edges[u, v] and u in available and v in available:
                matching.append((u, v))
                available.remove(u)
                available.remove(v)
        require(len(matching) == 2, "small-cube matching")
        first, second = matching
        for columns in product(range(16), repeat=4):
            assignments += 1
            valid = all(column != 15 for column in columns)
            if valid:
                for vertices in combinations(range(4), 2):
                    if core_edges[vertices]:
                        valid &= (columns[vertices[0]] & columns[vertices[1]]).bit_count() <= 2
                for vertices in combinations(range(4), 3):
                    if all(core_edges[edge] for edge in combinations(vertices, 2)):
                        valid &= (columns[vertices[0]] & columns[vertices[1]] & columns[vertices[2]]).bit_count() <= 1
            z_first = columns[first[0]] & columns[first[1]]
            z_second = columns[second[0]] & columns[second[1]]
            accepted = valid and not (z_first.bit_count() == 2 and z_second == (15 ^ z_first))

            matrix = [[0] * 8 for _ in range(8)]
            for u, v in combinations(range(4), 2): matrix[u][v] = matrix[v][u] = 1
            for (u, v), value in core_edges.items(): matrix[4 + u][4 + v] = matrix[4 + v][4 + u] = value
            for v, column in enumerate(columns):
                for u in range(4): matrix[u][4 + v] = matrix[4 + v][u] = (column >> u) & 1
            literal_valid = not any(len({matrix[u][v] for u, v in combinations(chosen, 2)}) == 1
                                    for chosen in combinations(range(8), 5))
            literal_augmentation = any(
                all(matrix[u][4 + v] for part, edge in ((chosen, first), (remainder, second))
                    for u in part for v in edge)
                for chosen in combinations(range(4), 2)
                for remainder in ([v for v in range(4) if v not in chosen],)
            )
            require(accepted == (literal_valid and not literal_augmentation), "small-cube augmentation theorem")
        cases += 1
    require((cases, assignments) == (14, 164369), "small cube totals")
    return {"core_cases": cases, "assignments": assignments}


def prefix_audit(replay, counts):
    path = Path(replay) / "prefix-release.bin"
    raw = path.read_bytes()
    width = 8257
    require(len(raw) == 362 * 2 * width * 4, "prefix byte length")
    boundaries = 0
    for core in range(362):
        for joint in (False, True):
            values = struct.unpack_from("<8257I", raw, (2 * core + int(joint)) * width * 4)
            require(values[0] == 0 and values[-1] == counts[core][2 if joint else 1], "prefix endpoint")
            require(all(a <= b for a, b in zip(values, values[1:])), "prefix monotonicity")
            boundaries += len(values)
    return {"boundaries": boundaries, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main(cache, replay, out, check_expected=False):
    start = time.monotonic()
    out = Path(out)
    out.mkdir()
    target_manifest = verify_target_manifest()
    cores = load_cores(cache)
    review_counts_path, native = run_ordered_census(cache, out)
    review_counts = read_counts(review_counts_path, 3)
    target_counts = read_counts(TARGET / "COUNTS.tsv", 5)
    target_release = read_counts(Path(replay) / "row_count-release.tsv", 5)
    target_columns = read_counts(Path(replay) / "column_check-release.tsv", 3)
    require(target_counts == target_release, "target release/committed row counts")
    require(target_columns == [row[:3] for row in target_counts], "target independent column counts")
    require(review_counts == [row[:3] for row in target_counts], "reviewer ordered-row counts")
    target_expected = json.loads((Path(replay) / "RESULT.json").read_text())
    require(hashlib.sha256((Path(replay) / "RESULT.json").read_bytes()).hexdigest() ==
            "f465b07c3546dc295272cdf1ea771fbd0340dd0b5b0c620f23194714dfc5e4ba", "target result digest")
    native_seconds = native.pop("seconds")
    evidence = {
        "status": "INDEPENDENT_H4059_ACCEPT",
        "target_manifest_sha256": target_manifest,
        "target_result_sha256": sha256(Path(replay) / "RESULT.json"),
        "reviewer_counts_sha256": sha256(review_counts_path),
        "native_ordered_rows": native,
        "contact_counts": {
            "records": 362,
            "entrywise_agreements": 362 * 3,
            "plain_range": [min(row[1] for row in review_counts), max(row[1] for row in review_counts)],
            "joint_range": [min(row[2] for row in review_counts), max(row[2] for row in review_counts)],
        },
        "complements": complement_audit(cores, target_counts),
        "global": parent_and_global_audit(target_counts, target_expected),
        "prefix": prefix_audit(replay, target_counts),
        "physical": physical_audit(cache, replay, cores, target_counts, target_expected),
        "small_cubes": small_cube_audit(),
        "target_found": False,
        "new_task_decisions": 0,
        "solver_calls": 0,
    }
    runtime = {"native_ordered_rows_seconds": native_seconds, "total_seconds": time.monotonic() - start}
    if check_expected:
        require(evidence == json.loads((HERE / "EXPECTED.json").read_text()), "committed review expectation mismatch")
    (out / "EVIDENCE.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    (out / "RUNTIME.json").write_text(json.dumps(runtime, indent=2, sort_keys=True) + "\n")
    print(json.dumps(evidence, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True)
    parser.add_argument("--target-replay", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    main(args.cache, args.target_replay, args.out, args.check_expected)

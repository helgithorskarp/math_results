#!/usr/bin/env python3
"""Independent checker for the complete h4045 packing-destination bridge.

The primary census uses adjacent-transposition orbit walks, rather than the
target's direct catalogue-permutation table construction.  It imports no
target Python module.  The target compiler is exercised only as a black-box
subprocess, and the target replay's physical JSONL certificates are checked
with the literal graph predicates below.
"""

from array import array
from collections import Counter
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "ramsey_r55_packing_destination_bridge"
PAIR43 = list(combinations(range(43), 2))
PAIR43_INDEX = {edge: k for k, edge in enumerate(PAIR43)}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def digest_obj(obj):
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def digest_list(values):
    return hashlib.sha256(canonical_bytes(values)).hexdigest()


def input_specs():
    return json.loads((TARGET / "INPUTS.json").read_text())


def catalog_lines(cache, n):
    spec = next(row for row in input_specs() if row["n"] == n)
    raw = (Path(cache) / spec["name"]).read_bytes()
    require(len(raw) == spec["bytes"], f"catalogue length n={n}")
    require(hashlib.sha256(raw).hexdigest() == spec["sha256"],
            f"catalogue hash n={n}")
    lines = raw.splitlines()
    require(len(lines) == spec["count"], f"catalogue count n={n}")
    require(len(set(lines)) == len(lines), f"literal duplicate n={n}")
    return lines


def parse_graph6(line, n):
    """Definition-level graph6 parser returning adjacency bit rows."""
    m = n * (n - 1) // 2
    require(type(line) is bytes and len(line) == 1 + (m + 5) // 6,
            "graph6 row size")
    require(line[0] == n + 63 and all(63 <= value <= 126 for value in line),
            "graph6 row syntax")
    payload = [value - 63 for value in line[1:]]
    rows = [0] * n
    bit_number = 0
    for high in range(1, n):
        for low in range(high):
            value = (payload[bit_number // 6] >> (5 - bit_number % 6)) & 1
            if value:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            bit_number += 1
    while bit_number < 6 * len(payload):
        require(((payload[bit_number // 6] >> (5 - bit_number % 6)) & 1) == 0,
                "graph6 nonzero padding")
        bit_number += 1
    return rows


def word_from_rows(rows):
    return sum(((rows[u] >> v) & 1) << k
               for k, (u, v) in enumerate(combinations(range(len(rows)), 2)))


def edge_masks(n, size):
    pairs = list(combinations(range(n), 2))
    index = {edge: k for k, edge in enumerate(pairs)}
    return [sum(1 << index[edge] for edge in combinations(vertices, 2))
            for vertices in combinations(range(n), size)]


def swap_adjacent(word, n, position, index):
    """Relabel by the adjacent transposition (position, position+1)."""
    out = word
    left, right = position, position + 1
    for vertex in range(n):
        if vertex in (left, right):
            continue
        a = index[tuple(sorted((left, vertex)))]
        b = index[tuple(sorted((right, vertex)))]
        if ((word >> a) ^ (word >> b)) & 1:
            out ^= (1 << a) | (1 << b)
    return out


def orbit_owners(cache, n):
    """Build all labelled orbits using Cayley-graph walks on adjacent swaps."""
    lines = catalog_lines(cache, n)
    representatives = [word_from_rows(parse_graph6(line, n)) for line in lines]
    pairs = list(combinations(range(n), 2))
    index = {edge: k for k, edge in enumerate(pairs)}
    owners = array("h", [-1]) * (1 << len(pairs))
    orbit_sizes = []
    for catalog_id, representative in enumerate(representatives):
        require(owners[representative] == -1, "catalogue isomorphism duplicate")
        owners[representative] = catalog_id
        queue = [representative]
        cursor = 0
        while cursor < len(queue):
            word = queue[cursor]
            cursor += 1
            for position in range(n - 1):
                moved = swap_adjacent(word, n, position, index)
                previous = owners[moved]
                require(previous in (-1, catalog_id), "orbit ownership collision")
                if previous == -1:
                    owners[moved] = catalog_id
                    queue.append(moved)
        orbit_sizes.append(len(queue))

    masks = edge_masks(n, 4)
    accepted = 0
    for word in range(len(owners)):
        admissible = all((word & mask) not in (0, mask) for mask in masks)
        require((owners[word] >= 0) == admissible,
                f"catalogue completeness mismatch n={n}, word={word}")
        accepted += int(admissible)

    raw_owners = array("h", owners)
    if sys.byteorder != "little":
        raw_owners.byteswap()
    return owners, {
        "n": n,
        "labelled_inputs": len(owners),
        "accepted": accepted,
        "rejected": len(owners) - accepted,
        "catalog_records": len(representatives),
        "orbit_sizes_sha256": digest_list(orbit_sizes),
        "owners_sha256": hashlib.sha256(raw_owners.tobytes()).hexdigest(),
    }


def selected_matching(rows, wanted):
    available = (1 << len(rows)) - 1
    chosen = []
    for u, v in combinations(range(len(rows)), 2):
        if (available >> u) & 1 and (available >> v) & 1 and (rows[u] >> v) & 1:
            chosen.append((u, v))
            available &= ~(1 << u)
            available &= ~(1 << v)
    require(len(chosen) >= wanted, "greedy matching too short")
    return tuple(chosen[:wanted])


def induced_word(rows, vertices):
    return sum(((rows[vertices[i]] >> vertices[j]) & 1) << k
               for k, (i, j) in enumerate(combinations(range(len(vertices)), 2)))


def deletion_census(cache, source_n, owners):
    wanted = 4 if source_n == 11 else 2
    destination_n = source_n - 4
    histogram = Counter()
    per_source = Counter()
    matching_histogram = Counter()
    total = 0
    for line in catalog_lines(cache, source_n):
        rows = parse_graph6(line, source_n)
        matching = selected_matching(rows, wanted)
        matching_histogram[tuple(vertex for edge in matching for vertex in edge)] += 1
        destinations = set()
        for first, second in combinations(matching, 2):
            deleted = set(first + second)
            vertices = [v for v in range(source_n) if v not in deleted]
            word = induced_word(rows, vertices)
            catalog_id = owners[word]
            require(catalog_id >= 0, "induced destination absent from catalogue")
            histogram[catalog_id] += 1
            destinations.add(catalog_id)
            total += 1
        per_source[len(destinations)] += 1
    matching_json = json.dumps(
        sorted((list(key), count) for key, count in matching_histogram.items()),
        separators=(",", ":"),
    ).encode()
    destination_count = max(owners) + 1
    return {
        "source_order": source_n,
        "destination_order": destination_n,
        "source_cores": len(catalog_lines(cache, source_n)),
        "deletions": total,
        "destination_histogram": [histogram[i] for i in range(destination_count)],
        "distinct_destination_records": len(histogram),
        "destinations_per_source_histogram": [list(item) for item in sorted(per_source.items())],
        "distinct_selected_matchings": len(matching_histogram),
        "matching_histogram_sha256": hashlib.sha256(matching_json).hexdigest(),
    }


def parse_task(task):
    match = re.fullmatch(r"bo1-q(7|8|9|10)-r(5|6|7|8|9|10)-c([0-9]{6})", task)
    require(match is not None, "task syntax")
    q, r, c = map(int, match.groups())
    counts = {7: 640, 8: 546356, 9: 362, 10: 4}
    require(5 <= r <= q and 0 <= c < counts[q], "task range")
    return q, r, c


def physical_variable(u, v):
    if u > v:
        u, v = v, u
    return u * (85 - u) // 2 + v - u


def own_suffix(cache, task):
    q, r, c = parse_task(task)
    if q not in (8, 9):
        return []
    rows = parse_graph6(catalog_lines(cache, 43 - 4 * q)[c], 43 - 4 * q)
    matching = selected_matching(rows, 4 if q == 8 else 2)
    answer = []
    for block_number in range(r):
        block = list(range(4 * block_number, 4 * block_number + 4))
        for first, second in combinations(matching, 2):
            for chosen in combinations(block, 2):
                complement = [v for v in block if v not in chosen]
                clause = []
                for part, edge in ((chosen, first), (complement, second)):
                    for u in part:
                        for v in edge:
                            clause.append(-physical_variable(u, 4 * q + v))
                answer.append(clause)
    return answer


def black_box_suffixes(cache, target_expected):
    checked_tasks = []
    clauses = 0
    for row in target_expected["formulas"]["full_formula_representatives"]:
        task = row["task"]
        command = [
            sys.executable, "-B", str(TARGET / "compile_family.py"), str(cache),
            "--task", task, "--physical-suffix",
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        require(completed.returncode == 0, "target suffix subprocess failed")
        result = json.loads(completed.stdout)
        expected = own_suffix(cache, task)
        require(result["clauses"] == expected, f"target suffix mismatch {task}")
        require(result["scope"] == "NEW_GLOBAL_COVER_NOT_A_FIXED_TASK_RAMSEY_IMPLICATE",
                "target suffix scope")
        checked_tasks.append(task)
        clauses += len(expected)
    return {"tasks": checked_tasks, "task_count": len(checked_tasks), "clauses": clauses,
            "literals": 8 * clauses}


def decode_graph(obj):
    require(type(obj) is dict and obj.get("n") == 43, "physical graph order")
    text = obj.get("red_hex")
    require(type(text) is str and re.fullmatch(r"[0-9a-f]{226}", text),
            "physical graph word")
    word = int(text, 16)
    require(word < 1 << 903, "physical graph padding")
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


def has_clique(rows, vertices, wanted, size):
    candidate = sum(1 << v for v in vertices)
    full = (1 << 43) - 1

    def search(pool, remaining):
        if remaining == 0:
            return True
        if pool.bit_count() < remaining:
            return False
        while pool:
            bit = pool & -pool
            pool -= bit
            vertex = bit.bit_length() - 1
            adjacency = rows[vertex] if wanted else (full ^ rows[vertex] ^ (1 << vertex))
            if search(pool & adjacency, remaining - 1):
                return True
        return False

    return search(candidate, size)


def physical_identity(source, target, new_to_old):
    require(type(new_to_old) is list and all(type(v) is int for v in new_to_old),
            "permutation type")
    require(sorted(new_to_old) == list(range(43)), "physical permutation")
    before = decode_graph(source)
    after = decode_graph(target)
    for u, v in PAIR43:
        require(color(after, u, v) == color(before, new_to_old[u], new_to_old[v]),
                "physical edge identity")
    return 903


def carrier_check(cache, task, graph):
    q, r, c = parse_task(task)
    rows = decode_graph(graph)
    core_n = 43 - 4 * q
    core = parse_graph6(catalog_lines(cache, core_n)[c], core_n)
    for block in range(q):
        require(monochromatic(rows, range(4 * block, 4 * block + 4), int(block < r)),
                "fixed block colour")
    for u, v in combinations(range(core_n), 2):
        require(color(rows, 4 * q + u, 4 * q + v) == color(core, u, v),
                "catalogue core edge")
    words = []
    for block in range(1, q):
        signatures = [sum(color(rows, u, 4 * block + v) << u for u in range(4))
                      for v in range(4)]
        require(signatures == sorted(signatures, reverse=True), "root column ordering")
        words.append(sum(color(rows, u, 4 * block + v) << (4 * u + v)
                         for u in range(4) for v in range(4)))
    require(words[:r - 1] == sorted(words[:r - 1], reverse=True), "red block ordering")
    require(words[r - 1:] == sorted(words[r - 1:], reverse=True), "blue block ordering")
    for first, second in combinations(range(q), 2):
        vertices = list(range(4 * first, 4 * first + 4)) + list(range(4 * second, 4 * second + 4))
        require(not has_clique(rows, vertices, 0, 5) and not has_clique(rows, vertices, 1, 5),
                "two-block domain")
    for block in range(q):
        block_vertices = list(range(4 * block, 4 * block + 4))
        for vertex in range(4 * q, 43):
            require(not all(color(rows, u, vertex) == int(block < r) for u in block_vertices),
                    "block/core-star domain")
    remainder = list(range(4 * r, 43))
    require(not has_clique(rows, remainder, 1, 4), "red maximality")
    return q, r, rows


def check_normalization(cache, source, certificate):
    require(certificate.get("status") == "ORDERED_CARRIER_NO_RAMSEY_VERDICT",
            "normalization status")
    q, r, _ = parse_task(certificate["task"])
    require(q == len(source["blocks"]) and r == source["r"] and q in (9, 10),
            "normalization class")
    checks = physical_identity(source, certificate["graph"], certificate["new_to_old"])
    carrier_check(cache, certificate["task"], certificate["graph"])
    permutation = certificate["new_to_old"]
    require(permutation[:4] == source["blocks"][0], "root preservation")
    source_red = {frozenset(block) for block in source["blocks"][:r]}
    source_blue = {frozenset(block) for block in source["blocks"][r:]}
    target_red = {frozenset(permutation[4 * i:4 * i + 4]) for i in range(r)}
    target_blue = {frozenset(permutation[4 * i:4 * i + 4]) for i in range(r, q)}
    require(source_red == target_red and source_blue == target_blue,
            "normalization block partition")
    require(sorted(permutation[4 * q:]) == sorted(source["core"]),
            "normalization core partition")
    source_rows = decode_graph(source)
    root = source["blocks"][0]
    expected_children = []
    for block in source["blocks"][1:]:
        ordered = sorted(block, key=lambda v: (-sum(color(source_rows, u, v) << i
                                                   for i, u in enumerate(root)), v))
        expected_children.append(ordered)
    def root_word(block):
        return sum(color(source_rows, u, v) << (4 * i + j)
                   for i, u in enumerate(root) for j, v in enumerate(block))
    expected_children = (sorted(expected_children[:r - 1], key=root_word, reverse=True) +
                         sorted(expected_children[r - 1:], key=root_word, reverse=True))
    require(permutation[:4 * q] == root + sum(expected_children, []),
            "deterministic block normalization")
    return checks


def augmentation_violation(rows, q, r):
    if q == 10:
        return False
    core = list(range(4 * q, 43))
    core_rows = [sum(color(rows, core[i], core[j]) << j for j in range(len(core)))
                 for i in range(len(core))]
    matching_local = selected_matching(core_rows, 4 if q == 8 else 2)
    matching = [tuple(core[i] for i in edge) for edge in matching_local]
    for block_number in range(r):
        block = list(range(4 * block_number, 4 * block_number + 4))
        for first, second in combinations(matching, 2):
            for chosen in combinations(block, 2):
                complement = [v for v in block if v not in chosen]
                if all(color(rows, u, v) for part, edge in ((chosen, first),
                                                            (complement, second))
                       for u in part for v in edge):
                    return True
    return False


def check_reduction(cache, source, certificate):
    require(certificate.get("source_sha256") == digest_obj(source), "source binding")
    source_rows = decode_graph(source)
    if certificate.get("status") == "MONOCHROMATIC_FIVE":
        vertices = certificate.get("vertices")
        wanted = certificate.get("color")
        require(type(vertices) is list and len(vertices) == len(set(vertices)) == 5,
                "five-set shape")
        require(all(type(v) is int and 0 <= v < 43 for v in vertices) and wanted in (0, 1),
                "five-set range")
        require(monochromatic(source_rows, vertices, wanted), "five-set physical witness")
        return 10, None
    require(certificate.get("status") == "REDUCED_FAMILY_CARRIER_NO_RAMSEY_VERDICT",
            "reduction status")
    require(certificate["source_task"] == source["task"], "source task binding")
    q, r, _ = parse_task(source["task"])
    carrier_check(cache, source["task"], source)
    current = {"n": 43, "red_hex": source["red_hex"]}
    composed = list(range(43))
    checks = 0
    steps = certificate["steps"]
    require(type(steps) is list and len(steps) <= 10 - q, "step bound")
    current_task = source["task"]
    for step in steps:
        exchange = step["exchange"]
        normalization = step["normalization"]
        partition = {
            **current,
            "blocks": [list(range(4 * i, 4 * i + 4)) for i in range(q)],
            "core": list(range(4 * q, 43)),
            "r": r,
        }
        require(exchange.get("status") == "PACKING_TRANSPORT_NEEDS_CATALOG_AND_ROOT_ORDER",
                "exchange status")
        require(exchange.get("source_sha256") == digest_obj(partition), "exchange binding")
        replaced = exchange["replaced_block"]
        require(type(replaced) is int and 0 <= replaced < r, "replaced red block")
        first, second = exchange["new_blocks_old_labels"]
        block = partition["blocks"][replaced]
        require(len(first) == len(second) == 4 and len(set(first + second)) == 8,
                "exchange block size")
        require(set(first + second).intersection(block) == set(block), "exchange old block")
        require(len(set(first).intersection(block)) == len(set(second).intersection(block)) == 2,
                "exchange complementary split")
        current_rows = decode_graph(current)
        require(monochromatic(current_rows, first, 1) and monochromatic(current_rows, second, 1),
                "new red blocks")
        first_edge = tuple(sorted(set(first) - set(block)))
        second_edge = tuple(sorted(set(second) - set(block)))
        core = partition["core"]
        core_rows = [sum(color(current_rows, core[i], core[j]) << j
                         for j in range(len(core))) for i in range(len(core))]
        selected_local = selected_matching(core_rows, 4 if q == 8 else 2)
        selected = {tuple(core[i] for i in edge) for edge in selected_local}
        require(first_edge in selected and second_edge in selected and first_edge != second_edge,
                "selected matching edges")
        red_blocks = [old for i, old in enumerate(partition["blocks"][:r]) if i != replaced]
        expected_blocks = red_blocks + [first, second] + partition["blocks"][r:]
        expected_core = [v for v in core if v not in first_edge + second_edge]
        exchange_permutation = sum(expected_blocks, []) + expected_core
        require(exchange["new_to_old"] == exchange_permutation, "exchange permutation")
        output = exchange["output"]
        require(output["r"] == r + 1 and
                output["blocks"] == [list(range(4 * i, 4 * i + 4)) for i in range(q + 1)] and
                output["core"] == list(range(4 * (q + 1), 43)), "exchange output partition")
        checks += physical_identity(current, output, exchange_permutation)
        checks += check_normalization(cache, output, normalization)
        through_exchange = [composed[v] for v in exchange_permutation]
        composed = [through_exchange[v] for v in normalization["new_to_old"]]
        current = normalization["graph"]
        current_task = normalization["task"]
        q += 1
        r += 1
    require(certificate["destination_task"] == current_task and certificate["graph"] == current,
            "final graph/task binding")
    require(certificate["new_to_old"] == composed, "composed permutation")
    checks += physical_identity(source, certificate["graph"], composed)
    final_q, final_r, final_rows = carrier_check(cache, current_task, current)
    require((final_q, final_r) == (q, r), "final class")
    require(not augmentation_violation(final_rows, final_q, final_r),
            "terminal augmentation violation")
    return checks, len(steps)


def physical_stream_check(cache, target_replay, target_expected):
    replay = Path(target_replay)
    normal = replay / "normal-physical" / "physical.jsonl"
    optimized = replay / "optimized-physical" / "physical.jsonl"
    normal_raw = normal.read_bytes()
    optimized_raw = optimized.read_bytes()
    require(normal_raw == optimized_raw, "normal/optimized physical stream mismatch")
    expected_hash = target_expected["physical"]["certificate_sha256"]
    require(hashlib.sha256(normal_raw).hexdigest() == expected_hash,
            "target physical stream hash")

    normalizations = successful = bad = fixtures = checks = 0
    step_histogram = Counter()
    destinations = set()
    normalization_sample = reduction_sample = None
    for raw_line in normal_raw.splitlines():
        row = json.loads(raw_line)
        source = row["source"]
        certificate = row["certificate"]
        require(has_clique(decode_graph(source), range(43), 0, 5) or
                has_clique(decode_graph(source), range(43), 1, 5),
                "fixture unexpectedly target-valid")
        fixtures += 1
        if row["kind"] == "normalization":
            checks += check_normalization(cache, source, certificate)
            normalizations += 1
            if normalization_sample is None:
                normalization_sample = row
        elif row["kind"] == "reduction":
            edge_checks, steps = check_reduction(cache, source, certificate)
            checks += edge_checks
            if certificate["status"] == "MONOCHROMATIC_FIVE":
                bad += 1
            else:
                successful += 1
                step_histogram[steps] += 1
                destinations.add(certificate["destination_task"])
                if reduction_sample is None and steps:
                    reduction_sample = row
        else:
            raise ValueError("unknown physical row kind")

    expected = target_expected["physical"]
    require(normalizations == expected["normalizations"], "normalization count")
    require(successful == expected["successful_reductions"], "reduction count")
    require(bad == expected["monochromatic_five_outputs"], "bad-five count")
    require(dict(step_histogram) == {int(k): v for k, v in expected["step_histogram"].items()},
            "step histogram")
    require(len(destinations) == expected["distinct_destination_tasks"],
            "destination task count")
    require(checks == expected["edge_identities"], "physical identity count")

    # Independent checker self-controls on two already validated records.
    rejected = 0
    altered = deepcopy(normalization_sample)
    altered["certificate"]["new_to_old"][0] = altered["certificate"]["new_to_old"][1]
    try:
        check_normalization(cache, altered["source"], altered["certificate"])
    except (ValueError, KeyError, TypeError):
        rejected += 1
    else:
        raise ValueError("checker accepted duplicate normalization label")
    for mutation in ("binding", "destination", "composite"):
        altered = deepcopy(reduction_sample)
        certificate = altered["certificate"]
        if mutation == "binding":
            certificate["source_sha256"] = "0" * 64
        elif mutation == "destination":
            certificate["destination_task"] = "bo1-q10-r10-c000003"
        else:
            certificate["new_to_old"][0], certificate["new_to_old"][1] = (
                certificate["new_to_old"][1], certificate["new_to_old"][0])
        try:
            check_reduction(cache, altered["source"], certificate)
        except (ValueError, KeyError, TypeError):
            rejected += 1
        else:
            raise ValueError(f"checker accepted {mutation} corruption")
    require(rejected == 4, "checker corruption controls")
    return {
        "stream_sha256": expected_hash,
        "records": fixtures,
        "normalizations": normalizations,
        "successful_reductions": successful,
        "monochromatic_five_outputs": bad,
        "step_histogram": dict(sorted(step_histogram.items())),
        "distinct_destination_tasks": len(destinations),
        "physical_edge_identities": checks,
        "all_sources_explicitly_non_Ramsey": True,
        "checker_corruptions_rejected": rejected,
    }


def check_target_expected(target_expected):
    raw = (TARGET / "EXPECTED.json").read_bytes()
    require(hashlib.sha256(raw).hexdigest() ==
            "f37cd7fd458ed76de16a07219a5d0e7017921b75fe6cff92a69c8e99b70eb0d2",
            "target EXPECTED identity")
    require(json.loads(raw) == target_expected, "target EXPECTED parse")


def run(cache, target_replay):
    start = time.monotonic()
    target_expected = json.loads((TARGET / "EXPECTED.json").read_text())
    check_target_expected(target_expected)

    owners3, lookup3 = orbit_owners(cache, 3)
    owners7, lookup7 = orbit_owners(cache, 7)
    expected_lookup = {row["n"]: row for row in target_expected["lookup"]}
    for row in (lookup3, lookup7):
        expected = expected_lookup[row["n"]]
        for key in ("labelled_inputs", "accepted", "rejected", "catalog_records", "owners_sha256"):
            require(row[key] == expected[key], f"lookup mismatch n={row['n']} {key}")
        require(row["orbit_sizes_sha256"] == digest_list(expected["orbit_sizes"]),
                f"orbit sizes n={row['n']}")

    q8 = deletion_census(cache, 11, owners7)
    q9 = deletion_census(cache, 7, owners3)
    for actual, expected in zip((q8, q9), target_expected["census"]["core_interfaces"]):
        for key in ("source_order", "destination_order", "source_cores", "deletions",
                    "distinct_destination_records", "destinations_per_source_histogram",
                    "distinct_selected_matchings", "matching_histogram_sha256"):
            require(actual[key] == expected[key], f"deletion census {actual['source_order']} {key}")
        require(actual["destination_histogram"] == expected["destination_histogram"],
                f"destination histogram {actual['source_order']}")

    counts = {7: 640, 8: 546356, 9: 362, 10: 4}
    registry = [{
        "q": q,
        "r": r,
        "tasks": counts[q],
        "added_clauses_per_task": 36 * r if q == 8 else 6 * r if q == 9 else 0,
    } for q in range(7, 11) for r in range(5, q + 1)]
    require(registry == target_expected["census"]["registry"], "complete registry")
    affected = sum(row["tasks"] for row in registry if row["added_clauses_per_task"])
    added = sum(row["tasks"] * row["added_clauses_per_task"] for row in registry)
    require(affected == target_expected["census"]["affected_tasks"], "affected task count")
    require(sum(row["tasks"] for row in registry) == target_expected["census"]["total_tasks"],
            "whole task count")
    require(added == target_expected["census"]["total_added_clauses_over_registry"],
            "virtual clause total")
    patterns = q8["distinct_selected_matchings"] + q9["distinct_selected_matchings"]
    suffix_clauses = (q8["distinct_selected_matchings"] * 36 * sum(range(5, 9)) +
                      q9["distinct_selected_matchings"] * 6 * sum(range(5, 10)))
    require(patterns == target_expected["formulas"]["matching_patterns"], "matching pattern total")
    require(suffix_clauses == target_expected["formulas"]["clauses_checked"],
            "suffix clause audit count")
    require(8 * suffix_clauses == target_expected["formulas"]["literals_checked"],
            "suffix literal audit count")

    black_box = black_box_suffixes(cache, target_expected)
    require(black_box["task_count"] == 9 and black_box["clauses"] == 1146,
            "black-box suffix coverage")
    physical = physical_stream_check(cache, target_replay, target_expected)
    return {
        "status": "INDEPENDENT_H4045_ACCEPT",
        "target_expected_sha256": hashlib.sha256((TARGET / "EXPECTED.json").read_bytes()).hexdigest(),
        "catalogue_orbits": [lookup3, lookup7],
        "q8_deletions": {
            "source_cores": q8["source_cores"],
            "deletions": q8["deletions"],
            "distinct_destinations": q8["distinct_destination_records"],
            "absent_destinations": [i for i, count in enumerate(q8["destination_histogram"]) if not count],
            "destination_histogram_sha256": digest_list(q8["destination_histogram"]),
            "destinations_per_source_histogram": q8["destinations_per_source_histogram"],
            "distinct_selected_matchings": q8["distinct_selected_matchings"],
            "matching_histogram_sha256": q8["matching_histogram_sha256"],
        },
        "q9_deletions": {
            "source_cores": q9["source_cores"],
            "deletions": q9["deletions"],
            "distinct_destinations": q9["distinct_destination_records"],
            "destination_histogram_sha256": digest_list(q9["destination_histogram"]),
            "destinations_per_source_histogram": q9["destinations_per_source_histogram"],
            "distinct_selected_matchings": q9["distinct_selected_matchings"],
            "matching_histogram_sha256": q9["matching_histogram_sha256"],
        },
        "registry": {
            "tasks": sum(row["tasks"] for row in registry),
            "affected_tasks": affected,
            "virtual_added_clauses": added,
            "matching_patterns": patterns,
            "suffix_clauses_checked_by_count": suffix_clauses,
            "suffix_literals_checked_by_count": 8 * suffix_clauses,
        },
        "black_box_suffixes": black_box,
        "physical_certificates": physical,
        "seconds": time.monotonic() - start,
    }


def stable(receipt):
    result = deepcopy(receipt)
    result.pop("seconds", None)
    # JSON receipts stringify dictionary keys (notably the step histogram).
    # Round-trip here so the in-memory and persisted schemas are identical.
    return json.loads(json.dumps(result, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True)
    parser.add_argument("--target-replay", required=True)
    parser.add_argument("--receipt")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    receipt = run(args.cache, args.target_replay)
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        require(stable(receipt) == expected, "review expectation mismatch")
        for path in (("registry", "virtual_added_clauses"),
                     ("q8_deletions", "deletions"),
                     ("physical_certificates", "physical_edge_identities")):
            altered = deepcopy(expected)
            altered[path[0]][path[1]] += 1
            require(stable(receipt) != altered, "altered review expectation accepted")
    if args.receipt:
        Path(args.receipt).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": receipt["status"],
        "seconds": receipt["seconds"],
        "q8_deletions": receipt["q8_deletions"]["deletions"],
        "physical_edge_identities": receipt["physical_certificates"]["physical_edge_identities"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()

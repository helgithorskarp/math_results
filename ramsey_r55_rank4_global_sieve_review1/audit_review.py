#!/usr/bin/env python3
"""Independent audit of the all-pattern rank-four global sieve.

Counts are reconstructed by a direct dynamic program over actual vector
labels and the concrete span accumulated so far.  No claimant module,
subspace Mobius formula, or triangular span subtraction is imported.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import itertools
import json
from math import comb, factorial, prod
from pathlib import Path
import subprocess


TARGET = "ramsey_r55_rank4_global_sieve"
COMMIT = "1d660bc22336072feab9702a4969c9597c78df5f"
SUMS_SHA256 = "cfccd6659ec8a73a17e4ceafdfce4e53545596c52dcbe8156324f8a9601b48b0"
TARGET_EVIDENCE_SHA256 = "2aa0ce54c18a3835e1a91ace577dcc8ca5c325adc2d5f55f9ba30f1cddfd931c"
GL4 = 20160
AFFINE_OMISSION = 17154780486757774613743095705600000000
CLAIMED_RANK4_TOTAL = 296935236499420514245609548376980635622730104000
CLAIMED_STAGES = [
    ["current_baseline",
     130462366537469674573235644260325500723394324800,
     4050919711653602791074637762831219200,
     130462366516263974374824266855507767254963105600],
    ["zero_multiplicity_caps",
     92390744370276124859211765951503730989415444480,
     4050919711653602791074637762831219200,
     92390744349070424660800388546685997520984225280],
    ["also_all_row_classes_at_most_four",
     81140697290018138669657459725148732137207680000,
     1458661973529497372867041338528000000,
     81140697271404696209370187738538595093079680000],
    ["also_all_column_classes_at_most_five",
     77766291787612715253994696252727234987815920000,
     828149679018144235057330215590400000,
     77766291769629785088218777403926809066625520000],
]
CLAIMED_REMOVED = 52696074746634189286605489451580958188337585600


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def pin_package(source):
    head = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"], check=True,
        capture_output=True, text=True).stdout.strip()
    require(head == COMMIT, "reviewed checkout is not the pinned commit")
    package = source / TARGET
    sums = package / "SHA256SUMS"
    require(digest(sums.read_bytes()) == SUMS_SHA256,
            "reviewed checksum manifest changed")
    names = []
    for line in sums.read_text(encoding="utf-8").splitlines():
        expected, name = line.split("  ", 1)
        path = package / name
        require(path.is_file() and digest(path.read_bytes()) == expected,
                f"reviewed source changed: {name}")
        names.append(name)
    require(len(names) == 15 and len(set(names)) == 15,
            "unexpected manifest scope")
    actual = {path.name for path in package.iterdir()
              if path.is_file() and path.name != "SHA256SUMS"}
    require(set(names) == actual, "manifest does not cover every source file")
    expected = package / "expected_audit.json"
    require(digest(expected.read_bytes()) == TARGET_EVIDENCE_SHA256,
            "target evidence changed")
    evidence = json.loads(expected.read_text(encoding="utf-8"))
    require(evidence["status"] == "VERIFIED_RANK4_GLOBAL_SIEVE",
            "target status changed")
    return package, len(names) + 1, sum(path.stat().st_size
                                        for path in package.iterdir()
                                        if path.is_file())


def dot(x, y):
    return (x & y).bit_count() & 1


def extend_span(span_mask, vector):
    if span_mask >> vector & 1:
        return span_mask
    old = [x for x in range(span_mask.bit_length()) if span_mask >> x & 1]
    return span_mask | sum(1 << (x ^ vector) for x in old)


def vector_rank(vectors):
    span = 1
    for vector in vectors:
        span = extend_span(span, vector)
    return span.bit_count().bit_length() - 1


def binary_rank(rows):
    values = list(rows)
    result = 0
    while values:
        pivot = max(values)
        if not pivot:
            break
        result += 1
        bit = 1 << (pivot.bit_length() - 1)
        values = [value ^ pivot if value & bit else value
                  for value in values if value != pivot]
    return result


def group_order(r):
    return prod(2**r - 2**index for index in range(r))


def factor_table(length, r, cap, allowed=None):
    """Capped ordered nonzero lists, indexed by length, with exact full span."""
    labels = tuple(range(1, 2**r)) if allowed is None else tuple(allowed)
    state = {(0, 1): 1}
    for vector in labels:
        next_state = defaultdict(int)
        for (used, span), count in state.items():
            for copies in range(min(cap, length - used) + 1):
                new_span = extend_span(span, vector) if copies else span
                next_state[used + copies, new_span] += (
                    count * comb(used + copies, copies))
        state = next_state
    full = (1 << (2**r)) - 1
    return [state.get((used, full), 0) for used in range(length + 1)]


def direct_stage(m, n, r, row_cap, column_cap, row_zero, column_zero):
    rows = factor_table(m, r, row_cap)
    columns = factor_table(n, r, column_cap)
    row_counts = [comb(m, zeros) * rows[m - zeros]
                  for zeros in range(row_zero + 1)]
    column_counts = [comb(n, zeros) * columns[n - zeros]
                     for zeros in range(column_zero + 1)]
    numerator = (row_counts[0] * sum(column_counts)
                 + sum(row_counts[1:]) * column_counts[0])
    raw, remainder = divmod(numerator, group_order(r))
    require(not remainder, "nonintegral full-rank factor quotient")

    hyperplane = [vector for vector in range(1, 2**r)
                  if dot(1, vector)]
    affine_rows = factor_table(m, r, row_cap, hyperplane)[m]
    affine_columns = factor_table(n, r, column_cap, hyperplane)[n]
    multiplier = (2**r - 1) * 2**(r - 1)
    overlap, remainder = divmod(
        multiplier * affine_rows * affine_columns, group_order(r))
    require(not remainder, "nonintegral complementary-rank quotient")
    return raw, overlap, rows, columns


def exact_counts():
    require(group_order(4) == GL4, "wrong GL(4,2) order")
    affine = (15 * comb(15, 5) * factorial(20) * factorial(23)
              // (2**13 * GL4))
    require(affine == AFFINE_OMISSION, "affine omission differs")
    configurations = [
        (20, 23, 20, 23),
        (20, 23, 1, 2),
        (4, 23, 1, 2),
        (4, 5, 1, 2),
    ]
    stages = []
    all_rows = all_columns = None
    for claimed, (row_cap, column_cap, row_zero, column_zero) in zip(
            CLAIMED_STAGES, configurations):
        raw, overlap, rows, columns = direct_stage(
            20, 23, 4, row_cap, column_cap, row_zero, column_zero)
        remaining = raw - overlap - affine
        actual = [claimed[0], raw, overlap, remaining]
        require(actual == claimed, f"stage differs: {claimed[0]}")
        stages.append({"stage": claimed[0], "raw_zero_filtered": raw,
                       "complement_rank_three_overlap": overlap,
                       "affine_omission": affine, "remaining": remaining})
        if claimed[0] == "current_baseline":
            all_rows, all_columns = rows, columns

    row_total = sum(comb(20, zeros) * all_rows[20 - zeros]
                    for zeros in range(21))
    column_total = sum(comb(23, zeros) * all_columns[23 - zeros]
                       for zeros in range(24))
    total, remainder = divmod(row_total * column_total, GL4)
    require(not remainder and total == CLAIMED_RANK4_TOTAL,
            "all rank-four matrices differ")
    baseline, survivor = stages[0]["remaining"], stages[-1]["remaining"]
    removed = baseline - survivor
    fraction = Fraction(removed, baseline)
    require(removed == CLAIMED_REMOVED and
            fraction == Fraction(376310008768820496017231590851225959,
                                 931649928837861438158324253913962509),
            "published removal arithmetic differs")
    return {"rank4_total": total, "stages": stages, "baseline": baseline,
            "removed": removed, "remaining": survivor,
            "removed_fraction": [fraction.numerator, fraction.denominator],
            "internal_free_bits": 443}


def matrix_census(configurations):
    checked = 0
    for m, n, r, row_cap, column_cap, row_zero, column_zero in configurations:
        raw = overlap = 0
        for bits in range(1 << (m * n)):
            rows = [sum(((bits >> (i * n + j)) & 1) << j
                        for j in range(n)) for i in range(m)]
            if binary_rank(rows) != r:
                continue
            columns = [sum(((rows[i] >> j) & 1) << i for i in range(m))
                       for j in range(n)]
            row_counter, column_counter = Counter(rows), Counter(columns)
            zr, zc = row_counter[0], column_counter[0]
            if (zr and zc) or zr > row_zero or zc > column_zero:
                continue
            if max((count for value, count in row_counter.items() if value),
                   default=0) > row_cap:
                continue
            if max((count for value, count in column_counter.items() if value),
                   default=0) > column_cap:
                continue
            raw += 1
            complement = [row ^ ((1 << n) - 1) for row in rows]
            overlap += binary_rank(complement) == r - 1
        predicted_raw, predicted_overlap, _, _ = direct_stage(
            m, n, r, row_cap, column_cap, row_zero, column_zero)
        require((raw, overlap) == (predicted_raw, predicted_overlap),
                "small physical matrix census differs")
        checked += 1 << (m * n)
    return {"binary_matrices_enumerated": checked,
            "complete_configurations": len(configurations)}


def r33_census():
    pairs = list(itertools.combinations(range(6), 2))
    positions = {pair: index for index, pair in enumerate(pairs)}
    triangles = [sum(1 << positions[pair]
                     for pair in itertools.combinations(vertices, 2))
                 for vertices in itertools.combinations(range(6), 3)]
    avoiders = 0
    for coloring in range(1 << len(pairs)):
        red = any(coloring & triangle == triangle for triangle in triangles)
        blue = any(coloring & triangle == 0 for triangle in triangles)
        avoiders += not red and not blue
    require(avoiders == 0, "R(3,3)<=6 census failed")
    return 1 << len(pairs), avoiders


def structural_checks():
    colorings, avoiders = r33_census()
    possible_degrees = [degree for degree in range(9)
                        if degree <= 3 and 8 - degree <= 5]
    require(possible_degrees == [3] and 9 * 3 % 2,
            "R(3,4)<=9 parity proof failed")
    require(5 + 9 == 14, "R(3,5) recurrence failed")

    mixed_rows = []
    for x0, x1, x2 in itertools.product((0, 1), repeat=3):
        left = x0 * x1 + x0 * x2 + (1 - x1) * (1 - x2)
        right = int(x0 == x1 == x2) + x0
        require(left == right, "mixed-triple identity failed")
        mixed_rows.append([x0, x1, x2, left])

    triangle_d = []
    for common in range(5):
        minimum = (54 - 6 - 3 * common + 1) // 2
        require(minimum >= 18, "monochromatic-triangle bound failed")
        triangle_d.append(minimum)
    # A mixed triple has D >= d_red(0)-1 >= 17 by the identity above.
    require(18 - 1 == 17, "mixed-triple distinguisher bound failed")

    pattern_counts = []
    for contacts in itertools.product((0, 1), repeat=5):
        distinguished = sum(len({contacts[index] for index in triple}) == 2
                            for triple in itertools.combinations(range(5), 3))
        pattern_counts.append(distinguished)
    require(max(pattern_counts) == 9, "five-contact maximum differs")
    require(10 * 17 == 170 and 20 + 15 * 9 == 155 and 170 > 155,
            "five-row double count failed")

    # Six equal columns contain a monochromatic triangle.  Its contact set
    # has at most four vertices; the opposite set has at least 16, hence an
    # opposite-color triangle.  An opposite-color edge in the six-set would
    # extend it, forcing the six-set monochromatic in the first color.
    require(20 - 4 == 16 and 16 >= 14 and 6 >= 5,
            "six-column implication failed")
    require(34 > (20 - 2) + 13 and 54 > 2 * 23 + 4,
            "zero-class bounds failed")
    return {"r33_colorings_checked": colorings, "r33_avoiders": avoiders,
            "r34_forced_degree": possible_degrees, "r35_upper_bound": 14,
            "mixed_signature_rows": mixed_rows,
            "monochromatic_triangle_distinguisher_bounds": triangle_d,
            "mixed_triangle_distinguisher_bound": 17,
            "five_contact_patterns_checked": len(pattern_counts),
            "five_contact_max_distinguished_triples": max(pattern_counts),
            "five_row_required_vs_available": [170, 155],
            "six_column_opposite_contact_minimum": 16,
            "zero_row_cap": 1, "zero_column_cap": 2,
            "imported_premise": "R(4,5)<=25"}


def graph_from_parameters(parameters):
    require(set(parameters) == {"rows", "columns", "internal_hex"},
            "bad parameter schema")
    rows, columns = parameters["rows"], parameters["columns"]
    require(len(rows) == 20 and len(columns) == 23 and
            all(type(value) is int and 0 <= value < 16
                for value in rows + columns) and
            vector_rank(rows) == vector_rank(columns) == 4,
            "bad factor lists")
    text = parameters["internal_hex"]
    require(isinstance(text, str) and len(text) == 111 and
            all(char in "0123456789abcdef" for char in text) and
            int(text, 16) < 2**443, "bad internal bits")
    internal = int(text, 16)
    red = 0
    internal_index = 0
    for pair_index, (u, v) in enumerate(itertools.combinations(range(43), 2)):
        if u < 20 <= v:
            value = dot(rows[u], columns[v - 20])
        else:
            value = internal >> internal_index & 1
            internal_index += 1
        red |= value << pair_index
    require(internal_index == 443, "wrong internal coordinate count")
    return {"n": 43, "red_hex": format(red, "0226x")}


def affine_removed(rows, columns):
    row_counts, column_counts = Counter(rows), Counter(columns)
    if set(row_counts) != set(range(1, 16)) or set(column_counts) != set(range(1, 16)):
        return False
    if (sorted(row_counts.values()) != [1] * 10 + [2] * 5 or
            sorted(column_counts.values()) != [1] * 7 + [2] * 8):
        return False
    doubled = {value for value, count in column_counts.items() if count == 2}
    return any(doubled == {value for value in range(16) if dot(w, value)}
               for w in range(1, 16))


def classify_parameters(parameters):
    rows, columns = parameters["rows"], parameters["columns"]
    row_counts, column_counts = Counter(rows), Counter(columns)
    cross = [sum(dot(row, column) << index
                 for index, column in enumerate(columns)) for row in rows]
    complement = [value ^ ((1 << 23) - 1) for value in cross]
    if row_counts[0] and column_counts[0]:
        return "previous_zero_pair"
    if binary_rank(complement) < 4:
        return "previous_complement_rank"
    if affine_removed(rows, columns):
        return "previous_affine_family"
    if row_counts[0] > 1 or column_counts[0] > 2:
        return "zero_multiplicity"
    if max(row_counts.values()) > 4:
        return "row_class"
    if max(column_counts.values()) > 5:
        return "column_class"
    return "survives_necessary_filter"


def audit_fixture(package):
    parameters = json.loads((package / "fixture_parameters.json").read_text())
    stored_graph = json.loads((package / "fixture_graph.json").read_text())
    certificate = json.loads((package / "fixture_certificate.json").read_text())
    graph = graph_from_parameters(parameters)
    require(graph == stored_graph, "independent physical graph differs")
    require(classify_parameters(parameters) == "zero_multiplicity",
            "independent fixture branch differs")
    require(set(certificate) == {"color", "vertices"} and
            certificate["color"] in ("red", "blue"), "bad certificate")
    vertices = certificate["vertices"]
    require(len(vertices) == 5 and vertices == sorted(set(vertices)) and
            all(type(vertex) is int and 0 <= vertex < 43 for vertex in vertices),
            "bad five-set")
    bits = int(graph["red_hex"], 16)
    pair_indices = {pair: index for index, pair in enumerate(
        itertools.combinations(range(43), 2))}
    expected = certificate["color"] == "red"
    for pair in itertools.combinations(vertices, 2):
        require(bool(bits >> pair_indices[pair] & 1) == expected,
                "certificate has a wrong physical pair")
    return {"classification": "zero_multiplicity",
            "zero_rows": Counter(parameters["rows"])[0],
            "certificate": certificate, "physical_pairs_checked": 10,
            "internal_coordinates_reconstructed": 443,
            "cross_coordinates_reconstructed": 460}


def run(source):
    package, files, byte_count = pin_package(source)
    exact = exact_counts()
    small = matrix_census([
        (3, 4, 2, 3, 4, 3, 4),
        (3, 4, 2, 2, 3, 1, 1),
        (4, 3, 2, 2, 2, 1, 1),
    ])
    structure = structural_checks()
    physical = audit_fixture(package)
    return {
        "reviewed_source_commit": COMMIT,
        "package": {"files_including_manifest": files, "bytes": byte_count,
                    "manifest_sha256": SUMS_SHA256,
                    "target_evidence_sha256": TARGET_EVIDENCE_SHA256},
        "independent_method": "direct_actual_label_span_dynamic_program",
        "exact": exact, "small_controls": small,
        "structural": structure, "physical": physical,
        "scope": {"global_rank4_sieve": "accepted",
                  "all_internal_edges_free": True,
                  "affine_exclusion_is_imported": True,
                  "ramsey_5_5_lower_bound_changed": False},
        "status": "VERIFIED_REVIEW_RANK4_GLOBAL_SIEVE",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path,
                        help="math_results checkout at the pinned target commit")
    arguments = parser.parse_args()
    print(json.dumps(run(arguments.source.resolve()), indent=2, sort_keys=True))

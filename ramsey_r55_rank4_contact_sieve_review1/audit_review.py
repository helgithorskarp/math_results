#!/usr/bin/env python3
"""Independent audit of the global rank-four contact sieve.

The core counts use a direct dynamic program over actual vector labels and the
span built so far.  This imports no claimant module and uses neither subspace
Mobius inversion nor actual-subspace subtraction.
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


TARGET = "ramsey_r55_rank4_contact_sieve"
COMMIT = "f47adb4544ee5d94f008c77740ba87938788e320"
SUMS_SHA256 = "c3fe87fac1eb5ef010bc4f25756aa6f91f3ba8020df49791a20fd30eea4a3482"
TARGET_EVIDENCE_SHA256 = "9bfd58873ef6811410c4488f86c4346fcec5ca13f4a5211664d9ceb53e383182"
GL4 = 20160
AFFINE_OMISSION = 17154780486757774613743095705600000000
CLAIMED_A = {
    1: [42020554074439580640000, 51309706203219784320000],
    2: [4735692146711766240000, 5001904543041806400000],
}
CLAIMED_B = {
    1: [447395575597132344934175424, 641090420239944866589478080,
        463592890925341052836536576],
    2: [184866039010490656652817984, 246475931674506495282345024,
        174192316192824727453463808],
}
CLAIMED_FIRST = 65606361852310603228542207086337682833491520000
CLAIMED_SECOND = 19751595038087124073509685089835183465384320000
CLAIMED_Q = 828149679018144235057330215590400000
CLAIMED_BASELINE = 77766291769629785088218777403926809066625520000
CLAIMED_REMOVAL = 45854766813395329476014377761445169152516800000
CLAIMED_REMAINING = 31911524956234455612204399642481639914108720000


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
                f"reviewed file changed: {name}")
        names.append(name)
    require(len(names) == 19 and len(set(names)) == 19,
            "unexpected package checksum scope")
    actual = {path.name for path in package.iterdir()
              if path.is_file() and path.name != "SHA256SUMS"}
    require(set(names) == actual, "checksum manifest does not cover package")
    expected = package / "expected_audit.json"
    require(digest(expected.read_bytes()) == TARGET_EVIDENCE_SHA256,
            "target evidence changed")
    target = json.loads(expected.read_text(encoding="utf-8"))
    require(target["status"] == "VERIFIED_RANK4_CONTACT_SIEVE",
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


def rank(vectors, r=4):
    span = 1
    for vector in vectors:
        span = extend_span(span, vector)
    return (span.bit_count()).bit_length() - 1


def factor_table(length, r, cap, allowed=None):
    """Counts capped ordered nonzero lists by length and exact span."""
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


def row_event_table(length, r, cap, threshold, marked):
    """Directly track marked populations and the span of admitted labels."""
    marked_labels = tuple(1 << index for index in range(marked))
    state = {(0, 1, (0,) * marked): 1}
    for vector in range(1, 2**r):
        next_state = defaultdict(int)
        position = (marked_labels.index(vector)
                    if vector in marked_labels else None)
        for (used, span, populations), count in state.items():
            for copies in range(min(cap, length - used) + 1):
                new_populations = list(populations)
                if position is not None:
                    new_populations[position] += copies
                new_span = extend_span(span, vector) if copies else span
                next_state[(used + copies, new_span,
                            tuple(new_populations))] += (
                    count * comb(used + copies, copies))
        state = next_state
    full = (1 << (2**r)) - 1
    output = []
    for zeros in range(2):
        nonzeros = length - zeros
        count = sum(value for (used, span, populations), value in state.items()
                    if used == nonzeros and span == full and
                    all(threshold <= population <= cap
                        for population in populations))
        output.append(comb(length, zeros) * count)
    return output


def column_event_table(length, r, cap, marked, bad):
    """Track contact counts and exact span while inserting actual labels."""
    marked_labels = tuple(1 << index for index in range(marked))
    state = {(0, 1, (0,) * marked): 1}
    for vector in range(1, 2**r):
        signature = tuple(dot(x, vector) for x in marked_labels)
        next_state = defaultdict(int)
        for (used, span, contacts), count in state.items():
            for copies in range(min(cap, length - used) + 1):
                new_contacts = tuple(contact + copies * bit
                                     for contact, bit in zip(contacts, signature))
                new_span = extend_span(span, vector) if copies else span
                next_state[(used + copies, new_span, new_contacts)] += (
                    count * comb(used + copies, copies))
        state = next_state
    full = (1 << (2**r)) - 1
    output = []
    for zeros in range(3):
        nonzeros = length - zeros
        count = sum(value for (used, span, contacts), value in state.items()
                    if used == nonzeros and span == full and
                    all(contact in bad for contact in contacts))
        output.append(comb(length, zeros) * count)
    return output


def brute_list_events(length, r, cap, threshold, marked, bad):
    row = [0, 0]
    column = [0, 0]
    marked_labels = tuple(1 << index for index in range(marked))
    for word in itertools.product(range(2**r), repeat=length):
        counts = Counter(word)
        zeros = counts[0]
        if zeros > 1 or max((count for label, count in counts.items()
                             if label), default=0) > cap or rank(word, r) != r:
            continue
        if all(threshold <= counts[label] <= cap for label in marked_labels):
            row[zeros] += 1
        contacts = [sum(dot(label, vector) for vector in word)
                    for label in marked_labels]
        if all(contact in bad for contact in contacts):
            column[zeros] += 1
    return row, column


def small_controls():
    comparisons = 0
    bad = frozenset((0, 1, 4, 5))
    for marked in (1, 2):
        brute_row, brute_column = brute_list_events(
            5, 2, 3, 2, marked, bad)
        direct_row = row_event_table(5, 2, 3, 2, marked)
        direct_column = column_event_table(5, 2, 3, marked, bad)[:2]
        require(brute_row == direct_row, "small direct row DP failed")
        require(brute_column == direct_column, "small direct column DP failed")
        comparisons += 4
    return {"labeled_words_enumerated": 2 * 4**5,
            "event_count_comparisons": comparisons}


def exact_counts():
    require(prod(2**4 - 2**index for index in range(4)) == GL4,
            "wrong GL(4,2) order")
    bad = frozenset(range(10)) | frozenset(range(14, 24))
    rows = {marked: row_event_table(20, 4, 4, 3, marked)
            for marked in (1, 2)}
    columns = {marked: column_event_table(23, 4, 5, marked, bad)
               for marked in (1, 2)}
    require(rows == CLAIMED_A, "direct row event counts differ")
    require(columns == CLAIMED_B, "direct column event counts differ")

    flags = {marked: (rows[marked][0] * sum(columns[marked])
                      + rows[marked][1] * columns[marked][0])
             for marked in (1, 2)}
    first, remainder1 = divmod(15 * flags[1], GL4)
    second, remainder2 = divmod(comb(15, 2) * flags[2], GL4)
    require(not remainder1 and not remainder2, "nonintegral factor quotient")
    require(first == CLAIMED_FIRST and second == CLAIMED_SECOND,
            "direct moment counts differ")

    row_factors = factor_table(20, 4, 4)
    column_factors = factor_table(23, 4, 5)
    u = [comb(20, zeros) * row_factors[20 - zeros]
         for zeros in range(2)]
    v = [comb(23, zeros) * column_factors[23 - zeros]
         for zeros in range(3)]
    raw_numerator = u[0] * sum(v) + u[1] * v[0]
    raw, raw_remainder = divmod(raw_numerator, GL4)
    require(not raw_remainder, "nonintegral direct baseline quotient")

    hyperplane = [vector for vector in range(1, 16) if dot(1, vector)]
    require(len(hyperplane) == 8, "wrong affine hyperplane")
    affine_u = factor_table(20, 4, 4, hyperplane)[20]
    affine_v = factor_table(23, 4, 5, hyperplane)[23]
    overlap, overlap_remainder = divmod(120 * affine_u * affine_v, GL4)
    require(not overlap_remainder and overlap == CLAIMED_Q,
            "direct complementary-rank overlap differs")
    affine_omission = (15 * comb(15, 5) * factorial(20) * factorial(23)
                       // (2**13 * GL4))
    require(affine_omission == AFFINE_OMISSION,
            "affine-duplication omission count differs")
    baseline = raw - overlap - affine_omission
    require(baseline == CLAIMED_BASELINE, "direct retained baseline differs")

    removal = first - second - overlap
    remaining = baseline - removal
    fraction = Fraction(removal, baseline)
    require(removal == CLAIMED_REMOVAL and remaining == CLAIMED_REMAINING,
            "union-bound arithmetic differs")
    require(fraction == Fraction(2340145696609374678214780,
                                 3968713956534742273879267),
            "published fraction differs")
    require(all(k - comb(k, 2) <= int(k > 0) for k in range(7)),
            "Bonferroni pointwise bound failed")
    return {
        "row_events": {str(key): value for key, value in rows.items()},
        "column_events": {str(key): value for key, value in columns.items()},
        "first_moment": first,
        "second_binomial_moment": second,
        "raw_capped_zero_filtered": raw,
        "complement_rank_three_overlap": overlap,
        "affine_omission": affine_omission,
        "baseline": baseline,
        "removed_lower_bound": removal,
        "remaining_upper_bound": remaining,
        "removed_fraction": [fraction.numerator, fraction.denominator],
        "bonferroni_k_checked": list(range(7)),
    }


def graph_from_parameters(parameters):
    require(set(parameters) == {"rows", "columns", "internal_hex"},
            "bad parameter schema")
    rows, columns = parameters["rows"], parameters["columns"]
    require(len(rows) == 20 and len(columns) == 23 and
            all(type(value) is int and 0 <= value < 16
                for value in rows + columns) and
            rank(rows) == rank(columns) == 4, "bad factor lists")
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
    require(internal_index == 443, "wrong internal-coordinate count")
    return {"n": 43, "red_hex": format(red, "0226x")}


def audit_fixture(package):
    parameters = json.loads((package / "fixture_parameters.json").read_text())
    stored_graph = json.loads((package / "fixture_graph.json").read_text())
    stored_certificate = json.loads(
        (package / "fixture_certificate.json").read_text())
    graph = graph_from_parameters(parameters)
    require(graph == stored_graph, "independent physical graph differs")

    row_counts = Counter(parameters["rows"])
    violations = []
    for label, population in sorted(row_counts.items()):
        contacts = sum(dot(label, vector) for vector in parameters["columns"])
        if population >= 3 and not 10 <= contacts <= 13:
            violations.append([label, population, contacts])
    require(violations == [[1, 3, 9]], "fixture violation changed")

    require(set(stored_certificate) == {"color", "vertices"} and
            stored_certificate["color"] in ("red", "blue"),
            "bad certificate schema")
    vertices = stored_certificate["vertices"]
    require(len(vertices) == 5 and vertices == sorted(set(vertices)) and
            all(type(vertex) is int and 0 <= vertex < 43 for vertex in vertices),
            "bad physical five-set")
    bits = int(graph["red_hex"], 16)
    pair_index = {pair: index for index, pair in enumerate(
        itertools.combinations(range(43), 2))}
    expected = stored_certificate["color"] == "red"
    for pair in itertools.combinations(vertices, 2):
        require(bool(bits >> pair_index[pair] & 1) == expected,
                "certificate has a wrong physical edge")
    return {"violation_rows_type_population_contacts": violations,
            "certificate": stored_certificate, "physical_pairs_checked": 10,
            "internal_coordinates_reconstructed": 443,
            "cross_coordinates_reconstructed": 460}


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
    # The standard recurrence gives R(3,5)<=R(2,5)+R(3,4)<=5+9=14.
    require(5 + 9 == 14, "R(3,5) recurrence arithmetic failed")
    # Imported R(4,5)<=25 gives both color degrees at least 18.  The local
    # proof then only uses a<=4 for a monochromatic triangle.
    distinguisher_lower_bounds = []
    for common in range(5):
        minimum = (54 - 6 - 3 * common + 1) // 2
        require(minimum >= 18, "triangle distinguisher bound weakened")
        distinguisher_lower_bounds.append(minimum)
    require(20 - 3 == 17 and 17 < min(distinguisher_lower_bounds),
            "tripled type could be monochromatic")
    contact_rows = []
    for red_contacts in range(24):
        keep = red_contacts <= 13 and 23 - red_contacts <= 13
        require(keep == (10 <= red_contacts <= 13),
                "contact interval implication failed")
        if keep:
            contact_rows.append(red_contacts)
    return {"triangle_common_neighbor_cases": list(range(5)),
            "distinguisher_lower_bounds": distinguisher_lower_bounds,
            "available_same_side_distinguishers": 17,
            "permitted_contact_counts": contact_rows,
            "r33_colorings_checked": colorings,
            "r33_avoiders": avoiders,
            "r34_forced_degree": possible_degrees,
            "r35_upper_bound": 14,
            "imported_premise": "R(4,5)<=25"}


def run(source):
    package, files, byte_count = pin_package(source)
    small = small_controls()
    exact = exact_counts()
    physical = audit_fixture(package)
    structure = structural_checks()
    return {
        "reviewed_source_commit": COMMIT,
        "package": {"files_including_manifest": files, "bytes": byte_count,
                    "manifest_sha256": SUMS_SHA256,
                    "target_evidence_sha256": TARGET_EVIDENCE_SHA256},
        "independent_method": "direct_actual_label_span_dynamic_program",
        "small_controls": small,
        "structural": structure,
        "exact": exact,
        "physical": physical,
        "scope": {"new_contact_sieve": "accepted",
                  "removal_is_lower_bound_not_exact_union": True,
                  "baseline_h3765_is_imported_and_directly_recounted": True,
                  "ramsey_5_5_lower_bound_changed": False},
        "status": "VERIFIED_REVIEW_RANK4_CONTACT_SIEVE",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path,
                        help="math_results checkout at the pinned target commit")
    args = parser.parse_args()
    print(json.dumps(run(args.source.resolve()), indent=2, sort_keys=True))

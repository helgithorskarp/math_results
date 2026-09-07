#!/usr/bin/env python3
"""Independent exact audit of the unconditional 60-branch good43 cover.

No module from the target package is imported.  Pair domains are reconstructed
with literal complete-graph edge masks, root representatives with explicit
child permutations, and every clause of six freshly generated CNFs is checked
against a separate physical-edge reconstruction.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
from math import comb, prod
from pathlib import Path
import argparse
import json
import subprocess
import sys
import tempfile


ATOMS = {
    "R4": (4, 0b111111),
    "B4": (4, 0),
    "R3": (3, 0b111),
    "B3": (3, 0),
    "E3": (3, 0b001),
    "P3": (3, 0b011),
}
LAST = ("B3", "E3", "P3", "R3")
FULL_BRANCHES = ((5, 0, 0), (5, 4, 3), (6, 2, 1),
                 (6, 2, 2), (7, 0, 1), (7, 4, 2))
EXPECTED_AUDIT_SHA256 = "04294d5a0a82634da8938e9c2b4e933dd8a7a29cd941750561a070ed619b0029"
EXPECTED_DOMAIN_SHA256 = "5c36ea521e0e1470e0417671eea7d9f14fa85b625f4a052a448e76ee547bc68d"
EXPECTED_ROOT_SHA256 = "2562a431f9ed3df1659d8821d38e59665209781ac6ac6f491a9f81b14e41dbb3"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def json_bytes(value, sort_keys=False):
    return (json.dumps(value, indent=2, sort_keys=sort_keys) + "\n").encode()


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(1024 * 1024)
            if not block:
                return digest.hexdigest()
            digest.update(block)


def local_edge_index(size):
    return {edge: index for index, edge in enumerate(combinations(range(size), 2))}


def atom_edge(kind, first, second):
    if first > second:
        first, second = second, first
    size, mask = ATOMS[kind]
    require(0 <= first < second < size, ("atom edge", kind, first, second))
    return mask >> local_edge_index(size)[first, second] & 1


def pair_domain(left, right):
    """Enumerate a two-atom domain by literal K5 masks in K_(a+b)."""
    a = ATOMS[left][0]
    b = ATOMS[right][0]
    order = a + b
    positions = {edge: index for index, edge in enumerate(combinations(range(order), 2))}
    inside = 0
    for first, second in combinations(range(a), 2):
        inside |= atom_edge(left, first, second) << positions[first, second]
    for first, second in combinations(range(b), 2):
        inside |= atom_edge(right, first, second) << positions[a + first, a + second]
    cross_positions = [positions[first, a + second]
                       for first in range(a) for second in range(b)]
    clique_masks = []
    for vertices in combinations(range(order), 5):
        clique_masks.append(sum(1 << positions[edge]
                                for edge in combinations(vertices, 2)))
    expanded = [inside] * (1 << (a * b))
    for state in range(1, len(expanded)):
        low = state & -state
        coordinate = low.bit_length() - 1
        expanded[state] = expanded[state ^ low] | (1 << cross_positions[coordinate])
    allowed = []
    for state, edges in enumerate(expanded):
        if all(edges & clique != clique and edges & clique != 0
               for clique in clique_masks):
            allowed.append(state)
    return tuple(allowed)


def forbidden_pattern_count(left, right):
    a = ATOMS[left][0]
    b = ATOMS[right][0]
    patterns = set()
    for vertices in combinations(range(a + b), 5):
        fixed = []
        cross = 0
        for first, second in combinations(vertices, 2):
            if second < a:
                fixed.append(atom_edge(left, first, second))
            elif first >= a:
                fixed.append(atom_edge(right, first - a, second - a))
            else:
                cross |= 1 << (first * b + second - a)
        for color in (0, 1):
            if all(value == color for value in fixed):
                patterns.add((cross, cross if color else 0))
    return len(patterns)


def bitmap_record(left, right, allowed):
    bits = ATOMS[left][0] * ATOMS[right][0]
    bitmap = sum(1 << state for state in allowed)
    encoded = format(bitmap, f"0{(1 << bits) // 4}x")
    return {
        "left": left,
        "right": right,
        "matrix_bits": bits,
        "count": len(allowed),
        "forbidden_patterns": forbidden_pattern_count(left, right),
        "allowed_bitmap_hex": encoded,
        "bitmap_sha256": sha256(bytes.fromhex(encoded)).hexdigest(),
    }


def transpose_state(state, rows, columns):
    result = 0
    for row in range(rows):
        for column in range(columns):
            result |= ((state >> (row * columns + column)) & 1) << (column * rows + row)
    return result


def child_automorphisms(kind):
    size = ATOMS[kind][0]
    group = []
    for permutation in permutations(range(size)):
        if all(atom_edge(kind, first, second) ==
               atom_edge(kind, permutation[first], permutation[second])
               for first, second in combinations(range(size), 2)):
            group.append(permutation)
    return tuple(group)


def permute_columns(state, size, permutation):
    result = 0
    for row in range(4):
        for new_column, old_column in enumerate(permutation):
            result |= ((state >> (row * size + old_column)) & 1) << (row * size + new_column)
    return result


def comparisons(kind):
    size = ATOMS[kind][0]
    if kind == "E3":
        return ((0, 1),)
    if kind == "P3":
        return ((1, 2),)
    return tuple((index, index + 1) for index in range(size - 1))


def signature(state, size, column):
    return sum(((state >> (row * size + column)) & 1) << row for row in range(4))


def root_orbits(kind, allowed):
    size = ATOMS[kind][0]
    group = child_automorphisms(kind)
    allowed_set = set(allowed)
    fixed = [0] * len(group)
    canonical = []
    images = 0
    for state in allowed:
        orbit = []
        for index, permutation in enumerate(group):
            moved = permute_columns(state, size, permutation)
            require(moved in allowed_set, ("domain not invariant", kind, state, moved))
            orbit.append(moved)
            fixed[index] += moved == state
            images += 1
        if state == min(orbit):
            canonical.append(state)
    sorted_states = [state for state in allowed if all(
        signature(state, size, first) >= signature(state, size, second)
        for first, second in comparisons(kind))]
    require(canonical == sorted_states, ("signature/orbit mismatch", kind))
    require(sum(fixed) == len(group) * len(canonical), ("Burnside mismatch", kind))
    bitmap = sum(1 << state for state in canonical)
    encoded = format(bitmap, f"0{(1 << (4 * size)) // 4}x")
    return tuple(canonical), {
        "child": kind,
        "count": len(canonical),
        "allowed_bitmap_hex": encoded,
        "bitmap_sha256": sha256(bytes.fromhex(encoded)).hexdigest(),
    }, {
        "child": kind,
        "group_order": len(group),
        "fixed_point_sum": sum(fixed),
        "orbits": len(canonical),
        "group_images": images,
    }


def branch_types(branch):
    r, s, t = branch
    require(r in (5, 6, 7) and s in range(5) and t in range(4), ("branch", branch))
    return ["R4"] * r + ["B4"] * (7 - r) + ["R3"] * s + ["B3"] * (4 - s) + [LAST[t]]


def clique_subset_count(kind, color):
    size = ATOMS[kind][0]
    result = []
    for selected in range(size + 1):
        result.append(sum(all(atom_edge(kind, first, second) == color
                              for first, second in combinations(vertices, 2))
                          for vertices in combinations(range(size), selected)))
    return result


def physical_clause_count(types, color):
    coefficients = [1, 0, 0, 0, 0, 0]
    for kind in types:
        atom = clique_subset_count(kind, color)
        updated = [0] * 6
        for first, left in enumerate(coefficients):
            for second, right in enumerate(atom):
                if first + second <= 5:
                    updated[first + second] += left * right
        coefficients = updated
    return coefficients[5]


def domains_for(types, domain_map, root_map, first, second):
    return root_map[types[second]] if first == 0 else domain_map[types[first], types[second]]


def branch_cardinality(types, domain_map, root_map, rooted):
    return prod(len(root_map[types[second]]) if rooted and first == 0
                else len(domain_map[types[first], types[second]])
                for first, second in combinations(range(12), 2))


def count_audit(published, domain_map, root_map):
    rows = []
    for r in (5, 6, 7):
        for s in range(5):
            for t in range(4):
                branch = [r, s, t]
                types = branch_types(branch)
                red = physical_clause_count(types, 1)
                blue = physical_clause_count(types, 0)
                ordering = 120 * sum(len(comparisons(kind)) for kind in types[1:])
                rows.append({
                    "branch": branch,
                    "atoms": types,
                    "count": branch_cardinality(types, domain_map, root_map, True),
                    "unrooted_count": branch_cardinality(types, domain_map, root_map, False),
                    "red_clauses": red,
                    "blue_clauses": blue,
                    "root_order_clauses": ordering,
                    "cnf_variables": 847,
                    "cnf_clauses": red + blue + ordering + 1,
                })
    require(published["branches"] == rows, "all published branch records")
    total = sum(row["count"] for row in rows)
    unrooted = sum(row["unrooted_count"] for row in rows)
    baseline = 60 * 2 ** 846
    fraction = Fraction(total, baseline)
    require(published["retained_rooted_family"] == total, "rooted total")
    require(published["retained_pair_domain_family"] == unrooted, "unrooted total")
    require(published["raw_packing_family"] == baseline, "packing baseline")
    require(published["full_labelled_graph_space"] == 2 ** 903, "full graph space")
    require(published["retained_fraction_of_packing"] == {
        "numerator": fraction.numerator, "denominator": fraction.denominator}, "fraction")
    require(total < 2 ** 787 and total * 2 ** 65 < baseline, "rooted bounds")
    require(total * 2 ** 36 < unrooted < 2 ** 823, "unrooted bounds")
    require(unrooted * 2 ** 29 < baseline, "pair-domain bound")
    require(published["branch_count"] == 60 and published["fixed_edges"] == 57 and
            published["variable_edges"] == 846 and published["matrix_coordinates"] == 66,
            "global dimensions")
    require(published["five_sets_in_two_atoms"] == 1971 and
            published["five_sets_across_three_or_more_atoms"] == comb(43, 5) - 1971,
            "five-set partition")
    return rows, total, unrooted


def unrank(index, rows, domain_map, root_map):
    require(type(index) is int and 0 <= index < sum(row["count"] for row in rows), "index")
    for row in rows:
        if index >= row["count"]:
            index -= row["count"]
            continue
        types = row["atoms"]
        matrices = []
        for first, second in combinations(range(12), 2):
            states = domains_for(types, domain_map, root_map, first, second)
            index, digit = divmod(index, len(states))
            matrices.append(states[digit])
        require(index == 0, "unrank overflow")
        return {"branch": row["branch"], "matrices": matrices}
    raise ValueError("unrank branch")


def rank(parameters, rows, domain_map, root_map):
    branch = parameters["branch"]
    row_index = next((index for index, row in enumerate(rows) if row["branch"] == branch), None)
    require(row_index is not None, "rank branch")
    row = rows[row_index]
    require(len(parameters["matrices"]) == 66, "rank matrices")
    value = sum(previous["count"] for previous in rows[:row_index])
    place = 1
    for state, (first, second) in zip(parameters["matrices"], combinations(range(12), 2)):
        states = domains_for(row["atoms"], domain_map, root_map, first, second)
        positions = {candidate: position for position, candidate in enumerate(states)}
        require(state in positions, ("rank state", branch, first, second))
        value += positions[state] * place
        place *= len(states)
    require(place == row["count"], "rank branch cardinality")
    return value


def layout(branch):
    types = branch_types(branch)
    blocks = [list(range(4 * index, 4 * index + 4)) for index in range(7)]
    blocks += [list(range(28 + 3 * index, 31 + 3 * index)) for index in range(5)]
    fixed = {}
    for kind, block in zip(types, blocks):
        for first, second in combinations(range(len(block)), 2):
            fixed[block[first], block[second]] = atom_edge(kind, first, second)
    return types, blocks, fixed


def reconstruct_graph(parameters):
    types, blocks, fixed = layout(parameters["branch"])
    matrix = [[0] * 43 for _ in range(43)]
    for (first, second), color in fixed.items():
        matrix[first][second] = matrix[second][first] = color
    for state, (left, right) in zip(parameters["matrices"], combinations(range(12), 2)):
        for row, first in enumerate(blocks[left]):
            for column, second in enumerate(blocks[right]):
                color = state >> (row * len(blocks[right]) + column) & 1
                matrix[first][second] = matrix[second][first] = color
    bits = sum(matrix[first][second] << index
               for index, (first, second) in enumerate(combinations(range(43), 2)))
    return matrix, {"n": 43, "red_hex": format(bits, "0226x")}


def count_fives(matrix):
    red = 0
    blue = 0
    for vertices in combinations(range(43), 5):
        colors = [matrix[first][second] for first, second in combinations(vertices, 2)]
        red += all(colors)
        blue += not any(colors)
    return red, blue


def index_audit(target, rows, total, domain_map, root_map):
    offset = 0
    checks = 0
    for row in rows:
        for index in (offset, offset + row["count"] // 2, offset + row["count"] - 1):
            parameters = unrank(index, rows, domain_map, root_map)
            require(rank(parameters, rows, domain_map, root_map) == index, ("round trip", index))
            checks += 1
        offset += row["count"]
    require(offset == total, "index interval")
    example = json.loads((target / "example-parameters.json").read_text())
    example_index = rank(example, rows, domain_map, root_map)
    require(unrank(example_index, rows, domain_map, root_map) == example, "example rank/unrank")
    matrix, graph = reconstruct_graph(example)
    require(graph == json.loads((target / "example-graph.json").read_text()), "example physical graph")
    red, blue = count_fives(matrix)
    require((red, blue) == (462, 1225), "example target violations")
    return checks, example_index, red, blue


def read_clause(handle, expected, context):
    line = handle.readline()
    require(line, ("premature CNF end", context))
    actual = tuple(map(int, line.split()))
    require(actual == tuple(expected) + (0,), ("CNF clause", context, actual[:20], expected[:20]))


def independent_cnf_audit(path, branch):
    types, blocks, fixed = layout(list(branch))
    free_pairs = [edge for edge in combinations(range(43), 2) if edge not in fixed]
    variables = {edge: index + 2 for index, edge in enumerate(free_pairs)}
    require(len(free_pairs) == 846, "free edge variables")
    root_count = 0
    physical_count = 0
    red_count = 0
    blue_count = 0
    expected_total = (physical_clause_count(types, 1) + physical_clause_count(types, 0) +
                      120 * sum(len(comparisons(kind)) for kind in types[1:]) + 1)
    with path.open("r", encoding="ascii") as handle:
        require(handle.readline().strip() == f"p cnf 847 {expected_total}", "CNF header")
        read_clause(handle, (1,), (branch, "constant"))
        for child in range(1, 12):
            for first_column, second_column in comparisons(types[child]):
                for left in range(16):
                    for right in range(left + 1, 16):
                        expected = []
                        for column, value in ((first_column, left), (second_column, right)):
                            for row in range(4):
                                variable = variables[blocks[0][row], blocks[child][column]]
                                expected.append(-variable if value >> row & 1 else variable)
                        read_clause(handle, expected, (branch, "root", child, left, right))
                        root_count += 1
        for vertices in combinations(range(43), 5):
            edges = tuple(combinations(vertices, 2))
            for color in (1, 0):
                if any(fixed[edge] != color for edge in edges if edge in fixed):
                    continue
                expected = [(-1 if color else 1) * variables[edge]
                            for edge in edges if edge not in fixed]
                read_clause(handle, expected, (branch, vertices, color))
                physical_count += 1
                red_count += color == 1
                blue_count += color == 0
        require(handle.read() == "", ("extra CNF content", branch))
    require(root_count + physical_count + 1 == expected_total, ("clause total", branch))
    return {
        "variables": 847,
        "clauses": expected_total,
        "root_clauses": root_count,
        "physical_clauses": physical_count,
        "red_clauses": red_count,
        "blue_clauses": blue_count,
        "bytes": path.stat().st_size,
        "sha256": file_sha256(path),
    }


def cnf_audit(target, work_root):
    expected = json.loads((target / "EXPECTED_AUDIT.json").read_text())
    expected_by_branch = {tuple(record["branch"]): record for record in expected["cnfs"]}
    require(set(expected_by_branch) == set(FULL_BRANCHES), "expected CNF branches")
    results = []
    with tempfile.TemporaryDirectory(prefix="r55-global-review-", dir=work_root) as directory:
        directory = Path(directory)
        for branch in FULL_BRANCHES:
            path = directory / ("branch-" + "-".join(map(str, branch)) + ".cnf")
            process = subprocess.run(
                [sys.executable, "-B", "model.py", "--branch", ",".join(map(str, branch)),
                 "--cnf", str(path)],
                cwd=target, text=True, capture_output=True, check=True,
            )
            generated = json.loads(process.stdout)
            published = expected_by_branch[branch]
            require(set(generated) <= set(published) and
                    all(generated[key] == published[key] for key in generated),
                    ("generated formula record", branch))
            checked = independent_cnf_audit(path, branch)
            for key in ("variables", "clauses", "red_clauses", "blue_clauses", "bytes", "sha256"):
                require(checked[key] == published[key], ("formula metadata", branch, key))
            require(checked["root_clauses"] == published["root_order_clauses"],
                    ("root clause count", branch))
            require(checked["physical_clauses"] ==
                    published["physical_clauses_checked"], ("physical clause count", branch))
            results.append({"branch": list(branch), **checked})
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()
    require(args.target.is_dir(), "target package")
    require(args.work_root.is_dir(), "work root")

    domain_map = {}
    domain_records = []
    matrix_cases = 0
    for left in ATOMS:
        for right in ATOMS:
            allowed = pair_domain(left, right)
            domain_map[left, right] = allowed
            domain_records.append(bitmap_record(left, right, allowed))
            matrix_cases += 1 << (ATOMS[left][0] * ATOMS[right][0])
    require(matrix_cases == 335872, "matrix case count")
    published_domains = json.loads((args.target / "DOMAINS.json").read_text())
    require(domain_records == published_domains, "entrywise domain catalogs")
    require(sha256(json_bytes(domain_records)).hexdigest() == EXPECTED_DOMAIN_SHA256,
            "domain catalog SHA-256")
    transpose_cases = 0
    for (left, right), allowed in domain_map.items():
        source = set(allowed)
        transposed = set(domain_map[right, left])
        for state in range(1 << (ATOMS[left][0] * ATOMS[right][0])):
            moved = transpose_state(state, ATOMS[left][0], ATOMS[right][0])
            require((state in source) == (moved in transposed), ("transpose", left, right, state))
            transpose_cases += 1
    require(transpose_cases == 335872, "transpose cases")

    root_map = {}
    root_records = []
    orbit_records = []
    for kind in ATOMS:
        canonical, record, orbit = root_orbits(kind, domain_map["R4", kind])
        root_map[kind] = canonical
        root_records.append(record)
        orbit_records.append(orbit)
    require(root_records == json.loads((args.target / "ROOT_DOMAINS.json").read_text()),
            "entrywise root catalogs")
    require(sha256(json_bytes(root_records)).hexdigest() == EXPECTED_ROOT_SHA256,
            "root catalog SHA-256")

    published_counts = json.loads((args.target / "COUNTS.json").read_text())
    rows, total, unrooted = count_audit(published_counts, domain_map, root_map)
    boundary_checks, example_index, example_red, example_blue = index_audit(
        args.target, rows, total, domain_map, root_map)
    formulas = cnf_audit(args.target, args.work_root)
    require(sum(record["physical_clauses"] for record in formulas) == 8414656,
            "six-formula physical clause count")
    require(sum(record["root_clauses"] for record in formulas) == 19680,
            "six-formula root clause count")
    require(sum(record["bytes"] for record in formulas) == 377705100,
            "six-formula byte count")
    require(sha256((args.target / "EXPECTED_AUDIT.json").read_bytes()).hexdigest() ==
            EXPECTED_AUDIT_SHA256, "main audit SHA-256")

    print(json.dumps({
        "boundary_rank_round_trips": boundary_checks,
        "branches": len(rows),
        "cnf_bytes_checked": sum(record["bytes"] for record in formulas),
        "cnf_clauses_checked_entrywise": sum(record["clauses"] for record in formulas),
        "domain_matrix_cases": matrix_cases,
        "example_index": example_index,
        "example_red_fives": example_red,
        "example_blue_fives": example_blue,
        "physical_five_sets": comb(43, 5),
        "retained_pair_domain_family": unrooted,
        "retained_rooted_family": total,
        "root_orbits": orbit_records,
        "status": "VERIFIED_INDEPENDENT_UNCONDITIONAL_GLOBAL_PACKING_REVIEW",
        "transpose_cases": transpose_cases,
    }, sort_keys=True))


if __name__ == "__main__":
    main()

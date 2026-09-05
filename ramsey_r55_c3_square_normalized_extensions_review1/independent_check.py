#!/usr/bin/env python3
"""Clean-room review of the two normalized C3-square Ramsey formulas.

No module from the submitted package is imported.  The two actions are built
from quotient stabilizers, pair orbits and every Ramsey clause are reconstructed
from definitions, and the normalization tail is rebuilt from literal
centralizer permutations.  Saved DRAT proofs are then replayed against the
independently audited formulas.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import subprocess


PUBLISHED_RESULT_SHA256 = (
    "6b36241eb81ff7aa364fcc49e1bda698b3e5e6d671bb9c40d2aec3a00d0df0d5"
)
DRAT_TRIM_SHA256 = (
    "9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a"
)
CASES = {
    9: {"index": 9, "a": 1, "b": [0, 0, 0, 2], "c": 4},
    10: {"index": 10, "a": 1, "b": [0, 0, 1, 1], "c": 4},
}
EXPECTED = {
    9: {
        "variables": 105,
        "parent_clauses": 211323,
        "parent_sha256": "7846688b50408ebb6f9d6a9fc0a537d06186e9d732f5be9856edae6b7e88ca75",
        "full_clauses": 214163,
        "full_sha256": "e58d139ede296b86b44cb5d452c2cc80d374e0805e936dadfed5deb94cd7162f",
        "proof_bytes": 4359167,
        "proof_sha256": "9e10d8805ebb22704c6b17c408632ebc53a4d0b8f6f8b4a74fc5bbc2b7c57ac1",
        "rat_core_lemmas": 138,
    },
    10: {
        "variables": 103,
        "parent_clauses": 210907,
        "parent_sha256": "6455b56f83001e09fd53f7fa8bdbd26270df013a32b3895569ddab3e5d18d929",
        "full_clauses": 213747,
        "full_sha256": "3f583630b73b13026e24415838526984f376315aae9e0f5cc33a5f24e48c3420",
        "proof_bytes": 5517636,
        "proof_sha256": "58894c980c186d3811b33daef72a930b381f2dd80a101cc3c29fb2f53319800e",
        "rat_core_lemmas": 88,
    },
}

# Stabilizer generators for the four projective lines, in the parent case order.
KERNEL_DIRECTIONS = ((0, 1), (1, 0), (1, 2), (1, 1))
REGULAR_STARTS = (7, 16, 25, 34)
QUOTIENT_STARTS = (1, 4)
PROFILE_DIRECTIONS = (1, 3, 4, 5)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def file_info(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def normalize_line(vector: tuple[int, int]) -> tuple[int, int]:
    x, y = vector[0] % 3, vector[1] % 3
    require((x, y) != (0, 0), "zero projective vector")
    scale = pow(x if x else y, -1, 3)
    return x * scale % 3, y * scale % 3


def annihilator(direction: tuple[int, int]) -> tuple[int, int]:
    """Return a canonical nonzero functional whose kernel is direction."""
    return normalize_line((direction[1], -direction[0]))


def action(case: dict[str, object]) -> dict[tuple[int, int], tuple[int, ...]]:
    """Construct the literal F3^2 action from its orbit stabilizers."""
    offset = int(case["a"])
    quotients: list[tuple[int, tuple[int, int]]] = []
    for direction, multiplicity in zip(KERNEL_DIRECTIONS, case["b"], strict=True):
        functional = annihilator(direction)
        for _ in range(int(multiplicity)):
            quotients.append((offset, functional))
            offset += 3
    regulars = []
    for _ in range(int(case["c"])):
        regulars.append(offset)
        offset += 9
    require(offset == 43 and tuple(regulars) == REGULAR_STARTS,
            "unexpected block placement")
    require(tuple(start for start, _ in quotients) == QUOTIENT_STARTS,
            "unexpected quotient placement")

    translations = {}
    for x, y in product(range(3), repeat=2):
        image = list(range(43))
        for start, (u, v) in quotients:
            shift = (u * x + v * y) % 3
            for t in range(3):
                image[start + t] = start + (t + shift) % 3
        for start in regulars:
            for u, v in product(range(3), repeat=2):
                image[start + 3 * u + v] = (
                    start + 3 * ((u + x) % 3) + (v + y) % 3
                )
        translations[x, y] = tuple(image)

    identity = tuple(range(43))
    require(translations[0, 0] == identity and len(set(translations.values())) == 9,
            "action is not faithful")
    for left, right in product(translations, repeat=2):
        composed = tuple(translations[left][translations[right][v]] for v in range(43))
        wanted = translations[(left[0] + right[0]) % 3,
                              (left[1] + right[1]) % 3]
        require(composed == wanted, "F3^2 group law failed")
    return translations


def edge_variables(case: dict[str, object]) -> tuple[dict[tuple[int, int], int], dict[int, tuple[tuple[int, int], ...]]]:
    translations = action(case)
    generators = (translations[1, 0], translations[0, 1])
    unseen = set(combinations(range(43), 2))
    groups = []
    while unseen:
        seed = min(unseen)
        orbit, frontier = {seed}, [seed]
        while frontier:
            u, v = frontier.pop()
            for generator in generators:
                image = tuple(sorted((generator[u], generator[v])))
                if image not in orbit:
                    orbit.add(image)
                    frontier.append(image)
        require(orbit <= unseen, "pair orbits overlap")
        unseen -= orbit
        groups.append(tuple(sorted(orbit)))
    groups.sort(key=lambda orbit: orbit[0])
    ids = {edge: number for number, orbit in enumerate(groups, 1) for edge in orbit}
    inverse = {number: orbit for number, orbit in enumerate(groups, 1)}
    require(len(ids) == math.comb(43, 2), "pair orbit cover is incomplete")
    return ids, inverse


def bits(value: int, width: int) -> tuple[int, ...]:
    return tuple((value >> (width - 1 - j)) & 1 for j in range(width))


def forbidden(variables: tuple[int, ...], word: tuple[int, ...]) -> tuple[int, ...]:
    require(len(variables) == len(word) and len(set(variables)) == len(variables),
            "blocking word repeats a primary variable")
    return tuple(sorted(-variable if bit else variable
                        for variable, bit in zip(variables, word, strict=True)))


def shift_map(start: int, shift: int) -> tuple[int, ...]:
    image = list(range(43))
    if start in QUOTIENT_STARTS:
        require(0 <= shift < 3, "bad quotient shift")
        for j in range(3):
            image[start + j] = start + (j + shift) % 3
    else:
        require(start in REGULAR_STARTS and 0 <= shift < 9, "bad regular shift")
        x, y = divmod(shift, 3)
        for u, v in product(range(3), repeat=2):
            image[start + 3 * u + v] = (
                start + 3 * ((u + x) % 3) + (v + y) % 3
            )
    return tuple(image)


def regular_copy_map(order: tuple[int, ...]) -> tuple[int, ...]:
    require(tuple(sorted(order)) == tuple(range(4)), "bad block permutation")
    image = list(range(43))
    for new_block, old_block in enumerate(order):
        new_start, old_start = REGULAR_STARTS[new_block], REGULAR_STARTS[old_block]
        for j in range(9):
            image[new_start + j] = old_start + j
    return tuple(image)


def apply_vertex_map(edge: tuple[int, int], image: tuple[int, ...]) -> tuple[int, int]:
    return tuple(sorted((image[edge[0]], image[edge[1]])))


def induced_variable_map(image: tuple[int, ...], ids: dict[tuple[int, int], int],
                         inverse: dict[int, tuple[tuple[int, int], ...]]) -> dict[int, int]:
    require(tuple(sorted(image)) == tuple(range(43)), "map is not a permutation")
    induced = {}
    for variable, orbit in inverse.items():
        targets = {ids[apply_vertex_map(edge, image)] for edge in orbit}
        require(len(targets) == 1, "vertex map does not preserve the orbit partition")
        induced[variable] = targets.pop()
    require(set(induced.values()) == set(inverse), "induced variable map is not bijective")
    return induced


def profile_variables(ids: dict[tuple[int, int], int], start: int) -> tuple[int, ...]:
    edge = lambda u, v: ids[tuple(sorted((u, v)))]
    return (edge(0, start), *(edge(start, start + d) for d in PROFILE_DIRECTIONS))


def cross_variables(ids: dict[tuple[int, int], int], start: int) -> tuple[int, ...]:
    size = 3 if start in QUOTIENT_STARTS else 9
    edge = lambda u, v: ids[tuple(sorted((u, v)))]
    return tuple(edge(7, start + j) for j in range(size))


def normalization_tail(ids: dict[tuple[int, int], int]) -> tuple[list[tuple[int, ...]], dict[str, object]]:
    profiles = [profile_variables(ids, start) for start in REGULAR_STARTS]
    require(len(set(sum(profiles, ()))) == 20, "profile coordinates are not independent")
    order_clauses = set()
    for left, right in zip(profiles, profiles[1:]):
        for a, b in product(range(32), repeat=2):
            if a > b:
                order_clauses.add(forbidden(left + right, bits(a, 5) + bits(b, 5)))

    local_clauses = set()
    regular_minima = set()
    quotient_minima = set()
    local_semantics = {}
    for start in (*REGULAR_STARTS[1:], *QUOTIENT_STARTS):
        variables = cross_variables(ids, start)
        width = len(variables)
        accepted = set()
        for value in range(1 << width):
            word = bits(value, width)
            images = []
            for shift in range(width):
                image = shift_map(start, shift)
                images.append(tuple(word[image[start + j] - start] for j in range(width)))
            minimum = min(images)
            if word == minimum:
                accepted.add(value)
            else:
                local_clauses.add(forbidden(variables, word))
        wanted = 64 if width == 9 else 4
        require(len(accepted) == wanted, "wrong translation orbit count")
        (regular_minima if width == 9 else quotient_minima).update(accepted)

        relevant = [clause for clause in local_clauses
                    if set(map(abs, clause)) == set(variables)]
        for value in range(1 << width):
            assignment = dict(zip(variables, bits(value, width), strict=True))
            satisfies = all(any(assignment[abs(literal)] == (literal > 0)
                                for literal in clause) for clause in relevant)
            require(satisfies == (value in accepted), "local CNF semantics failed")
        local_semantics[str(start)] = {
            "width": width,
            "assignments_checked": 1 << width,
            "canonical_words": len(accepted),
        }

    require(len(order_clauses) == 3 * 496, "profile clause count differs")
    require(len(local_clauses) == 3 * 448 + 2 * 4, "local clause count differs")
    require(not order_clauses & local_clauses, "normalization families overlap")

    # Exact truth-table audit of each adjacent lexicographic comparator.
    comparator_assignments = 0
    for left, right in zip(profiles, profiles[1:]):
        relevant = [clause for clause in order_clauses
                    if set(map(abs, clause)) == set(left + right)]
        require(len(relevant) == 496, "comparator support differs")
        for a, b in product(range(32), repeat=2):
            word = bits(a, 5) + bits(b, 5)
            assignment = dict(zip(left + right, word, strict=True))
            satisfies = all(any(assignment[abs(literal)] == (literal > 0)
                                for literal in clause) for clause in relevant)
            require(satisfies == (a <= b), "profile comparator semantics failed")
            comparator_assignments += 1

    tail = sorted(order_clauses | local_clauses,
                  key=lambda clause: (len(clause), clause))
    require(len(tail) == 2840, "normalization tail count differs")
    return tail, {
        "profile_order_clauses": len(order_clauses),
        "profile_comparator_assignments": comparator_assignments,
        "regular_translation_clauses": 3 * 448,
        "quotient_rotation_clauses": 2 * 4,
        "tail_clauses": len(tail),
        "regular_binary_translation_classes": len(regular_minima),
        "quotient_binary_translation_classes": len(quotient_minima),
        "local_semantics": local_semantics,
    }


def centralizer_audit(case: dict[str, object], ids: dict[tuple[int, int], int],
                      inverse: dict[int, tuple[tuple[int, int], ...]]) -> dict[str, object]:
    translations = action(case)
    generators = (translations[1, 0], translations[0, 1])
    profiles = {start: profile_variables(ids, start) for start in REGULAR_STARTS}
    crosses = {start: cross_variables(ids, start)
               for start in (*REGULAR_STARTS[1:], *QUOTIENT_STARTS)}

    maps: list[tuple[str, tuple[int, ...]]] = []
    for order in permutations(range(4)):
        maps.append(("regular_permutation", regular_copy_map(order)))
    for start in REGULAR_STARTS[1:]:
        for shift in range(9):
            maps.append(("regular_translation", shift_map(start, shift)))
    for start in QUOTIENT_STARTS:
        for shift in range(3):
            maps.append(("quotient_rotation", shift_map(start, shift)))

    kinds = Counter()
    for kind, image in maps:
        for generator in generators:
            require(all(image[generator[v]] == generator[image[v]] for v in range(43)),
                    "claimed map does not centralize H")
        induced = induced_variable_map(image, ids, inverse)
        require(len(induced) == len(inverse), "incomplete induced variable action")
        kinds[kind] += 1

    # The post-sort translations preserve every profile.  A local shift acts
    # only on its own anchor word and permutes that word's variables.
    locality_checks = 0
    all_profile_variables = set(sum(profiles.values(), ()))
    for start in REGULAR_STARTS[1:]:
        for shift in range(9):
            induced = induced_variable_map(shift_map(start, shift), ids, inverse)
            require(all(induced[v] == v for v in all_profile_variables),
                    "regular translation changed a sorted profile")
            for other, variables in crosses.items():
                images = {induced[v] for v in variables}
                if other == start and start != 7:
                    require(images == set(variables), "translation left its anchor word")
                else:
                    require(all(induced[v] == v for v in variables),
                            "translation changed another anchor word")
                locality_checks += len(variables)
    for start in QUOTIENT_STARTS:
        for shift in range(3):
            induced = induced_variable_map(shift_map(start, shift), ids, inverse)
            require(all(induced[v] == v for v in all_profile_variables),
                    "quotient rotation changed a sorted profile")
            for other, variables in crosses.items():
                images = {induced[v] for v in variables}
                if other == start:
                    require(images == set(variables), "rotation left its anchor word")
                else:
                    require(all(induced[v] == v for v in variables),
                            "rotation changed another anchor word")
                locality_checks += len(variables)

    # Copy permutations carry coordinates identically, hence carry the five
    # profile coordinates identically.  This is precisely the sort operation.
    profile_transport_checks = 0
    for order in permutations(range(4)):
        induced = induced_variable_map(regular_copy_map(order), ids, inverse)
        for new_block, old_block in enumerate(order):
            new = profiles[REGULAR_STARTS[new_block]]
            old = profiles[REGULAR_STARTS[old_block]]
            require(tuple(induced[v] for v in new) == old,
                    "copy permutation changed profile coordinates")
            profile_transport_checks += 5

    # All four profiles can therefore be sorted; this exhausts their 32^4
    # abstract possibilities without assuming independent basis changes.
    profile_tuples = 0
    for values in product(range(32), repeat=4):
        ordered = tuple(sorted(values))
        require(Counter(ordered) == Counter(values)
                and all(ordered[j] <= ordered[j + 1] for j in range(3)),
                "profile sort has no copy permutation")
        profile_tuples += 1

    return {
        "maps_checked": len(maps),
        "map_kinds": dict(sorted(kinds.items())),
        "profile_transport_checks": profile_transport_checks,
        "locality_variable_checks": locality_checks,
        "profile_tuples_sorted": profile_tuples,
        # These are the distinct sequential choices in the stated normal-form
        # procedure.  They are not called a subgroup: conjugating by all S4
        # copy permutations would also generate translations of the anchor.
        "normalization_choice_count": 24 * (9 ** 3) * (3 ** 2),
        "independent_linear_basis_changes_used": False,
    }


def ramsey_clauses(ids: dict[tuple[int, int], int]) -> set[tuple[int, ...]]:
    clauses = set()
    for five in combinations(range(43), 5):
        positive = tuple(sorted({ids[edge] for edge in combinations(five, 2)}))
        clauses.add(positive)
        clauses.add(tuple(sorted(-literal for literal in positive)))
    return clauses


def read_clause(line: str) -> tuple[int, ...]:
    values = tuple(map(int, line.split()))
    require(values and values[-1] == 0 and all(values[:-1]), "malformed DIMACS clause")
    clause = values[:-1]
    require(tuple(sorted(clause)) == clause and len(set(clause)) == len(clause)
            and not any(-literal in clause for literal in clause),
            "noncanonical DIMACS clause")
    return clause


def formula_audit(index: int, work: Path) -> tuple[dict[str, object], dict[str, object]]:
    reference = EXPECTED[index]
    ids, inverse = edge_variables(CASES[index])
    variables = len(inverse)
    require(variables == reference["variables"], "pair-orbit count differs")
    histogram = Counter(len(orbit) for orbit in inverse.values())
    require(sum(size * count for size, count in histogram.items()) == 903,
            "pair orbits do not cover all literal edges")
    require(ids[(0, 1)] == 1, "complement-normalization variable differs")

    base = ramsey_clauses(ids)
    ramsey_count = len(base)
    require(all(tuple(sorted(-x for x in clause)) in base for clause in base),
            "Ramsey formula is not complement-symmetric")
    require((1,) not in base and (-1,) not in base, "unexpected Ramsey unit")
    base.add((1,))
    parent_expected = sorted(base, key=lambda clause: (len(clause), clause))
    require(len(parent_expected) == reference["parent_clauses"],
            "parent clause count differs")
    tail, tail_report = normalization_tail(ids)

    parent = work / f"parent_{index:02}.cnf"
    full = work / f"case_{index:02}.cnf"
    require(file_info(parent)["sha256"] == reference["parent_sha256"],
            "parent formula digest differs")
    require(file_info(full)["sha256"] == reference["full_sha256"],
            "full formula digest differs")
    with parent.open() as parent_stream, full.open() as full_stream:
        require(parent_stream.readline().rstrip("\n") ==
                f"p cnf {variables} {len(parent_expected)}", "parent header differs")
        require(full_stream.readline().rstrip("\n") ==
                f"p cnf {variables} {len(parent_expected) + len(tail)}",
                "full header differs")
        for clause in parent_expected:
            parent_line = parent_stream.readline()
            full_line = full_stream.readline()
            require(parent_line == full_line, "full formula changed a parent byte")
            require(read_clause(parent_line) == clause, "parent clause reconstruction differs")
        require(parent_stream.readline() == "", "extra parent content")
        for clause in tail:
            require(read_clause(full_stream.readline()) == clause,
                    "normalization tail reconstruction differs")
        require(full_stream.readline() == "", "extra full-formula content")

    report = {
        "index": index,
        "variables": variables,
        "edge_orbit_size_histogram": {str(k): histogram[k] for k in sorted(histogram)},
        "five_sets_checked": math.comb(43, 5),
        "ramsey_clauses": ramsey_count,
        "parent_clauses": len(parent_expected),
        "tail": tail_report,
        "full_clauses": len(parent_expected) + len(tail),
        "parent": file_info(parent),
        "full": file_info(full),
    }
    return report, centralizer_audit(CASES[index], ids, inverse)


def replay(index: int, work: Path, checker: Path) -> dict[str, object]:
    reference = EXPECTED[index]
    formula = work / f"case_{index:02}.cnf"
    proof = work / f"case_{index:02}.drat"
    proof_info = file_info(proof)
    require(proof_info == {"bytes": reference["proof_bytes"],
                           "sha256": reference["proof_sha256"]},
            "proof digest differs")
    log = work / f"review_replay_{index:02}.log"
    with log.open("w") as output:
        process = subprocess.run(
            [str(checker), str(formula), str(proof), "-t", "600"],
            stdout=output,
            stderr=subprocess.STDOUT,
            timeout=660,
        )
    text = log.read_text()
    require(process.returncode == 0 and "s VERIFIED" in text,
            "DRAT replay failed")
    match = re.search(r"(\d+) RAT lemmas in core", text)
    require(match is not None, "missing RAT statistic")
    rat = int(match.group(1))
    require(rat == reference["rat_core_lemmas"], "RAT-core count differs")
    return {"index": index, "proof": proof_info, "drat_trim_verified": True,
            "rat_core_lemmas": rat}


def published_manifest_audit(source: Path, work: Path) -> dict[str, object]:
    published_path = source / "result.json"
    require(file_info(published_path)["sha256"] == PUBLISHED_RESULT_SHA256,
            "published manifest changed")
    published = json.loads(published_path.read_text())
    regenerated = json.loads((work / "result.json").read_text())
    require(published["excluded_indices"] == [9, 10]
            and published["open_indices"] == []
            and published["complete_bounded_sweep"]
            and not published["target_graph_found"],
            "published bounded result differs")
    require(regenerated["excluded_indices"] == [9, 10]
            and regenerated["open_indices"] == []
            and regenerated["complete_bounded_sweep"]
            and not regenerated["target_graph_found"],
            "regenerated bounded result differs")
    for position, index in enumerate((9, 10)):
        expected, pub, local = EXPECTED[index], published["cases"][position], regenerated["cases"][position]
        require(pub["action"] == CASES[index] and local["action"] == CASES[index],
                "case meaning differs")
        require(pub["status"] == local["status"] == "excluded", "case status differs")
        require(pub["formula"]["sha256"] == local["formula"]["sha256"] == expected["full_sha256"],
                "formula manifest digest differs")
        require(pub["proof"]["sha256"] == local["proof"]["sha256"] == expected["proof_sha256"],
                "proof manifest digest differs")
    return {"published_result": file_info(published_path),
            "regenerated_excluded_indices": regenerated["excluded_indices"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--drat-trim", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    source, work, checker = args.source.resolve(), args.work.resolve(), args.drat_trim.resolve()
    require(file_info(checker)["sha256"] == DRAT_TRIM_SHA256,
            "unexpected DRAT checker")

    report: dict[str, object] = {
        "manifest": published_manifest_audit(source, work),
        "drat_trim": file_info(checker),
        "formula_audits": [],
        "centralizer_audits": [],
        "proof_replays": [],
        "excluded_indices": [9, 10],
        "open_indices": [],
        "all_residual_c3_square_actions_excluded": True,
    }
    for index in (9, 10):
        formula_report, centralizer_report = formula_audit(index, work)
        report["formula_audits"].append(formula_report)
        report["centralizer_audits"].append({"index": index, **centralizer_report})
        report["proof_replays"].append(replay(index, work, checker))
        print(f"PASS case {index}: clean formula, centralizer coverage, general DRAT", flush=True)

    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Clean-room review of the eleven-cycle order-three Ramsey restriction.

This checker imports no submitted Python or C++ module.  It constructs the
literal order-three pair action, rebuilds every primary and auxiliary clause,
compares the complete canonical DIMACS streams, and replays exactly the four
claimed DRAT refutations.  Separate exhaustive controls cover the local
arithmetic, signed/repeated prefix counters, and centralizer normalization.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from math import factorial
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess


SENTINEL = 1_000_000_000
EXCLUDED = (0, 1, 2, 5)
OPEN = (3, 4)
PUBLISHED_RESULT_SHA256 = (
    "d04644ec9a3f6f4df569fe8edb8bc7a0422a8732adcbb0f1590758397f8bd8fe"
)
DRAT_TRIM_SHA256 = (
    "9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a"
)
EXPECTED = {
    0: (34196, 613487, 527393,
        "3c25b935879113509dceacaaef331843e690c1a9bae5b36c0ea718192663e7be"),
    1: (34226, 614357, 528023,
        "414ac62719c664576301cc4d1485f4f2c6220e22abf9f744d58286aa59e02a57"),
    2: (34250, 615050, 528527,
        "9456f1c526c809178499a7a86a40e6f5875ad77731f1293de21d9601f5ccf5ec"),
    3: (34268, 615572, 528905,
        "82f27b524e893d237f7a478c43bc9d49ff559faaa28e260d688d1591bdfaad20"),
    4: (34280, 615920, 529157,
        "c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f"),
    5: (34286, 616094, 529283,
        "7a982d0d0930d2e5a6108eda46b102dc0b76d5a2a6d23538aba81f23ab1e99ec"),
}
PROOFS = {
    0: (10796990, "7be766a3d560e9910807a40635eb53d0db72e105dee9b54f1664b28704362a51", 59),
    1: (22515780, "ac35c0c6eb0b284322107c635190a1a93547f8f2f51ecce01756cc9371d12f2d", 420),
    2: (66105036, "1d47fcddd152813279b3c2893778feaa783bbdd6e982bc62f277c053eaa48c54", 932),
    5: (123939118, "d6461dabbac88646436b0579ac1fb2dbeed01b4412a224d56d4ad8101c9430e2", 1558),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def file_info(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def pair_values(red_cycles: int) -> tuple[dict[tuple[int, int], int], dict[str, int]]:
    """Discover actual pair orbits, then apply the documented variable order."""
    sigma = tuple(3 * (v // 3) + (v + 1) % 3 if v < 33 else v
                  for v in range(43))
    unseen = set(combinations(range(43), 2))
    orbits: list[tuple[tuple[int, int], ...]] = []
    while unseen:
        edge = min(unseen)
        orbit = set()
        while edge not in orbit:
            orbit.add(edge)
            edge = tuple(sorted((sigma[edge[0]], sigma[edge[1]])))
        require(orbit <= unseen, "pair orbits overlap")
        unseen -= orbit
        orbits.append(tuple(sorted(orbit)))

    cross = sorted(orbit for orbit in orbits
                   if orbit[0][1] < 33
                   and orbit[0][0] // 3 != orbit[0][1] // 3)
    fixed = sorted(orbit for orbit in orbits if orbit[0][0] >= 33)
    links = sorted((orbit for orbit in orbits if orbit[0][0] < 33 <= orbit[0][1]),
                   key=lambda orbit: (orbit[0][1], orbit[0][0]))
    internal = sorted(orbit for orbit in orbits
                      if orbit[0][1] < 33
                      and orbit[0][0] // 3 == orbit[0][1] // 3)
    require((len(orbits), len(cross), len(fixed), len(links), len(internal))
            == (331, 165, 45, 110, 11), "wrong literal pair-orbit partition")

    values: dict[tuple[int, int], int] = {}
    for variable, orbit in enumerate(cross + fixed + links, 1):
        for edge in orbit:
            values[edge] = variable
    for orbit in internal:
        color = orbit[0][0] // 3 < red_cycles
        for edge in orbit:
            values[edge] = SENTINEL if color else -SENTINEL
    require(len(values) == 903, "not every literal pair received a value")
    return values, {
        "all": len(orbits), "moving_cross": len(cross),
        "fixed_fixed": len(fixed), "fixed_moving": len(links),
        "internal_constants": len(internal),
    }


def reconstruct_formula(red_cycles: int) -> tuple[int, set[tuple[int, ...]], dict[str, int]]:
    values, orbit_counts = pair_values(red_cycles)
    clauses: set[tuple[int, ...]] = set()

    def edge(a: int, b: int) -> int:
        return values[tuple(sorted((a, b)))]

    def add(literals) -> None:
        row = set(literals)
        if SENTINEL in row:
            return
        row.discard(-SENTINEL)
        if any(-literal in row for literal in row):
            return
        require(all(1 <= abs(literal) < SENTINEL for literal in row),
                "literal outside exact variable range")
        clauses.add(tuple(sorted(row)))

    five_sets = 0
    for vertices in combinations(range(43), 5):
        five_sets += 1
        edges = [edge(a, b) for a, b in combinations(vertices, 2)]
        add(edges)
        add(-literal for literal in edges)
    require(five_sets == 962598, "five-set cover differs")
    ramsey_clauses = len(clauses)

    next_variable = 320
    colors = [int(i < red_cycles) for i in range(11)]
    deficit_tokens: list[list[int]] = [[] for _ in range(11)]
    complete_tokens: list[list[int]] = [[] for _ in range(11)]
    gate_truth_assignments = 0
    for left, right in combinations(range(11), 2):
        bits = tuple(edge(3 * left, 3 * right + offset) for offset in range(3))
        gates: dict[int, tuple[int, int, int]] = {}
        for color in sorted({colors[left], colors[right]}):
            one, two, complete = next_variable + 1, next_variable + 2, next_variable + 3
            next_variable += 3
            gates[color] = (one, two, complete)
            for assignment in product((0, 1), repeat=3):
                weight = sum(bit == color for bit in assignment)
                deficit = 2 - weight + 3 * (weight == 3)
                falsified = [-variable if bit else variable
                             for variable, bit in zip(bits, assignment, strict=True)]
                add(falsified + [one if deficit >= 1 else -one])
                add(falsified + [two if deficit >= 2 else -two])
                add(falsified + [complete if weight == 3 else -complete])
                gate_truth_assignments += 1
        for endpoint in (left, right):
            one, two, complete = gates[colors[endpoint]]
            deficit_tokens[endpoint].extend((one, two))
            complete_tokens[endpoint].append(complete)
        if left == 0:
            add((-bits[1], bits[0]))
            add((-bits[2], bits[1]))

    counter_calls = 0
    counter_cells = 0

    def at_most(inputs: list[int], bound: int) -> None:
        nonlocal next_variable, counter_calls, counter_cells
        cells: dict[tuple[int, int], int] = {}
        for prefix in range(1, len(inputs) + 1):
            for threshold in range(1, min(prefix, bound + 1) + 1):
                next_variable += 1
                cells[prefix, threshold] = next_variable
                counter_cells += 1
        for prefix, literal in enumerate(inputs, 1):
            for threshold in range(1, min(prefix, bound + 1) + 1):
                cell = cells[prefix, threshold]
                if threshold == 1:
                    add((-literal, cell))
                if (prefix - 1, threshold) in cells:
                    add((-cells[prefix - 1, threshold], cell))
                if threshold > 1 and (prefix - 1, threshold - 1) in cells:
                    add((-literal, -cells[prefix - 1, threshold - 1], cell))
        if (len(inputs), bound + 1) in cells:
            add((-cells[len(inputs), bound + 1],))
        counter_calls += 1

    for row in deficit_tokens:
        require(len(row) == 20, "deficit-token row differs")
        at_most(row, 8)

    triangle_pairs = tuple(combinations(range(11), 2))
    for triangle in range(11):
        sign = 1 if colors[triangle] else -1
        fixed_own = [sign * edge(3 * triangle, fixed) for fixed in range(33, 43)]
        common = fixed_own + [token for token in complete_tokens[triangle] for _ in range(3)]
        require(len(common) == 40, "common-neighborhood input differs")
        at_most(common, 4)

        moving_own = [
            sign * edge(3 * left, 3 * right + offset)
            for left, right in triangle_pairs if triangle in (left, right)
            for offset in range(3)
        ]
        outside_own = fixed_own + moving_own
        require(len(outside_own) == 40, "moving-degree input differs")
        at_most(outside_own, 22)
        at_most([-literal for literal in outside_own], 24)

    for fixed in range(33, 43):
        incident = [edge(fixed, other) for other in range(33, 43) if other != fixed]
        incident.extend(edge(3 * moving, fixed) for moving in range(11) for _ in range(3))
        require(len(incident) == 42, "fixed-degree input differs")
        at_most(incident, 24)
        at_most([-literal for literal in incident], 24)

    # Canonical anchor words are componentwise ordered within each internal color.
    for block in range(1, 10):
        if colors[block] == colors[block + 1]:
            for offset in range(3):
                add((-edge(0, 3 * block + offset),
                     edge(0, 3 * (block + 1) + offset)))

    # Adjacent fixed signatures are lexicographically nondecreasing.
    for fixed in range(33, 42):
        left = [edge(3 * moving, fixed) for moving in range(11)]
        right = [edge(3 * moving, fixed + 1) for moving in range(11)]
        for position in range(11):
            for prefix in product((0, 1), repeat=position):
                row: list[int] = []
                for coordinate, bit in enumerate(prefix):
                    row.extend((-left[coordinate], -right[coordinate])
                               if bit else (left[coordinate], right[coordinate]))
                add(row + [-left[position], right[position]])

    expected_variables, _, expected_ramsey, _ = EXPECTED[red_cycles]
    require(next_variable == expected_variables, "auxiliary variable count differs")
    require(ramsey_clauses == expected_ramsey, "Ramsey clause count differs")
    return next_variable, clauses, {
        "five_sets": five_sets,
        "ramsey_clauses": ramsey_clauses,
        "gate_truth_assignments": gate_truth_assignments,
        "counter_calls": counter_calls,
        "counter_cells": counter_cells,
        **{f"edge_orbits_{name}": count for name, count in orbit_counts.items()},
    }


def compare_formula(red_cycles: int, path: Path) -> dict[str, object]:
    variables, clauses, audit = reconstruct_formula(red_cycles)
    wanted_variables, wanted_clauses, _, wanted_sha = EXPECTED[red_cycles]
    require((variables, len(clauses)) == (wanted_variables, wanted_clauses),
            f"formula dimensions differ for r={red_cycles}")
    info = file_info(path)
    require(info["sha256"] == wanted_sha, f"formula digest differs for r={red_cycles}")
    ordered = sorted(clauses, key=lambda clause: (len(clause), clause))
    with path.open() as stream:
        require(stream.readline() == f"p cnf {variables} {len(ordered)}\n",
                f"DIMACS header differs for r={red_cycles}")
        for number, wanted in enumerate(ordered, 1):
            observed = tuple(map(int, stream.readline().split()))
            require(observed and observed[-1] == 0 and observed[:-1] == wanted,
                    f"canonical clause mismatch at {number}, r={red_cycles}")
        require(stream.readline() == "", f"trailing DIMACS content for r={red_cycles}")
    return {"red_cycles": red_cycles, "variables": variables,
            "clauses": len(clauses), "formula": info,
            "exact_canonical_match": True, **audit}


def local_arithmetic() -> dict[str, object]:
    histogram: Counter[tuple[int, int]] = Counter()
    feasible_profiles = 0
    budget_only_false = 0
    missing_upper = 0
    for weights in product(range(4), repeat=10):
        complete = weights.count(3)
        deficit = sum((2, 1, 0, 2)[weight] for weight in weights)
        allowed = [fixed for fixed in range(11)
                   if fixed + 3 * complete <= 4
                   and 18 <= 2 + fixed + sum(weights) <= 24]
        lower = max(0, deficit - 4 - 3 * complete)
        upper = min(10, 4 - 3 * complete, deficit + 2 - 3 * complete)
        require(allowed == list(range(lower, upper + 1)), "fixed-count interval differs")
        require(bool(allowed) == (deficit <= 8 and complete <= 1),
                "local existence criterion differs")
        budget_only_false += deficit <= 8 and not allowed
        missing_upper += sum(fixed + 3 * complete <= 4
                             and 2 + fixed + sum(weights) > 24
                             for fixed in range(11))
        feasible_profiles += len(allowed)
        if allowed:
            histogram[complete, deficit] += len(allowed)

    occupancy: Counter[tuple[int, int]] = Counter()
    for n0 in range(11):
        for n1 in range(11 - n0):
            for n2 in range(11 - n0 - n1):
                n3 = 10 - n0 - n1 - n2
                multiplicity = factorial(10) // (
                    factorial(n0) * factorial(n1) * factorial(n2) * factorial(n3)
                )
                weight_sum = n1 + 2 * n2 + 3 * n3
                deficit = 2 * n0 + n1 + 2 * n3
                count = sum(fixed + 3 * n3 <= 4
                            and 18 <= 2 + fixed + weight_sum <= 24
                            for fixed in range(11))
                if count:
                    occupancy[n3, deficit] += multiplicity * count
    require(histogram == occupancy, "multinomial local census differs")
    require((feasible_profiles, budget_only_false, missing_upper)
            == (80726, 23565, 12), "local arithmetic totals differ")
    return {
        "weight_vectors": 4 ** 10,
        "fixed_count_trials": 11 * 4 ** 10,
        "feasible_profiles": feasible_profiles,
        "budget_only_false_weight_vectors": budget_only_false,
        "profiles_admitted_without_upper_degree": missing_upper,
        "multinomial_entrywise_match": True,
        "by_complete_blocks": {
            str(complete): sum(count for (blocks, _), count in histogram.items()
                               if blocks == complete)
            for complete in (0, 1)
        },
    }


def counter_clauses(inputs: list[int], bound: int) -> tuple[int, set[tuple[int, ...]], dict[tuple[int, int], int]]:
    primary = max(map(abs, inputs))
    next_variable = primary
    cells = {}
    clauses = set()
    for prefix in range(1, len(inputs) + 1):
        for threshold in range(1, min(prefix, bound + 1) + 1):
            next_variable += 1
            cells[prefix, threshold] = next_variable
    for prefix, literal in enumerate(inputs, 1):
        for threshold in range(1, min(prefix, bound + 1) + 1):
            cell = cells[prefix, threshold]
            if threshold == 1:
                clauses.add(tuple(sorted((-literal, cell))))
            if (prefix - 1, threshold) in cells:
                clauses.add(tuple(sorted((-cells[prefix - 1, threshold], cell))))
            if threshold > 1 and (prefix - 1, threshold - 1) in cells:
                clauses.add(tuple(sorted((-literal, -cells[prefix - 1, threshold - 1], cell))))
    if (len(inputs), bound + 1) in cells:
        clauses.add((-cells[len(inputs), bound + 1],))
    return next_variable, clauses, cells


def unit_conflict(clauses: set[tuple[int, ...]], assumptions: list[int]) -> bool:
    values: dict[int, bool] = {}
    for literal in assumptions:
        if abs(literal) in values and values[abs(literal)] != (literal > 0):
            return True
        values[abs(literal)] = literal > 0
    while True:
        changed = False
        for clause in clauses:
            unknown = []
            for literal in clause:
                if abs(literal) not in values:
                    unknown.append(literal)
                elif values[abs(literal)] == (literal > 0):
                    break
            else:
                if not unknown:
                    return True
                if len(unknown) == 1:
                    variable, value = abs(unknown[0]), unknown[0] > 0
                    if variable in values and values[variable] != value:
                        return True
                    if variable not in values:
                        values[variable] = value
                        changed = True
        if not changed:
            return False


def counter_semantics() -> dict[str, int]:
    trials = 0
    for length in range(1, 7):
        rows = (
            list(range(1, length + 1)),
            [(-1) ** variable * variable for variable in range(1, length + 1)],
            [1 if position < 3 else position - 1 for position in range(length)],
        )
        for inputs in rows:
            primary = max(map(abs, inputs))
            for bound in range(length + 1):
                _, clauses, cells = counter_clauses(inputs, bound)
                for primary_bits in product((False, True), repeat=primary):
                    values = {variable + 1: bit for variable, bit in enumerate(primary_bits)}
                    running = 0
                    for prefix, literal in enumerate(inputs, 1):
                        running += values[abs(literal)] == (literal > 0)
                        for threshold in range(1, min(prefix, bound + 1) + 1):
                            values[cells[prefix, threshold]] = running >= threshold
                    total = sum(values[abs(literal)] == (literal > 0) for literal in inputs)
                    assumptions = [variable + 1 if bit else -variable - 1
                                   for variable, bit in enumerate(primary_bits)]
                    if total <= bound:
                        require(all(any(values[abs(literal)] == (literal > 0)
                                        for literal in clause) for clause in clauses),
                                "prefix counter lost a valid signed/repeated assignment")
                    else:
                        require(unit_conflict(clauses, assumptions),
                                "prefix counter did not force an overflow")
                    trials += 1
    require(trials == 1734, "counter semantic trial count differs")
    return {"signed_and_repeated_assignments": trials}


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[v]] for v in range(43))


def normalization_audit() -> dict[str, int | bool | list[int]]:
    sigma = tuple(3 * (v // 3) + (v + 1) % 3 if v < 33 else v
                  for v in range(43))
    maps = []
    # Rotations of every moving cycle.
    for block in range(11):
        for shift in (1, 2):
            image = list(range(43))
            for offset in range(3):
                image[3 * block + offset] = 3 * block + (offset + shift) % 3
            maps.append(tuple(image))
    # Adjacent whole-cycle swaps generate all coordinate-identical S_11 maps.
    for block in range(10):
        image = list(range(43))
        for offset in range(3):
            image[3 * block + offset] = 3 * (block + 1) + offset
            image[3 * (block + 1) + offset] = 3 * block + offset
        maps.append(tuple(image))
    # Adjacent fixed-vertex swaps generate S_10.
    for fixed in range(33, 42):
        image = list(range(43))
        image[fixed], image[fixed + 1] = image[fixed + 1], image[fixed]
        maps.append(tuple(image))
    for image in maps:
        require(tuple(sorted(image)) == tuple(range(43)), "normalizer map is not bijective")
        require(compose(image, sigma) == compose(sigma, image),
                "claimed relabeling does not centralize the order-three action")

    canonical_words = []
    rotations_checked = 0
    for word in product((0, 1), repeat=3):
        rotations = [word[shift:] + word[:shift] for shift in range(3)]
        matches = {candidate for candidate in rotations
                   if candidate == tuple(sorted(candidate, reverse=True))}
        require(len(matches) == 1, "anchor word lacks a unique canonical word")
        canonical_words.extend(matches)
        rotations_checked += len(rotations)
    chain = sorted(set(canonical_words), key=sum)
    require(chain == [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
            "canonical anchor-word chain differs")
    require(all(all(left[k] <= right[k] for k in range(3))
                for left, right in zip(chain, chain[1:])),
            "weight order is not componentwise order")

    complement_counts = {min(red, 11 - red) for red in range(12)}
    require(complement_counts == set(range(6)), "complement count cover differs")
    internal_profiles = 0
    for mask in range(1 << 11):
        colors = [(mask >> block) & 1 for block in range(11)]
        reverse = sum(colors) > 5
        normalized = sorted((bit ^ reverse for bit in colors), reverse=True)
        require(sum(normalized) in range(6), "internal colors did not enter six-case cover")
        internal_profiles += 1

    # A first 1>0 difference is exactly the forbidden lexicographic event.
    signature_pairs = 0
    for left_value in range(1 << 11):
        left = tuple((left_value >> (10 - position)) & 1 for position in range(11))
        for right_value in range(1 << 11):
            right = tuple((right_value >> (10 - position)) & 1 for position in range(11))
            forbidden = any(left[:position] == right[:position]
                            and left[position] == 1 and right[position] == 0
                            for position in range(11))
            require((not forbidden) == (left <= right), "fixed-signature order differs")
            signature_pairs += 1
    return {
        "centralizer_generators_checked": len(maps),
        "three_bit_rotations_checked": rotations_checked,
        "canonical_anchor_words": len(chain),
        "internal_color_profiles": internal_profiles,
        "complement_counts": sorted(complement_counts),
        "fixed_signature_pairs_checked": signature_pairs,
        "independent_reflections_or_extra_automorphisms_used": False,
    }


def manifest_audit(source: Path, proof_work: Path) -> dict[str, object]:
    path = source / "result.json"
    require(file_info(path)["sha256"] == PUBLISHED_RESULT_SHA256,
            "published result manifest changed")
    result = json.loads(path.read_text())
    require(result["excluded_counts"] == list(EXCLUDED)
            and result["open_counts"] == list(OPEN)
            and result["complete_bounded_sweep"]
            and not result["all_counts_excluded"]
            and not result["target_graph_found"], "published case partition differs")
    require([row["red_cycles"] for row in result["cases"]] == list(range(6)),
            "published six-case cover is incomplete")
    for red_cycles, row in enumerate(result["cases"]):
        expected_variables, expected_clauses, _, expected_sha = EXPECTED[red_cycles]
        require(row["formula"]["variables"] == expected_variables
                and row["formula"]["clauses"] == expected_clauses
                and row["formula"]["sha256"] == expected_sha,
                "published formula record differs")
        wanted_status = "excluded" if red_cycles in EXCLUDED else "open"
        require(row["status"] == wanted_status, "published case status differs")
        if red_cycles in EXCLUDED:
            proof_bytes, proof_sha, rat = PROOFS[red_cycles]
            require(row["proof"] == {"bytes": proof_bytes, "sha256": proof_sha}
                    and row["replay"]["verified"]
                    and row["replay"]["rat_core_lemmas"] == rat,
                    "published proof record differs")
        else:
            require(row["solver_code"] == 0
                    and "s UNKNOWN" in (proof_work / f"r{red_cycles}.solve.log").read_text(),
                    "open case is not explicit UNKNOWN")
    return {"published_result": file_info(path), "six_case_cover": True,
            "excluded_counts": list(EXCLUDED), "open_counts": list(OPEN)}


def replay(red_cycles: int, formula: Path, proof: Path,
           checker: Path, work: Path) -> dict[str, object]:
    expected_bytes, expected_sha, expected_rat = PROOFS[red_cycles]
    info = file_info(proof)
    require(info == {"bytes": expected_bytes, "sha256": expected_sha},
            f"proof digest differs for r={red_cycles}")
    log = work / f"independent_replay_r{red_cycles}.log"
    with log.open("w") as output:
        process = subprocess.run(
            [str(checker), str(formula), str(proof), "-t", "300"],
            stdout=output, stderr=subprocess.STDOUT, timeout=360,
        )
    text = log.read_text()
    require(process.returncode == 0 and "s VERIFIED" in text,
            f"DRAT replay failed for r={red_cycles}")
    match = re.search(r"(\d+) RAT lemmas in core", text)
    require(match is not None and int(match.group(1)) == expected_rat,
            f"RAT core count differs for r={red_cycles}")
    return {"red_cycles": red_cycles, "proof": info,
            "drat_trim_verified": True, "rat_core_lemmas": expected_rat}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--formula-work", required=True, type=Path)
    parser.add_argument("--proof-work", required=True, type=Path)
    parser.add_argument("--drat-trim", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    formula_work = args.formula_work.resolve()
    proof_work = args.proof_work.resolve()
    checker = args.drat_trim.resolve()
    require(file_info(checker)["sha256"] == DRAT_TRIM_SHA256,
            "unexpected drat-trim binary")

    report: dict[str, object] = {
        "manifest": manifest_audit(source, proof_work),
        "local_arithmetic": local_arithmetic(),
        "counter_semantics": counter_semantics(),
        "normalization": normalization_audit(),
        "drat_trim": file_info(checker),
        "formula_audits": [],
        "proof_replays": [],
    }
    for red_cycles in range(6):
        formula = formula_work / f"r{red_cycles}.cnf"
        report["formula_audits"].append(compare_formula(red_cycles, formula))
        print(f"FORMULA r={red_cycles} exact clean-room match", flush=True)
        if red_cycles in EXCLUDED:
            report["proof_replays"].append(
                replay(red_cycles, formula, proof_work / f"r{red_cycles}.drat",
                       checker, args.report.parent)
            )
            print(f"PROOF r={red_cycles} general DRAT verified", flush=True)
    report["excluded_counts"] = list(EXCLUDED)
    report["open_counts"] = list(OPEN)
    report["all_claimed_exclusions_verified"] = True
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS eleven-cycle review: r=0,1,2,5 excluded; r=3,4 open", flush=True)


if __name__ == "__main__":
    main()

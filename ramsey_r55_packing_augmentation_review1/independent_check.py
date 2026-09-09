#!/usr/bin/env python3
"""Independent exact audit of the h4035 packing-exchange reduction.

This checker imports no target module.  It counts compatible intersection
masks as unordered multisets with explicit permutation multiplicities (rather
than using the producer's union-state recurrence), reconstructs the carrier
from h3887's public task registry, and checks the target transport program as
a black box against a specification-level encoder and verifier.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools as it
import json
import math
import subprocess
import sys
import tempfile
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "ramsey_r55_packing_augmentation"
CARRIER = REPOSITORY / "ramsey_r55_maximal_block_order"
DEGREE = REPOSITORY / "ramsey_r55_q8_degree_carrier"

TARGET_EXPECTED_SHA256 = "98ed5c3d23ba0b76ee23e22b51ca81400a70379f09a5eec5f515ead2f02272f6"
TARGET_MANIFEST_SHA256 = "8953c27c830920d51fa3ad839a03185489ba7f0b3395ff5389cf31c7c3f2a2e6"
TARGET_PINS_SHA256 = "a158ee93a85080fbbc62d01d71986b2217658941815027617bbaea037644c7aa"
CARRIER_TASKS_SHA256 = "657e2585f5fce56abc4bb7806bd093d1978c39ea791b9d02695ed19e22ef1f4c"
DEGREE_EXPECTED_SHA256 = "b652d2e5fb5a30fbfd7e3236e50aa7f9c9bff22188d1bf8967cc4d2138d7416c"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def as_fraction(value: dict[str, int]) -> Fraction:
    return Fraction(value["numerator"], value["denominator"])


def fraction_dict(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def decimal_string(value: Fraction, places: int = 16) -> str:
    with localcontext() as context:
        context.prec = places + 20
        result = Decimal(value.numerator) / Decimal(value.denominator)
        return format(result, f".{places}f")


def audit_target_manifest() -> None:
    require(sha256(TARGET / "MANIFEST.json") == TARGET_MANIFEST_SHA256,
            "target manifest hash")
    manifest = json.loads((TARGET / "MANIFEST.json").read_text())
    for name, digest in manifest.items():
        require(sha256(TARGET / name) == digest,
                "target manifest member: " + name)


PAIRS = tuple(sum(1 << j for j in pair)
              for pair in it.combinations(range(4), 2))


def conflict(masks: tuple[int, ...]) -> bool:
    """Whether two distinct selected edges complete complementary pairs."""
    return any((masks[i] & pair) == pair
               and (masks[j] & (15 ^ pair)) == (15 ^ pair)
               for i in range(len(masks))
               for j in range(i + 1, len(masks))
               for pair in PAIRS)


def independent_mask_counts() -> tuple[list[int], list[int], int]:
    """Count ordered endpoint-star tuples via unordered mask multisets."""
    weights = [0] * 15
    for left in range(15):
        for right in range(15):
            weights[left & right] += 1
    require(weights == [3 ** (4 - mask.bit_count()) - 2
                        for mask in range(15)], "intersection weights")

    allowed = []
    checked = 0
    for size in range(1, 5):
        total = 0
        for masks in it.combinations_with_replacement(range(15), size):
            checked += 1
            if conflict(masks):
                continue
            frequencies = Counter(masks)
            multiplicity = math.factorial(size)
            for count in frequencies.values():
                multiplicity //= math.factorial(count)
            ways = multiplicity
            for mask in masks:
                ways *= weights[mask]
            total += ways
        allowed.append(total)

    # A direct endpoint-star exhaustion independently checks the m=2 layer.
    literal_two = sum(not conflict((a & b, c & d))
                      for a, b, c, d in it.product(range(15), repeat=4))
    require(literal_two == allowed[1], "literal two-edge count")
    return weights, allowed, checked


def carrier_formula(q: int, r: int, n: int) -> int:
    red_children = r - 1
    blue_children = q - r
    return (math.comb(1998 + red_children - 1, red_children)
            * math.comb(1931 + blue_children - 1, blue_children)
            * 37823 ** (math.comb(red_children, 2)
                        + math.comb(blue_children, 2))
            * 35714 ** (red_children * blue_children)
            * 15 ** (q * n))


def audit_registry() -> tuple[list[dict], int]:
    require(sha256(CARRIER / "TASKS.json") == CARRIER_TASKS_SHA256,
            "h3887 task registry hash")
    source = json.loads((CARRIER / "TASKS.json").read_text())
    require(source["format"] == "bo1" and source["macro_classes"] == 18,
            "h3887 registry header")
    cursor = 0
    task_count = 0
    projected = []
    for row in source["classes"]:
        q, r, n = row["q"], row["r"], row["n"]
        require(n == 43 - 4 * q and 7 <= q <= 10 and 5 <= r <= q,
                "h3887 class identity")
        require(row["core_start"] == 0 and row["core_stop"] > 0,
                "h3887 core interval")
        per_task = carrier_formula(q, r, n)
        require(row["per_task"] == per_task, "h3887 per-task count")
        require(row["code_start"] == cursor, "h3887 code contiguity")
        cursor += row["core_stop"] * per_task
        require(row["code_stop"] == cursor, "h3887 code interval")
        task_count += row["core_stop"]
        projected.append({"q": q, "r": r, "n": n,
                          "core_count": row["core_stop"],
                          "per_task": per_task})
    require(cursor == source["P"], "h3887 global carrier")
    require(task_count == source["tasks"] == 2_189_178,
            "h3887 task count")
    return projected, cursor


def reconstruct_counts(classes: list[dict], allowed: list[int]) -> dict:
    probabilities = {
        8: Fraction(allowed[3], 15 ** 8),
        9: Fraction(allowed[1], 15 ** 4),
    }
    rows = []
    old = 0
    new = 0
    old_by_q: dict[int, int] = Counter()
    new_by_q: dict[int, int] = Counter()
    for source in classes:
        q, r = source["q"], source["r"]
        fraction = probabilities[q] ** r if q in probabilities else Fraction(1)
        retained = source["per_task"] * fraction
        require(retained.denominator == 1, "nonintegral retained task")
        row = {"q": q, "r": r, "core_count": source["core_count"],
               "per_task": source["per_task"],
               "retained_per_task": retained.numerator,
               "retained_fraction": fraction_dict(fraction),
               "clauses_per_task": (36 * r if q == 8
                                    else 6 * r if q == 9 else 0)}
        rows.append(row)
        old += source["core_count"] * source["per_task"]
        new += source["core_count"] * retained.numerator
        old_by_q[q] += source["core_count"] * source["per_task"]
        new_by_q[q] += source["core_count"] * retained.numerator

    require(sha256(DEGREE / "EXPECTED.json") == DEGREE_EXPECTED_SHA256,
            "h4029 degree certificate hash")
    degree = json.loads((DEGREE / "EXPECTED.json").read_text())
    degree_bounds = {row["r"]: as_fraction(row["sorted_fraction_bound"])
                     for row in degree["ordered_transfer"]["classes"]}
    old_composite = Fraction(0)
    new_composite = Fraction(0)
    degree_stricter = {}
    for source in classes:
        q, r = source["q"], source["r"]
        alive = source["core_count"] - (518 if (q, r) == (7, 5) else 0)
        prior = degree_bounds[r] if q == 8 else Fraction(1)
        packing = probabilities[q] ** r if q in probabilities else Fraction(1)
        if q == 8:
            degree_stricter[r] = prior < packing
        old_composite += alive * source["per_task"] * prior
        new_composite += alive * source["per_task"] * min(prior, packing)

    affected_tasks = sum(row["core_count"] for row in classes
                         if row["q"] in (8, 9))
    q_removed = {q: Fraction(old_by_q[q] - new_by_q[q], old_by_q[q])
                 for q in (8, 9)}
    return {
        "rows": rows,
        "old": old,
        "new": new,
        "removed": Fraction(old - new, old),
        "old_composite": old_composite,
        "new_composite": new_composite,
        "composite_decrease": Fraction(old_composite - new_composite,
                                        old_composite),
        "affected_tasks": affected_tasks,
        "remaining_tasks": sum(row["core_count"] for row in classes) - 518,
        "q_removed": q_removed,
        "degree_stricter": degree_stricter,
        "degree_bounds": degree_bounds,
    }


def audit_expected(expected: dict, rebuilt: dict, allowed: list[int],
                   pins: dict, classes: list[dict], old: int) -> None:
    require([level["allowed"] for level in expected["levels"]] == allowed,
            "selected-edge counts")
    require([level["total"] for level in expected["levels"]]
            == [15 ** (2 * size) for size in range(1, 5)],
            "selected-edge totals")
    require(expected["classes"] == rebuilt["rows"], "class table")
    require(expected["old_carrier"] == rebuilt["old"] == old,
            "old carrier")
    require(expected["new_carrier"] == rebuilt["new"], "new carrier")
    require(as_fraction(expected["removed_fraction"]) == rebuilt["removed"],
            "global removed fraction")
    require(as_fraction(expected["old_composite_upper"])
            == rebuilt["old_composite"], "old composite envelope")
    require(as_fraction(expected["new_composite_upper"])
            == rebuilt["new_composite"], "new composite envelope")
    require(as_fraction(expected["composite_upper_decrease"])
            == rebuilt["composite_decrease"], "composite decrease")
    require(expected["affected_tasks"] == rebuilt["affected_tasks"]
            == 2_187_234, "affected task count")
    require(expected["remaining_whole_tasks"] == rebuilt["remaining_tasks"]
            == 2_188_660, "remaining whole tasks")
    require(expected["gate"] == "PASS" and 20 * rebuilt["removed"] > 1,
            "strict five-percent gate")
    require(expected["new_task_decisions"] == 0
            and expected["target_found"] is False, "claim status")
    require(pins["classes"] == classes, "target carrier pins")
    require(pins["old_carrier"] == old, "target old-carrier pin")
    require({int(r): as_fraction(value)
             for r, value in pins["q8_degree_bounds"].items()}
            == rebuilt["degree_bounds"], "target h4029 pins")
    require(all(rebuilt["degree_stricter"].values()),
            "degree bound not stricter in a q8 class")


def red_edges(obj: dict) -> set[tuple[int, int]]:
    n = obj["n"]
    word = int(obj["red_hex"], 16)
    require(word < 1 << math.comb(n, 2), "graph word padding")
    return {pair for bit, pair in enumerate(it.combinations(range(n), 2))
            if word >> bit & 1}


def edge(edges: set[tuple[int, int]], u: int, v: int) -> bool:
    return tuple(sorted((u, v))) in edges


def mono(edges: set[tuple[int, int]], vertices: list[int] | tuple[int, ...],
         color: bool) -> bool:
    return all(edge(edges, u, v) == color
               for u, v in it.combinations(vertices, 2))


def validate_packing(obj: dict) -> set[tuple[int, int]]:
    n, blocks, core, r = obj["n"], obj["blocks"], obj["core"], obj["r"]
    require(type(n) is int and 8 <= n <= 43, "packing order")
    require(type(r) is int and 1 <= r <= len(blocks), "packing red count")
    vertices = [v for block in blocks for v in block] + core
    require(all(type(v) is int for v in vertices)
            and all(len(block) == 4 for block in blocks)
            and sorted(vertices) == list(range(n)), "packing partition")
    edges = red_edges(obj)
    require(all(mono(edges, block, i < r)
                for i, block in enumerate(blocks)), "packing colors")
    require(all(not mono(edges, four, color)
                for four in it.combinations(core, 4)
                for color in (False, True)), "Ramsey(4,4) core")
    remainder = [v for block in blocks[r:] for v in block] + core
    require(all(not mono(edges, four, True)
                for four in it.combinations(remainder, 4)), "red maximality")
    return edges


def greedy_matching(edges: set[tuple[int, int]], core: list[int],
                    needed: int) -> list[tuple[int, int]]:
    unused = set(core)
    matching = []
    for u, v in it.combinations(sorted(core), 2):
        if u in unused and v in unused and edge(edges, u, v):
            matching.append((u, v))
            unused.remove(u)
            unused.remove(v)
    require(len(matching) >= needed, "selected matching too short")
    require(all(not edge(edges, u, v) for u, v in it.combinations(unused, 2)),
            "greedy matching is not maximal")
    require(len(unused) <= 3, "Ramsey core left four unmatched vertices")
    return matching[:needed]


def expected_clauses(obj: dict) -> list[list[int]]:
    edges = validate_packing(obj)
    q = len(obj["blocks"])
    needed = {8: 4, 9: 2}[q]
    matching = greedy_matching(edges, obj["core"], needed)
    variables = {pair: i + 1
                 for i, pair in enumerate(it.combinations(range(43), 2))}
    result = []
    for block in obj["blocks"][:obj["r"]]:
        for first, second in it.combinations(matching, 2):
            for side in it.combinations(block, 2):
                complement = [v for v in block if v not in side]
                result.append([-variables[tuple(sorted((u, v)))]
                               for part, match_edge in ((side, first),
                                                        (complement, second))
                               for u in part for v in match_edge])
    return result


def graph6_edges(word: str) -> set[tuple[int, int]]:
    require(ord(word[0]) - 63 == 11, "fixture graph6 order")
    bits = "".join(format(ord(character) - 63, "06b")
                   for character in word[1:])
    pairs = ((i, j) for j in range(1, 11) for i in range(j))
    return {pair for bit, pair in enumerate(pairs) if bits[bit] == "1"}


def fixture(q: int, r: int, inject_block: int | None = None) -> dict:
    catalog_fixture = json.loads((TARGET / "FIXTURE.json").read_text())
    core_graph = graph6_edges(catalog_fixture["graph6"])
    core_order = 43 - 4 * q
    edges = {pair for block in range(r)
             for pair in it.combinations(range(4 * block, 4 * block + 4), 2)}
    edges |= {(4 * q + u, 4 * q + v) for u, v in core_graph
              if v < core_order}
    obj = {"n": 43,
           "blocks": [list(range(4 * i, 4 * i + 4)) for i in range(q)],
           "core": list(range(4 * q, 43)), "r": r}

    def encode() -> str:
        value = sum((pair in edges) << bit
                    for bit, pair in enumerate(it.combinations(range(43), 2)))
        return format(value, "0226x")

    obj["red_hex"] = encode()
    current = validate_packing(obj)
    if inject_block is not None:
        matching = greedy_matching(current, obj["core"], {8: 4, 9: 2}[q])
        block = obj["blocks"][inject_block]
        for part, match_edge in ((block[:2], matching[0]),
                                 (block[2:], matching[1])):
            edges |= {tuple(sorted((u, v))) for u in part for v in match_edge}
        obj["red_hex"] = encode()
        validate_packing(obj)
    return obj


def run_target_transport(source: dict, mode: str, work: Path) -> dict:
    input_path = work / "input.json"
    input_path.write_text(json.dumps(source, sort_keys=True) + "\n")
    command = [sys.executable, "-B", str(TARGET / "transport.py"),
               str(input_path)]
    if mode == "clauses":
        command.append("--clauses")
    process = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(process.stdout)


def verify_certificate(source: dict, certificate: dict) -> int:
    require(certificate["status"]
            == "PACKING_TRANSPORT_NEEDS_CATALOG_AND_ROOT_ORDER",
            "transport status")
    binding = hashlib.sha256(json.dumps(source, sort_keys=True,
                                       separators=(",", ":")).encode()).hexdigest()
    require(certificate["source_sha256"] == binding, "transport binding")
    destination = certificate["output"]
    old_edges = validate_packing(source)
    new_edges = validate_packing(destination)
    permutation = certificate["new_to_old"]
    n = source["n"]
    require(destination["n"] == n and sorted(permutation) == list(range(n)),
            "transport permutation")
    require(all(edge(new_edges, i, j)
                == edge(old_edges, permutation[i], permutation[j])
                for i, j in it.combinations(range(n), 2)),
            "transported edge mismatch")
    old_blocks = source["blocks"]
    transported_blocks = [frozenset(permutation[v] for v in block)
                          for block in destination["blocks"]]
    replaced = certificate["replaced_block"]
    new_blocks = [frozenset(block)
                  for block in certificate["new_blocks_old_labels"]]
    require(0 <= replaced < source["r"] and len(new_blocks) == 2
            and all(len(block) == 4 for block in new_blocks)
            and not (new_blocks[0] & new_blocks[1]), "replacement blocks")
    expected = ([frozenset(block) for i, block in enumerate(old_blocks[:source["r"]])
                 if i != replaced] + new_blocks
                + [frozenset(block) for block in old_blocks[source["r"]:]])
    require(transported_blocks == expected, "transported packing")
    old_block = set(old_blocks[replaced])
    require(all(len(set(block) & old_block) == 2 for block in new_blocks),
            "replacement split")
    consumed = set().union(*map(set, new_blocks)) - old_block
    require(len(consumed) == 4 and consumed <= set(source["core"]),
            "consumed core vertices")
    require(destination["r"] == source["r"] + 1
            and len(destination["blocks"]) == len(old_blocks) + 1,
            "packing statistic increase")
    require({permutation[v] for v in destination["core"]}
            == set(source["core"]) - consumed, "transported core")
    return math.comb(n, 2)


def audit_transport(scratch: Path) -> dict:
    clauses_checked = 0
    transfers = 0
    edges_checked = 0
    corruptions = 0
    with tempfile.TemporaryDirectory(prefix="h4035-review-", dir=scratch) as name:
        work = Path(name)
        for q in (8, 9):
            for r in range(5, q + 1):
                source = fixture(q, r)
                result = run_target_transport(source, "clauses", work)
                expected = expected_clauses(source)
                require(result["scope"]
                        == "NEW_GLOBAL_COVER_ONLY_NOT_A_RAMSEY_IMPLICATE",
                        "clause scope")
                require(result["clauses"] == expected, "black-box clauses")
                clauses_checked += len(expected)
                for selected_block in (0, r - 1):
                    injected = fixture(q, r, selected_block)
                    certificate = run_target_transport(injected, "step", work)
                    edges_checked += verify_certificate(injected, certificate)
                    transfers += 1
                    bad = copy.deepcopy(certificate)
                    bad["new_to_old"][0] = bad["new_to_old"][1]
                    try:
                        verify_certificate(injected, bad)
                    except (ValueError, KeyError, TypeError):
                        corruptions += 1
                    else:
                        raise ValueError("accepted corrupt transport")
    return {"macro_classes": 9, "clauses_compared": clauses_checked,
            "clause_literals_compared": 8 * clauses_checked,
            "transports_verified": transfers,
            "physical_edges_verified": edges_checked,
            "corrupt_transports_rejected": corruptions}


def expected_controls(expected: dict, rebuilt: dict, allowed: list[int],
                      pins: dict, classes: list[dict], old: int) -> list[str]:
    controls = {
        "four_edge_count": lambda data: data["levels"][3].__setitem__(
            "allowed", data["levels"][3]["allowed"] + 1),
        "retained_class": lambda data: data["classes"][3].__setitem__(
            "retained_per_task", data["classes"][3]["retained_per_task"] + 1),
        "global_carrier": lambda data: data.__setitem__(
            "new_carrier", data["new_carrier"] + 1),
        "composite_bound": lambda data: data["new_composite_upper"].__setitem__(
            "numerator", data["new_composite_upper"]["numerator"] + 1),
    }
    rejected = []
    for name, mutate in controls.items():
        altered = copy.deepcopy(expected)
        mutate(altered)
        try:
            audit_expected(altered, rebuilt, allowed, pins, classes, old)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("accepted corrupt expected result: " + name)
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch", type=Path, required=True,
                        help="existing directory for small transient fixtures")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    require(args.scratch.is_dir(), "scratch directory does not exist")
    audit_target_manifest()
    require(sha256(TARGET / "EXPECTED.json") == TARGET_EXPECTED_SHA256,
            "target expected hash")
    require(sha256(TARGET / "PINS.json") == TARGET_PINS_SHA256,
            "target pins hash")
    expected = json.loads((TARGET / "EXPECTED.json").read_text())
    pins = json.loads((TARGET / "PINS.json").read_text())
    weights, allowed, multisets_checked = independent_mask_counts()
    classes, old = audit_registry()
    rebuilt = reconstruct_counts(classes, allowed)
    audit_expected(expected, rebuilt, allowed, pins, classes, old)
    transport = audit_transport(args.scratch)
    controls = expected_controls(expected, rebuilt, allowed, pins, classes, old)
    receipt = {
        "status": "INDEPENDENT_H4035_ACCEPT",
        "target_expected_sha256": TARGET_EXPECTED_SHA256,
        "h3887_tasks_sha256": CARRIER_TASKS_SHA256,
        "h4029_expected_sha256": DEGREE_EXPECTED_SHA256,
        "intersection_weights": weights,
        "allowed_endpoint_tuples": {str(i + 1): value
                                    for i, value in enumerate(allowed)},
        "unordered_mask_multisets_checked": multisets_checked,
        "literal_two_edge_star_tuples_checked": 15 ** 4,
        "macro_classes_reconstructed": len(classes),
        "affected_tasks": rebuilt["affected_tasks"],
        "remaining_whole_tasks": rebuilt["remaining_tasks"],
        "removed_fraction_decimal": decimal_string(rebuilt["removed"]),
        "q8_removed_fraction_decimal": decimal_string(rebuilt["q_removed"][8]),
        "q9_removed_fraction_decimal": decimal_string(rebuilt["q_removed"][9]),
        "q8_degree_bound_stricter_in_all_classes":
            all(rebuilt["degree_stricter"].values()),
        "composite_decrease_decimal":
            decimal_string(rebuilt["composite_decrease"]),
        "transport": transport,
        "rejected_numeric_controls": controls,
        "new_task_decisions": 0,
        "target_found": False,
    }
    if args.check_expected:
        pinned = json.loads((HERE / "EXPECTED.json").read_text())
        require(receipt == pinned, "review receipt differs from pin")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

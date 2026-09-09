#!/usr/bin/env python3
"""Third exact audit of h4041's zero direct fixed-prefix effect.

No target module is imported.  The 4x3 core words are reconstructed as
multisets of row types modulo the six column actions, rather than by either
supplied canonicalizer.  The h4021 interface is invoked only as a black box.
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
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "ramsey_r55_h4021_q10_carrier_effect"
Q10 = REPOSITORY / "ramsey_r55_q10_recovered_cube_refutations"
CUT = REPOSITORY / "ramsey_r55_structural_cut_interface"

TARGET_MANIFEST_SHA256 = "81b09558c6e50fb60db90075bd6fb823b16c5e8c7dc1e435eaf4b763db48b1bb"
TARGET_EXPECTED_SHA256 = "d90d691dd0462d2df8d768862eb06dbbd36fb9fea4c48564eed56f21013d803c"
Q10_TASKS_SHA256 = "349b2307a16696323b927a546ea6b365668fb09a01532f91480a0093950fb548"
Q10_WORDS_SHA256 = "f0fbe833fb976c89c3d5d20782dc5f595f55881112687f8e208a7dfea4e79ba5"
CUT_TEMPLATE_SHA256 = "672c8fed249efca052b21ed7b4cb6a01364977d5074edf1f252e3b8d055d0d99"
CUT_INTERFACE_SHA256 = "bc5161252c0cae025f6b217d21440e39a989dc9d0189d0e2f5c0ff9ef4011dca"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_hashes() -> None:
    require(sha256(TARGET / "MANIFEST.json") == TARGET_MANIFEST_SHA256,
            "target manifest hash")
    manifest = json.loads((TARGET / "MANIFEST.json").read_text())
    for name, digest in manifest.items():
        require(sha256(TARGET / name) == digest,
                "target manifest member: " + name)
    expected = {
        Q10 / "TASKS.json": Q10_TASKS_SHA256,
        Q10 / "CORE_WORDS.json": Q10_WORDS_SHA256,
        CUT / "TEMPLATE.json": CUT_TEMPLATE_SHA256,
        CUT / "interface.py": CUT_INTERFACE_SHA256,
    }
    for path, digest in expected.items():
        require(sha256(path) == digest, "dependency hash: " + str(path))


def permute_row(row: int, columns: tuple[int, ...]) -> int:
    return sum(((row >> old) & 1) << new
               for new, old in enumerate(columns))


def encode_row_multiset(rows: list[int] | tuple[int, ...]) -> int:
    """Use decreasing row values in low-to-high three-bit chunks."""
    return sum(row << (3 * index)
               for index, row in enumerate(sorted(rows, reverse=True)))


def canonical_words() -> tuple[list[int], int]:
    """Quotient row permutations first, then the six column actions."""
    representatives = set()
    admissible_multisets = 0
    for rows in it.combinations_with_replacement(range(8), 4):
        # An all-one column is the forbidden red extension of the root K4.
        if any(all((row >> column) & 1 for row in rows)
               for column in range(3)):
            continue
        admissible_multisets += 1
        images = [encode_row_multiset(
            [permute_row(row, columns) for row in rows])
            for columns in it.permutations(range(3))]
        representatives.add(min(images))
    words = sorted(representatives)
    require(admissible_multisets == 239, "admissible row-multiset count")
    require(len(words) == 65, "S4 x S3 orbit count")
    return words, admissible_multisets


def physical_maps() -> tuple[dict[tuple[int, int], int],
                             dict[int, tuple[int, int]]]:
    forward = {}
    next_variable = 2
    for u, v in it.combinations(range(43), 2):
        if u < 40 and u // 4 != v // 4:
            forward[u, v] = next_variable
            next_variable += 1
    require(next_variable == 842, "q10 physical variable count")
    reverse = {variable: edge for edge, variable in forward.items()}
    require(len(reverse) == len(forward), "injective variable map")
    require({variable: reverse[variable]
             for variable in (121, 139, 148, 155, 156)} == {
                 121: (3, 6), 139: (3, 24), 148: (3, 33),
                 155: (3, 40), 156: (3, 41)}, "physical variable pins")
    return forward, reverse


def reconstruct_tasks(words: list[int],
                      variables: dict[tuple[int, int], int]) -> list[dict]:
    contacts = [variables[row, column] for row in range(4)
                for column in (40, 41, 42)]
    branches = {
        "d20-22": (variables[3, 24], variables[3, 41]),
        "d22-20": (variables[3, 6], variables[3, 40]),
    }
    output = []
    for branch, (pivot, core_literal) in branches.items():
        for index, word in enumerate(words):
            contact_assignment = [
                variable if word >> bit & 1 else -variable
                for bit, variable in enumerate(contacts)]
            for pivot_bit in (0, 1):
                cube = contact_assignment + [pivot if pivot_bit else -pivot]
                closed = not pivot_bit and -core_literal in cube
                output.append({
                    "id": f"{branch}-w{index:02d}-p{pivot_bit}",
                    "branch": branch,
                    "word": word,
                    "cube": cube,
                    "status": "CERTIFIED_UNSAT" if closed else "UNKNOWN",
                    "certificate": (("d20-22-strong"
                                     if branch == "d20-22"
                                     else "d22-20-corezero")
                                    if closed else None),
                    "forced_residual_literal": (
                        variables[3, 33]
                        if branch == "d22-20" and not pivot_bit and not closed
                        else None),
                })
    require(len(output) == 260 and len({row["id"] for row in output}) == 260,
            "complete task product")
    return output


def fixed_prefix(task: dict, reverse: dict[int, tuple[int, int]]) \
        -> dict[tuple[int, int], int]:
    fixed = {}
    for start in range(0, 40, 4):
        for edge in it.combinations(range(start, start + 4), 2):
            fixed[edge] = 1
    for edge in it.combinations(range(40, 43), 2):
        fixed[edge] = 0
    literals = list(task["cube"])
    if task["forced_residual_literal"] is not None:
        literals.append(task["forced_residual_literal"])
    for literal in literals:
        require(abs(literal) in reverse, "unknown physical variable")
        edge = reverse[abs(literal)]
        color = int(literal > 0)
        require(edge not in fixed or fixed[edge] == color,
                "inconsistent fixed prefix")
        fixed[edge] = color
    return fixed


def audit_template(template: dict) -> None:
    require(template["n"] == 43 and template["root"] == 0,
            "template order and root")
    require([len(module) for module in template["modules"]] == [4, 4, 4, 3, 3]
            and sorted(sum(template["modules"], [])) == list(range(1, 19)),
            "template module partition")
    fixed = template["fixed"]
    pairs = [tuple(sorted(row[:2])) for row in fixed]
    require(len(fixed) == len(set(pairs)) == 147,
            "147 distinct template pairs")
    require(all(0 <= u < v < 43 and color in (0, 1)
                for u, v, color in fixed), "template fixed rows")
    root_rows = [row for row in fixed if 0 in row[:2]]
    require(len(root_rows) == 18 and all(row[2] == 1 for row in root_rows),
            "18-edge red template root star")


def expected_result(tasks: list[dict], template: dict,
                    reverse: dict[int, tuple[int, int]]) -> tuple[dict, list[dict]]:
    audit_template(template)
    unknown = [task for task in tasks if task["status"] == "UNKNOWN"]
    require(len(tasks) == 260 and len(unknown) == 161,
            "complete imported task scope")
    require(Counter(task["status"] for task in tasks)
            == {"CERTIFIED_UNSAT": 99, "UNKNOWN": 161},
            "h3987 ledger status partition")

    histogram = Counter()
    branches = Counter()
    fixed_counts = Counter()
    root_color_pairs = 0
    per_task = []
    for task in unknown:
        fixed = fixed_prefix(task, reverse)
        degrees = [[0, 0] for _ in range(43)]
        for (u, v), color in fixed.items():
            degrees[u][color] += 1
            degrees[v][color] += 1
        maximum_red = max(row[1] for row in degrees)
        maximum_blue = max(row[0] for row in degrees)
        eligible = sum(row[color] >= 18
                       for row in degrees for color in (0, 1))
        root_color_pairs += eligible
        histogram[maximum_red, maximum_blue, len(fixed)] += 1
        branches[task["branch"]] += 1
        fixed_counts[len(fixed)] += 1
        per_task.append({
            "id": task["id"],
            "branch": task["branch"],
            "fixed_edges": len(fixed),
            "max_fixed_red_degree": maximum_red,
            "max_fixed_blue_degree": maximum_blue,
            "eligible_root_color_pairs": eligible,
            "forced_residual_literal": task["forced_residual_literal"],
        })
    require(root_color_pairs == 0, "nonzero eligible root/color pair")
    require(branches == {"d20-22": 67, "d22-20": 94},
            "unknown branch partition")
    require(fixed_counts == {76: 132, 77: 29}, "fixed-edge histogram")
    maximum_red = max(row[0] for row in histogram)
    maximum_blue = max(row[1] for row in histogram)
    require((maximum_red, maximum_blue) == (6, 6), "degree maxima")
    per_task_embeddings = 2 * math.perm(43, 19)
    result = {
        "status": "CERTIFIED_ZERO_DIRECT_H4021_Q10_PREFIX_CLOSURES",
        "scope": "all h3987 tasks whose ledger status is UNKNOWN",
        "interface": {
            "fixed_template_edges": 147,
            "root_star_edges": 18,
            "necessary_fixed_same_color_root_degree_for_conflict": 18,
        },
        "carrier": {
            "all_tasks": 260,
            "previously_certified_unsat": 99,
            "unknown_tasks_checked": 161,
            "unknown_by_branch": dict(sorted(branches.items())),
            "fixed_edge_count_histogram": {
                str(key): fixed_counts[key] for key in sorted(fixed_counts)},
            "root_color_pairs_checked": 161 * 43 * 2,
            "eligible_root_color_pairs": 0,
            "ordered_interface_embeddings_covered": per_task_embeddings,
            "direct_conflict_embeddings": 0,
            "new_task_closures": 0,
            "remaining_unknown_tasks": 161,
            "maximum_fixed_red_degree": maximum_red,
            "maximum_fixed_blue_degree": maximum_blue,
        },
        "degree_histogram": [
            {"max_fixed_red_degree": red,
             "max_fixed_blue_degree": blue,
             "fixed_edges": count,
             "tasks": histogram[red, blue, count]}
            for red, blue, count in sorted(histogram)
        ],
        "carrier_task_digest_sha256": hashlib.sha256(
            json.dumps(per_task, separators=(",", ":"),
                       sort_keys=True).encode()).hexdigest(),
        "limitations": [
            "No h3987 UNKNOWN task is decided.",
            "The result concerns h4021 CONFLICT under the fixed q10 prefix only.",
            "Nonempty h4021 clauses may still prune later SAT search.",
            "No claim is made about templates completed by currently free edges.",
            "No good43 graph is produced.",
        ],
    }
    return result, per_task


def target_clause(template: dict, vertices: list[int], color: int) \
        -> list[list[int]]:
    result = []
    for u, v, prescribed in template["fixed"]:
        physical = sorted((vertices[u], vertices[v]))
        literal_truth = 1 - (prescribed if color else 1 - prescribed)
        result.append([*physical, literal_truth])
    return result


def complete_mapping(clause: list[list[int]], root: int, mode: str) -> dict:
    truth = {(u, v): value for u, v, value in clause}
    root_pair = next((u, v) for u, v, value in clause
                     if root in (u, v))
    entries = []
    next_variable = 10_000
    for pair in it.combinations(range(43), 2):
        if pair not in truth:
            entries.append([*pair, "var", next_variable])
            next_variable += 1
        elif mode == "one_free" and pair == root_pair:
            entries.append([*pair, "var", next_variable])
            next_variable += 1
        elif mode == "tautology" and pair == root_pair:
            entries.append([*pair, "fixed", truth[pair]])
        else:
            entries.append([*pair, "fixed", 1 - truth[pair]])
    return {"edges": entries}


def invoke_interface(vertices: list[int], color: int, output: Path,
                     mapping: Path | None = None) -> dict:
    command = [sys.executable, "-B", str(CUT / "interface.py"),
               "--vertices", ",".join(map(str, vertices)),
               "--color", str(color), "--out", str(output)]
    if mapping is not None:
        command.extend(["--map", str(mapping)])
    subprocess.run(command, check=True, capture_output=True)
    return json.loads(output.read_text())


def black_box_interface_audit(template: dict, scratch: Path) -> dict:
    embeddings = [
        list(range(19)),
        list(range(42, 23, -1)),
        [(7 * index + 3) % 43 for index in range(19)],
    ]
    emissions = 0
    statuses = Counter()
    with tempfile.TemporaryDirectory(prefix="h4041-review-", dir=scratch) as name:
        work = Path(name)
        for embedding_index, vertices in enumerate(embeddings):
            require(len(set(vertices)) == 19, "test embedding injectivity")
            for color in (0, 1):
                output = work / f"emission-{embedding_index}-{color}.json"
                emitted = invoke_interface(vertices, color, output)
                expected = target_clause(template, vertices, color)
                require(emitted["n"] == 43 and emitted["vertices"] == vertices
                        and emitted["color"] == color,
                        "black-box emission identity")
                require(emitted["physical_clause"] == expected,
                        "black-box physical clause")
                require(len(expected) == len({(u, v) for u, v, _ in expected})
                        == 147, "black-box clause width")
                physical_root = vertices[0]
                root_rows = [row for row in expected
                             if physical_root in row[:2]]
                require(len(root_rows) == 18
                        and {1 - truth for _, _, truth in root_rows} == {color},
                        "black-box selected-color root star")
                emissions += 1

        # Exercise all receiver statuses on the nontrivial affine embedding.
        vertices = embeddings[-1]
        for color in (0, 1):
            expected = target_clause(template, vertices, color)
            for mode, status in (("conflict", "CONFLICT"),
                                 ("one_free", "CLAUSE"),
                                 ("tautology", "TAUTOLOGY")):
                mapping_path = work / f"mapping-{color}-{mode}.json"
                mapping_path.write_text(json.dumps(
                    complete_mapping(expected, vertices[0], mode)))
                output = work / f"receiver-{color}-{mode}.json"
                emitted = invoke_interface(vertices, color, output, mapping_path)
                receiver = emitted["receiver"]
                require(receiver["status"] == status,
                        "black-box receiver status")
                if status == "CLAUSE":
                    require(len(receiver["clause"]) == 1,
                            "one-literal receiver control")
                statuses[status] += 1
    return {"emissions_compared": emissions,
            "physical_clause_rows_compared": emissions * 147,
            "receiver_status_controls": dict(sorted(statuses.items()))}


def audit_expected(actual: dict, rebuilt: dict) -> None:
    require(actual == rebuilt, "target expected result differs")


def corruption_controls(expected: dict, rebuilt: dict) -> list[str]:
    mutations = {
        "eligible_root": lambda value: value["carrier"].__setitem__(
            "eligible_root_color_pairs", 1),
        "false_closure": lambda value: value["carrier"].__setitem__(
            "new_task_closures", 1),
        "degree_maximum": lambda value: value["carrier"].__setitem__(
            "maximum_fixed_red_degree", 18),
        "embedding_count": lambda value: value["carrier"].__setitem__(
            "ordered_interface_embeddings_covered",
            value["carrier"]["ordered_interface_embeddings_covered"] + 1),
        "task_digest": lambda value: value.__setitem__(
            "carrier_task_digest_sha256", "0" * 64),
    }
    rejected = []
    for name, mutate in mutations.items():
        altered = copy.deepcopy(expected)
        mutate(altered)
        try:
            audit_expected(altered, rebuilt)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("accepted corruption: " + name)
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch", required=True, type=Path,
                        help="existing directory for small temporary files")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    require(args.scratch.is_dir(), "scratch directory does not exist")
    audit_hashes()
    require(sha256(TARGET / "EXPECTED.json") == TARGET_EXPECTED_SHA256,
            "target expected hash")
    words, row_multisets = canonical_words()
    word_file = json.loads((Q10 / "CORE_WORDS.json").read_text())
    variables, reverse = physical_maps()
    require(word_file == {
        "words": words,
        "variables": [variables[row, column] for row in range(4)
                      for column in (40, 41, 42)]}, "core-word registry")
    tasks = reconstruct_tasks(words, variables)
    published_tasks = json.loads((Q10 / "TASKS.json").read_text())
    require(published_tasks == tasks, "task registry reconstruction")
    template = json.loads((CUT / "TEMPLATE.json").read_text())
    rebuilt, per_task = expected_result(tasks, template, reverse)
    expected = json.loads((TARGET / "EXPECTED.json").read_text())
    audit_expected(expected, rebuilt)
    black_box = black_box_interface_audit(template, args.scratch)
    rejected = corruption_controls(expected, rebuilt)
    direct_clause_width_lower_bound = (
        rebuilt["interface"]["root_star_edges"]
        - max(rebuilt["carrier"]["maximum_fixed_red_degree"],
              rebuilt["carrier"]["maximum_fixed_blue_degree"]))
    require(direct_clause_width_lower_bound == 12,
            "direct non-tautological clause-width lower bound")
    receipt = {
        "status": "INDEPENDENT_H4041_ACCEPT",
        "target_expected_sha256": TARGET_EXPECTED_SHA256,
        "h3987_tasks_sha256": Q10_TASKS_SHA256,
        "h4021_template_sha256": CUT_TEMPLATE_SHA256,
        "admissible_row_multisets": row_multisets,
        "canonical_core_word_orbits": len(words),
        "task_records_reconstructed": len(tasks),
        "unknown_tasks_checked": rebuilt["carrier"]["unknown_tasks_checked"],
        "previously_certified_unsat_imported":
            rebuilt["carrier"]["previously_certified_unsat"],
        "fixed_edge_count_histogram":
            rebuilt["carrier"]["fixed_edge_count_histogram"],
        "maximum_fixed_red_degree":
            rebuilt["carrier"]["maximum_fixed_red_degree"],
        "maximum_fixed_blue_degree":
            rebuilt["carrier"]["maximum_fixed_blue_degree"],
        "root_color_pairs_checked":
            rebuilt["carrier"]["root_color_pairs_checked"],
        "ordered_embeddings_per_task":
            rebuilt["carrier"]["ordered_interface_embeddings_covered"],
        "task_labelled_ordered_embeddings": (
            len(per_task)
            * rebuilt["carrier"]["ordered_interface_embeddings_covered"]),
        "direct_conflict_embeddings": 0,
        "new_task_closures": 0,
        "proved_minimum_non_tautological_direct_clause_width":
            direct_clause_width_lower_bound,
        "black_box_interface": black_box,
        "rejected_result_corruptions": rejected,
        "target_found": False,
    }
    if args.check_expected:
        pinned = json.loads((HERE / "EXPECTED.json").read_text())
        require(receipt == pinned, "review receipt differs from pin")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

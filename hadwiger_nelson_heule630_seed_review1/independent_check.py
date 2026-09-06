#!/usr/bin/env python3
"""Independent exact review of the 630-vertex five-chromatic seed.

The script imports no submitted executable.  It reconstructs all geometry,
generates the four-colour CNF from the graph definition, checks the compact
positive witnesses, and requires a real DRAT proof checked by an external
drat-trim executable.  Generated CNFs, proofs, and logs stay in --work.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
import os
from pathlib import Path
import resource
import subprocess
import sys


TARGET_COMMIT = "14a0c9b76d7907ab0d7107a0a8796e3c0784dc68"
TARGET_HASHES = {
    ".gitignore": "618f50be681a673d863a99f7b6a6e65af69cc8aa0bf7a37c72347f3e72c03809",
    "PROOF.md": "c94d920c671f18cd19fd6867c83db728fb48f58845df8544a339c1de5e1fa857",
    "README.md": "be107116ef95b4814d07ae236938a16cf8215573bc9853e50a48cc94d5027961",
    "build.py": "f3e2c4d579feccec7cab9a31903b814d5428c0d146053ed488ec1dc1cf6bcf4c",
    "cases.json": "7a08c2f2818e9545a1719e2f16a05eed2f9d82afc46384d4cd07acdcc10d76c0",
    "certificate.json": "fffa224298854425f7c40726a9dd96196b1c5e82b75ffa4d8c6c19fefbc8274f",
    "controls.py": "90d8487ffcad25c6830bf1c75e1d759567779bac21a091bbd6355df97d6a3be2",
    "independent.py": "091b762038fae447dad5679cd6cc25009291869d641af75a7b26b5cfc0551d60",
    "manifest.json": "b8115ea866c6ff2661ae440f9f6e85929d3c8bb6cd83b5f9fb88aa82a61d5747",
    "native.py": "f1ce9e6d8014c06b1882f5346217f1c4988852f7b0ee80e3db7b452ad25c87ae",
    "plan.json": "5da817c4506312cf5d30a83ec6242c3581ea882b4a1be48355c8e07d5a91a9df",
    "preparation.json": "72baacfe588ea5e3baf8527553aea8d633c65ca1eada9c7d9d793745729891de",
    "result.json": "10f2081745322a66e5a9cd549925aac1d93e0c0fcb9f6b1d5472f28a9a841c7b",
    "run.py": "e0b9f6f6033716fe687a27f00c6a6fbb9e38c81a4042ddee93146e425a64b0e1",
    "validation.json": "7f99bdefc02fbd38a81c4c0533b3b9faf6b19abc74299f07145d948837d153cc",
    "verify.py": "13268f6106966542793e9e078adba774865304561ca1abd4bfadd201f9d8e07f",
}
TARGET_MANIFEST_HASH = "e91ef9dc4cc128a573818be3df377c1f0e75fd7edc9227f71e0fc2cf75c94252"
INPUT_HASHES = {
    "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json":
        "bc8e0f5f5ec7fa5f2376cc77ba0e65f6023b340cf48990370d5eda575d30ae79",
    "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json":
        "89345930e1bea184ce2457b0e14a015bcd9a2901cfc609a6468cf050234a8317",
}
OLD_INPUT = "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json"
FRESH_INPUT = "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json"
EXPECTED_HOST_EDGE_HASH = "8dd36c195b3e252ec2be150ea6a029375707293fec70b63da9fc157eed4140f0"
EXPECTED_CNF_HASH = "8c123d547fc4c2ff24338880b8a9d61e6edb798b844900c172de6e6a6e3c7e4f"
OMITTED = [399, 462]
SCALE = 96
UNIT = (SCALE * SCALE,) + (0,) * 7


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def file_record(path: Path) -> dict[str, int | str]:
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def verify_sources(target: Path, repository: Path) -> dict[str, object]:
    source_records = {}
    for name, expected in TARGET_HASHES.items():
        record = file_record(target / name)
        require(record["sha256"] == expected, "reviewed source identity: " + name)
        source_records[name] = record
    manifest_raw = (target / "SHA256SUMS").read_bytes()
    require(sha256(manifest_raw).hexdigest() == TARGET_MANIFEST_HASH,
            "reviewed SHA256SUMS identity")
    manifest = {}
    for line in manifest_raw.decode("ascii").splitlines():
        digest, name = line.split(maxsplit=1)
        manifest[name] = digest
    require(manifest == TARGET_HASHES, "reviewed source manifest entries")
    source_records["SHA256SUMS"] = {
        "bytes": len(manifest_raw), "sha256": TARGET_MANIFEST_HASH,
    }
    inputs = {}
    for name, expected in INPUT_HASHES.items():
        record = file_record(repository / name)
        require(record["sha256"] == expected, "mathematical input identity: " + name)
        inputs[name] = record
    return {"target_files": source_records, "mathematical_inputs": inputs}


# A coefficient vector is recursively represented as
# A+B*sqrt(11), then each half as C+D*sqrt(5), then as E+F*sqrt(3).
# This tower multiplication is independent of the submitted ordered-XOR and
# sparse-radicand implementations.
def vector_add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(left, right))


def vector_scale(value: tuple[int, ...], factor: int) -> tuple[int, ...]:
    return tuple(factor * entry for entry in value)


def tower_product(left: tuple[int, ...], right: tuple[int, ...],
                  primes: tuple[int, ...] = (11, 5, 3)) -> tuple[int, ...]:
    require(len(left) == len(right) == 2 ** len(primes), "tower vector shape")
    if not primes:
        return (left[0] * right[0],)
    half = len(left) // 2
    a, b = left[:half], left[half:]
    c, d = right[:half], right[half:]
    remaining = primes[1:]
    low = vector_add(tower_product(a, c, remaining),
                     vector_scale(tower_product(b, d, remaining), primes[0]))
    high = vector_add(tower_product(a, d, remaining),
                      tower_product(b, c, remaining))
    return low + high


def scaled_axis(raw) -> tuple[int, ...]:
    values = [SCALE * Fraction(value) for value in raw]
    require(len(values) == 8 and all(value.denominator == 1 for value in values),
            "coordinate axis and scale")
    return tuple(int(value) for value in values)


def scaled_point(raw) -> tuple[tuple[int, ...], tuple[int, ...]]:
    require(isinstance(raw, list) and len(raw) == 2, "coordinate point shape")
    return scaled_axis(raw[0]), scaled_axis(raw[1])


def squared_distance(left, right) -> tuple[int, ...]:
    total = (0,) * 8
    for axis in range(2):
        delta = tuple(a - b for a, b in zip(left[axis], right[axis]))
        total = vector_add(total, tower_product(delta, delta))
    return total


def reconstruct_graph(repository: Path) -> dict[str, object]:
    old = json.loads((repository / OLD_INPUT).read_text(encoding="utf-8"))
    old_labels = [index for index, provenance in enumerate(old["provenance"])
                  if "510" in provenance]
    require(len(old_labels) == 510 and old_labels == sorted(set(old_labels)),
            "canonical old-label selection")
    require([old_labels[index] for index in OMITTED] == [436, 505],
            "omitted old-to-union label map")
    fresh = json.loads((repository / FRESH_INPUT).read_text(encoding="utf-8"))
    fresh_ids = [row["centre_index"] for row in fresh]
    require(len(fresh_ids) == 122 and fresh_ids == sorted(set(fresh_ids)),
            "canonical fresh-label selection")
    points = [scaled_point(old["coordinates"][str(label)]) for label in old_labels]
    points.extend(scaled_point(row["coordinates"]) for row in fresh)
    require(len(points) == len(set(points)) == 632, "632 distinct exact points")
    edges = [(left, right) for left, right in combinations(range(632), 2)
             if squared_distance(points[left], points[right]) == UNIT]
    require(len(edges) == len(set(edges)) == 3112, "complete H632 edge set")
    edge_raw = "".join(f"{left},{right}\n" for left, right in edges).encode("ascii")
    require(sha256(edge_raw).hexdigest() == EXPECTED_HOST_EDGE_HASH,
            "canonical H632 edge stream")
    retained = set(range(632)) - set(OMITTED)
    induced_edges = [(left, right) for left, right in edges
                     if left in retained and right in retained]
    require(len(induced_edges) == 3098, "630-seed induced edge count")
    degrees = Counter(vertex for edge in edges for vertex in edge)
    require(len(edges) - len(induced_edges)
            == degrees[399] + degrees[462] - int((399, 462) in set(edges)) == 14,
            "exact two-vertex edge loss")
    induced_raw = "".join(f"{left},{right}\n" for left, right in induced_edges).encode("ascii")
    return {
        "points": points,
        "edges": edges,
        "retained": sorted(retained),
        "induced_edges": induced_edges,
        "old_labels": old_labels,
        "fresh_ids": fresh_ids,
        "host_edge_sha256": sha256(edge_raw).hexdigest(),
        "induced_edge_sha256": sha256(induced_raw).hexdigest(),
        "omitted_degrees": {"399": degrees[399], "462": degrees[462]},
        "omitted_adjacent": (399, 462) in set(edges),
    }


def first_triangle(vertices: list[int], edges: list[tuple[int, int]]) -> list[int]:
    vertex_set = set(vertices)
    relevant = [(left, right) for left, right in edges
                if left in vertex_set and right in vertex_set]
    adjacency = {vertex: set() for vertex in vertices}
    edge_set = set(relevant)
    for left, right in relevant:
        adjacency[left].add(right)
        adjacency[right].add(left)
    for left in vertices:
        higher = sorted(vertex for vertex in adjacency[left] if vertex > left)
        for middle, right in combinations(higher, 2):
            if (middle, right) in edge_set:
                return [left, middle, right]
    return []


def colour_cnf(vertices, edges, colours: int):
    vertices = sorted(vertices)
    position = {vertex: index for index, vertex in enumerate(vertices)}
    relevant = [(left, right) for left, right in edges
                if left in position and right in position]

    def variable(vertex: int, colour: int) -> int:
        return colours * position[vertex] + colour + 1

    clauses = []
    for vertex in vertices:
        clauses.append([variable(vertex, colour) for colour in range(colours)])
        clauses.extend([-variable(vertex, left), -variable(vertex, right)]
                       for left, right in combinations(range(colours), 2))
    for left, right in relevant:
        clauses.extend([-variable(left, colour), -variable(right, colour)]
                       for colour in range(colours))
    triangle = first_triangle(vertices, edges)
    clauses.extend([variable(vertex, colour)]
                    for colour, vertex in enumerate(triangle))
    variable_count = colours * len(vertices)
    raw = (f"p cnf {variable_count} {len(clauses)}\n"
           + "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)).encode("ascii")
    return clauses, raw, triangle


def parse_dimacs(raw: bytes) -> tuple[int, list[list[int]]]:
    lines = raw.decode("ascii").splitlines()
    header = lines[0].split()
    require(len(header) == 4 and header[:2] == ["p", "cnf"], "DIMACS header")
    variables, expected_clauses = map(int, header[2:])
    clauses = []
    for line in lines[1:]:
        values = list(map(int, line.split()))
        require(values and values[-1] == 0 and 0 not in values[:-1], "DIMACS clause terminator")
        require(all(1 <= abs(value) <= variables for value in values[:-1]),
                "DIMACS variable range")
        clauses.append(values[:-1])
    require(len(clauses) == expected_clauses, "DIMACS clause count")
    return variables, clauses


def encoding_controls() -> int:
    possible_edges = list(combinations(range(3), 2))
    examined = 0
    for edge_bits in range(8):
        edges = [edge for index, edge in enumerate(possible_edges)
                 if edge_bits & (1 << index)]
        clauses, _, triangle = colour_cnf(range(3), edges, 4)
        for bits in range(1 << 12):
            truth = {variable + 1: bool(bits & (1 << variable)) for variable in range(12)}
            cnf_value = all(any(truth[abs(literal)] == (literal > 0)
                                for literal in clause) for clause in clauses)
            selected = [{colour for colour in range(4)
                         if truth[4 * vertex + colour + 1]} for vertex in range(3)]
            direct = all(len(colours) == 1 for colours in selected)
            if direct:
                row = [next(iter(colours)) for colours in selected]
                direct = (all(row[left] != row[right] for left, right in edges)
                          and all(row[vertex] == colour
                                  for colour, vertex in enumerate(triangle)))
            require(cnf_value == direct, "definition-level encoder equivalence")
            examined += 1
    require(examined == 32768, "complete small encoding controls")
    return examined


def check_colouring(text: str, omitted: list[int], edges, colours: int) -> dict[str, object]:
    require(len(text) == 632 and set(text) <= set("." + "".join(map(str, range(colours)))),
            "colouring length and alphabet")
    require([vertex for vertex, colour in enumerate(text) if colour == "."] == omitted,
            "colouring omission set")
    checks = 0
    for left, right in edges:
        if text[left] == "." or text[right] == ".":
            continue
        checks += 1
        require(text[left] != text[right], "monochromatic exact unit edge")
    frequencies = Counter(text)
    frequencies.pop(".", None)
    return {"edge_checks": checks,
            "colour_frequencies": {key: frequencies[key] for key in sorted(frequencies)}}


def child_limits() -> None:
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024 ** 3,) * 2)
    resource.setrlimit(resource.RLIMIT_FSIZE, (512 * 1024 ** 2,) * 2)


def run_command(command: list[Path | str], log: Path, timeout: int) -> int:
    with log.open("wb") as stream:
        try:
            completed = subprocess.run([str(part) for part in command], stdout=stream,
                                       stderr=subprocess.STDOUT, timeout=timeout,
                                       preexec_fn=child_limits, check=False)
        except subprocess.TimeoutExpired as error:
            raise ReviewFailure("external proof command timed out") from error
    return completed.returncode


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--lrat-check", type=Path, required=True)
    proof_group = parser.add_mutually_exclusive_group(required=True)
    proof_group.add_argument("--proof", type=Path)
    proof_group.add_argument("--regenerate-with", type=Path, metavar="KISSAT")
    parser.add_argument("--solver-seed", type=int, default=17)
    args = parser.parse_args()

    repository = args.repository.resolve()
    target = repository / "hadwiger_nelson_heule632_pair_pilot"
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    source = verify_sources(target, repository)
    graph = reconstruct_graph(repository)

    clauses, cnf_raw, triangle = colour_cnf(graph["retained"], graph["edges"], 4)
    variables, parsed_clauses = parse_dimacs(cnf_raw)
    require(parsed_clauses == clauses, "generated and parsed clause identity")
    require((variables, len(clauses), triangle) == (2520, 16805, [0, 143, 146]),
            "winning CNF size and pinned triangle")
    require((len(graph["retained"]), len(graph["induced_edges"])) == (630, 3098),
            "winning graph order and size")
    require(sha256(cnf_raw).hexdigest() == EXPECTED_CNF_HASH,
            "canonical four-colour CNF")
    cnf_path = work / "four.cnf"
    cnf_path.write_bytes(cnf_raw)

    certificate = json.loads((target / "certificate.json").read_text(encoding="utf-8"))
    preparation = json.loads((target / "preparation.json").read_text(encoding="utf-8"))
    require(certificate["winner_index"] == 5 and certificate["omitted"] == OMITTED,
            "certificate winning support")
    require((certificate["vertices"], certificate["unit_edges"],
             certificate["four_cnf_sha256"])
            == (630, 3098, EXPECTED_CNF_HASH), "certificate theorem summary")
    require(preparation["selected"][5]["omitted"] == OMITTED
            and preparation["selected"][5]["unit_edges"] == 3098
            and preparation["selected"][5]["cnf_sha256"] == EXPECTED_CNF_HASH,
            "frozen winning case identity")
    five_check = check_colouring(certificate["five_colouring"], OMITTED,
                                 graph["edges"], 5)
    require(five_check["edge_checks"] == 3098
            and set(five_check["colour_frequencies"]) == set("01234"),
            "proper genuine five-colouring")

    require([row["index"] for row in certificate["four_colourings"]] == list(range(5)),
            "five positive prefix rows")
    prefix_checks = 0
    prefix_records = []
    for row in certificate["four_colourings"]:
        prepared = preparation["selected"][row["index"]]
        require(row["omitted"] == prepared["omitted"], "prefix omission provenance")
        record = check_colouring(row["colouring"], row["omitted"], graph["edges"], 4)
        require(record["edge_checks"] == prepared["unit_edges"], "prefix retained edge count")
        prefix_checks += record["edge_checks"]
        prefix_records.append({"index": row["index"], "omitted": row["omitted"], **record})
    require(prefix_checks == 15511, "all positive prefix edge checks")

    malformed = []
    malformed.append(certificate["five_colouring"][:-1])
    malformed.append(certificate["five_colouring"].replace(".", "0", 1))
    bad = list(certificate["five_colouring"])
    first_edge = graph["induced_edges"][0]
    bad[first_edge[1]] = bad[first_edge[0]]
    malformed.append("".join(bad))
    bad = list(certificate["five_colouring"]); bad[0] = "5"; malformed.append("".join(bad))
    rejected = 0
    for text in malformed:
        try:
            check_colouring(text, OMITTED, graph["edges"], 5)
        except ReviewFailure:
            rejected += 1
        else:
            raise ReviewFailure("malformed positive certificate accepted")
    require(rejected == 4, "all malformed positive controls rejected")
    boolean_controls = encoding_controls()

    solver_record = None
    if args.regenerate_with is not None:
        solver = args.regenerate_with.resolve()
        require(solver.is_file(), "solver executable exists")
        proof = work / "regenerated.drat"
        solver_log = work / "solver.log"
        code = run_command([solver, f"--seed={args.solver_seed}", "--conflicts=500000",
                            "--time=60", cnf_path, proof], solver_log, 75)
        solver_lines = solver_log.read_text(encoding="utf-8", errors="replace").splitlines()
        require(code == 20 and "s UNSATISFIABLE" in solver_lines,
                "solver produced a refutation trace")
        solver_record = {"sha256": file_record(solver)["sha256"],
                         "seed": args.solver_seed,
                         "exit_code": code,
                         "proof_regenerated": True}
    else:
        proof = args.proof.resolve()
        require(proof.is_file(), "supplied proof exists")
    require(proof.stat().st_size > 0, "nonempty DRAT proof")

    checker = args.drat_trim.resolve()
    require(checker.is_file(), "DRAT checker executable exists")
    checker_log = work / "drat-trim.log"
    lrat_path = work / "core.lrat"
    checker_code = run_command([checker, cnf_path, proof, "-L", lrat_path, "-t", "300"],
                               checker_log, 315)
    checker_lines = checker_log.read_text(encoding="utf-8", errors="replace").splitlines()
    require(checker_code == 0 and "s VERIFIED" in checker_lines,
            "DRAT proof checks against reviewer CNF")
    require(lrat_path.is_file() and lrat_path.stat().st_size > 0,
            "DRAT checker emitted a nonempty LRAT trace")
    lrat_checker = args.lrat_check.resolve()
    require(lrat_checker.is_file(), "LRAT checker executable exists")
    lrat_log = work / "lrat-check.log"
    lrat_code = run_command([lrat_checker, cnf_path, lrat_path], lrat_log, 315)
    lrat_lines = lrat_log.read_text(encoding="utf-8", errors="replace").splitlines()
    require(lrat_code == 0 and "c VERIFIED" in lrat_lines,
            "LRAT trace checks against reviewer CNF")
    lrat_rows = lrat_path.read_bytes().splitlines(keepends=True)
    require(lrat_rows and lrat_rows[-1].split(maxsplit=1)[1].startswith(b"0 "),
            "LRAT terminal empty-clause row")
    truncated_lrat = work / "missing-empty-clause.lrat"
    truncated_lrat.write_bytes(b"".join(lrat_rows[:-1]))
    truncated_log = work / "missing-empty-clause.log"
    truncated_code = run_command([lrat_checker, cnf_path, truncated_lrat],
                                 truncated_log, 315)
    truncated_lines = truncated_log.read_text(encoding="utf-8", errors="replace").splitlines()
    require(truncated_code != 0 and "c NOT VERIFIED" in truncated_lines,
            "LRAT checker rejects trace without terminal empty clause")
    proof_record = file_record(proof)

    result = {
        "all_checks_passed": True,
        "accepted_claim": "H632 minus old vertices 399 and 462 has 630 vertices, 3098 edges, and chromatic number exactly five",
        "reviewed_source_commit": TARGET_COMMIT,
        "source_identity": source,
        "geometry": {
            "host_vertices": 632,
            "distinct_points": 632,
            "exact_pairs_checked": 199396,
            "host_edges": 3112,
            "host_edge_sha256": graph["host_edge_sha256"],
            "omitted_old_vertices": OMITTED,
            "omitted_union_labels": [436, 505],
            "omitted_degrees": graph["omitted_degrees"],
            "omitted_adjacent": graph["omitted_adjacent"],
            "seed_vertices": 630,
            "seed_edges": 3098,
            "seed_edge_sha256": graph["induced_edge_sha256"],
        },
        "four_colour_lower_bound": {
            "variables": variables,
            "clauses": len(clauses),
            "clause_partition": {
                "at_least_one": 630,
                "at_most_one": 3780,
                "edge_colour": 12392,
                "triangle_pins": 3,
            },
            "pinned_triangle": triangle,
            "cnf_bytes": len(cnf_raw),
            "cnf_sha256": sha256(cnf_raw).hexdigest(),
            "definition_level_boolean_controls": boolean_controls,
            "proof": proof_record,
            "proof_checkers": {
                "drat_trim": {**file_record(checker), "exit_code": checker_code,
                              "exact_verified_line": True},
                "lrat_check": {**file_record(lrat_checker), "exit_code": lrat_code,
                               "exact_verified_line": True},
            },
            "derived_lrat": file_record(lrat_path),
            "solver": solver_record,
        },
        "five_colour_upper_bound": five_check,
        "positive_pilot_prefix": {
            "rows": prefix_records,
            "total_edge_checks": prefix_checks,
        },
        "negative_controls": {
            "malformed_positive_colourings_rejected": rejected,
            "lrat_without_empty_clause_rejected": True,
        },
        "scope": {
            "chromatic_number_exact": 5,
            "record_improvement": False,
            "sub509_graph": False,
            "minimality": False,
            "vertex_criticality": False,
            "unattempted_pilot_pairs_decided": False,
        },
        "trust_boundary": [
            "the two SHA-256-pinned coordinate tables",
            "linear independence of the eight squarefree radical basis elements",
            "ordinary CPython integer/Fraction arithmetic, JSON decoding, and exhaustive pair enumeration",
            "soundness of the independently built drat-trim and lrat-check proof checkers; solver UNSAT output is not trusted",
            "SHA-256 collision resistance for source and stream identities",
        ],
        "python": sys.version.split()[0],
    }
    atomic_json(args.report.resolve(), result)
    print(json.dumps({
        "all_checks_passed": True,
        "vertices": 630,
        "edges": 3098,
        "chromatic_number": 5,
        "cnf_sha256": sha256(cnf_raw).hexdigest(),
        "proof_sha256": proof_record["sha256"],
        "proof_bytes": proof_record["bytes"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()

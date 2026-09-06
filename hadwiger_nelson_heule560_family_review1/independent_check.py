#!/usr/bin/env python3
"""Independent exact review of the H560 seed and its M492/U68 reduction.

No executable from the reviewed contribution is imported.  This checker
reconstructs the Euclidean graph with exact quadratic-tower arithmetic,
rebuilds the direct four-colour CNF, requires checked DRAT and LRAT evidence,
checks the five-colour witness, and independently produces or consumes all
492 positive singleton-deletion witnesses.  Large generated artifacts stay
in --work.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import comb
import os
from pathlib import Path
import resource
import subprocess
import sys


TARGET_COMMIT = "5cc08e6ec43644ccd6ce741c641edf8799bd4955"
TARGET_HASHES = {
    ".gitignore": "618f50be681a673d863a99f7b6a6e65af69cc8aa0bf7a37c72347f3e72c03809",
    "PROOF.md": "dde81a527421f8d9e341f7da2de898157e27ea049fdbb25981dec5cc7f48c32e",
    "README.md": "effe2ba2e56d105725eb0ddeb2abb76b76622f9ecd8af19159607c6a46d0d9fe",
    "boundary.json": "8732adbdfe9792d6b6496bfec89da64b0127c388c2bb79f892b1d35a9c396f5e",
    "certificate.json": "3a22660e40329c0aef34e108b91747f529adb046cf687df5b05b3531ca17e35b",
    "check_boundary.py": "e4910171272b5648fdd4488e4003279b4a8d4dedfc31043d5c1680597d736cf5",
    "initial_positive.json": "dfac460b2f15d658996d8adbc42a86cc2a4339f96c45a12fa78d0cf9034e4e70",
    "manifest.json": "9cc31271e966ba44593f3d153adf7b065cf20b05eb9ff9faded1a451aef50eba",
    "plan.json": "1b27410491811802ffae0503e88f26bc2f8ea90ae890b1d5a5651156c7e5329d",
    "search.py": "3d53c9d43049fe5fa42bb18eaa8f4a163b0d24b8fb7b8f65c403e758b2200d30",
    "search_summary.json": "abf669ccbd786dde9fe19aaed704d6052141d27ae8c58c8ae2b0ec57e075fa05",
    "sweep.tsv": "889c8b69ba999107db3952f57ddf07e0baa10d24b5321038ad89ca74abda8752",
    "validation.json": "acd1863a75a50cb5d8cdc254a6e68d084fe59fc2915c0de3c2e7d21c632e4072",
    "verify.py": "f2e94656d4cc45989ce3a14bc8249cd45e7336371f96c30e62fa85400936849f",
}
TARGET_MANIFEST_HASH = "4383cbca8e4f5a4ec446959e975c6ab92246b3c80e014098645fbf01dbd9345c"
INPUT_HASHES = {
    "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json":
        "bc8e0f5f5ec7fa5f2376cc77ba0e65f6023b340cf48990370d5eda575d30ae79",
    "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json":
        "89345930e1bea184ce2457b0e14a015bcd9a2901cfc609a6468cf050234a8317",
}
OLD_INPUT = "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json"
FRESH_INPUT = "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json"
EXPECTED_HOST_EDGE_HASH = "8dd36c195b3e252ec2be150ea6a029375707293fec70b63da9fc157eed4140f0"
EXPECTED_CNF_HASH = "9dbec7853461556956cd34e406d475ba1f13144fae87e72b6f136e2b4805d673"
TARGET_PROOF_HASH = "1044755e0d6697500bc7c67ac8124e5361cf97e72c02b5ace24d592c063f7b1d"
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


def integer_stream_record(values: list[int]) -> dict[str, int | str]:
    raw = "".join(f"{value}\n" for value in values).encode("ascii")
    return {"count": len(values), "bytes": len(raw),
            "sha256": sha256(raw).hexdigest()}


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
    input_records = {}
    for name, expected in INPUT_HASHES.items():
        record = file_record(repository / name)
        require(record["sha256"] == expected, "mathematical input identity: " + name)
        input_records[name] = record
    return {"target_files": source_records, "mathematical_inputs": input_records}


# Coefficients are recursively represented in
# Q(sqrt(3))(sqrt(5))(sqrt(11)), with outer halves A+B*sqrt(p).
# This differs from both reviewed XOR convolution and sparse-radicand code.
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


def reconstruct_host(repository: Path) -> dict[str, object]:
    old = json.loads((repository / OLD_INPUT).read_text(encoding="utf-8"))
    old_labels = [index for index, provenance in enumerate(old["provenance"])
                  if "510" in provenance]
    require(len(old_labels) == 510 and old_labels == sorted(set(old_labels)),
            "canonical old-label selection")
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
    return {"points": points, "edges": edges, "old_labels": old_labels,
            "fresh_ids": fresh_ids, "host_edge_sha256": sha256(edge_raw).hexdigest()}


def induced_graph(vertices: list[int], edges: list[tuple[int, int]]) -> dict[str, object]:
    vertex_set = set(vertices)
    require(vertices == sorted(vertex_set) and vertex_set <= set(range(632)),
            "canonical retained support")
    relevant = [(left, right) for left, right in edges
                if left in vertex_set and right in vertex_set]
    raw = "".join(f"{left},{right}\n" for left, right in relevant).encode("ascii")
    degrees = Counter(vertex for edge in relevant for vertex in edge)
    return {"vertices": vertices, "vertex_set": vertex_set, "edges": relevant,
            "edge_sha256": sha256(raw).hexdigest(),
            "degree_histogram": dict(sorted(Counter(degrees.values()).items()))}


def first_triangle(vertices: list[int], edges: list[tuple[int, int]]) -> list[int]:
    adjacency = {vertex: set() for vertex in vertices}
    edge_set = set(edges)
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    for left in vertices:
        higher = sorted(vertex for vertex in adjacency[left] if vertex > left)
        for middle, right in combinations(higher, 2):
            if (middle, right) in edge_set:
                return [left, middle, right]
    return []


def colour_cnf(vertices: list[int], edges: list[tuple[int, int]], colours: int):
    positions = {vertex: index for index, vertex in enumerate(vertices)}

    def variable(vertex: int, colour: int) -> int:
        return colours * positions[vertex] + colour + 1

    clauses = []
    for vertex in vertices:
        clauses.append([variable(vertex, colour) for colour in range(colours)])
        clauses.extend([-variable(vertex, left), -variable(vertex, right)]
                       for left, right in combinations(range(colours), 2))
    for left, right in edges:
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
        require(values and values[-1] == 0 and 0 not in values[:-1],
                "DIMACS clause terminator")
        require(all(1 <= abs(value) <= variables for value in values[:-1]),
                "DIMACS variable range")
        clauses.append(values[:-1])
    require(len(clauses) == expected_clauses, "DIMACS clause count")
    return variables, clauses


def direct_encoding_controls() -> int:
    possible_edges = list(combinations(range(3), 2))
    examined = 0
    for edge_bits in range(8):
        edges = [edge for index, edge in enumerate(possible_edges)
                 if edge_bits & (1 << index)]
        clauses, _, triangle = colour_cnf(list(range(3)), edges, 4)
        for bits in range(1 << 12):
            truth = {variable + 1: bool(bits & (1 << variable))
                     for variable in range(12)}
            actual = all(any(truth[abs(literal)] == (literal > 0)
                             for literal in clause) for clause in clauses)
            chosen = [{colour for colour in range(4)
                       if truth[4 * vertex + colour + 1]} for vertex in range(3)]
            expected = all(len(entry) == 1 for entry in chosen)
            if expected:
                row = [next(iter(entry)) for entry in chosen]
                expected = (all(row[left] != row[right] for left, right in edges)
                            and all(row[vertex] == colour
                                    for colour, vertex in enumerate(triangle)))
            require(actual == expected, "direct encoder definition control")
            examined += 1
    require(examined == 32768, "complete direct encoding controls")
    return examined


def activation_cnf(vertex_count: int, edges: list[tuple[int, int]],
                   triangle: list[int]):
    colour = lambda vertex, value: 4 * vertex + value + 1
    active = lambda vertex: 4 * vertex_count + vertex + 1
    clauses = []
    for vertex in range(vertex_count):
        clauses.append([colour(vertex, value) for value in range(4)])
        clauses.extend([-colour(vertex, left), -colour(vertex, right)]
                       for left, right in combinations(range(4), 2))
    for left, right in edges:
        clauses.extend([-active(left), -active(right),
                        -colour(left, value), -colour(right, value)]
                       for value in range(4))
    clauses.extend([-active(vertex), colour(vertex, value)]
                   for value, vertex in enumerate(triangle))
    return clauses


def activation_encoding_controls() -> int:
    possible_edges = list(combinations(range(3), 2))
    examined = 0
    for edge_bits in range(8):
        edges = [edge for index, edge in enumerate(possible_edges)
                 if edge_bits & (1 << index)]
        triangle = [0, 1, 2] if len(edges) == 3 else []
        clauses = activation_cnf(3, edges, triangle)
        for bits in range(1 << 15):
            truth = {variable + 1: bool(bits & (1 << variable))
                     for variable in range(15)}
            actual = all(any(truth[abs(literal)] == (literal > 0)
                             for literal in clause) for clause in clauses)
            chosen = [{colour for colour in range(4)
                       if truth[4 * vertex + colour + 1]} for vertex in range(3)]
            selected = {vertex for vertex in range(3) if truth[13 + vertex]}
            expected = all(len(entry) == 1 for entry in chosen)
            if expected:
                row = [next(iter(entry)) for entry in chosen]
                expected = all(left not in selected or right not in selected
                               or row[left] != row[right] for left, right in edges)
                expected = expected and all(vertex not in selected
                                            or row[vertex] == value
                                            for value, vertex in enumerate(triangle))
            require(actual == expected, "activation encoder definition control")
            examined += 1
    require(examined == 262144, "complete activation encoding controls")
    return examined


def check_colouring(text: str, omitted: list[int], host_edges, colours: int):
    require(len(text) == 632 and set(text) <= set("." + "".join(map(str, range(colours)))),
            "colouring length and alphabet")
    require([vertex for vertex, value in enumerate(text) if value == "."] == omitted,
            "colouring exact support")
    checks = 0
    for left, right in host_edges:
        if text[left] == "." or text[right] == ".":
            continue
        checks += 1
        require(text[left] != text[right], "monochromatic exact unit edge")
    frequencies = Counter(text)
    frequencies.pop(".", None)
    return {"edge_checks": checks,
            "colour_frequencies": {key: frequencies[key] for key in sorted(frequencies)}}


def check_witness_rows(rows: dict[str, object], mandatory: list[int],
                       retained: list[int], host_edges) -> dict[str, object]:
    require(sorted(map(int, rows)) == mandatory, "one witness for each mandatory vertex")
    retained_set = set(retained)
    checks = 0
    witness_frequencies = Counter()
    for label in sorted(rows, key=int):
        vertex = int(label)
        row = rows[label]
        require(isinstance(row, dict) and isinstance(row.get("colouring"), str),
                "witness row structure")
        omitted = sorted(set(range(632)) - (retained_set - {vertex}))
        record = check_colouring(row["colouring"], omitted, host_edges, 4)
        checks += record["edge_checks"]
        witness_frequencies.update(row["colouring"].replace(".", ""))
    return {"rows": len(rows), "edge_checks": checks,
            "aggregate_colour_frequencies": {
                key: witness_frequencies[key] for key in sorted(witness_frequencies)}}


def generate_witnesses(work: Path, mandatory: list[int], retained: list[int],
                       retained_edges: list[tuple[int, int]], host_edges,
                       triangle: list[int], solver_name: str) -> tuple[dict[str, object], dict[str, object]]:
    import pysat
    import pysolvers
    from pysat.solvers import Solver

    positions = {vertex: index for index, vertex in enumerate(retained)}
    local_edges = [(positions[left], positions[right]) for left, right in retained_edges]
    local_triangle = [positions[vertex] for vertex in triangle]
    clauses = activation_cnf(len(retained), local_edges, local_triangle)
    activation_base = 4 * len(retained)
    checkpoint = work / "witness-checkpoint.json"
    rows = {}
    if checkpoint.exists():
        saved = json.loads(checkpoint.read_text(encoding="utf-8"))
        require(saved.get("solver_name") == solver_name, "checkpoint solver identity")
        rows = saved.get("rows", {})
        completed = sorted(map(int, rows))
        require(completed == mandatory[:len(completed)], "checkpoint mandatory prefix")
        if rows:
            check_witness_rows(rows, completed, retained, host_edges)

    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        for index, deleted in enumerate(mandatory):
            if str(deleted) in rows:
                continue
            assumptions = [activation_base + position + 1
                           if vertex != deleted else -(activation_base + position + 1)
                           for position, vertex in enumerate(retained)]
            answer = solver.solve(assumptions=assumptions)
            require(answer is True, "positive singleton witness generation")
            model = solver.get_model()
            truth = {abs(literal): literal > 0 for literal in model}
            require(set(range(1, 5 * len(retained) + 1)) <= set(truth),
                    "complete activation model")
            require(all(truth[abs(literal)] == (literal > 0)
                        for literal in assumptions), "activation assumptions")
            require(all(any(truth[abs(literal)] == (literal > 0)
                            for literal in clause) for clause in clauses),
                    "all activation model clauses")
            text = ["."] * 632
            for position, vertex in enumerate(retained):
                if vertex == deleted:
                    continue
                chosen = [colour for colour in range(4)
                          if truth[4 * position + colour + 1]]
                require(len(chosen) == 1, "one colour in positive model")
                text[vertex] = str(chosen[0])
            row = {"colouring": "".join(text),
                   "source": f"reviewer-activation-{solver_name}"}
            check_colouring(row["colouring"],
                            sorted(set(range(632)) - (set(retained) - {deleted})),
                            host_edges, 4)
            rows[str(deleted)] = row
            if (index + 1) % 25 == 0 or index + 1 == len(mandatory):
                atomic_json(checkpoint, {"solver_name": solver_name, "rows": rows})

    witness_path = work / "witnesses.json"
    atomic_json(witness_path, rows)
    native = Path(pysolvers.__file__)
    generator = {"python_sat_version": pysat.__version__, "solver_name": solver_name,
                 "pysolvers_native": file_record(native), "witnesses_regenerated": True}
    return rows, generator


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


def expect_failure(callback, message: str) -> None:
    try:
        callback()
    except ReviewFailure:
        return
    raise ReviewFailure(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--lrat-check", type=Path, required=True)
    parser.add_argument("--resume-work", action="store_true")
    proof_group = parser.add_mutually_exclusive_group(required=True)
    proof_group.add_argument("--proof", type=Path)
    proof_group.add_argument("--regenerate-with", type=Path, metavar="KISSAT")
    parser.add_argument("--solver-seed", type=int, default=29)
    witness_group = parser.add_mutually_exclusive_group(required=True)
    witness_group.add_argument("--witnesses", type=Path)
    witness_group.add_argument("--regenerate-witnesses", action="store_true")
    parser.add_argument("--pysat-solver", default="m22")
    args = parser.parse_args()

    repository = args.repository.resolve()
    target = repository / "hadwiger_nelson_heule632_minimize"
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=args.resume_work)
    source = verify_sources(target, repository)
    host = reconstruct_host(repository)
    certificate = json.loads((target / "certificate.json").read_text(encoding="utf-8"))
    boundary = json.loads((target / "boundary.json").read_text(encoding="utf-8"))

    retained = certificate["retained"]
    graph = induced_graph(retained, host["edges"])
    omitted = sorted(set(range(632)) - graph["vertex_set"])
    require(certificate["omitted"] == omitted, "certificate retained/omitted partition")
    require((certificate["vertices"], certificate["unit_edges"], len(retained),
             len(graph["edges"])) == (560, 2758, 560, 2758),
            "exact H560 order and size")

    clauses, cnf_raw, triangle = colour_cnf(retained, graph["edges"], 4)
    variables, parsed_clauses = parse_dimacs(cnf_raw)
    require(parsed_clauses == clauses, "generated and parsed clause identity")
    require((variables, len(clauses), triangle) == (2240, 14955, [0, 143, 146]),
            "H560 CNF size and triangle")
    require(sha256(cnf_raw).hexdigest() == EXPECTED_CNF_HASH,
            "canonical H560 four-colour CNF")
    require((certificate["four_cnf_variables"], certificate["four_cnf_clauses"],
             certificate["four_cnf_sha256"], certificate["triangle"])
            == (2240, 14955, EXPECTED_CNF_HASH, triangle),
            "certificate direct formula summary")
    cnf_path = work / "four.cnf"
    cnf_path.write_bytes(cnf_raw)

    five_check = check_colouring(certificate["five_colouring"], omitted,
                                 host["edges"], 5)
    require(five_check["edge_checks"] == 2758
            and set(five_check["colour_frequencies"]) == set("01234"),
            "proper genuine five-colouring")
    malformed_five = []
    malformed_five.append(certificate["five_colouring"][:-1])
    malformed_five.append(certificate["five_colouring"].replace(".", "0", 1))
    bad = list(certificate["five_colouring"])
    left, right = graph["edges"][0]
    bad[right] = bad[left]
    malformed_five.append("".join(bad))
    bad = list(certificate["five_colouring"]); bad[0] = "5"
    malformed_five.append("".join(bad))
    for text in malformed_five:
        expect_failure(lambda text=text: check_colouring(text, omitted, host["edges"], 5),
                       "malformed five-colour witness accepted")

    direct_controls = direct_encoding_controls()
    activation_controls = activation_encoding_controls()

    mandatory = boundary["mandatory_vertices"]
    optional = boundary["optional_vertices"]
    require(mandatory == sorted(set(mandatory)) and optional == sorted(set(optional)),
            "canonical boundary sets")
    require(not set(mandatory) & set(optional)
            and set(mandatory) | set(optional) == graph["vertex_set"],
            "M/U partition of H560")
    require((len(mandatory), len(optional), comb(68, 16),
             boundary["maximum_optional_vertices_at_target"],
             boundary["exact_size_508_supports"])
            == (492, 68, 1469568786235308, 16, 1469568786235308),
            "exact reduced family cardinality")

    if args.regenerate_witnesses:
        rows, witness_generator = generate_witnesses(
            work, mandatory, retained, graph["edges"], host["edges"], triangle,
            args.pysat_solver)
        witness_path = work / "witnesses.json"
    else:
        witness_path = args.witnesses.resolve()
        require(witness_path.is_file(), "supplied witness table exists")
        rows = json.loads(witness_path.read_text(encoding="utf-8"))
        witness_generator = {"witnesses_regenerated": False}
    witness_check = check_witness_rows(rows, mandatory, retained, host["edges"])
    require(witness_check["rows"] == 492 and witness_check["edge_checks"] == 1351849,
            "all mandatory singleton witnesses")

    missing = dict(rows)
    del missing[str(mandatory[0])]
    expect_failure(lambda: check_witness_rows(missing, mandatory, retained, host["edges"]),
                   "missing mandatory witness accepted")
    wrong_support = copy.deepcopy(rows)
    first_label = str(mandatory[0])
    wrong = list(wrong_support[first_label]["colouring"])
    wrong[mandatory[0]] = "0"
    wrong_support[first_label]["colouring"] = "".join(wrong)
    expect_failure(lambda: check_witness_rows(wrong_support, mandatory, retained,
                                               host["edges"]),
                   "wrong singleton support accepted")
    improper = copy.deepcopy(rows)
    deleted = mandatory[0]
    left, right = next((left, right) for left, right in graph["edges"]
                       if deleted not in (left, right))
    bad = list(improper[first_label]["colouring"])
    bad[right] = bad[left]
    improper[first_label]["colouring"] = "".join(bad)
    expect_failure(lambda: check_witness_rows(improper, mandatory, retained,
                                               host["edges"]),
                   "monochromatic singleton witness accepted")

    solver_record = None
    if args.regenerate_with is not None:
        solver = args.regenerate_with.resolve()
        require(solver.is_file(), "solver executable exists")
        proof = work / "regenerated.drat"
        solver_log = work / "solver.log"
        code = run_command([solver, f"--seed={args.solver_seed}", "--conflicts=2000000",
                            "--time=120", cnf_path, proof], solver_log, 135)
        solver_lines = solver_log.read_text(encoding="utf-8", errors="replace").splitlines()
        require(code == 20 and "s UNSATISFIABLE" in solver_lines,
                "solver produced a refutation trace")
        solver_record = {**file_record(solver), "seed": args.solver_seed,
                         "exit_code": code, "proof_regenerated": True}
    else:
        proof = args.proof.resolve()
        require(proof.is_file(), "supplied proof exists")
    require(proof.stat().st_size > 0, "nonempty DRAT proof")

    checker = args.drat_trim.resolve()
    lrat_checker = args.lrat_check.resolve()
    require(checker.is_file() and lrat_checker.is_file(), "proof checker executables exist")
    checker_log = work / "drat-trim.log"
    lrat_path = work / "core.lrat"
    checker_code = run_command([checker, cnf_path, proof, "-L", lrat_path, "-t", "300"],
                               checker_log, 315)
    checker_lines = checker_log.read_text(encoding="utf-8", errors="replace").splitlines()
    require(checker_code == 0 and "s VERIFIED" in checker_lines,
            "DRAT proof checks against reviewer CNF")
    require(lrat_path.is_file() and lrat_path.stat().st_size > 0,
            "DRAT checker emitted nonempty LRAT")
    lrat_log = work / "lrat-check.log"
    lrat_code = run_command([lrat_checker, cnf_path, lrat_path], lrat_log, 315)
    lrat_lines = lrat_log.read_text(encoding="utf-8", errors="replace").splitlines()
    require(lrat_code == 0 and "c VERIFIED" in lrat_lines,
            "LRAT trace checks against reviewer CNF")
    lrat_rows = lrat_path.read_bytes().splitlines(keepends=True)
    require(lrat_rows and len(lrat_rows[-1].split(maxsplit=1)) == 2
            and lrat_rows[-1].split(maxsplit=1)[1].startswith(b"0 "),
            "LRAT terminal empty-clause row")
    truncated = work / "missing-empty-clause.lrat"
    truncated.write_bytes(b"".join(lrat_rows[:-1]))
    truncated_log = work / "missing-empty-clause.log"
    truncated_code = run_command([lrat_checker, cnf_path, truncated],
                                 truncated_log, 315)
    truncated_lines = truncated_log.read_text(encoding="utf-8", errors="replace").splitlines()
    require(truncated_code != 0 and "c NOT VERIFIED" in truncated_lines,
            "LRAT checker rejects missing terminal empty clause")
    proof_record = file_record(proof)

    result = {
        "all_checks_passed": True,
        "accepted_claim": ("the fixed H560 graph has chromatic number five and every "
                           "non-four-colourable subgraph within it contains M492, giving "
                           "the stated M plus 16-of-U68 equivalence at order at most 508"),
        "reviewed_source_commit": TARGET_COMMIT,
        "source_identity": source,
        "geometry": {
            "host_vertices": 632,
            "distinct_points": 632,
            "exact_pairs_checked": 199396,
            "host_edges": 3112,
            "host_edge_sha256": host["host_edge_sha256"],
            "seed_vertices": len(retained),
            "seed_edges": len(graph["edges"]),
            "seed_edge_sha256": graph["edge_sha256"],
            "omitted_vertices": omitted,
            "degree_histogram": graph["degree_histogram"],
        },
        "four_colour_lower_bound": {
            "variables": variables,
            "clauses": len(clauses),
            "clause_partition": {"at_least_one": 560, "at_most_one": 3360,
                                 "edge_colour": 11032, "triangle_pins": 3},
            "pinned_triangle": triangle,
            "cnf_bytes": len(cnf_raw),
            "cnf_sha256": sha256(cnf_raw).hexdigest(),
            "definition_level_boolean_controls": direct_controls,
            "proof": proof_record,
            "proof_differs_from_target_seed_zero": proof_record["sha256"] != TARGET_PROOF_HASH,
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
        "mandatory_optional_reduction": {
            "mandatory_count": len(mandatory),
            "optional_count": len(optional),
            "mandatory_vertex_stream": integer_stream_record(mandatory),
            "optional_vertex_stream": integer_stream_record(optional),
            "maximum_optional_at_order_508": 16,
            "size_508_supports": comb(68, 16),
            "activation_definition_controls": activation_controls,
            "positive_witnesses": {**witness_check, **file_record(witness_path)},
            "generator": witness_generator,
            "family_closed": False,
        },
        "negative_controls": {
            "malformed_five_colourings_rejected": len(malformed_five),
            "missing_mandatory_row_rejected": True,
            "wrong_singleton_support_rejected": True,
            "monochromatic_singleton_witness_rejected": True,
            "lrat_without_empty_clause_rejected": True,
        },
        "scope": {
            "chromatic_number_exact": 5,
            "record_improvement": False,
            "sub509_graph_established": False,
            "family_equivalence_within_H560": True,
            "family_member_decided": False,
            "minimality": False,
            "vertex_criticality": False,
            "exploratory_sweep_reproduced": False,
        },
        "trust_boundary": [
            "the two SHA-256-pinned coordinate tables and target certificate files",
            "linear independence of the eight squarefree radical basis elements",
            "ordinary CPython integer/Fraction arithmetic and exhaustive pair enumeration",
            "soundness of independently built drat-trim and lrat-check binaries; solver UNSAT text alone is not trusted",
            "positive witness validity is checked definitionally, so its SAT solver need not be trusted for soundness",
            "SHA-256 collision resistance for source and stream identities",
        ],
        "python": sys.version.split()[0],
    }
    atomic_json(args.report.resolve(), result)
    print(json.dumps({
        "all_checks_passed": True,
        "vertices": len(retained),
        "edges": len(graph["edges"]),
        "chromatic_number": 5,
        "mandatory": len(mandatory),
        "optional": len(optional),
        "cnf_sha256": sha256(cnf_raw).hexdigest(),
        "proof_sha256": proof_record["sha256"],
        "witness_sha256": file_record(witness_path)["sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()

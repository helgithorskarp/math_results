#!/usr/bin/env python3
"""Replay and separate the h3977 chromatic and h3981 geometric evidence."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_REPOSITORY = HERE.parent
EVIDENCE_SHA256 = "0ab8d449ec9655a79a610460a163bd94c1b59de582e9142b588c65cbb1f5dd1f"
INPUT_SHA256 = {
    "hadwiger_nelson_h516_k23free_edge_repair/certificate.json": "a1cb7ecc7f33c16d4230b027f7809d57f8d5a07491538b5aa94f13b4d00e1808",
    "hadwiger_nelson_h516_k23free_edge_repair/expected.json": "62c12c8528e8a4cca30f59f42269ec0622515a50830bd1a53d6e40cd2d397655",
    "hadwiger_nelson_h516_k23free_edge_repair/five_colouring.json": "720466c1b6403de7d8247a33bb2844fccca306dfa21cc339b763968e6b2aea1d",
    "hadwiger_nelson_h516_k23free_edge_repair/four_colour.cnf": "f88078fe17e76339b18bf4f1d339921ae2b0bf19a44367cd1978877ce54b0828",
    "hadwiger_nelson_h516_k23free_edge_repair/four_colour.lrat": "d9b9250c8d40cb59b07d973ba96ca02ec9fce3e446fd5db9ac804599c7d15711",
    "hadwiger_nelson_h516_k23free_edge_repair/graph.json": "7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb",
    "hadwiger_nelson_h516_k23free_edge_repair/strict_lrat.cpp": "182f852cf0548b8f785700da9a4b2e6004d6ff16da3244c7a7badcd138919d20",
    "hadwiger_nelson_h516_k23free_edge_repair/verify.py": "9a6e4bc1a54d0064b4ebc682e401b61713a02c6baccac0b921caca6f420b8306",
    "hadwiger_nelson_h516_k23free_edge_repair/vertex_deletion_colours.json": "e72ec7eb94c012ba00af1fa8a30ee782c84609992ad30322e172fdb36424bb70",
    "hadwiger_nelson_301_repair_plane_obstruction/EXPECTED.json": "709a5aa82e23b6eb2cd039f43481ba552ae77e77b344e8eabb9dfb3ac05f4d64",
    "hadwiger_nelson_301_repair_plane_obstruction/certificate.json": "728c5af3dc90c6e01ac74c13d78768cae997f6fe91d39dfa1076600bfb61ab42",
    "hadwiger_nelson_301_repair_plane_obstruction/verify.py": "a42d4b59ab09ffb1a61a5ca32831bfec16f99c638f15ef5f3df46ec1e0da7a89",
    "hadwiger_nelson_301_repair_plane_obstruction_review1/EXPECTED.json": "e0e871172a93e0cf364ab662adb888cdcc7f4c547e13a32390778658e19989ca",
    "hadwiger_nelson_301_repair_plane_obstruction_review1/reproduce.py": "189d41083e6225fc6b198822f7dc0fb4126322a9fbb07e156a87f9dca7f069ca",
    "hadwiger_nelson_301_repair_plane_obstruction_review2/EXPECTED.json": "1b27348519beecfb663c3e4fd59748594fa83b3bb931ae852a69a388f85bb4ed",
    "hadwiger_nelson_301_repair_plane_obstruction_review2/independent_check.py": "b64d4f628f429d41ab4735691d101df8ca591688cd27552792b1eb301c2af229",
    "hadwiger_nelson_301_repair_plane_obstruction_review2/reproduce.py": "ee0b68bcfc0b478f609785951d1da41ae151d20f98c2dea66203ad2178cb7bf0",
    "hadwiger_nelson_301_forbidden_subgraph_interface/EXPECTED.json": "cb7f56c6f7084708617ea1b5dba5ba2b6429be8308a3ef5718ddfa8cca80200c",
    "hadwiger_nelson_301_forbidden_subgraph_interface/PROVENANCE.json": "4fc5d9454d79bd106e8cc8206c45f1d94b84fefabd576c4ca2acfc909c5608c4",
    "hadwiger_nelson_301_forbidden_subgraph_interface/certificate.json": "7119f912d305b5ae20439bd1a138d161277cd7fc95a82a09b23feec775f3de5c",
    "hadwiger_nelson_301_forbidden_subgraph_interface/graph.json": "a5260af89de966a18e66a6ad932cd8f11e230a846a6f07e8ffaad005802e657f",
    "hadwiger_nelson_301_forbidden_subgraph_interface/repair_clause.cnf": "2e525fb48c247195fb20e6f4c323da5e0b87611c9f0ea25974485e94dbd3dfe3",
    "hadwiger_nelson_301_forbidden_subgraph_interface/verify.py": "7c695f564e879f31f4bdf70eada21b9a213dbdce04841c2ccb4ec4a0b4dff9e6",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text())


def run(arguments: list[str], cwd: Path) -> str:
    result = subprocess.run(arguments, cwd=cwd, check=True, capture_output=True, text=True)
    need(not result.stderr, f"unexpected stderr from {Path(arguments[0]).name}: {result.stderr}")
    return result.stdout


def validate_graph(graph: dict) -> tuple[set[int], set[tuple[int, int]]]:
    need(graph["vertices"] == len(graph["labels"]) == 301, "candidate vertex count")
    need(graph["edge_count"] == len(graph["edges"]) == 1452, "candidate edge count")
    labels = set(graph["labels"])
    need(len(labels) == 301, "candidate labels")
    edges = {tuple(edge) for edge in graph["edges"]}
    need(len(edges) == 1452, "candidate edge uniqueness")
    need(all(len(edge) == 2 and edge[0] < edge[1] for edge in edges), "candidate edge order")
    need(all(left in labels and right in labels for left, right in edges), "candidate edge endpoints")
    return labels, edges


def parse_repair_clause(path: Path) -> tuple[int, set[int]]:
    lines = [line.strip() for line in path.read_text().splitlines() if line.strip() and not line.startswith("c")]
    need(len(lines) == 2, "repair clause line count")
    header = lines[0].split()
    need(header == ["p", "cnf", "1452", "1"], "repair clause header")
    literals = [int(value) for value in lines[1].split()]
    need(literals[-1] == 0 and all(value < 0 for value in literals[:-1]), "repair clause signs")
    variables = {-value for value in literals[:-1]}
    need(len(variables) == len(literals) - 1 == 690, "repair clause literals")
    return 1452, variables


def audit_metadata(
    evidence: dict,
    repository: Path,
    *,
    check_evidence_hash: bool = True,
    check_inputs: bool = True,
) -> dict:
    if check_evidence_hash:
        need(sha256(HERE / "EVIDENCE.json") == EVIDENCE_SHA256, "evidence identity")
    if check_inputs:
        for relative, digest in INPUT_SHA256.items():
            need(sha256(repository / relative) == digest, f"input identity: {relative}")

    candidate = evidence["candidate"]
    obstruction = evidence["obstruction"]
    reviews = evidence["independent_acceptances"]
    downstream = evidence["downstream_interface"]
    conclusion = evidence["combined_conclusion"]
    need(evidence["status"] == "FIXED_301_CANDIDATE_CLOSED_BY_ACCEPTED_ALL_MAPS_OBSTRUCTION", "status")
    need(evidence["record_improvement"] is False, "record status")
    need(candidate["evidence_role"] == "abstract_chromatic_producer", "candidate role")
    need(candidate["geometric_claim"] == "none", "candidate geometric scope")
    need(candidate["chromatic_number"] == 5 and candidate["vertex_critical"] is True, "candidate chromatic claim")
    need(candidate["K23_free"] is True and candidate["K4_free"] is True, "candidate subgraph gates")
    need(obstruction["evidence_role"] == "geometric_nonrealizability", "obstruction role")
    need(obstruction["chromatic_claim_used"] is False, "obstruction chromatic independence")
    need(len(reviews) == 2 and all(row["verdict"] == "ACCEPT" for row in reviews), "independent acceptances")
    need(all(row["chromatic_LRAT_in_verdict"] is False for row in reviews), "review scope")
    need(conclusion["physical_candidate_survives"] is False, "combined conclusion")
    need(downstream["evidence_role"] == "necessary_condition_for_any_later_repair", "downstream role")
    need(downstream["sufficient_for_realizability"] is False, "repair clause necessity only")
    need(downstream["preserves_five_chromaticity"] is False, "repair clause chromatic scope")
    need(downstream["independently_reviewed"] is False, "downstream review scope")

    candidate_dir = repository / candidate["directory"]
    candidate_certificate = load_json(candidate_dir / "certificate.json")
    candidate_expected = load_json(candidate_dir / "expected.json")
    candidate_graph = load_json(candidate_dir / "graph.json")
    labels, source_edges = validate_graph(candidate_graph)
    need(sha256(candidate_dir / "graph.json") == candidate["graph_sha256"], "candidate graph identity")
    need(candidate["graph_sha256"] == obstruction["graph_sha256"], "layer graph identity")
    need(candidate_certificate["graph_sha256"] == candidate["graph_sha256"], "candidate certificate graph")
    need(candidate_certificate["four_colour_CNF_sha256"] == candidate_expected["verification"]["CNF_sha256"], "candidate CNF identity")
    need(candidate_certificate["four_colour_LRAT_sha256"] == candidate_expected["verification"]["LRAT_sha256"], "candidate LRAT identity")
    need(candidate_certificate["strict_LRAT"]["additions"] == candidate["LRAT_additions"], "candidate LRAT additions")
    need(candidate_certificate["strict_LRAT"]["hints_used"] == candidate["LRAT_hints"], "candidate LRAT hints")

    obstruction_dir = repository / obstruction["directory"]
    obstruction_expected = load_json(obstruction_dir / "EXPECTED.json")
    need(sha256(obstruction_dir / "certificate.json") == obstruction["certificate_sha256"], "obstruction certificate identity")
    need(obstruction_expected["vertices"] == candidate["vertices"], "obstruction vertex count")
    need(obstruction_expected["edges"] == candidate["edges"], "obstruction edge count")
    need(obstruction_expected["mandatory_four_cycles"] == obstruction["mandatory_four_cycles"], "obstruction cycles")
    need(obstruction_expected["anchored_linear_rank"] == obstruction["anchored_rank"], "obstruction rank")
    need(obstruction_expected["coordinate_parameters"] == obstruction["coordinate_parameters"], "obstruction parameters")
    need(obstruction_expected["norm_identity_edges"] == obstruction["norm_identity_edges"], "obstruction norm support")
    need(obstruction_expected["unit_norm_sum"] == obstruction["unit_norm_sum"], "obstruction contradiction")

    review1_expected = load_json(repository / reviews[0]["directory"] / "EXPECTED.json")
    review2_expected = load_json(repository / reviews[1]["directory"] / "EXPECTED.json")
    need(review1_expected["graph_sha256"] == candidate["graph_sha256"], "review1 graph identity")
    need(review2_expected["graph_sha256"] == candidate["graph_sha256"], "review2 graph identity")
    need(review1_expected["certificate_sha256"] == obstruction["certificate_sha256"], "review1 certificate identity")
    need(review2_expected["certificate_sha256"] == obstruction["certificate_sha256"], "review2 certificate identity")
    need(review1_expected["independent_rank_prime"] == reviews[0]["rank_primes"][0], "review1 rank prime")
    need(review2_expected["independent_rank_primes"] == reviews[1]["rank_primes"], "review2 rank primes")

    interface_dir = repository / downstream["directory"]
    interface_expected = load_json(interface_dir / "EXPECTED.json")
    interface_provenance = load_json(interface_dir / "PROVENANCE.json")
    interface_graph = load_json(interface_dir / "graph.json")
    interface_labels = set(interface_graph["labels"])
    interface_edges = {tuple(edge) for edge in interface_graph["edges"]}
    need(len(interface_labels) == downstream["forbidden_subgraph_vertices"], "interface vertices")
    need(len(interface_edges) == downstream["forbidden_subgraph_edges"], "interface edges")
    need(interface_labels <= labels and interface_edges <= source_edges, "interface source containment")
    need(interface_expected["four_colourable"] is downstream["forbidden_subgraph_four_colourable"], "interface colouring scope")
    need(interface_provenance["original_graph_sha256"] == candidate["graph_sha256"], "interface source graph")
    source_edge_order = {tuple(edge): index + 1 for index, edge in enumerate(candidate_graph["edges"])}
    variable_count, repair_variables = parse_repair_clause(interface_dir / "repair_clause.cnf")
    need(variable_count == candidate["edges"], "repair variable count")
    need(repair_variables == {source_edge_order[edge] for edge in interface_edges}, "repair clause edge mapping")

    return {
        "candidate_certificate": candidate_certificate,
        "candidate_expected": candidate_expected,
        "obstruction_expected": obstruction_expected,
        "review1_expected": review1_expected,
        "review2_expected": review2_expected,
        "interface_expected": interface_expected,
    }


def replay(repository: Path, work: Path, compiler: str, metadata: dict) -> dict:
    candidate_dir = repository / "hadwiger_nelson_h516_k23free_edge_repair"
    obstruction_dir = repository / "hadwiger_nelson_301_repair_plane_obstruction"
    review1_dir = repository / "hadwiger_nelson_301_repair_plane_obstruction_review1"
    review2_dir = repository / "hadwiger_nelson_301_repair_plane_obstruction_review2"
    interface_dir = repository / "hadwiger_nelson_301_forbidden_subgraph_interface"

    candidate_output = run(
        [sys.executable, "-B", str(candidate_dir / "verify.py"), "--work", str(work / "candidate")],
        repository,
    )
    candidate_receipt = json.loads(candidate_output)
    expected_candidate = dict(metadata["candidate_expected"]["verification"])
    expected_candidate["negative_controls"] = metadata["candidate_expected"]["negative_controls"]
    need(candidate_receipt == expected_candidate, "candidate verification receipt")

    strict_checker = work / "strict_lrat"
    run(
        [compiler, "-O3", "-std=c++17", str(candidate_dir / "strict_lrat.cpp"), "-o", str(strict_checker)],
        repository,
    )
    lrat_output = run(
        [str(strict_checker), str(candidate_dir / "four_colour.cnf"), str(candidate_dir / "four_colour.lrat")],
        repository,
    ).splitlines()
    need(len(lrat_output) == 2 and lrat_output[0] == "VERIFIED_STRICT_RUP_LRAT", "strict LRAT verdict")
    lrat_receipt = json.loads(lrat_output[1])
    expected_lrat = metadata["candidate_certificate"]["strict_LRAT"]
    for key in ("variables", "original_clauses", "additions", "deletions", "hints_used", "proof_lines"):
        need(lrat_receipt[key] == expected_lrat[key], f"strict LRAT field: {key}")

    obstruction_arguments = [str(obstruction_dir / "verify.py"), "--controls", "--positive"]
    obstruction_normal = run([sys.executable, "-B", *obstruction_arguments], repository)
    obstruction_optimized = run([sys.executable, "-B", "-O", *obstruction_arguments], repository)
    obstruction_expected_text = (obstruction_dir / "EXPECTED.json").read_text()
    need(obstruction_normal == obstruction_optimized == obstruction_expected_text, "obstruction receipts")

    review1_output = run(
        [sys.executable, "-B", str(review1_dir / "reproduce.py"), str(repository), str(work / "review1")],
        repository,
    )
    need(json.loads(review1_output) == metadata["review1_expected"], "review1 reproduction")

    review2_output = run(
        [sys.executable, "-B", str(review2_dir / "reproduce.py"), str(repository), str(work / "review2")],
        repository,
    )
    review2_receipt = json.loads(review2_output)
    need(review2_receipt["status"] == "REPRODUCED_ACCEPT_REVIEW_H3981", "review2 verdict")
    need(review2_receipt["source_modes_equal"] is True, "review2 source modes")
    need(review2_receipt["independent_modes_equal"] is True, "review2 independent modes")

    interface_arguments = [str(interface_dir / "verify.py"), "--controls"]
    interface_normal = run([sys.executable, "-B", *interface_arguments], repository)
    interface_optimized = run([sys.executable, "-B", "-O", *interface_arguments], repository)
    interface_expected_text = (interface_dir / "EXPECTED.json").read_text()
    need(interface_normal == interface_optimized == interface_expected_text, "interface receipts")

    return {
        "candidate_audit": True,
        "strict_LRAT": True,
        "obstruction_normal_optimized_equal": True,
        "review1_reproduced": True,
        "review2_reproduced": True,
        "downstream_interface_checked": True,
        "lrat_additions": lrat_receipt["additions"],
        "lrat_hints": lrat_receipt["hints_used"],
    }


def controls(evidence: dict, repository: Path) -> int:
    mutations = []
    changed = copy.deepcopy(evidence)
    changed["candidate"]["graph_sha256"] = "0" * 64
    mutations.append(changed)
    changed = copy.deepcopy(evidence)
    changed["candidate"]["geometric_claim"] = "realized"
    mutations.append(changed)
    changed = copy.deepcopy(evidence)
    changed["obstruction"]["chromatic_claim_used"] = True
    mutations.append(changed)
    changed = copy.deepcopy(evidence)
    changed["independent_acceptances"][0]["verdict"] = "REJECT"
    mutations.append(changed)
    changed = copy.deepcopy(evidence)
    changed["combined_conclusion"]["physical_candidate_survives"] = True
    mutations.append(changed)
    changed = copy.deepcopy(evidence)
    changed["downstream_interface"]["sufficient_for_realizability"] = True
    mutations.append(changed)
    changed = copy.deepcopy(evidence)
    changed["record_improvement"] = True
    mutations.append(changed)
    rejected = 0
    for changed in mutations:
        try:
            audit_metadata(changed, repository, check_evidence_hash=False, check_inputs=False)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("mutated handoff accepted")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=DEFAULT_REPOSITORY)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--cxx", default="g++")
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    repository = args.repository.resolve()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    evidence = load_json(HERE / "EVIDENCE.json")
    metadata = audit_metadata(evidence, repository)
    replay_report = replay(repository, work, args.cxx, metadata)
    report = {
        "verified": True,
        "status": evidence["status"],
        "evidence_sha256": EVIDENCE_SHA256,
        "graph_sha256": evidence["candidate"]["graph_sha256"],
        "candidate": {
            "vertices": evidence["candidate"]["vertices"],
            "edges": evidence["candidate"]["edges"],
            "chromatic_number": evidence["candidate"]["chromatic_number"],
            "vertex_critical": evidence["candidate"]["vertex_critical"],
            "K23_free": evidence["candidate"]["K23_free"],
            "K4_free": evidence["candidate"]["K4_free"],
            "strict_LRAT_additions": replay_report["lrat_additions"],
            "strict_LRAT_hints": replay_report["lrat_hints"],
        },
        "geometric_obstruction": {
            "maps_excluded": metadata["obstruction_expected"]["maps_excluded"],
            "mandatory_four_cycles": evidence["obstruction"]["mandatory_four_cycles"],
            "anchored_rank": evidence["obstruction"]["anchored_rank"],
            "coordinate_parameters": evidence["obstruction"]["coordinate_parameters"],
            "norm_identity_edges": evidence["obstruction"]["norm_identity_edges"],
            "unit_norm_sum": evidence["obstruction"]["unit_norm_sum"],
        },
        "independent_acceptances": [
            evidence["independent_acceptances"][0]["contribution"],
            evidence["independent_acceptances"][1]["contribution"],
        ],
        "downstream_interface": {
            "contribution": evidence["downstream_interface"]["contribution"],
            "forbidden_subgraph_vertices": evidence["downstream_interface"]["forbidden_subgraph_vertices"],
            "forbidden_subgraph_edges": evidence["downstream_interface"]["forbidden_subgraph_edges"],
            "repair_clause_literals": evidence["downstream_interface"]["repair_clause_literals"],
            "necessary_only": True,
            "independently_reviewed": False,
        },
        "replay": {key: value for key, value in replay_report.items() if key not in {"lrat_additions", "lrat_hints"}},
        "record_improvement": False,
    }
    if args.controls:
        report["mutations_rejected"] = controls(evidence, repository)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

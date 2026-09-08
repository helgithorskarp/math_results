#!/usr/bin/env python3
"""Independent exact audit of the bounded h3993 norm-edge repair family."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt
from pathlib import Path


D = Path(__file__).resolve().parent
SOURCE = D.parent / "hadwiger_nelson_h516_k23free_edge_repair"
INTERFACE = D.parent / "hadwiger_nelson_301_forbidden_subgraph_interface"
GRAPH_SHA = "7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb"
FIVE_SHA = "720466c1b6403de7d8247a33bb2844fccca306dfa21cc339b763968e6b2aea1d"
INTERFACE_SHA = "7119f912d305b5ae20439bd1a138d161277cd7fc95a82a09b23feec775f3de5c"
REPAIR_CLAUSE_SHA = "2e525fb48c247195fb20e6f4c323da5e0b87611c9f0ea25974485e94dbd3dfe3"
CNF_SHA = "60055ca362217f4c8f5121a7d245de67c146c1283dc0adf04457224e7db6ad86"
LRAT_XZ_SHA = "d6b008ff352d2be03b170f2a662480ddfb955f8e0e842acfe1be0dff374e4aee"
LRAT_RAW_SHA = "1d8bb23ff2caca290b6f3f77637c134c36ce9efb8d10961e768dffaac954413b"
LRAT_XZ_SIZE = 7_544_256
LRAT_RAW_SIZE = 28_590_220
ANCHOR = (1, 189, 192)


def need(ok: bool, why: str) -> None:
    if not ok:
        raise ValueError(why)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_lrat_manifest() -> None:
    receipt = json.loads((D / "OMITTED_LRAT.json").read_text())
    need(receipt == {
        "archive_filename": "five_chromatic_repairs.lrat.xz",
        "archive_format": "XZ-compressed ASCII LRAT",
        "archive_sha256": LRAT_XZ_SHA,
        "archive_size_bytes": LRAT_XZ_SIZE,
        "publication_status": "retained locally and excluded from Git pending explicit human approval",
        "raw_lrat_sha256": LRAT_RAW_SHA,
        "raw_lrat_size_bytes": LRAT_RAW_SIZE,
        "strict_replay_receipt": {
            "additions": 66120,
            "deletions": 72205,
            "hints_used": 4202594,
            "original_clauses": 6145,
            "proof_lines": 98052,
            "status": "VERIFIED_STRICT_RUP_LRAT",
            "variables": 1227,
        },
    }, "omitted LRAT manifest")


def check_local_lrat_archive(required: bool) -> bool:
    path = D / "five_chromatic_repairs.lrat.xz"
    if not path.exists():
        need(not required, "required local LRAT archive is absent")
        return False
    need(path.is_file(), "local LRAT archive is not a regular file")
    need(path.stat().st_size == LRAT_XZ_SIZE, "local LRAT archive size")
    need(sha(path) == LRAT_XZ_SHA, "local LRAT archive identity")
    return True


def rank_mod(rows, prime):
    basis = {}
    for row in rows:
        current = {column: value % prime for column, value in enumerate(row) if value % prime}
        while current:
            pivot = min(current)
            coefficient = current[pivot]
            if pivot not in basis:
                inverse = pow(coefficient, -1, prime)
                basis[pivot] = {column: value * inverse % prime for column, value in current.items()}
                break
            for column, value in basis[pivot].items():
                updated = (current.get(column, 0) - coefficient * value) % prime
                if updated:
                    current[column] = updated
                else:
                    current.pop(column, None)
    return len(basis)


def candidate_graph(source, deleted_edge):
    edges = [edge for edge in source["edges"] if tuple(edge) != deleted_edge]
    return {
        "claim": "single-edge repair candidate from h3993 necessary interface",
        "source_graph_sha256": GRAPH_SHA,
        "source_contribution": "bafkreib67bj2x2xsk2tsvlxtw4a2rp3z65eysayh7yiaxyc7e2v6wlwpsm",
        "interface_contribution": "bafkreiaht6wdxk2gkh4uor2pyynmnzkmeqofcybncbeo6rnaxcxxto7u2i",
        "deleted_edge": list(deleted_edge),
        "labels": source["labels"],
        "edges": edges,
        "vertices": len(source["labels"]),
        "edge_count": len(edges),
        "triangle": list(ANCHOR),
        "geometry_status": "UNDECIDED",
    }


def graph_bytes(graph):
    return (json.dumps(graph, separators=(",", ":"), sort_keys=True) + "\n").encode()


def geometry_audit(graph, cert):
    labels = graph["labels"]
    position = {vertex: index for index, vertex in enumerate(labels)}
    edges = {tuple(edge) for edge in graph["edges"]}
    need(labels == sorted(set(labels)) and len(labels) == 301, "geometry graph labels")
    need(graph["edges"] == [list(edge) for edge in sorted(edges)] and len(edges) == 1451, "geometry graph edges")
    need(cert["receipt"]["source_sha256"] == hashlib.sha256(graph_bytes(graph)).hexdigest(), "geometry source identity")
    rows = []
    used = set()
    kinds = {"edge": 0, "odd_wheel": 0}
    rim_lengths = {}
    for cycle in cert["cycles"]:
        need(len(cycle) == 4 and len(set(cycle)) == 4 and all(vertex in position for vertex in cycle), "four-cycle vertices")
        need(all(tuple(sorted((left, right))) in edges for left, right in zip(cycle, cycle[1:] + cycle[:1])), "four-cycle edge")
        for index in range(2):
            left, right = sorted((cycle[index], cycle[index + 2]))
            key = f"{left},{right}"
            need(key in cert["diagonal_obstructions"], "missing diagonal obstruction")
            witness = cert["diagonal_obstructions"][key]
            if key in used:
                continue
            used.add(key)
            need(witness["type"] in kinds, "diagonal obstruction type")
            kinds[witness["type"]] += 1
            if witness["type"] == "edge":
                need((left, right) in edges, "diagonal edge")
            else:
                hub = witness["hub"]
                rim = witness["rim"]
                rim_lengths[len(rim)] = rim_lengths.get(len(rim), 0) + 1
                need(len(rim) >= 3 and len(rim) % 2 == 1 and len(set(rim)) == len(rim), "odd simple rim")
                need(hub not in rim and all(vertex in position and vertex != right for vertex in rim + [hub]), "quotient wheel vertices")

                def quotient_edge(x, y):
                    if x == y:
                        return False
                    xs = [left, right] if x == left else [x]
                    ys = [left, right] if y == left else [y]
                    return any(tuple(sorted((u, v))) in edges for u in xs for v in ys)

                need(all(quotient_edge(hub, vertex) for vertex in rim), "wheel spokes")
                need(all(quotient_edge(x, y) for x, y in zip(rim, rim[1:] + rim[:1])), "wheel rim")
        row = [0] * len(labels)
        for index, vertex in enumerate(cycle):
            row[position[vertex]] = (-1) ** index
        rows.append(row)
    need(used == set(cert["diagonal_obstructions"]), "unused diagonal obstruction")
    anchor = cert["translation_anchor"]
    need(anchor in position, "translation anchor")
    rows.append([int(vertex == anchor) for vertex in labels])
    free = cert["free_labels"]
    need(len(set(free)) == len(free) and all(vertex in position for vertex in free), "free labels")
    need(len(cert["parametrization"]) == len(labels), "parametrization rows")
    parametrization = []
    for entries in cert["parametrization"]:
        row = {}
        for column, numerator, denominator in entries:
            need(type(column) is int and 0 <= column < len(free) and column not in row, "parameter column")
            need(type(numerator) is int and type(denominator) is int and denominator > 0 and numerator != 0, "rational entry")
            row[column] = Q(numerator, denominator)
        parametrization.append(row)
    for column, vertex in enumerate(free):
        need(parametrization[position[vertex]] == {column: Q(1)}, "free parameter row")
    for relation in rows:
        output = {}
        for index, coefficient in enumerate(relation):
            if coefficient:
                for column, value in parametrization[index].items():
                    output[column] = output.get(column, Q(0)) + coefficient * value
        need(all(value == 0 for value in output.values()), "parametrization relation")
    prime = cert["rank_prime"]
    need(type(prime) is int and 2 <= prime <= 2**31 - 1 and all(prime % divisor for divisor in range(2, isqrt(prime) + 1)), "rank prime")
    rank = rank_mod(rows, prime)
    need(rank == cert["affine_rank"] == len(labels) - len(free), "rank and nullity")
    quadratic = {}
    weight_sum = 0
    used_edges = set()
    for left, right, weight in cert["norm_weights"]:
        need((left, right) in edges and (left, right) not in used_edges, "norm edge")
        need(type(weight) is int and weight != 0, "norm weight")
        used_edges.add((left, right))
        weight_sum += weight
        difference = parametrization[position[left]].copy()
        for column, value in parametrization[position[right]].items():
            difference[column] = difference.get(column, Q(0)) - value
        difference = {column: value for column, value in difference.items() if value}
        for i, x in difference.items():
            for j, y in difference.items():
                quadratic[i, j] = quadratic.get((i, j), Q(0)) + weight * x * y
    need(weight_sum == cert["weight_sum"] and weight_sum != 0, "nonzero norm sum")
    need(all(value == 0 for value in quadratic.values()), "quadratic identity")
    receipt = cert["receipt"]
    need(receipt["contradictory_norm_identity_found"] is True, "obstruction receipt")
    need(receipt["anchored_rank"] == rank and receipt["coordinate_parameters"] == len(free), "rank receipt")
    need(receipt["mandatory_four_cycles"] == len(rows) - 1, "cycle receipt")
    need(receipt["norm_identity_edges"] == len(used_edges) and receipt["unit_norm_sum"] == weight_sum, "norm receipt")
    return {
        "cycles": len(rows) - 1,
        "diagonal_obstructions": len(used),
        "obstruction_types": kinds,
        "odd_wheel_rim_lengths": dict(sorted(rim_lengths.items())),
        "rank": rank,
        "parameters": len(free),
        "norm_edges": len(used_edges),
        "norm_sum": weight_sum,
    }


def cnf_bytes(labels, edges, repair_cases):
    position = {vertex: index for index, vertex in enumerate(labels)}
    gates = [4 * len(labels) + index + 1 for index in range(len(repair_cases))]
    auxiliaries = [4 * len(labels) + len(repair_cases) + index + 1 for index in range(len(repair_cases) - 1)]
    gate = dict(zip(repair_cases, gates))
    clauses = []
    for vertex in labels:
        clauses.append([4 * position[vertex] + colour + 1 for colour in range(4)])
    for left, right in edges:
        prefix = [gate[(left, right)]] if (left, right) in gate else []
        for colour in range(4):
            clauses.append(prefix + [-4 * position[left] - colour - 1, -4 * position[right] - colour - 1])
    for colour, vertex in enumerate(ANCHOR):
        clauses.append([4 * position[vertex] + colour + 1])
    clauses.append(gates)
    clauses.append([-gates[0], auxiliaries[0]])
    for index in range(1, len(gates) - 1):
        clauses.append([-gates[index], auxiliaries[index]])
        clauses.append([-auxiliaries[index - 1], auxiliaries[index]])
        clauses.append([-gates[index], -auxiliaries[index - 1]])
    clauses.append([-gates[-1], -auxiliaries[-1]])
    lines = [f"p cnf {4 * len(labels) + len(gates) + len(auxiliaries)} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode()


def audit(classification):
    check_lrat_manifest()
    need(sha(SOURCE / "graph.json") == GRAPH_SHA, "source graph identity")
    need(sha(SOURCE / "five_colouring.json") == FIVE_SHA, "source five-colouring identity")
    need(sha(INTERFACE / "certificate.json") == INTERFACE_SHA, "interface identity")
    need(sha(INTERFACE / "repair_clause.cnf") == REPAIR_CLAUSE_SHA, "repair clause identity")
    source = json.loads((SOURCE / "graph.json").read_text())
    labels = source["labels"]
    edges = [tuple(edge) for edge in source["edges"]]
    edge_set = set(edges)
    need(labels == sorted(set(labels)) and len(labels) == 301, "source labels")
    need(edges == sorted(edge_set) and len(edges) == 1452, "source edges")
    interface = json.loads((INTERFACE / "certificate.json").read_text())
    norm_edges = {(left, right) for left, right, weight in interface["norm_weights"] if weight}
    need(len(norm_edges) == 18, "interface norm support")
    lines = [line for line in (INTERFACE / "repair_clause.cnf").read_text().splitlines() if line and not line.startswith("c")]
    need(lines[0] == "p cnf 1452 1", "repair clause header")
    repair_indices = {-int(value) - 1 for value in lines[1].split()[:-1]}
    need(len(repair_indices) == 690, "repair clause variables")
    repair_edges = {edges[index] for index in repair_indices}
    need(norm_edges <= repair_edges, "norm support lies in repair clause")
    cases = classification["cases"]
    need(len(cases) == 18 and {tuple(row["edge"]) for row in cases} == norm_edges, "classified norm support")
    need(len({row["source_edge_index_one_based"] for row in cases}) == 18, "source edge indices")
    for row in cases:
        edge = tuple(row["edge"])
        need(edges[row["source_edge_index_one_based"] - 1] == edge, "source edge index")
    four = [row for row in cases if row["classification"] == "FOUR_COLOURABLE"]
    exact = [row for row in cases if row["classification"] == "EXACTLY_FIVE_CHROMATIC_AND_NO_PLANE_UNIT_EDGE_MAP"]
    need(len(four) == classification["four_colourable_cases"] == 6, "four-colourable count")
    need(len(exact) == classification["exactly_five_nonrealizable_cases"] == 12, "five/nonrealizable count")
    for row in four:
        deleted = tuple(row["edge"])
        word = row["four_colouring_word"]
        need(len(word) == len(labels) and set(word) <= set("0123"), "four-colouring word")
        colouring = dict(zip(labels, map(int, word)))
        need(all(edge == deleted or colouring[edge[0]] != colouring[edge[1]] for edge in edges), "four-colouring edge")
    source_five = json.loads((SOURCE / "five_colouring.json").read_text())["colours"]
    need(set(source_five) == set(map(str, labels)) and all(source_five[str(left)] != source_five[str(right)] for left, right in edges), "source five-colouring")
    geometry = {}
    for row in exact:
        deleted = tuple(row["edge"])
        graph = candidate_graph(source, deleted)
        path = D / row["geometric_certificate"]
        need(sha(path) == row["geometric_certificate_sha256"], "geometric certificate identity")
        cert = json.loads(path.read_text())
        need(cert["receipt"] == row["geometric_receipt"], "geometric receipt identity")
        geometry[f"{deleted[0]},{deleted[1]}"] = geometry_audit(graph, cert)
    repair_cases = [tuple(row["edge"]) for row in exact]
    rebuilt = cnf_bytes(labels, edges, repair_cases)
    need(rebuilt == (D / "five_chromatic_repairs.cnf").read_bytes(), "combined CNF reconstruction")
    need(hashlib.sha256(rebuilt).hexdigest() == CNF_SHA, "combined CNF identity")
    return {
        "verified": True,
        "source_vertices": len(labels),
        "source_edges": len(edges),
        "norm_support_repairs": len(cases),
        "four_colourable_repairs": len(four),
        "exactly_five_nonrealizable_repairs_if_LRAT_accepts": len(exact),
        "combined_CNF_variables": 4 * len(labels) + 2 * len(exact) - 1,
        "combined_CNF_clauses": 6145,
        "combined_CNF_sha256": CNF_SHA,
        "compressed_LRAT_sha256": LRAT_XZ_SHA,
        "uncompressed_LRAT_sha256": LRAT_RAW_SHA,
        "geometric_audits": geometry,
        "family_decision": "no deletion of one h3993 norm-support edge is both non-four-colourable and plane unit-distance realizable",
    }


def controls(classification):
    rejected = []
    altered = copy.deepcopy(classification)
    row = next(row for row in altered["cases"] if row["classification"] == "FOUR_COLOURABLE")
    row["four_colouring_word"] = "0" * 301
    try:
        audit(altered)
    except ValueError:
        rejected.append("bad_four_colouring")
    else:
        raise ValueError("bad four-colouring accepted")
    altered = copy.deepcopy(classification)
    altered["cases"][0]["source_edge_index_one_based"] += 1
    try:
        audit(altered)
    except ValueError:
        rejected.append("bad_edge_index")
    else:
        raise ValueError("bad edge index accepted")
    exact = next(row for row in classification["cases"] if row["classification"].startswith("EXACTLY_FIVE"))
    graph = candidate_graph(json.loads((SOURCE / "graph.json").read_text()), tuple(exact["edge"]))
    cert = json.loads((D / exact["geometric_certificate"]).read_text())
    cert["norm_weights"][0][2] += 1
    cert["weight_sum"] += 1
    try:
        geometry_audit(graph, cert)
    except ValueError:
        rejected.append("bad_norm_identity")
    else:
        raise ValueError("bad norm identity accepted")
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", action="store_true")
    parser.add_argument(
        "--require-lrat-archive",
        action="store_true",
        help="require and hash-check the intentionally untracked generated LRAT archive",
    )
    args = parser.parse_args()
    classification = json.loads((D / "classification.json").read_text())
    result = audit(classification)
    expected = json.loads((D / "EXPECTED.json").read_text())
    need(json.loads(json.dumps(result)) == expected, "expected verification receipt")
    result["local_lrat_archive_checked"] = check_local_lrat_archive(args.require_lrat_archive)
    if args.controls:
        result["rejected_controls"] = controls(classification)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

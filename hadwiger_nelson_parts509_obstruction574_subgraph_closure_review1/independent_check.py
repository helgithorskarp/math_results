#!/usr/bin/env python3
"""Clean-room audit of the H574 hereditary four-colourability certificate.

No module from the reviewed contribution (or an earlier checker) is imported.
The program rebuilds the strict unit-distance graph with exact integer
arithmetic in Q(sqrt(3),sqrt(5),sqrt(11)), assembles all 509 deletion
colourings from their primitive data, and checks every retained edge.
"""

from argparse import ArgumentParser
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import lcm
from pathlib import Path


INPUT_HASHES = {
    "hadwiger_nelson_parts509_completion_census_degree9/points.tsv":
        "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    "hadwiger_nelson_parts509_swap_closure/completion_points.json":
        "b82909c48ce088deb89b555f4c8fa554bba44030570fdaaf0b9b607e9552a5a6",
    "hadwiger_nelson_parts509_s_replacement_budget/pool_S.json":
        "fd636275fccdd84266655ba9ada22412f7d2aef66a0ad66f6ee5bd738570939e",
    "hadwiger_nelson_parts509_pool_obstruction574/certificate.json":
        "327065c465ce0a52f7f5e783d5810ac68895edafb38d404feb031ff01380987c",
    "hadwiger_nelson_parts509_interface_lemma/interface_L.json":
        "a160340461815e57c46936fb7d0001b74881fe753d904a5ddc7fb866cfc29637",
    "hadwiger_nelson_parts509_obstruction574_subgraph_closure/certificate.json":
        "647c3011ac61449b274b1b8815ce17d1da6c948da54ba6ed79546eb856c20469",
}
EXPECTED_EDGE_SHA256 = "37d330b472e101c001e04aca6a1dc52ddf4f048d025adce0794f4e521682f575"
RADICANDS = (3, 5, 11)


class AuditFailure(RuntimeError):
    """A malformed input or failed mathematical check."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def digest(path: Path) -> str:
    result = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def exact_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def square_in_multiquadratic(coordinates: tuple[int, ...]) -> tuple[int, ...]:
    """Square coefficients in the squarefree bit-mask basis.

    Basis index i represents the product of sqrt(3), sqrt(5), sqrt(11)
    selected by the bits of i.  Repeated radicals contribute their radicands.
    """
    require(len(coordinates) == 8, "field element must have eight coefficients")
    result = [0] * 8
    for left, a in enumerate(coordinates):
        for right, b in enumerate(coordinates):
            factor = 1
            repeated = left & right
            for bit, radicand in enumerate(RADICANDS):
                if repeated & (1 << bit):
                    factor *= radicand
            result[left ^ right] += a * b * factor
    return tuple(result)


def squared_distance(first, second) -> tuple[int, ...]:
    dx = tuple(a - b for a, b in zip(first[0], second[0], strict=True))
    dy = tuple(a - b for a, b in zip(first[1], second[1], strict=True))
    sx = square_in_multiquadratic(dx)
    sy = square_in_multiquadratic(dy)
    return tuple(a + b for a, b in zip(sx, sy, strict=True))


def read_exact_points(repository: Path):
    original_path = repository / "hadwiger_nelson_parts509_completion_census_degree9/points.tsv"
    completion_path = repository / "hadwiger_nelson_parts509_swap_closure/completion_points.json"
    original = []
    for line in original_path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        require(len(row) == 16, "original coordinate width")
        original.append((row[:8], row[8:]))
    require(len(original) == 509, "original coordinate count")

    completion_raw = exact_json(completion_path)
    require(type(completion_raw) is dict and type(completion_raw.get("points")) is list,
            "completion point list")
    rational_completion = []
    denominator = 96
    for record in completion_raw["points"]:
        require(type(record) is dict and "x" in record and "y" in record,
                "completion point fields")
        x = tuple(Fraction(value) for value in record["x"])
        y = tuple(Fraction(value) for value in record["y"])
        require(len(x) == len(y) == 8, "completion coordinate width")
        for value in x + y:
            denominator = lcm(denominator, value.denominator)
        rational_completion.append((x, y))
    require(len(rational_completion) == 1158, "completion coordinate count")
    require(denominator == 288, "common coordinate denominator")

    points = [
        (tuple(value * (denominator // 96) for value in x),
         tuple(value * (denominator // 96) for value in y))
        for x, y in original
    ]
    for x, y in rational_completion:
        scaled = tuple(value * denominator for value in x + y)
        require(all(value.denominator == 1 for value in scaled), "nonintegral scaled point")
        points.append((tuple(int(value) for value in scaled[:8]),
                       tuple(int(value) for value in scaled[8:])))
    return denominator, points


def reconstruct_graph(repository: Path, pool_labels: list[int]):
    denominator, points = read_exact_points(repository)
    pool = exact_json(repository / "hadwiger_nelson_parts509_s_replacement_budget/pool_S.json")
    universe = tuple(sorted(pool["W_S"]))
    require(len(universe) == len(set(universe)) == 303, "pool universe size")
    require(pool_labels == sorted(set(pool_labels)), "H pool labels sorted and distinct")
    require(len(pool_labels) == 200 and set(pool_labels) <= set(universe), "H pool selection")
    labels = tuple(range(374)) + tuple(pool_labels)
    require(len(labels) == len(set(labels)) == 574, "H label count")
    require(all(type(label) is int and 0 <= label < len(points) for label in labels),
            "H label range")
    require(len({points[label] for label in labels}) == 574, "H coordinate collision")

    unit = (denominator * denominator,) + (0,) * 7
    edges = tuple(
        (left, right)
        for left, right in combinations(labels, 2)
        if squared_distance(points[left], points[right]) == unit
    )
    edge_bytes = "".join(f"{left},{right}\n" for left, right in edges).encode("ascii")
    require(len(edges) == 2707, "strict unit-edge count")
    require(sha256(edge_bytes).hexdigest() == EXPECTED_EDGE_SHA256,
            "strict unit-edge stream hash")
    return denominator, labels, edges


def validate_colouring(labels, position, edges, deleted: int, colours: str) -> int:
    require(type(deleted) is int and deleted in position, "deleted label")
    require(type(colours) is str and len(colours) == len(labels), "colour string length")
    require(set(colours) <= set(".0123"), "colour alphabet")
    dots = tuple(labels[index] for index, value in enumerate(colours) if value == ".")
    require(dots == (deleted,), "unique deletion marker")
    checked = 0
    for left, right in edges:
        if left == deleted or right == deleted:
            continue
        require(colours[position[left]] != colours[position[right]],
                f"monochromatic retained edge after deleting {deleted}: {left},{right}")
        checked += 1
    return checked


def require_exact_coverage(actual, expected, message: str) -> None:
    require(tuple(actual) == tuple(expected), message)


def expect_failure(action, message: str) -> None:
    try:
        action()
    except AuditFailure:
        return
    raise AuditFailure(message)


def audit_certificates(repository: Path, labels, edges):
    target = repository / "hadwiger_nelson_parts509_obstruction574_subgraph_closure"
    old = exact_json(repository / "hadwiger_nelson_parts509_pool_obstruction574/certificate.json")
    new = exact_json(target / "certificate.json")
    interfaces = exact_json(repository / "hadwiger_nelson_parts509_interface_lemma/interface_L.json")

    pool_labels = old["pool_labels"]
    require(tuple(new["labels"]) == labels, "new certificate label order")
    require_exact_coverage((row["vertex"] for row in old["deletions"]), pool_labels,
                           "old deletion coverage")
    require_exact_coverage((row["vertex"] for row in new["deletions"]), range(309),
                           "new deletion coverage")
    require(len(interfaces["classes"]) == 20, "interface record count")

    position = {label: index for index, label in enumerate(labels)}
    degrees = {label: 0 for label in labels}
    for left, right in edges:
        degrees[left] += 1
        degrees[right] += 1

    assembled = sha256()
    checked = 0
    retained_counts = []
    assembled_rows = []
    for row in old["deletions"]:
        pattern = row["pattern"]
        require(type(pattern) is int and 0 <= pattern < len(interfaces["classes"]),
                "old interface index")
        left = interfaces["classes"][pattern]["witness_colouring_L"]
        require(type(left) is str and len(left) == 374 and set(left) <= set("0123"),
                "old L colouring")
        colours = left + row["pool_colours"]
        count = validate_colouring(labels, position, edges, row["vertex"], colours)
        checked += count
        retained_counts.append(count)
        assembled_rows.append((row["vertex"], colours))
        assembled.update(f"{row['vertex']}:{colours}\n".encode("ascii"))
    for row in new["deletions"]:
        count = validate_colouring(labels, position, edges, row["vertex"], row["colours"])
        checked += count
        retained_counts.append(count)
        assembled_rows.append((row["vertex"], row["colours"]))
        assembled.update(f"{row['vertex']}:{row['colours']}\n".encode("ascii"))

    forced = set(pool_labels) | set(range(309))
    require(len(forced) == 509, "forced vertices must be distinct")
    expected_checks = sum(len(edges) - degrees[vertex] for vertex in forced)
    require(checked == expected_checks == 1_372_888, "retained-edge incidence count")

    # Three negative controls exercise the local checker and the exact coverage gate.
    deleted, valid = assembled_rows[-1]
    expect_failure(
        lambda: validate_colouring(labels, position, edges, deleted,
                                    valid.replace(".", "0", 1)),
        "missing deletion marker was accepted",
    )
    corrupt = list(valid)
    for left, right in edges:
        if deleted not in (left, right):
            corrupt[position[right]] = corrupt[position[left]]
            break
    expect_failure(
        lambda: validate_colouring(labels, position, edges, deleted, "".join(corrupt)),
        "monochromatic edge mutation was accepted",
    )
    expect_failure(
        lambda: require_exact_coverage(range(308), range(309), "truncated coverage"),
        "truncated coverage was accepted",
    )

    return {
        "old_pool_deletion_colourings": len(old["deletions"]),
        "new_L_deletion_colourings": len(new["deletions"]),
        "distinct_forced_vertices": len(forced),
        "verified_retained_edge_incidences": checked,
        "retained_edges_per_colouring": {
            "minimum": min(retained_counts),
            "maximum": max(retained_counts),
        },
        "assembled_witness_family_sha256": assembled.hexdigest(),
        "mutation_controls_rejected": 3,
        "all_subgraphs_through_order": len(forced) - 1,
        "all_such_subgraphs_four_colourable": True,
    }


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    repository = args.repository.resolve()

    observed_hashes = {}
    for relative, expected in INPUT_HASHES.items():
        path = repository / relative
        observed_hashes[relative] = digest(path)
        require(observed_hashes[relative] == expected, f"input hash: {relative}")

    old = exact_json(repository / "hadwiger_nelson_parts509_pool_obstruction574/certificate.json")
    denominator, labels, edges = reconstruct_graph(repository, old["pool_labels"])
    degree = {label: 0 for label in labels}
    for left, right in edges:
        degree[left] += 1
        degree[right] += 1
    certificates = audit_certificates(repository, labels, edges)

    report = {
        "verdict": "ACCEPTED",
        "reviewed_source_commit": "6fd4065d7351caf6959453351fe6f5545c54a2e1",
        "inputs": observed_hashes,
        "geometry": {
            "basis": "1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)",
            "coordinate_denominator": denominator,
            "vertices": len(labels),
            "unordered_pairs_tested": len(labels) * (len(labels) - 1) // 2,
            "strict_unit_edges": len(edges),
            "edge_sha256": EXPECTED_EDGE_SHA256,
            "degree_minimum": min(degree.values()),
            "degree_maximum": max(degree.values()),
        },
        "certificates": certificates,
        "logical_bridge": (
            "A subgraph on at most 508 vertices omits some member v of the "
            "509-element forced set; restriction of the checked colouring of H-v "
            "is therefore a proper four-colouring, also after arbitrary edge deletion."
        ),
        "solver_or_negative_certificate_used": False,
        "target_scope": "all subgraphs of the one explicit graph H574 through order 508",
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

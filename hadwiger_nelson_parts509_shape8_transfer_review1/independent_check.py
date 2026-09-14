#!/usr/bin/env python3
"""Independent audit of the fixed Parts a=8 physical transfer.

This checker imports no Python module from the reviewed package or its prior
geometry review.  It reconstructs the ambient strict unit-distance graph from
the original coordinate fixtures, checks all positive witnesses and cuts, and
builds a different negative certificate: a four-colouring CNF on all 508
vertices, with selector-guarded terminal pins for the twelve claimed forbidden
interface patterns.
"""

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
import json
from math import lcm
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "hadwiger_nelson_parts509_shape8_transfer"
PRIMES = (3, 5, 11)
HASHES = {
    "points": "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    "completion": "b82909c48ce088deb89b555f4c8fa554bba44030570fdaaf0b9b607e9552a5a6",
    "pool": "fd636275fccdd84266655ba9ada22412f7d2aef66a0ad66f6ee5bd738570939e",
    "interface": "a160340461815e57c46936fb7d0001b74881fe753d904a5ddc7fb866cfc29637",
    "certificate": "82d57df8861e2299ff33a1757924b5b353fdb172e7ac729a9e5d619d3461ac41",
    "cuts": "17277f736dbb3fe5aa184121be6d3e0b67f8e5d2a6e1711e388dbf48b723f2ec",
    "pool_five": "faeac9789caced4f18f2def2be3388f4827e0a28d6d0b5bb9b5d265ae1f3cbcc",
    "seed_hashes": "7ed42704af6167e5bf0fd82ebaa8269926cc91ce0c033827bb6137afcf3673ce",
    "seed_shape0_5": "1d9f366326772ee98e48a5671a1df03e502f740e18c5631d08365a5e99ffe7c6",
    "seed_budget": "7293207b667f1f6a8a2a7353645b78e45fdc2c1f864cdb741a3d5ba7d836df0a",
    "seed_shape6": "23c440f74f78a8f6adf675de4e5f284cda4d5b1fe1e353eac48efff381b46288",
    "seed_shape7": "a7bc0aadf72becb81cc66000fa5d00135ddbfa95fcb375f47d36c08ce4a80ade",
    "seed_shrunk": "7b17a4ce0504c679b396b647e83a82cfcf356f7a6073afeb7fcb54b8f82c90c0",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    answer = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def field_multiply(left, right):
    """Multiply in the mask basis of Q(sqrt(3),sqrt(5),sqrt(11))."""
    answer = [0] * 8
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            coefficient = a * b
            overlap = i & j
            for bit, prime in enumerate(PRIMES):
                if overlap & (1 << bit):
                    coefficient *= prime
            answer[i ^ j] += coefficient
    return tuple(answer)


def squared_distance(first, second):
    dx = tuple(a - b for a, b in zip(first[0], second[0], strict=True))
    dy = tuple(a - b for a, b in zip(first[1], second[1], strict=True))
    sx = field_multiply(dx, dx)
    sy = field_multiply(dy, dy)
    return tuple(a + b for a, b in zip(sx, sy, strict=True))


def read_geometry():
    originals_path = (
        REPOSITORY / "hadwiger_nelson_parts509_completion_census_degree9" /
        "points.tsv"
    )
    completion_path = (
        REPOSITORY / "hadwiger_nelson_parts509_swap_closure" /
        "completion_points.json"
    )
    pool_path = (
        REPOSITORY / "hadwiger_nelson_parts509_s_replacement_budget" /
        "pool_S.json"
    )
    require(digest(originals_path) == HASHES["points"], "original point hash")
    require(digest(completion_path) == HASHES["completion"], "completion hash")
    require(digest(pool_path) == HASHES["pool"], "pool hash")

    originals = []
    for line in originals_path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        require(len(row) == 16, ("original point width", len(originals)))
        originals.append((row[:8], row[8:]))
    require(len(originals) == 509, ("original point count", len(originals)))

    raw_completion = json.loads(completion_path.read_text())
    completion = []
    denominator = 96
    for record in raw_completion["points"]:
        point = (
            tuple(Fraction(coefficient) for coefficient in record["x"]),
            tuple(Fraction(coefficient) for coefficient in record["y"]),
        )
        require(len(point[0]) == len(point[1]) == 8, "completion point width")
        for coefficient in point[0] + point[1]:
            denominator = lcm(denominator, coefficient.denominator)
        completion.append(point)
    require(len(completion) == 1158, ("completion point count", len(completion)))

    points = [
        (
            tuple((denominator // 96) * coefficient for coefficient in point[0]),
            tuple((denominator // 96) * coefficient for coefficient in point[1]),
        )
        for point in originals
    ]
    def scaled(coefficient):
        value = denominator * coefficient
        require(value.denominator == 1, ("nonintegral scaled coefficient", coefficient))
        return value.numerator

    points.extend(
        (
            tuple(scaled(coefficient) for coefficient in point[0]),
            tuple(scaled(coefficient) for coefficient in point[1]),
        )
        for point in completion
    )
    require(denominator == 288, ("coordinate denominator", denominator))

    pool = json.loads(pool_path.read_text())
    universe = tuple(sorted(pool["W_S"]))
    require(universe[:135] == tuple(range(374, 509)), "original S indexing")
    require(universe[135:] == tuple(sorted(pool["Q5"])), "Q5 indexing")
    require(len(universe) == 303 and len(universe[135:]) == 168, "pool sizes")
    ambient_vertices = tuple(range(374)) + universe
    require(len(ambient_vertices) == len(set(ambient_vertices)) == 677,
            "ambient label count")
    require(len({points[v] for v in ambient_vertices}) == 677,
            "ambient coordinate collision")

    target_norm = (denominator * denominator,) + (0,) * 7
    ambient_edges = tuple(
        (first, second)
        for first, second in combinations(ambient_vertices, 2)
        if squared_distance(points[first], points[second]) == target_norm
    )
    require(len(ambient_edges) == 3400, ("ambient edge count", len(ambient_edges)))
    edge_bytes = "".join(f"{a},{b}\n" for a, b in ambient_edges).encode("ascii")
    require(
        sha256(edge_bytes).hexdigest() ==
        "64a0f52154cb05b657a320c16569316cd1cba90748ed6dff71d4f45ca862b550",
        "ambient edge stream hash",
    )
    return denominator, points, ambient_vertices, universe, ambient_edges


def proper_colouring(vertices, edges, word, colours, label):
    require(len(word) == len(vertices), (label, "word length", len(word)))
    require(set(word) <= set(map(str, range(colours))), (label, "alphabet"))
    require(len(vertices) == len(set(vertices)), (label, "duplicate labels"))
    colouring = dict(zip(vertices, map(int, word), strict=True))
    require(all(colouring[a] != colouring[b] for a, b in edges),
            (label, "monochromatic edge"))
    return colouring


def read_inputs():
    paths = {
        "interface": REPOSITORY / "hadwiger_nelson_parts509_interface_lemma" /
        "interface_L.json",
        "certificate": TARGET / "certificate.json",
        "cuts": TARGET / "colouring_cuts.json",
        "pool_five": TARGET / "pool_five_colouring.txt",
        "seed_hashes": TARGET / "seed_hashes.json",
    }
    for key, path in paths.items():
        require(digest(path) == HASHES[key], (key, "hash"))
    interface = json.loads(paths["interface"].read_text())
    certificate = json.loads(paths["certificate"].read_text())
    cuts = json.loads(paths["cuts"].read_text())
    pool_five = paths["pool_five"].read_text().strip()
    return interface, certificate, cuts, pool_five


def audit_fixed_graph(points, ambient_vertices, universe, ambient_edges,
                      interface, certificate, pool_five):
    class_rows = tuple(interface["classes"])
    source_words = tuple(row["witness_colouring_L"] for row in class_rows)
    pins = tuple(interface["interface_L"])
    nonorigin_pins = tuple(interface["interface_L_nonorigin"])
    require(interface["class_count"] == len(source_words) == 20, "source class count")
    require(len(pins) == 19 and pins[0] == 0 and pins[1:] == nonorigin_pins,
            "source terminal count")

    left_edges = tuple((a, b) for a, b in ambient_edges if b < 374)
    require(len(left_edges) == 1860, ("left edge count", len(left_edges)))
    for index, (row, word) in enumerate(zip(class_rows, source_words, strict=True)):
        proper_colouring(tuple(range(374)), left_edges, word, 4,
                         f"source class {index}")
        require(word[0] == "0", ("source origin pin", index))
        witness_interface = "".join(word[v] for v in nonorigin_pins)
        require(witness_interface == row["witness_interface"],
                ("source interface witness", index))
        images = []
        for image in permutations("123"):
            translation = str.maketrans("123", "".join(image))
            images.append(witness_interface.translate(translation))
        require(min(images) == row["class"], ("source orbit representative", index))
    restrictions = tuple("".join(word[v] for v in pins) for word in source_words)
    require(len(set(restrictions)) == 20, "source restrictions not distinct")

    cross_edges = tuple(
        edge for edge in ambient_edges if (edge[0] < 374) != (edge[1] < 374)
    )
    cross_pins = {
        a if a < 374 else b
        for a, b in cross_edges
    }
    require(len(cross_edges) == 36 and cross_pins == set(pins),
            ("ambient interface", len(cross_edges), sorted(cross_pins)))

    selected = tuple(certificate["X"])
    selected_set = set(selected)
    S = set(universe[:135])
    Q5 = set(universe[135:])
    require(selected == tuple(sorted(selected_set)) and selected_set <= set(universe),
            "selected pool labels")
    require(len(selected_set & S) == 126 and len(selected_set & Q5) == 8,
            "fixed a=8 shape")
    require(
        (certificate["source_order"], certificate["driver_order"],
         certificate["full_order"]) == (374, 134, 508),
        "reported support dimensions",
    )
    support = tuple(range(374)) + selected
    support_set = set(support)
    require(len(support) == 508 and len({points[v] for v in support}) == 508,
            "fixed support points")
    edges = tuple(
        (a, b) for a, b in ambient_edges if a in support_set and b in support_set
    )
    require(len(edges) == certificate["unit_edges"] == 2435,
            ("fixed edge count", len(edges)))

    allowed = tuple(certificate["allowed_classes"])
    forbidden = tuple(certificate["forbidden_classes"])
    require(allowed == (4, 7, 12, 13, 14, 15, 17, 19), "allowed class list")
    require(set(allowed).isdisjoint(forbidden), "relation overlap")
    require(sorted(allowed + forbidden) == list(range(20)), "relation partition")
    positive_rows = certificate["positive_words"]
    require(tuple(row["class"] for row in positive_rows) == allowed,
            "positive class coverage")
    for row in positive_rows:
        p = row["class"]
        colouring = proper_colouring(support, edges, row["word"], 4,
                                     f"positive class {p}")
        require(all(colouring[v] == int(source_words[p][v]) for v in pins),
                ("positive terminal mismatch", p))
    proper_colouring(support, edges, certificate["five_colouring"], 5,
                     "fixed five-colouring")
    proper_colouring(ambient_vertices, ambient_edges, pool_five, 5,
                     "ambient five-colouring")

    selected_cross = tuple(
        edge for edge in edges if (edge[0] < 374) != (edge[1] < 374)
    )
    selected_pins = {
        a if a < 374 else b
        for a, b in selected_cross
    }
    require(len(selected_cross) == 30 and selected_pins == set(pins),
            ("selected interface", len(selected_cross), sorted(selected_pins)))
    return {
        "source_words": source_words,
        "pins": pins,
        "support": support,
        "edges": edges,
        "allowed": allowed,
        "forbidden": forbidden,
        "ambient_cross_edges": len(cross_edges),
        "selected_cross_edges": len(selected_cross),
        "selected_interface_vertices": len(selected_pins),
    }


def parse_positive_dimacs(path, universe):
    rows = []
    lines = path.read_text(encoding="ascii").splitlines()
    header = lines[0].split()
    require(header[:2] == ["p", "cnf"], (path.name, "DIMACS header"))
    for line in lines[1:]:
        literals = tuple(map(int, line.split()))
        require(literals and literals[-1] == 0, (path.name, "unterminated clause"))
        clause = literals[:-1]
        require(clause and all(1 <= literal <= len(universe) for literal in clause),
                (path.name, "literal range"))
        rows.append(tuple(universe[literal - 1] for literal in clause))
    require(len(rows) == int(header[3]), (path.name, "clause count"))
    return rows


def old_constraints(universe):
    paths = {
        "seed_shape0_5": REPOSITORY /
        "hadwiger_nelson_parts509_pool_shape_closure/killing_sets.json",
        "seed_budget": REPOSITORY /
        "hadwiger_nelson_parts509_s_replacement_budget/certificate.json",
        "seed_shape6": REPOSITORY /
        "hadwiger_nelson_parts509_pool_shape6_verified/killing_clauses.cnf",
        "seed_shape7": REPOSITORY /
        "hadwiger_nelson_parts509_pool_shape7_verified/killing_clauses.cnf",
        "seed_shrunk": REPOSITORY /
        "hadwiger_nelson_parts509_pool_cover_shrink01/colourings.json",
    }
    for key, path in paths.items():
        require(digest(path) == HASHES[key], (key, "hash"))
    rows = [
        tuple(row["D"])
        for row in json.loads(paths["seed_shape0_5"].read_text())["sets"]
    ]
    rows.extend(
        tuple(row["D"])
        for row in json.loads(paths["seed_budget"].read_text())["killing_sets"]
    )
    rows.extend(parse_positive_dimacs(paths["seed_shape6"], universe))
    rows.extend(parse_positive_dimacs(paths["seed_shape7"], universe))
    rows.extend(
        tuple(row["D"])
        for row in json.loads(paths["seed_shrunk"].read_text())
    )
    normalized = {tuple(sorted(row)) for row in rows}
    require(len(normalized) == 17266, ("seed clause count", len(normalized)))

    published_hashes = json.loads((TARGET / "seed_hashes.json").read_text())
    for path_text, expected in published_hashes.items():
        require(digest(REPOSITORY / path_text) == expected,
                ("published seed hash", path_text))
    return normalized


def audit_cuts(universe, ambient_edges, source_words, cuts):
    pool_set = set(universe)
    S = set(universe[:135])
    Q5 = set(universe[135:])
    clauses = old_constraints(universe)
    strict_witnesses = []
    for row_number, row in enumerate(cuts, 1):
        deleted = tuple(row["D"])
        deleted_set = set(deleted)
        require(deleted == tuple(sorted(deleted_set)) and deleted_set <= pool_set,
                ("cut definition", row_number))
        word = row["c"]
        require(len(word) == len(universe) and set(word) <= set(".0123"),
                ("cut word", row_number))
        require({v for v, colour in zip(universe, word, strict=True) if colour == "."}
                == deleted_set, ("cut deletion word", row_number))
        p = row["p"]
        colouring = {v: int(source_words[p][v]) for v in range(374)}
        colouring.update(
            (v, int(colour))
            for v, colour in zip(universe, word, strict=True)
            if colour != "."
        )
        require(all(
            a not in colouring or b not in colouring or colouring[a] != colouring[b]
            for a, b in ambient_edges
        ), ("improper cut colouring", row_number))

        excluded = set(row["excluded_X"])
        require(len(excluded) == 134 and len(excluded & S) == 126 and
                len(excluded & Q5) == 8, ("cut shape", row_number))
        require(not excluded & deleted_set, ("cut does not exclude witness", row_number))
        require(all(excluded & set(clause) for clause in clauses),
                ("cut not a strict refinement", row_number))
        strict_witnesses.append(len(clauses))
        clauses.add(deleted)
    return tuple(len(row["D"]) for row in cuts), tuple(strict_witnesses)


def full_graph_cnf(support, edges, pins, source_words, forbidden):
    position = {vertex: index for index, vertex in enumerate(support)}

    def colour_variable(vertex, colour):
        return 4 * position[vertex] + colour + 1

    clauses = []
    for vertex in support:
        variables = [colour_variable(vertex, colour) for colour in range(4)]
        clauses.append(variables)
        clauses.extend([-a, -b] for a, b in combinations(variables, 2))
    for a, b in edges:
        for colour in range(4):
            clauses.append([-colour_variable(a, colour), -colour_variable(b, colour)])

    selector_start = 4 * len(support)
    selectors = tuple(selector_start + index + 1 for index in range(len(forbidden)))
    clauses.append(list(selectors))
    for selector, p in zip(selectors, forbidden, strict=True):
        for pin in pins:
            clauses.append([
                -selector,
                colour_variable(pin, int(source_words[p][pin])),
            ])
    variables = selector_start + len(selectors)
    encoded = (
        f"p cnf {variables} {len(clauses)}\n" +
        "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    ).encode("ascii")
    require(variables == 2044 and len(clauses) == 13525,
            ("independent CNF dimensions", variables, len(clauses)))
    return encoded, variables, len(clauses)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--kissat", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    args = parser.parse_args()
    require(bool(args.kissat) == bool(args.drat_trim),
            "provide both proof executables or neither")
    args.work.mkdir(parents=True, exist_ok=True)

    denominator, points, ambient_vertices, universe, ambient_edges = read_geometry()
    interface, certificate, cuts, pool_five = read_inputs()
    audit = audit_fixed_graph(
        points, ambient_vertices, universe, ambient_edges,
        interface, certificate, pool_five,
    )
    cut_sizes, strict_witnesses = audit_cuts(
        universe, ambient_edges, audit["source_words"], cuts,
    )
    encoded, variables, clause_count = full_graph_cnf(
        audit["support"], audit["edges"], audit["pins"],
        audit["source_words"], audit["forbidden"],
    )
    cnf = args.work / "forbidden-full-graph.cnf"
    cnf.write_bytes(encoded)
    result = {
        "status": "POSITIVE_AND_INDEPENDENT_CNF_VERIFIED_PROOF_NOT_RUN",
        "geometry": {
            "field": "Q(sqrt(3),sqrt(5),sqrt(11))",
            "common_denominator": denominator,
            "ambient_points": len(ambient_vertices),
            "ambient_unit_edges": len(ambient_edges),
            "fixed_points": len(audit["support"]),
            "fixed_unit_edges": len(audit["edges"]),
            "ambient_cross_edges": audit["ambient_cross_edges"],
            "selected_cross_edges": audit["selected_cross_edges"],
            "selected_interface_vertices": audit["selected_interface_vertices"],
        },
        "relation": {
            "input_classes": len(audit["source_words"]),
            "allowed_classes": list(audit["allowed"]),
            "forbidden_classes": list(audit["forbidden"]),
            "positive_words_checked": len(audit["allowed"]),
            "terminal_count": len(audit["pins"]),
        },
        "cuts": {
            "sizes": list(cut_sizes),
            "strict_against_prior_clause_counts": list(strict_witnesses),
        },
        "independent_cnf": {
            "encoding": "all 508 vertices exactly-one plus physical edges and terminal pins",
            "variables": variables,
            "clauses": clause_count,
            "sha256": digest(cnf),
        },
        "target_four_colourable": True,
        "record_candidate": False,
    }

    if args.kissat:
        proof = args.work / "forbidden-full-graph.drat"
        solver_log = args.work / "solver.log"
        checker_log = args.work / "checker.log"
        with solver_log.open("w") as stream:
            solver = subprocess.run(
                [str(args.kissat.resolve()), "--time=300", "-f", str(cnf), str(proof)],
                stdout=stream,
                stderr=subprocess.STDOUT,
                check=False,
            )
        require(solver.returncode == 20, ("Kissat did not prove UNSAT", solver.returncode))
        with checker_log.open("w") as stream:
            checker = subprocess.run(
                [str(args.drat_trim.resolve()), str(cnf), str(proof)],
                stdout=stream,
                stderr=subprocess.STDOUT,
                check=False,
            )
        require(checker.returncode == 0 and "s VERIFIED" in checker_log.read_text(),
                ("DRAT proof not verified", checker.returncode))
        result.update({
            "status": "INDEPENDENT_FULL_GRAPH_RELATION_VERIFIED",
            "proof": {
                "bytes": proof.stat().st_size,
                "sha256": digest(proof),
                "solver_sha256": digest(args.kissat),
                "checker_sha256": digest(args.drat_trim),
            },
        })
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

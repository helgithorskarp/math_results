#!/usr/bin/env python3
"""Independent audit of the nine-branch Ramsey(5,5) tail selector.

This checker imports no module from the reviewed package.  It parses the
Ramsey(3,5,12) graph6 input independently, reconstructs the physical variable
map and both complete CNF encodings from their mathematical definitions, and
checks the residual-repacking and restricted block-symmetry mechanisms.  If
``--cnf-dir`` is supplied, every byte of ``direct.cnf`` and ``factored.cnf``
is compared with the independent reconstruction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from math import comb
from pathlib import Path


TARGET_MANIFEST_SHA256 = (
    "78ccc0f542611ab22ba331b3c43b3c4c383de55995fe291ed925faac1e1c3548"
)
PARENT_MANIFEST_SHA256 = (
    "5d1e479ae9d8e9d33a013029096ea73409607923e96a703033b9ea2feb8b1a8c"
)
CATALOG_SHA256 = (
    "322e7a54e67f4201bd37998ab420afb3eee41b1dcd6b277b7f055bda152da95e"
)
ALL_SELECTORS = (1 << 12) - 1
N = 43
TAIL_START = 31
SELECTORS = tuple(range(796, 808))


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def verify_manifest(directory: Path, expected_hash: str, expected_count: int) -> int:
    manifest = directory / "SHA256SUMS"
    require(file_sha256(manifest) == expected_hash,
            f"manifest identity mismatch: {directory.name}")
    count = 0
    for line in manifest.read_text().splitlines():
        digest, name = line.split("  ", 1)
        require(file_sha256(directory / name) == digest,
                f"manifest entry mismatch: {directory.name}/{name}")
        count += 1
    require(count == expected_count,
            f"manifest entry count mismatch: {directory.name}")
    return count


def parse_graph6(record: str) -> tuple[int, ...]:
    """Parse a small graph6 record directly into red-neighbour bit masks."""
    require(record and all(63 <= ord(char) <= 126 for char in record),
            "graph6 alphabet")
    order = ord(record[0]) - 63
    require(order == 12, "catalog order")
    payload = []
    for char in record[1:]:
        value = ord(char) - 63
        payload.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    required = comb(order, 2)
    require(len(payload) == required and not any(payload[required:]),
            "graph6 payload length or padding")
    adjacency = [0] * order
    position = 0
    for high in range(1, order):
        for low in range(high):
            if payload[position]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            position += 1
    return tuple(adjacency)


def is_red_clique(vertices, adjacency) -> bool:
    return all((adjacency[u] >> v) & 1 for u, v in combinations(vertices, 2))


def is_blue_clique(vertices, adjacency) -> bool:
    return all(not ((adjacency[u] >> v) & 1)
               for u, v in combinations(vertices, 2))


def edge_count(mask: int, adjacency) -> int:
    vertices = [v for v in range(12) if mask >> v & 1]
    return sum((adjacency[u] >> v) & 1 for u, v in combinations(vertices, 2))


def partition_counts(adjacency) -> tuple[int, int, int, int]:
    """Count three named independent triples, leaving a fourth triple."""
    triples = [sum(1 << v for v in q)
               for q in combinations(range(12), 3)
               if is_blue_clique(q, adjacency)]
    states = {0: 1}
    for _ in range(3):
        following = defaultdict(int)
        for used, multiplicity in states.items():
            for triple in triples:
                if not used & triple:
                    following[used | triple] += multiplicity
        states = following
    counts = [0, 0, 0, 0]
    for used, multiplicity in states.items():
        remainder = ALL_SELECTORS ^ used
        require(remainder.bit_count() == 3, "repacking remainder size")
        counts[edge_count(remainder, adjacency)] += multiplicity
    return tuple(counts)


def load_catalog(path: Path):
    require(file_sha256(path) == CATALOG_SHA256, "catalog identity")
    records = path.read_text().splitlines()
    require(len(records) == 12 and len(set(records)) == 12,
            "catalog cardinality or duplicates")
    graphs = [parse_graph6(record) for record in records]
    distributions = []
    for index, graph in enumerate(graphs):
        require(not any(is_red_clique(q, graph)
                        for q in combinations(range(12), 3)),
                f"catalog red triangle: {index}")
        require(not any(is_blue_clique(q, graph)
                        for q in combinations(range(12), 5)),
                f"catalog blue K5: {index}")
        counts = partition_counts(graph)
        require(counts[3] == 0 and sum(counts[:3]) > 0,
                f"catalog graph cannot be repacked: {index}")
        distributions.append(counts)
    totals = tuple(sum(row[t] for row in distributions) for t in range(4))
    require(totals == (43536, 52278, 26814, 0),
            f"unexpected ordered repacking totals: {totals}")
    return records, graphs, distributions, totals


def clean_clause(literals):
    values = set(literals)
    if 1 in values or any(-literal in values
                          for literal in values if literal != -1):
        return None
    values.discard(-1)
    return tuple(sorted(values, key=lambda literal: (abs(literal), literal)))


class IndependentEncoding:
    def __init__(self, graphs):
        self.graphs = graphs
        self.blocks = [tuple(range(4 * index, 4 * index + 4))
                       for index in range(7)] + [(28, 29, 30)]
        self.fixed = {}
        for index, block in enumerate(self.blocks):
            expression = 1 if index < 5 or index == 7 else 794 + index - 5
            for pair in combinations(block, 2):
                self.fixed[pair] = expression
        self.free = {}
        next_variable = 2
        for pair in combinations(range(N), 2):
            if pair[0] < TAIL_START and pair not in self.fixed:
                self.free[pair] = next_variable
                next_variable += 1
        require(next_variable == 794 and len(self.free) == 792,
                "physical variable map")

        self.tail_tables = {}
        for u, v in combinations(range(TAIL_START, N), 2):
            self.tail_tables[u, v] = sum(
                (((graph[u - TAIL_START] >> (v - TAIL_START)) & 1) << index)
                for index, graph in enumerate(graphs)
            )

        canonical_masks = set()
        self.tail_cases = 0
        for size in range(2, 6):
            for subset in combinations(range(TAIL_START, N), size):
                for color in (1, 0):
                    active = self.active_table(subset, color)
                    canonical_masks.add(min(active, ALL_SELECTORS ^ active))
                    for selected, graph in enumerate(graphs):
                        direct = all(
                            bool((graph[u - TAIL_START] >> (v - TAIL_START)) & 1)
                            == bool(color)
                            for u, v in combinations(subset, 2)
                        )
                        require(direct == bool(active >> selected & 1),
                                "tail truth-table case")
                        self.tail_cases += 1
        canonical_masks.discard(0)
        self.canonical_masks = tuple(sorted(canonical_masks))
        require(len(self.canonical_masks) == 227, "tail predicate count")

    def edge_expression(self, pair):
        return self.fixed.get(pair, self.free.get(pair))

    def active_table(self, subset, color: int) -> int:
        active = ALL_SELECTORS
        for pair in combinations(subset, 2):
            if pair[0] >= TAIL_START:
                table = self.tail_tables[pair]
                active &= table if color else ALL_SELECTORS ^ table
        return active

    def predicate_variables(self):
        return {mask: 808 + index
                for index, mask in enumerate(self.canonical_masks)}

    def forbidden(self, subset, color: int, factored: bool, guards=()):
        active = self.active_table(subset, color)
        if active == 0:
            return None
        misses = ALL_SELECTORS ^ active
        literals = list(guards)
        if factored and misses:
            canonical = min(active, misses)
            flag = self.predicate_variables()[canonical]
            literals.append(flag if canonical == misses else -flag)
        elif not factored:
            literals.extend(796 + selected for selected in range(12)
                            if misses >> selected & 1)
        for pair in combinations(subset, 2):
            if pair[0] >= TAIL_START:
                continue
            expression = self.edge_expression(pair)
            require(expression is not None, f"missing edge expression: {pair}")
            literals.append(-expression if color else expression)
        return clean_clause(literals)

    def signature(self, vertex):
        return tuple(self.free[row, vertex] for row in range(3, -1, -1))

    def block_key(self, block_index):
        return tuple(bit for vertex in self.blocks[block_index]
                     for bit in self.signature(vertex))

    def comparison_specs(self):
        specs = []
        for block_index in range(1, 8):
            block = self.blocks[block_index]
            for left, right in zip(block, block[1:]):
                specs.append((self.signature(left), self.signature(right), (),
                              f"vertices {left}>={right}"))
        for left, right in ((1, 2), (2, 3), (3, 4)):
            specs.append((self.block_key(left), self.block_key(right), (),
                          f"red blocks {left}>={right}"))
        specs.extend([
            (self.block_key(4), self.block_key(5), (-794,),
             "blocks 4>=5 when block5 red"),
            (self.block_key(5), self.block_key(6), (794,),
             "blocks 5>=6 when block5 blue"),
            (self.block_key(5), self.block_key(6), (-795,),
             "blocks 5>=6 when block6 red"),
        ])
        return specs

    def symmetry_clauses(self, factored: bool):
        next_auxiliary = 808 + (len(self.canonical_masks) if factored else 0)
        clauses = []
        for left, right, guards, _description in self.comparison_specs():
            prefix = 1
            for position, (x, y) in enumerate(zip(left, right)):
                clause = clean_clause((*guards, -prefix, x, -y))
                if clause is not None:
                    clauses.append(clause)
                if position + 1 < len(left):
                    auxiliary = next_auxiliary
                    next_auxiliary += 1
                    for raw in ((-auxiliary, prefix),
                                (-auxiliary, -x, y),
                                (-auxiliary, x, -y),
                                (-prefix, -x, -y, auxiliary),
                                (-prefix, x, y, auxiliary)):
                        clause = clean_clause(raw)
                        if clause is not None:
                            clauses.append(clause)
                    prefix = auxiliary
        variables = next_auxiliary - 1
        require(len(clauses) == 900, "symmetry clause count")
        require(variables == (1184 if factored else 957),
                "symmetry auxiliary interval")
        return clauses, variables

    def sections(self, factored: bool):
        predicates = self.predicate_variables() if factored else {}
        yield "constant", iter(((1,),))
        selectors = [SELECTORS]
        selectors.extend((-left, -right)
                         for left, right in combinations(SELECTORS, 2))
        yield "selectors", iter(selectors)
        yield "block_colors", iter(((794, -795),))
        definitions = (
            (-(796 + selected),
             flag if mask >> selected & 1 else -flag)
            for mask, flag in predicates.items()
            for selected in range(12)
        )
        yield "tail_predicates", definitions
        symmetry, _variables = self.symmetry_clauses(factored)
        yield "symmetry", iter(symmetry)

        def target_clauses():
            for subset in combinations(range(N), 5):
                for color in (1, 0):
                    clause = self.forbidden(subset, color, factored)
                    if clause is not None:
                        yield clause

        yield "target", target_clauses()

        def closure_clauses():
            for start, guard in ((20, 794), (24, 795)):
                for subset in combinations(range(start, N), 4):
                    clause = self.forbidden(subset, 1, factored, (guard,))
                    if clause is not None:
                        yield clause

        yield "greedy_closure", closure_clauses()

    def definition_checks(self) -> int:
        checks = 0
        for mask in self.canonical_masks:
            for selected in range(12):
                wanted = bool(mask >> selected & 1)
                for value in (False, True):
                    # Evaluate all twelve implications under a one-hot selector.
                    accepted = all(
                        selected != index
                        or value == bool(mask >> index & 1)
                        for index in range(12)
                    )
                    require(accepted == (value == wanted),
                            "predicate implication semantics")
                    checks += 1
        require(checks == 5448, "predicate definition check count")
        return checks

    def onehot_checks(self) -> int:
        checks = 0
        for assignment in range(1 << 12):
            at_least_one = assignment != 0
            at_most_one = assignment.bit_count() <= 1
            require((at_least_one and at_most_one) ==
                    (assignment.bit_count() == 1), "one-hot semantics")
            checks += 1
        return checks


def clause_value(clause, values) -> bool:
    return any(values[abs(literal)] == (literal > 0) for literal in clause)


def comparator_checks():
    """Exhaust the local equivalence and every four-bit projected comparator."""
    local = 0
    for prefix, x, y, following in product((False, True), repeat=4):
        clauses = (
            (not following or prefix),
            (not following or not x or y),
            (not following or x or not y),
            (not prefix or not x or not y or following),
            (not prefix or x or y or following),
        )
        require(all(clauses) == (following == (prefix and x == y)),
                "local prefix equivalence")
        local += 1

    projected = 0
    auxiliary_assignments = 0
    x_variables = (2, 3, 4, 5)
    y_variables = (6, 7, 8, 9)
    auxiliaries = (10, 11, 12)
    clauses = []
    prefix = 1
    for position, (x_var, y_var) in enumerate(zip(x_variables, y_variables)):
        clause = clean_clause((-prefix, x_var, -y_var))
        require(clause is not None, "standalone comparison clause")
        clauses.append(clause)
        if position < 3:
            z = auxiliaries[position]
            for raw in ((-z, prefix), (-z, -x_var, y_var),
                        (-z, x_var, -y_var), (-prefix, -x_var, -y_var, z),
                        (-prefix, x_var, y_var, z)):
                clause = clean_clause(raw)
                if clause is not None:
                    clauses.append(clause)
            prefix = z
    require(len(clauses) == 18, "standalone comparator clause count")
    for x_value in range(16):
        for y_value in range(16):
            satisfying_extensions = 0
            for auxiliary_bits in range(8):
                values = {1: True}
                for position, variable in enumerate(x_variables):
                    values[variable] = bool(x_value >> (3 - position) & 1)
                for position, variable in enumerate(y_variables):
                    values[variable] = bool(y_value >> (3 - position) & 1)
                for position, variable in enumerate(auxiliaries):
                    values[variable] = bool(auxiliary_bits >> position & 1)
                satisfying_extensions += all(clause_value(c, values)
                                             for c in clauses)
                auxiliary_assignments += 1
            require(satisfying_extensions == (1 if x_value >= y_value else 0),
                    "projected four-bit comparator semantics")
            projected += 1
    return {"local_recurrence_assignments": local,
            "four_bit_input_pairs": projected,
            "four_bit_auxiliary_assignments": auxiliary_assignments}


def guard_is_active(guards, c5: bool, c6: bool) -> bool:
    values = {794: c5, 795: c6}
    return all(values[abs(literal)] != (literal > 0) for literal in guards)


def core_action_checks(encoding: IndependentEncoding):
    block_specs = []
    for _left, _right, guards, description in encoding.comparison_specs():
        if description.startswith("blocks") or description.startswith("red blocks"):
            words = description.split()
            pair = words[2 if words[0] == "red" else 1].split(">=")
            block_specs.append(((int(pair[0]), int(pair[1])), guards))
    report = {}
    for red_fours in (5, 6, 7):
        c5 = red_fours >= 6
        c6 = red_fours >= 7
        active = [pair for pair, guards in block_specs
                  if guard_is_active(guards, c5, c6)]
        red_children = list(range(1, red_fours))
        blue_children = list(range(red_fours, 7))
        expected = list(zip(red_children, red_children[1:]))
        expected += list(zip(blue_children, blue_children[1:]))
        require(active == expected, f"wrong active block action for r={red_fours}")
        closure = set(range(4 * red_fours, N)) if red_fours < 7 else set()
        expected_closure = set().union(
            *(set(encoding.blocks[index]) for index in range(red_fours, 8)),
            set(range(TAIL_START, N)),
        ) if red_fours < 7 else set()
        require(closure == expected_closure,
                f"closure union does not consist of whole blocks for r={red_fours}")
        report[str(red_fours)] = {"active_block_comparisons": active,
                                  "closure_vertices": len(closure)}
    return report


def formula_metrics(encoding: IndependentEncoding, factored: bool,
                    cnf_path: Path | None):
    section_counts = {}
    clause_lengths = Counter()
    clauses = 0
    literals = 0
    variables = 1184 if factored else 957
    actual = cnf_path.open("rb") if cnf_path is not None else None
    declared_clauses = None
    if actual is not None:
        header = actual.readline()
        fields = header.decode().split()
        require(len(fields) == 4 and fields[:3] == ["p", "cnf", str(variables)],
                f"CNF header: {cnf_path}")
        declared_clauses = int(fields[3])
        require(header == f"p cnf {variables} {declared_clauses}\n".encode(),
                f"noncanonical CNF header: {cnf_path}")
    else:
        # Without a file, first derive the clause count needed in the header.
        for section, stream in encoding.sections(factored):
            section_counts[section] = sum(1 for _ in stream)
        declared_clauses = sum(section_counts.values())
        header = f"p cnf {variables} {declared_clauses}\n".encode()

    digest = hashlib.sha256()
    digest.update(header)
    byte_count = len(header)
    try:
        replay_counts = {}
        for section, stream in encoding.sections(factored):
            count = 0
            for clause in stream:
                line = (" ".join(map(str, clause)) + " 0\n").encode()
                digest.update(line)
                byte_count += len(line)
                clauses += 1
                literals += len(clause)
                clause_lengths[len(clause)] += 1
                if actual is not None:
                    require(actual.readline() == line,
                            f"CNF literal mismatch: {section}:{count}")
                count += 1
            replay_counts[section] = count
        if section_counts:
            require(replay_counts == section_counts, "nondeterministic reconstruction")
        else:
            section_counts = replay_counts
        require(clauses == declared_clauses, "CNF declared clause count")
        if actual is not None:
            require(actual.read() == b"", f"trailing CNF bytes: {cnf_path}")
            require(cnf_path.stat().st_size == byte_count, "CNF byte count")
            require(file_sha256(cnf_path) == digest.hexdigest(), "CNF hash")
    finally:
        if actual is not None:
            actual.close()
    return {
        "variables": variables,
        "clauses": clauses,
        "literals": literals,
        "bytes": byte_count,
        "sha256": digest.hexdigest(),
        "sections": section_counts,
        "clause_lengths": {str(key): clause_lengths[key]
                           for key in sorted(clause_lengths)},
        "cnf_bytewise_checked": cnf_path is not None,
    }


def check_published(package: Path, direct, factored):
    generation = json.loads((package / "GENERATION.json").read_text())
    validation = json.loads((package / "VALIDATION.json").read_text())
    for key in ("variables", "clauses", "bytes", "sha256"):
        require(generation[key] == factored[key], f"GENERATION field: {key}")
    require({str(key): value for key, value in generation["clause_lengths"].items()}
            == factored["clause_lengths"], "GENERATION clause lengths")
    for name, actual in (("direct", direct), ("factored", factored)):
        expected = validation[name]
        for key in ("clauses", "literals", "sha256", "sections"):
            require(expected[key] == actual[key], f"VALIDATION {name}: {key}")
    result = json.loads((package / "RESULT.json").read_text())
    require(result["status"] == "UNKNOWN" and not result["target_found"]
            and not result["family_excluded"], "solver receipt scope")
    require(result["proof_status"] == "PARTIAL_STREAM_NOT_A_CERTIFICATE",
            "partial proof status")
    require(result["cnf"]["sha256"] == factored["sha256"],
            "solver receipt CNF identity")
    return {
        "generation_and_validation_match": True,
        "historical_solver_receipt_status": "UNKNOWN",
        "historical_solver_outputs_reproduced": False,
        "solver_receipt_used_for_verdict": False,
    }


def main(repository: Path, cnf_dir: Path | None):
    repository = repository.resolve()
    package = repository / "ramsey_r55_tail12_selector"
    parent = repository / "ramsey_r55_global_greedy_closure"
    manifests = {
        "target": verify_manifest(package, TARGET_MANIFEST_SHA256, 15),
        "reviewed_parent": verify_manifest(parent, PARENT_MANIFEST_SHA256, 29),
    }
    records, graphs, distributions, totals = load_catalog(parent / "r35_12.g6")
    encoding = IndependentEncoding(graphs)
    require(encoding.tail_cases == 37752, "tail membership case count")
    checks = {
        "onehot_assignments": encoding.onehot_checks(),
        "predicate_definition_cases": encoding.definition_checks(),
        "tail_membership_cases": encoding.tail_cases,
        "comparator": comparator_checks(),
        "core_actions": core_action_checks(encoding),
    }
    direct_path = cnf_dir / "direct.cnf" if cnf_dir is not None else None
    factored_path = cnf_dir / "factored.cnf" if cnf_dir is not None else None
    if cnf_dir is not None:
        require(direct_path.is_file() and factored_path.is_file(),
                "both generated formulas are required")
    direct = formula_metrics(encoding, False, direct_path)
    factored = formula_metrics(encoding, True, factored_path)
    require(direct["clauses"] == 1483700 and direct["literals"] == 17653433
            and direct["bytes"] == 79532312
            and direct["sha256"] ==
            "c34213d0ce43639589930cb4c4529233e331ee8590cf4ace5fa950964ab14275",
            "direct formula identity")
    require(factored["clauses"] == 1486424 and factored["literals"] == 14224206
            and factored["bytes"] == 66250106
            and factored["sha256"] ==
            "91bf5f741a7e8d08ad1da1e347825cf572060db601bb40f2e185da2c6f734dce",
            "factored formula identity")
    require(direct["literals"] - factored["literals"] == 3429227,
            "literal reduction")
    require(direct["bytes"] - factored["bytes"] == 13282206,
            "byte reduction")
    published = check_published(package, direct, factored)
    return {
        "status": "VERIFIED_NINE_BRANCH_TAIL_SELECTOR",
        "manifests": manifests,
        "catalog": {
            "sha256": CATALOG_SHA256,
            "graphs": len(records),
            "all_red_triangle_free": True,
            "all_blue_K5_free": True,
            "ordered_repackings_by_final_red_edges": list(totals),
            "every_graph_repackable": all(sum(row[:3]) > 0
                                           for row in distributions),
            "completeness_imported": True,
        },
        "physical_encoding": {
            "vertices": N,
            "physical_edge_variables": len(encoding.free),
            "core_color_variables": 2,
            "tail_selectors": 12,
            "tail_predicates": len(encoding.canonical_masks),
            "prefix_variables": 150,
            "physical_five_subsets": comb(N, 5),
            "checks": checks,
        },
        "formulas": {"direct": direct, "factored": factored,
                     "literal_reduction": direct["literals"] - factored["literals"],
                     "byte_reduction": direct["bytes"] - factored["bytes"]},
        "published_consistency": published,
        "scope": {
            "covered_branches": 9,
            "other_h3863_branches": 30,
            "good43_constructed": False,
            "branch_excluded": False,
            "ramsey_bound_improved": False,
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", type=Path)
    parser.add_argument("--cnf-dir", type=Path)
    arguments = parser.parse_args()
    print(json.dumps(main(arguments.repository, arguments.cnf_dir),
                     indent=2, sort_keys=True))

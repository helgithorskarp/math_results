#!/usr/bin/env python3
"""Independent definition-level verifier for the physical core certificate."""

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time


N = 44
EDGES = tuple(combinations(range(N), 2))
EDGE_NUMBER = {edge: i for i, edge in enumerate(EDGES)}
EXPECTED_CATALOG_SHA256 = "6b138e64a9f97e200ff2451d8477337568162451119562c71c2c7be3e794b117"
EXPECTED_CERTIFICATE_SHA256 = "7835a04409f6577b0d27e02c2f5ef55fc33ce9d9e8fcc40637d42760033e2747"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def parse_catalog(path):
    require(sha256(path.read_bytes()).hexdigest() == EXPECTED_CATALOG_SHA256,
            "catalog digest")
    result = []
    for number, row in enumerate(path.read_text().splitlines(), 1):
        index_text, order_text, generator_text = row.split("|")
        require(int(index_text) == number, "consecutive catalog indices")
        generators = []
        for encoded in generator_text.split(";"):
            permutation = tuple(int(x) - 1 for x in encoded.split(","))
            require(len(permutation) == N and set(permutation) == set(range(N)),
                    f"permutation {number}")
            generators.append(permutation)
        # This traversal is intentionally separate from the producer's helper.
        reached = {0}
        frontier = [0]
        while frontier:
            point = frontier.pop()
            for permutation in generators:
                image = permutation[point]
                if image not in reached:
                    reached.add(image)
                    frontier.append(image)
        require(len(reached) == N, f"transitivity {number}")
        result.append((number, int(order_text), tuple(generators)))
    require(len(result) == 2113, "complete catalog length")
    return result


def orbit_partition(generators):
    """Pair orbits by explicit graph traversal, not producer union-find."""
    labels = [-1] * len(EDGES)
    next_label = 0
    for seed in range(len(EDGES)):
        if labels[seed] >= 0:
            continue
        labels[seed] = next_label
        frontier = [seed]
        while frontier:
            edge_number = frontier.pop()
            u, v = EDGES[edge_number]
            for permutation in generators:
                a, b = permutation[u], permutation[v]
                if a > b:
                    a, b = b, a
                image = EDGE_NUMBER[(a, b)]
                if labels[image] < 0:
                    labels[image] = next_label
                    frontier.append(image)
        next_label += 1
    return tuple(labels)


def is_refinement(fine, coarse):
    cell_image = {}
    for fine_cell, coarse_cell in zip(fine, coarse):
        if fine_cell in cell_image and cell_image[fine_cell] != coarse_cell:
            return False
        cell_image[fine_cell] = coarse_cell
    return True


def retained_representatives(partitions):
    representative = {}
    for index, partition in enumerate(partitions, 1):
        representative.setdefault(partition, index)
    configurations = tuple(representative)
    answer = []
    for partition in configurations:
        size = len(set(partition))
        if not any(len(set(candidate)) > size
                   and is_refinement(candidate, partition)
                   for candidate in configurations):
            answer.append(representative[partition])
    return tuple(answer), representative


def generated_group(generators, maximum):
    identity = tuple(range(N))
    elements = {identity}
    frontier = [identity]
    while frontier:
        first = frontier.pop()
        for second in generators:
            product = tuple(second[first[i]] for i in range(N))
            if product not in elements:
                elements.add(product)
                require(len(elements) <= maximum, "regular group size bound")
                frontier.append(product)
    return elements


def simplify(clauses, literal):
    reduced = []
    opposite = -literal
    for clause in clauses:
        if literal in clause:
            continue
        if opposite in clause:
            clause = tuple(x for x in clause if x != opposite)
            if not clause:
                return None
        reduced.append(clause)
    return tuple(reduced)


def list_dpll(clauses):
    """Exact tuple-clause DPLL, independent of the producer's bit masks/cache."""
    calls = 0

    def search(current):
        nonlocal calls
        calls += 1
        while True:
            unit = next((clause[0] for clause in current if len(clause) == 1), None)
            if unit is None:
                break
            current = simplify(current, unit)
            if current is None:
                return False
            if not current:
                return True
        if not current:
            return True
        # Branch from a shortest clause.  The producer instead uses global
        # bit-mask occurrence scores and memoization.
        branch_clause = min(current, key=lambda c: (len(c), c))
        variable = min(map(abs, branch_clause))
        positive = simplify(current, variable)
        if positive is not None and search(positive):
            return True
        negative = simplify(current, -variable)
        return negative is not None and search(negative)

    return search(tuple(clauses)), calls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--certificates", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    require(sha256(args.certificates.read_bytes()).hexdigest()
            == EXPECTED_CERTIFICATE_SHA256, "certificate digest")
    actions = parse_catalog(args.catalog)
    partitions = [orbit_partition(action[2]) for action in actions]
    retained, unique = retained_representatives(partitions)
    certificate = json.loads(args.certificates.read_text())
    require(certificate["catalog_sha256"] == EXPECTED_CATALOG_SHA256,
            "embedded catalog digest")
    require(tuple(certificate["retained_partition_representatives"]) == retained,
            "maximal refinement representatives")
    require(tuple(certificate["regular_indices_delegated_to_cayley44"])
            == (1, 2, 3, 4), "regular catalog boundary")
    for index in (1, 2, 3, 4):
        elements = generated_group(actions[index - 1][2], N)
        require(len(elements) == N == actions[index - 1][1],
                f"regular group order {index}")
        require(all(permutation == tuple(range(N))
                    or all(permutation[point] != point for point in range(N))
                    for permutation in elements), f"regular action {index}")
    require(set(retained[:4]) == {1, 2, 3, 4}, "regular representatives")
    expected_new = set(retained) - {1, 2, 3, 4}
    items = certificate["certificates"]
    require({item["index"] for item in items} == expected_new
            and len(items) == len(expected_new), "certificate coverage")

    total_clauses = 0
    total_calls = 0
    maximum_calls = 0
    for item in items:
        index = item["index"]
        partition = partitions[index - 1]
        require(item["edge_orbits"] == len(set(partition)),
                f"orbit count {index}")
        clauses = []
        physical = set()
        for record in item["clauses"]:
            color, vertices = record[0], tuple(record[1:])
            require(color in ("blue", "red") and len(vertices) == 5
                    and len(set(vertices)) == 5
                    and all(0 <= v < N for v in vertices),
                    f"physical clause {index}")
            key = (color, tuple(sorted(vertices)))
            require(key not in physical, f"duplicate physical clause {index}")
            physical.add(key)
            orbit_set = sorted({partition[EDGE_NUMBER[edge]]
                                for edge in combinations(sorted(vertices), 2)})
            sign = 1 if color == "blue" else -1
            clauses.append(tuple(sign * (orbit + 1) for orbit in orbit_set))
        satisfiable, calls = list_dpll(tuple(clauses))
        require(not satisfiable, f"core {index} is satisfiable")
        total_clauses += len(clauses)
        total_calls += calls
        maximum_calls = max(maximum_calls, calls)

    # Every omitted catalog partition is coarser than a retained one.
    for index, coarse in enumerate(partitions, 1):
        require(any(is_refinement(partitions[rep - 1], coarse)
                    for rep in retained), f"refinement cover {index}")
    report = {
        "status": "VERIFIED_COMPLETE_VERTEX_TRANSITIVE44_PUNCTURE_EXCLUSION",
        "catalog_actions": len(actions),
        "exact_labeled_edge_partitions": len(unique),
        "retained_maximal_partitions": len(retained),
        "prior_cayley44_partitions": 4,
        "new_physical_core_partitions": len(items),
        "physical_core_clauses": total_clauses,
        "list_dpll_calls_total": total_calls,
        "list_dpll_calls_max": maximum_calls,
        "elapsed_seconds": time.monotonic() - started,
    }
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()

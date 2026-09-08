#!/usr/bin/env python3
"""Independent audit of the degree-44 vertex-transitive exclusion.

This checker deliberately imports no Python from the reviewed packages.  It
represents pair-orbit partitions as tuples of 946-bit cell masks (rather than
the producer/verifier label-vector representations), recomputes refinement
maximality, checks every physical core record, and uses a fresh bit-mask DPLL.
The four regular actions are solved directly from all 44-choose-5 subsets.
"""

from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import argparse
import json
from pathlib import Path
import time


N = 44
EDGE_COUNT = N * (N - 1) // 2
FIVE_COUNT = 1_086_008
CATALOG_SHA256 = "6b138e64a9f97e200ff2451d8477337568162451119562c71c2c7be3e794b117"
CERTIFICATE_SHA256 = "7835a04409f6577b0d27e02c2f5ef55fc33ce9d9e8fcc40637d42760033e2747"
REGULAR_CORE_SHA256 = {
    "c11_c4": "f2abeaf86f69532c969d00cc02edc18eaae70e7d6c5348f5a5890907e6511e2a",
    "c11_v4": "4b16f214102056c71a840707bda20272bb13e18bda6ad721ab3c466423225da0",
    "c11_sd_c4": "35969ecdccf44a8bbbbf6d19b4be6fd9c3906e5dac87d315dc22488ac8fdd8cf",
    "c11_sd_v4": "ad669591f1b9445c637b9cf04b77c3ad0ebc76b2d7081d2b874272032917a2e4",
}


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def edge_number(u, v):
    """Rank {u,v} in lexicographic combinations(range(44),2), without a map."""
    if u > v:
        u, v = v, u
    return u * (2 * N - u - 1) // 2 + v - u - 1


def parse_catalog(path):
    need(digest(path) == CATALOG_SHA256, "catalog SHA-256")
    actions = []
    for expected_index, row in enumerate(path.read_text().splitlines(), 1):
        fields = row.split("|")
        need(len(fields) == 3, f"catalog row fields {expected_index}")
        index, order = map(int, fields[:2])
        need(index == expected_index, f"catalog indexing {expected_index}")
        generators = []
        for encoded in fields[2].split(";"):
            permutation = tuple(int(value) - 1 for value in encoded.split(","))
            need(len(permutation) == N, f"permutation degree {index}")
            image_mask = 0
            for image in permutation:
                need(0 <= image < N and not image_mask >> image & 1,
                     f"permutation bijection {index}")
                image_mask |= 1 << image
            need(image_mask == (1 << N) - 1,
                 f"permutation image set {index}")
            generators.append(permutation)
        need(generators, f"nonempty generators {index}")

        reached = 1
        frontier = [0]
        while frontier:
            point = frontier.pop()
            for generator in generators:
                image = generator[point]
                if not reached >> image & 1:
                    reached |= 1 << image
                    frontier.append(image)
        need(reached == (1 << N) - 1, f"transitive action {index}")
        actions.append((order, tuple(generators)))
    need(len(actions) == 2113, "2113 catalog records")
    return tuple(actions)


def pair_cells(generators):
    """Return a canonical tuple of pair-orbit bit masks by graph traversal."""
    unseen = (1 << EDGE_COUNT) - 1
    cells = []
    while unseen:
        seed_bit = unseen & -unseen
        seed = seed_bit.bit_length() - 1
        cell = seed_bit
        unseen ^= seed_bit
        frontier = [seed]
        while frontier:
            number = frontier.pop()
            # Invert the small lexicographic rank by a bounded scan.  This is
            # outside the inner generator loop in all later computations.
            offset = 0
            for u in range(N - 1):
                row_length = N - u - 1
                if number < offset + row_length:
                    v = u + 1 + number - offset
                    break
                offset += row_length
            for generator in generators:
                image = edge_number(generator[u], generator[v])
                bit = 1 << image
                if unseen & bit:
                    unseen ^= bit
                    cell |= bit
                    frontier.append(image)
        cells.append(cell)
    need(sum(cell.bit_count() for cell in cells) == EDGE_COUNT,
         "pair-cell cardinality")
    need(sum(cells) == (1 << EDGE_COUNT) - 1, "pair-cell disjoint union")
    return tuple(sorted(cells))


def finer_than(fine, coarse):
    """Test refinement directly on cell masks."""
    for small in fine:
        if not any(small & ~large == 0 for large in coarse):
            return False
    return True


def maximal_representatives(partitions):
    first = {}
    for index, partition in enumerate(partitions, 1):
        first.setdefault(partition, index)
    unique = tuple(first)
    maximal = []
    for coarse in unique:
        if not any(len(fine) > len(coarse) and finer_than(fine, coarse)
                   for fine in unique):
            maximal.append(first[coarse])
    return tuple(maximal), first


def edge_cell_lookup(cells):
    lookup = [-1] * EDGE_COUNT
    for cell_index, cell in enumerate(cells):
        remaining = cell
        while remaining:
            bit = remaining & -remaining
            lookup[bit.bit_length() - 1] = cell_index
            remaining ^= bit
    need(all(index >= 0 for index in lookup), "complete edge-cell lookup")
    return tuple(lookup)


def five_support(five, lookup):
    support = 0
    for u, v in combinations(five, 2):
        support |= 1 << lookup[edge_number(u, v)]
    return support


def solve_cnf(variable_count, clauses):
    """Exact DPLL on (positive-mask, negative-mask) clauses.

    Unit propagation is a full rescan.  Branching is false-first on a maximum
    unresolved-occurrence variable, with the largest index breaking ties.
    """
    clauses = tuple(dict.fromkeys(clauses))
    full = (1 << variable_count) - 1
    calls = conflicts = units = branches = 0

    @lru_cache(maxsize=None)
    def search(true_mask, false_mask):
        nonlocal calls, conflicts, units, branches
        calls += 1
        while True:
            assigned = true_mask | false_mask
            unresolved = []
            forced = 0
            forced_true = False
            for positive, negative in clauses:
                if positive & true_mask or negative & false_mask:
                    continue
                remaining_positive = positive & ~assigned
                remaining_negative = negative & ~assigned
                remaining = remaining_positive | remaining_negative
                if not remaining:
                    conflicts += 1
                    return False
                if remaining & (remaining - 1) == 0:
                    forced = remaining
                    forced_true = bool(remaining_positive)
                    break
                unresolved.append((remaining_positive, remaining_negative))
            if forced:
                units += 1
                if forced_true:
                    true_mask |= forced
                else:
                    false_mask |= forced
                continue
            if not unresolved:
                return True
            break

        scores = [0] * variable_count
        for positive, negative in unresolved:
            remaining = positive | negative
            while remaining:
                bit = remaining & -remaining
                scores[bit.bit_length() - 1] += 1
                remaining ^= bit
        available = full & ~(true_mask | false_mask)
        need(available, "DPLL branch availability")
        candidates = (index for index in range(variable_count)
                      if available >> index & 1)
        variable = max(candidates, key=lambda index: (scores[index], index))
        bit = 1 << variable
        branches += 1
        # False-first differs from both reviewed implementations.
        return search(true_mask, false_mask | bit) or search(true_mask | bit,
                                                             false_mask)

    satisfiable = search(0, 0)
    return satisfiable, {
        "calls": calls,
        "conflicts": conflicts,
        "units": units,
        "branches": branches,
        "cached_states": search.cache_info().currsize,
    }


def brute_force(variable_count, clauses):
    for assignment in range(1 << variable_count):
        if all(positive & assignment
               or negative & (((1 << variable_count) - 1) ^ assignment)
               for positive, negative in clauses):
            return True
    return False


def solver_controls():
    signed_clauses = []
    for encoding in range(1, 3 ** 3):
        positive = negative = 0
        value = encoding
        for variable in range(3):
            state = value % 3
            value //= 3
            if state == 1:
                positive |= 1 << variable
            elif state == 2:
                negative |= 1 << variable
        signed_clauses.append((positive, negative))
    checked = 0
    for width in range(4):
        for formula in combinations(signed_clauses, width):
            expected = brute_force(3, formula)
            observed, _ = solve_cnf(3, formula)
            need(observed == expected, f"DPLL truth-table control {formula}")
            checked += 1
    need(checked == 2952, "DPLL control count")
    return checked


def compose(left, right):
    return tuple(left[right[point]] for point in range(N))


def regular_group(generators, claimed_order):
    identity = tuple(range(N))
    group = {identity}
    frontier = [identity]
    while frontier:
        element = frontier.pop()
        for generator in generators:
            product = compose(generator, element)
            if product not in group:
                group.add(product)
                need(len(group) <= claimed_order,
                     "catalog order lower than generated subgroup")
                frontier.append(product)
    need(len(group) == claimed_order == N, "regular group order 44")
    need(all(element == identity
             or all(element[point] != point for point in range(N))
             for element in group), "semiregular degree-44 action")
    return group


def permutation_power(element, exponent):
    result = tuple(range(N))
    for _ in range(exponent):
        result = compose(result, element)
    return result


def element_order(element):
    identity = tuple(range(N))
    result = identity
    for exponent in range(1, N + 1):
        result = compose(result, element)
        if result == identity:
            return exponent
    raise AssertionError("element order does not divide 44")


def generated_by(elements):
    identity = tuple(range(N))
    group = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in elements:
            product = compose(generator, current)
            if product not in group:
                group.add(product)
                frontier.append(product)
    return group


def model_coordinates(name):
    if name.endswith("v4"):
        return tuple((a, b, c)
                     for c in (0, 1) for b in (0, 1) for a in range(11))
    return tuple((a, b) for b in range(4) for a in range(11))


def model_product(name, left, right):
    twisted = "_sd_" in name
    if len(left) == 3:
        a, b, c = left
        d, e, f = right
        return ((a + (-d if twisted and b else d)) % 11,
                b ^ e, c ^ f)
    a, b = left
    c, d = right
    return ((a + (-c if twisted and b % 2 else c)) % 11,
            (b + d) % 4)


def explicit_isomorphism(name, group):
    """Find and verify a coordinate-model isomorphism to a catalog group."""
    identity = tuple(range(N))
    orders = {element: element_order(element) for element in group}
    elevens = [element for element in group if orders[element] == 11]
    involutions = [element for element in group if orders[element] == 2]
    fours = [element for element in group if orders[element] == 4]
    witness = None
    for a in elevens:
        a_inverse = permutation_power(a, 10)
        if name == "c11_c4":
            for b in fours:
                if compose(a, b) == compose(b, a) \
                        and len(generated_by((a, b))) == N:
                    witness = (a, b, identity)
                    break
        elif name == "c11_v4":
            for b in involutions:
                if compose(a, b) != compose(b, a):
                    continue
                for c in involutions:
                    if b != c and compose(a, c) == compose(c, a) \
                            and compose(b, c) == compose(c, b) \
                            and len(generated_by((a, b, c))) == N:
                        witness = (a, b, c)
                        break
                if witness:
                    break
        elif name == "c11_sd_c4":
            for b in fours:
                b_inverse = permutation_power(b, 3)
                if compose(compose(b, a), b_inverse) == a_inverse \
                        and len(generated_by((a, b))) == N:
                    witness = (a, b, identity)
                    break
        elif name == "c11_sd_v4":
            for b in involutions:
                if compose(compose(b, a), b) != a_inverse:
                    continue
                for c in involutions:
                    if c != b and compose(a, c) == compose(c, a) \
                            and compose(b, c) == compose(c, b) \
                            and len(generated_by((a, b, c))) == N:
                        witness = (a, b, c)
                        break
                if witness:
                    break
        if witness:
            break
    need(witness is not None, f"coordinate generators for {name}")
    a, b, c = witness
    mapping = {}
    for coordinate in model_coordinates(name):
        if len(coordinate) == 2:
            i, j = coordinate
            image = compose(permutation_power(a, i),
                            permutation_power(b, j))
        else:
            i, j, k = coordinate
            image = compose(compose(permutation_power(a, i),
                                    permutation_power(b, j)),
                            permutation_power(c, k))
        mapping[coordinate] = image
    need(len(set(mapping.values())) == N and set(mapping.values()) == group,
         f"bijective coordinate map {name}")
    for left in mapping:
        for right in mapping:
            need(mapping[model_product(name, left, right)]
                 == compose(mapping[left], mapping[right]),
                 f"homomorphism {name}")
    return mapping


def parse_core(path):
    variables = expected_clauses = None
    clauses = []
    for row in path.read_text().splitlines():
        if not row or row.startswith("c"):
            continue
        if row.startswith("p "):
            fields = row.split()
            need(len(fields) == 4 and fields[1] == "cnf", "DIMACS header")
            variables, expected_clauses = map(int, fields[2:])
            continue
        literals = tuple(map(int, row.split()))
        need(literals and literals[-1] == 0 and 0 not in literals[:-1],
             "DIMACS clause terminator")
        positive = negative = 0
        for literal in literals[:-1]:
            bit = 1 << (abs(literal) - 1)
            if literal > 0:
                positive |= bit
            else:
                negative |= bit
        need(not positive & negative and bool(positive) != bool(negative),
             "physical monochromatic clause")
        clauses.append((positive, negative))
    need(variables is not None and len(clauses) == expected_clauses,
         "DIMACS clause count")
    need(len(set(clauses)) == len(clauses), "distinct core clauses")
    return variables, tuple(clauses)


def exact_model_formula(name):
    coordinates = model_coordinates(name)
    number = {coordinate: index for index, coordinate in enumerate(coordinates)}
    identity = coordinates[0]
    inverses = {}
    for element in coordinates:
        choices = [candidate for candidate in coordinates
                   if model_product(name, element, candidate) == identity
                   and model_product(name, candidate, element) == identity]
        need(len(choices) == 1, f"unique inverse {name}")
        inverses[element] = choices[0]
    unseen = set(coordinates[1:])
    inverse_pairs = []
    while unseen:
        element = min(unseen, key=number.__getitem__)
        pair = tuple(sorted((element, inverses[element]), key=number.__getitem__))
        inverse_pairs.append(pair)
        unseen.difference_update(pair)
    variable = {element: index
                for index, pair in enumerate(inverse_pairs)
                for element in pair}
    exact = set()
    anchored = 0
    for tail_numbers in combinations(range(1, N), 4):
        five = (identity,) + tuple(coordinates[value] for value in tail_numbers)
        support = 0
        for left, right in combinations(five, 2):
            difference = model_product(name, inverses[left], right)
            support |= 1 << variable[difference]
        exact.add((support, 0))
        exact.add((0, support))
        anchored += 1
    need(anchored == 123410, f"anchored five-set count {name}")
    return len(inverse_pairs), exact, anchored


def check_regular_action(index, action, cells, name, cayley_root):
    order, generators = action
    group = regular_group(generators, order)
    mapping = explicit_isomorphism(name, group)
    variables, exact, anchored = exact_model_formula(name)
    need(variables == len(cells), f"pair-orbit variables {name}")
    core_path = cayley_root / "cores" / f"{name}.core.cnf"
    need(digest(core_path) == REGULAR_CORE_SHA256[name], f"core digest {name}")
    core_variables, clauses = parse_core(core_path)
    need(core_variables == variables, f"core variables {name}")
    need(set(clauses) <= exact, f"all core clauses physical {name}")
    satisfiable, stats = solve_cnf(variables, clauses)
    need(not satisfiable, f"regular action {index} physical core is SAT")
    return {
        "index": index,
        "group_model": name,
        "catalog_order": order,
        "generated_group_order": len(group),
        "explicit_isomorphism_elements": len(mapping),
        "edge_orbits": len(cells),
        "anchored_five_sets_enumerated": anchored,
        "all_five_sets_covered_by_translation": FIVE_COUNT,
        "exact_unique_clauses": len(exact),
        "physical_core_clauses": len(clauses),
        "physical_core_sha256": REGULAR_CORE_SHA256[name],
        "satisfiable": satisfiable,
        "dpll": stats,
    }


def check_physical_cores(certificate, partitions):
    expected_indices = set(certificate["retained_partition_representatives"])
    expected_indices.difference_update((1, 2, 3, 4))
    records = certificate["certificates"]
    need(len(records) == len(expected_indices) == 195,
         "195 nonregular maximal cores")
    need({record["index"] for record in records} == expected_indices,
         "physical core index coverage")
    clause_total = 0
    call_total = 0
    call_maximum = 0
    for record in records:
        index = record["index"]
        cells = partitions[index - 1]
        lookup = edge_cell_lookup(cells)
        need(record["edge_orbits"] == len(cells),
             f"core orbit count {index}")
        clauses = []
        physical = set()
        for item in record["clauses"]:
            need(isinstance(item, list) and len(item) == 6,
                 f"physical row shape {index}")
            color, vertices = item[0], tuple(item[1:])
            need(color in ("blue", "red"), f"physical color {index}")
            need(len(set(vertices)) == 5
                 and all(isinstance(v, int) and 0 <= v < N for v in vertices),
                 f"physical five-set {index}")
            key = (color, tuple(sorted(vertices)))
            need(key not in physical, f"duplicate physical row {index}")
            physical.add(key)
            support = five_support(vertices, lookup)
            clauses.append((support, 0) if color == "blue" else (0, support))
        satisfiable, stats = solve_cnf(len(cells), clauses)
        need(not satisfiable, f"physical core {index} is SAT")
        clause_total += len(clauses)
        call_total += stats["calls"]
        call_maximum = max(call_maximum, stats["calls"])
    need(clause_total == 15643, "physical clause total")
    return {
        "partitions": len(records),
        "clauses": clause_total,
        "dpll_calls_total": call_total,
        "dpll_calls_max": call_maximum,
        "all_unsat": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--certificates", type=Path, required=True)
    parser.add_argument("--cayley", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    started = time.monotonic()

    need(digest(args.certificates) == CERTIFICATE_SHA256,
         "certificate SHA-256")
    actions = parse_catalog(args.catalog)
    partitions = tuple(pair_cells(generators) for _, generators in actions)
    retained, unique = maximal_representatives(partitions)
    certificate = json.loads(args.certificates.read_text())
    need(certificate["format"]
         == "r55-vertex-transitive44-physical-cores-v1",
         "certificate format")
    need(certificate["catalog_sha256"] == CATALOG_SHA256,
         "embedded catalog SHA-256")
    need(tuple(certificate["regular_indices_delegated_to_cayley44"])
         == (1, 2, 3, 4), "regular boundary indices")
    need(tuple(certificate["retained_partition_representatives"]) == retained,
         "retained maximal representatives")
    need(retained[:4] == (1, 2, 3, 4), "regular maximal prefix")

    for catalog_index, coarse in enumerate(partitions, 1):
        need(any(finer_than(partitions[representative - 1], coarse)
                 for representative in retained),
             f"refinement cover catalog action {catalog_index}")

    controls = solver_controls()
    cores = check_physical_cores(certificate, partitions)
    regular_names = ("c11_c4", "c11_v4", "c11_sd_c4", "c11_sd_v4")
    regular = [check_regular_action(index, actions[index - 1],
                                    partitions[index - 1], name, args.cayley)
               for index, name in enumerate(regular_names, 1)]
    report = {
        "status": "INDEPENDENTLY_VERIFIED_VERTEX_TRANSITIVE44_EXCLUSION",
        "catalog_sha256": CATALOG_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "catalog_actions": len(actions),
        "unique_labeled_pair_partitions": len(unique),
        "retained_maximal_partitions": len(retained),
        "refinement_cover_actions": len(partitions),
        "solver_control_formulas": controls,
        "physical_cores": cores,
        "regular_actions_direct": regular,
        "imported_boundary": (
            "Completeness of the 2113-row degree-44 transitive-group catalog "
            "is imported from GAP TransGrp 3.6.3; all consequences of the "
            "pinned generator list are checked here."
        ),
        "elapsed_seconds": time.monotonic() - started,
    }
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()

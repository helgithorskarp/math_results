#!/usr/bin/env python3
"""Independent mod-3 audit of the G_11 exact-119-image obstruction.

No module or certificate logic from the reviewed package is imported.  The
source Cayley graph, orthogonal action, quotient graphs and every four-cycle
matrix are reconstructed from definitions.  Signed rhombus rows are reduced
over F_3, unlike the target's unsigned F_2 computation.  The script also emits
an exactly-one, symmetry-free four-colour CNF for the abstract source graph.
"""

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "hadwiger_nelson_g11_exact119_obstruction"
CHROMATIC = REPOSITORY / "hadwiger_nelson_finite_abelian_lifts"
Q = 11
TARGET_HASHES = {
    "AUDIT_EXPECTED.json": "71960f813a8087764ed00fa39ec329c540b254aebcc438fb65768da34f154e73",
    "EXPECTED.json": "eaff4319d26755efc614db82c8380a2dd5516ae59559ebbc2056341e6f4b4bad",
    "PROOF.md": "0eee70d8a63e63f0257e42ceba445900017b846dddc969e2756b92bfa311b2b9",
    "README.md": "4e0a9774b7857a58f58e0ccd6c3ce77d93489f24012064600fc76fb216155bc5",
    "VALIDATION.json": "4ce8745d4813ed541e0a174c8509cec3783fb17aff27eb2302c6b73ba44a382e",
    "audit.py": "a423dbaeefdc70222a111355b8082c1e09a288b19f19122cfa2e0f50c29d66c8",
    "certificate.json": "0c10098c25e19b05931abc6dfbe8449e5f295792fa0edfa19b738f29d2ffc8ac",
    "controls.py": "c9891a935030eafcd687cb24b68d2d48abb4a9fcce1bf07aa136d27b6596c905",
    "produce.py": "38f56bcf587d758021b3fd4f9b2e7a242ef6d20a97820eb4537842fca954416c",
    "verify.py": "702f767e7bfd31e77d23d6bfda9a12613a4b6e614c05093fbf2f27e2b673d02c",
}
CHROMATIC_HASHES = {
    "q11_five_colouring.json":
        "7a12bf22cb3ebdaec2a40f8e321c59e4bac59095c83a533b881aa3c0a7aab444",
    "q11_four_unsat.drat":
        "b54714d1acc3af2f1269aedcdf5bd2fdc6a899ef47037d6af8c8159c106e11b8",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def source_graph():
    points = tuple((x, y) for x in range(Q) for y in range(Q))
    edges = tuple(
        (first, second)
        for first, second in combinations(range(len(points)), 2)
        if ((points[first][0] - points[second][0]) ** 2 +
            (points[first][1] - points[second][1]) ** 2) % Q == 1
    )
    require(len(points) == 121 and len(edges) == 726,
            ("source census", len(points), len(edges)))
    return points, edges


def orthogonal_matrices():
    matrices = []
    for a, b, c, d in product(range(Q), repeat=4):
        if ((a * a + c * c) % Q == 1 and
                (b * b + d * d) % Q == 1 and
                (a * b + c * d) % Q == 0):
            matrices.append((a, b, c, d))
    return tuple(matrices)


def apply(matrix, point):
    a, b, c, d = matrix
    x, y = point
    return ((a * x + b * y) % Q, (c * x + d * y) % Q)


def norm(point):
    return (point[0] * point[0] + point[1] * point[1]) % Q


def first_quotient(edges, identified):
    require(1 <= identified < 121, ("first identification", identified))

    def image(vertex):
        if vertex == identified:
            return 0
        return vertex - (vertex > identified)

    answer = set()
    for first, second in edges:
        a, b = image(first), image(second)
        require(a != b, "first quotient loop")
        answer.add(tuple(sorted((a, b))))
    return tuple(sorted(answer))


def collapse(vertex, first, second):
    low, high = sorted((first, second))
    if vertex == high:
        vertex = low
    return vertex - (vertex > high)


def second_quotient(edges, first, second):
    answer = set()
    for u, v in edges:
        a = collapse(u, first, second)
        b = collapse(v, first, second)
        require(a != b, "second quotient loop")
        answer.add(tuple(sorted((a, b))))
    return tuple(sorted(answer))


def adjacency(order, edges):
    answer = [set() for _ in range(order)]
    for first, second in edges:
        require(0 <= first < second < order, "edge range")
        answer[first].add(second)
        answer[second].add(first)
    return answer


def four_cycles(order, edges):
    """Return one cyclic ordering for every undirected simple four-cycle."""
    adj = adjacency(order, edges)
    keys = set()
    cycles = []
    for a, c in combinations(range(order), 2):
        for b, d in combinations(sorted(adj[a] & adj[c]), 2):
            opposite_pairs = tuple(sorted(((a, c), (b, d))))
            if opposite_pairs in keys:
                continue
            keys.add(opposite_pairs)
            cycles.append((a, b, c, d))
    return tuple(cycles)


def row_mod3(cycle):
    """Encode +e_a-e_b+e_c-e_d as disjoint coefficient bit planes."""
    a, b, c, d = cycle
    return (1 << a) | (1 << c), (1 << b) | (1 << d)


def add_mod3(left, right, mask):
    """Coordinatewise addition of two packed F_3 vectors."""
    left_one, left_two = left
    right_one, right_two = right
    left_zero = mask ^ (left_one | left_two)
    right_zero = mask ^ (right_one | right_two)
    one = ((left_zero & right_one) | (left_one & right_zero) |
           (left_two & right_two))
    two = ((left_zero & right_two) | (left_two & right_zero) |
           (left_one & right_one))
    require(not (one & two), "overlapping ternary bit planes")
    return one, two


def rank_and_basis_mod3(cycles, columns):
    mask = (1 << columns) - 1
    basis = {}
    selected = []
    for cycle in cycles:
        one, two = row_mod3(cycle)
        while one | two:
            pivot = (one | two).bit_length() - 1
            if pivot not in basis:
                if two & (1 << pivot):
                    one, two = two, one
                basis[pivot] = (one, two)
                selected.append(cycle)
                break
            base_one, base_two = basis[pivot]
            if one & (1 << pivot):
                one, two = add_mod3((one, two), (base_two, base_one), mask)
            else:
                one, two = add_mod3((one, two), (base_one, base_two), mask)
    return len(basis), tuple(selected)


def projected_rank_mod3(cycles, first, second):
    projected = []
    for cycle in cycles:
        image = tuple(collapse(vertex, first, second) for vertex in cycle)
        if len(set(image)) == 4:
            projected.append(image)
    rank, _ = rank_and_basis_mod3(projected, 119)
    return rank


def reference_rank(matrix, columns):
    rows = [list(row) for row in matrix]
    rank = 0
    for column in range(columns):
        pivot = next((index for index in range(rank, len(rows))
                      if rows[index][column] % 3), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = 1 if rows[rank][column] % 3 == 1 else 2
        rows[rank] = [(inverse * value) % 3 for value in rows[rank]]
        for index in range(len(rows)):
            if index == rank:
                continue
            factor = rows[index][column] % 3
            if factor:
                rows[index] = [(a - factor * b) % 3
                               for a, b in zip(rows[index], rows[rank], strict=True)]
        rank += 1
    return rank


def small_rank_controls():
    checks = 0
    for columns in range(4):
        choices = 3 ** columns
        for row_count in range(4):
            for packed in range(choices ** row_count):
                value = packed
                matrix = []
                cycles = []
                for _ in range(row_count):
                    value, encoded = divmod(value, choices)
                    row = []
                    one = two = 0
                    for column in range(columns):
                        encoded, coefficient = divmod(encoded, 3)
                        row.append(coefficient)
                        if coefficient == 1:
                            one |= 1 << column
                        elif coefficient == 2:
                            two |= 1 << column
                    matrix.append(row)
                    # rank_and_basis_mod3 expects cycles, so exercise the same
                    # elimination directly below with synthetic packed rows.
                    cycles.append((one, two))
                mask = (1 << columns) - 1
                basis = {}
                for one, two in cycles:
                    while one | two:
                        pivot = (one | two).bit_length() - 1
                        if pivot not in basis:
                            if two & (1 << pivot):
                                one, two = two, one
                            basis[pivot] = (one, two)
                            break
                        base_one, base_two = basis[pivot]
                        if one & (1 << pivot):
                            one, two = add_mod3((one, two), (base_two, base_one), mask)
                        else:
                            one, two = add_mod3((one, two), (base_one, base_two), mask)
                require(len(basis) == reference_rank(matrix, columns),
                        ("mod-3 rank control", columns, row_count, packed))
                checks += 1
    require(checks == 21_304, ("rank control count", checks))
    return checks


def colouring_cnf(order, edges):
    clauses = []
    for vertex in range(order):
        variables = tuple(4 * vertex + colour + 1 for colour in range(4))
        clauses.append(variables)
        clauses.extend((-first, -second)
                       for first, second in combinations(variables, 2))
    for first, second in edges:
        for colour in range(4):
            clauses.append((-(4 * first + colour + 1),
                            -(4 * second + colour + 1)))
    encoded = (f"p cnf {4 * order} {len(clauses)}\n" +
               "".join(" ".join(map(str, clause)) + " 0\n"
                       for clause in clauses)).encode("ascii")
    return len(clauses), encoded


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf-out", type=Path, required=True)
    parser.add_argument("--result-out", type=Path)
    args = parser.parse_args()

    for name, expected in TARGET_HASHES.items():
        require(digest(TARGET / name) == expected, ("target hash", name))
    for name, expected in CHROMATIC_HASHES.items():
        require(digest(CHROMATIC / name) == expected, ("chromatic hash", name))
    rank_controls = small_rank_controls()
    points, source_edges = source_graph()
    colours = json.loads((CHROMATIC / "q11_five_colouring.json").read_text())
    require(type(colours) is list and len(colours) == 121 and
            set(colours) == set(range(5)) and
            all(colours[first] != colours[second] for first, second in source_edges),
            "source five-colouring")

    matrices = orthogonal_matrices()
    require(len(matrices) == 24, ("orthogonal group order", len(matrices)))
    shells = {value: tuple(point for point in points if norm(point) == value)
              for value in range(Q)}
    require(shells[0] == ((0, 0),) and len(shells[1]) == 12,
            "anisotropic/unit shells")
    for value in range(1, Q):
        require(len(shells[value]) == 12, ("shell size", value))
        representative = min(shells[value])
        require({apply(matrix, representative) for matrix in matrices} ==
                set(shells[value]), ("shell orbit", value))

    source_cycles = four_cycles(121, source_edges)
    source_rank, _ = rank_and_basis_mod3(source_cycles, 121)
    require(source_rank == 120, ("source rhombus rank", source_rank))

    event_hash = sha256()
    shell_records = []
    total_triples = total_pairs = total_fallbacks = total_fallback_cycles = 0
    for shell in range(2, 11):
        representative = min(shells[shell])
        identified = representative[0] * Q + representative[1]
        first_edges = first_quotient(source_edges, identified)
        first_cycles = four_cycles(120, first_edges)
        first_rank, first_basis = rank_and_basis_mod3(first_cycles, 120)
        require(first_rank == 119, ("one-collision rank", shell, first_rank))
        adj = adjacency(120, first_edges)
        triples = pair_events = fallbacks = fallback_cycles = 0

        def check_event(shape, first, second):
            nonlocal fallbacks, fallback_cycles, total_fallbacks, total_fallback_cycles
            rank = projected_rank_mod3(first_basis, first, second)
            if rank < 118:
                final_edges = second_quotient(first_edges, first, second)
                final_cycles = four_cycles(119, final_edges)
                rank, _ = rank_and_basis_mod3(final_cycles, 119)
                fallbacks += 1
                fallback_cycles += len(final_cycles)
                total_fallbacks += 1
                total_fallback_cycles += len(final_cycles)
            require(rank == 118, ("exact-119 rank", shell, shape, first, second, rank))
            event_hash.update((json.dumps([shell, shape, first, second, rank],
                                          separators=(",", ":")) + "\n").encode())

        for third in range(1, 120):
            if third not in adj[0]:
                check_event("triple", 0, third)
                triples += 1
                total_triples += 1
        for first, second in combinations(range(1, 120), 2):
            if second not in adj[first]:
                check_event("two_pairs", first, second)
                pair_events += 1
                total_pairs += 1
        shell_records.append({
            "norm": shell,
            "representative": list(representative),
            "one_collision_edges": len(first_edges),
            "one_collision_cycles": len(first_cycles),
            "one_collision_rank_mod_3": first_rank,
            "triple_events": triples,
            "two_pair_events": pair_events,
            "fallback_events": fallbacks,
            "fallback_cycles": fallback_cycles,
        })

    require(total_triples == 864 and total_pairs == 56_871,
            ("event totals", total_triples, total_pairs))
    clause_count, cnf = colouring_cnf(121, source_edges)
    args.cnf_out.parent.mkdir(parents=True, exist_ok=True)
    args.cnf_out.write_bytes(cnf)
    result = {
        "status": "INDEPENDENT MOD-3 RHOMBUS AUDIT PASSED; ABSTRACT FOUR-COLOUR CNF EMITTED",
        "source_vertices": 121,
        "source_edges": 726,
        "source_four_cycles": len(source_cycles),
        "source_rank_mod_3": source_rank,
        "orthogonal_matrices": len(matrices),
        "nonzero_shells": 10,
        "shell_size": 12,
        "one_collision_cases": 9,
        "one_collision_edge_counts": [record["one_collision_edges"]
                                      for record in shell_records],
        "one_collision_cycle_counts": [record["one_collision_cycles"]
                                       for record in shell_records],
        "one_collision_ranks_mod_3": [record["one_collision_rank_mod_3"]
                                      for record in shell_records],
        "triple_events": total_triples,
        "two_pair_events": total_pairs,
        "normalized_events_checked": total_triples + total_pairs,
        "exact119_final_ranks_mod_3": [118],
        "fallback_events": total_fallbacks,
        "fallback_cycles": total_fallback_cycles,
        "event_stream_sha256": event_hash.hexdigest(),
        "exactly_121_images_excluded": True,
        "exactly_120_images_excluded": True,
        "exactly_119_images_excluded": True,
        "all_edge_preserving_plane_maps_have_at_most_118_images": True,
        "five_colouring_checked": True,
        "mod3_rank_controls": rank_controls,
        "four_colour_cnf_variables": 484,
        "four_colour_cnf_clauses": clause_count,
        "four_colour_cnf_sha256": sha256(cnf).hexdigest(),
        "physical_unit_distance_graph_produced": False,
        "record_improvement": False,
    }
    if args.result_out:
        args.result_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

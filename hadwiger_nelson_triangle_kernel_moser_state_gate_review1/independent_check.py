#!/usr/bin/env python3
"""Clean-room exact review of the Moser/triangle-kernel state gate.

No module from the reviewed source or its analytic parent is imported.  The
checker uses a nested quadratic-field representation, enumerates every shell
colouring, exhausts every capacity-feasible blocker selection directly, and
rechecks the published LRAT additions by full-database RUP without its hints.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "hadwiger_nelson_triangle_kernel_moser_state_gate"
PARENT = REPOSITORY / "hadwiger_nelson_triangle_exterior_kernel"
TARGET_COMMIT = "b9394bdeca548f1866b39278e9d10da6c1a5b3fc"
PARENT_COMMIT = "d1ef2c978a6659a4f0ab1ef748be88e57486a4cb"

PINNED = {
    "hadwiger_nelson_triangle_kernel_moser_state_gate/.gitignore":
        "9952ea37227d2ac612d86260b23fdc5adaa2fc63a6b476ae989a6d4f59c606c5",
    "hadwiger_nelson_triangle_kernel_moser_state_gate/DISCOVERY_RECEIPT.json":
        "a70d97fe2a95f1ebdcc8159d652103e50632f4a513b554204be6dbe7430e9ea0",
    "hadwiger_nelson_triangle_kernel_moser_state_gate/README.md":
        "e656999157c3801f58d075a74a3ded643f0b0766b8a807a1d29f9fc0e7df471e",
    "hadwiger_nelson_triangle_kernel_moser_state_gate/SHA256SUMS":
        "de9ff9cf3eba00f42dadfa4f6a66734ee0beb6f334604a821c8ae6782baaf3dc",
    "hadwiger_nelson_triangle_kernel_moser_state_gate/build.py":
        "269dde2b547d74e01168b33f5ca2a935e35b9fb68f28a0bbee4bf2c5338ddbf9",
    "hadwiger_nelson_triangle_kernel_moser_state_gate/certificate.json":
        "7292ea36a61c909c615876f10db3f46ce0483cbb7b712ff08eb0fad17a76e021",
    "hadwiger_nelson_triangle_kernel_moser_state_gate/controls.py":
        "8f08cee3b6095f1af6aad8000bbba42daf0c37523c6b0a5123a6dec99753b05d",
    "hadwiger_nelson_triangle_kernel_moser_state_gate/expected.json":
        "c8385d2a6ce38da65421c287ff0ef05b8c9f941dbd2d163d6925b9cdaa42c7fd",
    "hadwiger_nelson_triangle_kernel_moser_state_gate/state.cnf":
        "ddc993123396619780d0862e4a3450b8b7d7a1fa5314653df608523378fe0557",
    "hadwiger_nelson_triangle_kernel_moser_state_gate/state.lrat":
        "e57328bac88d93b0f23d281d67a3c2755d97334dea36903d06751771aa2fc263",
    "hadwiger_nelson_triangle_kernel_moser_state_gate/validation.json":
        "5673832d09cd8fb5c793f9296cc3c045da66e747ede9b5afa6db6e5530d17e90",
    "hadwiger_nelson_triangle_kernel_moser_state_gate/verify.py":
        "0d6b1743bf4636ea4612f77e7ebf2f9c36d6aa78f6faeb42a42bc123426dcece",
    "hadwiger_nelson_triangle_exterior_kernel/.gitignore":
        "862263fa1f46c20f0d1e4dac5ffcc75abd55c08211b2c3864c5f8764b9d87793",
    "hadwiger_nelson_triangle_exterior_kernel/README.md":
        "e272c2ae4c6dbb43a10251ff3d40e729d1c2b041bac81917441ef7fa3b5037ee",
    "hadwiger_nelson_triangle_exterior_kernel/SHA256SUMS":
        "3fd6906022eb0402ad9b243e0bb51110b0b2c64d978d5acf8e76b0c5ed052ce9",
    "hadwiger_nelson_triangle_exterior_kernel/build.py":
        "24d5fc59e9504d35b668ce7637c47f683cd6ff2a8a6816d098d8906d387ebe99",
    "hadwiger_nelson_triangle_exterior_kernel/certificate.json":
        "c958f8d74bc0459a3f416947d4928b9dad90e2de0451c551b2082eb5fcd59bdd",
    "hadwiger_nelson_triangle_exterior_kernel/expected.json":
        "af7a6f90047307155027e6a2d84d912d9977bd64a4802cf7a0d263dab9239f15",
    "hadwiger_nelson_triangle_exterior_kernel/validation.json":
        "a375bf2d2d77a2ef111caf14497336a39dbbbccb58866197110d2ad0e91c21c7",
    "hadwiger_nelson_triangle_exterior_kernel/verify.py":
        "7aecce6f0157d82a6057f6fbbea792a3191c4991caafb018e8a483cbe6b96c11",
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


# Field elements use (a,b,c,d) = a+b*sqrt(3)+c*sqrt(11)+d*sqrt(33).
ZERO = (F(0),)*4
ONE = (F(1), F(0), F(0), F(0))


def fadd(left, right):
    return tuple(a+b for a, b in zip(left, right, strict=True))


def fneg(value):
    return tuple(-x for x in value)


def fsub(left, right):
    return fadd(left, fneg(right))


def mul_sqrt3(left, right):
    a, b = left
    c, d = right
    return a*c+3*b*d, a*d+b*c


def fmul(left, right):
    """Nested multiplication (A+B sqrt(11))(C+D sqrt(11))."""
    a, b = left[:2], left[2:]
    c, d = right[:2], right[2:]
    ac = mul_sqrt3(a, c)
    bd = mul_sqrt3(b, d)
    ad = mul_sqrt3(a, d)
    bc = mul_sqrt3(b, c)
    return (ac[0]+11*bd[0], ac[1]+11*bd[1], ad[0]+bc[0], ad[1]+bc[1])


def scalar(value):
    return F(value), F(0), F(0), F(0)


def cadd(left, right):
    return fadd(left[0], right[0]), fadd(left[1], right[1])


def csub(left, right):
    return fsub(left[0], right[0]), fsub(left[1], right[1])


def cmul(left, right):
    return (fsub(fmul(left[0], right[0]), fmul(left[1], right[1])),
            fadd(fmul(left[0], right[1]), fmul(left[1], right[0])))


def squared_distance(left, right):
    x, y = csub(left, right)
    return fadd(fmul(x, x), fmul(y, y))


def determinant(left, right):
    return fsub(fmul(left[0], right[1]), fmul(left[1], right[0]))


ORIGIN = (ZERO, ZERO)
UNIT = (ONE, ZERO)
OMEGA = (scalar(F(1, 2)), (F(0), F(1, 2), F(0), F(0)))
ETA = (scalar(F(5, 6)), (F(0), F(0), F(1, 6), F(0)))


def field_controls():
    radicands = (1, 3, 11, 33)
    checks = 0
    for i in range(4):
        for j in range(4):
            left = tuple(F(k == i) for k in range(4))
            right = tuple(F(k == j) for k in range(4))
            common = gcd(radicands[i], radicands[j])
            radical = radicands[i]*radicands[j]//(common*common)
            expected = tuple(F(common if radicands[k] == radical else 0)
                             for k in range(4))
            require(fmul(left, right) == expected, ("field product", i, j))
            checks += 1
    return checks


def complete_unit_edges(points):
    return tuple((a, b) for a, b in combinations(range(len(points)), 2)
                 if squared_distance(points[a], points[b]) == ONE)


def moser_geometry():
    points = (ORIGIN, UNIT, OMEGA, cadd(UNIT, OMEGA), ETA,
              cmul(ETA, OMEGA), cmul(ETA, cadd(UNIT, OMEGA)))
    require(len(set(points)) == 7, "Moser point collision")
    edges = complete_unit_edges(points)
    require(len(edges) == 11, ("Moser edge count", len(edges)))
    colours = tuple(word for word in product(range(4), repeat=7)
                    if all(word[a] != word[b] for a, b in edges))
    three = sum(all(word[a] != word[b] for a, b in edges)
                for word in product(range(3), repeat=7))
    require(len(colours) == 384 and three == 0,
            ("Moser colouring counts", len(colours), three))
    triples = []
    for triple in combinations(range(7), 3):
        a, b, c = (points[v] for v in triple)
        ab2 = squared_distance(a, b)
        bc2 = squared_distance(b, c)
        ca2 = squared_distance(c, a)
        area2 = determinant(csub(b, a), csub(c, a))
        if fmul(fmul(ab2, bc2), ca2) == fmul(scalar(4), fmul(area2, area2)):
            require(area2 != ZERO, ("degenerate circumcircle", triple))
            triples.append(triple)
    expected = [(0, 1, 3), (0, 2, 3), (0, 4, 6), (0, 5, 6),
                (1, 2, 4), (1, 2, 5), (1, 2, 6), (1, 4, 5),
                (2, 4, 5), (3, 4, 5)]
    require(triples == expected, ("unit-circumradius triples", triples))
    return points, edges, colours, tuple(triples)


def patch_check():
    centres = (ORIGIN, UNIT, OMEGA)
    roots = [UNIT]
    for _ in range(5):
        roots.append(cmul(roots[-1], OMEGA))
    require(cmul(roots[-1], OMEGA) == UNIT, "sixth root cycle")
    points = tuple(sorted({cadd(d, u) for d in centres for u in roots}))
    require(len(points) == 12, ("patch points", len(points)))
    edges = complete_unit_edges(points)
    require(len(edges) == 24, ("patch edges", len(edges)))
    fixed = {points.index(d): colour for colour, d in enumerate(centres)}
    free = tuple(v for v in range(12) if v not in fixed)
    colourings = 0
    for values in product(range(3), repeat=len(free)):
        word = dict(fixed)
        word.update(zip(free, values, strict=True))
        colourings += all(word[a] != word[b] for a, b in edges)
    require(colourings == 1, ("pinned patch three-colourings", colourings))
    return len(points), len(edges), colourings


def shell_graph():
    edges = set()
    for owner in range(3):
        for column in range(6):
            a = 6*owner+column
            b = 6*owner+(column+1) % 6
            edges.add(tuple(sorted((a, b))))
    for column in range(6):
        for first, second in combinations(range(3), 2):
            edges.add((6*first+column, 6*second+column))
    edges = tuple(sorted(edges))
    require(len(edges) == 36, ("shell edges", len(edges)))

    states = tuple(state for state in permutations(range(4), 3)
                   if all(state[owner] != owner for owner in range(3)))
    require(len(states) == 11, ("column states", len(states)))
    compatible = tuple(tuple(all(a[i] != b[i] for i in range(3)) for b in states)
                       for a in states)
    require(sum(map(sum, compatible)) == 44, "state compatibility count")

    colourings = []
    def extend(sequence):
        if len(sequence) == 6:
            if not compatible[sequence[-1]][sequence[0]]:
                return
            word = [None]*18
            for column, state_index in enumerate(sequence):
                for owner, colour in enumerate(states[state_index]):
                    word[6*owner+column] = colour
            word = tuple(word)
            require(all(word[a] != word[b] for a, b in edges), "shell colouring edge")
            require(all(word[6*owner+column] != owner
                        for owner in range(3) for column in range(6)),
                    "shell owner colour")
            colourings.append(word)
            return
        for state_index in range(len(states)):
            if not sequence or compatible[sequence[-1]][state_index]:
                extend(sequence+(state_index,))
    for first in range(len(states)):
        extend((first,))
    require(len(colourings) == len(set(colourings)), "duplicate shell colouring")
    return edges, states, compatible, tuple(colourings)


def restriction_classification(shell_colourings):
    full = (1 << len(shell_colourings))-1
    allowed = []
    for vertex in range(18):
        for forbidden in range(4):
            mask = 0
            for index, word in enumerate(shell_colourings):
                if word[vertex] != forbidden:
                    mask |= 1 << index
            allowed.append(mask)

    small_cases = 1
    require(full, "no shell colourings")
    for event in range(72):
        require(allowed[event], ("single restriction", event))
        small_cases += 1
    for first, second in combinations_with_replacement(range(72), 2):
        require(allowed[first] & allowed[second], ("two restrictions", first, second))
        small_cases += 1
    require(small_cases == 2701, ("at-most-two cases", small_cases))

    blockers = []
    triples_tested = 0
    for events in combinations_with_replacement(range(72), 3):
        triples_tested += 1
        if not (allowed[events[0]] & allowed[events[1]] & allowed[events[2]]):
            blockers.append(tuple((event//4, event % 4) for event in events))
    expected = [tuple((vertex, colour) for colour in range(4)
                      if colour != vertex//6) for vertex in range(18)]
    require(blockers == expected, ("three-restriction blockers", blockers))
    require(triples_tested == 64824, ("three-restriction cases", triples_tested))
    stream = "".join(";".join(f"{v},{c}" for v, c in blocker)+"\n"
                     for blocker in blockers).encode()
    return small_cases, triples_tested, tuple(blockers), sha256(stream).hexdigest()


def canonical_formula(moser_colours, triples):
    variables = tuple((owner, triple) for owner in range(3) for triple in triples)
    clauses = []
    coverage_sizes = []
    variable_coverage = [[0]*len(triples) for _ in range(3)]
    for colouring_index, colouring in enumerate(moser_colours):
        clause = []
        for index, (owner, triple) in enumerate(variables):
            if {colouring[v] for v in triple} == set(range(4))-{owner}:
                clause.append(index+1)
                variable_coverage[owner][index % len(triples)] |= 1 << colouring_index
        require(clause, ("uncovered without capacity", colouring_index))
        clauses.append(tuple(clause))
        coverage_sizes.append(len(clause))
    capacity_clauses = 0
    for vertex in range(7):
        for owner in range(3):
            group = [index+1 for index, (q, triple) in enumerate(variables)
                     if q == owner and vertex in triple]
            for chosen in combinations(group, 3):
                clauses.append(tuple(-x for x in chosen))
                capacity_clauses += 1
    require(capacity_clauses == 138 and len(clauses) == 522,
            ("formula dimensions", capacity_clauses, len(clauses)))
    lines = ["p cnf 30 522"]
    lines.extend(" ".join(map(str, clause))+" 0" for clause in clauses)
    raw = ("\n".join(lines)+"\n").encode("ascii")
    require(raw == (TARGET / "state.cnf").read_bytes(), "canonical CNF mismatch")
    return tuple(clauses), variable_coverage, tuple(coverage_sizes), raw


def direct_capacity_search(variable_coverage, colouring_count, triples):
    valid_masks = []
    for mask in range(1 << len(triples)):
        degrees = [0]*7
        for index, triple in enumerate(triples):
            if mask & (1 << index):
                for vertex in triple:
                    degrees[vertex] += 1
        if max(degrees, default=0) <= 2:
            valid_masks.append(mask)
    require(len(valid_masks) == 154, ("capacity-valid subsets", len(valid_masks)))

    coverages = []
    for owner in range(3):
        rows = []
        for mask in valid_masks:
            covered = 0
            for index in range(len(triples)):
                if mask & (1 << index):
                    covered |= variable_coverage[owner][index]
            rows.append((mask, covered))
        coverages.append(tuple(rows))

    full = (1 << colouring_count)-1
    cases = full_covers = 0
    maximum = -1
    first_best = None
    for mask0, cover0 in coverages[0]:
        for mask1, cover1 in coverages[1]:
            partial = cover0 | cover1
            for mask2, cover2 in coverages[2]:
                covered = partial | cover2
                cases += 1
                size = covered.bit_count()
                if size > maximum:
                    maximum = size
                    first_best = (mask0, mask1, mask2)
                full_covers += covered == full
    require(cases == 154**3 and full_covers == 0,
            ("direct capacity search", cases, full_covers))
    require(maximum == 378 and first_best == (581, 581, 581),
            ("best capacity cover", maximum, first_best))

    unconstrained = 0
    for owner in range(3):
        for covered in variable_coverage[owner]:
            unconstrained |= covered
    require(unconstrained == full, "all blocker types do not cover all colourings")
    return {
        "capacity_valid_subsets_per_owner": len(valid_masks),
        "capacity_feasible_three_owner_selections": cases,
        "full_cover_selections": full_covers,
        "maximum_moser_colourings_blocked": maximum,
        "minimum_surviving_moser_colourings": colouring_count-maximum,
        "first_maximum_masks": list(first_best),
        "all_types_cover_without_capacity": True,
    }


def full_database_rup(active_clauses, candidate):
    assignment = {}
    for literal in candidate:
        variable = abs(literal)
        value = literal < 0  # Negate every literal of the candidate clause.
        if variable in assignment and assignment[variable] != value:
            return True, 0
        assignment[variable] = value
    checks = 0
    while True:
        changed = False
        for clause in active_clauses:
            checks += 1
            satisfied = False
            unassigned = []
            for literal in clause:
                variable = abs(literal)
                if variable not in assignment:
                    unassigned.append(literal)
                elif assignment[variable] == (literal > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not unassigned:
                return True, checks
            if len(unassigned) == 1:
                literal = unassigned[0]
                variable = abs(literal)
                value = literal > 0
                if variable in assignment and assignment[variable] != value:
                    return True, checks
                if variable not in assignment:
                    assignment[variable] = value
                    changed = True
        if not changed:
            return False, checks


def replay_lrat_without_hints(initial_clauses, raw):
    active = {index+1: clause for index, clause in enumerate(initial_clauses)}
    additions = deletions = clause_checks = hint_references = 0
    last_addition = len(initial_clauses)
    final_empty = False
    for line in raw.decode("ascii").splitlines():
        tokens = line.split()
        require(tokens, "empty LRAT line")
        identifier = int(tokens[0])
        if tokens[1] == "d":
            deleted = tuple(map(int, tokens[2:]))
            require(deleted and deleted[-1] == 0, "LRAT deletion terminator")
            for clause_id in deleted[:-1]:
                require(clause_id in active, ("LRAT delete live", clause_id))
                del active[clause_id]
                deletions += 1
            continue
        values = tuple(map(int, tokens[1:]))
        require(values.count(0) == 2 and values[-1] == 0, "LRAT addition shape")
        cut = values.index(0)
        candidate = values[:cut]
        hints = values[cut+1:-1]
        require(identifier > last_addition and identifier not in active and hints,
                ("LRAT addition id", identifier))
        require(all(hint > 0 and hint in active for hint in hints),
                ("LRAT live hints", identifier))
        valid, checks = full_database_rup(tuple(active.values()), candidate)
        require(valid, ("not full-database RUP", identifier))
        clause_checks += checks
        hint_references += len(hints)
        active[identifier] = candidate
        last_addition = identifier
        additions += 1
        final_empty |= not candidate
    require(final_empty, "LRAT has no final empty clause")
    return additions, deletions, clause_checks, hint_references


def main():
    for name, expected in PINNED.items():
        require(digest(REPOSITORY / name) == expected, ("pinned source hash", name))
    basis_checks = field_controls()
    patch_points, patch_edges, patch_colourings = patch_check()
    _, moser_edges, moser_colours, triples = moser_geometry()
    shell_edges, states, compatible, shell_colourings = shell_graph()
    small_cases, triple_cases, blockers, blocker_hash = restriction_classification(shell_colourings)
    clauses, variable_coverage, coverage_sizes, cnf_raw = canonical_formula(moser_colours, triples)
    search = direct_capacity_search(variable_coverage, len(moser_colours), triples)
    lrat_raw = (TARGET / "state.lrat").read_bytes()
    lrat_additions, lrat_deletions, rup_checks, hint_references = \
        replay_lrat_without_hints(clauses, lrat_raw)
    try:
        replay_lrat_without_hints(clauses, b"\n".join(lrat_raw.splitlines()[:-1])+b"\n")
    except RuntimeError:
        truncated_lrat_rejected = True
    else:
        raise RuntimeError("truncated LRAT accepted")
    maximum_incidences = 7*3*2
    maximum_components = maximum_incidences//3
    maximum_kernel = 12+7+18*maximum_components
    require((maximum_incidences, maximum_components, maximum_kernel) == (42, 14, 271),
            "finite-kernel arithmetic")
    certificate = json.loads((TARGET / "certificate.json").read_text())
    checked_certificate = {
        "blocker_variables": 30,
        "blocking_restriction_multisets": len(blockers),
        "capacity_clauses": 138,
        "cnf_clauses": len(clauses),
        "cnf_sha256": sha256(cnf_raw).hexdigest(),
        "coverage_clause_size_histogram": {
            str(size): coverage_sizes.count(size) for size in sorted(set(coverage_sizes))},
        "coverage_clauses": len(moser_colours),
        "maximum_finite_kernel_vertices": maximum_kernel,
        "maximum_important_components": maximum_components,
        "moser_complete_unit_edges": [list(edge) for edge in moser_edges],
        "moser_proper_four_colourings": len(moser_colours),
        "moser_vertices": 7,
        "physical_incidence_bound": maximum_incidences,
        "record_candidate": False,
        "scope": "Moser exterior, no patch contacts, at most three incidences per generic component",
        "shell_column_states": len(states),
        "shell_compatible_ordered_state_pairs": sum(map(sum, compatible)),
        "three_incidence_restriction_multisets": triple_cases,
        "unit_circumradius_moser_triples": [list(triple) for triple in triples],
    }
    require(certificate == checked_certificate, "published certificate mismatch")

    result = {
        "status": "EXACT SCOPED THEOREM INDEPENDENTLY REPRODUCED",
        "verdict": "ACCEPT_HIGH_CONFIDENCE_SCOPED",
        "reviewed_source_commit": TARGET_COMMIT,
        "analytic_parent_commit": PARENT_COMMIT,
        "imports_reviewed_or_parent_code": False,
        "field_representation": "nested Q(sqrt(3),sqrt(11)) tower",
        "field_basis_product_controls": basis_checks,
        "patch_points": patch_points,
        "patch_complete_unit_edges": patch_edges,
        "patch_pinned_three_colourings": patch_colourings,
        "moser_vertices": 7,
        "moser_complete_unit_edges": len(moser_edges),
        "moser_proper_three_colourings": 0,
        "moser_proper_four_colourings": len(moser_colours),
        "moser_colour_stream_sha256": sha256(json.dumps(moser_colours, separators=(",", ":")).encode()).hexdigest(),
        "unit_circumradius_moser_triples": [list(triple) for triple in triples],
        "shell_vertices": 18,
        "shell_edges": len(shell_edges),
        "shell_column_states": len(states),
        "shell_compatible_ordered_state_pairs": sum(map(sum, compatible)),
        "complete_shell_four_colourings": len(shell_colourings),
        "shell_colour_stream_sha256": sha256(json.dumps(shell_colourings, separators=(",", ":")).encode()).hexdigest(),
        "restriction_multisets_through_two": small_cases,
        "three_incidence_restriction_multisets": triple_cases,
        "blocking_restriction_multisets": len(blockers),
        "blocking_restriction_stream_sha256": blocker_hash,
        "cnf_variables": 30,
        "cnf_clauses": len(clauses),
        "published_certificate_entrywise_reconstructed": True,
        "coverage_clause_size_histogram": {str(size): coverage_sizes.count(size)
                                           for size in sorted(set(coverage_sizes))},
        "cnf_sha256": sha256(cnf_raw).hexdigest(),
        **search,
        "independent_unsat_method": "exhaust all capacity-feasible blocker-type subsets",
        "published_lrat_sha256": sha256(lrat_raw).hexdigest(),
        "lrat_additions_full_database_rup": lrat_additions,
        "lrat_deletions": lrat_deletions,
        "full_database_rup_clause_checks": rup_checks,
        "lrat_live_hint_references": hint_references,
        "truncated_lrat_rejected": truncated_lrat_rejected,
        "maximum_shell_incidences_for_seven_exterior_points": maximum_incidences,
        "maximum_three_incidence_components": maximum_components,
        "maximum_finite_kernel_vertices": maximum_kernel,
        "complete_infinite_support_four_colourable_under_hypotheses": True,
        "global_hadwiger_nelson_progress": False,
        "record_candidate": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent exact audit of the degree-seven point-610 closure.

This checker imports no submitted Python module.  It verifies the positive
colourings in exact arithmetic, reconstructs the old cardinality CNF from the
mathematical constraints, and checks the elementary reduction and final
four-disjoint-set contradiction.  The load-bearing pseudo-Boolean proof is
checked with VeriPB and identified in the resulting report.
"""

from argparse import ArgumentParser
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from json import dump, load
from pathlib import Path
import subprocess


EXPECTED_CNF = "f09870b3f8e34778e85a4ec189e95ef07648e4ef48ebbaed3d68d5018450b6fa"
EXPECTED_EDGE = "88fee3eb7c788320a146ad1576ba2fe85d257f0c3edb70480030d1f6534c88a7"
EXPECTED_OPB = "03dfd3601258be7899c607696b96bf9b0ddba77784db404cca045e7b8dfdda9d"


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def multiply(a, b):
    """Multiply in Q(sqrt(3),sqrt(5),sqrt(11)) in the subset basis."""
    result = [Fraction(0)] * 8
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if not x or not y:
                continue
            common = i & j
            coefficient = x * y
            if common & 1:
                coefficient *= 3
            if common & 2:
                coefficient *= 5
            if common & 4:
                coefficient *= 11
            result[i ^ j] += coefficient
    return tuple(result)


def squared_distance(p, q):
    dx = tuple(a - b for a, b in zip(p[0], q[0]))
    dy = tuple(a - b for a, b in zip(p[1], q[1]))
    return tuple(a + b for a, b in zip(multiply(dx, dx), multiply(dy, dy)))


def parse_point(value):
    return tuple(tuple(Fraction(x) for x in axis) for axis in value)


def graph(points, vertices):
    one = (Fraction(1),) + (Fraction(0),) * 7
    return [(a, b) for a, b in combinations(vertices, 2)
            if squared_distance(points[a], points[b]) == one]


def proper(vertices, edges, deleted, colouring, palette):
    retained = [v for v in vertices if v not in set(deleted)]
    require(len(retained) == len(colouring), ("colouring length", deleted))
    require(set(colouring) <= set(palette), ("colour alphabet", deleted))
    colour = dict(zip(retained, colouring, strict=True))
    checked = 0
    for a, b in edges:
        if a in colour and b in colour:
            require(colour[a] != colour[b], ("monochromatic edge", a, b, deleted))
            checked += 1
    return checked


def sequential_at_most(literals, limit, next_variable):
    """Sinz prefix counter; return clauses and the last allocated variable."""
    n = len(literals)
    if limit >= n:
        return [], next_variable
    if limit == 0:
        return [[-x] for x in literals], next_variable
    counter = lambda i, j: next_variable + i * limit + j + 1
    rows = [[-literals[0], counter(0, 0)]]
    rows.extend([[-counter(0, j)] for j in range(1, limit)])
    for i in range(1, n):
        rows.append([-literals[i], counter(i, 0)])
        rows.append([-counter(i - 1, 0), counter(i, 0)])
        for j in range(1, limit):
            rows.append([-literals[i], -counter(i - 1, j - 1), counter(i, j)])
            rows.append([-counter(i - 1, j), counter(i, j)])
        rows.append([-literals[i], -counter(i - 1, limit - 1)])
    return rows, next_variable + n * limit


def cardinality_cnf(old):
    free = old["free"]
    variable = {v: i + 1 for i, v in enumerate(free)}
    family = [tuple(row["D"]) for row in old["family"]]
    keys = set(map(frozenset, family))
    minimal = [row for row in family
               if not any(other < frozenset(row) for other in keys)]
    rows = [[variable[v] for v in row] for row in minimal]
    added, last = sequential_at_most([variable[v] for v in free], 57, len(free))
    rows.extend(added)
    # At least four pool selectors means at most 72 negated selectors.
    added, last = sequential_at_most([-variable[v] for v in old["pool_free"]], 72, last)
    rows.extend(added)
    text = (f"p cnf {last} {len(rows)}\n" +
            "".join(" ".join(map(str, row)) + " 0\n" for row in rows)).encode()
    return text, minimal


def decision_opb(old, minimal):
    """Direct PB formulation of the hitting-set lower-bound decision problem."""
    variable = {v: i + 1 for i, v in enumerate(old["free"])}
    lines = [" ".join(f"+1 x{variable[v]}" for v in row) + " >= 1 ;"
             for row in minimal]
    lines.append(" ".join(f"+1 x{variable[v]}" for v in old["pool_free"]) + " >= 4 ;")
    lines.append(" ".join(f"-1 x{variable[v]}" for v in old["free"]) + " >= -57 ;")
    return (f"* #variable= 134 #constraint= {len(lines)} #equal= 0 intsize= 8\n" +
            "\n".join(lines) + "\n").encode()


def check_counter_small():
    """Exhaustively check canonical prefix-count extensions on small inputs."""
    tested = 0
    for n in range(2, 9):
        for limit in range(1, n):
            rows, last = sequential_at_most(list(range(1, n + 1)), limit, n)
            require(last == n + n * limit, "counter allocation")
            for bits in product((False, True), repeat=n):
                assignment = {i + 1: bits[i] for i in range(n)}
                for i in range(n):
                    count = sum(bits[:i + 1])
                    for j in range(limit):
                        assignment[n + i * limit + j + 1] = count >= j + 1
                satisfied = all(any(assignment[abs(lit)] == (lit > 0) for lit in row)
                                for row in rows)
                require(satisfied == (sum(bits) <= limit),
                        ("counter truth table", n, limit, bits))
                tested += 1
    return tested


def file_record(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def main():
    parser = ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--opb", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--veripb", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo.resolve()
    old_dir = root / "hadwiger_nelson_parts509_degree_pool_minimum"
    lift_dir = root / "hadwiger_nelson_parts509_degree7_extension610"
    close_dir = root / "hadwiger_nelson_parts509_degree7_extension610_closure"
    with (old_dir / "certificate_D7.json").open() as stream:
        old = load(stream)
    with (lift_dir / "certificate.json").open() as stream:
        lift = load(stream)
    with (lift_dir / "residual_instance.json").open() as stream:
        residual = load(stream)
    with (close_dir / "certificate.json").open() as stream:
        close = load(stream)

    require(old["vertices"] == list(range(585)), "old vertex labels")
    require(old["pool"] == list(range(509, 585)), "old pool labels")
    require(old["pool_free"] == old["pool"], "pool/free identity")
    require(len(old["forced"]) == 451 and len(old["free"]) == 134, "partition sizes")
    require(sorted(old["forced"] + old["free"]) == old["vertices"], "partition")
    points = {int(v): parse_point(point) for v, point in old["coordinates"].items()}
    with (root / "hadwiger_nelson_parts509_swap_closure/completion_points.json").open() as stream:
        completions = load(stream)["points"]
    require(len(completions) > 101, "completion census")
    points[610] = parse_point([completions[101]["x"], completions[101]["y"]])
    require(points[610] == (((Fraction(-5, 12),) + (Fraction(0),) * 4 +
                             (Fraction(-1, 12),) + (Fraction(0),) * 2),
                            (Fraction(0), Fraction(5, 12), Fraction(0), Fraction(0),
                             Fraction(-1, 12), Fraction(0), Fraction(0), Fraction(0))),
            "point 610 coordinates")

    old_edges = graph(points, old["vertices"])
    require(len(old_edges) == 3083, "old edge count")
    vertices = old["vertices"] + [610]
    edges = graph(points, vertices)
    edge_text = "".join(f"{a},{b}\n" for a, b in edges).encode()
    require(len(edges) == 3089 and sha256(edge_text).hexdigest() == EXPECTED_EDGE,
            "extended edge census")
    require([a for a, b in edges if b == 610] == [0, 1, 63, 163, 171, 198],
            "point 610 neighbourhood")

    old_checks = 0
    for v in old["forced"]:
        old_checks += proper(old["vertices"], old_edges, [v], old["forced_witness"][str(v)], "0123")
    for row in old["family"]:
        old_checks += proper(old["vertices"], old_edges, row["D"], row["witness"], "0123")
    require(len({tuple(row["D"]) for row in old["family"]}) == 425, "distinct killing sets")

    replacements = {(row["kind"], row["key"]): row["witness"]
                    for row in lift["replacement_witnesses"]}
    extended_checks = 0
    for index, v in enumerate(old["forced"]):
        suffix = lift["forced_append"][index]
        witness = (replacements[("forced", str(v))] if suffix == "."
                   else old["forced_witness"][str(v)] + suffix)
        extended_checks += proper(vertices, edges, [v], witness, "0123")
    for index, row in enumerate(old["family"]):
        if index == 188:
            require(row["D"] == [15, 23] and lift["killing_append"][index] == ".",
                    "unique excluded killing row")
            continue
        suffix = lift["killing_append"][index]
        witness = (replacements[("kill", str(index))] if suffix == "."
                   else row["witness"] + suffix)
        extended_checks += proper(vertices, edges, row["D"], witness, "0123")
    proper(vertices, edges, [], lift["five_colouring"], "01234")

    cnf, minimal = cardinality_cnf(old)
    require(len(minimal) == 337, "minimal killing family")
    require(sha256(cnf).hexdigest() == EXPECTED_CNF, "cardinality CNF hash")
    opb = decision_opb(old, minimal)
    require(sha256(opb).hexdigest() == EXPECTED_OPB, "decision OPB hash")
    require(args.opb.read_bytes() == opb, "supplied OPB differs from reconstruction")
    require(file_record(args.proof)["bytes"] > 0, "empty PB proof")
    small_tests = check_counter_small()

    verification = subprocess.run([str(args.veripb.resolve()), str(args.opb.resolve()),
                                   str(args.proof.resolve())],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  text=True)
    require(verification.returncode == 0 and
            "s VERIFIED UNSATISFIABLE" in verification.stdout,
            ("VeriPB rejected proof", verification.returncode, verification.stdout[-1000:]))

    require(residual["fixed_omitted_original_vertices"] == [15, 23], "residual omissions")
    require(residual["exact_deletions"] == residual["exact_additions"] == 3,
            "residual quotas")
    # Independently rederive the predecessor's case split from the old bound.
    # F has size 451.  A <=508 obstruction has |X|<=57 and >=4 pool points.
    # The degree-seven bound rules this out unless q is present.  With q, the
    # 508-vertex deletion budget gives |X|<=56.  Augmenting X by a missed
    # omitted-original or pool vertex turns every exceptional case into a
    # forbidden <=57 hitting set with >=4 pool points.
    require(len(old["forced"]) + 57 == 508, "old budget")
    require(len(old["forced"]) + 1 + 56 == 508, "extended budget")
    require(old["minimum_hitting_set"] == 58 and old["min_points"] == 4,
            "old hitting theorem parameters")

    groups = []
    for index in close["killing_rows"]:
        require(index != 188, "excluded row reused")
        remaining = set(old["family"][index]["D"]) - {15, 23}
        require(remaining and remaining <= set(old["pool"]), ("non-pool residue", index))
        groups.append(sorted(remaining))
    require(groups == close["required_pool_groups"], "closure groups")
    require(sum(map(len, groups)) == len(set().union(*map(set, groups))),
            "groups not disjoint")
    require(len(groups) == 4 > residual["exact_additions"], "no disjoint-set contradiction")
    report = {
        "status": "accepted at fixed-host closure scope",
        "vertices": len(vertices),
        "unit_edges": len(edges),
        "edge_sha256": EXPECTED_EDGE,
        "old_forced_witnesses": 451,
        "old_killing_witnesses": 425,
        "extended_forced_witnesses": 451,
        "extended_killing_witnesses": 424,
        "old_retained_edge_checks": old_checks,
        "extended_retained_edge_checks": extended_checks,
        "minimal_killing_sets": len(minimal),
        "cardinality_cnf": {"bytes": len(cnf), "sha256": EXPECTED_CNF,
                            "variables": 13244, "clauses": 26636},
        "counter_truth_table_assignments": small_tests,
        "opb": {"bytes": len(opb), "sha256": EXPECTED_OPB,
                "variables": 134, "constraints": 339},
        "veripb_proof": file_record(args.proof),
        "veripb_checker": file_record(args.veripb),
        "veripb_verified_unsatisfiable": True,
        "solver": file_record(args.solver),
        "fixed_omitted_originals": [15, 23],
        "exact_old_pool_points": 3,
        "disjoint_required_pool_groups": groups,
        "required_old_pool_points": 4,
        "direct_disjoint_set_contradiction": True,
        "imported_small_augmentation_closures": True,
        "imported_parts509_five_chromaticity": True,
    }
    with args.report.open("w") as stream:
        dump(report, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(args.report)


if __name__ == "__main__":
    main()

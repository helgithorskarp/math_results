#!/usr/bin/env python3
"""Generate exact SAT instances for order-15 strong Seymour counterexamples.

Generated DIMACS files are solver inputs and must be written below /scratch.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool


N = 15


def arc(pool: IDPool, i: int, j: int) -> int:
    """Literal asserting i -> j; the edge variable means low -> high."""
    if i == j:
        raise ValueError("loops are not tournament arcs")
    variable = pool.id(("edge", min(i, j), max(i, j)))
    return variable if i < j else -variable


def gated(clauses: list[list[int]], enabling_literal: int) -> list[list[int]]:
    """Return clauses active exactly when enabling_literal is true."""
    return [[-enabling_literal, *clause] for clause in clauses]


def conjunction(
    clauses: list[list[int]], output: int, left: int, right: int
) -> None:
    clauses.append([-output, left])
    clauses.append([-output, right])
    clauses.append([output, -left, -right])


def add_degree_flags(cnf: CNF, pool: IDPool, x: int) -> tuple[int, int]:
    """Enforce d+(x)>=6 and exact flags for thresholds seven and eight."""
    degree = [arc(pool, x, y) for y in range(N) if y != x]
    at_least_seven = pool.id(("degree-at-least-seven", x))
    at_least_eight = pool.id(("degree-at-least-eight", x))

    cnf.extend(
        CardEnc.atleast(
            degree, bound=6, vpool=pool, encoding=EncType.seqcounter
        ).clauses
    )
    cnf.extend(
        gated(
            CardEnc.atleast(
                degree, bound=7, vpool=pool, encoding=EncType.seqcounter
            ).clauses,
            at_least_seven,
        )
    )
    cnf.extend(
        gated(
            CardEnc.atmost(
                degree, bound=6, vpool=pool, encoding=EncType.seqcounter
            ).clauses,
            -at_least_seven,
        )
    )
    cnf.extend(
        gated(
            CardEnc.atleast(
                degree, bound=8, vpool=pool, encoding=EncType.seqcounter
            ).clauses,
            at_least_eight,
        )
    )
    cnf.extend(
        gated(
            CardEnc.atmost(
                degree, bound=7, vpool=pool, encoding=EncType.seqcounter
            ).clauses,
            -at_least_eight,
        )
    )
    cnf.append([-at_least_eight, at_least_seven])
    return at_least_seven, at_least_eight


def add_minimal_hall_obstruction(
    cnf: CNF,
    pool: IDPool,
    x: int,
    at_least_seven: int,
    at_least_eight: int,
    every_vertex_is_minimum: bool = False,
) -> None:
    """Give every degree-six/seven vertex a deficient Hall set.

    The witness is chosen inclusion-minimal.  Its neighbor set therefore has
    size |S|-1 and every neighbor has at least two preimages in S.  When x has
    degree six, it is a minimum-outdegree vertex, so the induced tournament on
    S has minimum out-degree at least one by Bai--Li--Park Lemma 2.5.
    """
    clauses: list[list[int]] = []
    s_literals: list[int] = []
    t_literals: list[int] = []

    for y in range(N):
        if y == x:
            continue
        selected = pool.id(("hall-left", x, y))
        s_literals.append(selected)
        clauses.append([-selected, arc(pool, x, y)])

    for z in range(N):
        if z == x:
            continue
        neighbor = pool.id(("hall-neighbor", x, z))
        t_literals.append(neighbor)
        products: list[int] = []
        for y in range(N):
            if y == x or y == z:
                continue
            selected = pool.id(("hall-left", x, y))
            product = pool.id(("hall-product", x, y, z))
            products.append(product)
            conjunction(clauses, product, selected, arc(pool, y, z))
            # A Hall neighbor must also be an in-neighbor of x.
            clauses.append([-product, -arc(pool, z, x), neighbor])
        clauses.append([-neighbor, arc(pool, z, x)])
        clauses.append([-neighbor, *products])
        twice = CardEnc.atleast(
            products, bound=2, vpool=pool, encoding=EncType.seqcounter
        )
        clauses.extend(gated(twice.clauses, neighbor))

    # |Gamma(S)|=|S|-1, expressed as
    # |Gamma(S)| + sum_y (1-1_S(y)) = N-2.
    clauses.extend(
        CardEnc.equals(
            [*t_literals, *[-selected for selected in s_literals]],
            bound=N - 2,
            vpool=pool,
            encoding=EncType.seqcounter,
        ).clauses
    )

    # The global minimum degree is six.  If x has degree exactly six, the
    # minimum-degree witness lemma gives |S|>=3 and positive internal degree.
    at_least_three = CardEnc.atleast(
        s_literals, bound=3, vpool=pool, encoding=EncType.seqcounter
    )
    if every_vertex_is_minimum:
        clauses.extend(at_least_three.clauses)
    else:
        clauses.extend(gated(at_least_three.clauses, -at_least_seven))
    for y in range(N):
        if y == x:
            continue
        internal_products: list[int] = []
        for z in range(N):
            if z == x or z == y:
                continue
            product = pool.id(("internal-product", x, y, z))
            internal_products.append(product)
            conjunction(
                clauses,
                product,
                pool.id(("hall-left", x, z)),
                arc(pool, y, z),
            )
        internal_clause = [-pool.id(("hall-left", x, y)), *internal_products]
        clauses.append(
            internal_clause
            if every_vertex_is_minimum
            else [at_least_seven, *internal_clause]
        )

    # Vertices of degree at least eight are automatically nonstrong because
    # they have at most six in-neighbors.  Activate this witness below eight.
    cnf.extend(gated(clauses, -at_least_eight))


def build(
    root_degree: int,
    root_hall_size: int,
    mode: str = "all",
    secondary_size: int | None = None,
    secondary_degree_region: str | None = None,
) -> tuple[CNF, IDPool]:
    """Build one of the nine exhaustive normalized root cases."""
    valid_sizes = {6: range(3, 6), 7: range(1, 7)}
    if root_degree not in valid_sizes or root_hall_size not in valid_sizes[root_degree]:
        raise ValueError("cases are d6-s3..5 and d7-s1..6")
    if mode not in {"all", "regular", "nonregular"}:
        raise ValueError("mode must be all, regular, or nonregular")
    if mode == "regular" and (root_degree != 7 or root_hall_size < 3):
        raise ValueError("regular cases are d7-s3..6")
    if secondary_size is not None and not (
        mode == "nonregular"
        and root_degree == 7
        and root_hall_size == 1
        and secondary_size in range(3, 7)
    ):
        raise ValueError("secondary normalization is only d7-s1, sizes 3..6")
    if secondary_degree_region is not None and not (
        secondary_size == 6
        and secondary_degree_region in {"witness", "neighbors"}
    ):
        raise ValueError("secondary degree region requires secondary size six")

    pool = IDPool()
    cnf = CNF()
    flags = [add_degree_flags(cnf, pool, x) for x in range(N)]

    # The degree sum is 105.  Relative to the minimum degree six, every
    # degree-at-least-eight vertex consumes at least two of 15 excess units.
    cnf.extend(
        CardEnc.atmost(
            [at_least_eight for _, at_least_eight in flags],
            bound=7,
            vpool=pool,
            encoding=EncType.seqcounter,
        ).clauses
    )

    for x, (at_least_seven, at_least_eight) in enumerate(flags):
        add_minimal_hall_obstruction(
            cnf,
            pool,
            x,
            at_least_seven,
            at_least_eight,
            every_vertex_is_minimum=mode == "regular",
        )

    if mode == "regular":
        # With average out-degree seven, minimum degree at least seven forces
        # every degree to equal seven.
        for at_least_seven, _ in flags:
            cnf.append([at_least_seven])
    elif mode == "nonregular" and root_degree == 7:
        # A nonregular tournament with minimum degree at least six has at
        # least one degree-six vertex.  Permutations inside each of the four
        # root regions preserve the normalization, so a degree-six vertex can
        # be moved to the displayed representative of its region.
        if root_hall_size == 1:
            # The sole witness vertex loses to the root and all seven root
            # in-neighbors, so minimum degree six forces its degree to be six.
            cnf.append([-flags[1][0]])
        elif root_hall_size == 2:
            # Both witness vertices dominate the unique Hall neighbor.  Label
            # their internal arc 1->2.  Vertex 2 then has only six possible
            # out-neighbors, all forced by the minimum-degree condition.
            cnf.append([arc(pool, 1, 2)])
            cnf.append([-flags[2][0]])
        else:
            representatives = [1]
            if root_hall_size < root_degree:
                representatives.append(root_hall_size + 1)
            representatives.append(root_degree + 1)
            if root_degree + root_hall_size <= N - 1:
                representatives.append(root_degree + root_hall_size)
            cnf.append([-flags[vertex][0] for vertex in representatives])

    # Normalize an ordinary Seymour root: its degree is six or seven.  Relabel
    # its two shores so the chosen minimal Hall witness and its neighbor set
    # are initial segments.
    root = 0
    for y in range(1, N):
        cnf.append(
            [arc(pool, root, y) if y <= root_degree else -arc(pool, root, y)]
        )
    for y in range(1, N):
        selected = pool.id(("hall-left", root, y))
        cnf.append([selected if y <= root_hall_size else -selected])
    for z in range(1, N):
        neighbor = pool.id(("hall-neighbor", root, z))
        in_neighbor_set = root_degree < z < root_degree + root_hall_size
        cnf.append([neighbor if in_neighbor_set else -neighbor])

    if secondary_size is not None:
        # In d7-s1 the sole root-witness vertex 1 has degree six and exactly
        # the six vertices 2..7 as out-neighbors.  Normalize its minimal Hall
        # witness within 2..7 and its neighbor set within 8..14.
        secondary_root = 1
        for y in range(N):
            if y == secondary_root:
                continue
            selected = pool.id(("hall-left", secondary_root, y))
            in_secondary_witness = 2 <= y < 2 + secondary_size
            cnf.append([selected if in_secondary_witness else -selected])
        for z in range(N):
            if z == secondary_root:
                continue
            neighbor = pool.id(("hall-neighbor", secondary_root, z))
            in_secondary_neighbors = 8 <= z < 8 + secondary_size - 1
            cnf.append([neighbor if in_secondary_neighbors else -neighbor])
        if secondary_size == 6:
            # The two remaining root in-neighbors dominate 0, 1, and all six
            # secondary witness vertices.  Orient their mutual arc 13->14;
            # their degree excesses are then at least two and one.  Since
            # vertex 1 has deficit one and vertex 0 has degree seven, the
            # score sum forces a degree-six vertex in 2..12.  Relabel it to
            # representative 2 (secondary witness) or 8 (neighbor set).
            cnf.append([arc(pool, 13, 14)])
            if secondary_degree_region == "witness":
                cnf.append([-flags[2][0]])
            elif secondary_degree_region == "neighbors":
                cnf.append([-flags[8][0]])
            else:
                cnf.append([-flags[2][0], -flags[8][0]])

    if mode == "regular":
        # Each root region can be relabeled independently.  In every region
        # of size at least two, orient one representative internal arc.
        regions = [
            list(range(1, root_hall_size + 1)),
            list(range(root_hall_size + 1, root_degree + 1)),
            list(range(root_degree + 1, root_degree + root_hall_size)),
            list(range(root_degree + root_hall_size, N)),
        ]
        for region in regions:
            if len(region) >= 2:
                cnf.append([arc(pool, region[0], region[1])])

    return cnf, pool


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_case(case: str) -> tuple[int, int]:
    degree_text, size_text = case.split("-")
    return int(degree_text[1:]), int(size_text[1:])


def main() -> None:
    parser = argparse.ArgumentParser()
    cases = [
        *[f"d6-s{size}" for size in range(3, 6)],
        *[f"d7-s{size}" for size in range(1, 7)],
    ]
    parser.add_argument("case", choices=cases)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--mode", choices=("all", "regular", "nonregular"), default="all"
    )
    parser.add_argument("--secondary-size", type=int)
    parser.add_argument(
        "--secondary-degree-region", choices=("witness", "neighbors")
    )
    parser.add_argument(
        "--map",
        type=Path,
        help="optional variable map, also required to be below /scratch",
    )
    args = parser.parse_args()
    for path in (args.output, args.map):
        if path is not None and (
            not path.is_absolute() or path.parts[:2] != ("/", "scratch")
        ):
            raise SystemExit("every output must be an absolute path below /scratch")

    root_degree, root_hall_size = parse_case(args.case)
    cnf, pool = build(
        root_degree,
        root_hall_size,
        mode=args.mode,
        secondary_size=args.secondary_size,
        secondary_degree_region=args.secondary_degree_region,
    )
    cnf.to_file(args.output)
    if args.map is not None:
        args.map.write_text(
            json.dumps(
                {str(variable): list(name) for name, variable in pool.obj2id.items()},
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
    print(
        json.dumps(
            {
                "case": args.case,
                "mode": args.mode,
                "secondary_size": args.secondary_size,
                "secondary_degree_region": args.secondary_degree_region,
                "variables": pool.top,
                "clauses": len(cnf.clauses),
                "sha256": sha256(args.output),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

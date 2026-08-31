#!/usr/bin/env python3
"""Independent exact 0-1 search for a 28-word LD code in Q_7."""

from __future__ import annotations

import argparse
import itertools
import pathlib
import time

import highspy


DIMENSION = 7
VERTEX_COUNT = 1 << DIMENSION
NEIGHBORS = tuple(
    tuple(vertex ^ (1 << coordinate) for coordinate in range(DIMENSION))
    for vertex in range(VERTEX_COUNT)
)
CLOSED_NEIGHBORHOODS = tuple(
    frozenset({vertex, *NEIGHBORS[vertex]}) for vertex in range(VERTEX_COUNT)
)


def scratch_path(raw_path: str) -> pathlib.Path:
    path = pathlib.Path(raw_path).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("generated solver artifacts must stay under /scratch")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("branch", type=int, choices=range(4))
    parser.add_argument("--time-limit", type=float, default=1800.0)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--mps", metavar="SCRATCH_PATH")
    parser.add_argument(
        "--isolated-bound",
        action="store_true",
        help="use the proved lower bound of 22 isolated codewords",
    )
    parser.add_argument(
        "--singleton-bound",
        action="store_true",
        help="use the proved lower bound of 50 singleton signatures",
    )
    parser.add_argument(
        "--distance-two-bound",
        action="store_true",
        help="use the proved lower bound of 44 distance-two code pairs",
    )
    args = parser.parse_args()

    started = time.monotonic()
    model = highspy.Highs()
    model.setOptionValue("time_limit", args.time_limit)
    model.setOptionValue("threads", args.threads)
    model.setOptionValue("mip_detect_symmetry", True)
    variables = model.addBinaries(
        VERTEX_COUNT, out_array=True, name_prefix="x"
    )

    model.addConstr(model.qsum(variables) == 28, name="cardinality")
    for vertex in range(VERTEX_COUNT):
        model.addConstr(
            model.qsum(variables[list(CLOSED_NEIGHBORHOODS[vertex])]) >= 1,
            name=f"dom_{vertex}",
        )

    # As in the SAT encoding, domination makes every separation constraint
    # except those for pairs at distance two redundant.
    separation_count = 0
    for first, second in itertools.combinations(range(VERTEX_COUNT), 2):
        if (first ^ second).bit_count() != 2:
            continue
        witnesses = sorted(
            CLOSED_NEIGHBORHOODS[first]
            ^ CLOSED_NEIGHBORHOODS[second]
        )
        model.addConstr(
            variables[first]
            + variables[second]
            + model.qsum(variables[witnesses])
            >= 1,
            name=f"sep_{first}_{second}",
        )
        separation_count += 1
    assert separation_count == 1344

    model.addConstr(variables[0] == 1, name="normalize_zero")
    for coordinate in range(DIMENSION):
        model.addConstr(
            variables[1 << coordinate]
            == (1 if coordinate < args.branch else 0),
            name=f"origin_degree_{coordinate}",
        )

    # The normalized origin has minimum induced degree in the code.
    if args.branch:
        for vertex in range(VERTEX_COUNT):
            model.addConstr(
                model.qsum(variables[list(NEIGHBORS[vertex])])
                >= args.branch * variables[vertex],
                name=f"minimum_degree_{vertex}",
            )

    if args.isolated_bound:
        if args.branch != 0:
            raise ValueError("the isolated-codeword reduction leaves only branch 0")
        nonisolated = model.addBinaries(
            VERTEX_COUNT, out_array=True, name_prefix="nonisolated"
        )
        for vertex in range(VERTEX_COUNT):
            # For binary variables, these inequalities make nonisolated_v
            # equivalent to x_v and a nonzero selected-neighbour count.
            model.addConstr(
                nonisolated[vertex] <= variables[vertex],
                name=f"nonisolated_selected_{vertex}",
            )
            model.addConstr(
                nonisolated[vertex]
                <= model.qsum(variables[list(NEIGHBORS[vertex])]),
                name=f"nonisolated_neighbor_upper_{vertex}",
            )
            for neighbor in NEIGHBORS[vertex]:
                model.addConstr(
                    nonisolated[vertex]
                    >= variables[vertex] + variables[neighbor] - 1,
                    name=f"nonisolated_neighbor_lower_{vertex}_{neighbor}",
                )
        model.addConstr(model.qsum(nonisolated) <= 6, name="nonisolated_count")

    if args.singleton_bound:
        if args.branch != 0:
            raise ValueError("the family-count reduction leaves only branch 0")
        singleton = model.addBinaries(
            VERTEX_COUNT, out_array=True, name_prefix="singleton"
        )
        for vertex in range(VERTEX_COUNT):
            cover = model.qsum(
                variables[list(CLOSED_NEIGHBORHOODS[vertex])]
            )
            # Domination already gives cover >= 1.  These two inequalities
            # make singleton_v equivalent to cover == 1.
            model.addConstr(
                cover >= 2 - singleton[vertex],
                name=f"singleton_lower_{vertex}",
            )
            model.addConstr(
                cover <= 8 - 7 * singleton[vertex],
                name=f"singleton_upper_{vertex}",
            )
        model.addConstr(
            model.qsum(singleton) >= 50, name="singleton_count"
        )
        model.addConstr(
            model.qsum(singleton) <= 56, name="singleton_count_upper"
        )

    if args.isolated_bound and args.singleton_bound:
        model.addConstr(
            model.qsum(nonisolated) + model.qsum(singleton) <= 56,
            name="singleton_nonisolated_joint_bound",
        )

    if args.distance_two_bound:
        distance_two_pairs = [
            (first, second)
            for first, second in itertools.combinations(range(VERTEX_COUNT), 2)
            if (first ^ second).bit_count() == 2
        ]
        assert len(distance_two_pairs) == 1344
        pair_selected = model.addBinaries(
            len(distance_two_pairs), out_array=True, name_prefix="distance_two"
        )
        for index, (first, second) in enumerate(distance_two_pairs):
            model.addConstr(
                pair_selected[index] <= variables[first],
                name=f"distance_two_left_{first}_{second}",
            )
            model.addConstr(
                pair_selected[index] <= variables[second],
                name=f"distance_two_right_{first}_{second}",
            )
            model.addConstr(
                pair_selected[index]
                >= variables[first] + variables[second] - 1,
                name=f"distance_two_lower_{first}_{second}",
            )
        model.addConstr(
            model.qsum(pair_selected) >= 44,
            name="distance_two_pair_count",
        )
        if args.singleton_bound:
            model.addConstr(
                model.qsum(pair_selected)
                >= 2 * model.qsum(singleton) - 56,
                name="distance_two_singleton_link",
            )

    if args.mps:
        model.writeModel(str(scratch_path(args.mps)))

    print(
        f"branch {args.branch}: {model.numVariables} variables, "
        f"{model.numConstrs} constraints; built in "
        f"{time.monotonic() - started:.3f}s",
        flush=True,
    )
    model.run()
    status = model.getModelStatus()
    print(f"status: {model.modelStatusToString(status)}", flush=True)
    print(f"nodes: {model.getInfo().mip_node_count}", flush=True)
    if status == highspy.HighsModelStatus.kOptimal:
        values = model.getSolution().col_value
        code = [
            vertex
            for vertex, value in enumerate(values)
            if value > 0.5
        ]
        print("code:", " ".join(f"{vertex:07b}" for vertex in code))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact 0-1 formulation for exploratory Q_7 size-29 searches.

This program is not part of the eight-orbit certificate.  A time limit without
a solution is not a nonexistence proof.
"""

from __future__ import annotations

import argparse
import itertools
import time

import highspy


DIMENSION = 7
VERTEX_COUNT = 1 << DIMENSION
NEIGHBORHOODS = tuple(
    frozenset(
        {vertex, *(vertex ^ (1 << coordinate) for coordinate in range(DIMENSION))}
    )
    for vertex in range(VERTEX_COUNT)
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, default=29)
    parser.add_argument("--zero-degree", type=int, choices=range(4))
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--threads", type=int, default=2)
    parser.add_argument(
        "--mps",
        help="optional output path under /scratch for the generated MPS",
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

    # Adding codewords preserves location-domination, so existence at size at
    # most K is equivalent to existence at size exactly K.
    model.addConstr(
        model.qsum(variables) == args.bound, name="exact_cardinality"
    )
    for vertex in range(VERTEX_COUNT):
        model.addConstr(
            model.qsum(variables[list(NEIGHBORHOODS[vertex])]) >= 1,
            name=f"dom_{vertex}",
        )
    for first, second in itertools.combinations(range(VERTEX_COUNT), 2):
        witnesses = sorted(
            NEIGHBORHOODS[first] ^ NEIGHBORHOODS[second]
        )
        model.addConstr(
            variables[first]
            + variables[second]
            + model.qsum(variables[witnesses])
            >= 1,
            name=f"sep_{first}_{second}",
        )

    # Translation normalizes a nonempty code to contain zero.
    model.addConstr(variables[0] == 1, name="normalize_zero")
    if args.zero_degree is not None:
        # The excess/average-degree bound gives a codeword of induced degree
        # at most 3 when |C| <= 29.  After translating it to zero, coordinate
        # permutations make its exact neighbor pattern canonical.  Thus the
        # four accepted values cover the entire search losslessly.
        for coordinate in range(DIMENSION):
            model.addConstr(
                variables[1 << coordinate]
                == (1 if coordinate < args.zero_degree else 0),
                name=f"degree_{coordinate}",
            )
    if args.mps:
        model.writeModel(args.mps)

    print(
        f"built {model.numVariables} variables and {model.numConstrs} "
        f"constraints in {time.monotonic() - started:.3f}s",
        flush=True,
    )
    model.run()
    status = model.getModelStatus()
    print(f"status: {model.modelStatusToString(status)}")
    print(f"nodes: {model.getInfo().mip_node_count}")
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

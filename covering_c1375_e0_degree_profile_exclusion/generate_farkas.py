#!/usr/bin/env python3
"""Regenerate deterministic rounded Farkas certificates with HiGHS."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import highspy
import numpy as np

import e0_degree_profile_exclusion as proof


SCALES = (10, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000, 1_000_000_000)


def solve(variable_count: int, rows: list[proof.Row]) -> highspy.Highs:
    starts = []
    indices = []
    values = []
    lower = []
    upper = []
    for row in rows:
        starts.append(len(indices))
        indices.extend(row.columns)
        values.extend([1.0] * len(row.columns))
        lower.append(-highspy.kHighsInf if row.lower is None else float(row.lower))
        upper.append(highspy.kHighsInf if row.upper is None else float(row.upper))
    solver = highspy.Highs()
    for name, value in (
        ("output_flag", False),
        ("presolve", "off"),
        ("solver", "simplex"),
        ("simplex_strategy", 1),
        ("threads", 1),
        ("random_seed", 0),
    ):
        if solver.setOptionValue(name, value) != highspy.HighsStatus.kOk:
            raise RuntimeError(f"HiGHS rejected {name}={value}")
    solver.addVars(variable_count, np.zeros(variable_count), np.ones(variable_count))
    solver.addRows(
        len(rows),
        np.asarray(lower, dtype=np.float64),
        np.asarray(upper, dtype=np.float64),
        len(indices),
        np.asarray(starts, dtype=np.int32),
        np.asarray(indices, dtype=np.int32),
        np.asarray(values, dtype=np.float64),
    )
    if solver.run() != highspy.HighsStatus.kOk:
        raise RuntimeError("HiGHS run failed")
    if solver.getModelStatus() != highspy.HighsModelStatus.kInfeasible:
        raise RuntimeError(f"expected infeasible LP, got {solver.getModelStatus()}")
    return solver


def exact_integer_ray(variable_count: int, rows: list[proof.Row], solver: highspy.Highs):
    status, exists, ray = solver.getDualRay()
    if status != highspy.HighsStatus.kOk or not exists:
        raise RuntimeError("HiGHS did not return a dual ray")
    maximum = max(abs(float(value)) for value in ray)
    if not maximum:
        raise RuntimeError("zero dual ray")
    for scale in SCALES:
        integers = [int(round(float(value) / maximum * scale)) for value in ray]
        divisor = math.gcd(*map(abs, integers))
        if divisor:
            integers = [value // divisor for value in integers]
        sparse = [[index, value] for index, value in enumerate(integers) if value]
        metrics = proof.farkas_metrics(variable_count, rows, sparse)
        if metrics["gap"] > 0:
            return sparse, metrics, scale
    raise RuntimeError("rounded ray did not retain a strict exact gap")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_link", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    source = proof.read_source(args.source_link)
    second = proof.second_link(source)
    group = proof.generated_group(second, proof.GROUP_GENERATORS)
    orbits = proof.profile_orbits(group)
    cases = []
    for orbit in proof.EXCLUDED_ORBITS:
        profile, orbit_size = orbits[orbit]
        primary, rows = proof.build_rows(second, profile)
        sparse, metrics, scale = exact_integer_ray(len(primary), rows, solve(len(primary), rows))
        partition = sorted((value for value in profile if value), reverse=True)
        case = {
            "orbit": orbit,
            "representative": list(profile),
            "orbit_size": orbit_size,
            "partition": partition,
            "row_count": len(rows),
            "matrix_nonzeros": sum(len(row.columns) for row in rows),
            "rounding_scale": scale,
            **metrics,
            "multipliers": sparse,
        }
        cases.append(case)
        print(
            f"orbit={orbit} support={metrics['support']} scale={scale} gap={metrics['gap']}",
            flush=True,
        )
    document = {
        "format": "C1375-e0-degree-profile-farkas-v1",
        "source_link_sha256": proof.sha256(args.source_link),
        "second_link_sha256": proof.second_link_sha256(second),
        "group_generators": [list(row) for row in proof.GROUP_GENERATORS],
        "group_order": len(group),
        "profile_orbits": len(orbits),
        "labeled_profiles": sum(size for _, size in orbits),
        "excluded_orbits": list(proof.EXCLUDED_ORBITS),
        "generator": {"highspy": highspy.Highs().version(), "numpy": np.__version__},
        "cases": cases,
    }
    args.output.write_text(
        json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="ascii",
    )
    proof.verify(args.source_link, args.output)
    print(f"wrote={args.output} sha256={proof.sha256(args.output)}")


if __name__ == "__main__":
    main()

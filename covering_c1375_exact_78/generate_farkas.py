#!/usr/bin/env python3
"""Deterministically regenerate all new exact Farkas certificates."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import highspy
import numpy as np

import exact_78 as proof


SCALES = (10, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000, 1_000_000_000)


def exact_integer_ray(variable_count: int, rows: list[proof.Row]):
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
        raise RuntimeError(f"expected infeasible, got {solver.modelStatusToString(solver.getModelStatus())}")
    status, exists, ray = solver.getDualRay()
    if status != highspy.HighsStatus.kOk or not exists:
        raise RuntimeError("HiGHS supplied no dual ray")
    divisor = max(abs(float(value)) for value in ray)
    if not divisor:
        raise RuntimeError("zero dual ray")
    for scale in SCALES:
        integers = [int(round(float(value) / divisor * scale)) for value in ray]
        common = math.gcd(*map(abs, integers))
        if common:
            integers = [value // common for value in integers]
        sparse = [[i, value] for i, value in enumerate(integers) if value]
        metrics = proof.farkas_metrics(variable_count, rows, sparse)
        if metrics["gap"] > 0:
            return sparse, metrics, scale
    raise RuntimeError("no rounded exact ray has positive gap")


def make_case(variable_count, rows, **metadata):
    sparse, metrics, scale = exact_integer_ray(variable_count, rows)
    return {
        **metadata,
        "row_count": len(rows),
        "matrix_nonzeros": sum(len(row.columns) for row in rows),
        "rounding_scale": scale,
        **metrics,
        "multipliers": sparse,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_link", type=Path)
    parser.add_argument("prior_witness", type=Path)
    parser.add_argument("prior_certificates", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    source = proof.read_source(args.source_link)
    second = proof.second_link(source)
    group = proof.generated_group(second)
    profiles = proof.profile_orbits(group)

    profile_cases = []
    for orbit, (profile, orbit_size) in enumerate(profiles):
        if orbit == proof.SURVIVING_PROFILE_ORBIT:
            continue
        case = make_case(
            462,
            proof.link_rows(second, profile),
            orbit=orbit,
            representative=list(profile),
            orbit_size=orbit_size,
            partition=sorted((x for x in profile if x), reverse=True),
        )
        profile_cases.append(case)
        print(
            f"profile={orbit:03d} support={case['support']} scale={case['rounding_scale']} gap={case['gap']}",
            flush=True,
        )

    witness = proof.read_blocks(args.prior_witness, 6, set(proof.R))
    source_extension = tuple(block for block in source if 1 not in block)
    canonical = (tuple(sorted(source_extension)), tuple(sorted(witness)))
    completion_cases = []
    for pair in ((0, 0), (0, 1)):
        rows, residual = proof.completion_rows(second, canonical[pair[0]], canonical[pair[1]])
        case = make_case(
            330,
            rows,
            pair=list(pair),
            residual_five_sets=residual,
        )
        completion_cases.append(case)
        print(
            f"completion={pair} residual={residual} support={case['support']} "
            f"scale={case['rounding_scale']} gap={case['gap']}",
            flush=True,
        )

    document = {
        "format": "C1375-exact-78-farkas-v1",
        "source_link_sha256": proof.sha256(args.source_link),
        "prior_witness_sha256": proof.sha256(args.prior_witness),
        "prior_certificate_sha256": proof.sha256(args.prior_certificates),
        "generator": {"highspy": highspy.Highs().version(), "numpy": np.__version__},
        "profile_cases": profile_cases,
        "completion_cases": completion_cases,
    }
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="ascii")
    proof.verify_all(args.source_link, args.prior_witness, args.prior_certificates, args.output)
    print(f"wrote={args.output} sha256={hashlib.sha256(args.output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()

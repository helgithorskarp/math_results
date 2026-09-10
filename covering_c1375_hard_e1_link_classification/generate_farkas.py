#!/usr/bin/env python3
"""Generate rounded exact Farkas certificates from deterministic HiGHS rays."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import highspy
import numpy as np

import hard_e1_link_classification as proof


SCALES = (10, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000)


def exact_integer_ray(rows: list[proof.Row]) -> tuple[list[list[int]], dict[str, int], int]:
    starts: list[int] = []
    indices: list[int] = []
    values: list[float] = []
    lower: list[float] = []
    upper: list[float] = []
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
            raise RuntimeError(f"HiGHS rejected option {name}={value}")
    n = len(proof.CANDIDATES)
    solver.addVars(n, np.zeros(n), np.ones(n))
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
        raise RuntimeError("expected an infeasible LP")
    ray_status, ray_exists, ray = solver.getDualRay()
    if ray_status != highspy.HighsStatus.kOk or not ray_exists:
        raise RuntimeError("HiGHS did not return a dual ray")
    max_abs = max(abs(float(value)) for value in ray)
    if not max_abs:
        raise RuntimeError("zero dual ray")
    for scale in SCALES:
        integers = [int(round(float(value) / max_abs * scale)) for value in ray]
        sparse = [[index, value] for index, value in enumerate(integers) if value]
        metrics = proof.farkas_metrics(rows, sparse)
        if metrics["gap"] > 0:
            return sparse, metrics, scale
    raise RuntimeError("rounded ray did not retain a strict exact gap")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_link", type=Path)
    parser.add_argument("witness", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    source = proof.read_source(args.source_link)
    second = proof.second_link(source)
    witness = proof.read_witness(args.witness)
    proof.verify_witness(source, second, witness)
    cases = []
    for orbit, (high, orbit_size) in enumerate(proof.HIGH_ORBITS):
        blocker = witness if orbit == 11 else None
        rows = proof.build_rows(second, high, blocker)
        sparse, metrics, scale = exact_integer_ray(rows)
        case = {
            "orbit": orbit,
            "high": list(high),
            "high_orbit_size": orbit_size,
            "known_blocker": blocker is not None,
            "row_count": len(rows),
            "matrix_nonzeros": sum(len(row.columns) for row in rows),
            "rounding_scale": scale,
            **metrics,
            "multipliers": sparse,
        }
        cases.append(case)
        print(
            f"orbit={orbit} rows={len(rows)} support={metrics['support']} "
            f"scale={scale} gap={metrics['gap']}",
            flush=True,
        )
    document = {
        "format": "C1375-hard-e1-link-farkas-v1",
        "source_link_sha256": hashlib.sha256(args.source_link.read_bytes()).hexdigest(),
        "witness_sha256": hashlib.sha256(args.witness.read_bytes()).hexdigest(),
        "generator": {"highspy": highspy.Highs().version(), "numpy": np.__version__},
        "cases": cases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="ascii")
    proof.verify_certificates(second, witness, args.output)
    print(f"wrote={args.output} sha256={proof.sha256(args.output)}")


if __name__ == "__main__":
    main()

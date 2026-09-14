#!/usr/bin/env python3
"""Exact orbit preflight; inherited dense-coordinate producer is hash-pinned."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def load_backend(name, pins):
    path = HERE.parent / "hadwiger_nelson_t721_weighted_cover" / name
    if hashlib.sha256(path.read_bytes()).hexdigest() != pins["inherited_files"][name]:
        raise ValueError("inherited source identity")
    spec = importlib.util.spec_from_file_location("t721_orbit_producer_geometry", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def conjugate(point, mask):
    return tuple(-v if ((i % 8) & mask).bit_count() % 2 else v
                 for i, v in enumerate(point))


def orbit_partition(points):
    groups = {}
    closure = set()
    for index, point in enumerate(points):
        images = {conjugate(point, mask) for mask in range(8)}
        closure.update(images)
        groups.setdefault(min(images), []).append(index)
    return groups, closure


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    pins = json.loads((HERE / "provenance.json").read_text())
    if hashlib.sha256(args.input.read_bytes()).hexdigest() != pins["input_sha256"]:
        raise ValueError("coordinate input identity")
    native = load_backend("native.py", pins)
    half = native.half(args.input)
    full = sorted(set(half) | {native.transform(p) for p in half})
    scale = math.lcm(*(x.denominator for p in full for x in p))
    points = [tuple(int(x * scale) for x in p) for p in full]
    if scale != 96 or len(points) != 1441:
        raise ValueError("source reconstruction")
    groups, closure = orbit_partition(points)
    occupancy = {}
    for group in groups.values():
        occupancy[str(len(group))] = occupancy.get(str(len(group)), 0) + 1
    result = {
        "source_points": len(points), "scale": scale,
        "source_points_sha256": digest(points),
        "galois_closure_points": len(closure),
        "galois_closure_sha256": digest(sorted(closure)),
        "source_orbits": len(groups),
        "source_orbit_occupancy": occupancy,
        "transversal_sha256": digest(sorted(groups)),
        "image_lower_bound": len(groups), "target_cap": 508,
        "cap_excluded": len(groups) > 508,
        "edge_preservation_tested": False,
        "chromaticity_tested": False, "record_candidate": False,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

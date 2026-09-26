#!/usr/bin/env python3
"""Replay the complete plane-reflection bound; no third-party Python packages."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from math import comb
from pathlib import Path
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
FULL = (1 << 25) - 1


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value):
    return sha256(canonical(value)).hexdigest()


def geometry(dimension):
    points = list(product(range(5), repeat=dimension))
    index = {p: i for i, p in enumerate(points)}
    directions = [v for v in points if any(v) and next(x for x in v if x) == 1]
    lines = sorted({tuple(sorted(index[tuple((p[j] + t * v[j]) % 5
                                            for j in range(dimension))]
                                 for t in range(5)))
                    for p in points for v in directions})
    if len(lines) != {2: 30, 3: 775}[dimension]:
        raise ValueError("incorrect geometry")
    return points, index, directions, lines


def affine_orbit_check(representatives):
    """Independently check disjoint affine orbits, using complement images."""
    points, index, _, planar_lines = geometry(2)
    line_masks = [sum(1 << p for p in line) for line in planar_lines]
    maps = []
    for a, b, c, d in product(range(5), repeat=4):
        if (a * d - b * c) % 5 == 0:
            continue
        for e, f in points:
            maps.append([index[((a * y + b * z + e) % 5,
                                (c * y + d * z + f) % 5)] for y, z in points])
    if len(maps) != 12000 or len({tuple(g) for g in maps}) != 12000:
        raise ValueError("wrong affine group")
    seen = bytearray(1 << 25)
    covered = Counter()
    classes = Counter()
    for n, mask, multiplicity in representatives:
        if mask.bit_count() != n or any(mask & line == line for line in line_masks):
            raise ValueError("bad representative")
        holes = [p for p in range(25) if not mask >> p & 1]
        orbit = {FULL ^ sum(1 << g[p] for p in holes) for g in maps}
        if min(orbit) != mask or len(orbit) != multiplicity:
            raise ValueError("incorrect orbit record")
        for image in orbit:
            if seen[image]:
                raise ValueError("overlapping orbits")
            seen[image] = 1
        covered[n] += len(orbit)
        classes[n] += 1
    return [{"size": n, "line_free": covered[n], "orbits": classes[n]}
            for n in sorted(covered)]


def allowed_direct(b, c):
    """Definition-level D(B,C), with all 25 slopes."""
    result = 0
    for y, z in product(range(5), repeat=2):
        safe = True
        for s, t in product(range(5), repeat=2):
            p = [5 * ((y + k * s) % 5) + (z + k * t) % 5 for k in range(5)]
            if all(mask >> p[k] & 1 for k, mask in [(1, b), (2, c), (3, c), (4, b)]):
                safe = False
                break
        if safe:
            result |= 1 << (5 * y + z)
    return result


def lift(a, b, c):
    return [25 * x + p for x, mask in enumerate([a, b, c, c, b])
            for p in range(25) if mask >> p & 1]


def check_set(selected, lines, expected_size):
    chosen = set(selected)
    if len(chosen) != len(selected) or len(chosen) != expected_size:
        raise ValueError("incorrect witness cardinality")
    if not chosen <= set(range(125)) or any(set(line) <= chosen for line in lines):
        raise ValueError("witness contains a full affine line")


def plane_profiles(selected, points, normals):
    profiles = Counter()
    for normal in normals:
        counts = [0] * 5
        for p in selected:
            counts[sum(a * b for a, b in zip(points[p], normal)) % 5] += 1
        profiles[tuple(sorted(counts))] += 1
    return [{"profile": list(p), "directions": count} for p, count in sorted(profiles.items())]


def controls(table):
    points, index, normals, lines = geometry(3)
    for row in table:
        b, c, a = row["example_b"], row["example_c"], row["example_allowed"]
        if allowed_direct(b, c) != a:
            raise ValueError("extremal D differs from definition")
        check_set(lift(a, b, c), lines, row["upper_total"])
    witness = json.loads((HERE / "witness70.json").read_text())
    a, b, c, c2, b2 = witness["layers"]
    if c != c2 or b != b2 or allowed_direct(b, c) != a:
        raise ValueError("incorrect reflected witness layers")
    selected = witness["points"]
    if lift(a, b, c) != selected:
        raise ValueError("witness decoding mismatch")
    check_set(selected, lines, 70)
    if {index[(-points[p][0] % 5, points[p][1], points[p][2])] for p in selected} != set(selected):
        raise ValueError("witness lacks the asserted plane reflection")
    comparisons = {}
    for name, path in [
        ("reflected", HERE / "witness70.json"),
        ("paper_figure4", HERE.parent / "known70.json"),
        ("order_three", HERE.parent / "odd_symmetry" / "witness70.json"),
    ]:
        sample = json.loads(path.read_text())["points"]
        check_set(sample, lines, 70)
        comparisons[name] = plane_profiles(sample, points, normals)
    if len({canonical(x) for x in comparisons.values()}) != 3:
        raise ValueError("three construction profiles are not distinct")
    # Products give a positive 64-set; selecting its central layer gives
    # an 80-set with transverse lines and must be rejected.
    rectangle = sum(1 << (5 * y + z) for y in range(4) for z in range(4))
    if allowed_direct(rectangle, rectangle) != 0:
        raise ValueError("zero-slope control failed")
    check_set(lift(0, rectangle, rectangle), lines, 64)
    try:
        check_set(lift(rectangle, rectangle, rectangle), lines, 80)
    except ValueError:
        pass
    else:
        raise ValueError("80-point negative control was accepted")
    return {"checked_affine_lines": len(lines),
            "boundary_examples": len(table), "witness_size": 70,
            "profile_comparison": comparisons, "cartesian_positive": 64,
            "cartesian_negative": 80}


def aggregate(rows):
    table = []
    for b, c in sorted({(r["bsize"], r["csize"]) for r in rows}):
        group = [r for r in rows if (r["bsize"], r["csize"]) == (b, c)]
        maximum = max(r["max_allowed"] for r in group)
        example = next(r for r in group if r["max_allowed"] == maximum)
        histogram = Counter()
        for row in group:
            if sum(row["histogram"].values()) != row["line_free_c"]:
                raise ValueError("incomplete C histogram")
            if row["subsets"] != comb(25, c):
                raise ValueError("incomplete fixed-size census")
            if row["relaxation_survivors71"] or 2 * (b + c) + row["max_allowed"] > 70:
                raise ValueError("reflection upper bound failed")
            for size, count in row["histogram"].items():
                histogram[int(size)] += count * row["b_orbit"]
        n_b = sum(r["b_orbit"] for r in group)
        n_c = group[0]["line_free_c"]
        if sum(histogram.values()) != n_b * n_c:
            raise ValueError("incomplete labelled pair count")
        table.append({"b": b, "c": c, "b_classes": len(group),
                      "line_free_b": n_b, "line_free_c": n_c,
                      "representative_pairs": len(group) * n_c,
                      "labelled_pairs": n_b * n_c,
                      "max_allowed": maximum, "upper_total": 2 * (b + c) + maximum,
                      "example_b": example["b"], "example_c": example["example_c"],
                      "example_allowed": example["example_allowed"],
                      "weighted_histogram": dict(sorted(histogram.items()))})
    return table


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--sanitize", action="store_true",
                        help="sanitize full catalogue, planar cap and all c=16 cases")
    args = parser.parse_args()
    out = args.out.resolve() if args.out else Path(tempfile.mkdtemp(prefix="affine-asymmetry71-"))
    out.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    flags = ["-std=c++20", "-Wall", "-Wextra", "-Wconversion", "-Werror", "-pedantic"]
    flags += (["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer",
               "-fno-pie", "-no-pie"] if args.sanitize else ["-O3"])
    binaries = {}
    for name in ["catalogue", "paired_sections", "direct_lines"]:
        binary = out / name
        subprocess.run(["g++", *flags, str(HERE / (name + ".cpp")), "-o", str(binary)], check=True)
        binaries[name] = str(binary)
    census = subprocess.run([binaries["catalogue"]], capture_output=True, text=True, check=True)
    if census.stdout != (HERE / "REPRESENTATIVES.txt").read_text():
        raise ValueError("representative catalogue mismatch")
    representatives = [list(map(int, s.split())) for s in census.stdout.splitlines()]
    planar = [json.loads(s) for s in census.stderr.splitlines()]
    orbit_check = affine_orbit_check(representatives)
    if orbit_check != [{k: r[k] for k in ["size", "line_free", "orbits"]} for r in planar[:3]]:
        raise ValueError("complement-orbit validation mismatch")
    for row in planar:
        if row["subsets"] != comb(25, row["size"]) or row["covered"] != row["line_free"]:
            raise ValueError("incomplete planar census")
    cap = json.loads(subprocess.check_output([binaries["direct_lines"], "17"],
                                            input=census.stdout, text=True))
    if cap != {"csize": 17, "subsets": comb(25, 17), "line_free_c": 0}:
        raise ValueError("independent planar-cap check failed")
    print("Planar catalogue, all affine orbits, and cap 16 verified.", file=sys.stderr, flush=True)
    rows, partitions = [], {}
    c_values = [16] if args.sanitize else list(range(12, 17))
    for c in c_values:
        records = []
        for name in ["paired_sections", "direct_lines"]:
            result = subprocess.check_output([binaries[name], str(c)],
                                             input=census.stdout, text=True)
            records.append([json.loads(s) for s in result.splitlines()])
        if records[0] != records[1]:
            raise ValueError(("complete enumerations disagree", c))
        wanted = [(n, mask, orbit) for n, mask, orbit in representatives if n >= c and n + c >= 28]
        if [(r["bsize"], r["b"], r["b_orbit"]) for r in records[0]] != wanted:
            raise ValueError("representative partition incomplete")
        rows.extend(records[0])
        partitions[str(c)] = {"records": len(records[0]), "sha256": digest(records[0])}
        print(f"c={c}: all {len(records[0])} representative records agree.", file=sys.stderr, flush=True)
    table = aggregate(rows)
    summary = {"status": "SANITIZED_C16_CHECK_PASSED" if args.sanitize else "COMPLETE_REFLECTION_BOUND_70",
               "planar_census": planar, "representatives_sha256": sha256(census.stdout.encode()).hexdigest(),
               "partitions": partitions, "bounds": table, "controls": controls(table),
               "record_count": len(rows),
               "entrywise_crosschecked_pairs": sum(r["line_free_c"] for r in rows)}
    # Normalize integer dictionary keys to JSON strings before comparison.
    summary = json.loads(json.dumps(summary))
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        if args.sanitize:
            expected["status"] = summary["status"]
            expected["partitions"] = {"16": expected["partitions"]["16"]}
            expected["bounds"] = [r for r in expected["bounds"] if r["c"] == 16]
            expected["controls"]["boundary_examples"] = 1
            expected["record_count"] = expected["partitions"]["16"]["records"]
            expected["entrywise_crosschecked_pairs"] = sum(r["representative_pairs"] for r in expected["bounds"])
        if summary != expected:
            raise ValueError("expected-output mismatch")
    output = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    (out / "result.json").write_text(output)
    print(output, end="")
    print(f"Completed in {time.monotonic() - started:.3f} seconds; outputs: {out}",
          file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()

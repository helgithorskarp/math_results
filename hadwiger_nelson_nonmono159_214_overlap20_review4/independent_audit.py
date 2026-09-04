#!/usr/bin/env python3
"""Independent audit of the mixed Parts 159/214 high-overlap exclusion.

The checker uses only the Python standard library and imports no submitted
module.  It checks every stored transform's exact orthogonality and overlap,
rebuilds both strict base graphs, and independently checks a deterministic
sample of full union colourings.  An optional extracted Parts source-data
directory enables exact coordinate-transcription checks.
"""

from __future__ import annotations

import ast
import hashlib
import itertools
import json
import lzma
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_nonmono159_214_overlap20"
SHARED = ROOT / "hadwiger_nelson_nonmono159_overlap10"
BASE = ROOT / "hadwiger_nelson_parts509_affine_overlap_scan"

EXPECTED_HASHES = {
    TARGET / "CENSUS.txt": "03beb6cee5ed7a15a461d401a76f6d7b09ee928fd990773626359a565958dc83",
    TARGET / "colorings.txt.xz": "867b9fa9b91ac9c0d8ec09af5508217f1417dce4a6f5120a533eab157fe6ed90",
    TARGET / "overlap_transforms.txt.xz": "5465fc73f2bd9c89a1a110617f4adf2a82d3d72616d7e58ad9155d119ee5ac40",
    TARGET / "points159.tsv": "4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02",
    TARGET / "points214.tsv": "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f",
    TARGET / "verify_colorings.cpp": "504992f8c2d56fc7d51cdf635b035547b9ba1d7ce652047b13818e8869926acb",
    TARGET / "verify.sh": "c9d238eccd0a091903f9a704cdf1aabe8d3999e183eb4fdbfa9b8065d50928a7",
    SHARED / "emit_graphs.cpp": "1dfa3ed4c1bd7032dd0ed0e657cee4e24d26571545ef6aa20a24765900084fe5",
    SHARED / "enumerate_overlaps.cpp": "c9559e88cf901004102d8f6a65040c7934d5183bd28044689477dced991eb09f",
    BASE / "enumerate_overlaps.cpp": "97f63813d3058be87b2b6de32cb3a6b7c4e268eb7e1f49893e9f7cbd51c37b3e",
}
EXPECTED_SOURCE_HASHES = {
    "graphs.txt": "c23fc5ec5e579b097235f3d13d62ad14bf78f440f975cb8d9721bd4c6e94d427",
    "v159e646.vtx": "fcf071687130592493968b0d3ba7596f90b500856eadaf829db48d08da5421e4",
    "v214e977.vtx": "5780a3bc556c9bbaf2585ae2f141388c237fdc77225fb9cd96f62ab61fd4bf8b",
}
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
RAD_INDEX = {value: index for index, value in enumerate(RADICANDS)}
ZERO = (0,) * 8


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def neg(value):
    return tuple(-coefficient for coefficient in value)


def subtract(left, right):
    return add(left, neg(right))


def scale(value, multiplier):
    return tuple(multiplier * coefficient for coefficient in value)


def multiply(left, right):
    result = [0] * 8
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            common = math.gcd(RADICANDS[i], RADICANDS[j])
            radical = RADICANDS[i] * RADICANDS[j] // (common * common)
            result[RAD_INDEX[radical]] += a * b * common
    return tuple(result)


def conjugate(value, mask):
    return tuple(
        -coefficient if (basis_mask & mask).bit_count() % 2 else coefficient
        for basis_mask, coefficient in enumerate(value)
    )


def inverse(value):
    if not any(value):
        raise ZeroDivisionError
    one = (Fraction(1),) + (Fraction(0),) * 7
    numerator = one
    for mask in range(1, 8):
        numerator = multiply(numerator, conjugate(value, mask))
    denominator = multiply(value, numerator)
    if any(denominator[1:]) or not denominator[0]:
        raise ArithmeticError("bad multiquadratic inverse")
    return scale(numerator, 1 / denominator[0])


def parse_field(text):
    values = tuple(map(int, text.split(",")))
    if len(values) != 8:
        raise ValueError("bad field tuple")
    return values


def read_points(path):
    scale_value, points = None, []
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("# scale "):
            scale_value = int(line[8:])
            continue
        if not line or line.startswith("#"):
            continue
        values = tuple(map(int, line.split()))
        if len(values) != 16:
            raise ValueError("bad point row")
        points.append((values[:8], values[8:]))
    if scale_value is None or len(points) != len(set(points)):
        raise ValueError("bad point inventory")
    return scale_value, points


def squared_distance(left, right):
    dx = subtract(left[0], right[0])
    dy = subtract(left[1], right[1])
    return add(multiply(dx, dx), multiply(dy, dy))


def is_unit(left, right, coordinate_scale):
    target = (coordinate_scale * coordinate_scale,) + ZERO[1:]
    return squared_distance(left, right) == target


def strict_edges(points, coordinate_scale):
    return [
        (u, v)
        for u, v in itertools.combinations(range(len(points)), 2)
        if is_unit(points[u], points[v], coordinate_scale)
    ]


def parse_transform_rows():
    rows, nonplacement = [], []
    with lzma.open(TARGET / "overlap_transforms.txt.xz", "rt", encoding="ascii") as stream:
        for raw in stream:
            line = raw.rstrip("\n")
            if not line.startswith("placement="):
                nonplacement.append(line)
                continue
            fields = dict(item.split("=", 1) for item in line.split(";"))
            rows.append({
                "overlaps": int(fields["placement"]),
                "reflected": int(fields["reflected"]),
                "denominator": int(fields["denominator"]),
                "c": parse_field(fields["c"]),
                "s": parse_field(fields["s"]),
                "tx": parse_field(fields["tx"]),
                "ty": parse_field(fields["ty"]),
            })
    rows.sort(key=lambda row: (
        row["reflected"], row["denominator"], row["c"], row["s"],
        row["tx"], row["ty"],
    ))
    if len(rows) != 13184:
        raise ValueError("bad transform count")
    keys = {
        (r["reflected"], r["denominator"], r["c"], r["s"], r["tx"], r["ty"])
        for r in rows
    }
    if len(keys) != len(rows):
        raise ValueError("duplicate transform")

    census = (TARGET / "CENSUS.txt").read_text(encoding="ascii").splitlines()
    if nonplacement != census[:-1] or census[-1] != "placements_with_at_least_twenty_overlaps=13184":
        raise ValueError("compressed transform census disagrees with CENSUS.txt")
    expected_histogram = {
        int(line.split("=", 1)[0][8:]): int(line.split("=", 1)[1])
        for line in census if line.startswith("overlap_")
    }
    actual_histogram = Counter(row["overlaps"] for row in rows)
    if {k: v for k, v in expected_histogram.items() if k >= 20} != dict(actual_histogram):
        raise ValueError("high-overlap histogram mismatch")
    return rows


def read_witnesses():
    witnesses, headers, flags = {}, {}, set()
    with lzma.open(TARGET / "colorings.txt.xz", "rt", encoding="ascii") as stream:
        for raw in stream:
            line = raw.rstrip("\n")
            if line.startswith("graph="):
                row = dict(item.split("=", 1) for item in line.split(";"))
                index = int(row["graph"])
                if row["status"] != "SAT" or index in witnesses:
                    raise ValueError("bad witness row")
                witnesses[index] = {
                    "order": int(row["order"]),
                    "edges": int(row["edges"]),
                    "colors": row["colors"],
                }
            else:
                key, value = line.split("=", 1)
                if value == "true":
                    flags.add(key)
                else:
                    headers[key] = int(value)
    if headers != {"graphs": 13184, "unsat": 0} or flags != {"direct_witness_verification"}:
        raise ValueError("bad witness headers or trailer")
    if sorted(witnesses) != list(range(13184)):
        raise ValueError("witness indices are incomplete")
    result = [witnesses[index] for index in range(13184)]
    for witness in result:
        if len(witness["colors"]) != witness["order"] or not set(witness["colors"]) <= set("0123"):
            raise ValueError("bad colouring string")
    return result


def oriented_images(transform, right):
    c, s = transform["c"], transform["s"]
    result = []
    for x, y in right:
        cx, sy = multiply(c, x), multiply(s, y)
        sx, cy = multiply(s, x), multiply(c, y)
        if transform["reflected"]:
            result.append((add(cx, sy), subtract(sx, cy)))
        else:
            result.append((subtract(cx, sy), add(sx, cy)))
    return result


def translated_image(oriented, transform):
    tx, ty = transform["tx"], transform["ty"]
    return [(add(x, tx), add(y, ty)) for x, y in oriented]


def union_points(left_scaled, right_image):
    index, points = {}, []
    for point in [*left_scaled, *right_image]:
        if point not in index:
            index[point] = len(index)
            points.append(point)
    return points


def audit_transforms_and_sample_colourings(left, right, transforms, witnesses, base_scale):
    orientation_cache, left_cache = {}, {}
    all_overlap_checks = 0
    for index, (transform, witness) in enumerate(zip(transforms, witnesses, strict=True)):
        denominator = transform["denominator"]
        if denominator <= 0 or transform["reflected"] not in (0, 1):
            raise ValueError("bad orientation metadata")
        norm = add(multiply(transform["c"], transform["c"]),
                   multiply(transform["s"], transform["s"]))
        if norm != (denominator * denominator,) + ZERO[1:]:
            raise ValueError("non-orthogonal transform")
        divisor = denominator
        for coefficient in (*transform["c"], *transform["s"]):
            divisor = math.gcd(divisor, abs(coefficient))
        if divisor != 1:
            raise ValueError("noncanonical orientation")

        orientation_key = (
            transform["reflected"], denominator, transform["c"], transform["s"]
        )
        if orientation_key not in orientation_cache:
            orientation_cache[orientation_key] = oriented_images(transform, right)
        right_image = translated_image(orientation_cache[orientation_key], transform)
        if len(set(right_image)) != len(right):
            raise ValueError("transform is not injective")
        if denominator not in left_cache:
            scaled = [(scale(x, denominator), scale(y, denominator)) for x, y in left]
            left_cache[denominator] = (scaled, set(scaled))
        left_scaled, left_scaled_set = left_cache[denominator]
        overlap = len(left_scaled_set & set(right_image))
        all_overlap_checks += len(right)
        if overlap != transform["overlaps"]:
            raise ValueError(f"overlap mismatch at graph {index}")
        if witness["order"] != len(left) + len(right) - overlap:
            raise ValueError(f"witness order mismatch at graph {index}")

    sample = {
        round(i * (len(transforms) - 1) / 15) for i in range(16)
    }
    for key in ("overlaps",):
        sample.add(min(range(len(transforms)), key=lambda i: transforms[i][key]))
        sample.add(max(range(len(transforms)), key=lambda i: transforms[i][key]))
    for key in ("order", "edges"):
        sample.add(min(range(len(witnesses)), key=lambda i: witnesses[i][key]))
        sample.add(max(range(len(witnesses)), key=lambda i: witnesses[i][key]))

    checked_pairs = 0
    for index in sorted(sample):
        transform, witness = transforms[index], witnesses[index]
        orientation_key = (
            transform["reflected"], transform["denominator"],
            transform["c"], transform["s"],
        )
        image = translated_image(orientation_cache[orientation_key], transform)
        points = union_points(left_cache[transform["denominator"]][0], image)
        colors = witness["colors"]
        edges = 0
        for u, v in itertools.combinations(range(len(points)), 2):
            checked_pairs += 1
            if is_unit(points[u], points[v], base_scale * transform["denominator"]):
                edges += 1
                if colors[u] == colors[v]:
                    raise ValueError(f"monochromatic sampled edge at graph {index}")
        if edges != witness["edges"]:
            raise ValueError(f"sampled edge count mismatch at graph {index}")
    return len(orientation_cache), len(sample), all_overlap_checks, checked_pairs


def parse_mathematica_expression(text):
    expression = (
        text.replace("Sqrt[11/3]", "sqrt11over3")
        .replace("Sqrt[", "sqrt").replace("]", "")
    )
    names = {
        "sqrt3": (Fraction(0), Fraction(1), Fraction(0), Fraction(0),
                  Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
        "sqrt5": (Fraction(0), Fraction(0), Fraction(1), Fraction(0),
                  Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
        "sqrt11": (Fraction(0), Fraction(0), Fraction(0), Fraction(0),
                   Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
        "sqrt33": (Fraction(0), Fraction(0), Fraction(0), Fraction(0),
                   Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
        "sqrt11over3": (Fraction(0), Fraction(0), Fraction(0), Fraction(0),
                       Fraction(0), Fraction(1, 3), Fraction(0), Fraction(0)),
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return (Fraction(node.value),) + (Fraction(0),) * 7
        if isinstance(node, ast.Name) and node.id in names:
            return names[node.id]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return neg(evaluate(node.operand))
        if isinstance(node, ast.BinOp):
            left, right = evaluate(node.left), evaluate(node.right)
            if isinstance(node.op, ast.Add):
                return add(left, right)
            if isinstance(node.op, ast.Sub):
                return subtract(left, right)
            if isinstance(node.op, ast.Mult):
                return multiply(left, right)
            if isinstance(node.op, ast.Div):
                return multiply(left, inverse(right))
        raise ValueError("unsupported source coordinate expression")

    return evaluate(ast.parse(expression, mode="eval").body)


def audit_source_transcription(source_dir, point_sets):
    for filename, expected in EXPECTED_SOURCE_HASHES.items():
        if sha256(source_dir / filename) != expected:
            raise ValueError(f"source archive file hash mismatch: {filename}")
    checked = 0
    for filename, (_, points) in zip(("v159e646.vtx", "v214e977.vtx"), point_sets, strict=True):
        lines = (source_dir / filename).read_text(encoding="ascii").splitlines()
        if len(lines) != len(points):
            raise ValueError("source coordinate inventory mismatch")
        for index, (line, point) in enumerate(zip(lines, points, strict=True)):
            x_text, y_text = line[1:-1].split(", ", 1)
            original = (parse_mathematica_expression(x_text), parse_mathematica_expression(y_text))
            transcribed = (scale(point[0], Fraction(1, 12)),
                           scale(point[1], Fraction(1, 12)))
            if original != transcribed:
                raise ValueError(f"coordinate transcription mismatch: {filename}:{index + 1}")
            checked += 1
    return checked


def main():
    for path, expected in EXPECTED_HASHES.items():
        if sha256(path) != expected:
            raise ValueError(f"artifact hash mismatch: {path}")

    left_set = read_points(TARGET / "points159.tsv")
    right_set = read_points(TARGET / "points214.tsv")
    if left_set[0] != 12 or right_set[0] != 12:
        raise ValueError("unexpected coordinate scale")
    left_edges = strict_edges(left_set[1], 12)
    right_edges = strict_edges(right_set[1], 12)
    if len(left_edges) != 646 or len(right_edges) != 977:
        raise ValueError("strict base-edge count mismatch")

    transforms = parse_transform_rows()
    witnesses = read_witnesses()
    orientations, samples, overlap_checks, sampled_pairs = (
        audit_transforms_and_sample_colourings(
            left_set[1], right_set[1], transforms, witnesses, 12
        )
    )
    result = {
        "all_checks": True,
        "graphs": len(transforms),
        "high_overlap_orientations": orientations,
        "max_overlap": max(row["overlaps"] for row in transforms),
        "overlap_membership_checks": overlap_checks,
        "left_edges": len(left_edges),
        "right_edges": len(right_edges),
        "sampled_graphs": samples,
        "sampled_vertex_pairs": sampled_pairs,
    }
    if len(sys.argv) == 2:
        result["source_coordinate_rows"] = audit_source_transcription(
            Path(sys.argv[1]), (left_set, right_set)
        )
    elif len(sys.argv) != 1:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} [extracted-source-directory]")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify the rotated-field obstruction for connectors to E457."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CORE = ROOT / "hadwiger_nelson_e457_equal_pair_source" / "core.json"
COLOURING = ROOT / "hadwiger_nelson_nonmono_field_obstruction" / "coloring.py"
REVIEW = ROOT / "hadwiger_nelson_nonmono_field_obstruction_review3" / "README.md"
DEPENDENCIES = {
    "hadwiger_nelson_e457_equal_pair_source/core.json":
        "d377e9526d13cc76aba6762ecd6a79bd04fe12d61e03a0b585a5ea38820d833b",
    "hadwiger_nelson_nonmono_field_obstruction/coloring.py":
        "a612f6f145f511340d930cf093939cf102128e960ae12977e86dfb1d1e5b486e",
    "hadwiger_nelson_nonmono_field_obstruction_review3/README.md":
        "6fdefb8029066dff966b38cfa0c4aba4ed83c5d293f22de2629ed2037227e2db",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def load_colouring():
    spec = importlib.util.spec_from_file_location("e457_field_colouring", COLOURING)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "missing colouring loader")
    spec.loader.exec_module(module)
    return module


def source_norm(row):
    """Squared norm in F, as rational + coefficient*sqrt(33)."""
    a, b, c, d = row
    return (
        F(3 * a * a + 11 * b * b + c * c + 33 * d * d, 1296),
        F(2 * (a * b + c * d), 1296),
    )


def rotate_to_e(row):
    """Multiply the represented point by conjugate((sqrt(3)+i)/2).

    A returned tuple (A,B,C,D) represents
    A+B*sqrt(33)+C*i*sqrt(3)+D*i*sqrt(11).
    """
    a, b, c, d = row
    return (
        F(3 * a + c, 72),
        F(b + d, 72),
        F(c - a, 72),
        F(3 * d - b, 72),
    )


def e_norm(row):
    a, b, c, d = row
    return (
        a * a + 33 * b * b + 3 * c * c + 11 * d * d,
        2 * (a * b + c * d),
    )


def difference(a, b):
    return tuple(x - y for x, y in zip(a, b, strict=True))


def edge_set(rows):
    return [
        (u, v)
        for u, v in itertools.combinations(range(len(rows)), 2)
        if source_norm(difference(rows[u], rows[v])) == (F(1), F(0))
    ]


def validate_rows(rows):
    require(type(rows) is list and len(rows) == 457, "wrong point count")
    require(all(type(row) is list and len(row) == 4
                and all(type(value) is int for value in row) for row in rows),
            "malformed coordinate row")
    require(len({tuple(row) for row in rows}) == 457, "duplicate physical point")
    require(rows[0] == [0, 0, 0, 0], "wrong O terminal")
    require(rows[1] == [0, 0, 96, 0], "wrong V terminal")


def verify(core_path=CORE, check_hashes=True):
    if check_hashes:
        for relative, expected in DEPENDENCIES.items():
            require(file_hash(ROOT / relative) == expected,
                    f"dependency changed: {relative}")
    core = json.loads(Path(core_path).read_text())
    require(core.get("schema") == "hn-e457-equal-pair-v1", "wrong source schema")
    rows = core.get("points")
    validate_rows(rows)
    transformed = [rotate_to_e(row) for row in rows]
    require(all(source_norm(row) == e_norm(image)
                for row, image in zip(rows, transformed, strict=True)),
            "rotation failed to preserve a source norm")

    edges = edge_set(rows)
    require(len(edges) == 2329, "wrong complete unit-edge count")
    colouring = load_colouring()
    colours = [colouring.color(image) for image in transformed]
    require(set(colours) <= set(range(4)), "invalid field colour")
    require(all(colours[u] != colours[v] for u, v in edges),
            "field word is not proper")
    require(colours[0] == colours[1] == 0, "marked pair is not equal in field word")

    endpoint_image = transformed[1]
    require(endpoint_image == (F(4, 3), F(0), F(4, 3), F(0)),
            "unexpected rotated endpoint")
    histogram = [colours.count(colour) for colour in range(4)]
    return {
        "verified": True,
        "vertices": len(rows),
        "complete_unit_edges": len(edges),
        "physical_pairs_checked": len(rows) * (len(rows) - 1) // 2,
        "ambient_field": "sqrt(3)*Q(i*sqrt(3),i*sqrt(11))",
        "unit_rotation": "(sqrt(3)+i)/2",
        "rotated_endpoint_coefficients": ["4/3", "0", "4/3", "0"],
        "endpoint_colours": [colours[0], colours[1]],
        "colour_histogram": histogram,
        "point_sha256": digest(rows),
        "edge_sha256": digest(edges),
        "field_word_sha256": hashlib.sha256(bytes(colours)).hexdigest(),
        "dependencies": DEPENDENCIES,
        "record_candidate": False,
    }


def main():
    output = verify()
    expected = json.loads((HERE / "expected.json").read_text())
    require(output == expected, "expected output mismatch")
    print(json.dumps(output, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()

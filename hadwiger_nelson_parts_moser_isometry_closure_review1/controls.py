#!/usr/bin/env python3
"""Small exact and adversarial controls for the independent audit."""

from __future__ import annotations

import hashlib
import json
from itertools import combinations, product
from pathlib import Path

import independent_audit as audit


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def brute(edges, masks):
    return any(
        all(masks[i] >> word[i] & 1 for i in range(len(masks)))
        and all(word[a] != word[b] for a, b in edges)
        for word in product(range(4), repeat=len(masks))
    )


def must_fail(callable_, label):
    try:
        callable_()
    except ValueError:
        return
    raise ValueError(f"negative control unexpectedly passed: {label}")


def run():
    inverse_checks = 0
    for seed in range(1, 41):
        value = tuple(((seed * (i + 3) + i * i) % 7) - 3 for i in range(8))
        if value == audit.ZERO:
            continue
        try:
            reciprocal = audit.inverse(value)
        except (StopIteration, ZeroDivisionError):
            continue
        audit.need(audit.mul(value, reciprocal) == audit.ONE, "inverse control")
        inverse_checks += 1

    motif = audit.spindle()
    edges = tuple(
        (a, b)
        for a, b in combinations(range(7), 2)
        if audit.norm(audit.csub(motif[a], motif[b])) == audit.ONE
    )
    counts = {
        colours: sum(
            all(word[a] != word[b] for a, b in edges)
            for word in product(range(colours), repeat=7)
        )
        for colours in (3, 4)
    }
    audit.need(len(edges) == 11 and counts == {3: 0, 4: 384}, "Moser control")

    extension_checks = 0
    for edge_set in ((), ((0, 1),)):
        for left in range(16):
            for right in range(16):
                masks = (left, right)
                audit.need(audit.extendable(edge_set, masks) == brute(edge_set, masks), "two-vertex list control")
                extension_checks += 1
    state = 20260913
    for n in range(1, 6):
        possible_edges = list(combinations(range(n), 2))
        for _ in range(200):
            state = (1103515245 * state + 12345) & 0x7FFFFFFF
            edge_set = tuple(edge for bit, edge in enumerate(possible_edges) if state >> bit & 1)
            masks = []
            for _vertex in range(n):
                state = (1103515245 * state + 12345) & 0x7FFFFFFF
                masks.append(state & 15)
            masks = tuple(masks)
            audit.need(audit.extendable(edge_set, masks) == brute(edge_set, masks), "seeded list control")
            extension_checks += 1

    audit.need(audit.unpack(bytes([0b11100100]), 4) == [0, 1, 2, 3], "colour unpack control")
    must_fail(lambda: audit.unpack(b"", 1), "short packed colour")
    must_fail(lambda: audit.unpack(bytes([0b11000000]), 3), "nonzero unused bits")

    hashes = {
        "parts_points": hashlib.sha256(
            (ROOT / "hadwiger_nelson_parts509_completion_census_degree9/points.tsv").read_bytes()
        ).hexdigest(),
        "parts_deletion_colours": hashlib.sha256(
            (ROOT / "hadwiger_nelson_parts509_criticality/certificate.json").read_bytes()
        ).hexdigest(),
        "quad_colour_library": hashlib.sha256(
            (ROOT / "hadwiger_nelson_parts509_quad_closure/certificate.json.gz").read_bytes()
        ).hexdigest(),
        "target_residual_colours": hashlib.sha256(
            (ROOT / "hadwiger_nelson_parts_moser_isometry_closure/certificate.json").read_bytes()
        ).hexdigest(),
    }
    result = {
        "extension_checks": extension_checks,
        "field_inverse_checks": inverse_checks,
        "input_hashes": hashes,
        "malformed_colour_controls_rejected": 2,
        "moser_colouring_counts": {str(key): value for key, value in counts.items()},
        "moser_edges": len(edges),
        "status": "PASS",
    }
    audit.need(result == json.loads((HERE / "EXPECTED_CONTROLS.json").read_text()), "control expectation")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    run()

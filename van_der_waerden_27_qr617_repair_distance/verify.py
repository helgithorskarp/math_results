#!/usr/bin/env python3
"""Check the QR-617 repair exclusion without importing the generator.

Python 3.11+ standard library only. Coordinates are zero based throughout.
This verifier checks a proof transcript, not search exhaustion or solver UNSAT.
"""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


P = 617
LAST = 6 * P


def require(condition, message):
    if not condition:
        raise ValueError(message)


def qr_color(x):
    """Euler's criterion: QR is color 0, nonresidue is color 1."""
    require(x % P != 0, "Exceptional position has no prescribed color")
    value = pow(x % P, (P - 1) // 2, P)
    require(value in (1, P - 1), "Euler criterion failed")
    return int(value == P - 1)


def progression(pair):
    require(isinstance(pair, list) and len(pair) == 2, "Bad AP encoding")
    a, d = pair
    require(type(a) is int and type(d) is int, "AP coordinates must be integers")
    require(a >= 0 and d > 0 and a + 6 * d <= LAST, "AP outside prefix")
    return {a + j * d for j in range(7)}


def check_elimination(v, pairs, allowed, radius):
    require(type(v) is int and v in allowed, "Duplicate or invalid elimination")
    require(isinstance(pairs, list) and len(pairs) in (1, radius), "Bad witness size")
    petals = []
    for pair in pairs:
        points = progression(pair)
        require(v in points and all(x % P for x in points), "AP must contain v and avoid exceptions")
        others = points - {v}
        require(all(qr_color(x) == 1 - qr_color(v) for x in others), "AP is not critical at v")
        petals.append(others & allowed)
    if any(not petal for petal in petals):
        return "empty"
    require(len(petals) == radius, "Need radius many nonempty petals")
    used = set()
    for petal in petals:
        require(not (petal & used), "Petals intersect")
        used.update(petal)
    return "packing"


def verify(data, certificate_bytes=None):
    require(isinstance(data, dict), "Certificate must be an object")
    require(data.get("format") == "qr617-critical-petals-v1", "Unknown format")
    require(data.get("prime") == P and data.get("prefix_length") == LAST + 1, "Wrong domain")
    require(data.get("reflect_each_record") is True, "Reflection flag missing")
    radius = data.get("radius")
    require(type(radius) is int and radius >= 1, "Invalid radius")
    require(all(P % q for q in range(2, 25)), "617 must be prime")
    allowed = {x for x in range(LAST + 1) if x % P}
    require(len(allowed) == 3696, "Wrong vertex count")
    require(all(qr_color(x) == qr_color(LAST - x) for x in allowed), "Reflection changes colors")
    counts = Counter()
    records = data.get("records")
    require(isinstance(records, list), "Missing records")
    for record in records:
        require(isinstance(record, list) and len(record) == 2, "Bad record")
        v, pairs = record
        mirror = LAST - v if type(v) is int else None
        require(v != mirror, "A nonzero residue cannot be the center")
        kind = check_elimination(v, pairs, allowed, radius)
        reflected = [[LAST - (a + 6 * d), d] for a, d in pairs]
        require(check_elimination(mirror, reflected, allowed, radius) == kind, "Reflection mismatch")
        allowed.remove(v)
        allowed.remove(mirror)
        counts[kind] += 1
    require(not allowed, "Eliminations do not cover all nonzero positions")

    # Directly check two obstructions for the otherwise free new endpoint.
    obstructions = data.get("extension_obstructions")
    require(isinstance(obstructions, list), "Missing endpoint obstructions")
    blocked_colors = set()
    for pair in obstructions:
        require(isinstance(pair, list) and len(pair) == 2, "Bad endpoint AP")
        a, d = pair
        require(type(a) is int and type(d) is int and a >= 0 and d > 0, "Bad endpoint coordinates")
        require(a + 6 * d == LAST + 1, "AP must end at the new endpoint")
        old = [a + j * d for j in range(6)]
        require(all(0 <= x <= LAST and x % P for x in old), "Endpoint AP touches an exception")
        colors = {qr_color(x) for x in old}
        require(len(colors) == 1, "Endpoint AP is not monochromatic on the prefix")
        blocked_colors.update(colors)
    require(blocked_colors == {0, 1}, "Must block both endpoint colors")
    result = {
        "verified": True,
        "excluded_radius_nonzero_positions": radius,
        "required_nonzero_changes": radius + 1,
        "prefix_nonzero_positions": 3696,
        "exceptional_prefix_positions_free": 7,
        "new_endpoint_free": True,
        "records": len(records),
        "packing_records": counts["packing"],
        "empty_records": counts["empty"],
        "eliminated_positions": 3696,
    }
    if certificate_bytes is not None:
        result["certificate_sha256"] = hashlib.sha256(certificate_bytes).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", type=Path, default=Path(__file__).with_name("certificate.json"))
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    print(json.dumps(verify(json.loads(raw), raw), sort_keys=True))


if __name__ == "__main__":
    main()

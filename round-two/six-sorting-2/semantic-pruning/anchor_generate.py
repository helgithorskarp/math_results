"""Regenerate the compact anchor certificate using packed truth functions."""

import argparse
import hashlib
import json
from pathlib import Path

import anchors

ROOT = Path(__file__).resolve().parent
semantic = anchors.semantic


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(",", ":")).encode()).hexdigest()


def compact(data):
    return {name: {"low_count": item["low_count"], "high_count": item["high_count"],
                   "envelope": item["envelope"], "summary": item["summary"],
                   "records_sha256": digest(item["records"]),
                   "mass_trace": [[z["ordinary_mass"], z["semantic_mass"]]
                                  for z in item["trace"]]}
            for name, item in data.items()}


def boolean_profile(n, gates):
    values = list(semantic.truth_columns(n))
    activity = []
    for a, b in gates:
        swapped = values[a] & ~values[b]
        activity.append((swapped & -swapped).bit_length() - 1 if swapped else None)
        values[a], values[b] = values[a] & values[b], values[a] | values[b]
    wrong_bits = failed = 0
    for i, actual in enumerate(values):
        expected = sum(1 << x for x in range(1 << n) if x.bit_count() >= n - i)
        wrong = actual ^ expected
        wrong_bits += wrong.bit_count()
        failed |= wrong
    failures = [x for x in range(1 << n) if (failed >> x) & 1]
    return {"failure_count": len(failures), "wrong_output_bits": wrong_bits,
            "failures_sha256": digest(failures),
            "failures": failures if len(failures) <= 100 else None,
            "activity_witnesses": activity}


def previous_rejection(n, data, budget):
    for cut in range(len(next(iter(data.values()))["trace"])):
        for name, lo, hi in semantic.FAMILIES:
            mass = data[name]["trace"][cut]["semantic_mass"]
            lower = semantic.SIZES[n - lo - hi] + anchors.log_ceiling(mass)
            if lower > budget:
                return {"cut": cut, "family": name, "mass": mass, "lower_bound": lower}
    return None


def build(fixture):
    cert = {"schema": "sorting-semantic-anchor-huffman-v1",
            "agent": "six-sorting-2", "role": "researcher", "cases": {}}
    for case in fixture["cases"]:
        n, gates = case["n"], case["gates"]
        limit = case["profile_size"]
        data = semantic.analyze(n, gates[:limit])
        trace = anchors.prefix_trace(n, gates[:limit])
        cert["cases"][case["name"]] = {
            "n": n, "size": len(gates), "profile_size": limit,
            "families": compact(data), "semantic_anchors": anchors.both(n, data),
            "ordinary_anchors": anchors.both(n, data, False), "anchor_trace": trace,
            "first_rejection": anchors.first_rejection(trace, case["budget"]),
            "previous_first_rejection": previous_rejection(n, data, case["budget"]),
            "boolean": boolean_profile(n, gates)}
    return cert


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    fixture = json.loads((ROOT / "anchor-fixture.json").read_text())
    cert = build(fixture)
    raw = (json.dumps(cert, sort_keys=True, separators=(",", ":")) + "\n").encode()
    path = ROOT / "anchor-certificate.json"
    if args.write:
        path.write_bytes(raw)
    elif path.read_bytes() != raw:
        raise ValueError("anchor certificate differs from complete regeneration")
    print(json.dumps({"status": "ANCHOR_CERTIFICATE_REGENERATED", "cases": len(cert["cases"]),
                      "certificate_sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}))


if __name__ == "__main__":
    main()

"""Produce the exact native-prefix equality reduction and 45 kernel images.

Production uses the published original-family Boolean-column profiler.
All gates are standard: (a,b), a<b, sends minimum to a.
"""

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / "semantic-pruning"
for filename, expected in (
        ("profile.py", "dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719"),
        ("anchors.py", "0b95573e7e3c446d0b7ca5352f6b5f4b8d92b91d6f3c72e7b4f783cd99d89902")):
    if hashlib.sha256((PARENT / filename).read_bytes()).hexdigest() != expected:
        raise ValueError("published production dependency changed: " + filename)
spec = importlib.util.spec_from_file_location("native_anchor_producer", PARENT / "anchors.py")
anchors = importlib.util.module_from_spec(spec)
spec.loader.exec_module(anchors)
semantic = anchors.semantic


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def compact(data):
    return {name: {"low_count": item["low_count"], "high_count": item["high_count"],
                   "envelope": item["envelope"], "summary": item["summary"],
                   "records_sha256": digest(item["records"])}
            for name, item in data.items()}


def snapshot(gates):
    data = semantic.analyze(13, gates)
    return {"families": compact(data), "anchors": anchors.both(13, data)}, data


def pairings(leaves):
    if not leaves:
        yield []
        return
    first = leaves[0]
    for j in range(1, len(leaves)):
        for remaining in pairings(leaves[1:j] + leaves[j + 1:]):
            yield [[first, leaves[j]]] + remaining


def kernels():
    for bottom in pairings(list(range(5, 11))):
        level = sorted([max(pair) for pair in bottom] + [11])
        for middle in pairings(level):
            yield bottom + middle + [sorted(max(pair) for pair in middle)]


def boolean_image(n, gates):
    columns = list(semantic.truth_columns(n))
    for a, b in gates:
        columns[a], columns[b] = columns[a] & columns[b], columns[a] | columns[b]
    return sorted({sum(((column >> x) & 1) << j for j, column in enumerate(columns))
                   for x in range(1 << n)})


def target(n, gates, start, stop):
    rows = sorted({(row >> start) & ((1 << (stop - start)) - 1)
                   for row in boolean_image(n, gates)})
    return {"n": stop - start, "original_wires": list(range(start, stop)),
            "size": len(rows), "image": rows, "image_sha256": digest(rows),
            "weight_counts": [sum(row.bit_count() == w for row in rows)
                              for w in range(stop - start + 1)]}


def build(fixture):
    gates = fixture["gates"]
    assert fixture["n"] == 13 and len(gates) == 46
    p = gates[:24]
    maximum = p + [[11, 12]]
    both = maximum + [[1, 2]]
    initial, _ = snapshot(p)
    at25, _ = snapshot(maximum)
    at26, _ = snapshot(both)
    cases = []
    for number, kernel in enumerate(kernels()):
        summary, data = snapshot(both + kernel)
        bound = max(item["lower_bound"] for item in summary["anchors"].values())
        witness = None
        if bound > 44:
            rows = data["two_maxima"]["records"]
            witness = next(row for row in rows if row[4] + row[5] >= 10)
        cases.append({"id": number, "kernel": kernel, "snapshot": summary,
                      "target": target(13, both + kernel, 2, 11),
                      "excluded_at_44": bound > 44,
                      "two_maximum_exclusion_record": witness})
    return {"schema": "native24-kernel-cover-certificate-v1", "agent": "six-sorting-2",
            "role": "researcher", "native_gate_list_sha256": digest(gates),
            "budget": 44, "prefix_length": 24, "prefix24": initial,
            "prefix25": at25, "prefix26": at26,
            "middle11": target(13, maximum, 1, 12),
            "middle10": target(13, both, 2, 12),
            "kernel_count": len(cases), "kernels": cases,
            "remaining_ids": [case["id"] for case in cases if not case["excluded_at_44"]]}


def main():
    fixture = json.loads((ROOT / "fixture.json").read_text())
    result = build(fixture)
    path = ROOT / "certificate.json"
    path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"agent": "six-sorting-2", "role": "researcher",
                      "kernel_count": result["kernel_count"],
                      "remaining": len(result["remaining_ids"]),
                      "certificate_bytes": path.stat().st_size,
                      "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest()},
                     sort_keys=True))


if __name__ == "__main__":
    main()

"""Produce four future-endpoint deletion certificates.

Uses pinned published Boolean-column production code. The independent
endpoint_verify.py imports no producer, profiler, sibling checker or solver.
No exhaustive suffix search is a premise.
"""

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEPENDENCIES = {
    "fixture.json": "93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6",
    "certificate.json": "21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06",
    "minimum-certificate.json": "147912afe63dc06c981e2a8e755ad279cb1907f913f6fa1489180ae96e6e39dd",
}
PRUNING_PRODUCER_SHA256 = "c4699f5c85be9906f410390538865f5ada0e93e0431c7fe2ac4e2876ee01589c"
# kernel: (initial low mask, initial high mask, stationary future endpoint)
WITNESSES = {11: (15, 1280, 3), 17: (15, 1088, 3),
             19: (1037, 258, 3), 26: (13, 1282, 10)}


def checked_bytes(name, expected):
    data = (ROOT / name).read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("published dependency changed: " + name)
    return data


checked_bytes("minimum_generate.py", PRUNING_PRODUCER_SHA256)
spec = importlib.util.spec_from_file_location("endpoint_pruning_producer", ROOT / "minimum_generate.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
s = m.semantic


def record_for(gates, low, high):
    """Keep this selected original clamping's complete Boolean domain."""
    free = [p for p in range(13) if not ((low | high) >> p) & 1]
    columns = iter(s.truth_columns(len(free)))
    values = [s.LOW if (low >> p) & 1 else s.HIGH if (high >> p) & 1
              else next(columns) for p in range(13)]
    d = r = redundant = 0
    for t, (a, b) in enumerate(gates):
        touch, identity = s.transition(values, a, b)
        d += touch
        r += identity
        if identity:
            redundant |= 1 << t
    return [low, high, *s.marked_ports(values), d, r, redundant]


def touch_witness(gates, endpoint):
    """First full Boolean input proving this endpoint needs a later touch."""
    columns = list(s.truth_columns(13))
    for a, b in gates:
        columns[a], columns[b] = columns[a] & columns[b], columns[a] | columns[b]
    local = endpoint - 3
    for x in range(8192):
        output = sum(((column >> x) & 1) << p for p, column in enumerate(columns))
        middle = (output >> 3) & 255
        correct = 1 if middle.bit_count() > 7 - local else 0
        actual = (middle >> local) & 1
        if actual != correct:
            return {"input_bits": x, "prefix_output_bits": output,
                    "middle_state": middle, "endpoint_value": actual,
                    "correct_endpoint_value": correct}
    raise ValueError("selected endpoint is already correct on the full image")


def build():
    sources = {name: json.loads(checked_bytes(name, pin)) for name, pin in DEPENDENCIES.items()}
    fixture, parent, previous = (sources[name] for name in DEPENDENCIES)
    if previous["remaining_eight_wire_ids"] != list(WITNESSES):
        raise ValueError("the preceding four-case frontier changed")
    targets = {item["kernel_id"]: item["target"] for item in previous["cases"]}
    cases = []
    for i, (low, high, endpoint) in WITNESSES.items():
        gates = (fixture["gates"][:24] + fixture["forced_gates"] +
                 parent["kernels"][i]["kernel"] + previous["forced_minimum_word"])
        record = record_for(gates, low, high)
        pruning = m.prune(gates, record)
        q = pruning["retained_prefix"]
        if len(gates) != 34 or record[4] + record[5] != 27 or len(q) != 7:
            raise ValueError("selected deletion budget changed")
        if not all(0 <= a < b < 7 for a, b in q):
            raise ValueError("selected seven-wire prefix is not standard")
        target = m.base.target(13, gates, 3, 11)
        if target != targets[i]:
            raise ValueError("the preceding eight-wire target changed")
        data = s.analyze(7, q)
        anchors = m.base.anchors.both(7, data)
        bound = max(item["lower_bound"] for item in anchors.values())
        if bound != 17:
            raise ValueError("inner anchor obstruction changed")
        cases.append({"kernel_id": i, "endpoint": endpoint,
                      "side": "minimum" if endpoint == 3 else "maximum",
                      "prefix_gates_sha256": m.base.digest(gates),
                      "target_size": target["size"], "target_sha256": target["image_sha256"],
                      "required_touch_witness": touch_witness(gates, endpoint),
                      "pruning": pruning, "inner_profiles": m.base.compact(data),
                      "inner_anchors": anchors, "inner_bound": bound,
                      "prefix_deletions": record[4] + record[5],
                      "forced_suffix_deletions": 1,
                      "total_lower_bound": record[4] + record[5] + 1 + bound})
    return {"schema": "native-endpoint-pruning-refinement-v1",
            "agent": "six-sorting-2", "role": "researcher",
            "parent_files_sha256": DEPENDENCIES,
            "excluded_kernel_ids": list(WITNESSES),
            "remaining_nine_wire_ids": previous["remaining_nine_wire_ids"],
            "remaining_eight_wire_ids": [], "cases": cases}


def main():
    result = build()
    path = ROOT / "endpoint-certificate.json"
    path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": "ENDPOINT_CERTIFICATE_REGENERATED",
                      "agent": "six-sorting-2", "role": "researcher",
                      "additional_exclusions": len(result["cases"]),
                      "remaining_targets": len(result["remaining_nine_wire_ids"]),
                      "bytes": path.stat().st_size,
                      "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()

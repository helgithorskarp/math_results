"""Produce paired original-clamping obstructions and single-root controls.

Packed Boolean columns produce the certificate. touch_verify.py independently
reconstructs it by literal scalar simulation and heap Huffman aggregation.
No solver, suffix enumeration, timeout or private experiment is a premise.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PINS = {
    "fixture.json": "93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6",
    "certificate.json": "21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06",
    "endpoint-certificate.json": "f08a97765b8f9e5cb3eef2d82ec454d59133ebe264d80c8e47222311e00cc9b9",
}
PRUNER_SHA256 = "c4699f5c85be9906f410390538865f5ada0e93e0431c7fe2ac4e2876ee01589c"
# Original low/high input masks. Every selected clamping keeps all256
# assignments of its eight unmarked original inputs before counting R.
STATIONARY = {
    0: (7, 320), 2: (13, 258), 3: (13, 258), 4: (41, 260), 5: (13, 258),
    6: (7, 1032), 7: (13, 258), 8: (13, 258), 9: (7, 320), 10: (7, 320),
    12: (7, 272), 15: (7, 1088), 16: (13, 258), 18: (7, 320), 20: (13, 258),
    21: (7, 1032), 24: (13, 130), 25: (41, 260), 27: (13, 258), 28: (13, 258),
    29: (13, 258), 30: (7, 1032), 31: (13, 258), 32: (7, 1032), 33: (13, 258),
    34: (13, 258), 36: (13, 258), 37: (13, 258), 38: (13, 258), 39: (13, 258),
    40: (41, 260), 41: (13, 258), 42: (13, 258),
}
MOVING = {3: (11, 260), 4: (11, 260), 5: (11, 320),
          12: (11, 260), 27: (11, 260), 28: (11, 260)}


def checked(name, pin):
    data = (ROOT / name).read_bytes()
    if hashlib.sha256(data).hexdigest() != pin:
        raise ValueError("published dependency changed: " + name)
    return data


checked("minimum_generate.py", PRUNER_SHA256)
spec = importlib.util.spec_from_file_location("touch_pruner", ROOT / "minimum_generate.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
s = m.semantic


def selected_record(gates, low, high):
    columns = iter(s.truth_columns(8))
    values = [s.LOW if low >> p & 1 else s.HIGH if high >> p & 1 else next(columns)
              for p in range(13)]
    d = r = mask = 0
    for t, (a, b) in enumerate(gates):
        hit, inactive = s.transition(values, a, b)
        d += hit
        r += inactive
        if inactive:
            mask |= 1 << t
    return [low, high, *s.marked_ports(values), d, r, mask]


def witness(gates, low, high):
    record = selected_record(gates, low, high)
    pruning = m.prune(gates, record)
    data = s.analyze(8, pruning["retained_prefix"])
    anchors = m.base.anchors.both(8, data)
    b = max(item["lower_bound"] for item in anchors.values())
    if record[4] + record[5] + b != 43:
        raise ValueError("selected clamping is not at the required tight budget")
    return {"pruning": pruning, "inner_profiles": m.base.compact(data),
            "inner_anchors": anchors, "inner_bound": b,
            "prefix_cost": record[4] + record[5], "cost_plus_bound": 43,
            "maximum_future_marked_touches_at_44": 1}


def boolean_witness(gates, x):
    cols = list(s.truth_columns(13))
    for a, b in gates:
        cols[a], cols[b] = cols[a] & cols[b], cols[a] | cols[b]
    out = sum(((col >> x) & 1) << p for p, col in enumerate(cols))
    return {"input_bits": x, "prefix_output_bits": out,
            "middle_state": (out >> 2) & 511,
            "correct_wire2": int(x.bit_count() > 10)}


def build():
    sources = {name: json.loads(checked(name, pin)) for name, pin in PINS.items()}
    fixture, parent, previous = (sources[name] for name in PINS)
    if previous["remaining_nine_wire_ids"] != list(STATIONARY):
        raise ValueError("preceding 33-case frontier changed")
    rows = []
    for i, (low, high) in STATIONARY.items():
        gates = fixture["gates"][:24] + fixture["forced_gates"] + parent["kernels"][i]["kernel"]
        target = m.base.target(13, gates, 2, 11)
        if target != parent["kernels"][i]["target"]:
            raise ValueError("parent nine-wire target changed")
        stationary = witness(gates, low, high)
        if stationary["pruning"]["outer_record"][2:4] != [7, 6144]:
            raise ValueError("stationary clamping does not mark the stated endpoints")
        if not all(x in target["image"] for x in (507, 509, 510)):
            raise ValueError("three single-zero controls missing from the exact target")
        row = {"kernel_id": i, "prefix_sha256": m.base.digest(gates),
               "target_size": target["size"], "target_sha256": target["image_sha256"],
               "stationary": stationary,
               "single_zero_states": [507, 509, 510],
               "forced_wire2_gate": [2, 3], "maximum_wire2_touches": 1}
        if i in MOVING:
            row["moving"] = witness(gates, *MOVING[i])
            if row["moving"]["pruning"]["outer_record"][2:4] != [11, 6144]:
                raise ValueError("moving clamping does not mark the stated ports")
            row["obstruction"] = boolean_witness(gates, 2559)
            if row["obstruction"]["prefix_output_bits"] != 8172:
                raise ValueError("literal pair obstruction changed")
        rows.append(row)
    return {"schema": "native-paired-touch-pruning-v1", "agent": "six-sorting-2",
            "role": "researcher", "parent_files_sha256": PINS,
            "excluded_kernel_ids": list(MOVING),
            "remaining_nine_wire_ids": [i for i in STATIONARY if i not in MOVING],
            "single_wire2_touch_kernel_ids": list(STATIONARY), "cases": rows}


def main():
    data = build()
    out = ROOT / "touch-certificate.json"
    out.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": "PAIRED_TOUCH_CERTIFICATE_REGENERATED",
                      "agent": "six-sorting-2", "role": "researcher",
                      "additional_exclusions": len(MOVING),
                      "remaining_targets": len(data["remaining_nine_wire_ids"]),
                      "single_touch_targets": len(STATIONARY), "bytes": out.stat().st_size,
                      "certificate_sha256": hashlib.sha256(out.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()

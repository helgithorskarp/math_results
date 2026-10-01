"""Produce the third-minimum refinement and two nested-pruning witnesses.

Uses the pinned Boolean-column producer; minimum_verify.py uses scalar
simulation instead. No solver or incomplete search is a premise.
"""

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_CERTIFICATE_SHA256 = "21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06"
BASE_GENERATOR_SHA256 = "08a37678a11392ed46907ab30b2463d841e3e068764c09e410244490f2212381"
IDS = (11, 14, 17, 19, 23, 26)
MINIMUM_WORD = [[3, 4], [2, 3]]


def checked_bytes(name, expected):
    data = (ROOT / name).read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("published dependency changed: " + name)
    return data


checked_bytes("generate.py", BASE_GENERATOR_SHA256)
spec = importlib.util.spec_from_file_location("native_base_producer", ROOT / "generate.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
semantic = base.semantic


def snapshot(gates):
    item = semantic.analyze_family(13, gates, 3, 1)
    return {"envelope": item["envelope"], "summary": item["summary"],
            "records_sha256": base.digest(item["records"])}, item


def prune(gates, record):
    """Remove marked touches and inactive free gates, tracking free carriers."""
    low, high = record[:2]
    free = [p for p in range(13) if not ((low | high) >> p) & 1]
    columns = semantic.truth_columns(len(free))
    values = [semantic.LOW if (low >> p) & 1 else
              semantic.HIGH if (high >> p) & 1 else columns[free.index(p)]
              for p in range(13)]
    carriers = [None if ((low | high) >> p) & 1 else free.index(p)
                for p in range(13)]
    retained, d, r, redundant_mask, touched_mask = [], 0, 0, 0, 0
    for t, (a, b) in enumerate(gates):
        if isinstance(values[a], str) or isinstance(values[b], str):
            d += 1
            touched_mask |= 1 << t
            order = lambda z: -1 if z == semantic.LOW else 1 if z == semantic.HIGH else 0
            if order(values[a]) > order(values[b]):
                values[a], values[b] = values[b], values[a]
                carriers[a], carriers[b] = carriers[b], carriers[a]
        else:
            if values[a] & ~values[b]:
                retained.append([carriers[a], carriers[b]])
            else:
                r += 1
                redundant_mask |= 1 << t
            values[a], values[b] = values[a] & values[b], values[a] | values[b]
    lp, hp = semantic.marked_ports(values)
    if [low, high, lp, hp, d, r, redundant_mask] != record:
        raise ValueError("pruning record does not match the complete conditional domain")
    output_free = [p for p in range(13) if carriers[p] is not None]
    rename = {carriers[p]: j for j, p in enumerate(output_free)}
    return {"outer_record": record, "marked_touch_mask": touched_mask,
            "input_free_wires": free, "output_free_wires": output_free,
            "input_to_output_wire": [rename[j] for j in range(len(free))],
            "retained_prefix": [[rename[a], rename[b]] for a, b in retained]}


def build():
    parent = json.loads(checked_bytes("certificate.json", BASE_CERTIFICATE_SHA256))
    fixture = json.loads((ROOT / "fixture.json").read_text())
    p26 = fixture["gates"][:24] + fixture["forced_gates"]
    cases, exclusions = [], []
    for i in IDS:
        p32 = p26 + parent["kernels"][i]["kernel"]
        snapshots = [snapshot(p32 + MINIMUM_WORD[:cut])[0] for cut in range(3)]
        p34 = p32 + MINIMUM_WORD
        cases.append({"kernel_id": i, "profiles32_33_34": snapshots,
                      "target": base.target(13, p34, 3, 11)})
        if i in (14, 23):
            input_low = 11 if i == 14 else 21
            _, outer = snapshot(p34)
            record = next(r for r in outer["records"] if r[:2] == [input_low, 256])
            witness = prune(p34, record)
            inner = semantic.analyze(9, witness["retained_prefix"])
            anchors = base.anchors.both(9, inner)
            witness.update({"kernel_id": i, "inner_profiles": base.compact(inner),
                            "inner_anchors": anchors,
                            "inner_bound": max(x["lower_bound"] for x in anchors.values()),
                            "total_bound": record[4] + record[5] +
                            max(x["lower_bound"] for x in anchors.values())})
            exclusions.append(witness)
    return {"schema": "native-third-minimum-refinement-v1", "agent": "six-sorting-2",
            "role": "researcher", "parent_certificate_sha256": BASE_CERTIFICATE_SHA256,
            "forced_minimum_word": MINIMUM_WORD, "cases": cases,
            "nested_exclusions": exclusions, "excluded_kernel_ids": [14, 23],
            "remaining_nine_wire_ids": [i for i in parent["remaining_ids"] if i not in IDS],
            "remaining_eight_wire_ids": [11, 17, 19, 26]}


def main():
    result = build()
    path = ROOT / "minimum-certificate.json"
    path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": "THIRD_MINIMUM_CERTIFICATE_REGENERATED",
                      "agent": "six-sorting-2", "role": "researcher",
                      "eight_wire_cases": len(result["cases"]),
                      "additional_exclusions": len(result["nested_exclusions"]),
                      "remaining_targets": len(result["remaining_nine_wire_ids"]) +
                      len(result["remaining_eight_wire_ids"]),
                      "bytes": path.stat().st_size,
                      "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest()},
                     sort_keys=True))


if __name__ == "__main__":
    main()

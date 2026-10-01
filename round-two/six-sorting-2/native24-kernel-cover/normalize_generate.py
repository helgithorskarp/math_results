"""Produce ten exact native-prefix normalization/correction obstructions.

Production uses pinned Boolean columns and dyadic anchor aggregation.
normalize_verify.py instead uses numeric ranks, scalar cubes and heap merges.
No solver, suffix enumeration or exploratory selected-pool census is a premise.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
PINS = {
    "fixture.json": "93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6",
    "certificate.json": "21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06",
    "touch-certificate.json": "04bcf3e1617c3ae2ce026149d1c76f620c8acf6e38bdc448719e26fa3ecd2455",
    "../../six-sorting-1/joint_extreme_kernel_barrier/frontier.json":
        "6041c9e1ed4bea12e3028836deb8b4e59de0e4d05205733393e4f4ca63c36667",
}
PRUNER_SHA256 = "c4699f5c85be9906f410390538865f5ada0e93e0431c7fe2ac4e2876ee01589c"
IDS = [6, 7, 10, 16, 18, 25, 29, 30, 37, 40]
WORD = [[3, 4], [2, 3]]
# kernel: original low mask, original high mask, required correction port.
CORRECTION = {6: (7, 328, 9), 7: (7, 1048, 10), 10: (7, 328, 10),
              16: (7, 1048, 10), 18: (7, 1064, 8), 25: (21, 104, 10),
              29: (11, 324, 10), 30: (7, 328, 9), 37: (7, 1064, 10),
              40: (21, 104, 10)}


def checked(name, pin):
    data = (ROOT / name).read_bytes()
    if hashlib.sha256(data).hexdigest() != pin:
        raise ValueError("published dependency changed: " + name)
    return data


checked("minimum_generate.py", PRUNER_SHA256)
spec = importlib.util.spec_from_file_location("normalize_pruner", ROOT / "minimum_generate.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
s = m.semantic


def record_for(gates, low, high):
    free = [q for q in range(13) if not (low | high) >> q & 1]
    columns = iter(s.truth_columns(len(free)))
    values = [s.LOW if low >> q & 1 else s.HIGH if high >> q & 1 else next(columns)
              for q in range(13)]
    d = r = mask = 0
    for t, (a, b) in enumerate(gates):
        hit, inactive = s.transition(values, a, b)
        d += hit
        r += inactive
        if inactive:
            mask |= 1 << t
    return [low, high, *s.marked_ports(values), d, r, mask]


def witness(gates, low, high, expected):
    record = record_for(gates, low, high)
    pruning = m.prune(gates, record)
    n = 13 - (low | high).bit_count()
    data = s.analyze(n, pruning["retained_prefix"])
    anchors = m.base.anchors.both(n, data)
    b = max(item["lower_bound"] for item in anchors.values())
    c = sum(record[4:6])
    if c + b != expected:
        raise ValueError("selected nested budget differs")
    return {"free_inputs": n, "pruning": pruning, "inner_profiles": m.base.compact(data),
            "inner_anchors": anchors, "inner_bound": b, "prefix_cost": c,
            "cost_plus_bound": c + b, "maximum_future_marked_touches_at_44": 44 - c - b}


def correction_witness(gates, port):
    columns = list(s.truth_columns(13))
    for a, b in gates:
        columns[a], columns[b] = columns[a] & columns[b], columns[a] | columns[b]
    for x in range(8192):
        expected = int(x.bit_count() > 12 - port)
        actual = columns[port] >> x & 1
        if actual != expected:
            out = sum(((col >> x) & 1) << q for q, col in enumerate(columns))
            return {"input_bits": x, "prefix_output_bits": out, "port": port,
                    "actual_value": actual, "correct_value": expected}
    raise ValueError("selected port needs no Boolean correction")


def build():
    sources = {name: json.loads(checked(name, pin)) for name, pin in PINS.items()}
    fixture, parent, previous, joined = (sources[name] for name in PINS)
    stationary = {row["kernel_id"]: row["stationary"] for row in previous["cases"]}
    frontier = joined["joint_remaining24_ids"]
    if len(frontier) != 24 or not set(IDS) <= set(frontier):
        raise ValueError("credited preceding frontier differs")
    cases = []
    for i in IDS:
        p32 = fixture["gates"][:24] + fixture["forced_gates"] + parent["kernels"][i]["kernel"]
        p34 = p32 + WORD
        lo, hi = stationary[i]["pruning"]["outer_record"][:2]
        a2 = witness(p32, lo, hi, 43)
        if {k: v for k, v in a2.items() if k != "free_inputs"} != stationary[i]:
            raise ValueError("preceding stationary certificate differs")
        a3 = witness(p32, 11, 320 if i == 10 else 260, 42)
        a4 = witness(p32, 5632, 3, 42)
        for item, ports in ((a2, [7, 6144]), (a3, [11, 6144]), (a4, [19, 6144])):
            if item["pruning"]["outer_record"][2:4] != ports:
                raise ValueError("normalization marker positions differ")
        low, high, port = CORRECTION[i]
        last = witness(p34, low, high, 44)
        if not (last["pruning"]["outer_record"][2] | last["pruning"]["outer_record"][3]) >> port & 1:
            raise ValueError("correction port does not carry a marker")
        target = m.base.target(13, p34, 3, 11)
        cases.append({"kernel_id": i, "prefix32_sha256": m.base.digest(p32),
                      "prefix34_sha256": m.base.digest(p34),
                      "target9_sha256": parent["kernels"][i]["target"]["image_sha256"],
                      "single_zero_states": [507, 509, 510],
                      "normalization_witnesses": {"low2": a2, "low3": a3, "low4": a4},
                      "normalized_target": target, "normalized_suffix_budget": 10,
                      "correction_pruning": last, "required_correction": correction_witness(p34, port),
                      "forced_suffix_marked_touches": 1, "total_lower_bound": 45})
    return {"schema": "native-third-minimum-correction-v1", "agent": "six-sorting-2",
            "role": "researcher", "parent_files_sha256": PINS,
            "credited_parent_graph": "bafkreib7kp2spfixj5s3ossbqyzn5y4pxuusek2laaqr47fm3bc4dyevwu",
            "previous_nine_wire_ids": frontier, "forced_minimum_word": WORD,
            "excluded_kernel_ids": IDS,
            "remaining_nine_wire_ids": [i for i in frontier if i not in IDS], "cases": cases}


def main():
    start = time.monotonic()
    data = build()
    out = ROOT / "normalize-certificate.json"
    out.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": "NORMALIZED_CORRECTION_CERTIFICATE_REGENERATED",
                      "agent": "six-sorting-2", "role": "researcher",
                      "additional_exclusions": len(IDS), "remaining_targets": len(data["remaining_nine_wire_ids"]),
                      "bytes": out.stat().st_size,
                      "certificate_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                      "seconds": time.monotonic() - start,
                      "maximum_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == "__main__":
    main()

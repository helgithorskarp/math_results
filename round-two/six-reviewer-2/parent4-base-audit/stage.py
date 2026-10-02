"""Raw-pair exhaustive capacity screens, with a stronger optional threshold."""
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import struct
from grid import C15, C18, ORDER, coordinates, marginal_row, need


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def run(stage, threshold, previous=None, record_path=None):
    _, points, labels, masks = coordinates()
    full = (1 << len(points)) - 1
    need(len(points) == 1118 and len(labels) == 36, "literal scope sizes")
    need(1 <= stage <= 4 and threshold in (1117, 1118), "bounded requested screen")
    if stage == 1:
        inputs = [(list(p), True) for p in product(range(15), range(18))]
    else:
        need(previous is not None and previous["stage"] == stage - 1,
             "immediately preceding complete frontier")
        need(previous["threshold"] == threshold and previous["complete"],
             "same threshold, completed enumeration")
        parents = previous["retained"]
        need(parents == sorted(parents) and len(parents) == len({tuple(p) for p, _ in parents}),
             "ordered distinct complete parents")
        inputs = [(p + [a], flag) for p, flag in parents
                  for a in range(ORDER[stage])]
    need(len(inputs) <= 40000, "fixed 40000 input resource guard, no exclusion on failure")
    retained = []
    digest = hashlib.sha256()
    canonical_digest = hashlib.sha256()
    canonical_records = bytearray()
    canonical_frontier = []
    canonical_count = 0
    histogram = {}
    canonical_histogram = {}
    marginal_entries = 0
    phase_intersections = 0
    witnesses = {}
    for phases, original_parent in inputs:
        gain, caps, bound = marginal_row(phases, labels, masks, full)
        raw = struct.pack("<38H", *phases, gain, *caps, bound)
        digest.update(raw)
        marginal_entries += len(caps)
        phase_intersections += sum(n for n in labels if n not in ORDER[:len(phases)])
        histogram[bound] = histogram.get(bound, 0) + 1
        if bound not in witnesses:
            witnesses[bound] = {"phases": phases, "gain": gain, "remaining_sum": sum(caps)}
        original = original_parent and bound >= 1118
        if bound >= threshold:
            retained.append([phases, original])
        if original_parent and phases[0] in C15 and phases[1] in C18:
            canonical_count += 1
            canonical_digest.update(raw)
            canonical_records.extend(raw)
            canonical_histogram[bound] = canonical_histogram.get(bound, 0) + 1
            if original:
                canonical_frontier.append(phases)
    if record_path:
        Path(record_path).write_bytes(canonical_records)
    return {"stage": stage, "threshold": threshold, "complete": True,
            "point_count": len(points), "original_labels": list(labels),
            "ordered_physical_points_sha256": hashlib.sha256(struct.pack("<1118H", *sorted(points))).hexdigest(),
            "raw_input_count": len(inputs), "raw_retained_count": len(retained),
            "raw_original_retained_count": sum(flag for _, flag in retained),
            "raw_row_sha256": digest.hexdigest(), "retained": retained,
            "bound_histogram": sorted(histogram.items()),
            "min_bound": min(histogram), "max_bound": max(histogram),
            "max_witness": witnesses[max(histogram)],
            "marginal_entries": marginal_entries, "phase_intersections": phase_intersections,
            "canonical_original": {"count": canonical_count,
                "retained": canonical_frontier, "row_sha256": canonical_digest.hexdigest(),
                "bound_histogram": sorted(canonical_histogram.items())}}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--stage", type=int, required=True)
    p.add_argument("--threshold", type=int, default=1117)
    p.add_argument("--previous")
    p.add_argument("--out", required=True)
    p.add_argument("--records")
    a = p.parse_args()
    before = json.loads(Path(a.previous).read_text()) if a.previous else None
    result = run(a.stage, a.threshold, before, a.records)
    Path(a.out).write_bytes(canonical(result) + b"\n")
    print(json.dumps({k: result[k] for k in ("stage", "threshold", "raw_input_count",
        "raw_retained_count", "raw_original_retained_count", "min_bound", "max_bound",
        "max_witness", "marginal_entries", "phase_intersections")}))

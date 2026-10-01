"""Independent literal scalar audit of four endpoint-deletion exclusions.

Standard library only; imports no producer, profiler, sibling checker or
solver. Distinct numeric extreme ranks and every original free assignment
are used before each family's semantic envelope is formed.
"""

from copy import deepcopy
import hashlib
import heapq
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
PINS = {
    "fixture.json": "93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6",
    "certificate.json": "21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06",
    "minimum-certificate.json": "147912afe63dc06c981e2a8e755ad279cb1907f913f6fa1489180ae96e6e39dd",
}
# These are the original input locations, not current marker-port classes.
SELECTED = {11: ([0, 1, 2, 3], [8, 10], 3),
            17: ([0, 1, 2, 3], [6, 10], 3),
            19: ([0, 2, 3, 10], [1, 8], 3),
            26: ([0, 2, 3], [1, 8, 10], 10)}
FAMILIES = (("one_minimum", 1, 0), ("one_maximum", 0, 1),
            ("two_minima", 2, 0), ("two_maxima", 0, 2), ("mixed_pair", 1, 1))
SMALL_LOWER_BOUNDS = {5: 9, 6: 12}
METRICS = {"outer_free_assignments": 0, "outer_gate_evaluations": 0,
           "inner_free_assignments": 0, "inner_gate_evaluations": 0,
           "pruning_function_assignments": 0, "full_boolean_inputs": 0,
           "stationary_endpoint_pair_controls": 0, "positive_seven_inputs": 0}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(",", ":")).encode()).hexdigest()


def require_pin(data, expected, name):
    need(hashlib.sha256(data).hexdigest() == expected, "dependency changed: " + name)


def marked(x):
    return x < 0 or x > 1


def marker_ports(row):
    return (sum(2 ** p for p, value in enumerate(row) if value < 0),
            sum(2 ** p for p, value in enumerate(row) if value > 1))


def simulate(values, gates):
    row = list(values)
    for a, b in gates:
        if row[a] > row[b]:
            row[a], row[b] = row[b], row[a]
    return row


def make_template(n, lows, highs):
    need(len(set(lows + highs)) == len(lows) + len(highs), "overlapping or repeated markers")
    need(all(0 <= p < n for p in lows + highs), "invalid marker location")
    template = [0] * n
    for rank, p in enumerate(lows):
        template[p] = rank - len(lows)
    for rank, p in enumerate(highs):
        template[p] = 2 + rank
    free = [p for p in range(n) if p not in lows and p not in highs]
    return template, free


def scalar_family(n, gates, lows, highs, level):
    """Activity is accumulated over this one original family's full cube."""
    template, free = make_template(n, lows, highs)
    touched = final_ports = None
    active = 0
    for assignment in range(2 ** len(free)):
        row = list(template)
        for j, p in enumerate(free):
            row[p] = (assignment >> j) & 1
        this_touch = 0
        for t, (a, b) in enumerate(gates):
            hit = marked(row[a]) or marked(row[b])
            if hit:
                this_touch |= 2 ** t
            if row[a] > row[b]:
                if not hit:
                    active |= 2 ** t
                row[a], row[b] = row[b], row[a]
        ports = marker_ports(row)
        if touched is None:
            touched, final_ports = this_touch, ports
        need(this_touch == touched and ports == final_ports,
             "marker trajectory depends on free values")
        METRICS[level + "_free_assignments"] += 1
        METRICS[level + "_gate_evaluations"] += len(gates)
    redundant = (2 ** len(gates) - 1) & ~(touched | active)
    return [sum(2 ** p for p in lows), sum(2 ** p for p in highs),
            *final_ports, touched.bit_count(), redundant.bit_count(), redundant]


def scalar_pruning(gates, record):
    lows = [p for p in range(13) if (record[0] >> p) & 1]
    highs = [p for p in range(13) if (record[1] >> p) & 1]
    reference, free = make_template(13, lows, highs)
    carriers = [free.index(p) if p in free else None for p in range(13)]
    retained, touched = [], 0
    for t, (a, b) in enumerate(gates):
        if marked(reference[a]) or marked(reference[b]):
            touched |= 2 ** t
            need(not ((record[6] >> t) & 1), "marked gate is also called redundant")
            if reference[a] > reference[b]:
                reference[a], reference[b] = reference[b], reference[a]
                carriers[a], carriers[b] = carriers[b], carriers[a]
        elif not ((record[6] >> t) & 1):
            retained.append([carriers[a], carriers[b]])
    output_free = [p for p in range(13) if not marked(reference[p])]
    rename = {carriers[p]: j for j, p in enumerate(output_free)}
    need(sorted(rename) == list(range(7)), "free carrier names are not bijective")
    need(touched.bit_count() == record[4], "wrong marked deletion count")
    need(record[6].bit_count() == record[5], "wrong redundant deletion count")
    result = {"outer_record": record, "marked_touch_mask": touched,
              "input_free_wires": free, "output_free_wires": output_free,
              "input_to_output_wire": [rename[j] for j in range(len(free))],
              "retained_prefix": [[rename[a], rename[b]] for a, b in retained]}
    need(len(result["retained_prefix"]) == 7, "retained prefix has the wrong size")
    need(all(0 <= a < b < 7 for a, b in result["retained_prefix"]),
         "selected retained prefix is not standard")
    for assignment in range(128):
        original, pruned = list(make_template(13, lows, highs)[0]), [0] * 7
        for j, p in enumerate(free):
            original[p] = pruned[rename[j]] = (assignment >> j) & 1
        full_output = simulate(original, gates)
        need([full_output[p] for p in output_free] == simulate(pruned, result["retained_prefix"]),
             "pruned function differs from the original conditional function")
        METRICS["pruning_function_assignments"] += 1
    return result, reference


def summarize_family(records, lo, hi):
    records.sort()
    classes = {}
    for record in records:
        key = tuple(record[2:4])
        d, c = classes.get(key, (0, 0))
        classes[key] = max(d, record[4]), max(c, record[4] + record[5])
    envelope = [[lp, hp, d, c] for (lp, hp), (d, c) in sorted(classes.items())]
    return {"low_count": lo, "high_count": hi, "envelope": envelope,
            "records_sha256": digest(records),
            "summary": {"ordinary_mass": sum(2 ** row[2] for row in envelope),
                        "semantic_mass": sum(2 ** row[3] for row in envelope),
                        "maximum_deletions": max(r[4] for r in records),
                        "maximum_semantic_deletions": max(r[4] + r[5] for r in records),
                        "maximum_redundancies": max(r[5] for r in records),
                        "port_classes": len(envelope)}}


def inner_profiles(gates):
    answer = {}
    for name, lo, hi in FAMILIES:
        records = []
        for lows in combinations(range(7), lo):
            for highs in combinations([p for p in range(7) if p not in lows], hi):
                records.append(scalar_family(7, gates, list(lows), list(highs), "inner"))
        answer[name] = summarize_family(records, lo, hi)
    return answer


def ceiling_log(x):
    need(x > 0, "nonpositive mass")
    exponent = 0
    while 2 ** exponent < x:
        exponent += 1
    return exponent


def huffman_bound(labels):
    """Combine the two smallest route budgets by 1+max, independently."""
    heap = list(labels)
    need(bool(heap), "empty route budget")
    heapq.heapify(heap)
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, max(a, b) + 1)
    return heap[0]


def anchor_bounds(profiles):
    answer = {}
    for side, count, column, unary in (("low", "low_count", 0, "one_minimum"),
                                       ("high", "high_count", 1, "one_maximum")):
        selected = {name: item for name, item in profiles.items() if item[count]}
        ports = sorted(row[column].bit_length() - 1 for row in profiles[unary]["envelope"])
        rows = []
        for p in ports:
            masses = {name: sum(2 ** row[3] for row in item["envelope"] if (row[column] >> p) & 1)
                      for name, item in selected.items()}
            label = max(SMALL_LOWER_BOUNDS[7 - item["low_count"] - item["high_count"]] +
                        ceiling_log(masses[name]) for name, item in selected.items() if masses[name])
            rows.append({"port": p, "anchored_masses": masses,
                         "label": label, "units": 2 ** (label - 9)})
        mass = sum(row["units"] for row in rows)
        bound = huffman_bound(row["label"] for row in rows)
        need(bound == 9 + ceiling_log(mass), "Huffman and dyadic bounds disagree")
        answer[side] = {"base": 9, "normalized_mass": mass, "lower_bound": bound, "rows": rows}
    return answer


def image_and_witness(gates, endpoint):
    image, witness = set(), None
    for x in range(8192):
        row = simulate([(x >> p) & 1 for p in range(13)], gates)
        sorted_row = sorted(row)
        need(row[:3] == sorted_row[:3] and row[11:] == sorted_row[11:], "outer ranks are not fixed")
        middle = sum(row[p] * 2 ** (p - 3) for p in range(3, 11))
        image.add(middle)
        if witness is None and row[endpoint] != sorted_row[endpoint]:
            witness = {"input_bits": x, "prefix_output_bits": sum(row[p] * 2 ** p for p in range(13)),
                       "middle_state": middle, "endpoint_value": row[endpoint],
                       "correct_endpoint_value": sorted_row[endpoint]}
        METRICS["full_boolean_inputs"] += 1
    need(witness is not None, "no input requires the selected endpoint to change")
    rows = sorted(image)
    return {"n": 8, "original_wires": list(range(3, 11)), "size": len(rows),
            "image": rows, "image_sha256": digest(rows),
            "weight_counts": [sum(x.bit_count() == weight for x in rows) for weight in range(9)]}, witness


def stationary_endpoint_controls(reference, pruning, endpoint):
    """Every seven-bit free state and every allowed suffix pair, locally."""
    free = pruning["output_free_wires"]
    need(endpoint not in free, "endpoint is not marked")
    need(set(free) | {endpoint} == set(range(3, 11)), "wrong allowed suffix partition")
    need((endpoint == 3 and reference[endpoint] < 0) or
         (endpoint == 10 and reference[endpoint] > 1), "wrong stationary extreme")
    rename = {p: j for j, p in enumerate(free)}
    for assignment in range(128):
        row, small = list(reference), [(assignment >> j) & 1 for j in range(7)]
        for j, p in enumerate(free):
            row[p] = small[j]
        for a, b in combinations(range(3, 11), 2):
            after = simulate(row, [(a, b)])
            need(marker_ports(after) == marker_ports(row), "a suffix gate moves a marker")
            expected = small if endpoint in (a, b) else simulate(small, [(rename[a], rename[b])])
            need([after[p] for p in free] == expected, "stationary deletion or free-pair transfer fails")
            METRICS["stationary_endpoint_pair_controls"] += 1


def reconstruct(sources):
    fixture, parent, previous = (sources[name] for name in PINS)
    need(fixture["n"] == 13 and len(fixture["gates"]) == 46, "wrong native fixture")
    need(fixture["forced_gates"] == [[11, 12], [1, 2]], "wrong parent forced word")
    need(previous["forced_minimum_word"] == [[3, 4], [2, 3]], "wrong minimum word")
    need(previous["remaining_eight_wire_ids"] == list(SELECTED), "wrong preceding frontier")
    remaining = [i for i in parent["remaining_ids"] if i not in (11, 14, 17, 19, 23, 26)]
    need(remaining == previous["remaining_nine_wire_ids"] and len(remaining) == 33,
         "remaining nine-wire target list differs")
    targets = {item["kernel_id"]: item["target"] for item in previous["cases"]}
    cases = []
    for i, (lows, highs, endpoint) in SELECTED.items():
        gates = (fixture["gates"][:24] + fixture["forced_gates"] +
                 parent["kernels"][i]["kernel"] + previous["forced_minimum_word"])
        need(len(gates) == 34 and all(0 <= a < b < 13 for a, b in gates), "invalid literal prefix")
        target, witness = image_and_witness(gates, endpoint)
        need(target == targets[i], "full Boolean image differs from the published eight-wire target")
        record = scalar_family(13, gates, lows, highs, "outer")
        need(record[4] + record[5] == 27, "prefix does not delete 27 gates")
        need(record[2:4] == ([15, 6144] if endpoint == 3 else [7, 7168]), "wrong outer marker ports")
        pruning, reference = scalar_pruning(gates, record)
        stationary_endpoint_controls(reference, pruning, endpoint)
        profiles = inner_profiles(pruning["retained_prefix"])
        anchors = anchor_bounds(profiles)
        bound = max(item["lower_bound"] for item in anchors.values())
        need(bound == 17, "seven-wire extension lower bound is not 17")
        cases.append({"kernel_id": i, "endpoint": endpoint,
                      "side": "minimum" if endpoint == 3 else "maximum",
                      "prefix_gates_sha256": digest(gates),
                      "target_size": target["size"], "target_sha256": target["image_sha256"],
                      "required_touch_witness": witness, "pruning": pruning,
                      "inner_profiles": profiles, "inner_anchors": anchors,
                      "inner_bound": bound, "prefix_deletions": record[4] + record[5],
                      "forced_suffix_deletions": 1, "total_lower_bound": record[4] + record[5] + 1 + bound})
    return {"schema": "native-endpoint-pruning-refinement-v1", "agent": "six-sorting-2",
            "role": "researcher", "parent_files_sha256": PINS,
            "excluded_kernel_ids": list(SELECTED), "remaining_nine_wire_ids": remaining,
            "remaining_eight_wire_ids": [], "cases": cases}


def match_certificate(candidate, reconstructed):
    need(candidate == reconstructed, "complete reconstructed certificate differs")


def main():
    start = time.monotonic()
    sources = {}
    for name, pin in PINS.items():
        data = (ROOT / name).read_bytes()
        require_pin(data, pin, name)
        sources[name] = json.loads(data)
    reconstructed = reconstruct(sources)
    certificate_bytes = (ROOT / "endpoint-certificate.json").read_bytes()
    certificate = json.loads(certificate_bytes)
    match_certificate(certificate, reconstructed)

    # Definition-level positive controls, including the imported small sizes.
    sorter7 = [(0, 6), (2, 3), (4, 5), (0, 2), (1, 4), (3, 6), (0, 1), (2, 5),
               (3, 4), (1, 2), (4, 6), (2, 3), (4, 5), (1, 2), (3, 4), (5, 6)]
    for x in range(128):
        row = [(x >> p) & 1 for p in range(7)]
        need(simulate(row, sorter7) == sorted(row), "known seven-wire sorter fails")
        METRICS["positive_seven_inputs"] += 1
    control_bound = max(x["lower_bound"] for x in anchor_bounds(inner_profiles(sorter7)).values())
    need(control_bound == 16, "anchor bound rejects a known sixteen-gate sorter")
    for x in range(8192):
        row = [(x >> p) & 1 for p in range(13)]
        need(simulate(row, sources["fixture.json"]["gates"]) == sorted(row), "known native sorter fails")
        METRICS["full_boolean_inputs"] += 1

    damaged = [deepcopy(certificate) for _ in range(5)]
    damaged[0]["cases"][0]["pruning"]["outer_record"][4] -= 1
    damaged[1]["cases"][1]["pruning"]["retained_prefix"][0].reverse()
    damaged[2]["cases"][2]["inner_anchors"]["high"]["rows"][0]["label"] -= 1
    damaged[3]["cases"][3]["required_touch_witness"]["input_bits"] += 1
    damaged[4]["remaining_nine_wire_ids"].pop()
    for altered in damaged:
        try:
            match_certificate(altered, reconstructed)
        except ValueError:
            pass
        else:
            raise ValueError("damaged certificate accepted")
    try:
        require_pin((ROOT / "fixture.json").read_bytes() + b" ", PINS["fixture.json"], "damaged fixture")
    except ValueError:
        pass
    else:
        raise ValueError("damaged dependency accepted")

    print(json.dumps({"status": "ALL_ENDPOINT_REFINEMENT_CHECKS_PASSED",
                      "agent": "six-sorting-2", "role": "researcher",
                      "additional_exclusions": 4, "remaining_targets": 33,
                      "target_sizes": [case["target_size"] for case in reconstructed["cases"]],
                      "inner_bounds": [case["inner_bound"] for case in reconstructed["cases"]],
                      "total_lower_bounds": [case["total_lower_bound"] for case in reconstructed["cases"]],
                      "seven_wire_positive_anchor_bound": control_bound,
                      "corruptions_rejected": len(damaged) + 1,
                      "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
                      "seconds": round(time.monotonic() - start, 3),
                      "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      **METRICS}, sort_keys=True))


if __name__ == "__main__":
    main()

"""Standalone scalar checker for paired-clamping touch restrictions.

Imports no sibling code, producer, profiler, solver or external dependency.
Distinct numeric marker ranks and every original free Boolean assignment
determine the deleted gates. Heap Huffman merges independently check the
producer's dyadic anchor formula. The universal routing proof is in TOUCH.md.
"""
from copy import deepcopy
import hashlib
import heapq
from itertools import combinations, permutations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
PINS = {
    "fixture.json": "93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6",
    "certificate.json": "21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06",
    "endpoint-certificate.json": "f08a97765b8f9e5cb3eef2d82ec454d59133ebe264d80c8e47222311e00cc9b9",
}
EXCLUDED = [3, 4, 5, 12, 27, 28]
FAMILIES = (("one_minimum", 1, 0), ("one_maximum", 0, 1),
            ("two_minima", 2, 0), ("two_maxima", 0, 2), ("mixed_pair", 1, 1))
SIZES = (0, 0, 1, 3, 5, 9, 12, 16, 19)
METRICS = {}


def need(test, message):
    if not test:
        raise ValueError(message)


def count(name, amount=1):
    METRICS[name] = METRICS.get(name, 0) + amount


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(",", ":")).encode()).hexdigest()


def marked(value):
    return value < 0 or value > 1


def ports(row):
    return [sum(2 ** i for i, v in enumerate(row) if v < 0),
            sum(2 ** i for i, v in enumerate(row) if v > 1)]


def simulate(row, gates):
    values = list(row)
    for a, b in gates:
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values


def template(n, low, high):
    need(low >= 0 and high >= 0 and not low & high and (low | high) < 2 ** n,
         "invalid original marker masks")
    lows = [i for i in range(n) if low >> i & 1]
    highs = [i for i in range(n) if high >> i & 1]
    free = [i for i in range(n) if not (low | high) >> i & 1]
    row = [0] * n
    for rank, i in enumerate(lows):
        row[i] = rank - len(lows)
    for rank, i in enumerate(highs):
        row[i] = rank + 2
    return row, free


def family(n, gates, low, high, level):
    initial, free = template(n, low, high)
    touches = final = None
    active = 0
    for x in range(2 ** len(free)):
        row = list(initial)
        for j, i in enumerate(free):
            row[i] = x >> j & 1
        hit_mask = 0
        for t, (a, b) in enumerate(gates):
            hit = marked(row[a]) or marked(row[b])
            if hit:
                hit_mask |= 2 ** t
            if row[a] > row[b]:
                if not hit:
                    active |= 2 ** t
                row[a], row[b] = row[b], row[a]
        if touches is None:
            touches, final = hit_mask, ports(row)
        need(touches == hit_mask and final == ports(row), "free-dependent marker route")
        count(level + "_free_assignments")
        count(level + "_gate_evaluations", len(gates))
    redundant = (2 ** len(gates) - 1) & ~(touches | active)
    return [low, high, *final, touches.bit_count(), redundant.bit_count(), redundant]


def pruning(n, gates, record):
    low, high = record[:2]
    reference, free = template(n, low, high)
    carrier = [free.index(i) if i in free else None for i in range(n)]
    word, touches = [], 0
    for t, (a, b) in enumerate(gates):
        if marked(reference[a]) or marked(reference[b]):
            touches |= 2 ** t
            need(not record[6] >> t & 1, "marked gate also deleted as free identity")
            if reference[a] > reference[b]:
                reference[a], reference[b] = reference[b], reference[a]
                carrier[a], carrier[b] = carrier[b], carrier[a]
        elif not record[6] >> t & 1:
            word.append([carrier[a], carrier[b]])
    output_free = [i for i in range(n) if not marked(reference[i])]
    rename = {carrier[i]: j for j, i in enumerate(output_free)}
    need(sorted(rename) == list(range(len(free))), "nonbijective free-carrier routing")
    result = {"outer_record": record, "marked_touch_mask": touches,
              "input_free_wires": free, "output_free_wires": output_free,
              "input_to_output_wire": [rename[i] for i in range(len(free))],
              "retained_prefix": [[rename[a], rename[b]] for a, b in word]}
    need(touches.bit_count() == record[4] and record[6].bit_count() == record[5],
         "deletion count differs")
    need(len(word) + record[4] + record[5] == len(gates), "gates not partitioned")
    for x in range(2 ** len(free)):
        full = list(template(n, low, high)[0])
        small = [0] * len(free)
        for j, i in enumerate(free):
            full[i] = small[rename[j]] = x >> j & 1
        actual = simulate(full, gates)
        need([actual[i] for i in output_free] == simulate(small, result["retained_prefix"]),
             "conditional pruning function differs")
        count("pruning_function_assignments")
    return result


def summary(records, l, h):
    records.sort()
    classes = {}
    for row in records:
        key = tuple(row[2:4])
        d, c = classes.get(key, (0, 0))
        classes[key] = max(d, row[4]), max(c, row[4] + row[5])
    envelope = [[lo, hi, d, c] for (lo, hi), (d, c) in sorted(classes.items())]
    return {"low_count": l, "high_count": h, "envelope": envelope,
            "records_sha256": digest(records),
            "summary": {"ordinary_mass": sum(2 ** row[2] for row in envelope),
                        "semantic_mass": sum(2 ** row[3] for row in envelope),
                        "maximum_deletions": max(row[4] for row in records),
                        "maximum_semantic_deletions": max(row[4] + row[5] for row in records),
                        "maximum_redundancies": max(row[5] for row in records),
                        "port_classes": len(envelope)}}


def profiles(n, gates, level="inner"):
    result = {}
    for name, l, h in FAMILIES:
        if l + h > n:
            continue
        records = []
        for lows in combinations(range(n), l):
            other = [i for i in range(n) if i not in lows]
            for highs in combinations(other, h):
                low, high = sum(2 ** i for i in lows), sum(2 ** i for i in highs)
                records.append(family(n, gates, low, high, level))
        result[name] = summary(records, l, h)
    return result


def ceil_log(mass):
    need(mass > 0, "empty dyadic mass")
    e = 0
    while 2 ** e < mass:
        e += 1
    return e


def huffman(labels):
    heap = list(labels)
    need(bool(heap), "empty route set")
    heapq.heapify(heap)
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, 1 + max(a, b))
    return heap[0]


def anchor_bounds(n, data):
    result = {}
    for side, column, count_name, unary in (("low", 0, "low_count", "one_minimum"),
                                          ("high", 1, "high_count", "one_maximum")):
        chosen = {name: item for name, item in data.items() if item[count_name]}
        sizes = {name: SIZES[n - item["low_count"] - item["high_count"]]
                 for name, item in chosen.items()}
        base = min(sizes.values())
        reachable = sorted(row[column].bit_length() - 1 for row in data[unary]["envelope"])
        rows = []
        for p in reachable:
            masses = {name: sum(2 ** row[3] for row in item["envelope"] if row[column] >> p & 1)
                      for name, item in chosen.items()}
            label = max(sizes[name] + ceil_log(mass) for name, mass in masses.items() if mass)
            rows.append({"port": p, "anchored_masses": masses, "label": label,
                         "units": 2 ** (label - base)})
        units = sum(row["units"] for row in rows)
        b = huffman(row["label"] for row in rows)
        need(b == base + ceil_log(units), "Huffman and dyadic formulas differ")
        result[side] = {"base": base, "normalized_mass": units, "lower_bound": b, "rows": rows}
    return result


def bound(n, gates, level="control"):
    if n < 2:
        return 0
    return max(x["lower_bound"] for x in anchor_bounds(n, profiles(n, gates, level)).values())


def audit_witness(gates, candidate, expected_ports):
    record = candidate["pruning"]["outer_record"]
    need(record[0].bit_count() == 3 and record[1].bit_count() == 2, "wrong five-mark family")
    row = family(13, gates, record[0], record[1], "outer")
    need(row[2:4] == expected_ports, "wrong current marker configuration")
    retained = pruning(13, gates, row)
    data = profiles(8, retained["retained_prefix"])
    anchors = anchor_bounds(8, data)
    b = max(x["lower_bound"] for x in anchors.values())
    need(row[4] + row[5] + b == 43, "clamping is not at budget43")
    actual = {"pruning": retained, "inner_profiles": data, "inner_anchors": anchors,
              "inner_bound": b, "prefix_cost": row[4] + row[5], "cost_plus_bound": 43,
              "maximum_future_marked_touches_at_44": 1}
    need(candidate == actual, "full clamping certificate differs")
    return actual


def audit_certificate(candidate, sources):
    fixture, parent, previous = (sources[name] for name in PINS)
    original = previous["remaining_nine_wire_ids"]
    need(set(candidate) == {"schema", "agent", "role", "parent_files_sha256", "excluded_kernel_ids",
                            "remaining_nine_wire_ids", "single_wire2_touch_kernel_ids", "cases"},
         "unexpected or missing certificate fields")
    need(candidate["schema"] == "native-paired-touch-pruning-v1", "wrong schema")
    need(candidate["agent"] == "six-sorting-2" and candidate["role"] == "researcher", "wrong attribution")
    need(candidate["parent_files_sha256"] == PINS, "dependency manifest differs")
    need(candidate["excluded_kernel_ids"] == EXCLUDED, "wrong exclusion list")
    need(candidate["remaining_nine_wire_ids"] == [i for i in original if i not in EXCLUDED],
         "remaining frontier differs")
    need(candidate["single_wire2_touch_kernel_ids"] == original and len(original) == 33,
         "single-touch coverage differs")
    need([row["kernel_id"] for row in candidate["cases"]] == original, "missing/reordered case")
    need(fixture["n"] == 13 and len(fixture["gates"]) == 46 and
         fixture["forced_gates"] == [[11, 12], [1, 2]], "wrong original fixture")
    for item in candidate["cases"]:
        i = item["kernel_id"]
        expected_keys = {"kernel_id", "prefix_sha256", "target_size", "target_sha256", "stationary",
                         "single_zero_states", "forced_wire2_gate", "maximum_wire2_touches"}
        if i in EXCLUDED:
            expected_keys |= {"moving", "obstruction"}
        need(set(item) == expected_keys, "unexpected or missing case fields")
        gates = fixture["gates"][:24] + fixture["forced_gates"] + parent["kernels"][i]["kernel"]
        need(len(gates) == 32 and all(0 <= a < b < 13 for a, b in gates), "wrong literal prefix")
        image = set()
        for x in range(8192):
            row = simulate([x >> p & 1 for p in range(13)], gates)
            expected = sorted(row)
            need(row[:2] == expected[:2] and row[11:] == expected[11:], "outer ranks not fixed")
            image.add(sum(row[p] * 2 ** (p - 2) for p in range(2, 11)))
            count("full_boolean_inputs")
        image = sorted(image)
        target = parent["kernels"][i]["target"]
        need(image == target["image"] and digest(image) == target["image_sha256"], "parent image differs")
        need(item["prefix_sha256"] == digest(gates) and item["target_size"] == len(image) and
             item["target_sha256"] == digest(image), "prefix/target metadata differs")
        need(item["single_zero_states"] == [507, 509, 510] and all(x in image for x in (507, 509, 510)),
             "single-zero controls differ")
        need(item["forced_wire2_gate"] == [2, 3] and item["maximum_wire2_touches"] == 1,
             "wrong root restriction")
        audit_witness(gates, item["stationary"], [7, 6144])
        if i in EXCLUDED:
            audit_witness(gates, item["moving"], [11, 6144])
            out = simulate([2559 >> p & 1 for p in range(13)], gates)
            witness = {"input_bits": 2559, "prefix_output_bits": sum(out[p] * 2 ** p for p in range(13)),
                       "middle_state": sum(out[p] * 2 ** (p - 2) for p in range(2, 11)),
                       "correct_wire2": sorted(out)[2]}
            need(item["obstruction"] == witness and witness["prefix_output_bits"] == 8172 and
                 out[2] == out[3] == 1 and witness["correct_wire2"] == 0, "pair obstruction differs")
        else:
            need("moving" not in item and "obstruction" not in item, "unsupported extra exclusion")


def tiny_routing_controls():
    """Full small sorters, changing carriers, and all local first-touch rows."""
    sorter = [[0, 1], [2, 3], [0, 2], [1, 3], [1, 2]]
    oriented = [(a, b) for a in range(4) for b in range(4) if a != b]
    nonidentity = 0
    for first in oriented:
        full_word = [list(first)] + sorter
        for x in range(16):
            row = [x >> i & 1 for i in range(4)]
            need(simulate(row, full_word) == sorted(row), "small positive sorter fails")
        for _, l, h in FAMILIES:
            for lows in combinations(range(4), l):
                for highs in combinations([i for i in range(4) if i not in lows], h):
                    low, high = sum(2 ** i for i in lows), sum(2 ** i for i in highs)
                    whole = family(4, full_word, low, high, "control")
                    all_pruned = pruning(4, full_word, whole)
                    k = 4 - l - h
                    q_all = all_pruned["retained_prefix"]
                    need(bound(k, q_all) <= len(q_all), "bound rejects a pruned positive sorter")
                    for x in range(2 ** k):
                        row = [x >> i & 1 for i in range(k)]
                        need(simulate(row, q_all) == sorted(row), "normalized pruned word fails to sort")
                    previous_cost = None
                    previous_record = None
                    for cut in range(len(full_word) + 1):
                        prefix = full_word[:cut]
                        record = family(4, prefix, low, high, "control")
                        pruned = pruning(4, prefix, record)
                        # Match the same original carrier in prefix and final labels.
                        inverse = {p: j for j, p in enumerate(pruned["input_to_output_wire"])}
                        phi = [all_pruned["input_to_output_wire"][inverse[p]] for p in range(k)]
                        conjugate = [[phi[a], phi[b]] for a, b in pruned["retained_prefix"]]
                        need(q_all[:len(conjugate)] == conjugate, "prefix/final carrier conjugation differs")
                        nonidentity += phi != list(range(k))
                        b = bound(k, pruned["retained_prefix"])
                        need(bound(k, conjugate) == b,
                             "bound is not invariant under carrier relabeling")
                        cost = record[4] + record[5] + b
                        if previous_cost is not None:
                            deleted = record[4] + record[5] > previous_record[4] + previous_record[5]
                            need(cost >= previous_cost + int(deleted), "nested cost monotonicity fails")
                            count("nested_cost_transition_controls")
                        previous_cost, previous_record = cost, record
                        wrong = set()
                        for x in range(16):
                            row = [x >> i & 1 for i in range(4)]
                            out = simulate(row, prefix)
                            wrong.update(p for p in range(4) if out[p] != sorted(row)[p])
                        needed = [p for p in wrong if (record[2] | record[3]) >> p & 1]
                        for p in needed:
                            index = next(t for t in range(cut, len(full_word)) if p in full_word[t])
                            need(whole[4] >= record[4] + 1 and all_pruned["marked_touch_mask"] >> index & 1,
                                 "required first touch is not marked")
                        charge = (len(needed) + 1) // 2
                        need(whole[4] - record[4] >= charge, "first-touch packing bound fails")
                        need(cost + charge <= len(full_word),
                             "required-touch bound rejects a known full sorter")
                        count("small_prefix_clamp_controls")
    need(nonidentity > 0, "no future-moving nonidentity carrier control")
    count("nonidentity_final_carrier_controls", nonidentity)

    # Every free output row, independently of any conditional reachable image.
    for q in (2, 3):
        reference, free = template(13, 3 | 2 ** q, 6144)
        for x in range(256):
            row = list(reference)
            for j, p in enumerate(free):
                row[p] = x >> j & 1
            for a, b in combinations(range(2, 11), 2):
                after = simulate(row, [(a, b)])
                if q == 2:
                    need(ports(after) == [7, 6144], "stationary low moves under allowed suffix pair")
                elif 3 in (a, b):
                    need((ports(after) == [7, 6144]) == ((a, b) == (2, 3)),
                         "wrong first marked gate reaches the terminal configuration")
                count("local_marker_pair_controls")
    for perm in permutations(range(4)):
        word = [[0, 3], [2, 1]]
        conjugate = [[perm[a], perm[b]] for a, b in word]
        need(bound(4, word) == bound(4, conjugate), "global wire-permutation control failed")
        count("wire_permutation_controls")


def main():
    started = time.monotonic()
    sources = {}
    for name, pin in PINS.items():
        data = (ROOT / name).read_bytes()
        need(hashlib.sha256(data).hexdigest() == pin, "published dependency changed: " + name)
        sources[name] = json.loads(data)
    data = (ROOT / "touch-certificate.json").read_bytes()
    certificate = json.loads(data)
    audit_certificate(certificate, sources)
    tiny_routing_controls()
    sorter8 = [[0, 2], [1, 3], [4, 6], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7],
               [0, 1], [2, 3], [4, 5], [6, 7], [2, 4], [3, 5], [1, 4], [3, 6],
               [1, 2], [3, 4], [5, 6]]
    for x in range(256):
        row = [x >> p & 1 for p in range(8)]
        need(simulate(row, sorter8) == sorted(row), "known nineteen-gate eight-wire sorter fails")
    need(bound(8, sorter8) == 19, "anchor bound rejects optimal eight-wire control")
    for x in range(8192):
        row = [x >> p & 1 for p in range(13)]
        need(simulate(row, sources["fixture.json"]["gates"]) == sorted(row), "native positive sorter fails")
        count("full_boolean_inputs")

    # Reject altered mathematical data without repeating the long image census.
    witness = certificate["cases"][2]["moving"]
    gates = (sources["fixture.json"]["gates"][:24] + sources["fixture.json"]["forced_gates"] +
             sources["certificate.json"]["kernels"][3]["kernel"])
    for mode in range(3):
        altered = deepcopy(witness)
        if mode == 0:
            altered["pruning"]["outer_record"][5] += 1
        elif mode == 1:
            altered["pruning"]["retained_prefix"][0].reverse()
        else:
            altered["inner_anchors"]["high"]["rows"][0]["label"] -= 1
        try:
            audit_witness(gates, altered, [11, 6144])
        except ValueError:
            count("damaged_witnesses_rejected")
        else:
            raise ValueError("damaged witness accepted")
    need(hashlib.sha256((ROOT / "fixture.json").read_bytes() + b" ").hexdigest() != PINS["fixture.json"],
         "damaged dependency was accepted")
    print(json.dumps({"status": "ALL_PAIRED_TOUCH_CHECKS_PASSED", "agent": "six-sorting-2",
                      "role": "researcher", "additional_exclusions": 6, "remaining_targets": 27,
                      "single_touch_targets": 33, "certificate_bytes": len(data),
                      "certificate_sha256": hashlib.sha256(data).hexdigest(),
                      "seconds": round(time.monotonic() - started, 3),
                      "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      **METRICS}, sort_keys=True))


if __name__ == "__main__":
    main()

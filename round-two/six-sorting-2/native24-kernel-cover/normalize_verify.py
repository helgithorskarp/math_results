"""Standalone scalar checker for ten normalized correction obstructions.

Imports no sibling code, producer, profiler, solver or external dependency.
Distinct numeric marker ranks and every original free Boolean assignment
determine the deleted gates. Heap Huffman merges independently check the
producer's dyadic anchor formula. The reusable scalar primitives are from touch_verify.py (same author).
This file is self-contained; the normalization bridge is in NORMALIZE.md.
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
    "touch-certificate.json": "04bcf3e1617c3ae2ce026149d1c76f620c8acf6e38bdc448719e26fa3ecd2455",
    "../../six-sorting-1/joint_extreme_kernel_barrier/frontier.json":
        "6041c9e1ed4bea12e3028836deb8b4e59de0e4d05205733393e4f4ca63c36667",
}
EXCLUDED = [6, 7, 10, 16, 18, 25, 29, 30, 37, 40]
WORD = [[3, 4], [2, 3]]
CORRECTION = {6: (7, 328, 9), 7: (7, 1048, 10), 10: (7, 328, 10),
              16: (7, 1048, 10), 18: (7, 1064, 8), 25: (21, 104, 10),
              29: (11, 324, 10), 30: (7, 328, 9), 37: (7, 1064, 10),
              40: (21, 104, 10)}
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


def audit_witness(gates, low, high, expected_cost, expected_ports=None):
    record = family(13, gates, low, high, "outer")
    if expected_ports is not None:
        need(record[2:4] == expected_ports, "wrong current marker positions")
    pruned = pruning(13, gates, record)
    n = 13 - (low | high).bit_count()
    need(n in (7, 8), "unsupported free cube dimension")
    data = profiles(n, pruned["retained_prefix"])
    anchors = anchor_bounds(n, data)
    b = max(x["lower_bound"] for x in anchors.values())
    c = sum(record[4:6])
    need(c + b == expected_cost, "nested clamping budget differs")
    return {"free_inputs": n, "pruning": pruned, "inner_profiles": data,
            "inner_anchors": anchors, "inner_bound": b, "prefix_cost": c,
            "cost_plus_bound": c + b, "maximum_future_marked_touches_at_44": 44 - c - b}


def boolean_images(p32):
    image9, image8 = set(), set()
    first_wrong = {}
    for x in range(8192):
        initial = [x >> p & 1 for p in range(13)]
        sorted_row = sorted(initial)
        a = simulate(initial, p32)
        need(a[:2] == sorted_row[:2] and a[11:] == sorted_row[11:], "P32 outer ranks differ")
        image9.add(sum(a[p] * 2 ** (p - 2) for p in range(2, 11)))
        b = simulate(a, WORD)
        need(b[:3] == sorted_row[:3] and b[11:] == sorted_row[11:], "P34 outer ranks differ")
        image8.add(sum(b[p] * 2 ** (p - 3) for p in range(3, 11)))
        for p in range(3, 11):
            if b[p] != sorted_row[p] and p not in first_wrong:
                first_wrong[p] = {"input_bits": x, "prefix_output_bits": sum(b[q] * 2 ** q for q in range(13)),
                                  "port": p, "actual_value": b[p], "correct_value": sorted_row[p]}
        count("full_boolean_inputs")
    rows = sorted(image8)
    target = {"n": 8, "original_wires": list(range(3, 11)), "size": len(rows),
              "image": rows, "image_sha256": digest(rows),
              "weight_counts": [sum(x.bit_count() == w for x in rows) for w in range(9)]}
    return sorted(image9), target, first_wrong


def reconstructed(sources):
    fixture, parent, previous, joined = (sources[name] for name in PINS)
    frontier = joined["joint_remaining24_ids"]
    need(frontier == [2, 6, 7, 8, 10, 15, 16, 18, 20, 24, 25, 29, 30, 31, 32, 33, 34, 36,
                      37, 38, 39, 40, 41, 42], "credited parent frontier differs")
    stationary = {row["kernel_id"]: row["stationary"] for row in previous["cases"]}
    need(fixture["n"] == 13 and len(fixture["gates"]) == 46 and
         fixture["forced_gates"] == [[11, 12], [1, 2]], "literal source fixture differs")
    cases = []
    for i in EXCLUDED:
        p32 = fixture["gates"][:24] + fixture["forced_gates"] + parent["kernels"][i]["kernel"]
        p34 = p32 + WORD
        need(len(p32) == 32 and all(0 <= a < b < 13 for a, b in p34), "bad prefix comparators")
        image9, target, wrong = boolean_images(p32)
        need(image9 == parent["kernels"][i]["target"]["image"], "preceding nine-wire image differs")
        need(all(x in image9 for x in (507, 509, 510)), "mandatory single-zero states missing")
        lo, hi = stationary[i]["pruning"]["outer_record"][:2]
        a2 = audit_witness(p32, lo, hi, 43, [7, 6144])
        need({k: v for k, v in a2.items() if k != "free_inputs"} == stationary[i],
             "prior stationary witness differs")
        a3 = audit_witness(p32, 11, 320 if i == 10 else 260, 42, [11, 6144])
        a4 = audit_witness(p32, 5632, 3, 42, [19, 6144])
        low, high, port = CORRECTION[i]
        need(low.bit_count() == high.bit_count() == 3, "wrong correction marker counts")
        last = audit_witness(p34, low, high, 44)
        record = last["pruning"]["outer_record"]
        need((record[2] | record[3]) >> port & 1, "correction port lacks a current marker")
        need(port in wrong, "required correction has no full Boolean witness")
        need(sum(record[4:6]) + last["inner_bound"] + 1 == 45, "wrong total lower bound")
        cases.append({"kernel_id": i, "prefix32_sha256": digest(p32), "prefix34_sha256": digest(p34),
                      "target9_sha256": digest(image9), "single_zero_states": [507, 509, 510],
                      "normalization_witnesses": {"low2": a2, "low3": a3, "low4": a4},
                      "normalized_target": target, "normalized_suffix_budget": 10,
                      "correction_pruning": last, "required_correction": wrong[port],
                      "forced_suffix_marked_touches": 1, "total_lower_bound": 45})
    return {"schema": "native-third-minimum-correction-v1", "agent": "six-sorting-2",
            "role": "researcher", "parent_files_sha256": PINS,
            "credited_parent_graph": "bafkreib7kp2spfixj5s3ossbqyzn5y4pxuusek2laaqr47fm3bc4dyevwu",
            "previous_nine_wire_ids": frontier, "forced_minimum_word": WORD,
            "excluded_kernel_ids": EXCLUDED, "remaining_nine_wire_ids": [i for i in frontier if i not in EXCLUDED],
            "cases": cases}


def local_normalization_controls():
    """All local scalar marker transitions and permitted gate commutations.

    These are finite implementation controls. The arbitrary-word argument
    and complete coverage are proved in NORMALIZE.md, without a depth bound.
    """
    for p in (2, 3, 4):
        template_row, free = template(13, 3 | 2 ** p, 6144)
        for x in range(256):
            row = list(template_row)
            for j, q in enumerate(free):
                row[q] = x >> j & 1
            for a, b in combinations(range(2, 11), 2):
                after = simulate(row, [(a, b)])
                expected = a if b == p else p
                need(ports(after) == [3 | 2 ** expected, 6144], "local low-marker route differs")
                count("local_marker_pair_controls")
        after_first = simulate(template_row, [[3, 4]])
        after_both = simulate(after_first, [[2, 3]])
        need(ports(after_both) == [7, 6144], "forced minimum word misses terminal lows")

    # Nine middle wires: event word (1,2),(0,1). Every permissible
    # preparation gate is verified on every Boolean row independently.
    before = [list(pair) for pair in combinations(range(3, 9), 2)]
    between = [list(pair) for pair in combinations(range(2, 9), 2)]
    for x in range(512):
        row = [x >> p & 1 for p in range(9)]
        for pair in before:
            need(simulate(row, [pair, [1, 2], [0, 1]]) ==
                 simulate(row, [[1, 2], [0, 1], pair]), "preceding disjoint gate does not commute")
            count("commutation_controls")
        for pair in between:
            need(simulate(row, [[1, 2], pair, [0, 1]]) ==
                 simulate(row, [[1, 2], [0, 1], pair]), "intervening disjoint gate does not commute")
            count("commutation_controls")


def positive_controls(fixture):
    sorter = fixture["gates"]
    for x in range(8192):
        row = [x >> p & 1 for p in range(13)]
        need(simulate(row, sorter) == sorted(row), "known native sorter fails")
        count("full_boolean_positive_inputs")
    for low, high in ((11, 260), (5632, 3), (7, 328)):
        record = family(13, sorter, low, high, "positive_outer")
        last = pruning(13, sorter, record)
        k = 13 - (low | high).bit_count()
        q = last["retained_prefix"]
        need(bound(k, q, "positive_inner") <= len(q), "nested bound rejects a known full sorter")
        for x in range(2 ** k):
            row = [x >> p & 1 for p in range(k)]
            need(simulate(row, q) == sorted(row), "pruned positive sorter fails")
            count("pruned_positive_inputs")
    sorter7 = [[0, 6], [2, 3], [4, 5], [0, 2], [1, 4], [3, 6], [0, 1], [2, 5],
               [3, 4], [1, 2], [4, 6], [2, 3], [4, 5], [1, 2], [3, 4], [5, 6]]
    for x in range(128):
        row = [x >> p & 1 for p in range(7)]
        need(simulate(row, sorter7) == sorted(row), "known sixteen-gate sorter fails")
    need(bound(7, sorter7, "positive_inner") == 16, "bound rejects optimal seven-wire control")
    for perm in permutations(range(4)):
        word = [[0, 3], [2, 1]]
        renamed = [[perm[a], perm[b]] for a, b in word]
        need(bound(4, word) == bound(4, renamed), "wire permutation changes the bound")
        count("wire_permutation_controls")


def match(candidate, expected):
    need(candidate == expected, "complete reconstructed certificate differs")


def main():
    started = time.monotonic()
    sources = {}
    for name, pin in PINS.items():
        raw = (ROOT / name).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == pin, "published dependency changed: " + name)
        sources[name] = json.loads(raw)
    raw = (ROOT / "normalize-certificate.json").read_bytes()
    candidate = json.loads(raw)
    expected = reconstructed(sources)
    match(candidate, expected)
    local_normalization_controls()
    positive_controls(sources["fixture.json"])
    # Entry-level equality rejects corruption after all finite computations
    # have been independently reconstructed; do not repeat the long census.
    damaged = [deepcopy(candidate) for _ in range(6)]
    damaged[0]["cases"][0]["normalization_witnesses"]["low4"]["pruning"]["outer_record"][4] += 1
    damaged[1]["cases"][0]["correction_pruning"]["pruning"]["retained_prefix"][0].reverse()
    damaged[2]["cases"][0]["correction_pruning"]["inner_anchors"]["high"]["rows"][0]["label"] -= 1
    damaged[3]["cases"][0]["required_correction"]["correct_value"] ^= 1
    damaged[4]["cases"][0]["normalized_target"]["image"].pop()
    damaged[5]["remaining_nine_wire_ids"].pop()
    for item in damaged:
        try:
            match(item, expected)
        except ValueError:
            count("damaged_certificates_rejected")
        else:
            raise ValueError("damaged certificate was accepted")
    need(hashlib.sha256((ROOT / "fixture.json").read_bytes() + b" ").hexdigest() != PINS["fixture.json"],
         "damaged fixture was accepted")
    print(json.dumps({"status": "ALL_NORMALIZED_CORRECTION_CHECKS_PASSED", "agent": "six-sorting-2",
                      "role": "researcher", "additional_exclusions": 10, "remaining_targets": 14,
                      "certificate_bytes": len(raw), "certificate_sha256": hashlib.sha256(raw).hexdigest(),
                      "seconds": time.monotonic() - started,
                      "maximum_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, **METRICS}, sort_keys=True))


if __name__ == "__main__":
    main()

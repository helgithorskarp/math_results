"""Standalone numeric/heap verifier for fourteen three-touch obstructions.

No producer, sibling implementation, profiler or solver is imported. The
numeric clamping/pruning and heap primitives below are credited and reused
from six-sorting-2's published touch_verify.py (source e260dd848eb8616697a952840c0027965e5851c3).
They are algorithmically different from the packed-column producer.
The new complete marked-word census uses explicit Cartesian products.
"""
from copy import deepcopy
import hashlib
import heapq
from itertools import combinations, permutations, product
import json
import os
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
SOURCE = Path(os.environ.get("SORTING_SOURCE_ROOT", ROOT.parents[2]))
BASE = "round-two/six-sorting-2/native24-kernel-cover/"
PINS = {
    BASE + "fixture.json": "93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6",
    BASE + "certificate.json": "21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06",
    BASE + "touch-certificate.json": "04bcf3e1617c3ae2ce026149d1c76f620c8acf6e38bdc448719e26fa3ecd2455",
    BASE + "normalize-certificate.json": "99bcad813962ff1495a7f9f217b5ec4a8b94b83e71020754ff5eacf6f7abe490",
}
FIXTURE_PIN = "664b1f3a8510dd357e461c8ce43add2fece674d22acc831f001ad47ef055f746"
IDS = [2, 8, 15, 20, 24, 31, 32, 33, 34, 36, 38, 39, 41, 42]
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


def boolean_image(gates):
    image, wrong = set(), {}
    for x in range(8192):
        initial = [x >> p & 1 for p in range(13)]
        row, correct = simulate(initial, gates), sorted(initial)
        need(all(row[p] == correct[p] for p in (0, 1, 11, 12)), "frozen output rank differs")
        y = sum(2 ** p for p, value in enumerate(row) if value)
        image.add(sum(2 ** p for p, value in enumerate(row[2:11]) if value))
        for p in range(13):
            if p not in wrong and row[p] != correct[p]:
                wrong[p] = [p, x, y, row[p], correct[p]]
        count("full_original_boolean_inputs")
    return sorted(image), [wrong[p] for p in sorted(wrong)]


def marked_word_census(low, high, wrong_ports, allow_other_wire2=False):
    """Independently enumerate every tuple of zero, one or two marked gates.

    Free preparations preserve marker positions. The proof explains why the
    imported unique root is itself marked and all required initial marked
    wrong ports must appear in this subsequence.
    """
    initial, _ = template(13, low, high)
    if allow_other_wire2:
        gates = list(combinations(range(2, 11), 2))
        root = None
    else:
        gates = [(2, 3)] + list(combinations(range(3, 11), 2))
        root = (2, 3)
    required = [p for p in wrong_ports if marked(initial[p])]
    counts, terminal = [], []
    for length in range(3):
        valid = 0
        for word in product(gates, repeat=length):
            if root is not None and word.count(root) > 1:
                continue
            row = list(initial)
            touched = set()
            for a, b in word:
                if not marked(row[a]) and not marked(row[b]):
                    break
                touched.add(a)
                touched.add(b)
                row[a], row[b] = min(row[a], row[b]), max(row[a], row[b])
            else:
                valid += 1
                count("complete_marked_words_checked")
                if (root is None or word.count(root) == 1) and ports(row) == [7, 7168]:
                    terminal.append({"word": [list(g) for g in word],
                                     "untouched_required_ports": [p for p in required if p not in touched]})
        counts.append(valid)
    terminal.sort(key=lambda x: x["word"])
    return {"allowed_standard_pairs": [list(g) for g in gates],
            "required_initial_marked_wrong_ports": required,
            "complete_counts_by_marked_word_length": counts,
            "root_terminal_words": terminal,
            "compatible_words": [x["word"] for x in terminal if not x["untouched_required_ports"]]}


def reconstruct(fixture, sources):
    native, parent, touch, normalized = (sources[BASE + name] for name in
                                        ("fixture.json", "certificate.json", "touch-certificate.json", "normalize-certificate.json"))
    need(fixture["agent"] == "six-sorting-1" and fixture["role"] == "researcher", "wrong author attribution")
    need(fixture["schema"] == "native-three-marked-touch-fixture-v1" and
         fixture["n"] == 13 and fixture["size_budget"] == 44, "wrong fixture domain")
    need(fixture["native_prefix24"] == native["gates"][:24] and fixture["known46"] == native["gates"],
         "literal native gates differ")
    need(fixture["forced_gates"] == native["forced_gates"] == [[11, 12], [1, 2]], "forced pair differs")
    need(fixture["previous_nine_wire_ids"] == normalized["remaining_nine_wire_ids"] == IDS,
         "preceding fourteen-target cover differs")
    need([item["kernel_id"] for item in fixture["cases"]] == IDS, "incomplete or repeated case IDs")
    cases = []
    for item in fixture["cases"]:
        i = item["kernel_id"]
        need(item["kernel"] == parent["kernels"][i]["kernel"] and i in touch["single_wire2_touch_kernel_ids"],
             "initial kernel or unique-root coverage differs")
        gates = fixture["native_prefix24"] + fixture["forced_gates"] + item["kernel"]
        need(len(gates) == 32 and all(0 <= a < b < 13 for a, b in gates), "invalid standard prefix")
        image, wrong = boolean_image(gates)
        need(image == parent["kernels"][i]["target"]["image"], "parent image differs")
        need([w[0] for w in wrong] == list(range(2, 11)), "wrong-port controls differ")
        low, high = item["original_low_mask"], item["original_high_mask"]
        need(low.bit_count() == high.bit_count() == 3, "wrong marked family")
        record = family(13, gates, low, high, "outer")
        need(record[2] == 19 and record[3] in (6656, 7168),
             "three-touch class not reached")
        pruned = pruning(13, gates, record)
        pruned.pop("marked_touch_mask")
        q = pruned["retained_prefix"]
        data = profiles(7, q)
        anchors = anchor_bounds(7, data)
        b = max(16, *(x["lower_bound"] for x in anchors.values()))
        cover = marked_word_census(record[2], record[3], [w[0] for w in wrong])
        need(not cover["compatible_words"], "two marked gates not excluded")
        need(sum(record[4:6]) + b == 42, "selected nested bound differs")
        cases.append({"kernel_id": i, "prefix32_sha256": digest(gates),
                      "target9_image": image, "target9_sha256": digest(image),
                      "full_boolean_wrong_port_witnesses": wrong, "pruning": pruned,
                      "inner_profiles": data, "inner_anchors": anchors, "inner_bound": b,
                      "prefix_cost": sum(record[4:6]), "C_plus_B": 42,
                      "two_touch_cover": cover, "minimum_future_marked_touches": 3,
                      "total_size_lower_bound": 45})
    return {"schema": "native-three-marked-touch-certificate-v1", "agent": "six-sorting-1",
            "role": "researcher", "parent_files_sha256": PINS,
            "credited_fourteen_target_graph": "bafkreie4gyppvazofxko6ohk7jbbltjmae6caeamkvb3tqflb5x2l7qzre",
            "previous_nine_wire_ids": IDS, "excluded_kernel_ids": IDS,
            "remaining_nine_wire_ids": [], "native_prefix24_standard_size_lower_bound": 45,
            "cases": cases}


def positive_controls(fixture):
    for name in ("known45", "known46"):
        need(len(fixture[name]) == (45 if name == "known45" else 46), "positive sorter size differs")
        for x in range(8192):
            row = [x >> p & 1 for p in range(13)]
            need(simulate(row, fixture[name]) == sorted(row), "known thirteen-wire sorter fails")
            count("positive_full_boolean_inputs")
    for high in (104, 42, 322):
        record = family(13, fixture["known46"], 21, high, "positive_outer")
        small = pruning(13, fixture["known46"], record)
        q = small["retained_prefix"]
        need(bound(7, q, "positive_inner") <= len(q), "nested bound rejects pruned positive sorter")
        for x in range(128):
            row = [x >> p & 1 for p in range(7)]
            need(simulate(row, q) == sorted(row), "pruned positive sorter fails")
            count("pruned_positive_inputs")
    sorter7 = [[0, 6], [2, 3], [4, 5], [0, 2], [1, 4], [3, 6], [0, 1], [2, 5],
               [3, 4], [1, 2], [4, 6], [2, 3], [4, 5], [1, 2], [3, 4], [5, 6]]
    for x in range(128):
        row = [x >> p & 1 for p in range(7)]
        need(simulate(row, sorter7) == sorted(row), "known seven-wire sorter fails")
        count("positive_seven_wire_inputs")
    need(bound(7, sorter7, "positive_inner") == 16, "bound rejects sixteen-gate positive sorter")
    for perm in permutations(range(4)):
        word = [[0, 3], [2, 1]]
        renamed = [[perm[a], perm[b]] for a, b in word]
        need(bound(4, word) == bound(4, renamed), "global relabeling changes the bound")
        count("wire_permutation_controls")
    # Relaxing q4 to q3 or allowing other wire2 gates admits compatible
    # short marked words: neither root nor marker-location condition is vacuous.
    need(marked_word_census(11, 7168, [3, 10])["compatible_words"], "q3 positive census is empty")
    need(marked_word_census(19, 7168, [4, 10], True)["compatible_words"],
         "unrestricted wire2 positive census is empty")
    count("positive_marked_word_censuses", 2)


def match(candidate, expected):
    need(candidate == expected, "complete independently reconstructed certificate differs")


def main():
    start = time.monotonic()
    raw_fixture = (ROOT / "fixture.json").read_bytes()
    need(hashlib.sha256(raw_fixture).hexdigest() == FIXTURE_PIN, "literal fixture changed")
    fixture = json.loads(raw_fixture)
    sources = {}
    for path, pin in PINS.items():
        raw = (SOURCE / path).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == pin, "published mathematical input changed: " + path)
        sources[path] = json.loads(raw)
    expected = reconstruct(fixture, sources)
    raw = (ROOT / "certificate.json").read_bytes()
    candidate = json.loads(raw)
    match(candidate, expected)
    positive_controls(fixture)
    damaged = [deepcopy(candidate) for _ in range(8)]
    damaged[0]["cases"][0]["pruning"]["outer_record"][4] -= 1
    damaged[1]["cases"][0]["pruning"]["retained_prefix"][0].reverse()
    damaged[2]["cases"][0]["inner_profiles"]["one_minimum"]["records_sha256"] = "0" * 64
    damaged[3]["cases"][0]["inner_anchors"]["low"]["rows"][0]["label"] -= 1
    damaged[4]["cases"][0]["full_boolean_wrong_port_witnesses"][-1][3] ^= 1
    damaged[5]["cases"][0]["two_touch_cover"]["complete_counts_by_marked_word_length"][2] -= 1
    damaged[6]["cases"][0]["two_touch_cover"]["root_terminal_words"] = []
    damaged[7]["excluded_kernel_ids"].pop()
    for item in damaged:
        try:
            match(item, expected)
        except ValueError:
            count("damaged_certificates_rejected")
        else:
            raise ValueError("damaged certificate was accepted")
    need(hashlib.sha256(raw_fixture + b" ").hexdigest() != FIXTURE_PIN, "damaged fixture accepted")
    print(json.dumps({"status": "ALL_THREE_TOUCH_CHECKS_PASSED", "agent": "six-sorting-1", "role": "researcher",
                      "new_kernel_exclusions": len(IDS), "remaining_native_targets": 0,
                      "certificate_bytes": len(raw), "certificate_sha256": hashlib.sha256(raw).hexdigest(),
                      "seconds": time.monotonic() - start,
                      "maximum_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      **METRICS}, sort_keys=True))


if __name__ == "__main__":
    main()

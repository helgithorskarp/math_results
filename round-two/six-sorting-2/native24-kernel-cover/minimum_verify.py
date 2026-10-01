"""Scalar certification of the third-minimum refinement and nested pruning.

Imports only the pinned independent scalar checker verify.py. Imports no
producer, Boolean-column profiler, solver, or solver result. All original
four-mark domains are enumerated before each family's image is compressed.
"""

from copy import deepcopy
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
BASE_CHECKER_SHA256 = "62942073dd9b335f71e3ad2e55fd18d5cd9831f668ff8dc734de0a86fec33c29"
BASE_CERTIFICATE_SHA256 = "21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06"
if hashlib.sha256((ROOT / "verify.py").read_bytes()).hexdigest() != BASE_CHECKER_SHA256:
    raise ValueError("published scalar dependency changed")
spec = importlib.util.spec_from_file_location("native_scalar_checker", ROOT / "verify.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
need = v.need
INNER_ASSIGNMENTS = 0


def snapshot(data):
    item = v.family_summary(data, 3, 1)
    return {key: item[key] for key in ("envelope", "summary", "records_sha256")}


def pruning_word(gates, record):
    """Use a scalar marker trajectory and the independently checked R mask."""
    low, high = record[:2]
    lows = [p for p in range(13) if (low >> p) & 1]
    highs = [p for p in range(13) if (high >> p) & 1]
    free = [p for p in range(13) if p not in lows and p not in highs]
    reference = [0] * 13
    for j, p in enumerate(lows):
        reference[p] = j - len(lows)
    for j, p in enumerate(highs):
        reference[p] = j + 2
    carriers = [None if p not in free else free.index(p) for p in range(13)]
    retained, touched = [], 0
    for t, (a, b) in enumerate(gates):
        if v.mark(reference[a]) or v.mark(reference[b]):
            touched |= 1 << t
            need(not (record[6] >> t) & 1, "touched gate recorded redundant")
            if reference[a] > reference[b]:
                reference[a], reference[b] = reference[b], reference[a]
                carriers[a], carriers[b] = carriers[b], carriers[a]
        elif not (record[6] >> t) & 1:
            retained.append([carriers[a], carriers[b]])
    output_free = [p for p in range(13) if not v.mark(reference[p])]
    rename = {carriers[p]: j for j, p in enumerate(output_free)}
    need(touched.bit_count() == record[4], "scalar marked-touch count changed")
    need(record[6].bit_count() == record[5], "scalar redundancy count changed")
    return {"outer_record": record, "marked_touch_mask": touched,
            "input_free_wires": free, "output_free_wires": output_free,
            "input_to_output_wire": [rename[j] for j in range(len(free))],
            "retained_prefix": [[rename[a], rename[b]] for a, b in retained]}


def check_pruning_function(gates, witness):
    """Check the original and pruned prefix functions on every free input."""
    low, high = witness["outer_record"][:2]
    lows = [p for p in range(13) if (low >> p) & 1]
    highs = [p for p in range(13) if (high >> p) & 1]
    free = witness["input_free_wires"]
    rename = witness["input_to_output_wire"]
    need(sorted(rename) == list(range(9)), "input relabel is not a permutation")
    need(witness["output_free_wires"] == list(range(3, 12)), "wrong free output ports")
    need(len(witness["retained_prefix"]) == 15, "wrong retained prefix size")
    need(all(0 <= a < b < 9 for a, b in witness["retained_prefix"]),
         "selected retained prefix is not standard")
    for assignment in range(512):
        original, pruned = [0] * 13, [0] * 9
        for j, p in enumerate(lows):
            original[p] = j - len(lows)
        for j, p in enumerate(highs):
            original[p] = j + 2
        for j, p in enumerate(free):
            original[p] = pruned[rename[j]] = (assignment >> j) & 1
        result = v.simulation(original, gates)
        need([result[p] for p in witness["output_free_wires"]] ==
             v.simulation(pruned, witness["retained_prefix"]),
             "pruning does not preserve the conditional function")


def inner_family(gates, lo, hi):
    """Independent scalar enumeration on nine wires, with numeric markers."""
    global INNER_ASSIGNMENTS
    members = []
    for lows in combinations(range(9), lo):
        for highs in combinations([p for p in range(9) if p not in lows], hi):
            free = [p for p in range(9) if p not in lows and p not in highs]
            template = [0] * 9
            for j, p in enumerate(lows):
                template[p] = j - len(lows)
            for j, p in enumerate(highs):
                template[p] = j + 2
            reference, touched, active = list(template), 0, 0
            for t, (a, b) in enumerate(gates):
                if v.mark(reference[a]) or v.mark(reference[b]):
                    touched |= 1 << t
                if reference[a] > reference[b]:
                    reference[a], reference[b] = reference[b], reference[a]
            for assignment in range(1 << len(free)):
                row = list(template)
                for j, p in enumerate(free):
                    row[p] = (assignment >> j) & 1
                for t, (a, b) in enumerate(gates):
                    hit = v.mark(row[a]) or v.mark(row[b])
                    need(hit == bool((touched >> t) & 1), "inner marker trajectory varies")
                    if row[a] > row[b]:
                        if not hit:
                            active |= 1 << t
                        row[a], row[b] = row[b], row[a]
                need(v.ports(row) == v.ports(reference), "inner final marker ports vary")
                INNER_ASSIGNMENTS += 1
            redundant = ((1 << len(gates)) - 1) & ~(touched | active)
            record = [sum(1 << p for p in lows), sum(1 << p for p in highs),
                      *v.ports(reference), touched.bit_count(), redundant.bit_count(), redundant]
            members.append((record, None))
    return v.family_summary(members, lo, hi)


def inner_anchors(profiles):
    answer = {}
    for side, index, count, unary in (("low", 0, "low_count", "one_minimum"),
                                      ("high", 1, "high_count", "one_maximum")):
        chosen = {name: item for name, item in profiles.items() if item[count] > 0}
        reachable = sorted(row[index].bit_length() - 1 for row in profiles[unary]["envelope"])
        rows = []
        for p in reachable:
            masses = {name: sum(1 << r[3] for r in item["envelope"] if (r[index] >> p) & 1)
                      for name, item in chosen.items()}
            label = max({7: 16, 8: 19}[9 - item["low_count"] - item["high_count"]] +
                        v.ceiling_log(masses[name]) for name, item in chosen.items() if masses[name])
            rows.append({"port": p, "anchored_masses": masses, "label": label,
                         "units": 1 << (label - 16)})
        mass = sum(row["units"] for row in rows)
        answer[side] = {"base": 16, "normalized_mass": mass,
                        "lower_bound": 16 + v.ceiling_log(mass), "rows": rows}
    return answer


def main():
    start = time.monotonic()
    parent_bytes = (ROOT / "certificate.json").read_bytes()
    need(hashlib.sha256(parent_bytes).hexdigest() == BASE_CERTIFICATE_SHA256, "parent changed")
    fixture = json.loads((ROOT / "fixture.json").read_text())
    parent = json.loads(parent_bytes)
    certificate = json.loads((ROOT / "minimum-certificate.json").read_text())
    base = v.extend(v.clamped_family(fixture["gates"][:24], 3, 1), fixture["forced_gates"], 24)
    print("ALL_ORIGINAL_FOUR_MARK_DOMAINS_BUILT", v.METRICS["original_free_assignments"], flush=True)
    image26 = v.apply_image(v.all_image(fixture["gates"][:24]), fixture["forced_gates"])
    out = {"schema": "native-third-minimum-refinement-v1", "agent": "six-sorting-2",
           "role": "researcher", "parent_certificate_sha256": BASE_CERTIFICATE_SHA256,
           "forced_minimum_word": [[3, 4], [2, 3]], "cases": [], "nested_exclusions": [],
           "excluded_kernel_ids": [14, 23],
           "remaining_nine_wire_ids": [i for i in parent["remaining_ids"]
                                       if i not in (11, 14, 17, 19, 23, 26)],
           "remaining_eight_wire_ids": [11, 17, 19, 26]}
    sort8 = [(0, 2), (1, 3), (4, 6), (5, 7), (0, 4), (1, 5), (2, 6), (3, 7),
             (0, 1), (2, 3), (4, 5), (6, 7), (2, 4), (3, 5), (1, 4), (3, 6),
             (1, 2), (3, 4), (5, 6)]
    for x in range(256):
        row = [(x >> p) & 1 for p in range(8)]
        need(v.simulation(row, sort8) == sorted(row), "eight-wire positive control")
    for i in (11, 14, 17, 19, 23, 26):
        kernel = parent["kernels"][i]["kernel"]
        data = v.extend(base, kernel, 26)
        snapshots = [snapshot(data)]
        need(snapshots[0]["envelope"] == [[7, 4096, 17, 18], [11, 4096, 16, 17],
                                         [19, 4096, 16, 17]], "saturated support differs")
        for offset, gate in enumerate(out["forced_minimum_word"], 32):
            data = v.extend(data, [gate], offset)
            snapshots.append(snapshot(data))
        need([x["summary"]["semantic_mass"] for x in snapshots] == [1 << 19] * 3,
             "saturated mass changes")
        need(snapshots[-1]["envelope"] == [[7, 4096, 18, 19]], "terminal min cost differs")
        image34 = v.apply_image(image26, kernel + out["forced_minimum_word"])
        for row in image34:
            need(list(row[:3]) == sorted(row)[:3] and list(row[11:]) == sorted(row)[11:],
                 "outer ranks not fixed")
        target = v.target(image34, 3, 11)
        out["cases"].append({"kernel_id": i, "profiles32_33_34": snapshots, "target": target})
        if i in (14, 23):
            input_low = 11 if i == 14 else 21
            record = next(r for r, _ in data if r[:2] == [input_low, 256])
            need(record[4:6] == [17, 2], "wrong outer deletion cost")
            gates = fixture["gates"][:24] + fixture["forced_gates"] + kernel + out["forced_minimum_word"]
            witness = pruning_word(gates, record)
            check_pruning_function(gates, witness)
            profiles = {name: inner_family(witness["retained_prefix"], lo, hi)
                        for name, lo, hi in v.FAMILIES}
            anchors = inner_anchors(profiles)
            bound = max(x["lower_bound"] for x in anchors.values())
            need(bound == 26, "inner lower bound not 26")
            witness.update({"kernel_id": i, "inner_profiles": profiles,
                            "inner_anchors": anchors, "inner_bound": bound, "total_bound": 19 + bound})
            out["nested_exclusions"].append(witness)
        print("BRANCH_CERTIFIED", i, target["size"], flush=True)

    # Every standard pair on the allowed wires is classified at each event.
    words, classified = [], 0
    def cover(live, word):
        nonlocal classified
        if len(live) == 1:
            need(live == {2: 19}, "incorrect minimum terminal")
            words.append(word)
            return
        for a in range(2, 11):
            for b in range(a + 1, 11):
                classified += 1
                if a not in live or b not in live or live[a] != live[b]:
                    continue
                following = dict(live)
                following[a] += 1
                del following[b]
                cover(following, word + [[a, b]])
    cover({2: 18, 3: 17, 4: 17}, [])
    need(words == [[[3, 4], [2, 3]]], "equal-cost minimum cover not unique")
    need(len(out["remaining_nine_wire_ids"]) == 33, "wrong nine-wire disjunction")
    need(len({x["target"]["image_sha256"] for x in out["cases"]}) == 6, "images not distinct")
    need(out == certificate, "complete independently reconstructed certificate differs")
    damaged = []
    first = deepcopy(certificate)
    first["cases"][0]["profiles32_33_34"][0]["envelope"][0][3] += 1
    damaged.append(first)
    second = deepcopy(certificate)
    second["nested_exclusions"][0]["retained_prefix"][0] = [0, 2]
    damaged.append(second)
    third = deepcopy(certificate)
    third["nested_exclusions"][1]["inner_anchors"]["low"]["rows"][1]["label"] -= 1
    damaged.append(third)
    for altered in damaged:
        need(altered != out, "corrupted evidence escaped reconstruction")
    print(json.dumps({"status": "ALL_THIRD_MINIMUM_REFINEMENT_CHECKS_PASSED",
                      "author_agent": "six-sorting-2", "role": "researcher",
                      "eight_wire_cases": 6, "additional_exclusions": 2, "remaining_targets": 37,
                      "classified_pairs": classified, "complete_equal_min_words": len(words),
                      "inner_free_assignments": INNER_ASSIGNMENTS,
                      "pruning_function_assignments": 1024, "corruptions_rejected": len(damaged),
                      "eight_wire_sizes": [x["target"]["size"] for x in out["cases"]],
                      "certificate_sha256": hashlib.sha256((ROOT / "minimum-certificate.json").read_bytes()).hexdigest(),
                      "seconds": round(time.monotonic() - start, 3),
                      "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      **v.METRICS}, sort_keys=True))


if __name__ == "__main__":
    main()

"""Independent scalar-image and exhaustive equal-merge cover checker.

No imports from the generator, parent profiler, parent checker, or solvers.
The original clamped domain is enumerated before compressing each family's
exact image. Different original families are never identified by marker ports.
"""

from copy import deepcopy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
FAMILIES = (("one_minimum", 1, 0), ("one_maximum", 0, 1),
            ("two_minima", 2, 0), ("two_maxima", 0, 2), ("mixed_pair", 1, 1))
SIZES = {11: 35, 12: 39}
METRICS = {"original_free_assignments": 0, "prefix_scalar_gate_evaluations": 0,
           "continuation_scalar_gate_evaluations": 0, "full_boolean_inputs": 0,
           "equal_merge_words": 0, "kernel_order_control_rows": 0}


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def mark(value):
    return value < 0 or value > 1


def ports(row):
    return (sum(2 ** i for i, x in enumerate(row) if x < 0),
            sum(2 ** i for i, x in enumerate(row) if x > 1))


def simulation(row, gates):
    values = list(row)
    for a, b in gates:
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values


def clamped_family(gates, lo, hi):
    members = []
    for lows in combinations(range(13), lo):
        for highs in combinations([i for i in range(13) if i not in lows], hi):
            free = [i for i in range(13) if i not in lows and i not in highs]
            template = [0] * 13
            for j, i in enumerate(lows):
                template[i] = j - len(lows)
            for j, i in enumerate(highs):
                template[i] = 2 + j
            reference = list(template)
            touched = 0
            for t, (a, b) in enumerate(gates):
                if mark(reference[a]) or mark(reference[b]):
                    touched |= 2 ** t
                if reference[a] > reference[b]:
                    reference[a], reference[b] = reference[b], reference[a]
            active, image = 0, set()
            for assignment in range(2 ** len(free)):
                row = list(template)
                for j, i in enumerate(free):
                    row[i] = (assignment >> j) & 1
                for t, (a, b) in enumerate(gates):
                    hit = mark(row[a]) or mark(row[b])
                    need(hit == bool((touched >> t) & 1), "conditional marker trajectory changed")
                    if row[a] > row[b]:
                        if not hit:
                            active |= 2 ** t
                        row[a], row[b] = row[b], row[a]
                need(ports(row) == ports(reference), "conditional final marker ports changed")
                image.add(tuple(row))
                METRICS["original_free_assignments"] += 1
                METRICS["prefix_scalar_gate_evaluations"] += len(gates)
            redundant = ((2 ** len(gates) - 1) & ~(touched | active))
            lm, hm = sum(2 ** i for i in lows), sum(2 ** i for i in highs)
            lp, hp = ports(reference)
            record = [lm, hm, lp, hp, touched.bit_count(), redundant.bit_count(), redundant]
            members.append((record, image))
    return members


def extend(members, gates, offset):
    result = []
    for record, original_image in members:
        record, image = list(record), original_image
        for t, (a, b) in enumerate(gates, offset):
            reference = next(iter(image))
            touched = mark(reference[a]) or mark(reference[b])
            active = False
            new_image = set()
            for original in image:
                need(touched == (mark(original[a]) or mark(original[b])), "nonuniform marker touch")
                row = list(original)
                if row[a] > row[b]:
                    if not touched:
                        active = True
                    row[a], row[b] = row[b], row[a]
                new_image.add(tuple(row))
                METRICS["continuation_scalar_gate_evaluations"] += 1
            if touched:
                record[4] += 1
            elif not active:
                record[5] += 1
                record[6] |= 2 ** t
            record[2], record[3] = ports(next(iter(new_image)))
            need(all(ports(row) == (record[2], record[3]) for row in new_image), "marker image varies")
            image = new_image
        result.append((record, image))
    return result


def family_summary(members, lo, hi):
    records = sorted(record for record, _ in members)
    classes = {}
    for r in records:
        key = r[2], r[3]
        d, c = classes.get(key, (0, 0))
        classes[key] = max(d, r[4]), max(c, r[4] + r[5])
    envelope = [[lp, hp, d, c] for (lp, hp), (d, c) in sorted(classes.items())]
    return {"low_count": lo, "high_count": hi, "envelope": envelope,
            "records_sha256": sha(records),
            "summary": {"ordinary_mass": sum(2 ** r[2] for r in envelope),
                        "semantic_mass": sum(2 ** r[3] for r in envelope),
                        "maximum_deletions": max(r[4] for r in records),
                        "maximum_semantic_deletions": max(r[4] + r[5] for r in records),
                        "maximum_redundancies": max(r[5] for r in records),
                        "port_classes": len(envelope)}}


def ceiling_log(mass):
    exponent = 0
    while 2 ** exponent < mass:
        exponent += 1
    return exponent


def summary(data):
    families = {name: family_summary(data[name], lo, hi) for name, lo, hi in FAMILIES}
    anchors = {}
    for side, count, column, unary in (("low", "low_count", 0, "one_minimum"),
                                        ("high", "high_count", 1, "one_maximum")):
        selected = {name: item for name, item in families.items() if item[count] > 0}
        reachable = sorted(row[column].bit_length() - 1 for row in families[unary]["envelope"])
        rows = []
        for port in reachable:
            masses = {name: sum(2 ** row[3] for row in item["envelope"]
                               if row[column] & (2 ** port)) for name, item in selected.items()}
            label = max(SIZES[13 - item["low_count"] - item["high_count"]] + ceiling_log(masses[name])
                        for name, item in selected.items() if masses[name])
            rows.append({"port": port, "anchored_masses": masses, "label": label,
                         "units": 2 ** (label - 35)})
        mass = sum(row["units"] for row in rows)
        anchors[side] = {"base": 35, "normalized_mass": mass,
                         "lower_bound": 35 + ceiling_log(mass), "rows": rows}
    return {"families": families, "anchors": anchors}


def all_image(gates):
    image = set()
    for x in range(8192):
        image.add(tuple(simulation([(x >> i) & 1 for i in range(13)], gates)))
        METRICS["full_boolean_inputs"] += 1
    return image


def apply_image(image, gates):
    return {tuple(simulation(row, gates)) for row in image}


def target(image, start, stop):
    rows = sorted({sum(row[i] * (2 ** (i - start)) for i in range(start, stop)) for row in image})
    return {"n": stop - start, "original_wires": list(range(start, stop)),
            "size": len(rows), "image": rows, "image_sha256": sha(rows),
            "weight_counts": [sum(row.bit_count() == w for row in rows) for w in range(stop - start + 1)]}


def complete_merge_cover():
    """DFS over every equal-weight binary event, with no selected kernel order."""
    representatives = {}
    all_words = []
    def visit(live, word, nodes):
        if len(live) == 1:
            need(live == {11: 9}, "wrong terminal maximum route")
            representative = tuple(pair for _, pair in sorted(nodes))
            representatives[representative] = True
            all_words.append((tuple(word), representative))
            return
        for a, b in combinations(sorted(live), 2):
            if live[a] != live[b]:
                continue
            level = live[a] + 1
            following = dict(live)
            del following[a]
            following[b] = level
            visit(following, word + [(a, b)], nodes + [(level, (a, b))])
    visit({**{i: 6 for i in range(5, 11)}, 11: 7}, [], [])
    need(len(representatives) == 45, "cover is not 45 kernels")
    for word, representative in all_words:
        for x in range(128):
            row = [0] * 13
            for i in range(7):
                row[5 + i] = (x >> i) & 1
            need(simulation(row, word) == simulation(row, representative), "canonical kernel changes image")
            METRICS["kernel_order_control_rows"] += 1
    METRICS["equal_merge_words"] = len(all_words)
    return set(representatives)


def rebuild(fixture):
    gates = fixture["gates"]
    need(fixture["n"] == 13 and len(gates) == 46, "wrong native dimensions")
    need(all(len(pair) == 2 and 0 <= pair[0] < pair[1] < 13 for pair in gates), "nonstandard gate")
    need(sha(gates) == "9adf68d7c1185ae5601aa2336bae54a8a08b7e94a08e2574b8c89c24d8b092c6", "native word changed")
    p = gates[:24]
    data24 = {name: clamped_family(p, lo, hi) for name, lo, hi in FAMILIES}
    data25 = {name: extend(rows, [(11, 12)], 24) for name, rows in data24.items()}
    data26 = {name: extend(rows, [(1, 2)], 25) for name, rows in data25.items()}
    p24, p25, p26 = summary(data24), summary(data25), summary(data26)
    need([(r["port"], r["label"]) for r in p24["anchors"]["low"]["rows"]] == [(0, 44)], "low equality premise")
    need([(r["port"], r["label"]) for r in p24["anchors"]["high"]["rows"]] == [(11, 43), (12, 43)], "high equality premise")
    need(p25["families"]["two_minima"]["envelope"] == [[3, 0, 8, 8], [5, 0, 8, 8]], "second minimum equality premise")
    need(p26["families"]["two_maxima"]["envelope"] ==
         [[0, 4096 + (2 ** i), 6, 6] for i in range(5, 11)] + [[0, 6144, 7, 7]], "second maximum equality premise")
    image24 = all_image(p)
    image25 = apply_image(image24, [(11, 12)])
    image26 = apply_image(image25, [(1, 2)])
    for row in image25:
        need(row[0] == min(row) and row[12] == max(row), "outer extreme failure")
    for row in image26:
        need(list(row[:2]) == sorted(row)[:2] and row[12] == max(row), "two-low extreme failure")
    middle11, middle10 = target(image25, 1, 12), target(image26, 2, 12)
    need(middle11["size"] == 143, "not the 143-state target")
    for target_data, control_name in ((middle11, "middle11_upper21"), (middle10, "middle10_upper20")):
        n = target_data["n"]
        control = fixture[control_name]
        need(len(control) == n + 10 and all(0 <= a < b < n for a, b in control), "invalid positive control")
        for x in target_data["image"]:
            row = [(x >> i) & 1 for i in range(n)]
            need(simulation(row, control) == sorted(row), "residual positive control fails")
    need(all(list(row) == sorted(row) for row in all_image(gates)), "native46 full control fails")
    normalized = p + [[11, 12], [1, 2]] + [[a + 2, b + 2] for a, b in fixture["middle10_upper20"]]
    need(all(list(row) == sorted(row) for row in all_image(normalized)), "normalized46 full control fails")
    cover = complete_merge_cover()
    cases = []
    # Lexical layer order is independently recovered from the complete DFS.
    for number, canonical in enumerate(sorted(cover)):
        kernel = [list(pair) for pair in canonical]
        continued = {name: extend(rows, kernel, 26) for name, rows in data26.items()}
        snap = summary(continued)
        bound = max(item["lower_bound"] for item in snap["anchors"].values())
        witness = None
        if bound > 44:
            witness = next(record for record, _ in sorted(continued["two_maxima"])
                           if record[4] + record[5] >= 10)
        image32 = apply_image(image26, kernel)
        for row in image32:
            need(list(row[:2]) == sorted(row)[:2] and list(row[11:]) == sorted(row)[11:], "fixed extreme pair failure")
        cases.append({"id": number, "kernel": kernel, "snapshot": snap,
                      "target": target(image32, 2, 11), "excluded_at_44": bound > 44,
                      "two_maximum_exclusion_record": witness})
    remaining = [case["id"] for case in cases if not case["excluded_at_44"]]
    need(len(remaining) == 39, "not 39 remaining branches")
    need(len({tuple(case["target"]["image"]) for case in cases}) == 45, "kernel images not distinct")
    return {"schema": "native24-kernel-cover-certificate-v1", "agent": "six-sorting-2", "role": "researcher",
            "native_gate_list_sha256": sha(gates), "budget": 44, "prefix_length": 24,
            "prefix24": p24, "prefix25": p25, "prefix26": p26,
            "middle11": middle11, "middle10": middle10,
            "kernel_count": len(cases), "kernels": cases, "remaining_ids": remaining}


def main():
    start = time.monotonic()
    fixture = json.loads((ROOT / "fixture.json").read_text())
    raw = (ROOT / "certificate.json").read_bytes()
    certificate = json.loads(raw)
    expected = rebuild(fixture)
    need(expected == certificate, "certificate differs from complete independent reconstruction")
    damaged = []
    bad = deepcopy(certificate); bad["middle11"]["image"].pop(); damaged.append(bad)
    bad = deepcopy(certificate); bad["kernels"].pop(); damaged.append(bad)
    bad = deepcopy(certificate); bad["prefix24"]["anchors"]["low"]["rows"][0]["label"] -= 1; damaged.append(bad)
    need(all(expected != bad for bad in damaged), "a certificate corruption passed")
    print(json.dumps({"status": "ALL_NATIVE24_CHECKS_PASSED", "agent": "six-sorting-2", "role": "researcher",
                      "kernels": 45, "remaining_targets": 39, "corruptions_rejected": len(damaged),
                      "certificate_sha256": hashlib.sha256(raw).hexdigest(),
                      "seconds": round(time.monotonic() - start, 3),
                      "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      **METRICS}, sort_keys=True))


if __name__ == "__main__":
    main()

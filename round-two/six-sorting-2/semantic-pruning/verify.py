"""Independent scalar checker; imports no producer or profile code."""

from copy import deepcopy
import hashlib
from itertools import product
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parent
FAMILIES = (("one_minimum", 1, 0), ("one_maximum", 0, 1),
            ("two_minima", 2, 0), ("two_maxima", 0, 2), ("mixed_pair", 1, 1))
SIZES = (0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39)


def need(test, message):
    if not test:
        raise ValueError(message)


def positions(values):
    low = high = 0
    for i, value in enumerate(values):
        if value < 0:
            low |= 1 << i
        elif value > 1:
            high |= 1 << i
    return low, high


def scalar_summary(rows):
    buckets = {}
    for row in rows:
        buckets.setdefault((row[2], row[3]), []).append((row[4], row[4] + row[5]))
    envelope = []
    for lo, hi in sorted(buckets):
        costs = buckets[lo, hi]
        envelope.append([lo, hi, max(x[0] for x in costs), max(x[1] for x in costs)])
    summary = {"ordinary_mass": sum(2 ** x[2] for x in envelope),
               "semantic_mass": sum(2 ** x[3] for x in envelope),
               "maximum_deletions": max(x[4] for x in rows),
               "maximum_semantic_deletions": max(x[4] + x[5] for x in rows),
               "maximum_redundancies": max(x[5] for x in rows),
               "port_classes": len(envelope)}
    return summary, envelope


def scalar_family(n, gates, low_count, high_count):
    low_masks = [s for s in range(1 << n) if s.bit_count() == low_count]
    high_masks = [s for s in range(1 << n) if s.bit_count() == high_count]
    histories = [[] for _ in range(len(gates) + 1)]
    assignments = evaluations = 0
    for lm in low_masks:
        for hm in high_masks:
            if lm & hm:
                continue
            lows = [i for i in range(n) if (lm >> i) & 1]
            highs = [i for i in range(n) if (hm >> i) & 1]
            free = [i for i in range(n) if not ((lm | hm) >> i) & 1]
            template = [0] * n
            for j, i in enumerate(lows):
                template[i] = j - len(lows)
            for j, i in enumerate(highs):
                template[i] = 2 + j

            # Only the extreme trajectory is taken from the all-zero middle row.
            # Every free assignment separately checks that same deletion trace.
            reference = template.copy()
            port_history = [positions(reference)]
            touched = 0
            for j, (a, b) in enumerate(gates):
                x, y = reference[a], reference[b]
                if x < 0 or x > 1 or y < 0 or y > 1:
                    touched |= 1 << j
                if x > y:
                    reference[a], reference[b] = y, x
                port_history.append(positions(reference))

            active = 0
            for assignment in range(1 << len(free)):
                values = template.copy()
                for j, i in enumerate(free):
                    values[i] = (assignment >> j) & 1
                for j, (a, b) in enumerate(gates):
                    x, y = values[a], values[b]
                    hit = x < 0 or x > 1 or y < 0 or y > 1
                    need(hit == bool((touched >> j) & 1), "marker trace depends on free values")
                    if x > y:
                        if not hit:
                            active |= 1 << j
                        values[a], values[b] = y, x
                need(positions(values) == port_history[-1], "incorrect extreme output ports")
                assignments += 1
                evaluations += len(gates)

            d = r = redundant_mask = 0
            for cut, (lo, hi) in enumerate(port_history):
                histories[cut].append([lm, hm, lo, hi, d, r, redundant_mask])
                if cut != len(gates):
                    if (touched >> cut) & 1:
                        d += 1
                    elif not (active >> cut) & 1:
                        r += 1
                        redundant_mask |= 1 << cut

    for rows in histories:
        rows.sort()
    trace = [scalar_summary(rows)[0] for rows in histories]
    for a, b in zip(trace, trace[1:]):
        need(a["ordinary_mass"] <= b["ordinary_mass"], "ordinary monotonicity")
        need(a["semantic_mass"] <= b["semantic_mass"], "semantic monotonicity")
    summary, envelope = scalar_summary(histories[-1])
    return {"low_count": low_count, "high_count": high_count,
            "records": histories[-1], "envelope": envelope,
            "summary": summary, "trace": trace}, assignments, evaluations


def integral_log_ceiling(mass):
    exponent = 0
    while 2 ** exponent < mass:
        exponent += 1
    return exponent


def full_boolean_check(n, gates, sorting):
    witnesses = [None] * len(gates)
    for x in range(1 << n):
        values = [(x >> i) & 1 for i in range(n)]
        for j, (a, b) in enumerate(gates):
            if values[a] > values[b]:
                if witnesses[j] is None:
                    witnesses[j] = x
                values[a], values[b] = values[b], values[a]
        if sorting:
            need(values == sorted(values), "positive sorting control fails")
    return witnesses


def local_fibres():
    tested = 0
    for n in range(2, 7):
        for a in range(n):
            for b in range(a + 1, n):
                fibres = {}
                for word in product(range(3), repeat=n):
                    image = list(word)
                    image[a], image[b] = min(word[a], word[b]), max(word[a], word[b])
                    charged = word[a] != 1 or word[b] != 1
                    fibres.setdefault(tuple(image), []).append(charged)
                    tested += 1
                for charges in fibres.values():
                    need(len(charges) in (1, 2), "marker fibre has too many preimages")
                    if len(charges) == 2:
                        need(all(charges), "double fibre has an uncharged input")
    return tested


def same(expected, candidate):
    need(expected == candidate, "certificate differs from complete scalar reconstruction")


def main():
    start = time.monotonic()
    fixture = json.loads((ROOT / "fixture.json").read_text())
    raw = (ROOT / "certificate.json").read_bytes()
    certificate = json.loads(raw)
    expected = {"schema": "sorting-extreme-semantic-pruning-v1",
                "agent": "six-sorting-2", "role": "researcher",
                "record_fields": ["input_low_mask", "input_high_mask", "output_low_mask",
                                  "output_high_mask", "D", "R", "redundant_gate_mask"],
                "cases": {}}
    total_assignments = total_evaluations = 0
    for name in ("prefix", "incumbent", "small_sorter", "small_duplicate"):
        n = fixture["n"] if name in ("prefix", "incumbent") else 4
        gates = fixture[name]
        need(2 <= n <= 13, "invalid order")
        for gate in gates:
            need(len(gate) == 2 and 0 <= gate[0] < gate[1] < n, "invalid standard gate")
        data = {}
        bounds = []
        for family, lo, hi in FAMILIES:
            result, assignments, evaluations = scalar_family(n, gates, lo, hi)
            data[family] = result
            total_assignments += assignments
            total_evaluations += evaluations
            k = n - lo - hi
            bounds.append(SIZES[k] + integral_log_ceiling(result["summary"]["semantic_mass"]))
        expected["cases"][name] = {"n": n, "size": len(gates), "families": data,
                                    "lower_bound": max(bounds)}
        if name != "prefix":
            full_boolean_check(n, gates, sorting=True)
            need(max(bounds) <= len(gates), "valid control rejected by the necessary bound")
    activity = full_boolean_check(13, fixture["prefix"], sorting=False)
    need(all(x is not None for x in activity), "globally redundant witness gate")
    expected["prefix_activity_witnesses"] = activity
    same(expected, certificate)

    prefix = expected["cases"]["prefix"]
    mixed = prefix["families"]["mixed_pair"]
    need(mixed["summary"]["ordinary_mass"] == 388, "ordinary mass is not 388")
    need(mixed["summary"]["semantic_mass"] == 524, "semantic mass is not 524")
    need(prefix["lower_bound"] == 45, "lower bound is not 45")
    for name, _, _ in FAMILIES:
        cap = 32 if name in ("one_minimum", "one_maximum") else 512
        need(prefix["families"][name]["summary"]["ordinary_mass"] <= cap,
             "witness already fails an ordinary profile bound")
    for row in mixed["records"]:
        low = row[0].bit_length() - 1
        high = row[1].bit_length() - 1
        redundant = high in (0, 1, 8) and low not in (6, 10)
        need(row[5] == int(redundant), "analytic redundancy characterization differs")
        need(row[6] == ((1 << 10) if redundant else 0), "redundant gate is not gate eleven")
    need(sum(x[5] for x in mixed["records"]) == 30, "not thirty mixed redundancies")

    # Compare complete entry sets and check that corrupted summaries/records fail.
    corruptions = []
    bad = deepcopy(certificate)
    bad["cases"]["prefix"]["families"]["mixed_pair"]["records"].pop()
    corruptions.append(bad)
    bad = deepcopy(certificate)
    bad["cases"]["prefix"]["families"]["mixed_pair"]["summary"]["semantic_mass"] = 512
    corruptions.append(bad)
    bad = deepcopy(certificate)
    bad["cases"]["prefix"]["lower_bound"] = 44
    corruptions.append(bad)
    for bad in corruptions:
        try:
            same(expected, bad)
        except ValueError:
            pass
        else:
            raise ValueError("corrupt certificate accepted")
    local_tests = local_fibres()
    print(json.dumps({"status": "ALL_INDEPENDENT_CHECKS_PASSED",
                      "agent": "six-sorting-2", "role": "researcher",
                      "python": sys.version.split()[0],
                      "scalar_free_assignments": total_assignments,
                      "scalar_gate_evaluations": total_evaluations,
                      "ternary_marker_transitions": local_tests,
                      "rejected_corruptions": len(corruptions),
                      "ordinary_mixed_mass": 388, "semantic_mixed_mass": 524,
                      "full_sorter_size_lower_bound": 45,
                      "certificate_sha256": hashlib.sha256(raw).hexdigest(),
                      "seconds": round(time.monotonic() - start, 3),
                      "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
                     sort_keys=True))


if __name__ == "__main__":
    main()

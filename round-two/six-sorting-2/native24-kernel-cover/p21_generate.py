"""Packed-column source certificate for the native P21 exclusion.

Only the ordinary touch count D is used by the new argument. Complete
original-domain D/R records are retained to permit entry-by-entry replay.
"""
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
PINS = {'fixture.json': '93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6', 'generate.py': '08a37678a11392ed46907ab30b2463d841e3e068764c09e410244490f2212381', 'p21-fixture.json': '7ab864ef0ab30eaae1c891a5b2a3b3cd2794293cd7e48493f1a4f5dd1d3022ba'}


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def read_inputs():
    for name, pin in PINS.items():
        need(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == pin,
             "dependency changed: " + name)
    return (json.loads((ROOT / "fixture.json").read_text())["gates"],
            json.loads((ROOT / "p21-fixture.json").read_text()))


def load_columns():
    spec = importlib.util.spec_from_file_location("p21_published_columns", ROOT / "generate.py")
    columns = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(columns)
    return columns.semantic


def ordinary(records):
    entries = sorted(r[:5] for r in records)
    classes = {}
    for row in entries:
        tag = tuple(row[2:4])
        classes[tag] = max(classes.get(tag, -1), row[4])
    return {"records_sha256": digest(entries),
            "envelope": [[*tag, d] for tag, d in sorted(classes.items())],
            "mass": sum(2 ** d for d in classes.values())}


def step(envelope, gate):
    a, b = gate
    bit_a, bit_b = 2 ** a, 2 ** b
    def swap(mask):
        return mask ^ (bit_a | bit_b) if bool(mask & bit_a) != bool(mask & bit_b) else mask
    out = {}
    for low, high, d in envelope:
        hit = bool((low | high) & (bit_a | bit_b))
        rank_a = -1 if low & bit_a else 1 if high & bit_a else 0
        rank_b = -1 if low & bit_b else 1 if high & bit_b else 0
        if rank_a > rank_b:
            low, high = swap(low), swap(high)
        tag = low, high
        out[tag] = max(out.get(tag, -1), d + hit)
    return [[*tag, d] for tag, d in sorted(out.items())]


def through(envelope, word):
    for gate in word:
        envelope = step(envelope, gate)
    return envelope


def minimum_cover(stems):
    words = sorted(word for stem in stems.values() for word in
                   [stem, [stem[1], stem[0], stem[2]]])
    states = set()
    for word in words:
        live = {i: 7 for i in range(1, 5)}
        states.add(tuple(sorted(live.items())))
        for a, b in word:
            need(live[a] == live[b], "unequal minimum merge")
            live[a] += 1
            del live[b]
            states.add(tuple(sorted(live.items())))
    return {"event_words": words, "canonical_stems": list(stems.values()),
            "equality_states": [list(map(list, z)) for z in sorted(states)]}


def high_cover():
    words = [[[9, 11], [11, 12]]]
    for r in [2, 3, 4, 5, 6, 7, 8, 10]:
        words.append([[min(r, 9), max(r, 9)], [max(r, 9), 11], [11, 12]])
    return {"route_ports": [9, 11, 12], "touch_budgets": [3, 2, 1],
            "event_words": sorted(words), "direct_branch_uses_native_P22": True}


def finite_controls():
    baseline = [[0, 1536, 4], [0, 2560, 4], [0, 4608, 5]]
    terminals, overflows, shadows = [], [], []
    for r in [2, 3, 4, 5, 6, 7, 8, 10]:
        word = [[min(r, 9), max(r, 9)], [max(r, 9), 11], [11, 12]]
        terminal = through(baseline, word)
        terminals.append({"r": r, "envelope": terminal,
                          "mass": sum(2 ** row[2] for row in terminal)})
        for a in range(2, 9):
            out = through(step(baseline, [a, 10]), word)
            overflows.append({"r": r, "preparation": [a, 10], "envelope": out,
                              "mass": sum(2 ** row[2] for row in out)})
        for q in range(5, 9):
            out = through([[0, 2 ** q + 4096, 5]], word)
            shadows.append({"r": r, "q": q, "envelope": out})
    return {"baseline_terminals": terminals, "preparation10_overflows": overflows,
            "shadow_suffixes": shadows, "selected_shadow_initial_mass": 96,
            "all_merged_cost_lower_bound": 7, "terminal_cost_lower_bound": 10,
            "ordinary_mass_ceiling": 512}


def build():
    native, fixture = read_inputs()
    s = load_columns()
    cases = []
    for name, stem in [("initial", [])] + list(fixture["minimum_stems"].items()):
        gates = native[:21] + stem
        families = {}
        for family_name, l, h in [("two_minima", 2, 0), ("two_maxima", 0, 2)]:
            data = s.analyze_family(13, gates, l, h)
            rows = data["records"]
            families[family_name] = {"low_count": l, "high_count": h,
                                     "records": rows, "records_sha256": digest(rows),
                                     "ordinary": ordinary(rows)}
        unary = []
        for p in range(13):
            values = [0] * 13
            values[p] = s.HIGH
            touches = 0
            for gate in gates:
                deletion, _ = s.transition(values, *gate)
                touches += deletion
            unary.append([p, values.index(s.HIGH), touches])
        high = families["two_maxima"]["ordinary"]["envelope"]
        anchors = [[p, sum(2 ** d for lo, hi, d in high if hi >> p & 1)]
                   for p in sorted({row[1] for row in unary})]
        selected = []
        if name != "initial":
            rows = {row[1]: row for row in families["two_maxima"]["records"]}
            selected = [rows[mask] for mask in fixture["selected_original_high_masks"]]
        cases.append({"name": name, "prefix_length": len(gates),
                      "prefix_sha256": digest(gates), "minimum_stem": stem,
                      "families": families, "unary_high_routes": unary,
                      "ordinary_high_anchors": anchors, "selected_records": selected})
    columns = list(s.truth_columns(13))
    for a, b in native:
        columns[a], columns[b] = columns[a] & columns[b], columns[a] | columns[b]
    outputs = sorted({sum(((c >> x) & 1) << p for p, c in enumerate(columns))
                      for x in range(8192)})
    need(outputs == [8192 - 2 ** (13 - w) for w in range(14)],
         "known native46 word fails a Boolean input")
    return {"schema": "native21-six-history-exclusion-certificate-v1",
            "agent": "six-sorting-2", "role": "researcher", "n": 13,
            "size_budget": 44, "small_size_lower_bound": 35, "prefix_length": 21,
            "parent_files_sha256": PINS, "cases": cases,
            "minimum_cover": minimum_cover(fixture["minimum_stems"]),
            "high_cover": high_cover(), "finite_controls": finite_controls(),
            "known_native46": {"gate_list_sha256": digest(native),
                               "boolean_inputs": 8192, "sorted_outputs": outputs},
            "native_prefix_total_interval": [45, 46],
            "native_prefix_suffix_interval": [24, 25]}


def main():
    start = time.monotonic()
    certificate = build()
    path = ROOT / "p21-certificate.json"
    path.write_text(json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({"status": "NATIVE21_COLUMN_CERTIFICATE_REGENERATED",
                      "agent": "six-sorting-2", "role": "researcher",
                      "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "bytes": path.stat().st_size, "seconds": time.monotonic() - start,
                      "maximum_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
                     sort_keys=True))


if __name__ == "__main__":
    main()

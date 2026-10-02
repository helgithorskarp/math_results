"""Exact mask/packed-column certificate for the weighted maximum reduction.

Actual author six-sorting-2, researcher. Ordinary marked-pair propagation
and packed columns credit this author's earlier p21_generate.py,
source dce3955b2880381edb2884b7446d282bf7bdeda5. No solver is used.
"""
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(",", ":")).encode()).hexdigest()


def pair_step(mask, d, gate, high=True):
    a, b = gate
    x, y = 1 << a, 1 << b
    touched = bool(mask & (x | y))
    move = bool(mask & x) and not mask & y if high else not mask & x and bool(mask & y)
    if move:
        mask ^= x | y
    return mask, d + touched


def through(records, gates, high=True):
    out = []
    for mask, d in records:
        for gate in gates:
            mask, d = pair_step(mask, d, gate, high)
        out.append([mask, d])
    classes = {}
    for mask, d in out:
        classes[mask] = max(classes.get(mask, -1), d)
    return [[m, classes[m]] for m in sorted(classes)]


def mass(envelope):
    return sum(1 << d for _, d in envelope)


def pairs(gates, high):
    records = []
    for a, b in combinations(range(13), 2):
        original = (1 << a) | (1 << b)
        m, d = original, 0
        for gate in gates:
            m, d = pair_step(m, d, gate, high)
        records.append([original, m, d])
    records.sort()
    envelope = through([[r[1], r[2]] for r in records], [])
    return {"records": records, "envelope": envelope, "mass": mass(envelope)}


def unary(gates, high=True):
    result = []
    for p in range(13):
        m, d = 1 << p, 0
        for gate in gates:
            m, d = pair_step(m, d, gate, high)
        result.append([p, m.bit_length() - 1, d])
    return result


def packed_histogram(gates):
    columns = [sum(1 << x for x in range(8192) if x >> p & 1) for p in range(13)]
    for a, b in gates:
        columns[a], columns[b] = columns[a] & columns[b], columns[a] | columns[b]
    counts = Counter(sum(((columns[p] >> x) & 1) << p for p in range(13))
                     for x in range(8192))
    return [[x, counts[x]] for x in sorted(counts)]


def singleton_word(r):
    return [[min(r, 9), max(r, 9)], [max(r, 9), 11], [11, 12]]


def generic_controls():
    baseline = [[1536, 4], [2560, 4], [4608, 5]]
    terminals, overflows, shadows, coalesced, boundary = [], [], [], [], []
    partners = list(range(9)) + [10]
    for r in partners:
        word = singleton_word(r)
        z = through(baseline, word)
        terminals.append([r, z, mass(z)])
        for a in range(9):
            z = through(through(baseline, [[a, 10]]), word)
            overflows.append([r, a, z, mass(z)])
        for q in range(9):
            z = through([[(1 << q) | 4096, 0]], word)
            shadows.append([r, q, z[0][0], z[0][1]])
        if r < 9:
            for d, target in [(6, coalesced), (5, boundary)]:
                z = through(baseline + [[(1 << r) | 4096, d]], word)
                target.append([r, z, mass(z)])
    closures = []
    for q in range(9):
        for gate in combinations(range(9), 2):
            m, d = pair_step((1 << q) | 4096, 0, gate)
            closures.append([q, list(gate), m, d])
    return {"baseline_terminals": terminals,
            "stationary10_overflows": overflows,
            "shadow_terminals": shadows,
            "coalesced_shadow_d6": coalesced,
            "threshold_boundary_d5": boundary,
            "shadow_closure_count": len(closures),
            "shadow_closure_sha256": digest(closures),
            "ordinary_mass_ceiling": 512,
            "strict_shadow_threshold": 32}


def build():
    f = json.loads((ROOT / "fixture.json").read_text())
    p = f["prefix19"]
    cases = []
    for name, gates in [("N19", p), ("H21", p + f["maximum_word"])]:
        low, high = pairs(gates, False), pairs(gates, True)
        routes = unary(gates)
        anchors = [[q, sum(1 << d for m, d in high["envelope"] if m >> q & 1)]
                   for q in sorted({r[1] for r in routes})]
        cases.append({"name": name, "gates": gates, "LOW": low, "HIGH": high,
                      "unary_low": unary(gates, False), "unary_high": routes,
                      "high_anchors": anchors, "Boolean_histogram": packed_histogram(gates)})
    histogram = Counter()
    for row, multiplicity in cases[1]["Boolean_histogram"]:
        histogram[(row >> 1) & 2047] += multiplicity
    target = sorted(histogram)
    native = f["native46_control"]
    normalized = p + f["maximum_word"] + [g for i, g in enumerate(native[19:], 19)
                                           if i not in (21, 27)]
    core_control = [[a - 1, b - 1] for a, b in normalized[21:]]
    baseline = {r[0]: r for r in cases[0]["HIGH"]["records"]}
    shadows = [baseline[m] for m in f["shadow_original_high_masks"]]
    shadow_mass = mass(through([[r[1], r[2]] for r in shadows], []))
    return {"schema": "weighted-max-native19-certificate-v1",
            "agent": "six-sorting-2", "role": "researcher",
            "size_budget": 44, "imported_size11_lower_bound": 35,
            "cases": cases,
            "maximum_event_words": sorted([f["maximum_word"]] +
                                           [singleton_word(r) for r in list(range(9)) + [10]]),
            "generic_controls": generic_controls(),
            "selected_N19_baseline": [baseline[m] for m in f["baseline_original_high_masks"]],
            "selected_N19_shadows": shadows,
            "selected_shadow_mass": shadow_mass,
            "H21_core": {"physical_ports": list(range(1, 12)),
                         "state_bit_j_is_physical_port": "j+1",
                         "states": target, "states_sha256": digest(target),
                         "original_input_multiplicities": [[x, histogram[x]] for x in target],
                         "completion_interval": [23, 25],
                         "size44_gate_budget": 23, "known25_control": core_control},
            "normalized46_control": normalized}


def main():
    started = time.monotonic()
    cert = build()
    (ROOT / "certificate.json").write_text(json.dumps(cert, separators=(",", ":")) + "\n")
    print(json.dumps({"status": "WEIGHTED_MAX_NATIVE19_CERTIFICATE_GENERATED",
                      "certificate_sha256": hashlib.sha256((ROOT / "certificate.json").read_bytes()).hexdigest(),
                      "core_state_count": len(cert["H21_core"]["states"]),
                      "core_states_sha256": cert["H21_core"]["states_sha256"],
                      "seconds": time.monotonic() - started,
                      "maximum_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == "__main__":
    main()

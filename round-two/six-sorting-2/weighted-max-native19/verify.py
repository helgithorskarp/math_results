"""Standalone scalar verifier; imports no producer or sibling research code.

Actual author six-sorting-2, researcher. Numeric original-cube primitives
credit p21_verify.py, source dce3955b2880381edb2884b7446d282bf7bdeda5.
Full route cover is budget DFS, not the producer's explicit word list.
Same-author algorithmic independence is not an external review verdict.
"""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
METRICS = {}
PREFIX19 = [[0,11],[1,7],[2,4],[3,5],[8,9],[10,12],
            [0,2],[3,6],[4,12],[5,7],[8,10],[0,8],[1,3],
            [2,5],[4,9],[6,11],[7,12],[0,1],[2,10]]
MAXIMUM = [[9,11],[11,12]]


def need(test, message):
    if not test:
        raise ValueError(message)


def count(name, amount=1):
    METRICS[name] = METRICS.get(name, 0) + amount


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(",", ":")).encode()).hexdigest()


def marked(value):
    return value < 0 or value > 1


def marked_mask(row):
    return sum(1 << i for i, v in enumerate(row) if marked(v))


def simulate(row, gates):
    values = list(row)
    for a, b in gates:
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values


def fixture_definition(f):
    need(set(f) == {"schema", "n", "size_budget", "imported_size11_lower_bound",
                    "prefix19", "native46_control", "maximum_word",
                    "baseline_original_high_masks", "shadow_original_high_masks"},
         "fixture fields differ")
    need(f["schema"] == "weighted-max-native19-inputs-v1" and f["n"] == 13
         and f["size_budget"] == 44 and f["imported_size11_lower_bound"] == 35,
         "fixture scope differs")
    need(f["prefix19"] == PREFIX19 and f["maximum_word"] == MAXIMUM,
         "literal native N19 or maximum word differs")
    need(f["baseline_original_high_masks"] == [768,2560,4608]
         and f["shadow_original_high_masks"] == [160,4224],
         "original selected family differs")
    native = f["native46_control"]
    need(len(native) == 46 and native[:19] == PREFIX19, "native46 prefix differs")
    need(all(len(g) == 2 and all(type(p) is int for p in g)
             and 0 <= g[0] < g[1] < 13 for g in native), "invalid native gate")


def template(original, high):
    positions = [p for p in range(13) if original >> p & 1]
    row = [0] * 13
    for j, p in enumerate(positions):
        row[p] = j + 2 if high else j - len(positions)
    free = [p for p in range(13) if p not in positions]
    return row, free


def original_record(gates, original, high):
    initial, free = template(original, high)
    common_touch = common_final = None
    for assignment in range(1 << len(free)):
        row = list(initial)
        for j, p in enumerate(free):
            row[p] = assignment >> j & 1
        touches = 0
        for t, (a, b) in enumerate(gates):
            if marked(row[a]) or marked(row[b]):
                touches |= 1 << t
            if row[a] > row[b]:
                row[a], row[b] = row[b], row[a]
        final = marked_mask(row)
        if common_touch is None:
            common_touch, common_final = touches, final
        need(touches == common_touch and final == common_final,
             "marked path depends on original free assignment")
        count("original_free_assignments")
        count("original_prefix_gate_evaluations", len(gates))
    count("original_pair_domains")
    return [original, common_final, common_touch.bit_count()]


def envelope(records):
    grouped = {}
    for _, mask, d in records:
        grouped.setdefault(mask, []).append(d)
    return [[m, max(grouped[m])] for m in sorted(grouped)]


def weight(z):
    return sum(2 ** d for _, d in z)


def family(gates, high):
    masks = sorted((1 << a) | (1 << b) for a, b in combinations(range(13), 2))
    records = [original_record(gates, m, high) for m in masks]
    z = envelope(records)
    return {"records": records, "envelope": z, "mass": weight(z)}


def unary(gates, high=True):
    result = []
    for p in range(13):
        row = [0] * 13
        row[p] = 2 if high else -1
        d = 0
        for a, b in gates:
            d += marked(row[a]) or marked(row[b])
            if row[a] > row[b]:
                row[a], row[b] = row[b], row[a]
        result.append([p, next(i for i, x in enumerate(row) if marked(x)), d])
        count("unary_routes")
    return result


def numeric_histogram(gates):
    h = Counter()
    for x in range(8192):
        row = simulate([x >> p & 1 for p in range(13)], gates)
        h[sum(v << p for p, v in enumerate(row))] += 1
        count("image_original_Boolean_inputs")
    return [[x, h[x]] for x in sorted(h)]


def numeric_passage(mask, d, gates, high=True):
    row, _ = template(mask, high)
    for a, b in gates:
        d += marked(row[a]) or marked(row[b])
        if row[a] > row[b]:
            row[a], row[b] = row[b], row[a]
    return marked_mask(row), d


def numeric_envelope(records, gates):
    rows = [[j, *numeric_passage(mask, d, gates)]
            for j, (mask, d) in enumerate(records)]
    return envelope(rows)


def fibre_anchor_audit():
    for high in [False, True]:
        for gate in combinations(range(13), 2):
            mapping, fibres = {}, {}
            for a, b in combinations(range(13), 2):
                old = (1 << a) | (1 << b)
                new, touch = numeric_passage(old, 0, [gate], high)
                mapping[old] = new, touch
                fibres.setdefault(new, []).append((old, touch))
                count("pair_gate_controls")
            for old_rows in fibres.values():
                need(len(old_rows) <= 2, "ordinary fibre exceeds two")
                if len(old_rows) == 2:
                    need(all(touch == 1 for _, touch in old_rows),
                         "ordinary double fibre is not charged")
                count("ordinary_fibres")
            for p in range(13):
                row = [0] * 13
                row[p] = 2 if high else -1
                out = simulate(row, [gate])
                target = next(j for j, x in enumerate(out) if marked(x))
                restricted = [(new, touch) for old, (new, touch) in mapping.items()
                              if old >> p & 1]
                if p in gate:
                    need(len({m for m, _ in restricted}) == len(restricted),
                         "touched anchor map not injective")
                    need(all(t == 1 and m >> target & 1 for m, t in restricted),
                         "touched anchor not charged/preserved")
                else:
                    need(all(bool(old >> p & 1) == bool(new >> p & 1)
                             for old, (new, _) in mapping.items()),
                         "untouched anchor membership changes")
                count("anchor_gate_controls")


def budget_route_cover():
    limits = (3, 2, 1)

    @lru_cache(None)
    def visit(positions, used):
        accepted = set()
        count("budget_route_states")
        for gate in combinations(range(13), 2):
            count("budget_next_gate_controls")
            if not any(p in gate for p in positions):
                continue  # Arbitrary non-events do not change this route state.
            target, charges = [], []
            for p in positions:
                row = [0] * 13
                row[p] = 2
                charges.append(int(marked(row[gate[0]]) or marked(row[gate[1]])))
                row = simulate(row, [gate])
                target.append(row.index(2))
            next_used = tuple(u + c for u, c in zip(used, charges))
            if any(u > cap for u, cap in zip(next_used, limits)):
                continue
            need(positions != (12,12,12), "terminal route admits another event")
            for suffix in visit(tuple(target), next_used):
                accepted.add((gate,) + suffix)
        if positions == (12,12,12):
            accepted.add(())
        return tuple(sorted(accepted))

    words = [[list(g) for g in w] for w in visit((9,11,12), (0,0,0))]
    need(len(words) == 11, "unexpected complete high-event cover")
    return sorted(words)


def generic_controls(words):
    baseline = [[1536,4],[2560,4],[4608,5]]
    terminals, overflows, shadows, coalesced, boundary = [], [], [], [], []
    singleton_words = {}
    for word in words:
        if len(word) == 2:
            need(word == MAXIMUM, "unexpected direct high-event word")
            continue
        need(len(word) == 3 and 9 in word[0], "unexpected singleton high-event word")
        r = next(p for p in word[0] if p != 9)
        singleton_words[r] = word
    need(sorted(singleton_words) == list(range(9)) + [10], "singleton partners incomplete")
    for r, word in sorted(singleton_words.items()):
        z = numeric_envelope(baseline, word)
        need(z == [[4608,7],[5120,7],[6144,8]] and weight(z) == 512,
             "singleton baseline terminals do not saturate")
        terminals.append([r, z, weight(z)])
        for a in range(9):
            z = numeric_envelope(baseline, [[a,10]] + word)
            need(weight(z) == 640, "stationary10 touch does not overflow")
            overflows.append([r, a, z, weight(z)])
        for q in range(9):
            mask, d = numeric_passage((1 << q) | 4096, 0, word)
            need((mask, d) == ((6144,3) if q == r else ((1 << q) | 4096,1)),
                 "shadow alternative differs")
            shadows.append([r,q,mask,d])
        if r < 9:
            for d, target, expected in [(6,coalesced,768), (5,boundary,512)]:
                z = numeric_envelope(baseline + [[(1 << r) | 4096,d]], word)
                need(weight(z) == expected, "weighted-shadow/boundary mass differs")
                target.append([r,z,weight(z)])
    closures = []
    for q in range(9):
        for gate in combinations(range(9),2):
            m, d = numeric_passage((1 << q) | 4096,0,[gate])
            need(m >> 12 & 1 and (m ^ 4096).bit_length() <= 9,
                 "shadow escapes ports0..8")
            closures.append([q,list(gate),m,d])
    return {"baseline_terminals":terminals, "stationary10_overflows":overflows,
            "shadow_terminals":shadows, "coalesced_shadow_d6":coalesced,
            "threshold_boundary_d5":boundary, "shadow_closure_count":len(closures),
            "shadow_closure_sha256":digest(closures),
            "ordinary_mass_ceiling":512, "strict_shadow_threshold":32}


def normalized_control(f):
    word = deepcopy(f["native46_control"])
    for position, gate in [(19,[9,11]),(20,[11,12])]:
        index = word.index(gate, position)
        while index > position:
            need(not set(word[index-1]) & set(word[index]),
                 "control normalization crosses an intersecting gate")
            word[index-1],word[index] = word[index],word[index-1]
            index -= 1
            count("control_disjoint_adjacent_swaps")
    need(word[:21] == PREFIX19 + MAXIMUM, "wrong normalized control prefix")
    for x in range(8192):
        row = [x >> p & 1 for p in range(13)]
        need(simulate(row,f["native46_control"]) == simulate(row,word) == sorted(row),
             "native/normalized46 control fails")
        count("control_original_Boolean_inputs")
    core = [[a-1,b-1] for a,b in word[21:]]
    need(len(core) == 25 and all(0 <= a < b < 11 for a,b in core),
         "normalized upper control not eleven-wire25")
    return word,core


def reconstruct(f):
    fixture_definition(f)
    fibre_anchor_audit()
    words = budget_route_cover()
    controls = generic_controls(words)
    cases = []
    for name,gates in [("N19",PREFIX19),("H21",PREFIX19+MAXIMUM)]:
        low, high = family(gates,False),family(gates,True)
        routes = unary(gates)
        anchors = [[q,sum(2 ** d for m,d in high["envelope"] if m >> q & 1)]
                   for q in sorted({r[1] for r in routes})]
        hist = numeric_histogram(gates)
        cases.append({"name":name, "gates":gates, "LOW":low, "HIGH":high,
                      "unary_low":unary(gates,False), "unary_high":routes,
                      "high_anchors":anchors, "Boolean_histogram":hist})
    need(cases[0]["high_anchors"] == [[9,64],[11,72],[12,176]], "N19 anchors differ")
    capacities = []
    for p,m in cases[0]["high_anchors"]:
        e = 0
        while m * 2 ** (e+1) <= 512:
            e += 1
        capacities.append([p,e])
    need(capacities == [[9,3],[11,2],[12,1]], "N19 route budgets not3/2/1")
    for case in cases:
        need({r[1] for r in case["unary_low"]} == {0}, "N19/H21 minimum not held0")
        need(case["LOW"]["mass"] == 448, "LOW mass differs")
    need(cases[0]["HIGH"]["mass"] == 232 and cases[1]["HIGH"]["mass"] == 448,
         "HIGH masses differ")
    need({r[1] for r in cases[1]["unary_high"]} == {12}, "H21 maximum not held12")
    lookup = {r[0]:r for r in cases[0]["HIGH"]["records"]}
    baseline = [lookup[m] for m in f["baseline_original_high_masks"]]
    need([r[1] for r in baseline] == [1536,2560,4608]
         and all(r[2] >= d for r,d in zip(baseline,[4,4,5])),
         "N19 baseline hypotheses fail")
    shadows = [lookup[m] for m in f["shadow_original_high_masks"]]
    need(all(r[1] >> 12 & 1 and (r[1] ^ 4096).bit_length() <= 9 for r in shadows),
         "N19 shadow-port hypotheses fail")
    shadow_mass = weight(envelope([[j,r[1],r[2]] for j,r in enumerate(shadows)]))
    need(shadow_mass == 64 and shadow_mass > 32, "N19 weighted-shadow premise fails")
    target_counts = Counter()
    for x,c in cases[1]["Boolean_histogram"]:
        row = [x >> p & 1 for p in range(13)]
        need(row[0] == min(row) and row[12] == max(row), "H21 held extrema fail")
        target_counts[sum(row[p] << (p-1) for p in range(1,12))] += c
    target = sorted(target_counts)
    need(len(cases[0]["Boolean_histogram"]) == 269
         and len(cases[1]["Boolean_histogram"]) == 246 and len(target) == 244,
         "complete image sizes differ")
    need(digest(target) == "99cee56789817c69f6636ba7e247abb7144e47d61ef072405bfdf3ae9ce69f01",
         "exact244-state target differs")
    need(sum(target_counts.values()) == 8192, "target loses original inputs")
    for k in range(12):
        total = sum(c for x,c in target_counts.items() if x.bit_count() == k)
        expected = 14 if k in [0,11] else comb(13,k+1)
        need(total == expected, "target multiplicity by weight differs")
    word,core = normalized_control(f)
    for x in target:
        row = [x >> j & 1 for j in range(11)]
        need(simulate(row,core) == sorted(row), "25-gate core control fails")
        count("control_core_states")
    return {"schema":"weighted-max-native19-certificate-v1",
            "agent":"six-sorting-2", "role":"researcher",
            "size_budget":44, "imported_size11_lower_bound":35,
            "cases":cases, "maximum_event_words":words, "generic_controls":controls,
            "selected_N19_baseline":baseline, "selected_N19_shadows":shadows,
            "selected_shadow_mass":shadow_mass,
            "H21_core":{"physical_ports":list(range(1,12)),
                        "state_bit_j_is_physical_port":"j+1", "states":target,
                        "states_sha256":digest(target),
                        "original_input_multiplicities":[[x,target_counts[x]] for x in target],
                        "completion_interval":[23,25], "size44_gate_budget":23,
                        "known25_control":core}, "normalized46_control":word}


def validate_certificate(actual, expected):
    need(json.dumps(actual,separators=(",",":"),sort_keys=True) ==
         json.dumps(expected,separators=(",",":"),sort_keys=True),
         "complete certificate differs from scalar reconstruction")


def damage_controls(cert, f):
    damaged = []
    def add(label, change):
        c = deepcopy(cert)
        change(c)
        damaged.append((label,c))
    add("missing-original-domain",lambda c:c["cases"][0]["HIGH"]["records"].pop())
    add("shadow-cost",lambda c:c["selected_N19_shadows"][0].__setitem__(2,4))
    add("strict-shadow-threshold",lambda c:c["generic_controls"].__setitem__("strict_shadow_threshold",64))
    add("missing-event-word",lambda c:c["maximum_event_words"].pop())
    add("baseline-terminal",lambda c:c["generic_controls"]["baseline_terminals"][0][1][0].__setitem__(1,6))
    add("stationary10-overflow",lambda c:c["generic_controls"]["stationary10_overflows"][0].__setitem__(3,512))
    add("missing-core-state",lambda c:c["H21_core"]["states"].pop())
    add("multiplicity",lambda c:c["H21_core"]["original_input_multiplicities"][0].__setitem__(1,13))
    add("physical-port-order",lambda c:c["H21_core"].__setitem__("state_bit_j_is_physical_port","j"))
    add("gate-budget",lambda c:c["H21_core"].__setitem__("size44_gate_budget",24))
    for label,c in damaged:
        try:
            validate_certificate(c,cert)
        except ValueError:
            count("damaged_certificates_rejected")
        else:
            raise ValueError("damaged certificate accepted: " + label)
    for label,key,value in [("literal-prefix","prefix19",PREFIX19[:-1]),
                            ("original-family","shadow_original_high_masks",[160]),
                            ("maximum-word","maximum_word",[[9,12],[11,12]])]:
        bad = deepcopy(f)
        bad[key] = value
        try:
            fixture_definition(bad)
        except ValueError:
            count("damaged_fixtures_rejected")
        else:
            raise ValueError("damaged fixture accepted: " + label)


def main():
    started = time.monotonic()
    f = json.loads((ROOT / "fixture.json").read_text())
    actual = json.loads((ROOT / "certificate.json").read_text())
    expected = reconstruct(f)
    validate_certificate(actual,expected)
    damage_controls(expected,f)
    print(json.dumps({"status":"WEIGHTED_MAX_NATIVE19_SCALAR_CERTIFICATE_VERIFIED",
                      "certificate_sha256":hashlib.sha256((ROOT / "certificate.json").read_bytes()).hexdigest(),
                      "full_reconstructed_certificate_sha256":digest(expected),
                      "core_state_count":len(expected["H21_core"]["states"]),
                      "core_states_sha256":expected["H21_core"]["states_sha256"],
                      "metrics":METRICS, "seconds":time.monotonic()-started,
                      "maximum_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == "__main__":
    main()

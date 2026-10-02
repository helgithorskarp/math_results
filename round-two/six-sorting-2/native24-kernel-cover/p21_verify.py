"""Standalone scalar certificate checker for native P21.

No generator, profiler, sibling checker, solver or external package is imported.
Numeric primitives are copied from this author's published p22_verify.py
(source bc3d409028c7cfdc4e773717a1b73eadc6d19386). Algorithmic independence
from packed columns is same-author evidence, not an external review verdict.
"""
from copy import deepcopy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
PINS = {'fixture.json': '93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6', 'generate.py': '08a37678a11392ed46907ab30b2463d841e3e068764c09e410244490f2212381', 'p21-fixture.json': '7ab864ef0ab30eaae1c891a5b2a3b3cd2794293cd7e48493f1a4f5dd1d3022ba'}
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


def ceil_log(mass):
    need(mass > 0, "empty dyadic mass")
    e = 0
    while 2 ** e < mass:
        e += 1
    return e


def placements(n,l,h):
    for lows in combinations(range(n),l):
        other=[i for i in range(n) if i not in lows]
        for highs in combinations(other,h):
            yield sum(2**i for i in lows),sum(2**i for i in highs)


def ordinary(records):
    entries=sorted(r[:5] for r in records)
    groups={}
    for row in entries:
        z=tuple(row[2:4]);groups[z]=max(groups.get(z,-1),row[4])
    return {'records_sha256':digest(entries),
            'envelope':[[*z,d] for z,d in sorted(groups.items())],
            'mass':sum(2**d for d in groups.values())}


def ordinary_transition(envelope,gate):
    grouped={};a,b=gate
    for lo,hi,d in envelope:
        tags=[-1 if lo>>p&1 else 2 if hi>>p&1 else 0 for p in range(13)]
        hit=marked(tags[a]) or marked(tags[b])
        if tags[a]>tags[b]:tags[a],tags[b]=tags[b],tags[a]
        target=tuple(ports(tags));grouped.setdefault(target,[]).append((d+hit,hit))
    out=[]
    for z,fibre in sorted(grouped.items()):
        need(len(fibre)<=2,'marker fibre larger than two')
        if len(fibre)==2:need(all(hit for _,hit in fibre),'uncharged double fibre')
        out.append([*z,max(d for d,_ in fibre)])
    return out


def input_definition(fixture):
    expected = {"schema": "native21-six-history-fixture-v1", "n": 13,
                "size_budget": 44, "prefix_length": 21, "small_size_lower_bound": 35,
                "minimum_stems": {"A": [[1, 2], [3, 4], [1, 3]],
                                  "B": [[1, 3], [2, 4], [1, 2]],
                                  "C": [[1, 4], [2, 3], [1, 2]]},
                "selected_original_high_masks": [768, 2560, 4608, 160, 4224, 130]}
    need(json.dumps(fixture, sort_keys=True) == json.dumps(expected, sort_keys=True),
         "fixture definition differs")


def read_inputs():
    for name, pin in PINS.items():
        need(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == pin,
             "dependency changed: " + name)
    native = json.loads((ROOT / "fixture.json").read_text())["gates"]
    need(len(native) == 46 and all(type(a) == type(b) == int and 0 <= a < b < 13
                                  for a, b in native), "invalid native46 word")
    need(native[:21] == [[0, 11], [1, 7], [2, 4], [3, 5], [8, 9], [10, 12],
                         [0, 2], [3, 6], [4, 12], [5, 7], [8, 10], [0, 8],
                         [1, 3], [2, 5], [4, 9], [6, 11], [7, 12], [0, 1],
                         [2, 10], [3, 8], [4, 6]], "literal P21 differs")
    fixture = json.loads((ROOT / "p21-fixture.json").read_text())
    input_definition(fixture)
    return native, fixture


def minimum_cover():
    states, words, representatives = set(), [], set()

    def visit(live, word, nodes):
        key = tuple(sorted(live.items()))
        if key not in states:
            states.add(key)
            envelope = [[1 + 2 ** p, 0, d] for p, d in sorted(live.items())]
            need(sum(2 ** d for d in live.values()) == 512, "minimum not saturated")
            for gate in combinations(range(13), 2):
                out = ordinary_transition(envelope, gate)
                permitted = sum(2 ** row[2] for row in out) <= 512
                preparation = not set(gate) & ({0} | set(live))
                event = all(p in live for p in gate) and live[gate[0]] == live[gate[1]]
                need(permitted == (preparation or event), "minimum event rule incomplete")
                count("minimum_standard_state_transitions")
        if len(live) == 1:
            need(live == {1: 9}, "wrong minimum terminal")
            representative = tuple(pair for _, pair in sorted(nodes))
            representatives.add(representative)
            words.append(tuple(word))
            for bits in range(16):
                row = [0] * 13
                for j, p in enumerate(range(1, 5)):
                    row[p] = bits >> j & 1
                need(simulate(row, word) == simulate(row, representative),
                     "canonical event order changes comparator function")
                count("minimum_event_order_boolean_controls")
            return
        for a, b in combinations(sorted(live), 2):
            if live[a] != live[b]:
                continue
            next_live = dict(live)
            next_live[a] += 1
            del next_live[b]
            visit(next_live, word + [(a, b)], nodes + [(next_live[a], (a, b))])

    visit({i: 7 for i in range(1, 5)}, [], [])
    need((len(words), len(representatives), len(states)) == (6, 3, 10),
         "complete minimum counts differ")
    return {"event_words": [list(map(list, word)) for word in sorted(words)],
            "canonical_stems": [list(map(list, word)) for word in sorted(representatives)],
            "equality_states": [list(map(list, z)) for z in sorted(states)]}


def high_cover():
    # Route12 has only its final merge available. With three routes the
    # other two require two merges each; with two routes every path needs one.
    # This necessary merge-tree rule imposes no preparation-length bound.
    budgets = (3, 2, 1)

    def enumerate_words(frozen_ports, label):
        seen, words = set(), []

        def feasible(positions, used):
            groups = len(set(positions))
            additional = [0 if groups == 1 else 2 if groups == 3 and p != 12 else 1
                          for p in positions]
            return all(d + r <= b for d, r, b in zip(used, additional, budgets))

        def visit(positions, used, word):
            state = positions, used
            fresh = state not in seen
            seen.add(state)
            if positions == (12, 12, 12):
                words.append(tuple(word))
            for gate in combinations(range(13), 2):
                frozen = bool(set(gate) & frozen_ports)
                hit = [p in gate for p in positions]
                preparation = not any(hit)
                next_positions = tuple(gate[1] if h else p for p, h in zip(positions, hit))
                next_used = tuple(d + h for d, h in zip(used, hit))
                event = not frozen and any(hit) and feasible(next_positions, next_used)
                if fresh:
                    count(label + "_high_standard_state_transitions")
                if event:
                    need(sum(next_used) > sum(used), "route event did not charge")
                    visit(next_positions, next_used, word + [gate])
                if not frozen and preparation:
                    need(next_positions == positions and next_used == used,
                         "preparation changed a unary route")
        visit((9, 11, 12), (0, 0, 0), [])
        count(label + "_high_route_states", len(seen))
        return [list(map(list, word)) for word in sorted(words)]

    actual = enumerate_words(set(), "initial")
    normalized = enumerate_words({0, 1}, "normalized")
    expected = [[[9, 11], [11, 12]]] + [
        [[min(r, 9), max(r, 9)], [max(r, 9), 11], [11, 12]]
        for r in [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]]
    need(actual == sorted(expected), "complete initial high event cover differs")
    need(normalized == [word for word in sorted(expected)
                        if not any(set(gate) & {0, 1} for gate in word)],
         "post-minimum high event cover differs")
    return {"route_ports": [9, 11, 12], "touch_budgets": list(budgets),
            "event_words": actual, "after_minimum_event_words": normalized,
            "direct_branch_uses_native_P22": True}


def transport_controls():
    for side in ["low", "high"]:
        envelope = [[2 ** a + 2 ** b, 0, (a + b) % 7] if side == "low"
                    else [0, 2 ** a + 2 ** b, (a + b) % 7]
                    for a, b in combinations(range(13), 2)]
        for gate in combinations(range(13), 2):
            out = ordinary_transition(envelope, gate)
            need(sum(2 ** r[2] for r in out) >= sum(2 ** r[2] for r in envelope),
                 "ordinary transport decreased mass")
            count("ordinary_full_fibre_controls")
    for p in range(13):
        for gate in combinations(range(13), 2):
            sources = [[0, 2 ** p + 2 ** q, 0] for q in range(13) if q != p]
            targets = [ordinary_transition([row], gate)[0] for row in sources]
            route_hit = p in gate
            destination = gate[1] if route_hit else p
            need(all(row[1] >> destination & 1 for row in targets),
                 "anchored membership lost")
            if route_hit:
                need(len({row[1] for row in targets}) == 12 and
                     all(row[2] == 1 for row in targets),
                     "touched restricted anchor is not injective and charged")
            else:
                ordinary_transition(sources, gate)  # audits every double fibre
            count("anchored_pair_route_controls")


def finite_controls():
    baseline = [[0, 1536, 4], [0, 2560, 4], [0, 4608, 5]]
    terminals, overflows, shadows = [], [], []
    for r in [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]:
        word = [[min(r, 9), max(r, 9)], [max(r, 9), 11], [11, 12]]
        out = baseline
        for gate in word:
            out = ordinary_transition(out, gate)
        need(out == [[0, 4608, 7], [0, 5120, 7], [0, 6144, 8]],
             "baseline terminal classes/costs differ")
        terminals.append({"r": r, "envelope": out, "mass": 512})
        count("baseline_terminal_controls")
        for a in range(9):
            out = ordinary_transition(baseline, [a, 10])
            need(out == [[0, 1536, 5], [0, 2560, 4], [0, 4608, 5]],
                 "preparation10 is not a charged stationary touch")
            for gate in word:
                out = ordinary_transition(out, gate)
            need(sum(2 ** row[2] for row in out) == 640,
                 "preparation10 overflow differs")
            overflows.append({"r": r, "preparation": [a, 10],
                              "envelope": out, "mass": 640})
            count("preparation10_overflow_controls")
        for q in range(5, 9):
            out = [[0, 2 ** q + 4096, 5]]
            for gate in word:
                out = ordinary_transition(out, gate)
            target = [[0, 6144, 8]] if q == r else [[0, 2 ** q + 4096, 6]]
            need(out == target, "shadow suffix alternative differs")
            shadows.append({"r": r, "q": q, "envelope": out})
            count("shadow_suffix_controls")
    for q in range(5, 9):
        for gate in combinations(range(9), 2):
            out = ordinary_transition([[0, 2 ** q + 4096, 0]], gate)
            need(out[0][1] in {2 ** j + 4096 for j in range(5, 9)},
                 "nine-port shadow range not closed")
            count("nine_port_shadow_closure_controls")
    need(3 * 2 ** 5 == 96 and ceil_log(96) == 7 and 7 + 3 == 10 and 2 ** 10 > 512,
         "final shadow contradiction differs")
    return {"baseline_terminals": terminals, "preparation10_overflows": overflows,
            "shadow_suffixes": shadows, "selected_shadow_initial_mass": 96,
            "all_merged_cost_lower_bound": 7, "terminal_cost_lower_bound": 10,
            "ordinary_mass_ceiling": 512}


def build():
    native, fixture = read_inputs()
    cases = []
    for name, stem in [("initial", [])] + list(fixture["minimum_stems"].items()):
        gates = native[:21] + stem
        families = {}
        for family_name, l, h in [("two_minima", 2, 0), ("two_maxima", 0, 2)]:
            rows = sorted(family(13, gates, lo, hi, "original")
                          for lo, hi in placements(13, l, h))
            need(len(rows) == 78, "original pair family incomplete")
            families[family_name] = {"low_count": l, "high_count": h,
                                     "records": rows, "records_sha256": digest(rows),
                                     "ordinary": ordinary(rows)}
            count("original_pair_domains", len(rows))
        low = families["two_minima"]["ordinary"]
        expected_low = [[1 + 2 ** p, 0, 7] for p in range(1, 5)] if not stem else [[3, 0, 9]]
        need(low["envelope"] == expected_low and low["mass"] == 512,
             "minimum hypothesis differs")
        unary = []
        for p in range(13):
            values = [0] * 13
            values[p] = 2
            touches = 0
            for a, b in gates:
                touches += marked(values[a]) or marked(values[b])
                if values[a] > values[b]:
                    values[a], values[b] = values[b], values[a]
            unary.append([p, values.index(2), touches])
            count("unary_high_original_routes")
        need({row[1] for row in unary} == {9, 11, 12}, "unary high ports differ")
        high = families["two_maxima"]["ordinary"]["envelope"]
        anchors = [[p, sum(2 ** d for lo, hi, d in high if hi >> p & 1)]
                   for p in sorted({row[1] for row in unary})]
        need(anchors == [[9, 64], [11, 80], [12, 192]], "ordinary route anchor masses differ")
        need([max(t for t in range(10) if 2 ** t * mass <= 512) for p, mass in anchors]
             == [3, 2, 1], "route budgets differ")
        rows = {row[1]: row for row in families["two_maxima"]["records"]}
        selected = [rows[mask] for mask in fixture["selected_original_high_masks"]]
        need([row[2:5] for row in selected] == [[0, 1536, 4], [0, 2560, 4],
                                              [0, 4608, 5], [0, 4128, 5],
                                              [0, 4224, 5], [0, 4352, 5]],
             "six selected original histories differ")
        count("selected_original_histories", len(selected))
        cases.append({"name": name, "prefix_length": len(gates),
                      "prefix_sha256": digest(gates), "minimum_stem": stem,
                      "families": families, "unary_high_routes": unary,
                      "ordinary_high_anchors": anchors, "selected_records": selected})
    outputs = set()
    for x in range(8192):
        row = [x >> p & 1 for p in range(13)]
        actual = simulate(row, native)
        need(actual == sorted(row), "known native46 word fails to sort")
        outputs.add(sum(v * 2 ** p for p, v in enumerate(actual)))
        count("known_native46_boolean_inputs")
        count("known_native46_gate_evaluations", 46)
    transport_controls()
    return {"schema": "native21-six-history-exclusion-certificate-v1",
            "agent": "six-sorting-2", "role": "researcher", "n": 13,
            "size_budget": 44, "small_size_lower_bound": 35, "prefix_length": 21,
            "parent_files_sha256": PINS, "cases": cases,
            "minimum_cover": minimum_cover(), "high_cover": high_cover(),
            "finite_controls": finite_controls(),
            "known_native46": {"gate_list_sha256": digest(native),
                               "boolean_inputs": 8192, "sorted_outputs": sorted(outputs)},
            "native_prefix_total_interval": [45, 46],
            "native_prefix_suffix_interval": [24, 25]}


def validate_certificate(supplied, expected):
    need(supplied == expected and
         json.dumps(supplied, sort_keys=True) == json.dumps(expected, sort_keys=True),
         "certificate differs from full scalar reconstruction")


def damages(expected):
    mutations = []
    bad = deepcopy(expected); bad["size_budget"] = 45; mutations.append(bad)
    bad = deepcopy(expected); bad["cases"][0]["families"]["two_maxima"]["records"][0][4] += 1; mutations.append(bad)
    bad = deepcopy(expected); bad["cases"][0]["families"]["two_maxima"]["records"][0][6] ^= 1; mutations.append(bad)
    bad = deepcopy(expected); bad["cases"][1]["selected_records"].pop(); mutations.append(bad)
    bad = deepcopy(expected); bad["minimum_cover"]["event_words"].pop(); mutations.append(bad)
    bad = deepcopy(expected); bad["high_cover"]["event_words"].pop(); mutations.append(bad)
    bad = deepcopy(expected); bad["finite_controls"]["preparation10_overflows"][0]["mass"] = 512; mutations.append(bad)
    bad = deepcopy(expected); bad["finite_controls"]["all_merged_cost_lower_bound"] = 6; mutations.append(bad)
    for bad in mutations:
        rejected = False
        try:
            validate_certificate(bad, expected)
        except ValueError:
            rejected = True
        need(rejected, "damaged certificate accepted")
        count("damaged_certificates_rejected")
    fixture = json.loads((ROOT / "p21-fixture.json").read_text())
    for field, value in [("n", 12), ("selected_original_high_masks", [768] * 6),
                         ("minimum_stems", {"A": [[2, 1]]})]:
        bad = deepcopy(fixture); bad[field] = value
        rejected = False
        try:
            input_definition(bad)
        except ValueError:
            rejected = True
        need(rejected, "damaged fixture accepted")
        count("damaged_fixtures_rejected")


def main():
    start = time.monotonic()
    expected = build()
    path = ROOT / "p21-certificate.json"
    validate_certificate(json.loads(path.read_text()), expected)
    damages(expected)
    print(json.dumps({"status": "NATIVE21_SCALAR_CERTIFICATE_VERIFIED",
                      "agent": "six-sorting-2", "role": "researcher",
                      "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "metrics": METRICS, "seconds": time.monotonic() - start,
                      "maximum_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
                     sort_keys=True))


if __name__ == "__main__":
    main()

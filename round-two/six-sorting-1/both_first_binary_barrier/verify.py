"""Standalone scalar-cube/forest/heap checker; imports no producer or sibling.
Numeric generic primitives are copied with credit from actual9285 verify.py
(source2b8d0d2b5766ecb8775c72db231fa5eb06ee512a), itself adapting actual9127
(source7f0c4f85a073c697803d580d3d04d4cba2aed07e). See SOURCE-CREDITS.md.
Bottom-up forest enumeration and full numeric original cubes differ from the
producer's weighted partitions and packed columns. Same author, no peer verdict.
"""
import argparse
from copy import deepcopy
from functools import lru_cache
import hashlib
import heapq
from itertools import combinations, permutations
import json
from pathlib import Path
import resource
import time
ROOT = Path(__file__).resolve().parent
FIXTURE_SHA256 = 'c08176afb29259b1fa371ac88895f8ce73df51c5792d7babe870aae00d5e770c'
SIZES = (0,0,1,3,5,9,12,16,19,25,29,35,39,44)
FAMILIES = (("one_minimum",1,0),("one_maximum",0,1),("two_minima",2,0),
            ("two_maxima",0,2),("mixed_pair",1,1))
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



def move(classes, gate, low):
    a, b = gate
    target = a if low else b
    result = {}
    for p, d in classes:
        hit = p in gate
        q = target if hit else p
        result[q] = max(result.get(q, -1), d+int(hit))
    return tuple(sorted(result.items()))



def mass(classes):
    return sum(2**d for _, d in classes)



@lru_cache(None)
def reachable(classes, low):
    """Merge currently live blocks, memoizing forests and cluster genealogies."""
    initial = tuple((1 << p, p, d) for p, d in classes)
    initial = (tuple(sorted(initial)), ())
    todo, visited, terminal = [initial], {initial}, set()
    local_gates = 0
    equality_count = 0
    while todo:
        forest, history = todo.pop()
        current = tuple(sorted((p, d) for _, p, d in forest))
        old_mass = mass(current)
        need(old_mass <= 512, 'reachable forest exceeds ordinary ceiling')
        live = {p for p, _ in current}
        for gate in combinations(range(1, 12), 2):
            new_mass = mass(move(current, gate, low))
            hits = len(live.intersection(gate))
            need(new_mass >= old_mass, 'ordinary mass decreased')
            if hits == 0:
                need(new_mass == old_mass, 'free preparation changed class mass')
            if hits == 1:
                need(new_mass > old_mass, 'singleton does not strictly increase mass')
            if hits == 2:
                ds = [d for p, d in current if p in gate]
                need((new_mass == old_mass) == (ds[0] == ds[1]),
                     'equal-cost characterization failed')
                equality_count += int(ds[0] == ds[1])
            local_gates += 1
        if len(forest) == 1:
            need(forest[0][2] == 9 and old_mass == 512,
                 'terminal root is not exactly saturated')
            terminal.add(history)
            continue
        for i, j in combinations(range(len(forest)), 2):
            mask1, p1, d1 = forest[i]
            mask2, p2, d2 = forest[j]
            block = mask1 | mask2
            port = min(p1, p2) if low else max(p1, p2)
            d = max(d1, d2)+1
            future_mass = old_mass-2**d1-2**d2+2**d
            if future_mass > 512:
                continue
            need(not(mask1 & mask2), 'two forest blocks overlap')
            fresh = tuple(sorted([row for k, row in enumerate(forest) if k not in (i, j)]
                                 +[(block, port, d)]))
            next_history = tuple(sorted(history+(block,)))
            state = (fresh, next_history)
            if state not in visited:
                visited.add(state)
                todo.append(state)
    return tuple(sorted(terminal)), len(visited), local_gates, equality_count



def decode(history, classes, low):
    blocks = set(history) | {1 << p for p, _ in classes}
    full = sum(1 << p for p, _ in classes)
    def visit(block):
        if block & (block-1) == 0:
            return [], block.bit_length()-1
        proper = [b for b in blocks if b != block and b & block == b]
        children = [b for b in proper if not any(b != c and b & c == b for c in proper)]
        need(len(children) == 2 and children[0] ^ children[1] == block,
             'cluster hierarchy has invalid direct children')
        children.sort(key=lambda b: (b & -b).bit_length())
        wl, p = visit(children[0])
        wr, q = visit(children[1])
        return wl+wr+[sorted((p, q))], min(p, q) if low else max(p, q)
    return visit(full)



@lru_cache(None)
def inner_checked(word):
    data=profiles(7,[list(g) for g in word],'inner')
    anchors=anchor_bounds(7,data)
    lower=max(16,*(a['lower_bound'] for a in anchors.values()))
    return lower,data,anchors



def initial_classes(gates):
    result=[]
    for side in ('low','high'):
        records=[]
        for a,b in combinations(range(13),2):
            mask=(1<<a)+(1<<b)
            records.append(family(13,gates,mask if side=='low' else 0,
                                  mask if side=='high' else 0,'base_pair'))
        item=summary(records,2 if side=='low' else 0,2 if side=='high' else 0)
        current=[]
        for lo,hi,d,_ in item['envelope']:
            z=lo if side=='low' else hi
            held=0 if side=='low' else 12
            need(z>>held&1 and z.bit_count()==2,'ordinary pair held marker differs')
            p=(z^(1<<held)).bit_length()-1; current.append((p,d))
        current=tuple(sorted(current));need(mass(current)==448,'base ordinary mass differs')
        result.append(current)
    return result



def zero_slack_closure(classes,low):
    todo=[classes];seen={classes}
    while todo:
        state=todo.pop()
        for (p,d),(q,e) in combinations(state,2):
            if d!=e: continue
            child=move(state,tuple(sorted((p,q))),low)
            need(mass(child)==448,'equal event consumed first slack')
            if child not in seen:seen.add(child);todo.append(child)
    return sorted(seen)


def signature(word, leaves):
    """Full numeric Boolean function on all candidate inputs."""
    index = {p: i for i, p in enumerate(leaves)}
    need(all(a in index and b in index for a, b in word), 'route uses a noncandidate')
    outputs = [0] * len(leaves)
    for x in range(1 << len(leaves)):
        row = [x >> i & 1 for i in range(len(leaves))]
        for a, b in word:
            a, b = index[a], index[b]
            if row[a] > row[b]:
                row[a], row[b] = row[b], row[a]
        for i, value in enumerate(row):
            outputs[i] |= value << x
        count('route_function_assignments')
    return tuple(outputs)


def check_scope(packet, fixture):
    need(fixture['schema'] == 'b23-both-first-binary-fixture-v1', 'fixture schema differs')
    need(packet['schema'] == 'b23-both-first-binary-certificate-v1', 'certificate schema differs')
    need(packet['agent'] == fixture['agent'] == 'six-sorting-1' and
         packet['role'] == fixture['role'] == 'researcher', 'attribution differs')
    need(packet['fixture_sha256'] == FIXTURE_SHA256, 'fixture link differs')
    need(packet['total_budget'] == fixture['total_budget'] == 44 and
         fixture['imported_S11_lower_bound'] == 35, 'mathematical scope differs')
    need(len(fixture['B23']) == 23 and set(fixture['LOW_suffixes']) == {'1', '2', '4'},
         'literal LOW-front family differs')
    need(len(fixture['root_selectors']) == 90, 'selected root family differs')
    need(packet['conditional_HIGH_first_binary_branches'] == 90, 'summary scope differs')
    need(packet['scope'] == 'First HIGH strict binary after LOW partners1/4; conditional both-first-binary B23 corollary.',
         'conditional statement differs')
    need(packet['route_census'] == {'valid_event_orders': 300, 'local_controls': 2145,
                                  'distinct_six_input_functions': 45}, 'producer census differs')
    need(len(fixture['selected_original_pool']) == 99 and
         fixture['selected_original_pool'] == sorted(fixture['selected_original_pool']) and
         len({tuple(p) for p in fixture['selected_original_pool']}) == 99,
         'credited selected pool differs')


def independent_cover(fixture):
    low, high = initial_classes(fixture['B23'])
    need([list(r) for r in low] == fixture['initial_LOW'] and
         [list(r) for r in high] == fixture['initial_HIGH'], 'original pair classes differ')
    need({p for p, d in low} == {1, 2, 3, 4} and
         {p for p, d in high} == {5, 6, 7, 9, 10, 11}, 'disjoint candidate supports differ')
    lh, ls, lc, le = reachable(low, True)
    hh, hs, hc, he = reachable(high, False)
    lfunc = {signature(decode(h, low, True)[0], (1, 2, 3, 4)) for h in lh}
    hfunc = {signature(decode(h, high, False)[0], (5, 6, 7, 9, 10, 11)) for h in hh}
    need(len(lh) == len(lfunc) == 3 and len(hh) == len(hfunc) == 45,
         'independent complete binary forest cover differs')
    actual = set()
    for suffix in fixture['LOW_suffixes'].values():
        need(len(suffix) == 3 and all(0 <= a < b < 13 for a, b in suffix),
             'LOW canonical word differs')
        actual.add(signature(suffix, (1, 2, 3, 4)))
        final = move(move(move(low, tuple(suffix[0]), True), tuple(suffix[1]), True),
                     tuple(suffix[2]), True)
        need(final == ((1, 9),), 'LOW terminal class differs')
    need(actual == lfunc, 'published LOW functions miss a binary genealogy')
    return hfunc, {'LOW_trees': len(lh), 'LOW_states': ls, 'LOW_local_controls': lc,
                   'LOW_equal_cost_controls': le, 'HIGH_trees': len(hh), 'HIGH_states': hs,
                   'HIGH_local_controls': hc, 'HIGH_equal_cost_controls': he}


def check_cover(packet, expected, fixture):
    cases = packet['root_records']
    need(len(cases) == 90, 'missing or extra conditional root')
    for block, partner in enumerate((1, 4)):
        actual = set()
        for tree_id, case in enumerate(cases[block*45:(block+1)*45]):
            selector = fixture['root_selectors'][block*45+tree_id]
            need((case['partner'], case['tree_id']) == (partner, tree_id) and
                 (selector['partner'], selector['tree_id']) == (partner, tree_id),
                 'root identifiers differ')
            word = case['HIGH_word']
            need(len(word) == 5 and all(0 <= a < b < 13 for a, b in word),
                 'HIGH word is not five standard gates')
            func = signature(word, (5, 6, 7, 9, 10, 11))
            need(func not in actual, 'duplicate full route function')
            actual.add(func)
            prefix = fixture['B23'] + fixture['LOW_suffixes'][str(partner)] + word
            need(len(prefix) == 31 and digest(prefix) == selector['prefix_sha256'],
                 'literal selected prefix link differs')
        need(actual == expected, 'independent binary forest functions not completely covered')


def scalar_base(packet, fixture):
    image = set()
    for x in range(8192):
        row = [x >> p & 1 for p in range(13)]
        output = simulate(row, fixture['B23'])
        need(output[0] == min(row) and output[12] == max(row), 'base held ranks differ')
        image.add(sum(v << p for p, v in enumerate(output)))
        count('base_boolean_inputs')
        count('base_gate_evaluations', 23)
    image = sorted(image)
    need(len(image) == packet['base_image_size'] == 179 and
         digest(image) == packet['base_image_sha256'], 'complete original base image differs')


def scalar_image(case, fixture, level='root'):
    gates = fixture['B23'] + fixture['LOW_suffixes'][str(case['partner'])] + case['HIGH_word']
    exact = set()
    for x in range(8192):
        row = [x >> p & 1 for p in range(13)]
        out = simulate(row, gates)
        target = sorted(row)
        need(all(out[p] == target[p] for p in (0, 1, 11, 12)), 'four held ranks differ')
        exact.add(sum(out[p] << (p-2) for p in range(2, 11)))
        count(level + '_boolean_inputs')
        count(level + '_gate_evaluations', len(gates))
    exact = sorted(exact)
    need(len(exact) == case['nine_core_image_size'] and
         digest(exact) == case['nine_core_image_sha256'], 'complete original nine-image differs')


def replay_case(case, fixture):
    partner, tree_id = case['partner'], case['tree_id']
    index = (0 if partner == 1 else 45) + tree_id
    gates = fixture['B23'] + fixture['LOW_suffixes'][str(partner)] + case['HIGH_word']
    selector = fixture['root_selectors'][index]['original_clampings']
    need(len(case['selected_records']) == len(selector), 'original-domain selection count differs')
    pool = {tuple(p) for p in fixture['selected_original_pool']}
    replay = []
    classes = set()
    total = 0
    for row, masks in zip(case['selected_records'], selector):
        need(len(row) == 8 and row[:2] == masks and tuple(masks) in pool,
             'selected original domain differs')
        lo, hi = masks
        need(lo.bit_count() == hi.bit_count() == 3 and not lo & hi, 'invalid original3/3 cube')
        original = family(13, gates, lo, hi, 'outer')
        need(original == row[:7], 'whole original numeric record differs')
        pruned = pruning(13, gates, original)
        q = tuple(tuple(g) for g in pruned['retained_prefix'])
        b, data, anchors = inner_checked(q)
        need(b == row[7], 'independent nested inner bound differs')
        current = tuple(original[2:4])
        need(current not in classes, 'selected current classes repeat')
        classes.add(current)
        label = sum(original[4:6]) + b
        total += 1 << label
        replay.append({'partner': partner, 'tree_id': tree_id, 'record': original,
                       'Q_sha256': digest(q), 'pruning_sha256': digest(pruned),
                       'inner_record_hashes': {name: item['records_sha256'] for name, item in data.items()},
                       'inner_anchor_bounds': {side: item['lower_bound'] for side, item in anchors.items()},
                       'B7': b, 'label': label})
    need(total == case['selected_mass'] and total > 1 << 44, 'strict selected root inequality failed')
    return replay


def check_middle(packet, fixture):
    gates = fixture['B23'] + fixture['LOW_suffixes']['2']
    original = family(13, gates, 40, 0, 'middle_LOW')
    pruned = pruning(13, gates, original)
    need(original == packet['middle_LOW_record'] and original[4:6] == [9, 1],
         'middle LOW whole-cube C10 certificate differs')
    need(len(pruned['retained_prefix']) == packet['middle_LOW_retained_length'] == 16 and
         digest(pruned) == packet['middle_LOW_pruning_sha256'], 'middle LOW oriented pruning differs')
    # Same current LOW positions at cut25 do not authorize the same free deletion.
    held = family(13, gates[:25], 40, 0, 'middle_identity_control')
    other = family(13, gates[:25], 5, 0, 'middle_active_control')
    need(held[2:4] == other[2:4] and held[6] >> 24 & 1 and not other[6] >> 24 & 1,
         'same-configuration original-domain identity control differs')


def rejected(function):
    try:
        function()
    except ValueError:
        return 1
    raise ValueError('damaged mathematical certificate accepted')


def controls(packet, fixture, expected):
    sorter = fixture['positive7']
    need(len(sorter) == 16, 'seven-wire positive control size differs')
    for x in range(128):
        row = [x >> p & 1 for p in range(7)]
        need(simulate(row, sorter) == sorted(row), 'seven-wire positive control fails')
        count('positive7_inputs')
    for cut in range(17):
        need(max(16, bound(7, sorter[:cut], 'positive_inner')) <= 16,
             'anchor bound rejects a prefix of an optimal sorter')
    need(len(fixture['positive11']) == 35, 'eleven-wire positive control size differs')
    for x in range(2048):
        row = [x >> p & 1 for p in range(11)]
        need(simulate(row, fixture['positive11']) == sorted(row), 'eleven-wire positive control fails')
        count('positive11_inputs')
    for perm in permutations(range(4)):
        gates = [[0, 3], [2, 1]]
        renamed = [[perm[a], perm[b]] for a, b in gates]
        need(bound(4, gates) == bound(4, renamed), 'oriented bound changes under a wire permutation')
        count('wire_permutation_controls')
    full_sorter = [[j-1, j] for i in range(1, 13) for j in range(i, 0, -1)]
    for lo, hi in fixture['root_selectors'][0]['original_clampings'][:2]:
        original = family(13, full_sorter, lo, hi, 'positive_outer')
        q = pruning(13, full_sorter, original)['retained_prefix']
        for x in range(128):
            row = [x >> p & 1 for p in range(7)]
            need(simulate(row, q) == sorted(row), 'complete pruned positive sorter fails')
            count('positive_pruned_inputs')
        need(max(16, bound(7, q, 'positive_inner')) <= len(q), 'nested bound rejects pruned positive sorter')

    damages = 0
    bad = deepcopy(packet)
    bad['root_records'].pop()
    damages += rejected(lambda: check_cover(bad, expected, fixture))
    bad = deepcopy(packet)
    bad['root_records'][-1] = deepcopy(bad['root_records'][0])
    damages += rejected(lambda: check_cover(bad, expected, fixture))
    bad = deepcopy(packet)
    bad['root_records'][0]['HIGH_word'].pop()
    damages += rejected(lambda: check_cover(bad, expected, fixture))
    bad = deepcopy(packet)
    bad['root_records'][0]['HIGH_word'][0] = [1, 5]
    damages += rejected(lambda: check_cover(bad, expected, fixture))
    bad_fixture = deepcopy(fixture)
    bad_fixture['total_budget'] = 45
    damages += rejected(lambda: check_scope(packet, bad_fixture))
    bad = deepcopy(packet['root_records'][0])
    bad['nine_core_image_size'] += 1
    damages += rejected(lambda: scalar_image(bad, fixture, 'damaged_image'))
    for column in (2, 4, 5, 6, 7):
        bad = deepcopy(packet['root_records'][0])
        bad['selected_records'][0][column] += 1
        damages += rejected(lambda: replay_case(bad, fixture))
    bad = deepcopy(packet['root_records'][0])
    bad['selected_mass'] = 1 << 44
    damages += rejected(lambda: replay_case(bad, fixture))
    bad = deepcopy(packet['root_records'][0])
    bad['selected_records'].pop()
    damages += rejected(lambda: replay_case(bad, fixture))
    bad = deepcopy(packet['root_records'][0])
    bad_fixture = deepcopy(fixture)
    bad['selected_records'][1] = deepcopy(bad['selected_records'][0])
    bad_fixture['root_selectors'][0]['original_clampings'][1] = list(bad['selected_records'][0][:2])
    damages += rejected(lambda: replay_case(bad, bad_fixture))
    bad = deepcopy(packet)
    bad['middle_LOW_record'][5] += 1
    damages += rejected(lambda: check_middle(bad, fixture))
    need(damages == 15, 'damaged-certificate census differs')
    return damages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=ROOT / 'certificate.json')
    args = parser.parse_args()
    start = time.monotonic()
    raw_fixture = (ROOT / 'fixture.json').read_bytes()
    need(hashlib.sha256(raw_fixture).hexdigest() == FIXTURE_SHA256, 'fixed fixture differs')
    fixture = json.loads(raw_fixture)
    raw = args.certificate.read_bytes()
    packet = json.loads(raw)
    check_scope(packet, fixture)
    expected, audit = independent_cover(fixture)
    check_cover(packet, expected, fixture)
    scalar_base(packet, fixture)
    check_middle(packet, fixture)
    replay = []
    masses = []
    for case in packet['root_records']:
        scalar_image(case, fixture)
        replay.extend(replay_case(case, fixture))
        masses.append({'partner': case['partner'], 'tree_id': case['tree_id'], 'mass': case['selected_mass']})
    need(len(replay) == packet['selected_occurrences'] == 582, 'selected cube census differs')
    need(inner_checked.cache_info().currsize == packet['distinct_inner_words'] == 449,
         'distinct inner word census differs')
    need(digest(replay) == packet['replay_sha256'] ==
         '7a2d35ac07b2beadd86a80d38d8e02c16be4f76a9d498a7927bcf24b54dee14b',
         'full selected replay differs')
    need(digest(masses) == packet['root_masses_sha256'] ==
         '365d560f5d233019a401cd8078d6e71625bd721f82da959de7c69537c0922931',
         'complete root masses differ')
    minimum = min(r['mass'] for r in masses)
    need(minimum == packet['minimum_selected_mass'] == 17 * (1 << 40), 'minimum strict mass differs')
    proof_metrics = dict(METRICS)
    damages = controls(packet, fixture, expected)
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher',
                      'status': 'BOTH_FIRST_BINARY_CERTIFICATE_VERIFIED',
                      'certificate_sha256': hashlib.sha256(raw).hexdigest(), 'conditional_roots': 90,
                      'selected_original_occurrences': 582, 'proof_distinct_inner_words': 449,
                      'minimum_selected_mass': minimum, 'size44_ceiling': 1 << 44,
                      'replay_sha256': digest(replay), 'root_masses_sha256': digest(masses),
                      'forest_audit': audit, 'proof_metrics': proof_metrics,
                      'control_metrics': {k: v-proof_metrics.get(k, 0) for k, v in METRICS.items()
                                          if v != proof_metrics.get(k, 0)},
                      'damages_rejected': damages, 'same_author_algorithmic_independence': True,
                      'external_person_review_claimed': False,
                      'scope': 'Arbitrary-depth conditional HIGH first-binary barrier and B23 both-first-binary corollary; singleton/global endpoints open.',
                      'seconds': time.monotonic()-start,
                      'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == '__main__':
    main()

"""Standalone numeric checker for the native-prefix nested-potential closure.

No producer, profiler, sibling implementation, solver or nonstandard package
is imported. Complete original numeric free cubes determine deletions and
carrier routing; heap merges check Boolean-column/dyadic production.
Scalar primitives are copied from the same author's normalize_verify.py.
The unformalized universal theorem and imported coverage are in NESTED.md.
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
PINS = {'fixture.json': '93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6', 'certificate.json': '21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06', 'nested-fixture.json': '2ac145e523afcb00fb13976664577b2f2f3b9e1b28c2ae3336a6a4eb2051833a', '../../six-sorting-1/joint_extreme_kernel_barrier/fixture.json': 'b4c5bf4dab6468b9443b63518d10a4316d4e2d8a9a584fe071961054a6fa0995', '../../../sorting_networks/thirteen_twenty_prefix_exclusion/fixture.json': 'be346569bc7aab34f5d11f7eacc6e944f043bcc6f13e544a73336b402aa20900'}
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

PRECEDING_FOURTEEN = [2,8,15,20,24,31,32,33,34,36,38,39,41,42]


def checked(name, pin):
    raw = (ROOT / name).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == pin, 'fixture pin differs: ' + name)
    return json.loads(raw)


def family_masks(n, l, h):
    for lows in combinations(range(n), l):
        rest = [i for i in range(n) if i not in lows]
        for highs in combinations(rest, h):
            yield sum(2 ** i for i in lows), sum(2 ** i for i in highs)


def pairings(vertices):
    if not vertices:
        yield []
        return
    first = vertices[0]
    for j in range(1, len(vertices)):
        for rest in pairings(vertices[1:j] + vertices[j + 1:]):
            yield [[first, vertices[j]]] + rest


def canonical_kernels():
    result = []
    for bottom in pairings(list(range(5, 11))):
        ports7 = sorted([max(pair) for pair in bottom] + [11])
        for middle in pairings(ports7):
            result.append(bottom + middle + [sorted(max(pair) for pair in middle)])
    return result


def nested_row(n, gates, low, high, level):
    record = family(n, gates, low, high, level)
    pruned = pruning(n, gates, record)
    k = len(pruned['input_free_wires'])
    if k < 2:
        data, anchors, b = {}, {}, 0
    else:
        data = profiles(k, pruned['retained_prefix'], level + '_inner')
        anchors = anchor_bounds(k, data)
        b = max(SIZES[k], *(a['lower_bound'] for a in anchors.values()))
    return {'pruning': pruned,
            'inner_records_sha256': {name: item['records_sha256'] for name, item in data.items()},
            'inner_anchor_leaves': {side: [[r['port'], r['label']] for r in a['rows']]
                                    for side, a in anchors.items()},
            'inner_anchor_bounds': {side: a['lower_bound'] for side, a in anchors.items()},
            'inner_bound': b, 'prefix_cost': record[4] + record[5],
            'nested_label': record[4] + record[5] + b}


def class_weights(rows):
    labels = {}
    for r in rows:
        z = tuple(r['pruning']['outer_record'][2:4])
        labels[z] = max(labels.get(z, -1), r['nested_label'])
    return {z: 2 ** label for z, label in labels.items()}


def tag_transition(n, configuration, gate):
    low, high = configuration
    tags = [-1 if low >> p & 1 else 2 if high >> p & 1 else 0 for p in range(n)]
    a, b = gate
    hit = tags[a] != 0 or tags[b] != 0
    tags[a], tags[b] = min(tags[a], tags[b]), max(tags[a], tags[b])
    return tuple(ports(tags)), hit


def input_sources():
    source = {name: checked(name, pin) for name, pin in PINS.items()}
    native, parent, selected, positive, incumbent = (source[name] for name in PINS)
    need((selected['n'], selected['l'], selected['h'], selected['free_inputs'],
          selected['size_budget'], selected['small_size_lower_bound'],
          selected['native_prefix_length'], selected['root_length'], selected['kernel_count'])
         == (13, 3, 3, 7, 44, 16, 24, 32, 45), 'fixture parameters differ')
    need(native['forced_gates'] == [[11,12],[1,2]], 'forced word differs')
    need(len(native['gates']) == 46 and positive['known46'] == native['gates'], 'native word differs')
    need(len(positive['known45']) == 45, '45-gate control size differs')
    need(positive['known45'][:20] == incumbent['prefix20'], 'prior incumbent prefix identity differs')
    kernels = canonical_kernels()
    need(len(kernels) == 45 and len({digest(k) for k in kernels}) == 45, 'canonical kernel count differs')
    need([c['kernel'] for c in parent['kernels']] == kernels, 'literal canonical cover differs')
    need([c['kernel_id'] for c in selected['cases']] == list(range(45)), 'selected kernel IDs differ')
    need(sum(len(c['original_clampings']) for c in selected['cases']) == 236, 'selected row count differs')
    for c in selected['cases']:
        masks = c['original_clampings']
        need(4 <= len(masks) <= 7 and len({tuple(v) for v in masks}) == len(masks), 'invalid selected rows')
        for lo, hi in masks:
            template(13, lo, hi)
            need(lo.bit_count() == hi.bit_count() == 3, 'selected family counts differ')
    for word in [native['gates'], positive['known45'], *kernels]:
        need(all(type(a) == type(b) == int and 0 <= a < b < 13 for a,b in word), 'bad literal comparator')
    return native, selected, positive, kernels


def reconstruct(native, selected, kernels):
    cases = []
    for c in selected['cases']:
        i = c['kernel_id']
        gates = native['gates'][:24] + native['forced_gates'] + kernels[i]
        rows = [nested_row(13, gates, lo, hi, 'outer') for lo, hi in c['original_clampings']]
        weights = class_weights(rows)
        need(len(weights) == len(rows), 'selected current configurations overlap')
        mass = sum(weights.values())
        need(mass > 2 ** 44 and ceil_log(mass) == 45, 'selected mass does not exclude size 44')
        cases.append({'kernel_id': i, 'prefix32_sha256': digest(gates),
                      'selected_domains': rows, 'selected_classes': len(weights),
                      'selected_mass': mass, 'total_lower_bound': ceil_log(mass),
                      'maximum_individual_label': max(r['nested_label'] for r in rows)})
    return {'schema': 'native-nested-selected-certificate-v1', 'agent': 'six-sorting-2',
            'role': 'researcher', 'parent_files_sha256': {name: pin for name, pin in PINS.items()
                                                       if not name.startswith('../')},
            'n': 13, 'l': 3, 'h': 3, 'free_inputs': 7, 'size_budget': 44, 'root_length': 32,
            'kernel_count': 45, 'closed_preceding_fourteen': PRECEDING_FOURTEEN,
            'remaining_kernel_ids': [], 'cases': cases}


def match(candidate, expected):
    need(candidate == expected, 'certificate differs from complete scalar reconstruction')


def boolean_sorter(n, gates, level):
    for bits in range(2 ** n):
        inp = [bits >> p & 1 for p in range(n)]
        need(simulate(inp, gates) == sorted(inp), 'positive sorter fails')
        count(level + '_boolean_inputs')


def transport_controls():
    sorter = [[0,1],[2,3],[0,2],[1,3],[1,2]]
    families = [(1,0),(0,1),(2,0),(0,2),(1,1)]
    for first in permutations(range(4), 2):
        word = [list(first)] + sorter
        boolean_sorter(4, word, 'transport')
        for l, h in families:
            masks = list(family_masks(4, l, h))
            prev = None
            for cut in range(7):
                rows = [nested_row(4, word[:cut], lo, hi, 'transport') for lo, hi in masks]
                weights = class_weights(rows)
                if prev is not None:
                    old_rows, old_weights = prev
                    fibres = {}
                    gate = word[cut - 1]
                    for z in old_weights:
                        z2, hit = tag_transition(4, z, gate)
                        fibres.setdefault(z2, []).append((z, hit))
                    need(set(fibres) == set(weights), 'configuration image differs')
                    for z2, fibre in fibres.items():
                        need(len(fibre) <= 2, 'marker fibre has more than two preimages')
                        if len(fibre) == 2:
                            need(all(hit for _, hit in fibre), 'uncharged double fibre')
                            count('transport_double_fibres')
                        need(weights[z2] >= sum(old_weights[z] for z, _ in fibre), 'fibre weight decreases')
                        count('transport_fibres')
                    need(sum(weights.values()) >= sum(old_weights.values()), 'selected potential decreases')
                    for old, new in zip(old_rows, rows):
                        po, pn = old['pruning'], new['pruning']
                        z2, hit = tag_transition(4, tuple(po['outer_record'][2:4]), gate)
                        need(z2 == tuple(pn['outer_record'][2:4]), 'original marker route differs')
                        delta = new['prefix_cost'] - old['prefix_cost']
                        need(delta in (0,1), 'nonlocal semantic charge')
                        need(new['nested_label'] >= old['nested_label'] + delta, 'original label decreases')
                        need(not hit or delta == 1, 'marked gate has no charge')
                        if delta:
                            rename = {a: b for a,b in zip(po['input_to_output_wire'], pn['input_to_output_wire'])}
                            need([[rename[a],rename[b]] for a,b in po['retained_prefix']]
                                 == pn['retained_prefix'], 'deleted gate is not carrier conjugacy')
                            need(new['inner_bound'] == old['inner_bound'], 'bound not invariant under conjugacy')
                        else:
                            a,b = gate
                            extra = [po['output_free_wires'].index(a), po['output_free_wires'].index(b)]
                            need(pn['retained_prefix'] == po['retained_prefix'] + [extra], 'retained append differs')
                        count('transport_original_steps')
                need(sum(weights.values()) <= 2 ** len(word), 'positive potential exceeds terminal cap')
                if cut == len(word):
                    need(len(weights) == 1, 'sorted marker family is not one class')
                    for r in rows:
                        q = r['pruning']['retained_prefix']
                        need(r['inner_bound'] <= len(q), 'terminal small bound exceeds pruned sorter')
                    count('transport_terminal_families')
                prev = rows, weights
    # Global relabelling preserves full family records up to mask relabelling,
    # hence both implemented anchor bounds. Reverse gates occur in this control.
    sample = [[0,3],[2,1],[3,1],[0,2]]
    expected = max(SIZES[4], bound(4, sample, 'permutation'))
    for perm in permutations(range(4)):
        relabelled = [[perm[a],perm[b]] for a,b in sample]
        need(max(SIZES[4], bound(4, relabelled, 'permutation')) == expected,
             'global permutation changes implemented bound')
        count('permutation_bounds')


def positive_controls(native, selected, positive):
    seven = [[0,6],[2,3],[4,5],[0,2],[1,4],[3,6],[0,1],[2,5],
             [3,4],[1,2],[4,6],[2,3],[4,5],[1,2],[3,4],[5,6]]
    boolean_sorter(7, seven, 'small_positive')
    small_b = max(SIZES[7], bound(7, seven, 'small_positive'))
    need(small_b <= 16, 'known 16-gate seven-input sorter rejected')
    domains = sorted({tuple(v) for c in selected['cases'] for v in c['original_clampings']})
    need(len(domains) == 32, 'unique original domain count differs')
    for name, word in [('known45', positive['known45']), ('known46', native['gates'])]:
        boolean_sorter(13, word, name)
        for cut in (0,24,len(word)):
            rows = [nested_row(13, word[:cut], lo, hi, 'positive') for lo, hi in domains]
            need(sum(class_weights(rows).values()) <= 2 ** len(word), 'known sorter selected potential rejected')
            if cut == len(word):
                need(len(class_weights(rows)) == 1, 'positive final classes do not merge')
                for r in rows:
                    q = r['pruning']['retained_prefix']
                    need(r['inner_bound'] <= len(q), 'positive pruned bound exceeds size')
                    boolean_sorter(7, q, 'pruned_positive')
            count('positive_prefix_families')


def corruptions(expected):
    def reject(changed):
        try:
            match(changed, expected)
        except ValueError:
            count('corruptions_rejected')
        else:
            raise ValueError('damaged certificate accepted')
    for field in ('nested_label','inner_bound','prefix_cost'):
        damaged = deepcopy(expected)
        damaged['cases'][0]['selected_domains'][0][field] += 1
        reject(damaged)
    damaged = deepcopy(expected)
    damaged['cases'][0]['selected_domains'][0]['pruning']['outer_record'][5] += 1
    reject(damaged)
    damaged = deepcopy(expected)
    damaged['cases'][0]['selected_domains'][0]['pruning']['retained_prefix'][0].reverse()
    reject(damaged)
    damaged = deepcopy(expected)
    damaged['cases'][0]['selected_domains'][0]['inner_anchor_leaves']['low'][0][1] += 1
    reject(damaged)
    damaged = deepcopy(expected)
    damaged['cases'][0]['selected_domains'][1] = deepcopy(damaged['cases'][0]['selected_domains'][0])
    reject(damaged)
    raw = (ROOT / 'nested-fixture.json').read_bytes()
    need(hashlib.sha256(raw + b' ').hexdigest() != PINS['nested-fixture.json'], 'damaged fixture pin accepted')
    count('corruptions_rejected')


def main():
    start = time.monotonic()
    native, selected, positive, kernels = input_sources()
    expected = reconstruct(native, selected, kernels)
    match(json.loads((ROOT / 'nested-certificate.json').read_text()), expected)
    transport_controls()
    positive_controls(native, selected, positive)
    corruptions(expected)
    print(json.dumps({'status': 'ALL_NATIVE24_NESTED_CHECKS_PASSED', 'agent': 'six-sorting-2',
                      'role': 'researcher', 'kernel_count': 45, 'selected_domains': 236,
                      'newly_closed_preceding_targets': 14, 'remaining_targets': 0,
                      'minimum_selected_mass': min(c['selected_mass'] for c in expected['cases']),
                      'size44_cap': 2 ** 44, **METRICS,
                      'certificate_sha256': hashlib.sha256((ROOT / 'nested-certificate.json').read_bytes()).hexdigest(),
                      'seconds': time.monotonic() - start,
                      'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == '__main__':
    main()

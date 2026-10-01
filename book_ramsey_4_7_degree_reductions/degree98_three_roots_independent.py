"""Separate exact audit of the 98-edge three-low-root reduction.
Actual author six-books-1, researcher, 2026-10-01. No predecessor imports.
"""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import json
import argparse
from copy import deepcopy
from hashlib import sha256
from random import Random

UP = tuple(combinations(range(3, 8), 2))
PAIRS = tuple(combinations(range(8), 2))
PBIT = {p: k for k, p in enumerate(PAIRS)}
GROUPS = {
    0: tuple(combinations(range(3, 8), 3)),
    1: tuple((0,) + t for t in UP),
    2: tuple((1,) + t for t in UP),
    5: tuple((0, 2, i) for i in range(3, 8)),
    6: tuple((1, 2, i) for i in range(3, 8)),
    7: ((0, 1, 2),),
}
PERMS = [(a, b, 2) + p for a, b in ((0, 1), (1, 0)) for p in permutations(range(3, 8))]

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def canon(edges):
    return min(sum(1 << bit for bit, (i, j) in enumerate(PAIRS)
                   if tuple(sorted((p[i], p[j]))) in edges) for p in PERMS)

def census():
    cores = Counter()
    for nb in UP:
        for nc in UP:
            for nz in combinations(range(3, 8), 3):
                degrees = {i: sum(i in t for t in (nb, nc, nz)) for i in range(3, 8)}
                for inside in combinations(UP, 4):
                    if any(degrees[i] + sum(i in pair for pair in inside) != 3 for i in range(3, 8)):
                        continue
                    edges = {(0, 1)} | {(0, i) for i in nb} | {(1, i) for i in nc} | {(2, i) for i in nz} | set(inside)
                    need(len(edges) == 12, 'twelve core edges')
                    cores[canon(edges)] += 1
    return cores

def bounded_rows(cap, col_initial, totals):
    columns = list(col_initial)
    remaining = list(cap)
    chosen = []
    nodes = 0
    # Special all-root row first, then rows with two, one and zero roots.
    order = (7, 5, 6, 1, 2, 0)
    patterns = {g: [(row, tuple(PBIT[p] for p in combinations(sorted(row), 2))) for row in GROUPS[g]] for g in order}
    def feasible(groups):
        for i in range(8):
            capacity = 0
            for g, count, minimum in groups:
                if any(i in row and all(columns[x] for x in row) and all(remaining[p] for p in pairs)
                       for row, pairs in patterns[g][minimum:]):
                    capacity += count
            if columns[i] > capacity:
                return False
        return True
    def step(g_index, count, minimum):
        nonlocal nodes
        nodes += 1
        if g_index == len(order):
            if not any(columns):
                need(len(chosen) == 13, 'thirteen direct rows')
                return tuple(chosen)
            return None
        group = order[g_index]
        if not count:
            if g_index + 1 == len(order):
                return step(g_index + 1, 0, 0)
            nxt = order[g_index + 1]
            return step(g_index + 1, totals[nxt], 0)
        future = [(group, count, minimum)] + [(g, totals[g], 0) for g in order[g_index + 1:]]
        if not feasible(future):
            return None
        for k in range(minimum, len(patterns[group])):
            row, pairs = patterns[group][k]
            if not all(columns[i] for i in row) or not all(remaining[p] for p in pairs):
                continue
            for i in row:
                columns[i] -= 1
            for p in pairs:
                remaining[p] -= 1
            chosen.append(sum(1 << i for i in row))
            result = step(g_index, count - 1, k)
            chosen.pop()
            for p in pairs:
                remaining[p] += 1
            for i in row:
                columns[i] += 1
            if result is not None:
                return result
        return None
    result = step(0, totals[7], 0)
    return result, nodes

def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()

def edge_weights(cap, initial):
    """Separate edge-by-edge enumeration of the five-edge weighted domain."""
    demand = list(initial)
    weights = [0] * 28
    def rec(k):
        if not any(demand):
            yield tuple(weights)
            return
        if k == 28:
            return
        i, j = PAIRS[k]
        for value in range(min(cap[k], demand[i], demand[j]) + 1):
            weights[k] = value
            demand[i] -= value
            demand[j] -= value
            available = [0] * 8
            for l in range(k + 1, 28):
                a, b = PAIRS[l]
                available[a] += min(cap[l], demand[b])
                available[b] += min(cap[l], demand[a])
            if all(demand[v] <= available[v] for v in range(8)):
                yield from rec(k + 1)
            demand[i] += value
            demand[j] += value
            weights[k] = 0
    yield from rec(0)

def roots():
    pair4 = tuple(combinations(range(4), 2))
    masks = []
    classes = {}
    for count in range(7):
        for edges in combinations(pair4, count):
            neighbors = [set() for _ in range(4)]
            for i, j in edges:
                neighbors[i].add(j)
                neighbors[j].add(i)
            f = []
            for i in range(3):
                degree_sum = 9 * 8 - len(neighbors[i] & {0, 1, 2}) + int(3 in neighbors[i])
                f.append(196 - 294 + 38 * 8 - 8 * 8 - 2 * degree_sum)
            if min(f) < 0:
                continue
            mask = sum(1 << k for k, pair in enumerate(pair4) if pair in edges)
            key = min(sum(1 << k for k, (i, j) in enumerate(pair4)
                          if tuple(sorted((p[i], p[j]))) in edges)
                      for pp in permutations(range(3)) for p in [pp + (3,)])
            masks.append([mask, key])
            k = len(neighbors[3])
            qz = 196 - 294 + 38 * 10 - 100 - 2 * (90 - k)
            shape = 'P3' if sum(len(n & {0, 1, 2}) for n in neighbors[:3]) == 4 else 'K3'
            if key not in classes:
                classes[key] = {'mask': key, 'shape': shape, 'k': k,
                                'sum_qA': sum(f), 'qz': qz, 'qB': 24 - sum(f) - qz,
                                'multiplicity': 0}
            classes[key]['multiplicity'] += 1
    p3 = []
    for e, g, r in ((e, g, r) for e in range(2) for g in range(2) for r in range(2)):
        have = (8 - 2 - e) - (3 + 3 - g)
        required = (10 - e) - ((4 - e) + (4 - e) - r)
        if have < 0:
            continue
        need(have < required, 'separate path containment gap')
        p3.append([e, g, r, have, required])
    k2 = []
    for g in range(2):
        for r in range(2):
            have = (8 - 2) - (2 + 2 - g)
            required = (10 - 2) - (2 + 2 - r)
            need(have < required, 'separate two-edge triangle gap')
            k2.append([g, r, have, required])
    need(3 * (3 - 2) < 10 - 3, 'separate three-edge triangle gap')
    return {'tested_masks': 64, 'eligible_masks': sorted(masks),
            'classes': [classes[k] for k in sorted(classes)],
            'P3_parameters': p3, 'K3_k2_parameters': k2, 'K3_k3_incidence': [3, 7]}

def baseline():
    data = Path(__file__).with_name('baseline21.rows').read_text().splitlines()
    need(len(data) == 21 and all(len(row) == 21 and set(row) <= {'0', '1'} for row in data), 'baseline format')
    for i in range(21):
        need(data[i][i] == '0' and all(data[i][j] == data[j][i] for j in range(21)), 'baseline symmetry')
    pages = [0, 0]
    for i, j in combinations(range(21), 2):
        color = int(data[i][j])
        common = sum(data[i][k] == data[j][k] == str(color) for k in range(21) if k not in (i, j))
        pages[color] = max(pages[color], common)
    need(pages == [6, 3], 'primary known21 pages')
    return {'vertices': 21, 'red_edges': sum(row.count('1') for row in data) // 2,
            'red_page_maximum': pages[1], 'blue_page_maximum': pages[0]}

def control_rows():
    # The two singly covered rows, six z rows and five cyclic U triples.
    result = [{0, 3, 4}, {1, 5, 6}, {0, 2, 3}, {0, 2, 4}, {0, 2, 7},
              {1, 2, 5}, {1, 2, 6}, {1, 2, 7}]
    result += [{3 + i, 3 + (i + 1) % 5, 3 + (i + 2) % 5} for i in range(5)]
    return result

def signed_controls(masks):
    """Alternative literal graph representation and outside regular controls."""
    identity_rows = gram_entries = outside_rows = 0
    hashes = []
    for number, mask in enumerate(masks):
        graph = [[0] * 22 for _ in range(22)]
        def edge(i, j):
            graph[i][j] = graph[j][i] = 1
        for i in range(1, 9):
            edge(0, i)
        for k, (i, j) in enumerate(PAIRS):
            if (mask >> k) & 1:
                edge(i + 1, j + 1)
        rows = control_rows()
        # Permute only the U columns; their prescribed sums all equal five.
        rng = Random(31698 + number)
        u = list(range(3, 8))
        rng.shuffle(u)
        perm = [0, 1, 2] + u
        rows = [{perm[i] for i in row} for row in rows]
        for j, row in enumerate(rows, 9):
            for i in row:
                edge(i + 1, j)
        for i in range(13):
            for d in (1, 4, 5):
                edge(i + 9, (i + d) % 13 + 9)
        degrees = list(map(sum, graph))
        need(degrees == [8, 8, 8, 10] + [9] * 18, 'separate signed histogram')
        f = [[0] * 22 for _ in range(22)]
        for i, j in combinations(range(22), 2):
            color = graph[i][j]
            pages = sum(graph[i][k] == graph[j][k] == color for k in range(22) if k not in (i, j))
            f[i][j] = f[j][i] = (3 if color else 6) - pages
        need(not any(f[0]) and any(v < 0 for line in f for v in line), 'separate signed saturation/page violation')
        for i in range(22):
            degree_sum = sum(degrees[j] for j in range(22) if graph[i][j])
            need(sum(f[i]) == 196 - 294 + 38 * degrees[i] - degrees[i] ** 2 - 2 * degree_sum,
                 'separate incident counting identity')
            identity_rows += 1
        for i in range(8):
            for j in range(8):
                actual = sum(i in row and j in row for row in rows)
                if i == j:
                    predicted = degrees[i + 1] - 4
                else:
                    common = sum(graph[i + 1][k + 1] * graph[j + 1][k + 1] for k in range(8))
                    predicted = (2 if graph[i + 1][j + 1] else degrees[i + 1] + degrees[j + 1] - 15) - common - f[i + 1][j + 1]
                need(actual == predicted, 'separate literal Gram identity')
                gram_entries += 1
        for i in range(9, 22):
            delta = graph[i][1] + graph[i][2] - graph[i][3]
            need(sum(f[i][1:9]) == 1 + delta and sum(f[i][9:22]) == delta, 'separate outside defect identity')
            outside_rows += 1
        hashes.append(sha256(encode(graph)).hexdigest())
    return {'graphs': len(masks), 'incident_rows': identity_rows, 'Gram_entries': gram_entries,
            'outside_defect_rows': outside_rows, 'signed_graph_hashes': hashes}

def full_matrix_compare(record, weights, data):
    e = [[0] * 8 for _ in range(8)]
    s = [[0] * 8 for _ in range(8)]
    for i in range(8):
        s[i][i] = [4, 4, 6, 5, 5, 5, 5, 5][i]
    for k, (i, j) in enumerate(PAIRS):
        e[i][j] = e[j][i] = weights[k]
        s[i][j] = s[j][i] = record['capacities'][k] - weights[k]
    need(data == {'J_mask': record['J_mask'], 'E': e, 'S': s}, 'full E/S entry differs')
    return 64, 64

def scientific_audit(full=None):
    controls = control_rows()
    caps = [sum(i in row and j in row for row in controls) for i, j in PAIRS]
    totals = {0: 5, 1: 1, 2: 1, 5: 3, 6: 3, 7: 0}
    witness, nodes = bounded_rows(caps, [4, 4, 6, 5, 5, 5, 5, 5], totals)
    need(witness is not None and [sum((r >> i) & (r >> j) & 1 for r in witness) for i, j in PAIRS] == caps,
         'positive direct binary incidence control')
    need(list(edge_weights([0] * 28, [0] * 8)) == [(0,) * 28], 'empty weighted control')
    cap1 = [0] * 28
    cap1[0] = 2
    need(list(edge_weights(cap1, [2, 2] + [0] * 6)) == [(2,) + (0,) * 27], 'weighted multiplicity control')
    groups = census()
    degrees = [8, 8, 10, 9, 9, 9, 9, 9]
    profiles = [(f, b, 2 - f - b) for f in range(3) for b in range(3 - f)]
    records = []
    direct = []
    compared_e = compared_s = 0
    matched_full = set()
    for mask, multiplicity in sorted(groups.items()):
        adj = [set() for _ in range(8)]
        for bit, (i, j) in enumerate(PAIRS):
            if (mask >> bit) & 1:
                adj[i].add(j)
                adj[j].add(i)
        caps = [(2 if j in adj[i] else degrees[i] + degrees[j] - 15) - len(adj[i] & adj[j]) for i, j in PAIRS]
        star = [sum(caps[k] for k, pair in enumerate(PAIRS) if i in pair) - 2 * (degrees[i] - 4) for i in range(8)]
        need(sum(star) == 10 and min(star) >= 0, 'separate weighted star budget')
        record = {'J_mask': mask, 'multiplicity': multiplicity, 'capacities': caps,
                  'defect_degrees': star, 'negative_capacity': min(caps) < 0,
                  'weighted_forms': 0, 'binary_incidence_survivors': 0}
        all_weights = []
        direct_record = {'J_mask': mask, 'profiles': []}
        if not record['negative_capacity']:
            for f, b, c in profiles:
                totals = {0: 5 + f, 1: b, 2: c, 5: 4 - b - f, 6: 4 - c - f, 7: f}
                witness, nodes = bounded_rows(caps, [d - 4 for d in degrees], totals)
                need(witness is None, 'direct capacitated binary incidence survives')
                direct_record['profiles'].append({'f': f, 'b': b, 'c': c, 'nodes': nodes})
            for weights in edge_weights(caps, star):
                all_weights.append(list(weights))
                if full is not None:
                    key = (mask, weights)
                    need(key in full, 'full matrix missing')
                    e_count, s_count = full_matrix_compare(record, weights, full[key])
                    compared_e += e_count
                    compared_s += s_count
                    matched_full.add(key)
        record['weighted_forms'] = len(all_weights)
        record['weighted_forms_sha256'] = sha256(encode(sorted(all_weights))).hexdigest()
        records.append(record)
        direct.append(direct_record)
    if full is not None:
        need(matched_full == set(full), 'extraneous full matrix')
    need(sum(groups.values()) == 3370 and len(groups) == 22, 'separate marked core census')
    need(sum(r['weighted_forms'] for r in records) == 1014, 'separate five-edge domain')
    need(sum(len(r['profiles']) for r in direct) == 126, 'all six profiles on nonnegative cores')
    return {'cores': records, 'root_census': roots(), 'direct_profiles': direct,
            'known21_validation_only': baseline(), 'signed_identity_controls': signed_controls(sorted(groups)),
            'E_entries_compared': compared_e, 'S_entries_compared': compared_s}

def match(expected, scientific):
    need(expected['agent'] == 'six-books-1' and expected['role'] == 'researcher' and expected['schema'] == 1, 'certificate identity')
    need(expected['claim'] == 'histogram(3,18,1) forces A=K3 and e(z,A)=0; histogram remains open', 'claim scope')
    need(expected['cores'] == scientific['cores'], 'complete core/capacity/weighted census differs')
    need(expected['root_census'] == scientific['root_census'], 'four-root census differs')
    need(expected['known21_validation_only'] == scientific['known21_validation_only'], 'baseline differs')
    patterns = sorted(tuple(i for i in range(8) if (m >> i) & 1) for m in range(256)
                      if m.bit_count() == 3 and 0 <= ((m >> 0) & 1) + ((m >> 1) & 1) - ((m >> 2) & 1) <= 1)
    need(expected['allowed_row_types'] == [list(t) for t in patterns], 'complete binary row domain differs')
    need(expected['marked_cubic_labeled'] == 3370 and expected['marked_cubic_classes'] == 22
         and expected['negative_capacity_classes'] == 1 and expected['weighted_forms'] == 1014
         and expected['binary_incidence_survivors'] == 0, 'finite coverage summary differs')
    for key in ('graphs', 'incident_rows', 'Gram_entries', 'outside_defect_rows'):
        need(expected['signed_identity_controls'][key] == scientific['signed_identity_controls'][key], 'signed control coverage differs')

def corruption_checks(expected, scientific):
    tests = []
    def rejected(label, mutate):
        altered = deepcopy(expected)
        mutate(altered)
        try:
            match(altered, scientific)
        except (RuntimeError, KeyError, TypeError):
            tests.append(label)
        else:
            raise RuntimeError('altered certificate accepted: ' + label)
    rejected('missing root mask', lambda x: x['root_census']['eligible_masks'].pop())
    rejected('wrong root surplus', lambda x: x['root_census']['classes'][0].__setitem__('qB', 999))
    rejected('missing cubic core', lambda x: x['cores'].pop())
    rejected('wrong orbit multiplicity', lambda x: x['cores'][0].__setitem__('multiplicity', 999))
    rejected('wrong pair capacity', lambda x: x['cores'][0]['capacities'].__setitem__(0, 99))
    rejected('wrong weighted star', lambda x: x['cores'][0]['defect_degrees'].__setitem__(0, 99))
    rejected('wrong weighted fingerprint', lambda x: x['cores'][0].__setitem__('weighted_forms_sha256', '0' * 64))
    rejected('wrong weighted count', lambda x: x.__setitem__('weighted_forms', 1013))
    rejected('omitted binary row type', lambda x: x['allowed_row_types'].pop())
    rejected('false survivor count', lambda x: x.__setitem__('binary_incidence_survivors', 1))
    rejected('overstated histogram exclusion', lambda x: x.__setitem__('claim', 'histogram completely excluded'))
    return tests

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--matrices', type=Path, help='compare every regenerated local E/S entry')
    parser.add_argument('--output', type=Path, help='write the separate audit summary')
    args = parser.parse_args()
    full = None
    if args.matrices:
        data = json.loads(args.matrices.read_text())
        full = {}
        for record in data:
            need(len(record['E']) == 8 and all(len(row) == 8 for row in record['E']), 'full matrix shape')
            weights = tuple(record['E'][i][j] for i, j in PAIRS)
            key = (record['J_mask'], weights)
            need(key not in full, 'duplicate full matrix')
            full[key] = record
        need(len(full) == 1014, 'full matrix cardinality')
    scientific = scientific_audit(full)
    expected = json.loads(Path(__file__).with_name('degree98_three_roots_expected.json').read_text())
    match(expected, scientific)
    rejected = corruption_checks(expected, scientific)
    if full is not None:
        key = next(iter(full))
        changed = deepcopy(full[key])
        changed['S'][0][1] += 1
        record = next(r for r in scientific['cores'] if r['J_mask'] == key[0])
        try:
            full_matrix_compare(record, key[1], changed)
        except RuntimeError:
            rejected.append('changed full Gram entry')
        else:
            raise RuntimeError('full Gram corruption accepted')
    out = {'agent': 'six-books-1', 'role': 'researcher', 'complete': True,
           'separate_domain': 'marked-neighbor subsets/internal edges; direct grouped rows; edge-wise weighted audit',
           'marked_cubic_labeled': 3370, 'marked_cubic_classes': 22, 'direct_root_profiles': 126,
           'direct_search_nodes': sum(p['nodes'] for r in scientific['direct_profiles'] for p in r['profiles']),
           'weighted_forms': 1014, 'binary_incidence_survivors': 0, 'positive_control': True,
           'E_entries_compared': scientific['E_entries_compared'], 'S_entries_compared': scientific['S_entries_compared'],
           'corruptions_rejected': rejected, 'separate_signed_graph_controls': scientific['signed_identity_controls']}
    if args.output:
        args.output.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'separate_signed_graph_controls'}))

if __name__ == '__main__':
    main()

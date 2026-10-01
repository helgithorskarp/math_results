"""Literal set validation of the ordinary proof; no solver or census premise."""
import argparse
import copy
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise ValueError(message)


def shift(points, k, p=7):
    return {(x+k) % p for x in points}


def reverse(points, p=7):
    return {(-x) % p for x in points}


def sym(k):
    return {k % 7, (-k) % 7}


def classes(points):
    return {min(x, 7-x) for x in points}


def rho(points):
    return tuple(len(points & shift(points, k)) for k in range(1, 4))


def progression(center, step):
    return {(center-step) % 7, center % 7, (center+step) % 7}


def step_class(points):
    options = [(h, d) for h in range(7) for d in range(1, 4)
               if progression(h, d) == points]
    require(len(options) <= 1, 'progression center/step not unique')
    return options[0][1] if options else None


def matrix(internal, cross):
    out = [[set() for _ in range(3)] for _ in range(3)]
    for i in range(3):
        out[i][i] = internal[i]
    for (i, j), points in cross.items():
        out[i][j] = points
        out[j][i] = reverse(points)
    return out


def graph(internal, cross, fixed=(True, False, False)):
    n = 21 + int(fixed is not None)
    rows = [set() for _ in range(n)]
    for i, j in itertools.combinations(range(n), 2):
        if j == 21:
            red = fixed[i//7]
        elif i//7 == j//7:
            red = (j-i) % 7 in internal[i//7]
        else:
            red = (j-i) % 7 in cross[i//7, j//7]
        if red:
            rows[i].add(j)
            rows[j].add(i)
    return rows


def page_histograms(rows):
    n = len(rows)
    for i, neighbors in enumerate(rows):
        require(i not in neighbors and all(0 <= j < n for j in neighbors), 'literal loop/range')
        require(all(i in rows[j] for j in neighbors), 'literal asymmetric rows')
    hist = [{}, {}]
    for i, j in itertools.combinations(range(n), 2):
        red = j in rows[i]
        pages = len(rows[i] & rows[j]) if red else len(set(range(n))-{i, j}-rows[i]-rows[j])
        h = hist[0 if red else 1]
        h[pages] = h.get(pages, 0)+1
    return [{str(k): v for k, v in sorted(h.items())} for h in hist]


def validate_identities(internal, cross, fixed=(True, False, False)):
    rows = graph(internal, cross, fixed)
    m = matrix(internal, cross)
    n = len(rows)
    for i, j in itertools.combinations(range(n), 2):
        red = j in rows[i]
        common = len(rows[i] & rows[j])
        if j == 21:
            formula = sum(len(m[i//7][k]) for k in range(3) if fixed[k])
        else:
            a, b = i//7, j//7
            offset = (j-i) % 7
            formula = sum(len(m[a][k] & shift(m[b][k], offset)) for k in range(3))
            if fixed is not None:
                formula += int(fixed[a] and fixed[b])
        require(formula == common, 'literal/oriented correlation mismatch')
        if not red:
            blue = len(set(range(n))-{i, j}-rows[i]-rows[j])
            require(blue == n-2-len(rows[i])-len(rows[j])+formula, 'blue complement identity')
    return rows


def phase_graph(h):
    internal = [sym(1), set(range(1, 7))-sym(2), set(range(1, 7))-sym(1)]
    cross = {(0, 1): {0, 2, 5}, (0, 2): {0, 3, 4},
             (1, 2): shift({0, 1, 6}, h)}
    return validate_identities(internal, cross)


def validate_books(records):
    require(isinstance(records, list) and len(records) == 7, 'incomplete phase book list')
    seen = set()
    for record in records:
        require(set(record) == {'h', 'spine', 'color', 'pages', 'degrees_histogram'}, 'phase schema')
        h = record['h']
        require(type(h) is int and 0 <= h < 7 and h not in seen, 'phase range/duplication')
        seen.add(h)
        rows = phase_graph(h)
        require(record['degrees_histogram'] == {'7': 1, '9': 7, '10': 14}, 'phase degree scope')
        require([len(r) for r in rows] == [9]*7+[10]*14+[7], 'literal phase degrees')
        spine = record['spine']
        require(len(spine) == 2 and all(type(x) is int and 0 <= x < 22 for x in spine), 'spine range')
        i, j = spine
        require(i < j and record['color'] in ('red', 'blue'), 'spine ordering/color')
        red = record['color'] == 'red'
        require((j in rows[i]) == red, 'book spine color mismatch')
        pages = record['pages']
        require(all(type(x) is int and 0 <= x < 22 for x in pages), 'page range')
        require(len(set(pages)) == len(pages) and i not in pages and j not in pages, 'book page duplication/endpoints')
        actual = sorted(rows[i] & rows[j]) if red else sorted(set(range(22))-{i, j}-rows[i]-rows[j])
        require(pages == actual and len(pages) >= (4 if red else 7), 'literal book pages mismatch')
    require(seen == set(range(7)), 'phase coverage')


def read_primary(path):
    lines = path.read_text().splitlines()
    require(len(lines) == 21 and all(len(x) == 21 and set(x) <= {'0', '1'} for x in lines), 'primary dimensions/alphabet')
    return [{j for j, bit in enumerate(line) if bit == '1'} for line in lines]


def kg_control():
    pairs = [frozenset((t, (t+d) % 7)) for d in (1, 2, 3) for t in range(7)]
    require(len(set(pairs)) == 21, 'KG labeling is not bijective')
    rows = [{j for j, q in enumerate(pairs) if p.isdisjoint(q)} for p in pairs]
    action = [next(j for j, q in enumerate(pairs) if q == frozenset((x+1) % 7 for x in p))
              for p in pairs]
    require(action == [7*(i//7)+(i+1) % 7 for i in range(21)], 'KG order-seven action')
    internal = [{j for j in rows[7*i] if 7*i <= j < 7*(i+1)} for i in range(3)]
    internal = [{j-7*i for j in s} for i, s in enumerate(internal)]
    cross = {(i, j): {k-7*j for k in rows[7*i] if 7*j <= k < 7*(j+1)}
             for i in range(3) for j in range(i+1, 3)}
    require(validate_identities(internal, cross, None) == rows, 'KG block and root-pair controls disagree')
    require(all(len(x) == 10 for x in rows), 'KG degrees')
    return page_histograms(rows)


def compute(books_path, primary_path):
    k1 = [(15-l, l, s) for l in range(16) for s in (0, 2, 4, 6)
          if l <= 5 and 15-l+s <= 10]
    require(k1 == [(10, 5, 0)] and 5+k1[0][1] > 6, 'one-cycle packing')
    k2 = [(a, b, 8-a-b) for a in range(9) for b in range(9-a)]
    joined = [(a, b, z) for a, b, z in k2 if a > 0 and b > 0 and a+z <= 4 and b+z <= 4]
    require(joined == [(4, 4, 0)] and 5+4 > 6, 'two-cycle packing')
    margins = []
    for m in range(4):
        for n in range(4):
            value = m*m+n*n-9*(m+n)+34
            require(value == 2+m*(m-1)+n*(n-1)-(4+4*(2*(m+n)-9)), 'A energy expansion')
            if value <= 0:
                margins.append([m, n])
    require(margins == [[3, 3]], 'A scalar coverage')
    outside = [[s, 7-s, s*(s-1)+6+(7-s)*(6-s), 3*s+6*(6-s)] for s in (0, 2, 4, 6)]
    require([s for s, q, l, u in outside if l <= u] == [2, 4], 'outside energy coverage')
    triple_sets = [set(s) for s in itertools.combinations(range(7), 3)]
    vec_counts = {}
    for points in triple_sets:
        vec = rho(points)
        vec_counts[str(list(vec))] = vec_counts.get(str(list(vec)), 0)+1
        d = step_class(points)
        require((d is not None) == (vec != (1, 1, 1)), 'three-set classification')
        if d is not None:
            expected = {min(d, 7-d): 2, min(2*d % 7, 7-2*d % 7): 1,
                        min(3*d % 7, 7-3*d % 7): 0}
            require(vec == tuple(expected[k] for k in (1, 2, 3)), 'progression correlation vector')
    single_two = single_four = 0
    for b in (1, 2, 3):
        for points in triple_sets:
            for size in (5, 3):
                d = sym(b) if size == 5 else set(range(1, 7))-sym(b)
                for values in itertools.combinations(range(7), size):
                    q = set(values)
                    if any(rho(d)[k-1]+rho(points)[k-1]+rho(q)[k-1] > (3 if k in d else 6)
                           for k in (1, 2, 3)):
                        continue
                    if size == 5:
                        missing = set(range(7))-q
                        difference = next(iter(missing))
                        difference = (next(x for x in missing if x != difference)-difference) % 7
                        require(min(difference, 7-difference) == min(3*b % 7, 7-3*b % 7), 'missing pair class')
                        require(step_class(points) == min(2*b % 7, 7-2*b % 7), 'outside-cycle P step')
                        single_two += 1
                    else:
                        require({step_class(points), step_class(q)} == {b, min(3*b % 7, 7-3*b % 7)}, 'complement-cycle step pair')
                        single_four += 1
    records = json.loads(books_path.read_text())
    validate_books(records)
    f = [len({0, 2, 5} & shift({0, 1, 6}, t)) for t in range(7)]
    require(f == [1, 2, 1, 1, 1, 1, 2], 'phase neighborhood table')
    allowed_h = [h for h in range(7) if all(f[(k-h) % 7] <= 1 for k in (0, 3, 4))]
    require(allowed_h == [0], 'phase implication')
    primary = read_primary(primary_path)
    primary_hist = page_histograms(primary)
    degrees = [len(r) for r in primary]
    require({d: degrees.count(d) for d in set(degrees)} == {8: 4, 9: 16, 10: 1}, 'primary degree histogram')
    require(sum(degrees)//2 == 93 and max(map(int, primary_hist[0])) == 3 and max(map(int, primary_hist[1])) == 6, 'primary incumbent caps')
    kg_hist = kg_control()
    require(kg_hist == [{'3': 105}, {'5': 105}], 'KG literal page baseline')
    controls = 0
    for t in range(64):
        internal = [{x for i in range(1, 4) if (t+j*3) % 8 >> (i-1) & 1 for x in sym(i)}
                    for j in range(3)]
        cross = {(i, j): {k for k in range(7) if ((t+11*i+19*j)*37) % 128 >> k & 1}
                 for i in range(3) for j in range(i+1, 3)}
        fixed = tuple(bool(t >> i & 1) for i in range(3))
        validate_identities(internal, cross, fixed)
        controls += 1
    # p17 scalar contradiction and the complete allowable orbit-size list.
    require(90 > 10*3+6*6 and 18-10 > 6 and 9-2 > 3, 'large-prime bounds')
    orbit_sizes = sorted({2**i*3**j for i in range(5) for j in range(3) if 2**i*3**j <= 22})
    failures = 0
    damaged = []
    data = copy.deepcopy(records);data.pop();damaged.append(data)
    data = copy.deepcopy(records);data[1]['h'] = 0;damaged.append(data)
    data = copy.deepcopy(records);data[0]['color'] = 'red';damaged.append(data)
    data = copy.deepcopy(records);data[0]['pages'][0] = 0;damaged.append(data)
    data = copy.deepcopy(records);data[1]['pages'].pop();damaged.append(data)
    data = copy.deepcopy(records);data[1]['spine'] = [0, 0];damaged.append(data)
    for data in damaged:
        rejected = False
        try:
            validate_books(data)
        except ValueError:
            rejected = True
        require(rejected, 'damaged phase evidence accepted')
        failures += 1
    bad_rows = [set(r) for r in primary];bad_rows[0].add(0)
    rejected = False
    try:
        page_histograms(bad_rows)
    except ValueError:
        rejected = True
    require(rejected, 'literal loop accepted');failures += 1
    # The wrong cross orientation must disagree with at least one literal phase.
    p, q = {0, 2, 5}, {1, 2, 3}
    require(any(len(p & shift(q, k)) != len(p & shift(reverse(q), k)) for k in range(7)), 'orientation fault not detected')
    failures += 1
    return {'one_cycle_packing': [list(x) for x in k1], 'fixed_partition_tuples': len(k2),
            'two_cycle_packing': [list(x) for x in joined], 'A_margin_states': 16,
            'A_admissible_mn': margins, 'outside_energy': outside,
            'three_set_vectors': vec_counts, 'single_outside_cycle_masks': single_two,
            'single_outside_complement_masks': single_four, 'phase_count': len(records),
            'phase_allowed_h': allowed_h, 'primary_red_histogram': primary_hist[0],
            'primary_blue_histogram': primary_hist[1], 'KG_histograms': kg_hist,
            'allowed_global_orbit_sizes': orbit_sizes,
            'literal_identity_graphs': controls+8, 'literal_identity_spines': 231*(controls+7)+210,
            'primary_spines': 210, 'damaged_or_fault_controls': failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=HERE/'expected.json')
    parser.add_argument('--books', type=Path, default=HERE/'phase_books.json')
    parser.add_argument('--primary', type=Path, default=HERE/'primary21.rows')
    args = parser.parse_args()
    actual = compute(args.books, args.primary)
    expected = json.loads(args.expected.read_text())['check']
    require(actual == expected, 'compact expected checker output mismatch')
    print(json.dumps(actual, sort_keys=True))


if __name__ == '__main__':
    main()

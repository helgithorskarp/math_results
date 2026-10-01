"""six-reviewer-2: independent ordinary odd-prime proof checks, stdlib only."""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random


def require(condition, message):
    if not condition:
        raise ValueError(message)


def compact(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def corr(points, p=7):
    """Unordered difference-class inventory, independent of shift intersections."""
    out = [0] * p
    out[0] = len(points)
    for a, b in combinations(sorted(points), 2):
        d = (b-a) % p
        out[d] += 1
        out[-d % p] += 1
    return tuple(out)


def pair(d, p=7):
    return frozenset((d % p, -d % p))


def ap(h, d):
    return frozenset(((h-d) % 7, h % 7, (h+d) % 7))


def orbit_graph(internal, cross, fixed=(1, 0, 0), p=7):
    """Union of complete edge orbits; no author graph construction imported."""
    n = len(internal)*p + (fixed is not None)
    rows = [set() for _ in range(n)]
    def edge(a, b):
        require(a != b, 'loop in edge orbit')
        rows[a].add(b)
        rows[b].add(a)
    for block, D in enumerate(internal):
        require(0 not in D and D == {-x % p for x in D}, 'invalid internal orbit')
        for offset in range(p):
            for step in D:
                edge(block*p+offset, block*p+(offset+step) % p)
    for (a, b), S in cross.items():
        require(a < b, 'cross orbit ordering')
        for offset in range(p):
            for step in S:
                edge(a*p+offset, b*p+(offset+step) % p)
    if fixed is not None:
        for block, bit in enumerate(fixed):
            if bit:
                for offset in range(p):
                    edge(n-1, block*p+offset)
    return rows


def validate_rows(rows):
    n = len(rows)
    for i, row in enumerate(rows):
        require(i not in row, 'literal loop')
        require(all(type(j) is int and 0 <= j < n for j in row), 'literal range')
        require(all(i in rows[j] for j in row), 'literal asymmetry')


def all_pages(rows):
    validate_rows(rows)
    V = set(range(len(rows)))
    records = []
    for i, j in combinations(range(len(rows)), 2):
        red = j in rows[i]
        pages = rows[i] & rows[j] if red else V - (rows[i] | rows[j] | {i, j})
        records.append((i, j, red, tuple(sorted(pages))))
    return records


def histograms(records):
    return [{str(k): v for k, v in sorted(Counter(len(p) for i, j, red, p in records if red == color).items())}
            for color in (True, False)]


def phase(h):
    return orbit_graph([pair(1), frozenset(range(1, 7))-pair(2),
                        frozenset(range(1, 7))-pair(1)],
                       {(0, 1): ap(0, 2), (0, 2): ap(0, 3), (1, 2): ap(h, 1)})


def validate_books(books):
    require(type(books) is list and len(books) == 7, 'phase coverage length')
    seen = set()
    for book in books:
        require(set(book) == {'h', 'spine', 'color', 'pages', 'degrees_histogram'}, 'book schema')
        h = book['h']
        require(type(h) is int and h in range(7) and h not in seen, 'phase label')
        seen.add(h)
        rows = phase(h)
        require(book['degrees_histogram'] == {'7': 1, '9': 7, '10': 14}, 'degree record')
        require(len(book['spine']) == 2, 'spine length')
        i, j = book['spine']
        require(type(i) is int and type(j) is int and 0 <= i < j < 22, 'spine range')
        require(book['color'] in ('red', 'blue'), 'color alphabet')
        record = next(r for r in all_pages(rows) if r[:2] == (i, j))
        require(record[2] == (book['color'] == 'red'), 'book color')
        require(type(book['pages']) is list and all(type(v) is int for v in book['pages']), 'page type')
        require(tuple(book['pages']) == record[3], 'complete literal pages')
        require(len(record[3]) >= (4 if record[2] else 7), 'forbidden book size')
    require(seen == set(range(7)), 'phase coverage')


def primary(path):
    lines = path.read_text().splitlines()
    require(len(lines) == 21 and all(len(x) == 21 and set(x) <= {'0', '1'} for x in lines), 'primary schema')
    rows = [{j for j, bit in enumerate(line) if bit == '1'} for line in lines]
    pages = all_pages(rows)
    require(Counter(map(len, rows)) == {8: 4, 9: 16, 10: 1}, 'primary degrees')
    require(sum(map(len, rows))//2 == 93 and [max(map(int, h)) for h in histograms(pages)] == [3, 6], 'primary caps')
    return rows, histograms(pages)


def key(rows):
    return tuple(frozenset(j-7*b for j in rows[7*a] if 7*b <= j < 7*(b+1))
                 for a, b in ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)))


def numeric(K):
    return [sum(1 << i for i in points) for points in K]


def compare_inventory(candidate, records):
    require(type(candidate) is list and all(type(r) is list and len(r) == 6 and all(type(x) is int for x in r) for r in candidate), 'inventory schema')
    require(sorted(candidate) == records, 'entrywise inventory mismatch')


def phase0_orbits():
    rows = phase(0)
    pages = {(i, j): (red, p) for i, j, red, p in all_pages(rows)}
    action = [7*(i//7)+(i+1) % 7 for i in range(21)]+[21]
    unseen = set(pages)
    out = []
    while unseen:
        representative = min(unseen)
        orbit = set()
        i, j = representative
        for unused in range(7):
            orbit.add(tuple(sorted((i, j))))
            i, j = action[i], action[j]
        red, record = pages[representative]
        require(len(orbit) == 7 and all(pages[spine][0] == red and len(pages[spine][1]) == len(record) for spine in orbit), 'phase-zero spine orbit')
        require(orbit <= unseen, 'spine orbits overlap')
        unseen -= orbit
        out.append({'spine': list(representative), 'color': 'red' if red else 'blue', 'pages': len(record), 'orbit_size': len(orbit)})
    require(len(out) == 33 and sum(r['orbit_size'] for r in out) == 231, 'sharp witness coverage')
    offending = {spine for spine, (red, p) in pages.items() if not red and len(p) == 7}
    require(offending == {(i, 7+(i+d) % 7) for i in range(7) for d in (1, 6)}, 'two blue-book orbits')
    return out


def normalized_inventory():
    """Actual point permutations of seven graphs, rather than formal mask formulas."""
    result = set()
    for h, a, u, v, exchange in product(range(7), (1, 2, 3), range(7), range(7), (False, True)):
        base = phase(h)
        image = [a*i % 7 for i in range(7)]
        image += [7+(a*i+u) % 7 for i in range(7)]
        image += [14+(a*i+v) % 7 for i in range(7)]
        image += [21]
        if exchange:
            image = [j+7 if 7 <= j < 14 else j-7 if 14 <= j < 21 else j for j in image]
        require(set(image) == set(range(22)), 'normalization point map')
        transformed = [set() for _ in range(22)]
        for i, row in enumerate(base):
            transformed[image[i]] = {image[j] for j in row}
        result.add(key(transformed))
    require(len(result) == 2058, 'actual normalized carrier')
    return result


def factorized_inventory():
    V = frozenset(range(7))
    words = [frozenset(s) for r in range(8) for s in combinations(range(7), r)]
    C = {S: corr(S) for S in words}
    internals = [S for S in words if 0 not in S and S == {-i % 7 for i in S}]
    triples = [S for S in words if len(S) == 3]
    small = [S for S in words if len(S) <= 3]
    require(len(words) == 128 and len(internals) == 8, 'subset coverage')
    for S in words:
        require(sum(C[S][1:]) == len(S)*(len(S)-1), 'correlation energy')
        for k in range(7):
            require(C[S][k] == sum((i+k) % 7 in S for i in S), 'direct correlation oracle')
    triples_by_vector = Counter(C[S][1:4] for S in triples)
    require(triples_by_vector == {(2, 1, 0): 7, (0, 2, 1): 7, (1, 0, 2): 7, (1, 1, 1): 14}, 'triple difference types')
    Akeys = set()
    Ainputs = 0
    for D in internals:
        if len(D) > 3:
            continue
        for P, R in product(small, repeat=2):
            Ainputs += 1
            degree = 1+len(D)+len(P)+len(R)
            if all(1+C[D][k]+C[P][k]+C[R][k] <= 3 if k in D else
                   20-2*degree+1+C[D][k]+C[P][k]+C[R][k] <= 6 for k in range(1, 7)):
                Akeys.add((D, P, R))
    require(Ainputs == 16384 and all(len(D) == 2 and len(P) == len(R) == 3 for D, P, R in Akeys), 'root-local scalar reduction')
    tables = {}
    single_counts = {}
    family = set()
    joins = 0
    for s in (0, 2, 4, 6):
        options = defaultdict(list)
        for Q in words:
            if len(Q) != 7-s:
                continue
            for D in internals:
                if len(D) != s:
                    continue
                for P in triples:
                    if all(C[D][k]+C[P][k]+C[Q][k] <= (3 if k in D else 6) for k in range(1, 7)):
                        options[Q].append((D, P))
        single_counts[str(s)] = sum(map(len, options.values()))
        start = len(family)
        for Q, values in options.items():
            for (DB, P), (DC, R) in product(values, repeat=2):
                for DA in internals:
                    if len(DA) != 2:
                        continue
                    joins += 1
                    if (DA, P, R) in Akeys:
                        K = (DA, DB, DC, P, R, Q)
                        require(K not in family, 'duplicate factorized key')
                        family.add(K)
        tables[str(s)] = len(family)-start
    require(single_counts == {'0': 0, '2': 147, '4': 294, '6': 0}, 'single outside inventory')
    require(tables == {'0': 0, '2': 0, '4': 2058, '6': 0}, 'factorized family')
    require(family == normalized_inventory(), 'actual normalization does not cover every internal key')
    failed = Counter()
    for DA, DB, DC, P, R, Q in sorted(family, key=numeric):
        rows = orbit_graph([DA, DB, DC], {(0, 1): P, (0, 2): R, (1, 2): Q})
        require(list(map(len, rows)) == [9]*7+[10]*14+[7], 'derived family degrees')
        record = next((r for r in all_pages(rows) if len(r[3]) > (3 if r[2] else 6)), None)
        require(record is not None, 'literal complete survivor')
        failed['red' if record[2] else 'blue'] += 1
    records = sorted(map(numeric, family))
    return records, {'A_inputs': Ainputs, 'A_internal_keys': len(Akeys),
                     'single_outside_keys': single_counts, 'factorized_joins': joins,
                     'internal_family_by_s': tables, 'internal_family_count': len(family),
                     'actual_point_normalization_exact': True, 'literal_first_failures': dict(sorted(failed.items())),
                     'complete_survivors': 0, 'inventory_sha256': sha256(compact(records)).hexdigest()}


def formula_controls():
    rng = random.Random(8810)
    graphs = spines = 0
    for flags in product((0, 1), repeat=3):
        for trial in range(16):
            D = [frozenset(x for d in (1, 2, 3) if rng.randrange(2) for x in pair(d)) for _ in range(3)]
            X = {(a, b): frozenset(i for i in range(7) if rng.randrange(2)) for a, b in combinations(range(3), 2)}
            rows = orbit_graph(D, X, flags)
            M = [[frozenset() for _ in range(3)] for _ in range(3)]
            for a in range(3):
                M[a][a] = D[a]
            for (a, b), S in X.items():
                M[a][b] = S
                M[b][a] = frozenset(-i % 7 for i in S)
            for i, j, red, pages in all_pages(rows):
                common = sum(k in rows[i] and k in rows[j] for k in range(22))
                if j == 21:
                    formula = sum(len(M[i//7][b]) for b in range(3) if flags[b])
                else:
                    a, b = i//7, j//7
                    difference = (j-i) % 7
                    formula = sum(sum((k-difference) % 7 in M[b][c] for k in M[a][c]) for c in range(3))
                    formula += flags[a]*flags[b]
                require(formula == common, 'oriented orbit count')
                brute = tuple(k for k in range(22) if k not in (i, j) and
                              ((k in rows[i] and k in rows[j]) if red else (k not in rows[i] and k not in rows[j])))
                require(pages == brute, 'literal third-vertex oracle')
                if not red:
                    require(len(pages) == 20-len(rows[i])-len(rows[j])+common, 'blue inclusion-exclusion')
                spines += 1
            graphs += 1
    small = 0
    for code in range(64):
        rows = [set() for _ in range(4)]
        for bit, (i, j) in enumerate(combinations(range(4), 2)):
            if code >> bit & 1:
                rows[i].add(j); rows[j].add(i)
        for i, j, red, pages in all_pages(rows):
            require(pages == tuple(k for k in range(4) if k not in (i, j) and
                                  ((k in rows[i] and k in rows[j]) if red else (k not in rows[i] and k not in rows[j]))), 'four-point oracle')
        small += 1
    return {'arbitrary_graphs': graphs, 'arbitrary_spines': spines, 'four_point_graphs': small, 'seed': 8810}


def remaining_checks(books, primary_path):
    validate_books(books)
    _, primary_hist = primary(primary_path)
    one = [(15-l, l, s) for l in range(16) for s in (0, 2, 4, 6) if l <= 5 and 15-l+s <= 10]
    two = [(a, b, 8-a-b) for a in range(9) for b in range(9-a) if a and b and a+8-a-b <= 4 and b+8-a-b <= 4]
    require(one == [(10, 5, 0)] and two == [(4, 4, 0)], 'fixed point partitions')
    energies = [[s, 7-s, s*(s-1)+6+(7-s)*(6-s), 3*s+6*(6-s)] for s in (0, 2, 4, 6)]
    require([s for s, q, l, u in energies if l <= u] == [2, 4], 'outside energy')
    phases = []
    for h in range(7):
        rows = phase(h)
        records = all_pages(rows)
        rotate = [7*(i//7)+(i+1) % 7 for i in range(21)]+[21]
        require(all({rotate[j] for j in rows[i]} == rows[rotate[i]] for i in range(22)), 'actual order-seven action')
        maxima = [max(len(p) for i, j, red, p in records if red == color) for color in (True, False)]
        phases.append({'h': h, 'red_max': maxima[0], 'blue_max': maxima[1], 'histograms': histograms(records)})
    require([x['red_max'] for x in phases] == [3, 4, 4, 4, 4, 4, 4], 'sharp red phase')
    require(phases[0]['blue_max'] == 7, 'sharp blue capacity control')
    p17 = []
    for chosen in combinations(range(1, 9), 5):
        D = frozenset(x for d in chosen for x in pair(d, 17))
        rows = orbit_graph([D], {}, None, p=17)
        rows += [set() for _ in range(5)]
        for i, j in combinations(range(17, 22), 2):
            rows[i].add(j); rows[j].add(i)
        records = all_pages(rows)
        require(any(len(p) > (3 if red else 6) for i, j, red, p in records), 'seventeen-cycle survivor')
        p17.append(sum(corr(D, 17)[1:]))
    require(len(p17) == 56 and set(p17) == {90} and 90 > 10*3+6*6, 'seventeen-cycle energy')
    p13 = orbit_graph([frozenset()], {}, None, p=13)+[set() for _ in range(9)]
    for i, j in combinations(range(13, 22), 2):
        p13[i].add(j);p13[j].add(i)
    require(len(p13[13] & p13[14]) == 7, 'thirteen fixed clique')
    require(all(18-s > 6 for s in (0, 2, 4, 6, 8, 10)), 'nineteen fixed-cycle spine')
    roots = [frozenset(s) for s in combinations(range(7), 2)]
    kg = [{j for j, T in enumerate(roots) if S.isdisjoint(T)} for S in roots]
    require(histograms(all_pages(kg)) == [{'3': 105}, {'5': 105}], 'KG21 positive control')
    damaged = []
    for change in range(6):
        b = deepcopy(books)
        if change == 0: b.pop()
        elif change == 1: b[1]['h'] = 0
        elif change == 2: b[0]['color'] = 'red'
        elif change == 3: b[0]['pages'][0] = -1
        elif change == 4: b[0]['pages'].append(b[0]['pages'][0])
        else: b[0]['spine'] = [0, 0]
        try:
            validate_books(b)
        except ValueError:
            damaged.append(change)
        else:
            raise ValueError('damaged phase book accepted')
    try:
        all_pages([{0}])
    except ValueError:
        damaged.append('loop')
    else:
        raise ValueError('loop accepted')
    conditional = sorted({2**a*3**b*5**c for a in range(5) for b in range(3) for c in range(2) if 2**a*3**b*5**c <= 22})
    combined = sorted({2**a*3**b for a in range(5) for b in range(3) if 2**a*3**b <= 22})
    require(conditional == [1,2,3,4,5,6,8,9,10,12,15,16,18,20] and combined == [1,2,3,4,6,8,9,12,16,18], 'group scope')
    return {'one_cycle': one, 'two_cycles': two, 'outside_energy': energies,
            'phases': phases, 'p17_masks': len(p17), 'p17_energy': 90, 'p17_upper': 66,
            'primary_histograms': primary_hist, 'KG21_histograms': histograms(all_pages(kg)),
            'damaged_rejections': damaged, 'conditional_orbit_sizes': conditional,
            'combined_orbit_sizes': combined}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    here = Path(__file__).resolve().parent
    parser.add_argument('--books', type=Path, default=here/'PHASE_BOOKS.json')
    parser.add_argument('--primary', type=Path, default=here/'PRIMARY21.rows')
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--compare-author-records', type=Path)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    records, enumeration = factorized_inventory()
    result = {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer',
              'complete': True, 'factorized_inventory': enumeration,
              'controls': formula_controls(),
              'ordinary_checks': remaining_checks(json.loads(args.books.read_text()), args.primary),
              'phase0_spine_orbits': phase0_orbits()}
    compare_inventory(records, records)
    for bad in (records[:-1], records[:-1]+[records[0]], [[0]+records[0][1:]]+records[1:]):
        try:
            compare_inventory(bad, records)
        except ValueError:
            pass
        else:
            raise ValueError('damaged inventory accepted')
    result['controls']['damaged_inventory_rejections'] = 3
    if args.compare_author_records is not None:
        author = json.loads(args.compare_author_records.read_text())
        compare_inventory(author, records)
    encoded = compact(result)+b'\n'
    if args.expected is not None:
        require(encoded == compact(json.loads(args.expected.read_text()))+b'\n', 'expected record mismatch')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir/'RESULT.json').write_bytes(encoded)
    (args.output_dir/'INTERNAL_RECORDS.json').write_bytes(compact(records)+b'\n')
    (args.output_dir/'PHASE0.rows').write_text(''.join(''.join('1' if j in r else '0' for j in range(22))+'\n' for r in phase(0)))
    print(encoded.decode(), end='')


if __name__ == '__main__':
    main()

"""Independent bitset validation; the template scan is supplementary only."""
import argparse
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FULL = 127


def ensure(test, message):
    if not test:
        raise RuntimeError(message)


def rotate(word, shift):
    shift %= 7
    return ((word << shift) | (word >> (7-shift))) & FULL


def reverse(word):
    return sum(1 << ((-i) % 7) for i in range(7) if word >> i & 1)


def pair(step):
    return (1 << (step % 7)) | (1 << ((-step) % 7))


def ap(center, step):
    return sum(1 << ((center+k*step) % 7) for k in (-1, 0, 1))


def block_rows(d, p, flags=(1, 0, 0)):
    m = [[d[0], p[0], p[1]], [reverse(p[0]), d[1], p[2]],
         [reverse(p[1]), reverse(p[2]), d[2]]]
    rows = []
    for i in range(3):
        for offset in range(7):
            word = sum(rotate(m[i][j], offset) << (7*j) for j in range(3))
            if flags is not None and flags[i]:
                word |= 1 << 21
            rows.append(word)
    if flags is not None:
        rows.append(sum(FULL << (7*i) for i in range(3) if flags[i]))
    return rows, m


def histograms(rows):
    n = len(rows)
    universe = (1 << n)-1
    out = [{}, {}]
    for i, row in enumerate(rows):
        ensure(row & ~universe == 0 and not row >> i & 1, 'literal range or loop')
        for j in range(i+1, n):
            red = row >> j & 1
            ensure(red == (rows[j] >> i & 1), 'literal asymmetry')
            count = (row & rows[j]).bit_count() if red else (universe & ~(row | rows[j] | (1 << i) | (1 << j))).bit_count()
            h = out[0 if red else 1]
            h[count] = h.get(count, 0)+1
    return [{str(k): v for k, v in sorted(h.items())} for h in out]


def validate_literal(d, p, flags=(1, 0, 0)):
    rows, m = block_rows(d, p, flags)
    n = len(rows)
    universe = (1 << n)-1
    for i in range(n):
        for j in range(i+1, n):
            common = (rows[i] & rows[j]).bit_count()
            if j == 21:
                formula = sum(m[i//7][k].bit_count() for k in range(3) if flags[k])
            else:
                a, b = i//7, j//7
                formula = sum((m[a][k] & rotate(m[b][k], j-i)).bit_count() for k in range(3))
                if flags is not None:
                    formula += int(flags[a] and flags[b])
            ensure(formula == common, 'literal oriented orbit identity')
            if not rows[i] >> j & 1:
                blue = (universe & ~(rows[i] | rows[j] | (1 << i) | (1 << j))).bit_count()
                ensure(blue == n-2-rows[i].bit_count()-rows[j].bit_count()+formula, 'blue complement identity')
    histograms(rows)
    return rows


def primary_rows(path):
    lines = path.read_bytes().splitlines()
    ensure(len(lines) == 21 and all(len(line) == 21 and set(line) <= {48, 49} for line in lines), 'primary rows shape/alphabet')
    rows = [sum(1 << j for j, bit in enumerate(line) if bit == 49) for line in lines]
    histograms(rows)
    return rows


def kg_baseline():
    roots = [(1 << i) | (1 << ((i+d) % 7)) for d in (1, 2, 3) for i in range(7)]
    ensure(len(set(roots)) == 21, 'KG root labels')
    rows = [sum(1 << j for j, q in enumerate(roots) if q & r == 0) for r in roots]
    for i, root in enumerate(roots):
        ensure(rotate(root, 1) == roots[7*(i//7)+(i+1) % 7], 'KG seven-cycle action')
    d = [rows[7*i] >> (7*i) & FULL for i in range(3)]
    p = [rows[0] >> 7 & FULL, rows[0] >> 14 & FULL, rows[7] >> 14 & FULL]
    ensure(validate_literal(d, p, None) == rows, 'KG block identity')
    ensure(all(r.bit_count() == 10 for r in rows), 'KG red degrees')
    return histograms(rows)


def validate_books(records):
    ensure(len(records) == 7 and {r['h'] for r in records} == set(range(7)), 'phase book coverage')
    d = [pair(1), (FULL ^ 1) ^ pair(2), (FULL ^ 1) ^ pair(1)]
    for record in records:
        h = record['h']
        ensure(type(h) is int and 0 <= h < 7, 'phase range')
        p = [ap(0, 2), ap(0, 3), ap(h, 1)]
        rows = validate_literal(d, p)
        ensure([r.bit_count() for r in rows] == [9]*7+[10]*14+[7], 'phase degrees')
        ensure(record['degrees_histogram'] == {'7': 1, '9': 7, '10': 14}, 'phase degree record')
        i, j = record['spine']
        ensure(type(i) is int and type(j) is int and 0 <= i < j < 22, 'phase spine')
        red = record['color'] == 'red'
        ensure(record['color'] in ('red', 'blue') and (rows[i] >> j & 1) == red, 'phase spine color')
        pages = record['pages']
        ensure(all(type(v) is int and 0 <= v < 22 for v in pages) and len(pages) == len(set(pages)), 'phase page range or repeats')
        mask = sum(1 << v for v in pages)
        actual = rows[i] & rows[j] if red else ((1 << 22)-1) & ~(rows[i] | rows[j] | (1 << i) | (1 << j))
        ensure(mask == actual and len(pages) >= (4 if red else 7), 'phase book pages')


def compute(books_path, primary_path):
    records = json.loads(books_path.read_text())
    validate_books(records)
    primary = primary_rows(primary_path)
    primary_hist = histograms(primary)
    ensure(sum(r.bit_count() for r in primary)//2 == 93, 'primary red edges')
    ensure(max(map(int, primary_hist[0])) == 3 and max(map(int, primary_hist[1])) == 6, 'primary book caps')
    kg_hist = kg_baseline()
    ensure(kg_hist == [{'3': 105}, {'5': 105}], 'KG book caps')
    internal = {s: [] for s in (0, 2, 4, 6)}
    for code in range(8):
        d = sum(pair(i) for i in range(1, 4) if code >> (i-1) & 1)
        internal[d.bit_count()].append(d)
    by_size = {s: [word for word in range(128) if word.bit_count() == s] for s in range(8)}
    rotated = [[rotate(w, k) for k in range(7)] for w in range(128)]
    correlations = [[(w & rotated[w][k]).bit_count() for k in range(1, 4)] for w in range(128)]
    control_count = 0
    all_internal = [d for values in internal.values() for d in values]
    for number in range(48):
        d = [all_internal[(number*j+j) % 8] for j in (1, 3, 5)]
        p = [((number+11*j)*53) % 128 for j in (1, 2, 3)]
        flags = tuple((number >> j) & 1 for j in range(3))
        validate_literal(d, p, flags)
        control_count += 1
    families = {}
    good_internal = set()
    for s in (0, 2, 4, 6):
        qdomain = by_size[7-s]
        outside = internal[s]
        counts = dict(domain=0, A=0, B=0, C=0, cross=0, survivors=0)
        for da in internal[2]:
            for p in by_size[3]:
                for r in by_size[3]:
                    if any(correlations[da][k-1]+correlations[p][k-1]+correlations[r][k-1] >
                           (2 if da >> k & 1 else 3) for k in range(1, 4)):
                        # Every completion has this same failed A spine.
                        multiplicity = len(outside)**2*len(qdomain)
                        counts['domain'] += multiplicity
                        counts['A'] += multiplicity
                        continue
                    for db in outside:
                        for dc in outside:
                            for q in qdomain:
                                counts['domain'] += 1
                                if any(correlations[db][k-1]+correlations[p][k-1]+correlations[q][k-1] >
                                       (3 if db >> k & 1 else 6) for k in range(1, 4)):
                                    counts['B'] += 1
                                    continue
                                if any(correlations[dc][k-1]+correlations[r][k-1]+correlations[q][k-1] >
                                       (3 if dc >> k & 1 else 6) for k in range(1, 4)):
                                    counts['C'] += 1
                                    continue
                                key = (da, db, dc, p, r, q)
                                ensure(key not in good_internal, 'duplicate internal template')
                                good_internal.add(key)
                                m = [[da, p, r], [reverse(p), db, q], [reverse(r), reverse(q), dc]]
                                found = False
                                for i, j in ((0, 1), (0, 2), (1, 2)):
                                    for offset in range(7):
                                        red = m[i][j] >> offset & 1
                                        pages = sum((m[i][k] & rotated[m[j][k]][offset]).bit_count() for k in range(3))
                                        bound = 3 if red else (9, 10, 10)[i]+(9, 10, 10)[j]-14
                                        if pages > bound:
                                            found = True
                                            break
                                    if found:
                                        break
                                counts['cross' if found else 'survivors'] += 1
        ensure(sum(counts[key] for key in ('A', 'B', 'C', 'cross', 'survivors')) == counts['domain'], 'incomplete accounting')
        ensure(counts['survivors'] == 0, 'derived branch contains a survivor')
        families[str(s)] = counts
    # Independently construct the exact orbit/center family predicted by the proof.
    predicted = set()
    for a in (1, 2, 3):
        for exchange in (False, True):
            for u, v, w in itertools.product(range(7), repeat=3):
                if exchange:
                    db, dc = (FULL ^ 1) ^ pair(a), (FULL ^ 1) ^ pair(2*a)
                    p, r = ap(u, 3*a), ap(v, 2*a)
                else:
                    db, dc = (FULL ^ 1) ^ pair(2*a), (FULL ^ 1) ^ pair(a)
                    p, r = ap(u, 2*a), ap(v, 3*a)
                predicted.add((pair(a), db, dc, p, r, ap(w, a)))
    ensure(len(predicted) == 2058 and good_internal == predicted, 'normalization family does not match complete internal survivors')
    total = sum(f['domain'] for f in families.values())
    ensure(total == 1881600, 'derived domain coverage')
    return {'families': families, 'derived_domain': total,
            'normalized_family_members': len(predicted), 'normalization_full_set_equality': True,
            'phase_books': len(records), 'primary_histograms': primary_hist,
            'KG_histograms': kg_hist, 'literal_identity_graphs': control_count+8,
            'literal_identity_spines': 231*(control_count+7)+210, 'primary_spines': 210}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=HERE/'expected.json')
    parser.add_argument('--books', type=Path, default=HERE/'phase_books.json')
    parser.add_argument('--primary', type=Path, default=HERE/'primary21.rows')
    args = parser.parse_args()
    actual = compute(args.books, args.primary)
    expected = json.loads(args.expected.read_text())['verify']
    ensure(actual == expected, 'compact expected verifier output mismatch')
    print(json.dumps(actual, sort_keys=True))


if __name__ == '__main__':
    main()

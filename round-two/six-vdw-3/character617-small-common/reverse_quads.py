"""Generate all anchored threshold-four quadruples by descending largest-row traversal."""
import argparse
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--start', type=int, required=True)
    p.add_argument('--stop', type=int, required=True)
    p.add_argument('--output', type=Path, required=True)
    o = p.parse_args()
    rows = sorted({pow(q, 2, 617) for q in range(1, 617)})
    columns = sorted(set(range(1, 617)) - set(rows))
    if not 3 <= o.start < o.stop <= len(rows):
        raise ValueError('Complete disjoint largest-row domain')
    supports = []
    for d in (285, 314, 362, 381, 409, 570):
        positions = []
        r = 1
        for _ in range(6):
            r = (r + d) % 617
            positions.append(r)
        supports.append(positions)
    positive = set().union(*map(set, supports))
    inverse = {q: next(k for k in range(1, 617) if q * k % 617 == 1) for q in range(1, 617)}
    ratios = positive | {inverse[t] for t in positive}
    if len(rows) != 308 or len(positive) != 33 or len(ratios) != 66 or positive & {inverse[t] for t in positive}:
        raise ValueError('Literal endpoint field graph')
    neighborhoods = []
    for q in rows:
        physical = [t for t in columns if t * inverse[q] % 617 in ratios]
        if len(physical) != 66:
            raise ValueError('Literal all-column neighborhood')
        neighborhoods.append(sum(1 << t for t in physical))
    records = []
    tested = [0, 0, 0]
    for z in range(o.start, o.stop):
        tested[0] += 1
        cz = neighborhoods[0] & neighborhoods[z]
        if cz.bit_count() < 4:
            continue
        for y in range(z - 1, 1, -1):
            tested[1] += 1
            cy = cz & neighborhoods[y]
            if cy.bit_count() < 4:
                continue
            for x in range(y - 1, 0, -1):
                tested[2] += 1
                cx = cy & neighborhoods[x]
                if cx.bit_count() >= 4:
                    records.append({'A': [1, rows[x], rows[y], rows[z]],
                                    'C': [t for t in columns if cx >> t & 1]})
    records.sort(key=lambda r: r['A'])
    result = {'schema': 'character617-reverse-quad-part-v1', 'start': o.start, 'stop': o.stop,
              'tested': tested, 'records': records}
    o.output.write_text(json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n')


if __name__ == '__main__':
    main()

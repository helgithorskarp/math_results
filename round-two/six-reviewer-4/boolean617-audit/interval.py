"""Fresh actual-integer unit implications, independently checked."""
import argparse
import json
from field import P, gauss, need, squares

N = 3704

def generate(t):
    roots = (1, 2, t)
    table = gauss()
    cases = []
    for root in roots:
        candidates = []
        fixed = [None if n % P in roots else table[(n-root) % P] for n in range(N+1)]
        for column in (q for q in (1, 2) if q != root):
            target_color = table[(column-root) % P]
            units = []
            for m in range(column, N+1, P):
                answer = None
                for d in range(1, P):
                    for slot in range(7):
                        a = m-slot*d
                        if a < 1 or a+6*d > N:
                            continue
                        if all(fixed[a+j*d] == 1-target_color for j in range(7) if j != slot):
                            answer = [m, a, d, slot]
                            break
                    if answer is not None:
                        break
                if answer is None:
                    break
                units.append(answer)
            if len(units) == 7:
                candidates.append({'root': root, 'column': column, 'units': units})
                break
        need(candidates, 'unit search incomplete; no exclusion inferred')
        cases.append(candidates[0])
    return {'t': t, 'cases': cases}

def validate(record, expected_t):
    need(type(record) is dict and record['t'] == expected_t and expected_t not in (1, 2), 'physical third root')
    roots = (1, 2, expected_t)
    need([r['root'] for r in record['cases']] == list(roots), 'physical projection coverage')
    table = squares()
    units = 0
    for case in record['cases']:
        root, column = case['root'], case['column']
        need(column in (1, 2) and column != root, 'free vertical column')
        rows = case['units']
        need([row[0] for row in rows] == list(range(column, N+1, P)), 'seven independent occurrences')
        expected = table[(column-root) % P]
        for m, a, d, slot in rows:
            need(all(type(x) is int for x in (m, a, d, slot)) and 1 <= a and 1 <= d and 0 <= slot <= 6 and a+6*d <= N, 'integer AP bounds')
            need(m == a+slot*d, 'target occurrence identity')
            points = [a+j*d for j in range(7) if j != slot]
            need(all(n % P not in roots for n in points), 'six fixed supports avoid every original root')
            need(all(table[(n-root) % P] == 1-expected for n in points), 'six opposing literal colors')
            units += 1
        vertical = list(range(column, N+1, P))
        need(len(vertical) == 7 and all(n % P == column for n in vertical), 'vertical contradiction')
    return units

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['generate', 'validate', 'batch', 'check_batch'])
    parser.add_argument('value')
    args = parser.parse_args()
    if args.action == 'batch':
        lower, upper = map(int, args.value.split(':'))
        print(json.dumps([generate(t) for t in range(lower, upper) if t not in (1, 2)], sort_keys=True))
    elif args.action == 'check_batch':
        lower, upper = map(int, args.value.split(':')[1:])
        records = json.load(open(args.value.split(':')[0]))
        need([r['t'] for r in records] == [t for t in range(lower, upper) if t not in (1, 2)], 'entire physical batch')
        print(json.dumps({'third_roots': len(records), 'verified_integer_units': sum(validate(r, r['t']) for r in records)}, sort_keys=True))
    elif args.action == 'generate':
        print(json.dumps(generate(int(args.value)), sort_keys=True))
    else:
        record = json.load(open(args.value))
        print(json.dumps({'t': record['t'], 'verified_integer_units': validate(record, record['t'])}, sort_keys=True))

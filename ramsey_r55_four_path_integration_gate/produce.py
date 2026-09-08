"""Exact lower-bound certificate for the declared direct four-path carrier."""
from itertools import combinations, product
from math import comb, factorial
import json


def block(kind):
    n = 5 if kind == 'P' else 4
    return n, {(i, j) for i, j in combinations(range(n), 2)
               if (j == i + 1 if kind == 'P' else kind == 'K')}


def events(left, right):
    n, red = block(left)
    m, second = block(right)
    out = []
    for color in (0, 1):
        for k in range(1, 5):
            for s, t in product(combinations(range(n), k),
                                combinations(range(m), 5-k)):
                if all(int(e in red) == color for e in combinations(s, 2)) and all(
                        int(e in second) == color for e in combinations(t, 2)):
                    out.append({'color': color, 'left': list(s), 'right': list(t),
                                'mask': sum(1 << (m*i+j) for i in s for j in t)})
    return out


def allowed(word, ev):
    return all((word & e['mask']) != (e['mask'] if e['color'] else 0) for e in ev)


def canonical_columns(word):
    return tuple(sorted(sum(((word >> (4*i+j)) & 1) << i for i in range(4))
                        for j in range(4)))


def make():
    event_lists = {key: events(*key) for key in ('PP', 'PK', 'KK', 'KB')}
    bounds = {}
    for key in ('PP', 'PK'):
        bits = block(key[0])[0] * block(key[1])[0]
        bounds[key] = (1 << bits) - sum(1 << (bits-e['mask'].bit_count())
                                       for e in event_lists[key])
    exact, root = {}, {}
    for key in ('KK', 'KB'):
        domain = [w for w in range(1 << 16) if allowed(w, event_lists[key])]
        exact[key] = len(domain)
        root[key] = len({canonical_columns(w) for w in domain})
    counts = {3: 4, 7: 362, 11: 546356, 15: 640}
    baseline = []
    for q in range(7, 11):
        for r in range(5, q+1):
            a, b, n = r-1, q-r, 43-4*q
            term = (counts[n] * comb(root['KK']+a-1, a) * comb(root['KB']+b-1, b)
                    * exact['KK']**(comb(a, 2)+comb(b, 2)) * exact['KB']**(a*b)
                    * 15**(q*n))
            baseline.append({'q': q, 'r': r, 'n': n, 'term': term})
    p = sum(row['term'] for row in baseline)
    raw = counts[11] * bounds['PP']**6 * bounds['PK']**12 * exact['KK']**3 * 32**44 * 15**33
    group = 2**4 * factorial(4) * factorial(4)**3 * factorial(3)
    return {'format': 'four-path-gate-v1', 'events': event_lists,
            'pair_lower_bounds': bounds, 'pair_exact_counts': exact, 'root_counts': root,
            'core_counts': {str(k): v for k, v in counts.items()}, 'baseline_terms': baseline,
            'P': p, 'macro_raw_lower': raw, 'group_order': group,
            'normalized_lower': (raw+group-1)//group,
            'raw_to_group_P_floor': raw//(group*p),
            'status': 'DIRECT_INTEGRATION_REDUCTION_GATE_FAILED'}


if __name__ == '__main__':
    print(json.dumps(make(), indent=2, sort_keys=True))

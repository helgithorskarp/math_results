"""Exact conditional occupancy obstruction, Python integer/set computation."""
from itertools import combinations, product
import json
from math import gcd, prod

S = tuple(t for t in range(180) if t % 9 != 6)
R0 = frozenset(x for x in range(720) if x % 8 != 5 and x % 9 != 6 and x % 18 != 3)
FIRST = tuple(m for m in range(8, 721) if 720 % m == 0 and m not in (8, 9))
FREE = tuple(d for d in range(2, 721) if 720 % d == 0 and d not in (2, 4))
PAIRS = ((10, 18), (12, 15), (16, 20), (24, 30), (36, 40), (45, 48), (60, 72))
SINGLES = tuple(m for m in FIRST if m not in {x for g in PAIRS for x in g})
PARITY_GROUPS = PAIRS + tuple((m,) for m in SINGLES)
CORE = (10, 12, 15, 16, 18, 20)
TERNARY_GROUPS = (CORE,) + tuple(g for g in PARITY_GROUPS if set(g).isdisjoint(CORE))


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def bits(values):
    return sum(1 << x for x in values)


def shape(identifier):
    if identifier == 4:
        return bits(t for t in S if t % 3 != 0)
    need(0 <= identifier < 4, 'unknown target shape')
    p, b = identifier // 2, identifier % 2 + 1
    return bits(t for t in S if t % 2 == p or t % 3 == b)


def maximum_union(raw, group):
    # Full raw ORIGINAL phase products. No resource or phase is identified.
    count = prod(group)
    if len(group) == 6:
        left = [a | b | c | d for a in raw[10] for b in raw[12]
                for c in raw[15] for d in raw[18]]
        right = [a | b for a in raw[16] for b in raw[20]]
        need(len(left) * len(right) == count, 'incomplete core phase product')
        maximum = max((a | b).bit_count() for a in left for b in right)
    elif len(group) == 2:
        m, n = group
        maximum = max((a | b).bit_count() for a in raw[m] for b in raw[n])
        need(len(raw[m]) * len(raw[n]) == count, 'incomplete pair phase product')
    else:
        m, = group
        maximum = max(a.bit_count() for a in raw[m])
        need(len(raw[m]) == count, 'incomplete singleton phase product')
    return count, maximum


def compute():
    need(len(S) == 160 and len(R0) == 530 and len(FREE) == 27 and len(FIRST) == 22,
         'domain/inventory mismatch')
    e = {d: d // gcd(d, 4) for d in FREE}
    domains = {d: tuple(sorted({t % e[d] for t in S})) for d in FREE}
    masks = {d: {r: bits(t for t in S if t % e[d] == r) for r in domains[d]} for d in FREE}
    weights = {d: max(v.bit_count() for v in masks[d].values()) for d in FREE}
    cache = {}

    def maxima(U):
        if U not in cache:
            cache[U] = {d: max((U & v).bit_count() for v in masks[d].values()) for d in FREE}
        return cache[U]

    rows, candidates, effective_count, raw_count = [], [], 0, 0
    for d, f in combinations(FREE, 2):
        if weights[d] + weights[f] < 99:
            continue
        candidates.append([d, f])
        raw_count += d * f
        for r, q in product(domains[d], domains[f]):
            effective_count += 1
            U = masks[d][r] | masks[f][q]
            if U.bit_count() < 99:
                continue
            remaining = sum(v for k, v in maxima(U).items() if k not in (d, f))
            bound = min(U.bit_count(), remaining // 4)
            rows.append([d, f, r, q, format(U, '045x'), U.bit_count(), remaining, bound,
                         int(bound >= 99)])
    rows.sort()
    survivors = [row for row in rows if row[-1]]
    allowed = {format(shape(i), '045x') for i in range(5)}
    need(all(row[4] in allowed for row in survivors), 'unclassified sparse-copy union')

    first = []
    for identifier in range(5):
        U = shape(identifier)
        compulsory = R0 - {4 * t for t in S if U >> t & 1}
        F = bits(compulsory)
        raw = {m: [bits(range(a, 720, m)) & F for a in range(m)] for m in FIRST}
        groups = PARITY_GROUPS if identifier < 4 else TERNARY_GROUPS
        need(sorted(m for g in groups for m in g) == list(FIRST), 'non-disjoint ORIGINAL first partition')
        entries = []
        for group in groups:
            count, cap = maximum_union(raw, group)
            entries.append({'moduli': list(group), 'raw_phase_tuples': count, 'maximum': cap})
        total = sum(entry['maximum'] for entry in entries)
        need(total < len(compulsory), 'first-stage compulsory complement not excluded')
        first.append({'shape_id': identifier, 'union_hex': format(U, '045x'),
                      'union_count': U.bit_count(), 'compulsory_count': len(compulsory),
                      'groups': entries, 'total_capacity': total})
    return {'schema': 1, 'floor_used_for_tail_consequence': 99,
            'original_free_d': list(FREE), 'original_first_m': list(FIRST),
            'weights': [[d, weights[d]] for d in FREE],
            'candidate_original_pairs': candidates, 'raw_tail_phase_pairs': raw_count,
            'effective_tail_phase_pairs': effective_count, 'large_union_rows': rows,
            'first_complement_bounds': first,
            'scope': 'conditional normalized720 firststage and29 ORIGINAL7d tail; not a global LCM exclusion'}


if __name__ == '__main__':
    print(json.dumps(compute(), indent=2))

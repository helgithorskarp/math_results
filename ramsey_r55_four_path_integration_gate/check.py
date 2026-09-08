"""Separate physical adjacency / subset / clique audit; imports no producer code."""
from collections import Counter
from itertools import combinations, permutations
from math import factorial
from pathlib import Path
import argparse
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def adjacency(kind):
    size = {'P': 5, 'K': 4, 'B': 4}[kind]
    return [[int(i != j and (abs(i-j) == 1 if kind == 'P' else kind == 'K'))
             for j in range(size)] for i in range(size)]


def physical_events(x, y):
    a, b = adjacency(x), adjacency(y)
    n, m = len(a), len(b)
    found = []
    for vertices in combinations(range(n+m), 5):
        left = [v for v in vertices if v < n]
        right = [v-n for v in vertices if v >= n]
        for c in (0, 1):
            mask = 0
            feasible = True
            for u, v in combinations(vertices, 2):
                if v < n:
                    feasible &= a[u][v] == c
                elif u >= n:
                    feasible &= b[u-n][v-n] == c
                else:
                    mask |= 1 << ((u*m)+(v-n))
            if feasible:
                require(mask > 0, 'unexpected internal forbidden set')
                found.append({'color': c, 'left': left, 'right': right, 'mask': mask})
    return found


def has_clique(rows, size):
    def visit(candidates, need):
        if need == 0:
            return True
        while candidates.bit_count() >= need:
            bit = candidates & -candidates
            candidates ^= bit
            if visit(candidates & rows[bit.bit_length()-1], need-1):
                return True
        return False
    return visit((1 << len(rows))-1, size)


def good(rows):
    full = (1 << len(rows))-1
    complement = [full ^ row ^ (1 << i) for i, row in enumerate(rows)]
    return not has_clique(rows, 5) and not has_clique(complement, 5)


def exact_pairs(second):
    base = [sum(v << j for j, v in enumerate(row)) for row in adjacency('K')]
    base += [sum(v << (j+4) for j, v in enumerate(row)) for row in adjacency(second)]
    count = 0
    orbits = set()
    for word in range(65536):
        rows = base[:]
        for i in range(4):
            for j in range(4):
                if (word >> (i*4+j)) & 1:
                    rows[i] |= 1 << (4+j)
                    rows[4+j] |= 1 << i
        if good(rows):
            count += 1
            orbits.add(tuple(sorted(rows[j] & 15 for j in range(4, 8))))
    return count, len(orbits)


def multiset(m, k):
    # Coefficient of (1-x)^(-m), by adding one available symbol at a time.
    dp = [1] + [0]*k
    for _ in range(m):
        for t in range(1, k+1):
            dp[t] += dp[t-1]
    return dp[k]


def stars(kind):
    a = adjacency(kind)
    n = len(a)
    accepted = 0
    for word in range(1 << n):
        rows = [sum(v << j for j, v in enumerate(row)) | (((word >> i) & 1) << n)
                for i, row in enumerate(a)] + [word]
        accepted += good(rows)
    return accepted


def internal_group(kind):
    a = adjacency(kind)
    return sum(all(a[i][j] == a[p[i]][p[j]] for i in range(len(a)) for j in range(len(a)))
               for p in permutations(range(len(a))))


def coordinate_audit():
    blocks = [list(range(5*i, 5*i+5)) for i in range(4)]
    blocks += [list(range(20+4*i, 24+4*i)) for i in range(3)]
    owner = {v: i for i, block in enumerate(blocks) for v in block}
    tally = Counter()
    for u, v in combinations(range(43), 2):
        i, j = owner.get(u), owner.get(v)
        if i is None and j is None:
            tally['core_fixed'] += 1
        elif j is None:
            tally['P_star' if i < 4 else 'K_star'] += 1
        elif i == j:
            tally['block_fixed'] += 1
        else:
            tally['PP' if j < 4 else 'PK' if i < 4 else 'KK'] += 1
    expected = {'core_fixed': 55, 'block_fixed': 58, 'PP': 150, 'PK': 240,
                'KK': 48, 'P_star': 220, 'K_star': 132}
    require(dict(tally) == expected, 'physical coordinate partition')
    return expected


def validate(cert, expensive=None):
    require(cert['format'] == 'four-path-gate-v1', 'format')
    hist = {}
    for key in ('PP', 'PK', 'KK', 'KB'):
        expected = physical_events(*key)
        norm = lambda e: (e['color'], tuple(e['left']), tuple(e['right']), e['mask'])
        require(sorted(map(norm, cert['events'][key])) == sorted(map(norm, expected)), 'events '+key)
        require(len({norm(e) for e in expected}) == len(expected), 'duplicate events')
        hist[key] = dict(sorted(Counter(f"{e['color']}:{e['mask'].bit_count()}" for e in expected).items()))
    require(hist['PP'] == {'0:6': 12} and hist['PK'] == {'1:4': 5, '1:6': 16}, 'union-bound event volumes')
    lower = {'PP': (1 << 25)-12*(1 << 19),
             'PK': (1 << 20)-5*(1 << 16)-16*(1 << 14)}
    require(cert['pair_lower_bounds'] == lower, 'union bounds')
    if expensive is None:
        expensive = {key: exact_pairs(key[1]) for key in ('KK', 'KB')}
    require(cert['pair_exact_counts'] == {k: v[0] for k, v in expensive.items()}, 'exact pair domains')
    require(cert['root_counts'] == {k: v[1] for k, v in expensive.items()}, 'root column domains')
    require(expensive == {'KK': (37823, 1998), 'KB': (35714, 1931)}, 'upstream domain agreement')
    counts = {'3': 4, '7': 362, '11': 546356, '15': 640}
    require(cert['core_counts'] == counts, 'imported core counts')
    terms = []
    for q in (7, 8, 9, 10):
        for r in range(5, q+1):
            a, b, n = r-1, q-r, 43-4*q
            same = (a*(a-1)+b*(b-1))//2
            term = (counts[str(n)] * multiset(1998, a) * multiset(1931, b)
                    * 37823**same * 35714**(a*b) * 15**(q*n))
            terms.append({'q': q, 'r': r, 'n': n, 'term': term})
    require(cert['baseline_terms'] == terms, 'baseline recurrence')
    p = sum(t['term'] for t in terms)
    require(cert['P'] == p, 'baseline sum')
    require((stars('P'), stars('K')) == (32, 15), 'star domains')
    aut = (internal_group('P'), internal_group('K'))
    require(aut == (2, 24), 'internal block automorphism orders')
    group = aut[0]**4 * factorial(4) * aut[1]**3 * factorial(3)
    raw = 546356 * lower['PP']**6 * lower['PK']**12 * 37823**3 * 32**44 * 15**33
    require(cert['macro_raw_lower'] == raw, 'macro product')
    require(cert['group_order'] == group == 31850496, 'permitted group order')
    require(cert['normalized_lower'] == (raw+group-1)//group, 'orbit lower bound')
    require(12*group*p < raw < 13*group*p, 'strict integer comparison')
    require(cert['raw_to_group_P_floor'] == 12, 'ratio interval')
    require(cert['status'] == 'DIRECT_INTEGRATION_REDUCTION_GATE_FAILED', 'status')
    return {'status': 'CHECKED_DIRECT_INTEGRATION_REDUCTION_GATE_FAILED',
            'event_histogram_color_colon_fixed_bits': hist,
            'physical_K4_pair_matrices_checked': 131072,
            'internal_block_permutations_checked': 144,
            'star_words_checked': 48, 'baseline_terms': 18,
            'coordinate_edges': coordinate_audit(),
            'strict_comparison': '12*Gamma*P < R < 13*Gamma*P',
            'new_target_solver_calls': 0, 'physical_target_task_decisions': 0}, expensive


def audit_catalog(path):
    data = Path(path).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    require(digest == '39e10a1bb2d6b36d556e646e12f0181b2bc3bd45b334ad7f495b8900d7680433', 'catalog digest')
    words = data.splitlines()
    require(len(words) == len(set(words)) == 546356, 'catalog literal uniqueness')
    require(len(data) == 6556272 and all(len(w) == 11 and w[0] == 74 for w in words), 'catalog format')
    return {'sha256': digest, 'bytes': len(data), 'distinct_literal_cores': len(words),
            'scope': 'Integrity and literal uniqueness; Ramsey membership and catalog completeness imported'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--catalog11', type=Path)
    args = parser.parse_args()
    output, _ = validate(json.loads(args.certificate.read_text()))
    if args.catalog11:
        output['catalog11'] = audit_catalog(args.catalog11)
    print(json.dumps(output, indent=2, sort_keys=True))

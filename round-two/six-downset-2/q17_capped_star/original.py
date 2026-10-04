"""Separate literal-set reader for the q17/k8 original rational matrix.

This module imports no exploratory/parent/peer mathematical executable.
It rebuilds proper entries from sets, then checks the independent residual
lift, actual empty vertex, both endpoint identities and physical metric.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def mask(member):
    return sum(1 << i for i in member)


def member_type(member):
    return (sum(1 << i for i in member if i < 3),
            sum(3 <= i <= 10 for i in member), sum(i >= 11 for i in member))


def set_members():
    members = []
    for size in range(4):
        for subset in combinations(range(20), size):
            if size <= 2 or (sum(i < 3 for i in subset) >= 2 and
                             not (1 in subset and 2 in subset and
                                  any(3 <= i <= 10 for i in subset))):
                members.append(subset)
    return sorted(members, key=mask)


def literal_masks():
    return [v for v in range(1 << 20) if v.bit_count() <= 2 or
            (v.bit_count() == 3 and (v & 7).bit_count() >= 2 and
             not ((v & 6) == 6 and v & (((1 << 11) - 1) ^ 7)))]


def build(data):
    require(tuple(data[key] for key in ('q', 'k', 'ground_points', 'N', 's', 'h', 'denominator')) ==
            (17, 8, 20, 255, 55, 200, 32768), 'exact new original carrier and rational units')
    items = data['free_pair_values']
    require(data['free_pair_type_count'] == len(items) == 143, 'complete new free-pair data')
    table = {}
    for item in items:
        key = tuple(tuple(t) for t in item['types'])
        require(len(key) == 2 and all(len(t) == 3 and all(type(x) is int for x in t) for t in key),
                'literal type domain')
        require(key == tuple(sorted(key)) and key not in table and type(item['numerator']) is int,
                'unique unordered rational pair data')
        table[key] = item['numerator']
    members = set_members()
    proper, Q = members[1:], members[2:]
    sets = list(map(frozenset, members))
    proper_sets, residual_sets = sets[1:], sets[2:]
    keys = {tuple(sorted((member_type(v), member_type(w))))
            for i, v in enumerate(Q) for j, w in enumerate(Q[i + 1:], i + 1)
            if residual_sets[i].isdisjoint(residual_sets[j])}
    require(set(table) == keys, 'every actual disjoint original pair and no unused pair type')
    den, s, N, h = 32768, 55, 255, 200
    C = []
    for i, v in enumerate(proper):
        row = []
        for j, w in enumerate(proper):
            if i == j:
                value = 54 * den
            elif not proper_sets[i].isdisjoint(proper_sets[j]):
                value = -den
            elif i == 0 or j == 0:
                value = 0
            else:
                value = table[tuple(sorted((member_type(v), member_type(w))))]
            row.append(value)
        C.append(row)
    star = [i for i, v in enumerate(proper) if 0 in v]
    for i, v in enumerate(proper):
        if 0 not in v:
            C[i][0] = C[0][i] = -sum(C[i][j] for j in star if j != 0)
    T = [row[1:] for row in C[1:]]
    row_sums = list(map(sum, C))
    L = [[den + sum(row_sums)] + [den - x for x in row_sums]] + [
        [den - row_sums[i]] + [den + x for x in row] for i, row in enumerate(C)]
    r = [int(0 in v) for v in Q]
    b = [1 - x for x in r]
    cols = [{i + 2: 1, 1 if r[i] else 0: -1} for i in range(253)]
    G = [[sum(x * cols[j].get(k, 0) for k, x in cols[i].items())
          for j in range(253)] for i in range(253)]
    clear = s * h
    GI = [[clear * int(i == j) - h * r[i] * r[j] - s * b[i] * b[j]
           for j in range(253)] for i in range(253)]
    cap = [[N * den * GI[i][j] - clear * T[i][j] for j in range(253)] for i in range(253)]
    return {'members': members, 'C_num': C, 'T_num': T, 'L_num': L,
            'G': G, 'GI_num': GI, 'cap_num': cap, 'r': r, 'b': b,
            'denominator': den, 'cap_clear': clear, 'N': N, 's': s, 'h': h}


def lift(matrix, r):
    out = [[0] * 255 for _ in range(255)]
    cols = [{i + 2: 1, 1 if r[i] else 0: -1} for i in range(253)]
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            for a, x in cols[i].items():
                for b, y in cols[j].items():
                    out[a][b] += value * x * y
    return out


def audit(point):
    members = point['members']
    require([mask(v) for v in members] == literal_masks(), 'ENTIRE original literal membership')
    require(len(members) == 255 and members[:2] == [(), (0,)] and (1,) in members[2:] and
            (2,) in members[2:], 'actual empty, maximum pivot and smaller singletons')
    collection = set(members)
    require(all(tuple(x for x in v if x != i) in collection for v in members for i in v),
            'every downward deletion')
    sizes = [sum(i in v for v in members) for i in range(20)]
    require(sizes == [55, 47, 47] + [22] * 8 + [23] * 9, 'all original star sizes')
    C, T, L, G, GI, cap = (point[key] for key in ('C_num', 'T_num', 'L_num', 'G', 'GI_num', 'cap_num'))
    den, clear = point['denominator'], point['cap_clear']
    require((den, clear, point['N'], point['s'], point['h']) == (32768, 11000, 255, 55, 200),
            'complete original units and carrier parameters')
    require(len(C) == 254 and all(len(row) == 254 for row in C) and
            len(T) == 253 and all(len(row) == 253 for row in T) and
            len(L) == 255 and all(len(row) == 255 for row in L), 'complete physical dimensions')
    r = [int(0 in v) for v in members[2:]]
    b = [1 - x for x in r]
    require(point['r'] == r and point['b'] == b and sum(r) == 54 and sum(b) == 199,
            'every original incidence and complementary-group coordinate')
    require(len({member_type(v) for v in members[2:]}) == 22, 'actual residual member type census')
    proper = members[1:]
    star = [i for i, v in enumerate(proper) if 0 in v]
    require(all(C[i][j] == C[j][i] and
                (C[i][j] == 54 * den if i == j else C[i][j] == -den)
                for i, v in enumerate(proper) for j, w in enumerate(proper)
                if i == j or set(v).intersection(w)), 'whole fixed proper diagonal and support')
    require(all(sum(row[j] for j in star) == 0 for row in C), 'every proper maximum-star equation')
    require(T == [row[1:] for row in C[1:]], 'ENTIRE actual residual principal matrix')
    require(all(sum(row) == 255 * den for row in L), 'every original regular row including empty')
    require(all(L[i][j] == L[j][i] and
                (not set(v).intersection(w) or L[i][j] == 55 * den * int(i == j))
                for i, v in enumerate(members) for j, w in enumerate(members)),
            'EVERY original M symmetry and intersection support position')
    lower_lift = lift(T, r)
    require(all(L[i][j] == den + lower_lift[i][j] for i in range(255) for j in range(255)),
            'EVERY original lower lift including empty and anchor')
    require(all(G[i][j] == int(i == j) + r[i] * r[j] + b[i] * b[j]
                for i in range(253) for j in range(253)), 'EVERY physical Gram position')
    rs = [sum(GI[k][j] for k in range(253) if r[k]) for j in range(253)]
    bs = [sum(GI[k][j] for k in range(253) if b[k]) for j in range(253)]
    require(all(GI[i][j] + r[i] * rs[j] + b[i] * bs[j] == clear * int(i == j) and
                GI[i][j] + r[j] * rs[i] + b[j] * bs[i] == clear * int(i == j)
                for i in range(253) for j in range(253)), 'BOTH entire inverse-metric products')
    require(all(cap[i][j] == 255 * den * GI[i][j] - clear * T[i][j]
                for i in range(253) for j in range(253)), 'EVERY correctly scaled residual cap')
    centered = [255 * int(0 in v) - 55 for v in members]
    require(sum(centered) == 0 and sum(x * x for x in centered) == 255 * 55 * 200,
            'whole centered star and original projector normalization')
    require(all(sum(row[j] * centered[j] for j in range(255)) == 0 for row in L),
            'EVERY original centered-star kernel equation')
    cap_lift = lift(cap, r)
    require(all(clear * (255 * den * int(i == j) - L[i][j]) ==
                cap_lift[i][j] + den * centered[i] * centered[j]
                for i in range(255) for j in range(255)), 'EVERY original cap lift and star projector')
    return {'agent': 'six-downset-2', 'role': 'researcher', 'q': 17, 'k': 8,
            'N': 255, 's': 55, 'h': 200, 'point_stars': sizes,
            'original_L_num_sha256': digest(L), 'original_T_num_sha256': digest(T),
            'original_cap_num_sha256': digest(cap), 'physical_Gram_sha256': digest(G),
            'original_positions_per_endpoint': 65025, 'residual_dimension': 253,
            'physical_metric_positions': 64009, 'every_original_kernel_equation': 255,
            'no_parent_factors_or_margins_used': True}


def shifted_form(point, endpoint):
    require(endpoint in ('lower', 'upper'), 'endpoint domain')
    factor = point['denominator'] * (1 if endpoint == 'lower' else point['cap_clear'])
    source = point['T_num'] if endpoint == 'lower' else point['cap_num']
    require(factor % 1024 == 0, 'exact rational margin clearing')
    return [[x - (factor // 1024) * int(i == j) for j, x in enumerate(row)]
            for i, row in enumerate(source)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--coefficients', default=str(Path(__file__).with_name('COEFFICIENTS.json')))
    parser.add_argument('--record', required=True)
    args = parser.parse_args()
    point = build(json.loads(Path(args.coefficients).read_bytes()))
    record = audit(point)
    Path(args.record).write_bytes(canonical(record) + b'\n')
    print(json.dumps(record))

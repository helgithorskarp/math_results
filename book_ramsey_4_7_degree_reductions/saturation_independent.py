"""Separate author checker using literal bitsets and integer walk counts.

Imports no main generator, matrix code, or local research modules. The
expected file supplies compact controls; classification is an external theorem.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def ensure(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def decode(rows: list[int], n: int) -> list[int]:
    ensure(isinstance(rows, list) and len(rows) == n, 'row count')
    for i, row in enumerate(rows):
        ensure(type(row) is int and 0 <= row < 1 << n, 'row integer/range')
        ensure(row >> i & 1 == 0, 'zero diagonal')
        for j, other in enumerate(rows):
            ensure((row >> j & 1) == (other >> i & 1), 'symmetric adjacency')
    return rows


def check_controls(records: list[list[int]]) -> dict[str, int]:
    count = {name: 0 for name in ('graphs', 'spines', 'block_entries', 'square_entries',
                                 'incident_rows', 'nonzero_block_defects', 'negative_spine_defects')}
    ensure(len(records) == 32 and len({tuple(r) for r in records}) == 32, 'control domain')
    all_vertices, u_mask, w_mask = (1 << 22)-1, (1 << 11)-1, ((1 << 11)-1) << 11
    for raw in records:
        red = decode(raw, 22)
        blue = [all_vertices ^ row ^ (1 << i) for i, row in enumerate(red)]
        ensure([row.bit_count() for row in red] == [8]*11+[10]*11, 'control degrees')
        ensure(all((row & u_mask).bit_count() == 4 for row in red), 'partition degrees')
        defect = {}
        for i in range(22):
            for j in range(i+1, 22):
                if red[i] >> j & 1:
                    value = 3-(red[i] & red[j]).bit_count()
                else:
                    value = 6-(blue[i] & blue[j]).bit_count()
                defect[i, j] = defect[j, i] = value
                count['spines'] += 1
                count['negative_spine_defects'] += int(value < 0)
        ensure(sum(defect.values()) == 0, 'signed total')
        for i in range(22):
            ensure(sum(defect.get((i, j), 0) for j in range(22)) ==
                   4*(red[i] & u_mask).bit_count()-16, 'literal incident row')
            count['incident_rows'] += 1
        a = [row & u_mask for row in red[:11]]
        q = [(row & w_mask) >> 11 for row in blue[11:]]
        m = [(row & w_mask) >> 11 for row in red[:11]]
        mt = [row & u_mask for row in red[11:]]
        for i in range(11):
            for j in range(11):
                # These are literal two-step walks and shared cross neighbors,
                # not products through the main implementation's routine.
                u_value = ((a[i] & a[j]).bit_count()-(a[i] >> j & 1)+
                           (m[i] & m[j]).bit_count())
                w_value = ((q[i] & q[j]).bit_count()-(q[i] >> j & 1)+
                           (mt[i] & mt[j]).bit_count())
                am = (a[i] & mt[j]).bit_count()
                mq = (m[i] & q[j]).bit_count()
                ensure(u_value == 6*(i == j)+2-defect.get((i, j), 0), 'U walk identity')
                ensure(w_value == 6*(i == j)+2-defect.get((i+11, j+11), 0), 'W walk identity')
                ensure(am-mq == -defect[i, j+11], 'cross walk identity')
                count['block_entries'] += 3
                count['nonzero_block_defects'] += sum(v != 0 for v in
                    (defect.get((i, j), 0), defect.get((i+11, j+11), 0), defect[i, j+11]))
        for i in range(22):
            diagonal_i = -1 if i < 11 else 3
            yi = 2 if i < 11 else 0
            for j in range(22):
                diagonal_j = -1 if j < 11 else 3
                yj = 2 if j < 11 else 0
                if i == j:
                    square = diagonal_i**2+4*red[i].bit_count()
                else:
                    square = (4*(red[i] & red[j]).bit_count()+
                              2*(diagonal_i+diagonal_j)*(red[i] >> j & 1))
                ensure(square == 25*(i == j)+24-4*(yi+yj)-4*defect.get((i, j), 0),
                       'literal square entries')
                count['square_entries'] += 1
        count['graphs'] += 1
    return count


def scalar_audit() -> dict:
    records, full, low = [], [], []
    handshake = 0
    for n8 in range(23):
        for n10 in range(23-n8):
            for n11 in range(23-n8-n10):
                n9 = 22-n8-n10-n11
                degree_sum = 8*n8+9*n9+10*n10+11*n11
                if degree_sum & 1:
                    continue
                handshake += 1
                incident = 132-3*(4*n8+n9+n11)
                odd = n9+n11
                if incident == odd:
                    records.append(dict(n8=n8, n9=n9, n10=n10, n11=n11, edges=degree_sum//2))
                if (incident == 0 and odd == 0 and n11 <= 6 and
                        97 <= degree_sum//2 <= 112 and (n11 == 0 or degree_sum//2 >= 106)):
                    full.append([n8, n9, n10, n11, degree_sum//2])
    records.sort(key=lambda r: (r['n8'], r['n11']))
    survivors = [r for r in records if r['n11'] <= 6 and
                 (r['n11'] == 0 or r['edges'] >= 106)]
    for e in range(97, 106):
        hists = []
        for c in range(23):
            for b in range(23-c):
                a = 22-c-b
                if 8*a+9*b+10*c == 2*e and 132-3*(4*a+b)-b >= 4:
                    hists.append([a, b, c])
        hists.sort()
        low.append(dict(edges=e, histograms=hists))
    # Divisibility is forced by equal edge counts in the two parts of H.
    pairs = []
    for r in range(1, 6):
        s = 6-r
        pairs.append([r, s, 11-r*(11//r), 11-s*(11//s)])
        ensure(not (11 % r == 0 and 11 % s == 0), 'bipartite eleven-edge root impossibility')
    layers = [2*(4+2), 3*(4+2)//2, 4*(4+2)//3]
    ensure(11 not in layers and 22 % 3 == 1, 'classification specialization')
    ensure(len(records) == 21 and full == [[11, 0, 11, 0, 99]], 'scalar boundary coverage')
    return dict(handshake_histograms=handshake, equality_histograms=records,
                high_cut_survivors=survivors, saturated_scalar_survivor=full,
                bipartite_root_pairs=pairs, nonbipartite_root_degree=3,
                nonbipartite_root_degree_sum=22, exceptional_layer_orders=layers,
                low_edge_histograms=low)


def arbitrary_partition_audit(records: list[list[int]]) -> dict[str, int]:
    ensure(len(records) == 32, 'arbitrary control count')
    counts = dict(graphs=0, spines=0, square_entries=0, incident_rows=0,
                  rows_with_nonfour_D8_neighbors=0)
    mask = (1 << 22)-1
    for raw in records:
        red = decode(raw, 22)
        ensure([row.bit_count() for row in red] == [8]*11+[10]*11, 'arbitrary degrees')
        blue = [mask ^ row ^ (1 << i) for i, row in enumerate(red)]
        f = {}
        for i in range(22):
            for j in range(i+1, 22):
                if red[i] >> j & 1:
                    v = 3-(red[i] & red[j]).bit_count()
                else:
                    v = 6-(blue[i] & blue[j]).bit_count()
                f[i, j] = f[j, i] = v
                counts['spines'] += 1
        ensure(sum(f.values()) == 0, 'arbitrary total')
        for i in range(22):
            s = (red[i] & ((1 << 11)-1)).bit_count()
            ensure(sum(f.get((i, j), 0) for j in range(22)) == 4*(s-4), 'arbitrary row')
            # Also audit the row-count derivation through neighbor degrees.
            d = red[i].bit_count()
            neighbor_sum = sum(red[j].bit_count() for j in range(22) if red[i] >> j & 1)
            ensure(198-294+38*d-d*d-2*neighbor_sum == 4*(s-4), 'row derivation')
            counts['incident_rows'] += 1
            counts['rows_with_nonfour_D8_neighbors'] += int(s != 4)
            for j in range(22):
                di = -1 if i < 11 else 3
                dj = -1 if j < 11 else 3
                yi, yj = 2*(i < 11), 2*(j < 11)
                lhs = (di*di+4*d if i == j else
                       4*(red[i] & red[j]).bit_count()+2*(di+dj)*(red[i] >> j & 1))
                ensure(lhs == 25*(i == j)+24-4*(yi+yj)-4*f.get((i, j), 0), 'arbitrary square')
                counts['square_entries'] += 1
        counts['graphs'] += 1
    ensure(counts['rows_with_nonfour_D8_neighbors'] > 0, 'nontrivial partition bridge')
    return counts


def check_disconnected(data: dict) -> None:
    rows = decode(data['rows'], 11)
    x = data['zero_sum_vector']
    ensure(len(x) == 11 and all(type(v) is int for v in x) and sum(x) == 0, 'component vector')
    ensure(all(row.bit_count() == 4 for row in rows), 'component degrees')
    ax = [sum(x[j] for j in range(11) if row >> j & 1) for row in rows]
    aax = [sum(ax[j] for j in range(11) if row >> j & 1) for row in rows]
    quadratic = sum(x[i]*(6*x[i]+2*sum(x)+ax[i]-aax[i]) for i in range(11))
    ensure(ax == [4*v for v in x], 'eigenvalue four')
    ensure(sum(v*v for v in x) == data['squared_norm'] == 330, 'norm')
    ensure(quadratic == data['gram_quadratic'] == -1980, 'negative Gram certificate')


def verify(data: dict) -> dict:
    ensure(data['agent'] == 'six-books-1' and data['role'] == 'researcher', 'attribution')
    counts = check_controls(data['control_rows'])
    ensure(counts == data['counts'], 'control counts mismatch')
    arbitrary_counts = arbitrary_partition_audit(data['arbitrary_partition_rows'])
    ensure(arbitrary_counts == data['arbitrary_partition_counts'], 'arbitrary control mismatch')
    scalar = scalar_audit()
    ensure(scalar == data['arithmetic'], 'all scalar records differ')
    check_disconnected(data['disconnected_control'])
    return dict(counts=counts, arbitrary_partition_counts=arbitrary_counts,
                equality_candidates=len(scalar['equality_histograms']),
                high_cut_survivors=scalar['high_cut_survivors'], disconnected_gram=-1980, status='passed')


def negative_controls(data: dict) -> None:
    import copy
    changes = [
        lambda d: d['control_rows'][0].__setitem__(0, d['control_rows'][0][0] | 1),
        lambda d: d['control_rows'][0].__setitem__(0, d['control_rows'][0][0] ^ 2),
        lambda d: d['counts'].__setitem__('block_entries', d['counts']['block_entries']+1),
        lambda d: d['arithmetic']['high_cut_survivors'][0].__setitem__('edges', 98),
        lambda d: d['arithmetic']['exceptional_layer_orders'].__setitem__(0, 11),
        lambda d: d['disconnected_control'].__setitem__('gram_quadratic', 0),
    ]
    for mutation in changes:
        bad = copy.deepcopy(data)
        mutation(bad)
        rejected = False
        try:
            verify(bad)
        except ValueError:
            rejected = True
        ensure(rejected, 'corrupt certificate accepted')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative-controls', action='store_true')
    args = parser.parse_args()
    data = json.loads(Path(__file__).with_name('saturation_expected.json').read_text())
    result = verify(data)
    if args.negative_controls:
        negative_controls(data)
        result['rejected_corruptions'] = 6
    print(json.dumps(result, sort_keys=True))

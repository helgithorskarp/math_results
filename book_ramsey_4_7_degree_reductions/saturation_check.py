"""Exact author controls for the saturation obstruction; Python 3.11+ stdlib.

This is not a census of graphs or a replay of the external spectral theorem.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import random


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def regular_graph(seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    a = [[int((i-j) % 11 in (1, 2, 9, 10)) for j in range(11)]
         for i in range(11)]
    for _ in range(128):
        edges = [(i, j) for i in range(11) for j in range(i+1, 11) if a[i][j]]
        (i, j), (k, l) = rng.sample(edges, 2)
        if rng.randrange(2):
            k, l = l, k
        if len({i, j, k, l}) != 4 or a[i][k] or a[j][l]:
            continue
        for x, y in ((i, j), (k, l)):
            a[x][y] = a[y][x] = 0
        for x, y in ((i, k), (j, l)):
            a[x][y] = a[y][x] = 1
    return a


def cross_matrix(seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    m = [[int((i-j) % 11 in (0, 1, 3, 5)) for j in range(11)]
         for i in range(11)]
    for _ in range(128):
        i, j = rng.sample(range(11), 2)
        k, l = rng.sample(range(11), 2)
        if m[i][k] == m[j][l] and m[i][l] == m[j][k] and m[i][k] != m[i][l]:
            for x, y in ((i, k), (j, l), (i, l), (j, k)):
                m[x][y] = 1-m[x][y]
    return m


def multiply(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def controls() -> tuple[list[list[int]], dict[str, int]]:
    records = []
    counts = dict(graphs=0, spines=0, block_entries=0, square_entries=0,
                  incident_rows=0, nonzero_block_defects=0, negative_spine_defects=0)
    for seed in range(32):
        a, q, m = regular_graph(990000+seed), regular_graph(991000+seed), cross_matrix(992000+seed)
        for matrix in (a, q, m):
            require(all(sum(row) == 4 for row in matrix), 'row regularity')
            require(all(sum(col) == 4 for col in zip(*matrix)), 'column regularity')
        r = [[0]*22 for _ in range(22)]
        for i in range(11):
            for j in range(11):
                r[i][j] = a[i][j]
                r[i+11][j+11] = int(i != j)-q[i][j]
                r[i][j+11] = r[j+11][i] = m[i][j]
        nr = [{j for j in range(22) if r[i][j]} for i in range(22)]
        nb = [set(range(22))-nr[i]-{i} for i in range(22)]
        require(list(map(len, nr)) == [8]*11+[10]*11, 'full degrees')
        f = [[0]*22 for _ in range(22)]
        for i in range(22):
            for j in range(i+1, 22):
                f[i][j] = f[j][i] = (3-len(nr[i] & nr[j]) if r[i][j]
                                       else 6-len(nb[i] & nb[j]))
                counts['spines'] += 1
                counts['negative_spine_defects'] += int(f[i][j] < 0)
        require(sum(map(sum, f)) == 0, 'signed total defect')
        for i in range(22):
            require(sum(f[i]) == 4*len(nr[i] & set(range(11)))-16,
                    'degree-eight-neighbor row identity')
            counts['incident_rows'] += 1
        a2, q2 = multiply(a, a), multiply(q, q)
        mt = list(map(list, zip(*m)))
        mm, mtm, am, mq = multiply(m, mt), multiply(mt, m), multiply(a, m), multiply(m, q)
        for i in range(11):
            for j in range(11):
                require(a2[i][j]-a[i][j]+mm[i][j] == 6*(i == j)+2-f[i][j],
                        'U Gram identity')
                require(q2[i][j]-q[i][j]+mtm[i][j] == 6*(i == j)+2-f[i+11][j+11],
                        'W Gram identity')
                require(am[i][j]-mq[i][j] == -f[i][j+11], 'intertwining identity')
                counts['block_entries'] += 3
                counts['nonzero_block_defects'] += sum(v != 0 for v in
                    (f[i][j], f[i+11][j+11], f[i][j+11]))
        y = [2]*11+[0]*11
        k = [[2*r[i][j]+(3-2*y[i])*(i == j) for j in range(22)] for i in range(22)]
        k2 = multiply(k, k)
        for i in range(22):
            for j in range(22):
                h = 25*(i == j)+24-4*(y[i]+y[j])-4*f[i][j]
                require(k2[i][j] == h, 'global integer square')
                counts['square_entries'] += 1
        records.append([sum(r[i][j] << j for j in range(22)) for i in range(22)])
        counts['graphs'] += 1
    require(len({tuple(rows) for rows in records}) == 32, 'distinct controls')
    return records, counts


def arithmetic() -> dict:
    equality = []
    histogram_count = 0
    fully_saturated = []
    for a in range(23):
        for b in range(23-a):
            for h in range(23-a-b):
                c = 22-a-b-h
                twice_edges = 8*a+9*b+10*c+11*h
                if twice_edges % 2:
                    continue
                histogram_count += 1
                if 3*a+b+h == 33:
                    equality.append(dict(n8=a, n9=b, n10=c, n11=h, edges=twice_edges//2))
                if (h <= 6 and 97 <= twice_edges//2 <= 112 and
                        (h == 0 or twice_edges//2 >= 106) and 3*a+b+h <= 33):
                    if 4*a+b+h == 44:
                        fully_saturated.append([a, b, c, h, twice_edges//2])
    equality.sort(key=lambda v: (v['n8'], v['n11']))
    require(len(equality) == 21, 'all parity-equality histograms before high-count cut')
    surviving_high_cut = [v for v in equality if v['n11'] <= 6 and
                         (v['n11'] == 0 or v['edges'] >= 106)]
    require(surviving_high_cut == [dict(n8=7, n9=12, n10=3, n11=0, edges=97),
                                 dict(n8=9, n9=6, n10=7, n11=0, edges=98),
                                 dict(n8=11, n9=0, n10=11, n11=0, edges=99)], 'equality after high cut')
    require(fully_saturated == [[11, 0, 11, 0, 99]], 'fully saturated scalar reduction')
    bipartite = [[r, 6-r, 11 % r, 11 % (6-r)] for r in range(1, 6)]
    require(all(x[2] or x[3] for x in bipartite), 'no bipartite root degree pair')
    require(22 % 3 != 0, 'no cubic eleven-edge root')
    require(11 not in (12, 9, 8), 'not an exceptional layer order')
    low_edges = []
    for e in range(97, 106):
        candidates = []
        for a in range(23):
            for b in range(23-a):
                c = 22-a-b
                if 8*a+9*b+10*c == 2*e and 3*a+b <= 32:
                    candidates.append([a, b, c])
        low_edges.append(dict(edges=e, histograms=candidates))
    return dict(handshake_histograms=histogram_count, equality_histograms=equality,
                high_cut_survivors=surviving_high_cut, saturated_scalar_survivor=fully_saturated,
                bipartite_root_pairs=bipartite, nonbipartite_root_degree=3,
                nonbipartite_root_degree_sum=22, exceptional_layer_orders=[12, 9, 8],
                low_edge_histograms=low_edges)


def arbitrary_partition_controls() -> tuple[list[list[int]], dict[str, int]]:
    records = []
    counts = dict(graphs=0, spines=0, square_entries=0, incident_rows=0,
                  rows_with_nonfour_D8_neighbors=0)
    for seed in range(32):
        rng = random.Random(993000+seed)
        internal_degree = 2*(seed % 5)
        cross_degree = 8-internal_degree
        a_offsets = set(range(1, internal_degree//2+1))
        a_offsets |= {11-v for v in a_offsets}
        q_offsets = set(range(1, cross_degree//2+1))
        q_offsets |= {11-v for v in q_offsets}
        r = [[0]*22 for _ in range(22)]
        for i in range(11):
            for j in range(11):
                r[i][j] = int((i-j) % 11 in a_offsets)
                r[i+11][j+11] = int(i != j and (i-j) % 11 not in q_offsets)
                r[i][j+11] = r[j+11][i] = int((i-j) % 11 < cross_degree)
        # Full-host switches preserve each degree but destroy the equitable
        # partition. They test the bridge before four-neighbor regularity.
        for _ in range(128):
            edges = [(i, j) for i in range(22) for j in range(i+1, 22) if r[i][j]]
            (i, j), (k, l) = rng.sample(edges, 2)
            if rng.randrange(2):
                k, l = l, k
            if len({i, j, k, l}) != 4 or r[i][k] or r[j][l]:
                continue
            for x, z in ((i, j), (k, l)):
                r[x][z] = r[z][x] = 0
            for x, z in ((i, k), (j, l)):
                r[x][z] = r[z][x] = 1
        nr = [{j for j in range(22) if r[i][j]} for i in range(22)]
        nb = [set(range(22))-nr[i]-{i} for i in range(22)]
        require(list(map(len, nr)) == [8]*11+[10]*11, 'arbitrary partition degrees')
        f = [[0]*22 for _ in range(22)]
        for i in range(22):
            for j in range(i+1, 22):
                f[i][j] = f[j][i] = (3-len(nr[i] & nr[j]) if r[i][j]
                                       else 6-len(nb[i] & nb[j]))
                counts['spines'] += 1
        require(sum(map(sum, f)) == 0, 'arbitrary signed total')
        for i in range(22):
            s = len(nr[i] & set(range(11)))
            require(sum(f[i]) == 4*s-16, 'arbitrary partition row identity')
            counts['incident_rows'] += 1
            counts['rows_with_nonfour_D8_neighbors'] += int(s != 4)
        y = [2]*11+[0]*11
        k = [[2*r[i][j]+(3-2*y[i])*(i == j) for j in range(22)] for i in range(22)]
        k2 = multiply(k, k)
        for i in range(22):
            for j in range(22):
                require(k2[i][j] == 25*(i == j)+24-4*(y[i]+y[j])-4*f[i][j],
                        'arbitrary partition square identity')
                counts['square_entries'] += 1
        records.append([sum(r[i][j] << j for j in range(22)) for i in range(22)])
        counts['graphs'] += 1
    require(counts['rows_with_nonfour_D8_neighbors'] > 0, 'nonzero row bridge coverage')
    return records, counts


def disconnected_control() -> dict:
    # A=K5+CP(3), both components four-regular. The zero-sum component
    # vector produces the exact forbidden Gram quadratic form.
    a = [[0]*11 for _ in range(11)]
    for i in range(11):
        for j in range(11):
            if i < 5 and j < 5:
                a[i][j] = int(i != j)
            elif i >= 5 and j >= 5:
                a[i][j] = int(i != j and (i-5)//2 != (j-5)//2)
    x = [6]*5+[-5]*6
    a2 = multiply(a, a)
    g = [[6*(i == j)+2+a[i][j]-a2[i][j] for j in range(11)] for i in range(11)]
    value = sum(x[i]*g[i][j]*x[j] for i in range(11) for j in range(11))
    require(sum(x) == 0 and value == -1980, 'disconnected negative Gram control')
    return dict(rows=[sum(a[i][j] << j for j in range(11)) for i in range(11)],
                zero_sum_vector=x, squared_norm=330, gram_quadratic=value)


def run() -> dict:
    records, counts = controls()
    arbitrary, arbitrary_counts = arbitrary_partition_controls()
    return dict(agent='six-books-1', role='researcher',
                status='exact arithmetic controls for a written proof with named external spectral classification',
                control_rows=records, counts=counts,
                arbitrary_partition_rows=arbitrary, arbitrary_partition_counts=arbitrary_counts,
                arithmetic=arithmetic(),
                disconnected_control=disconnected_control())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    result = run()
    path = Path(__file__).with_name('saturation_expected.json')
    if args.write_expected:
        path.write_text(json.dumps(result, indent=2)+'\n')
    else:
        require(result == json.loads(path.read_text()), 'expected output mismatch')
    print(json.dumps(dict(counts=result['counts'], arbitrary_partition_counts=result['arbitrary_partition_counts'],
                         equality_candidates=len(result['arithmetic']['equality_histograms']),
                         high_cut_survivors=result['arithmetic']['high_cut_survivors'],
                         disconnected_gram=-1980, status='passed'), sort_keys=True))

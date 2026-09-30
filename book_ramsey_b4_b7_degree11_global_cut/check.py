"""Literal-page audits for the degree11 global cut.

Author: six-books-3, researcher. Python 3.11+, standard library only.
Controls validate identities, not existence of valid full22 colorings.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def graph(rows):
    n = len(rows)
    require(all(len(r) == n and set(r) <= {'0', '1'} for r in rows), 'bad matrix')
    adj = [{j for j, bit in enumerate(r) if bit == '1'} for r in rows]
    require(all(i not in adj[i] and all((j in adj[i]) == (i in adj[j])
                for j in range(n)) for i in range(n)), 'not a simple graph')
    return adj


def pages(adj, i, j):
    if j in adj[i]:
        return len(adj[i] & adj[j])
    full = set(range(len(adj)))
    return len((full-adj[i]-{i}) & (full-adj[j]-{j}))


def baseline():
    data = (HERE/'baseline21.rows').read_bytes()
    adj = graph(data.decode().splitlines())
    require(len(adj) == 21, 'baseline order')
    maxima = [0, 0]
    for i, j in combinations(range(21), 2):
        color = int(j not in adj[i])
        maxima[color] = max(maxima[color], pages(adj, i, j))
    result = {'red_edges': sum(map(len, adj))//2,
              'degrees': {str(d): c for d, c in sorted(Counter(map(len, adj)).items())},
              'spine_maxima': maxima, 'sha256': hashlib.sha256(data).hexdigest()}
    require(result['red_edges'] == 93 and result['degrees'] == {'8': 4, '9': 16, '10': 1}
            and maxima == [3, 6], 'known baseline did not reproduce')
    return result


def controlled_graph(local, variant, fixture_index):
    adj = [set(row) for row in local] + [set() for _ in range(11)]
    for i in range(11):
        adj[i].add(11)
        adj[11].add(i)
    for b in range(10):
        if variant < 48:
            z = (variant+5*b) % 12
        elif variant < 64:
            z = 3+(variant+b) % 4
        else:
            z = 4+(variant+b) % 2
        offset, step = (7*variant+2*b) % 11, 1+(variant+3*b) % 10
        missing = {(offset+step*j) % 11 for j in range(z)}
        for i in set(range(11))-missing:
            adj[i].add(12+b)
            adj[12+b].add(i)
    for i, j in combinations(range(10), 2):
        if ((variant+1)*(i+1)+(j+1)*(j+3)+7*fixture_index) % 5 < 2:
            adj[12+i].add(12+j)
            adj[12+j].add(12+i)
    return adj


def identity_controls():
    fixtures = json.loads((HERE/'fixtures.json').read_text())
    counts = Counter()
    fixture_receipts = []
    stream = hashlib.sha256()
    for fi, fixture in enumerate(fixtures):
        local = graph(fixture['rows'])
        h = list(map(len, local))
        require(h == [3]*10+[2], 'bad local histogram')
        T = sum(j in local[i] and k in local[i] and k in local[j]
                for i, j, k in combinations(range(11), 3))
        root_core = [set(a) for a in local]+[set(range(11))]
        for i in range(11):
            root_core[i].add(11)
        require(all(pages(root_core, i, j) <= (3 if j in root_core[i] else 6)
                    for i, j in combinations(range(12), 2)), 'invalid local core')
        counts['local_spines'] += 66
        fixture_receipts.append({'name': fixture['name'], 'triangles': T})
        for variant in range(80):
            adj = controlled_graph(local, variant, fi)
            stream.update((''.join(''.join('1' if j in adj[i] else '0' for j in range(22))
                                   for i in range(22))+'\n').encode())
            Z = [set(range(11))-adj[b] for b in range(12, 22)]
            z = list(map(len, Z))
            t = [sum(i in row for row in Z) for i in range(11)]
            eps = {(i, j): (3 if j in adj[i] else 6)-pages(adj, i, j)
                   for i, j in combinations(range(11), 2)}
            U = sum(eps.values())
            UR = sum(eps[(i, j)] for i, j in eps if j in local[i])
            F = sum((a-3)*(a-4)//2 for a in z)
            K = sum((a-4)*(a-5)//2 for a in z)
            Q = sum(sum(j in local[i] for i, j in combinations(row, 2)) for row in Z)
            require(U+F+t[10] == 10, 'first budget')
            require(3*(U+K+T)+UR+Q == 22-4*t[10], 'second budget')
            require(sum(z) == 40+F-K == sum(t), 'total misses')
            for i in range(11):
                require(len(adj[i]) == 11+h[i]-t[i], 'full degree identity')
                e_i = sum(value for edge, value in eps.items() if i in edge)
                u_i = sum(len(row)-4 for row in Z if i in row)
                Pt = sum(t[j] for j in local[i])
                Ph = sum(h[j] for j in local[i])
                require((3-h[i])*t[i]-Pt == 5*h[i]-h[i]**2+2-2*Ph-e_i-u_i,
                        'row identity; check the +2 constant')
                counts['row_identities'] += 1
            for (i, j), unused in eps.items():
                S = sum(i in row and j in row for row in Z)
                common = len(local[i] & local[j])
                if j in local[i]:
                    rhs = t[i]+t[j]-8-common-unused
                else:
                    rhs = h[i]+h[j]-3-common-unused
                require(S == rhs, 'mixed pair identity')
                counts['pair_identities'] += 1
            counts['graphs'] += 1
    return {'counts': dict(sorted(counts.items())), 'fixtures': fixture_receipts,
            'control_stream_sha256': stream.hexdigest()}


def joint_root_cut():
    # The blue endpoint pair: V has two red neighbors at each endpoint;
    # X has at most two. Use literal subsets to recover both minima.
    fixed = set(range(8))
    vs = [set(x) for x in combinations(range(8), 2)]
    minimum_V = min(len(fixed-a-b) for a in vs for b in vs)
    blue = []
    for k in (10, 11):
        universe = set(range(k-3))
        xs = [set(s) for z in range(3) for s in combinations(universe, z)]
        minimum_X = min(len(universe-a-b) for a in xs for b in xs)
        require(minimum_V+minimum_X > 6, 'blue endpoint cut')
        blue.append({'degree_x': k, 'minimum_V': minimum_V, 'minimum_X': minimum_X,
                     'V_subset_pairs': len(vs)**2, 'X_subset_pairs': len(xs)**2})
    # The red endpoint pair. Enumerate its actual allowed neighbor sets
    # in disjoint V,X,D and test both red-page and degree-seven cuts.
    red = []
    for k in (10, 11):
        V, X, D = set(range(8)), set(range(8, 8+k-3)), set(range(30, 30+13-k))
        vs = [{j} for j in V]
        xs = [set()]+[{j} for j in X]
        ds = [set(s) for z in range(len(D)+1) for s in combinations(D, z)]
        counts = Counter({'examined': 0, 'degrees_at_least7': 0,
                          'red_cap_survivors': 0, 'capacity_cut_survivors': 0})
        states = [(a|b|c, 3+len(a)+len(b)+len(c)) for a in vs for b in xs for c in ds]
        for (Na, da) in states:
            for (Nb, db) in states:
                counts['examined'] += 1
                if min(da, db) < 7:
                    continue
                counts['degrees_at_least7'] += 1
                common = 2+len(Na & Nb)  # v,x are already red pages.
                if common > 3:
                    continue
                counts['red_cap_survivors'] += 1
                if (da == 7 and db-1-common < 6) or (db == 7 and da-1-common < 6):
                    continue
                counts['capacity_cut_survivors'] += 1
        require(counts['capacity_cut_survivors'] == 0, 'joint-root red cut has survivors')
        red.append({'degree_x': k, **dict(counts)})
    return {'blue': blue, 'red': red}


def finite_boundaries():
    budgets = []
    for tx in range(2, 7):
        survivors = []
        for U in range(9):
            for K in range(9):
                for T in range(9):
                    for UR in range(U+1):
                        Q = 22-4*tx-3*(U+K+T)-UR
                        if Q >= 0 and U <= 10-tx:
                            survivors.append([U, K, T, UR, Q])
        if tx == 6:
            require(not survivors, 'degree7 budget')
        if tx == 5:
            require(survivors == [[0, 0, 0, 0, 2]], 'degree8 equality budget')
        if tx == 4:
            require(all(sum(x[:3]) <= 2 for x in survivors), 'degree9 budget')
        budgets.append({'t_x': tx, 'states': survivors})
    require(all((z-4)*(z-5)//2 >= 0 and z-4 <= 1+(z-4)*(z-5)//2
                for z in range(12)), 'integer curvature bounds')
    load_states = []
    for n3 in range(1, 11):
        for n5 in range(11-n3):
            for n6 in range(11-n3-n5):
                for n7 in range(11-n3-n5-n6):
                    n4 = 10-n3-n5-n6-n7
                    if 3*n3+4*n4+5*n5+6*n6+7*n7 == 40 and n5 >= n3:
                        load_states.append([n3, n4, n5, n6, n7])
    require(load_states == [[j, 10-2*j, j, 0, 0] for j in range(1, 6)],
            'balanced cubic-load consequence')
    small = []
    for n in (1, 3, 5):
        pairs = list(combinations(range(n), 2))
        degree_candidates, survivors = 0, 0
        for mask in range(1 << len(pairs)):
            adj = [set() for _ in range(n)]
            for p, (i, j) in enumerate(pairs):
                if mask >> p & 1:
                    adj[i].add(j)
                    adj[j].add(i)
            if list(map(len, adj)) != [2]+[3]*(n-1):
                continue
            degree_candidates += 1
            if not any(adj[i] & adj[j] for i, j in pairs if j in adj[i]):
                survivors += 1
        require(survivors == 0, 'small triangle-free component survived')
        small.append({'order': n, 'all_graphs': 1 << len(pairs),
                      'degree_candidates': degree_candidates, 'triangle_free': survivors})
    accepted, maximum, boundary = 0, -1, []
    for n7 in range(23):
        for n8 in range(23-n7):
            for n9 in range(23-n7-n8):
                for n11 in range(23-n7-n8-n9):
                    n10 = 22-n7-n8-n9-n11
                    total = 7*n7+8*n8+9*n9+10*n10+11*n11
                    if n7 or total % 2 or (n11 and not n9) or 49*n11 > 3*(total//2):
                        continue
                    accepted += 1
                    e = total//2
                    maximum = max(maximum, e)
                    if e == 112:
                        boundary.append([n7, n8, n9, n10, n11])
    require(maximum == 112 and boundary == [[0, 0, 1, 16, 5], [0, 0, 2, 14, 6]],
            'global edge boundary')
    local_degree_histograms = []
    for n8 in range(3):
        for n9 in range(3):
            delta = 2*n8+n9
            if delta <= 2:
                local_degree_histograms.append({'n8': n8, 'n9': n9, 'n10':10-n8-n9,
                                                'Delta': delta,
                                                'minimum_full_edges':108-delta})
    boundary106 = []
    for state in local_degree_histograms:
        if state['Delta'] == 2:
            boundary106.append([0, state['n8'], state['n9']+7, state['n10']+4, 1])
    boundary106.sort()
    require(boundary106 == [[0,0,9,12,1],[0,1,7,13,1]], 'degree11 branch at106')
    uniform_degree_loads = []
    for a in range(15):
        for b in range(15-a):
            for c in range(15-a-b):
                d = 14-a-b-c
                if 7*a+8*b+9*c+10*d >= 140:
                    uniform_degree_loads.append([a,b,c,d])
    require(uniform_degree_loads == [[0,0,0,14]], 'degree7 root without degree11')
    outside_states=[]
    for z in range(12):
        if (z-4)*(z-5)//2 > 2:
            continue
        for hB in range(3,z+1):
            outside_states.append([z,hB,11-z+hB])
    require(sorted({s[0] for s in outside_states}) == [3,4,5,6]
            and min(s[2] for s in outside_states)==8, 'minimum degree outside degree11 root')
    return {'budgets': budgets, 'balanced_load_histograms': load_states,
            'small_components': small, 'global_degree_histograms_surviving_cuts': accepted,
            'maximum_edges_from_cuts': maximum, 'histograms_at112': boundary,
            'cubic_neighbor_full_degree_histograms':local_degree_histograms,
            'degree11_branch_histograms_at106':boundary106,
            'degree7_blue_neighbor_loads_without_degree11':uniform_degree_loads,
            'outside_degree_states':outside_states, 'global_minimum_degree':8}


def run():
    return {'schema': 'book-degree11-global-cut-v1',
            'scope': 'identity and finite-boundary audits of the written universal counting proof',
            'baseline': baseline(), 'identities': identity_controls(),
            'joint_root_cut': joint_root_cut(), 'finite_boundaries': finite_boundaries()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    result = run()
    serialized = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.write_expected:
        (HERE/'expected.json').write_text(serialized)
    else:
        require(result == json.loads((HERE/'expected.json').read_text()), 'expected result differs')
    print(serialized, end='')


if __name__ == '__main__':
    main()

"""Separate triangle-incidence and weighted-subset audit.

Author: six-books-3, researcher. No imports from check.py.
Exact Python integers; explicit checks work under Python -O.
"""
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json

DIR = Path(__file__).resolve().parent


def check(ok, message):
    if not ok:
        raise ValueError(message)


def matrix(rows):
    n = len(rows)
    check(all(len(row) == n and all(c in '01' for c in row) for row in rows), 'matrix shape')
    A = [[int(c) for c in row] for row in rows]
    check(all(A[i][i] == 0 and all(A[i][j] == A[j][i] for j in range(n))
              for i in range(n)), 'simple symmetry')
    return A


def triangle_pages(A):
    """A monochromatic triangle contributes one page to each of its spines."""
    n = len(A)
    result = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if A[i][j] == A[i][k] == A[j][k]:
                    for a, b in ((i, j), (i, k), (j, k)):
                        result[a][b] += 1
                        result[b][a] += 1
    return result


def baseline():
    raw = (DIR/'baseline21.rows').read_bytes()
    A = matrix(raw.decode().splitlines())
    check(len(A) == 21, 'baseline order')
    C = triangle_pages(A)
    degree_counts = {}
    for row in A:
        key = str(sum(row))
        degree_counts[key] = degree_counts.get(key, 0)+1
    maxima = [max(C[i][j] for i in range(21) for j in range(i+1, 21) if A[i][j] == color)
              for color in (1, 0)]
    result = {'red_edges': sum(sum(row) for row in A)//2, 'degrees': degree_counts,
              'spine_maxima': maxima, 'sha256': hashlib.sha256(raw).hexdigest()}
    check(result['red_edges'] == 93 and degree_counts == {'8':4, '9':16, '10':1}
          and maxima == [3,6], 'baseline result')
    return result


def controls():
    receipts, graph_count, pair_count, row_count, local_count = [], 0, 0, 0, 0
    stream = hashlib.sha256()
    for fi, fixture in enumerate(json.loads((DIR/'fixtures.json').read_text())):
        J = matrix(fixture['rows'])
        h = [sum(row) for row in J]
        check(h == [3]*10+[2], 'fixture degree sequence')
        T = sum(J[i][j]*J[i][k]*J[j][k]
                for i in range(11) for j in range(i+1,11) for k in range(j+1,11))
        core = [row+[1] for row in J]+[[1]*11+[0]]
        C0 = triangle_pages(core)
        check(all(C0[i][j] <= 6-3*core[i][j]
                  for i in range(12) for j in range(i+1,12)), 'root core pages')
        local_count += 66
        receipts.append({'name':fixture['name'], 'triangles':T})
        for m in range(80):
            A = [[0]*22 for _ in range(22)]
            for i in range(11):
                for j in range(11):
                    A[i][j] = J[i][j]
                A[i][11] = A[11][i] = 1
            for b in range(10):
                if m <= 47:
                    size = (m+5*b) % 12
                elif m <= 63:
                    size = 3+(m+b) % 4
                else:
                    size = 4+(m+b) % 2
                order = [((7*m+2*b)+(1+(m+3*b) % 10)*j) % 11 for j in range(11)]
                check(len(set(order)) == 11, 'row permutation')
                bits = [1]*11
                for j in order[:size]:
                    bits[j] = 0
                for i in range(11):
                    A[i][12+b] = A[12+b][i] = bits[i]
            for i in range(10):
                for j in range(i+1,10):
                    color = int(((m+1)*(i+1)+(j+1)*(j+3)+7*fi) % 5 < 2)
                    A[12+i][12+j] = A[12+j][12+i] = color
            stream.update((''.join(''.join(map(str,row)) for row in A)+'\n').encode())
            C = triangle_pages(A)
            M = [[1-A[i][b] for i in range(11)] for b in range(12,22)]
            z = [sum(row) for row in M]
            t = [sum(row[i] for row in M) for i in range(11)]
            E = [[0]*11 for _ in range(11)]
            for i in range(11):
                for j in range(i+1,11):
                    E[i][j] = E[j][i] = 6-3*A[i][j]-C[i][j]
            U = sum(sum(row) for row in E)//2
            UR = sum(E[i][j] for i in range(11) for j in range(i+1,11) if J[i][j])
            F = sum(comb(a,2)-3*a+6 for a in z)
            K = sum(comb(a,2)-4*a+10 for a in z)
            Q = sum(M[b][i]*M[b][j]*J[i][j]
                    for b in range(10) for i in range(11) for j in range(i+1,11))
            check(10-t[10] == U+F, 'first capacity budget')
            check(22-4*t[10] == 3*U+3*K+3*T+UR+Q, 'red capacity budget')
            check(sum(t) == sum(z) == 40+F-K, 'incidence sum')
            for i in range(11):
                check(sum(A[i]) == 11+h[i]-t[i], 'full degree count')
                ei = sum(E[i])
                ui = sum((z[b]-4)*M[b][i] for b in range(10))
                ph = sum(J[i][j]*h[j] for j in range(11))
                pt = sum(J[i][j]*t[j] for j in range(11))
                check((3-h[i])*t[i]-pt == 5*h[i]-h[i]*h[i]+2-2*ph-ei-ui,
                      'row incidence equation')
                row_count += 1
                for j in range(i+1,11):
                    gram = sum(row[i]*row[j] for row in M)
                    p2 = sum(J[i][a]*J[a][j] for a in range(11))
                    value = t[i]+t[j]-8 if J[i][j] else h[i]+h[j]-3
                    check(gram == value-p2-E[i][j], 'pair triangle partition')
                    pair_count += 1
            graph_count += 1
    return {'counts': {'graphs':graph_count, 'local_spines':local_count,
                       'pair_identities':pair_count, 'row_identities':row_count},
            'fixtures':receipts, 'control_stream_sha256':stream.hexdigest()}


def choose(n, r):
    return comb(n,r) if 0 <= r <= n else 0


def paired_subsets(n, ra, rb):
    for overlap in range(min(ra,rb)+1):
        weight = choose(n,ra)*choose(ra,overlap)*choose(n-ra,rb-overlap)
        if weight:
            yield overlap, weight


def joint_roots():
    blue, red = [], []
    for k in (10,11):
        minima, totals = [], []
        for n, allowed in ((8,(2,)), (k-3,(0,1,2))):
            distribution = {}
            for ra in allowed:
                for rb in allowed:
                    for overlap, weight in paired_subsets(n,ra,rb):
                        common_blue = n-ra-rb+overlap
                        distribution[common_blue] = distribution.get(common_blue,0)+weight
            minima.append(min(distribution))
            totals.append(sum(distribution.values()))
        check(sum(minima)>6, 'blue joint-root bound')
        blue.append({'degree_x':k, 'minimum_V':minima[0], 'minimum_X':minima[1],
                     'V_subset_pairs':totals[0], 'X_subset_pairs':totals[1]})
        counters = {'examined':0, 'degrees_at_least7':0,
                    'red_cap_survivors':0, 'capacity_cut_survivors':0}
        for ov, wv in paired_subsets(8,1,1):
            for ra in (0,1):
                for rb in (0,1):
                    for ox, wx in paired_subsets(k-3,ra,rb):
                        for da in range(14-k):
                            for db in range(14-k):
                                for od, wd in paired_subsets(13-k,da,db):
                                    weight = wv*wx*wd
                                    counters['examined'] += weight
                                    degree_a, degree_b = 4+ra+da, 4+rb+db
                                    if min(degree_a,degree_b)<7:
                                        continue
                                    counters['degrees_at_least7'] += weight
                                    pages = 2+ov+ox+od
                                    if pages>3:
                                        continue
                                    counters['red_cap_survivors'] += weight
                                    outside_at_a = degree_b-1-pages
                                    outside_at_b = degree_a-1-pages
                                    if degree_a == 7 and outside_at_a<6:
                                        continue
                                    if degree_b == 7 and outside_at_b<6:
                                        continue
                                    counters['capacity_cut_survivors'] += weight
        check(counters['capacity_cut_survivors']==0, 'red joint-root bound')
        red.append({'degree_x':k, **counters})
    return {'blue':blue,'red':red}


def boundaries():
    budgets = []
    for tx in (2,3,4,5,6):
        states = []
        budget = 22-4*tx
        for total in range(budget//3+1):
            for U in range(total+1):
                for K in range(total-U+1):
                    T = total-U-K
                    for UR in range(U+1):
                        Q = budget-3*total-UR
                        if Q>=0 and 10-tx-U>=0:
                            states.append([U,K,T,UR,Q])
        budgets.append({'t_x':tx, 'states':sorted(states)})
    check(budgets[-1]['states']==[], 'degree7 budget')
    check(budgets[-2]['states']==[[0,0,0,0,2]], 'degree8 budget')
    load = []
    for low in range(1,11):
        for six in range(11):
            for seven in range(11):
                five = low-2*six-3*seven
                four = 10-low-five-six-seven
                if five>=low and min(five,four)>=0:
                    load.append([low,four,five,six,seven])
    check(load==[[j,10-2*j,j,0,0] for j in range(1,6)], 'degree-load balance')
    small = []
    for n in (1,3,5):
        edges = [(i,j) for i in range(n) for j in range(i+1,n)]
        count, tf = 0,0
        for bits in range(1<<len(edges)):
            A = [[0]*n for _ in range(n)]
            for e,(i,j) in enumerate(edges):
                A[i][j]=A[j][i]=(bits>>e)&1
            if [sum(row) for row in A] != [2]+[3]*(n-1):
                continue
            count += 1
            triangles = sum(A[i][j]*A[i][k]*A[j][k]
                            for i in range(n) for j in range(i+1,n) for k in range(j+1,n))
            tf += int(triangles==0)
        check(tf==0, 'small connectedness component')
        small.append({'order':n,'all_graphs':1<<len(edges), 'degree_candidates':count,
                      'triangle_free':tf})
    accepted, maximum, at112 = 0,-1,[]
    for k in range(23):
        for a in range(23-k):
            for b in range(23-k-a):
                for c in range(23-k-a-b):
                    d = 22-k-a-b-c
                    degree_sum = 220+k-3*a-2*b-c
                    if a or degree_sum%2 or (k>0 and c==0):
                        continue
                    e = degree_sum//2
                    if 49*k>3*e:
                        continue
                    accepted += 1
                    maximum=max(maximum,e)
                    if e==112:
                        at112.append([a,b,c,d,k])
    at112.sort()
    check(maximum==112 and at112==[[0,0,1,16,5],[0,0,2,14,6]], 'global upper bound')
    local = []
    for a in range(3):
        for b in range(3):
            deficit = 2*a+b
            if deficit>2:
                continue
            local.append({'n8':a,'n9':b,'n10':10-a-b,'Delta':deficit,
                          'minimum_full_edges':108-deficit})
    at106=[]
    # Root degree11, distinguished neighbor degree9, six degree9 and
    # four degree10 vertices in the cubic outside B, plus ten neighbors.
    for loads in local:
        if loads['minimum_full_edges']==106:
            counts={7:0,8:loads['n8'],9:7+loads['n9'],10:4+loads['n10'],11:1}
            check(sum(counts.values())==22 and sum(d*c for d,c in counts.items())==212,
                  '106-edge degree sum')
            at106.append([counts[d] for d in range(7,12)])
    at106.sort()
    check(at106==[[0,0,9,12,1],[0,1,7,13,1]], '106-edge boundary')
    no11=[]
    for a in range(15):
        for b in range(15-a):
            c=-3*a-2*b  # Total deficiency from ten must be zero.
            if 0<=c<=14-a-b:
                no11.append([a,b,c,14-a-b-c])
    check(no11==[[0,0,0,14]], 'degree7 uniform-load consequence')
    outside=[]
    for z in range(12):
        if comb(z,2)-4*z+10>2:
            continue
        for degree in range(7,12):
            internal=degree-11+z
            if 3<=internal<=z:
                outside.append([z,internal,degree])
    check(min(s[2] for s in outside)==8 and sorted({s[0] for s in outside})==[3,4,5,6],
          'outside minimum-degree cut')
    return {'budgets':budgets,'balanced_load_histograms':load, 'small_components':small,
            'global_degree_histograms_surviving_cuts':accepted,
            'maximum_edges_from_cuts':maximum, 'histograms_at112':at112,
            'cubic_neighbor_full_degree_histograms':local,
            'degree11_branch_histograms_at106':at106,
            'degree7_blue_neighbor_loads_without_degree11':no11,
            'outside_degree_states':outside, 'global_minimum_degree':8}


def main():
    actual = {'schema':'book-degree11-global-cut-v1',
              'scope':'identity and finite-boundary audits of the written universal counting proof',
              'baseline':baseline(), 'identities':controls(),
              'joint_root_cut':joint_roots(), 'finite_boundaries':boundaries()}
    check(actual == json.loads((DIR/'expected.json').read_text()), 'independent expected mismatch')
    print(json.dumps(actual,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()

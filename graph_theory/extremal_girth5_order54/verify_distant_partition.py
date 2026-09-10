#!/usr/bin/env python3
"""Exact controls for the whole 2P3+P2+5K1 exclusion; standard library only."""
import json
from itertools import combinations
from pathlib import Path
from verify import graph, require, hoffman_singleton_edges, check_girth_and_identities
from verify_boundary import rational_rank
from forest_profiles import profiles
from shared_center_cases import RESIDUAL

HERE = Path(__file__).resolve().parent


def check_partition_control(G):
    """Construct far sets directly, then check the matrix-derived incidence rule."""
    check_girth_and_identities(G)
    n = len(G)
    degrees = list(map(len, G))
    k = max(degrees)
    F = [{u for u in range(n) if u != v and u not in G[v]
          and not (G[u] & G[v])} for v in range(n)]
    T = {v for v in range(n) if degrees[v] == k and not F[v]}
    require(T, 'control has no maximum-degree sink')
    C = [G[v] & T for v in range(n)]
    partition_rows = 0
    for v in range(n):
        require(not (F[v] & T), 'a sink appears in a far set')
        for t in T:
            count = sum(t in C[u] for u in F[v])
            expected = (k-degrees[v]) * (t not in C[v])
            require(count == expected, 'entrywise far-incidence identity')
        if degrees[v] == k-1:
            blocks = [C[v]] + [C[u] for u in sorted(F[v])]
            require(set().union(*blocks) == T, 'partition misses a high point')
            require(sum(map(len, blocks)) == len(T), 'partition overlap')
            partition_rows += 1
    # Check the polynomial identity by adjacency/common-neighbor definitions.
    for u in range(n):
        for v in range(n):
            lhs = len(G[u] & G[v]) + int(v in G[u]) - (k-1)*(u == v)
            rhs = 1-int(v in F[u])-(k-degrees[u])*(u == v)
            require(lhs == rhs, 'polynomial diagonal/off-diagonal identity')
    return {'n': n, 'edges': sum(degrees)//2, 'sink_count': len(T),
            'partition_rows': partition_rows}


def minimum_dot(weights, budget=9):
    """Independent exact DP: every integer epsilon with squared cost <=9."""
    states = {0: 0}
    for weight in weights:
        new = {}
        for cost, dot in states.items():
            for eps in range(-3, 4):
                c = cost + eps*eps
                if c <= budget:
                    new[c] = min(new.get(c, 10**9), dot + weight*eps)
        states = new
    return min(states.values())


def main():
    hs = hoffman_singleton_edges()
    controls = [check_partition_control(graph(50, sorted(hs-deleted)))
                for deleted in (set(), {(0,1)}, {(0,1),(2,3)})]
    data = json.loads((HERE/'lower_bound_54_185.json').read_text())
    G = graph(data['n'], data['edges'])
    controls.append(check_partition_control(G))
    require(sum(x['partition_rows'] for x in controls) > 0, 'vacuous controls')
    print('PASS: entrywise distant-neighborhood partitions on four graph controls')

    # Check the rank deduction on the established degree-eight-sink fixture.
    d = list(map(len, G)); T = [v for v in range(54) if d[v] == 8]
    low = [v for v in range(54) if v not in T]
    F = [{u for u in range(54) if u != v and u not in G[v]
          and not G[u] & G[v]} for v in range(54)]
    require(len(T) == 4 and all(not F[v] for v in T), 'rank fixture changed')
    K = [[int(v in F[u])+(8-d[u])*(u == v) for v in low] for u in low]
    P = [[len(G[u] & G[v])+int(v in G[u])-7*(u == v)
          for v in range(54)] for u in range(54)]
    rank_k, rank_p = rational_rank(K), rational_rank(P)
    require(rank_p == 1+rank_k == 48, 'rank decomposition fixture')

    require(24*7+13*16-13*5-17*8-24*7 == 7, 'epsilon total arithmetic')
    for h in range(3):
        require(5*h+8*(3+h)+7*(5-2*h) == 59-h, 'high local balance')
    require(2*5-3*7 == -11, 'weighted epsilon balance')
    require(121 > 9*4 and 64 > 9*6, 'strict quadratic contradictions')
    # The corresponding parameter-dependent identities on an actual graph.
    S = sum(x-6 for x in d)
    # Extend epsilon as s+d-14 for this fixture, which also has degrees4,5.
    eps = {v: sum(d[u]-6 for u in G[v])+d[v]-14 for v in low}
    h = {t: len(G[t] & set(T)) for t in T}
    for t in T:
        require(sum(eps[v] for v in G[t] if v in eps) == S-50+h[t],
                'generalized local epsilon identity')
    require(sum(len(G[v] & set(T))*eps[v] for v in low)
            == len(T)*(S-50)+sum(h.values()), 'weighted epsilon identity control')
    print('PASS: exact epsilon balances and rank decomposition control')

    expected_histograms = {
        1: ({2:2,3:15}, {1:6,2:15,3:3}),
        2: ({2:2,3:15}, {0:1,1:3,2:18,3:2}),
        4: ({2:3,3:13,4:1}, {1:5,2:17,3:2}),
        6: ({2:4,3:11,4:2}, {1:4,2:19,3:1}),
    }
    require(set(RESIDUAL) == set(expected_histograms), 'prior residual profile cover')
    rows = []
    for index, (a,b) in expected_histograms.items():
        row6,row7 = profiles(5,2)[index]
        require({c:n for c,n in enumerate(row6) if n} == a, 'six histogram mismatch')
        require({c:n for c,n in enumerate(row7) if n} == b, 'seven histogram mismatch')
        require(sum(a.values()) == 17 and sum(b.values()) == 24, 'profile sizes')
        require(sum(c*n for c,n in a.items()) == 49 and
                sum(c*n for c,n in b.items()) == 45, 'profile incidence totals')
        weights = [c-3 for c,n in a.items() for _ in range(n)]
        R = sum(x*x for x in weights)
        pos = sum(max(c-3,0)*n for hist in (a,b) for c,n in hist.items())
        ceilings = {c:(c-1+pos)//3 for c in b}
        if index != 6:
            require(all(ceilings[c] <= 0 for c in b if c < 3), 'seven epsilon signs')
        else:
            require(ceilings == {1:0,2:1,3:1}, 'profile-six epsilon ceilings')
        dot_min = minimum_dot(weights)
        q_bound = 2 if index == 6 else 0
        require(dot_min-q_bound > -11, 'independent integer contradiction')
        rows.append({'profile':index,'R':R,'positive_excess':pos,
                     'epsilon_ceilings':{str(c):v for c,v in ceilings.items()},
                     'six_dot_minimum':dot_min,
                     'total_dot_lower_bound':dot_min-q_bound})
    require([r['R'] for r in rows] == [2,2,4,6], 'quadratic norms')
    # The only possible far-size multiset for a special seven vertex.
    triples = [t for t in combinations(range(41),3)
               if sum(([2]*4+[3]*11+[4]*2+[1]*4+[2]*19+[3])[x] for x in t) == 11]
    require(triples and all(15 in t and 16 in t for t in triples), 'forced two c=4 vertices')
    require(len(triples) == 12, 'all possible degree-six/seven c=3 third vertices')
    print('PASS: all four inherited profiles excluded by exact integer bounds')

    universe = set(range(5)); pairs = [set(p) for p in combinations(range(5),2)]
    counts = [0]*11
    for mask in range(1 << len(pairs)):
        chosen = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        if all(len((universe-p) & (universe-q)) <= 1 for p,q in combinations(chosen,2)):
            require(all(not p & q for p,q in combinations(chosen,2)), 'complement intersection identity')
            counts[len(chosen)] += 1
    require(counts == [1,10,15]+[0]*8, 'five-point packing complete enumeration')
    require(max(i for i,n in enumerate(counts) if n) == 2, 'special-vertex packing bound')
    # Nonvacuous sharp positive control; a third overlapping pair is rejected.
    positive = [{0,1},{2,3}]
    require(len((universe-positive[0]) & (universe-positive[1])) == 1, 'packing positive control')
    require(any(len((universe-p)&(universe-q)) > 1
                for p,q in combinations(positive+[{0,4}],2)), 'packing rejection control')
    print('PASS: complete five-point packing; at most two special seven vertices')
    remaining = ['5_0','5_1','6_0','6_1']
    cover_sizes = [len(profiles(m,k)) for m,k in [(5,0),(5,1),(6,0),(6,1)]]
    require(cover_sizes == [49,29,24,13] and sum(cover_sizes) == 115, 'remaining cover')
    result = {'verified':True,'excluded_forest':'2P3+P2+5K1','profiles':rows,
              'special_required_minimum':4,'special_packing_maximum':2,
              'five_point_packing_counts':counts,'controls':controls,
              'control_rank_K':rank_k,'control_rank_polynomial':rank_p,
              'remaining_forests':remaining,'remaining_histograms':115}
    path = HERE/'distant_partition_expected.json'
    if path.exists():
        require(json.loads(path.read_text()) == result, 'expected record differs')
    print(json.dumps(result,sort_keys=True))
    return result


if __name__ == '__main__':
    main()

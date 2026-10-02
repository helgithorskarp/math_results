"""Fresh physical leave frames and literal packing counts; six-reviewer-5.

No researcher executable or expected fixture import. Frames are complete
necessary local degree controls, not asserted realizable twenty-stars.
"""
import hashlib
import json
import math
from itertools import combinations
from pathlib import Path


def require(ok, message):
    if not ok: raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def digest(value):
    return hashlib.sha256((canonical(value)+'\n').encode()).hexdigest()


def compositions(total, length):
    if length == 1:
        yield (total,); return
    for first in range(1, total-length+2):
        for tail in compositions(total-first, length-1): yield (first,)+tail


def physical_rows():
    frames = []; role_checks = 0; charge_checks = 0; nontrivial_q = 0
    for h in range(1, 6):
        high = tuple(range(1, h+1)); low = tuple(range(h+1, 18))
        edges = tuple(combinations(high, 2))
        for weights in compositions(5, h):
            for selected in combinations(edges, h-1):
                graph = {p:set() for p in range(1, 18)}
                for u, v in selected: graph[u].add(v); graph[v].add(u)
                next_low = 0
                for point, weight in zip(high, weights):
                    friends = 1+3*weight-len(graph[point])
                    require(friends >= 0, 'negative low-friend requirement')
                    for q in low[next_low:next_low+friends]:
                        graph[point].add(q); graph[q].add(point)
                    next_low += friends
                require(next_low == len(low), 'all low points assigned exactly once')
                require(sum(map(len, graph.values())) == 32, 'sixteen physical leave edges')
                replication = {}
                for p in graph:
                    require((16-len(graph[p])) % 3 == 0, 'literal replication inversion')
                    replication[p] = (16-len(graph[p]))//3
                require(sum(replication.values()) == 80, 'twenty quadruple incidence control')
                require(tuple(5-replication[p] for p in high) == weights, 'weighted row recovery')
                require(all(replication[p] == 5 and len(graph[p]) == 1 for p in low), 'literal low-friend degrees')
                require(all(not(graph[p] & set(low)) for p in low), 'no low-low leaves')
                for mask in range(1 << h):
                    hubs = {p for i,p in enumerate(high) if mask >> i & 1}
                    k = len(hubs); q = sum(u in hubs or v in hubs for u,v in selected)
                    e = 5-h; unit = e == 0; z = int(unit and k == 1 and q == 0)
                    require(k == 0 or q >= k-1, 'coupled physical hub charge')
                    require((q == 0) == all(not(graph[p] & set(high)) for p in hubs), 'all marked hubs isolated iff q0')
                    if unit: require(k <= z+2*q, 'new pointwise unit charge')
                    else: require(k <= q+1-int(k == 0), 'new pointwise nonunit charge')
                    charge_checks += 2
                    # Every proposed second unit center has pair replication4.
                    # Test literal first-row hypotheses for both orientations.
                    if z or (not unit and k >= 1 and q == 0):
                        for neighbor in set(high)-hubs:
                            if replication[neighbor] != 4: continue
                            for mark in hubs:
                                require(mark != neighbor and mark != 0 and neighbor != 0, 'three distinct roles')
                                require(replication[mark] < 5 and not(graph[mark] & set(high)), 'literal isolated deficient mark')
                                role_checks += 1
                    if unit and k == 1 and q > 0: nontrivial_q += 1
                    frames.append([h, weights, selected, sorted(hubs), e, k, q, z])
    require(len(frames) == 8162 and nontrivial_q > 0, 'complete enlarged coupled frame population')
    return {'coupled_frames':len(frames), 'pointwise_charge_checks':charge_checks,
            'literal_selector_role_checks':role_checks, 'unit_k1_qpositive_controls':nontrivial_q,
            'whole_ordered_frame_sha256':digest(frames)}


def load_code(path):
    raw = Path(path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == 'cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d', 'credited live primary bytes')
    lines = raw.decode().splitlines()
    require(len(lines) == 69 and all(len(s) == 18 and set(s) <= {'0','1'} for s in lines), 'primary binary rows')
    words = tuple(frozenset(p for p,c in enumerate(s) if c == '1') for s in lines)
    require(len(set(words)) == 69 and all(len(w) == 5 for w in words), '69 distinct weight-five words')
    require(all(len(a & b) <= 2 for a,b in combinations(words, 2)), 'every primary pair intersection')
    return words


def primary_partitions(path):
    words = load_code(path); points = set(range(18)); N = len(words)
    point = {p:sum(p in w for w in words) for p in points}
    pairs = {tuple(sorted((p,q))):sum({p,q} <= w for w in words) for p,q in combinations(points, 2)}
    delta = {pair:5-value for pair,value in pairs.items()}
    covered = set()
    for word in words:
        for triple in combinations(sorted(word), 3):
            require(triple not in covered, 'unique actual triple ownership'); covered.add(triple)
    missing = [t for t in combinations(range(18), 3) if t not in covered]
    require(len(covered) == 690 and len(missing) == 126, 'primary owned/unowned triples')
    require(max(point.values()) <= 20 and max(pairs.values()) <= 5, 'actual prior caps')
    records = []; predicates = 0; signed_E = 0; nonzero_corrections = 0
    for m in range(1, 6):
        for chosen in combinations(range(18), m):
            H = set(chosen); S = points-H; n = len(S)
            P = sum(pairs[pair] for pair in pairs if set(pair) <= H)
            T = sum(set(t) <= H for t in covered)
            A0 = sum(set(t) <= S for t in missing)
            high = {s:{p for p in points-{s} if delta[tuple(sorted((s,p)))] > 0} for s in S}
            E = sum(5-len(high[s]) for s in S)
            D_S = sum(20-point[s] for s in S)
            W = sum(value for pair,value in delta.items() if len(set(pair) & H) == 1)
            K = sum(len(high[s] & H) for s in S)
            X = sum(value-1 for pair,value in delta.items() if set(pair) <= S and value > 0)
            Q = 0; low_leaves = 0; tau = 0; bad = 0
            for triple in missing:
                if set(triple) <= S:
                    support = sum(delta[pair] > 0 for pair in combinations(triple, 2))
                    tau += support == 3; bad += support <= 1
                for s in set(triple) & S:
                    ends = set(triple)-{s}
                    if ends <= high[s] and ends & H: Q += 1
                    if not(ends & high[s]): low_leaves += 1
            hub_sum = sum(point[p] for p in H)
            require(A0 == math.comb(n, 3)-10*N+6*hub_sum-3*P+T, 'literal homogeneous word polynomial')
            require(W == 85*m-4*hub_sum-2*(5*math.comb(m, 2)-P), 'actual mixed weighted deficit')
            require(E == W-K+2*X-4*D_S, 'signed nonsaturated correction')
            B = 4*n-math.comb(n, 3)+10*N-6*hub_sum
            require(E+Q+2*tau == B+3*P-T+6*D_S+low_leaves+bad, 'whole general leave/triple identity')
            predicates += 4; signed_E += E < 0
            nonzero_corrections += bool(D_S or low_leaves or bad)
            records.append([chosen, P, T, A0, E, Q, W, K, X, tau, D_S, low_leaves, bad])
    require(len(records) == 12615 and signed_E > 0 and nonzero_corrections > 0, 'nonvacuous general controls')
    return {'primary_words':N,'word_pair_checks':math.comb(N,2),'hub_partitions':len(records),
            'literal_general_identity_checks':predicates,'signed_E_partitions':signed_E,
            'nonsaturation_or_lowleave_correction_partitions':nonzero_corrections,
            'whole_ordered_partition_sha256':digest(records)}

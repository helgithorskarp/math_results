"""Necessary rows: classified unit leaves, all nonunit high-leave graphs."""
from collections import Counter
import itertools


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def canonical(edges, h):
    return min(tuple(sorted(tuple(sorted((p[a], p[b]))) for a, b in edges))
               for p in itertools.permutations(range(h)))


def unit_graphs(data):
    fixtures = data['fixtures']
    need([r['original_fixture_index'] for r in fixtures] ==
         [11,15,16,17,19,20,21,22], 'missing/repeated credited unit fixture')
    graphs = set()
    literal = set()
    for row in fixtures:
        qs = row['quadruples']
        need(len(qs) == 20 and all(len(q) == len(set(q)) == 4 for q in qs),
             'invalid twenty-quadruple fixture')
        need(all(type(p) is int and 0 <= p < 17 for q in qs for p in q),
             'invalid fixture point domain')
        image = tuple(sorted(tuple(sorted(q)) for q in qs))
        need(image not in literal, 'duplicated literal fixture')
        literal.add(image)
        pairs = Counter(ab for q in qs for ab in itertools.combinations(sorted(q),2))
        need(max(pairs.values()) == 1, 'repeated fixture pair')
        rho = [sum(p in q for q in qs) for p in range(17)]
        need(sorted(rho) == [4]*5+[5]*12, 'wrong unit replications')
        high = [p for p in range(17) if rho[p] == 4]
        lookup = {p:i for i,p in enumerate(high)}
        need(not any(rho[a] == rho[b] == 5 and (a,b) not in pairs
                     for a,b in itertools.combinations(range(17),2)),
             'low-low fixture leave')
        leave = [(lookup[a],lookup[b]) for a,b in itertools.combinations(high,2)
                 if (a,b) not in pairs]
        need(len(leave) == 4, 'wrong unit high-leave count')
        graphs.add(canonical(leave,5))
    known = {
        canonical(((0,1),(1,2),(2,3),(3,4)),5),
        canonical(((0,1),(0,2),(0,3),(0,4)),5),
        canonical(((0,1),(1,2),(2,3),(3,0)),5),
        canonical(((0,1),(0,2),(0,3),(3,4)),5),
    }
    need(graphs == known, 'unit graph types differ from the stated four')
    check_two_hub_charge(graphs)
    return graphs


def check_two_hub_charge(graphs):
    for graph in graphs:
        for hubs in itertools.combinations(range(5),2):
            need(sum(a in hubs or b in hubs for a,b in graph) >= 2,
                 'two deficient hubs have charge less than two')


def statistics(delta, leave, hubs):
    h = len(delta)
    e = 5-h
    ld = Counter(p for ab in leave for p in ab)
    d = tuple(delta[p] if p < h else 0 for p in hubs)
    q = sum(a in hubs or b in hubs for a,b in leave)
    g = h-sum(p < h for p in hubs)
    good = tuple(int((e == 0 and d[j] == 1 or e == 1 and d[j] == 2)
                     and ld[p] == 0) for j,p in enumerate(hubs))
    return d + (e,q,g) + good


def necessary_rows(graphs):
    types = set()
    for delta in ((4,1),(3,2),(3,1,1),(2,2,1),(2,1,1,1),(1,1,1,1,1)):
        h = len(delta)
        for leave in itertools.combinations(list(itertools.combinations(range(h),2)),h-1):
            if h == 5 and canonical(leave,h) not in graphs:
                continue
            # Three dummy low points suffice for three distinct hub labels;
            # every actual link has at least twelve low points.
            for hubs in itertools.permutations(range(h+3),3):
                row = statistics(delta,leave,hubs)
                if row[3]+row[4] <= 3:
                    types.add(row)
    bases = sorted(r for r in types if r[3]+r[4] == 0)
    need(len(bases) == 4 and {r[:3] for r in bases} ==
         {(0,0,0),(1,0,0),(0,1,0),(0,0,1)}, 'wrong zero-cost row types')
    for row in types:
        if sum(d > 0 for d in row[:3]) >= 2:
            need(row[4] >= 2, 'nonunit two-hub charge')
    return sorted(types), bases

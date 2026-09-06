#!/usr/bin/env python3
"""Optional certificate producer; requires python-sat 1.9.dev15."""
import itertools as it
import json
from pathlib import Path
from pysat.solvers import Solver

D = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def edge(a, b):
    return min((a-b) % 43, (b-a) % 43) in D


def find_clique(rows, mask, k):
    if k == 0:
        return []
    while mask.bit_count() >= k:
        bit = mask & -mask
        mask ^= bit
        v = bit.bit_length()-1
        q = find_clique(rows, mask & rows[v], k-1)
        if q is not None:
            return [v]+q
    return None


def opposite(rows):
    full = (1 << len(rows))-1
    return [full ^ (1 << v) ^ r for v, r in enumerate(rows)]


def colored_graph(core_rows, stars, chosen, colors):
    rows = core_rows[:] + [0]*len(chosen)
    for j, s in enumerate(chosen):
        rows[34+j] = stars[s]
        for u in range(34):
            if stars[s] >> u & 1:
                rows[u] |= 1 << (34+j)
    for (a,b), c in zip(it.combinations(range(len(chosen)),2), colors):
        if c:
            rows[34+a] |= 1 << (34+b)
            rows[34+b] |= 1 << (34+a)
    return rows


def produce():
    covers = set()
    for i,j in it.combinations_with_replacement(range(9),2):
        gaps = [5]*9
        gaps[i] -= 1
        gaps[j] -= 1
        positions = [0]
        for g in gaps[:-1]:
            positions.append(positions[-1]+g)
        for a in range(43):
            covers.add(tuple(sorted(22*(v+a) % 43 for v in positions)))
    def orbit(ds):
        return {tuple(sorted((a+s*v) % 43 for v in ds))
                for a in range(43) for s in (-1,1)}
    representatives = sorted({min(orbit(ds)) for ds in covers})
    need(len(covers) == 215 and len(representatives) == 5, 'cover census')
    records = []
    for index, deleted in enumerate(representatives):
        old = [v for v in range(43) if v not in deleted]
        rr = [sum(1 << j for j,b in enumerate(old) if a != b and edge(a,b)) for a in old]
        bb = opposite(rr)
        clauses = []
        for q in it.combinations(range(34),4):
            cs = {edge(old[u],old[v]) for u,v in it.combinations(q,2)}
            if len(cs) == 1:
                sign = -1 if True in cs else 1
                clauses.append([sign*(v+1) for v in q])
        stars = []
        with Solver(name='cadical195', bootstrap_with=clauses) as solver:
            while solver.solve():
                model = solver.get_model()[:34]
                stars.append(sum(1 << i for i,x in enumerate(model) if x > 0))
                solver.add_clause([-x for x in model])
        stars.sort()
        full = (1 << 34)-1
        allowed, adj = {}, [0]*len(stars)
        for a,x in enumerate(stars):
            for b in range(a,len(stars)):
                y = stars[b]
                colors = []
                if find_clique(bb, full ^ (x|y), 3) is None:
                    colors.append(0)
                if find_clique(rr, x&y, 3) is None:
                    colors.append(1)
                if a == b:
                    need(not colors, 'a repeated attachment can occur')
                elif colors:
                    allowed[a,b] = colors
                    adj[a] |= 1 << b
                    adj[b] |= 1 << a
        cohorts = []
        def visit(chosen, available):
            cohorts.append(chosen)
            while available:
                bit = available & -available
                available ^= bit
                v = bit.bit_length()-1
                visit(chosen+[v],available & adj[v])
        visit([], (1 << len(stars))-1)
        pair_cap = max(map(len,cohorts))
        # Complete graph assembly for discovery; physical certificates below
        # permit an independent checker to avoid trusting this recursion.
        best_chosen, best_rows = [], rr
        terminal = []
        for chosen in sorted(cohorts, key=lambda q: (-len(q),q)):
            if len(chosen) < len(best_chosen):
                break
            pools = [allowed[a,b] for a,b in it.combinations(chosen,2)]
            for colors in it.product(*pools):
                rows = colored_graph(rr,stars,chosen,colors)
                forbidden = None
                for c, r in ((0,opposite(rows)),(1,rows)):
                    q = find_clique(r,(1 << len(rows))-1,5)
                    if q is not None:
                        forbidden = {'color':c,'vertices':q}
                        break
                if forbidden is None:
                    if len(chosen) > len(best_chosen):
                        best_chosen, best_rows = chosen[:], rows
                elif len(chosen) == pair_cap:
                    terminal.append({'star_ids':chosen, 'colors':list(colors),
                                     'five':forbidden})
        max_added = len(best_chosen)
        need(max_added in (pair_cap,pair_cap-1), 'unexpected terminal depth')
        if max_added == pair_cap:
            terminal = []
        red_edges = [[u,v] for u,v in it.combinations(range(len(best_rows)),2)
                     if best_rows[u] >> v & 1]
        records.append({'class':index,'deleted':list(deleted),'stars':stars,
                        'pair_cap':pair_cap,'maximum_added':max_added,
                        'terminal':terminal,
                        'maximal_witness':{'n':len(best_rows),'red_edges':red_edges,
                                           'star_ids':best_chosen}})
    return {'schema':1,'red_distances':sorted(D),'minimum_deletions':9,
            'minimum_deletion_sets':215,'dihedral_classes':5,'records':records}


if __name__ == '__main__':
    print(json.dumps(produce(),sort_keys=True,separators=(',',':')))

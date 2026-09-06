#!/usr/bin/env python3
"""Physical edge-list audit. Imports no search, clause or indexing producer."""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

N = 43
ACTION = tuple(3*(v//3)+(v+1)%3 if v<33 else v for v in range(N))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    lines = Path(path).read_text().splitlines()
    need(lines and lines[0] == '43', 'order header')
    pairs = [tuple(map(int, s.split())) for s in lines[1:]]
    need(all(len(e) == 2 and 0 <= e[0] < e[1] < N for e in pairs), 'physical pairs')
    need(pairs == sorted(set(pairs)), 'unique sorted pairs')
    return set(pairs)


def literal(red):
    """All 962,598 literal five-sets; early exit after both colors appear."""
    rows = [[int(tuple(sorted((a,b))) in red) for b in range(N)] for a in range(N)]
    bad = [[], []]
    for q in combinations(range(N), 5):
        color = rows[q[0]][q[1]]
        if all(rows[a][b] == color for a,b in combinations(q,2)):
            bad[color].append(q)
    return bad


def recursive(red):
    """Different algorithm: bit-intersection clique recursion in each color."""
    masks = [0]*N
    for a,b in red:
        masks[a] |= 1<<b
        masks[b] |= 1<<a
    allbits = (1<<N)-1
    def cliques(rows):
        found = []
        def visit(prefix, candidates):
            if len(prefix) == 5:
                found.append(tuple(prefix))
                return
            if candidates.bit_count() < 5-len(prefix):
                return
            while candidates:
                bit = candidates & -candidates
                candidates ^= bit
                v = bit.bit_length()-1
                visit(prefix+[v], candidates & rows[v])
        visit([],allbits)
        return found
    return [cliques([allbits ^ row ^ (1<<v) for v,row in enumerate(masks)]),cliques(masks)]


def audit(path, coreword, neighborhoods=False):
    red = read(path)
    for a,b in combinations(range(N),2):
        image = tuple(sorted((ACTION[a],ACTION[b])))
        need(((a,b) in red) == (image in red), 'C3 action')
    for i in range(11):
        need(all(((a,b) in red) == (i<4) for a,b in combinations(range(3*i,3*i+3),2)), 'internal colors')
    word = ''.join(str(int((3*i,3*j+d) in red)) for i,j in combinations(range(4),2) for d in range(3))
    need(word == coreword, 'core word')
    bad = literal(red)
    need(bad == recursive(red), 'literal/recursive defects differ')
    total = sum(map(len,bad))
    unseen = {tuple(q) for group in bad for q in group}
    orbits = []
    while unseen:
        q = min(unseen)
        orbit = {q}
        for _ in range(2):
            q = tuple(sorted(ACTION[v] for v in q))
            orbit.add(q)
        need(orbit <= unseen, 'defect orbit closure')
        unseen -= orbit
        rep = min(orbit)
        orbits.append({'representative':rep,'size':len(orbit),'red':all(e in red for e in combinations(rep,2))})
    degrees = [sum(tuple(sorted((a,b))) in red for b in range(N) if b!=a) for a in range(N)]
    report = {'red_edges':len(red),'red_k5':len(bad[1]),'blue_k5':len(bad[0]),
              'defects':total,'defect_orbits':orbits,'degree_histogram':dict(sorted(Counter(degrees).items())),
              'degrees':degrees,'empty_fixed_vertices':[f for f in range(33,43) if not any((v,f) in red for v in range(12))],
              'core_word':word,'target_graph':total==0}
    if neighborhoods:
        # Discover every physical unordered-pair action orbit. Freeze internal
        # triangle and red-core pairs; the other 302 orbits are the search moves.
        left = set(combinations(range(N),2));moves=[]
        while left:
            e=min(left);orbit={e}
            for _ in range(2):
                e=tuple(sorted(ACTION[v] for v in e));orbit.add(e)
            need(orbit<=left,'pair orbit partition');left-=orbit
            a,b=min(orbit)
            if b<12 or (b<33 and a//3==b//3):
                continue
            moves.append(orbit)
        need(len(moves)==302,'physical move count')
        values=[sum(map(len,recursive(red ^ m))) for m in moves]
        report['one_orbit_neighbors']={'moves':len(moves),'minimum':min(values),
           'improving':sum(s<total for s in values),'neutral':sum(s==total for s in values),
           'score_histogram':dict(sorted(Counter(values).items()))}
    return report


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--edges',type=Path,required=True)
    p.add_argument('--word',required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--neighbors',action='store_true')
    a=p.parse_args();result=audit(a.edges,a.word,a.neighbors)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('VERIFIED',result['defects'],'defects;',result['red_k5'],'red;',result['blue_k5'],'blue')


if __name__=='__main__':
    main()

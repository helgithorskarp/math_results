"""Forward-incidence generator of compact negative-unit RUP certificates."""
from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from geometry import DIRS, affine


def chamber(n):
    return tuple((x,y) for x in range(-20*n,20*n+1)
                 for y in range(-20*n,20*n+1)
                 if -12*n<x-y<12*n and -7*n<x+2*y<10*n
                 and -4*n<2*x+y<19*n)


def clauses_for(n, fixture):
    cells = chamber(n)
    poses = [dict(r,pose=r['pose'][:4]+[n*t for t in r['pose'][4:]])
             for r in fixture['placements']]
    incidence = defaultdict(list)
    prefix = [defaultdict(set) for _ in range(5)]
    images = []
    for r in poses:
        image = [affine([p],r['pose'])[0] for p in cells]
        images.append(image)
        for v,q in enumerate(image):
            incidence[q].append(v)
            for k in range(r['level'],5):
                prefix[k][q].add(v)
    zero = set()
    edges = set()
    for row in incidence.values():
        mult = Counter(row)
        zero.update(v for v,m in mult.items() if m>1)
        edges.update(itertools.combinations(sorted(mult),2))
    implications = set()
    for k in range(4):
        for j,r in enumerate(poses):
            if r['level']>k:
                continue
            for p,(x,y) in enumerate(images[j]):
                for a,b in DIRS:
                    other = tuple(sorted(prefix[k+1].get((x+a,y+b),())))
                    if p not in other:
                        implications.add((p,other))
    if n>1:
        index = {p:i for i,p in enumerate(cells)}
        for i,(x,y) in enumerate(cells):
            implications.add((i,tuple(sorted(index[x+a,y+b] for a,b in DIRS
                                             if (x+a,y+b) in index))))
    clauses = {(-(v+1),) for v in zero}
    clauses.update((-(a+1),-(b+1)) for a,b in edges)
    clauses.update((-(p+1),)+tuple(v+1 for v in other)
                   for p,other in implications)
    return cells, zero, edges, implications, tuple(sorted(clauses)), len(incidence)


def negative_units(n, zero, edges, implications):
    """Reachability/conflict discovery; every output unit needs reader audit."""
    zero = set(zero)
    adjacency = [0 for _ in range(n)]
    for a,b in edges:
        adjacency[a] |= 1<<b
        adjacency[b] |= 1<<a
    trace = []
    implications = sorted(implications)
    def add(p):
        if p not in zero:
            zero.add(p)
            trace.append(p+1)
    while True:
        before = set(zero)
        outgoing = [set() for _ in range(n)]
        for p,other in implications:
            if p in zero:
                continue
            live = set(other)-zero
            if not live:
                add(p)
            elif len(live)==1:
                outgoing[p].update(live)
        for p in range(n):
            if p in zero:
                continue
            reach = {p}
            todo = [p]
            while todo:
                v = todo.pop()
                for w in outgoing[v]-reach:
                    reach.add(w)
                    todo.append(w)
            bits = sum(1<<v for v in reach)
            if reach&zero or any(adjacency[v]&bits for v in reach):
                add(p)
        if zero==before:
            return trace


def digest(clauses):
    h = hashlib.sha256()
    for clause in clauses:
        h.update((' '.join(map(str,clause))+' 0\n').encode())
    return h.hexdigest()


def main():
    fixture = json.loads((HERE.parent/'seed.json').read_text())
    cases = []
    for n in range(1,6):
        cells,zero,edges,implications,clauses,global_cells = clauses_for(n,fixture)
        trace = negative_units(len(cells),zero,edges,implications)
        case = {'scale':n,'variables':len(cells),'global_cells':global_cells,
                'packing_units':len(zero),'packing_conflicts':len(edges),
                'implications':len(implications),'clauses':len(clauses),
                'cnf_sha256':digest(clauses),'negative_units':trace}
        cases.append(case)
        print(json.dumps({k:v for k,v in case.items() if k!='negative_units'}),flush=True)
    result = {'format':'negative-unit-rup-v1','agent':'six-heesch-2',
              'role':'researcher','fixture_sha256':hashlib.sha256((HERE.parent/'seed.json').read_bytes()).hexdigest(),
              'cases':cases}
    (HERE/'certificate.json').write_text(json.dumps(result,separators=(',',':'))+'\n')


if __name__=='__main__':
    main()

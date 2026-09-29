"""Four-colour complement of a maximum special support in the first column."""
import argparse
import itertools
from pathlib import Path


def formula():
    positions=list(range(3,55))
    E={(q,c):4*j+c+1 for j,q in enumerate(positions) for c in range(4)}
    clauses=[]
    def onehot(row):
        clauses.append(row)
        clauses.extend([[-x,-y] for x,y in itertools.combinations(row,2)])
    for q in positions:onehot([E[q,c] for c in range(4)])
    bad=set()
    for x in range(1,109):
        for y in range(x,109):
            z=(x+y)%109
            if not z:continue
            values=tuple(min(q,109-q) for q in (x,y,z))
            if any(q in (1,2) for q in values):continue
            for c in range(4):bad.add(tuple(sorted({-E[q,c] for q in values})))
    clauses.extend(map(list,sorted(bad,key=lambda row:(len(row),row))))
    for j,q in enumerate(positions):
        for c in range(1,4):clauses.append([-E[q,c],*[E[old,c-1] for old in positions[:j]]])
    free=list(range(1,108,2))+[108]
    V={(q,c):208+4*j+c+1 for j,q in enumerate(free) for c in range(4)}
    for q in free:onehot([V[q,c] for c in range(4)])
    for x,y in itertools.combinations(free,2):
        d=min(y-x,109-y+x)
        if d in (1,2):continue
        for c in range(4):clauses.append([-V[x,c],-V[y,c],-E[d,c]])
    return 428,clauses


def dimacs():
    n,clauses=formula()
    return (f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in clauses)).encode()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output',type=Path)
    args=parser.parse_args();args.output.write_bytes(dimacs())

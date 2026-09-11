"""Emit one of the four globally exhaustive coordinate-profile CNFs.

Requires python-sat. No timeout or partial solver run is an exclusion.
Point variable 25*x+5*y+z+1 means that (x,y,z) belongs to S.
"""
import argparse
from itertools import product
from pathlib import Path
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool

p=argparse.ArgumentParser()
p.add_argument('--case',type=int,choices=range(4),required=True)
p.add_argument('--out',type=Path,required=True)
p.add_argument('--many-full',action='store_true',help='add the proved >=74 full-plane cut')
args=p.parse_args()
points=list(product(range(5),repeat=3)); index={p:i+1 for i,p in enumerate(points)}
directions=[d for d in points if any(d) and next(x for x in d if x)==1]
lines=set()
for d in directions:
    for a in points:
        lines.add(tuple(sorted(index[tuple((x+t*y)%5 for x,y in zip(a,d))]
                               for t in range(5))))
planes=[[i+1 for i,p in enumerate(points) if sum(x*y for x,y in zip(p,d))%5==c]
        for d in directions for c in range(5)]
assert len(lines)==775 and len(planes)==155
cnf=CNF(); pool=IDPool(start_from=126)
for l in sorted(lines): cnf.append([-v for v in l])
def card(kind,lits,bound):
    return getattr(CardEnc,kind)(lits=lits,bound=bound,vpool=pool,
                                encoding=EncType.totalizer).clauses
cnf.extend(card('equals',list(range(1,126)),73))
for h in planes: cnf.extend(card('atmost',h,16))
for axis in range(3):
    low=9 if axis<args.case else 10
    for c,size in enumerate((16,16,16,low,25-low)):
        cnf.extend(card('equals',[i+1 for i,p in enumerate(points) if p[axis]==c],size))
if args.many_full:
    full=[]
    for h in planes:
        indicator=pool.id(); full.append(indicator)
        for clause in card('atleast',h,16): cnf.append([-indicator]+clause)
    cnf.extend(card('atleast',full,74))
args.out.parent.mkdir(parents=True,exist_ok=True)
cnf.to_file(str(args.out))
print(f'case={args.case} variables={cnf.nv} clauses={len(cnf.clauses)} many_full={args.many_full}')

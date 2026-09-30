"""Pinned T214 geometry and exact compact triangular cells.

Agent six-heesch-2, researcher. Prior pair exclusions are imported lemmas.
"""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys

if sys.flags.optimize:
    raise RuntimeError('mathematical assertions require an unoptimized interpreter')

BASE=Path(__file__).resolve().parent
PRIOR=BASE.parent/'heesch_polyiamond_local_deficit'
PINS={'geometry.py':'4293a107c8e3469411d70340122d5a8d4107e8bb2f060a14dff14332d367b736',
      'expected.json':'aa1cc1ec4e4878359592f42f234af862781c47cca89c6d810bd9d0ed21186b21'}
for name,digest in PINS.items():
    assert hashlib.sha256((PRIOR/name).read_bytes()).hexdigest()==digest,name
sys.path.insert(0,str(PRIOR))
import geometry as g

OFFSETS=((0,0,0),(1,-1,0),(0,-1,0),(1,-1,-1),(0,0,-1),(1,0,-1))


def vertices(t):
    k,x,y=t
    assert k in (0,1)
    return tuple(sorted(((x,y),(x+1,y),(x,y+1)) if k==0 else
                        ((x+1,y),(x,y+1),(x+1,y+1))))


def compact(t):
    x=min(v[0] for v in t);y=min(v[1] for v in t)
    for k in (0,1):
        if vertices((k,x,y))==t:return k,x,y
    raise AssertionError(('nonunit triangle',t))


def masks(cells):
    out=defaultdict(int)
    for k,x,y in cells:
        slots=(((x,y),0),((x+1,y),2),((x,y+1),4)) if k==0 else \
              (((x+1,y),1),((x,y+1),5),((x+1,y+1),3))
        for v,j in slots:
            assert not out[v] & (1<<j)
            out[v]|=1<<j
    return out


def star(v):
    x,y=v
    return {(k,x+a,y+b) for k,a,b in OFFSETS}


def footprint(shape,pose):
    return frozenset(compact(g.move(t,pose)) for t in shape)


def adjacent(t):
    k,x,y=t
    return ((1,x,y),(1,x-1,y),(1,x,y-1)) if k==0 else \
           ((0,x,y),(0,x+1,y),(0,x,y+1))


def write(path,value):
    path.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')


def cnf_text(nv,clauses):
    return f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)

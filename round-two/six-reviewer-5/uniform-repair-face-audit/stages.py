"""Reusable checked original cap solves; polynomial energy assembly is separate."""
import json,sys
from pathlib import Path
from parse_exact import rational
import original_field as O
from cap_sectors import gram
P=Path(__file__).resolve().parent

def read(x):
    if isinstance(x,dict):return {a:read(b) for a,b in x.items()}
    if isinstance(x,list):return [read(y) for y in x]
    if isinstance(x,str):
        a,b=rational(x);ring=O.q.numer.ring
        n=ring.from_dict({e:O.FIELD.domain.convert(c) for e,c in a.items()})
        d=ring.from_dict({e:O.FIELD.domain.convert(c) for e,c in b.items()})
        O.require(bool(d),'nonzero recorded denominator')
        return O.q.field.raw_new(n,d)
    if type(x) is int:return O.FIELD.convert(x)
    return x

def load(name):return read(json.loads((P/(name+'.json')).read_text()))

def standard():
    U,D,norm=gram(True)
    S,V=O.short(U,[5],masses=norm)
    E=O.energy(D,V)[0][0]/2
    O.write('standard-stage',dict(U=U,Delta=D,norms=norm,S=S,V=V,nu=S[0][0]/2,Delta_energy=E))
    print('checked original standard stage saved',flush=True)

def trivial():
    U,D,norm=gram(False)
    S,V=O.short(U,[2,4,3,10],masses=norm)
    O.write('trivial-stage',dict(U=U,Delta=D,norms=norm,H4=S,V4=V))
    print('checked original trivial solve7 stage saved',flush=True)

if __name__=='__main__':{'standard':standard,'trivial':trivial}[sys.argv[1]]()

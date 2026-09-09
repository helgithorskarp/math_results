#!/usr/bin/env python3
"""Produce short Q(omega) identities by exact rational linear algebra."""
import argparse
from pathlib import Path
from itertools import combinations,product
from collections import Counter
import importlib.util
import json
import sympy as S
from sympy.polys.matrices import DomainMatrix
import exact as X

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('pencil_producer',HERE.parent/'hadwiger_nelson_radix_five_active_pencil/produce.py')
H=importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)
U,V=S.symbols('U V');s=S.sqrt(-3);om=(1+s)/2;K=S.QQ.algebraic_field(s)
E=lambda d:d[0]+d[1]*om
C=lambda d:(d[0]+d[1],-d[1])


def inventory():
    rows,edges=H.G.inventory()
    circle=H.G.primitive({(2,0):1,(0,2):3,(0,0):-1})
    eventrows={H.G.distance_event(r):r for r in rows if sum(d!=(0,0) for d in r)>1}
    factors=sorted(list(eventrows)+[circle]);byid={i:eventrows[f] for i,f in enumerate(factors) if f!=circle}
    buckets={}
    for c,row in byid.items():buckets.setdefault(H.signature(row),[]).append(c)
    for bucket in buckets.values():bucket.sort()
    patterns=[];quintets=[];trace=[];counts=Counter()
    for i,j in combinations(range(1,5),2):
        ei=tuple(int(k==i-1) for k in range(4));ej=tuple(int(k==j-1) for k in range(4))
        for a,b in product(range(1,4),repeat=2):
            pen=H.pencil((ei,a),(ej,b));patterns.append(pen)
            for lift in product(*(buckets[t] for t in pen)):
                first,second=byid[lift[pen.index((ei,a))]],byid[lift[pen.index((ej,b))]]
                alpha=H.G.emul(first[i],C(first[0]));beta=H.G.emul(second[j],C(second[0]))
                key=tuple(sorted(H.G.canon((byid[c][0],H.G.emul(byid[c][i],C(alpha)),H.G.emul(byid[c][j],C(beta)))) for c in lift))
                q=tuple(sorted(lift));counts[key]+=1;quintets.append(q);trace.append((q,key))
    X.need(len(patterns)==54 and len(quintets)==6912 and len(counts)==32 and set(counts.values())=={216},'source census')
    return factors,sorted(patterns),sorted(quintets),sorted(counts),sorted(trace)


def coeff(x):
 q=K.from_sympy(x).to_list();q=[S.Rational(c) for c in q];q=[S.Rational(0)]*(2-len(q))+q
 return q[1]-q[0],2*q[0]
def terms(p):return {ij:coeff(c) for ij,c in S.Poly(p,U,V,extension=s).terms()}
def solve(gs,target,m):
 mons=[(i,d-i) for d in range(m+1) for i in range(d+1)]
 columns=[]
 for g in gs:
  for mon in mons:
   shifted={(i+mon[0],j+mon[1]):ab for (i,j),ab in terms(g).items()}
   columns.append(shifted)
   columns.append({ij:(-b,a+b) for ij,(a,b) in shifted.items()})
 t=terms(target);support=sorted(set(t).union(*(set(c) for c in columns)))
 mat=[[col.get(ij,(0,0))[part] for col in columns]+[t.get(ij,(0,0))[part]] for ij in support for part in (0,1)]
 reduced,pivots=DomainMatrix.from_Matrix(S.Matrix(mat)).convert_to(S.QQ).rref()
 if len(columns) in pivots:return None
 rr=reduced.to_Matrix();solution=[S.Rational(0)]*len(columns)
 for i,j in enumerate(pivots):solution[j]=rr[i,-1]
 multipliers=[]
 for k in range(len(gs)):
  d={}
  for j,ij in enumerate(mons):
   a,b=solution[2*(k*len(mons)+j):2*(k*len(mons)+j)+2]
   if a or b:d[ij]=(a,b)
  multipliers.append(d)
 def encode(d):
  out=[]
  for (i,j),(a,b) in sorted(d.items()):
   den=S.ilcm(a.q,b.q);out.append([i,j,int(a*den),int(b*den),int(den)])
  return out
 return [encode(d) for d in multipliers]


def produce():
    factors,patterns,quintets,keys,trace=inventory()
    results=[]
    for index,key in enumerate(keys):
        gs=[]
        for r in key:
            a,b,c=map(E,r);ac,bc,cc=map(E,map(C,r))
            q=S.expand((a+b*U+c*V)*(ac*(1+U)*(1+V)-bc*U*(1+V)-cc*V*(1+U))-(1+U)*(1+V))
            if q!=0:gs.append(q)
        D=(1+U)*(1+V)
        targets=[('difference',S.expand(D**2*(U-V))),('norm',S.expand(D**2*(4*V**2+V+1)))] if index==0 else [('contradiction',S.expand(D**2))]
        identities=[]
        for name,target in targets:
            answer=None
            for degree in range(2,7):
                answer=solve(gs,target,degree)
                if answer is not None:break
            X.need(answer is not None,'bounded identity generation succeeds')
            identities.append({'claim':name,'multipliers':answer,'multiplier_degree_bound':degree})
        results.append({'normalized_rows':key,'identities':identities})
    certificate={'schema':'hn-radix-two-coordinate-identities-v1','normal_forms':results}
    # Recheck after JSON conversion, using the portable exact multiplier checker.
    X.check_identities(json.loads(json.dumps(certificate)),keys)
    return certificate,{'curve_inventory_sha256':X.digest(factors),'patterns_sha256':X.digest(patterns),
                        'quintets_sha256':X.digest(quintets),'normal_forms_sha256':X.digest(keys),
                        'normalization_transcript_sha256':X.digest(trace)}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();certificate,summary=produce()
    with args.out.open('x') as f:json.dump(certificate,f,sort_keys=True,separators=(',',':'));f.write('\n')
    print(json.dumps(summary,indent=2,sort_keys=True))

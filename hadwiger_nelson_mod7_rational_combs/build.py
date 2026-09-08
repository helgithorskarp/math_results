#!/usr/bin/env python3
"""Produce the compact mod-7 rational-comb certificate."""
from __future__ import annotations
import argparse,hashlib,json,math,time
from pathlib import Path

P=7
ROOT={1:1,2:3,4:2}
WEIGHT={s:(3*ROOT[s])%P if s in ROOT else 0 for s in range(P)}

def need(ok,msg):
    if not ok:raise ValueError(msg)

def squarefree(n):
    c=1;s=n;p=2
    while p*p<=s:
        while s%(p*p)==0:s//=p*p;c*=p
        p+=1
    return c,s

def colour(D,t):
    r=2*D%P
    j=(t*pow(r,-1,P))%P
    if j in (0,1):return 0
    if j in (2,3):return 1
    if j in (4,5):return 2
    return 3

def generate():
    conic=[]
    for D in range(1,P):
        r=2*D%P
        for s in range(P):
            a=WEIGHT[s]
            for c in range(P):
                for k in range(P):
                    if (k*k+s*c*c-D*D)%P:continue
                    deltas=sorted({(k+a*c)%P,(k-a*c)%P})
                    need(not set(deltas)&{0,r,-r%P},'residue lemma')
                    conic.append([D,s,c,k,deltas])
        for t in range(P):
            for d in range(P):
                if d in (0,r,-r%P):continue
                need(colour(D,t)!=colour(D,(t+d)%P),'quotient colouring')
    rows=[]
    D=24
    for k in range(D):
        c,s=squarefree(D*D-k*k)
        rows.append([k,c,s,WEIGHT[s%P],sorted({(k+c*WEIGHT[s%P])%P,(k-c*WEIGHT[s%P])%P})])
    need(all(not set(x[4])&{0,2*(D%P)%P,-2*(D%P)%P} for x in rows),'D=24 table')
    return {
      'prime':P,
      'quadratic_residue_roots':{str(k):v for k,v in ROOT.items()},
      'weights':[WEIGHT[s] for s in range(P)],
      'colour_pairs_in_r_units':[[0,1],[2,3],[4,5],[6]],
      'residue_conic_rows':conic,
      'distance24_factor_rows':rows,
      'distance24_triangle':[[[0,1],0],[[0,1],24],[[12,3],12]],
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--discover',action='store_true');a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic();data=generate()
    raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
    published=Path(__file__).with_name('certificate.json')
    if not a.discover:need(raw==published.read_bytes(),'published certificate mismatch')
    (out/'certificate.json').write_bytes(raw)
    report={'status':'PASS','certificate_bytes':len(raw),'certificate_sha256':hashlib.sha256(raw).hexdigest(),'residue_conic_rows':len(data['residue_conic_rows']),'distance24_factor_rows':len(data['distance24_factor_rows']),'seconds':time.monotonic()-start,'native_solver_calls':0}
    (out/'build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()

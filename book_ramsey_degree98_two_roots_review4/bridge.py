#!/usr/bin/env python3
"""Independent literal red/blue counting checks of the host-to-matrix bridge.

The 84 synthetic graphs have the target degrees but need not avoid books.
Their signed defects test identities, not existence or nonexistence.
"""
from itertools import combinations
from pathlib import Path
import hashlib
import json

def need(ok,message):
    if not ok:raise ValueError(message)

def inspect(r):
    n=len(r);v=set(range(n))
    need(all(len(row)==n for row in r),'square adjacency')
    need(all(r[i][i]==0 for i in v) and all(r[i][j]==r[j][i] and r[i][j] in (0,1)
             for i in v for j in v),'simple symmetric graph')
    nr=[{j for j in v if r[i][j]} for i in v]
    nb=[v-{i}-nr[i] for i in v]
    d=list(map(len,nr));e=sum(d)//2;f=[[0]*n for _ in v]
    rc=[];bc=[]
    for i,j in combinations(range(n),2):
        cr=len(nr[i]&nr[j]);cb=len(nb[i]&nb[j])
        defect=3-cr if r[i][j] else 6-cb
        f[i][j]=f[j][i]=defect
        (rc if r[i][j] else bc).append(cr if r[i][j] else cb)
        need(cr==d[i]+d[j]-14+(17-d[i]-d[j])*r[i][j]-defect
             if n==22 else True,'literal off-diagonal red-square identity')
    if n==22:
        need(all(sum(f[i])==2*e-294+38*d[i]-d[i]**2-2*sum(d[j] for j in nr[i])
                 for i in v),'literal incident defect identity')
        need(all(sum(f[i])%2==d[i]%2 for i in v),'incident parity identity')
        k=[[2*r[i][j]+(2*d[i]-17)*int(i==j) for j in v] for i in v]
        for i in v:
            for j in v:
                literal=sum(k[i][t]*k[t][j] for t in v)
                expected=(2*d[i]-17)**2+4*d[i] if i==j else 4*(d[i]+d[j]-14)-4*f[i][j]
                need(literal==expected,'literal K-square bridge')
    return e,d,max(rc),max(bc)

def run():
    graphs=0
    for extra in combinations(range(2,11),3):
        steps=(1,)+extra
        r=[[int(i!=j and ((i-j)%22 in steps or (j-i)%22 in steps or (i-j)%22==11))
            for j in range(22)] for i in range(22)]
        r[0][1]=r[1][0]=0
        e,d,red,blue=inspect(r)
        need(e==98 and sorted(d)==[8,8]+[9]*20,'synthetic target histogram')
        graphs+=1
    raw=Path(__file__).with_name('baseline21.rows').read_bytes()
    fixture=[[int(x) for x in row] for row in raw.decode().splitlines()]
    e,d,red,blue=inspect(fixture)
    need(len(fixture)==21 and e==93 and red<=3 and blue<=6,'credited 21-point positive baseline')
    return {'agent':'six-reviewer-4','role':'independent mathematical reviewer',
            'signed_target_histogram_graphs':graphs,'full_K_square_entries':graphs*22**2,
            'off_diagonal_red_square_checks':graphs*231,'incident_and_parity_checks':graphs*22,
            'synthetic_graphs_are_admissible_hosts':False,'baseline_vertices':21,
            'baseline_red_edges':e,'baseline_red_cap':red,'baseline_blue_cap':blue,
            'baseline_sha256':hashlib.sha256(raw).hexdigest(),'all_passed':True}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))

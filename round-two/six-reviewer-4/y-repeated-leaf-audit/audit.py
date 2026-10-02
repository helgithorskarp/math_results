#!/usr/bin/env python3
"""Independent set-neighbor enumeration with degree-sensitive RED intersection caps.

Unlike the native literal BLUE counts, uses c_B=20-d_i-d_j+c_R.
One complete, naturally disjoint T-degree stratum per bounded direct process.
No native/author module imported. All checks are active under python -O.
"""
from pathlib import Path
import argparse, itertools, json, math

def need(b, s):
    if not b: raise RuntimeError(s)

def masks(n):
    return [sum(1<<j for j in c) for c in itertools.combinations(range(6),n)]

def initial():
    r=[set() for _ in range(16)]
    def edge(i,j):r[i].add(j);r[j].add(i)
    for i,j in [(0,1),(0,2),(1,2),(2,9),(2,10),(3,7),(7,6),(6,4),(4,5),(5,8),(8,3),
                (9,6),(9,8),(10,5),(10,7),(9,13),(9,15),(10,13),(10,14)]:edge(i,j)
    for i in range(3,11):edge(0,i)
    for i in range(13,16):edge(2,i)
    return r

def addrow(r,i,mask):
    for j in range(6):
        if mask>>j&1:r[i].add(3+j);r[3+j].add(i)

def passes(r,vertices,d,missing):
    q={i:d[i]-len(r[i]) for i in vertices}
    if any(v<0 or v>missing for v in q.values()):return False
    for i,j in itertools.combinations(vertices,2):
        common=len(r[i]&r[j])+max(0,q[i]+q[j]-missing)
        cap=3 if j in r[i] else d[i]+d[j]-14
        if common>cap:return False
    return True

def stratum(tf):
    need(tf in range(8),'T flag');l=[tf>>j&1 for j in range(3)]
    d=[10]*16;d[2]=9
    for j in range(3):d[13+j]-=l[j]
    verts14=[i for i in range(16) if i not in (11,12)];verts16=list(range(16))
    rs=[masks(3-l[0]),masks(4-l[1]),masks(4-l[2])]
    base=initial();tested={f:0 for f in range(32) if f&7==tf and f.bit_count()<=3};survive=dict(tested)
    triples=screen14=0;interfaces=[]
    for rows in itertools.product(*rs):
        triples+=1;r=[set(s) for s in base]
        for j,mask in enumerate(rows):addrow(r,13+j,mask)
        if not passes(r,verts14,d,8):continue
        screen14+=1
        for ls0,ls1 in itertools.product(range(2),repeat=2):
            flag=tf|(ls0<<3)|(ls1<<4)
            if flag.bit_count()>3:continue
            for s0,s1 in itertools.product(masks(4-ls0),masks(4-ls1)):
                tested[flag]+=1;h=[set(s) for s in r];dd=list(d)
                for si,mask,low in ((11,s0,ls0),(12,s1,ls1)):
                    dd[si]=10-low
                    for j in (1,2,14,15):h[si].add(j);h[j].add(si)
                    addrow(h,si,mask)
                if not passes(h,verts16,dd,6):continue
                survive[flag]+=1
                interfaces.append({'flag':flag,'T_rows':list(rows),'SY_rows':[s0,s1],
                                   'Q_ranks_X':[dd[i]-len(h[i])for i in range(3,9)]})
    return {'complete':True,'T_count':['T',tf,triples,screen14],
            'F_counts':[['F',f,tested[f],survive[f]]for f in sorted(tested)],
            'interfaces':interfaces}

def main():
    p=argparse.ArgumentParser();p.add_argument('--tflag',type=int,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();x=stratum(a.tflag);a.out.write_text(json.dumps(x,sort_keys=True)+'\n')
    print(json.dumps({'complete':True,'tflag':a.tflag,'counts':x['T_count'],'survivors':len(x['interfaces'])}))
if __name__=='__main__':main()

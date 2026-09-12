#!/usr/bin/env python3
"""Complete good(n) class with gamma(G), gamma(complement G) >= 4.
No graph catalog, packing, degree profile, or automorphism assumption.
Primary variables are lexicographically ordered pairs. Auxiliaries certify
common neighbors of every triple, independently in each color.
"""
import argparse, hashlib, itertools, json, math, time
from pathlib import Path

def shape(n):
    p=math.comb(n,2)
    return p+2*math.comb(n,3)*(n-3), 2*math.comb(n,5)+2*math.comb(n,3)*(3*(n-3)+1)+6

def clauses(n):
    ids={e:i+1 for i,e in enumerate(itertools.combinations(range(n),2))}
    def edge(u,v):return ids[tuple(sorted((u,v)))]
    for u,v in itertools.combinations(range(4),2):yield [edge(u,v)]
    for s in itertools.combinations(range(n),5):
        es=[edge(u,v) for u,v in itertools.combinations(s,2)]
        yield es
        yield [-x for x in es]
    top=len(ids)
    for col in [1,-1]:
        for t in itertools.combinations(range(n),3):
            ws=[]
            for v in range(n):
                if v in t:continue
                top+=1;ws.append(top)
                for u in t:yield [-top,col*edge(u,v)]
            yield ws
    assert top==shape(n)[0]

def control_model(n):
    assert n in (29,37)
    residues={u*u%n for u in range(1,n)}
    old=lambda u,v:u!=v and (u-v)%n in residues
    q=next(s for s in itertools.combinations(range(n),4) if all(old(u,v) for u,v in itertools.combinations(s,2)))
    perm=list(q)+[v for v in range(n) if v not in q]
    a=lambda u,v:old(perm[u],perm[v])
    out=[False]+[a(u,v) for u,v in itertools.combinations(range(n),2)]
    for col in [True,False]:
        for t in itertools.combinations(range(n),3):
            for v in range(n):
                if v not in t:out.append(all(a(u,v)==col for u in t))
    return out,perm

def verify_controls():
    out={}
    for n in (29,37):
        model,perm=control_model(n);count=0
        for count,c in enumerate(clauses(n),1):
            assert any(model[abs(x)]==(x>0) for x in c),(n,count,c)
        assert count==shape(n)[1] and len(model)==shape(n)[0]+1
        out[str(n)]={'all_generated_clauses_satisfied':True,'clauses':count,'variables':len(model)-1,'root_relabeling':perm}
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=43);p.add_argument('--output',type=Path);p.add_argument('--controls',action='store_true');a=p.parse_args();start=time.monotonic()
    if a.controls:print(json.dumps(verify_controls(),indent=2));return
    assert 25<=a.n<=46 and a.output
    nv,nc=shape(a.n);h=hashlib.sha256();size=0
    with a.output.open('wb') as f:
        head=f'p cnf {nv} {nc}\n'.encode();f.write(head);h.update(head);size+=len(head)
        for cnum,c in enumerate(clauses(a.n),1):
            row=(' '.join(map(str,c))+' 0\n').encode();f.write(row);h.update(row);size+=len(row)
    assert cnum==nc
    out={'n':a.n,'primary_variables':math.comb(a.n,2),'variables':nv,'clauses':nc,'bytes':size,'sha256':h.hexdigest(),'elapsed_seconds':time.monotonic()-start,'scope':'ALL good(n) graphs with domination number at least four in BOTH colors, relabeled to put a red K4 first','solver_status':'NOT_RUN'}
    a.output.with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()

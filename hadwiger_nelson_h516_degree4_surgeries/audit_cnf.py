"""Exact full-pair geometry and direct-CNF check; no source-generator import."""
from pathlib import Path
from itertools import combinations
import argparse,hashlib,json
P=Path(__file__).resolve().parent
RAD=[1,3,5,15,11,33,55,165]

def need(ok,why):
    if not ok:raise ValueError(why)

def main():
    global P
    ap=argparse.ArgumentParser();ap.add_argument("--work",type=Path,required=True);a=ap.parse_args();P=a.work.resolve()
    raw=(P/'SOURCE.json').read_bytes();s=json.loads(raw);plan=json.loads((P/'CONTRACT.json').read_text())
    need(hashlib.sha256(raw).hexdigest()==plan['source_sha256'],'source identity')
    labels=s['labels'];points=s['coordinates'];need(len(points)==516 and len(set(tuple(x+y) for x,y in points))==516,'distinct geometry')
    edges=[];pairs=0
    for u,v in combinations(range(516),2):
        value=[0]*8;pairs+=1
        for axis in range(2):
            d=[points[u][axis][j]-points[v][axis][j] for j in range(8)]
            value[0]+=sum(a*a*r for a,r in zip(d,RAD))
            for i,j in combinations(range(8),2):value[i^j]+=2*d[i]*d[j]*RAD[i&j]
        if value==[9216]+[0]*7:edges.append((u,v))
    index={v:i for i,v in enumerate(labels)};want=sorted((index[u],index[v]) for u,v in s['edges'])
    need(edges==want and len(edges)==2538,'strict edge census')
    meta=json.loads((P/'SOURCE_CNF_META.json').read_text());tri=meta['triangle'];need(len(tri)==3 and len(set(tri))==3,'triangle shape')
    es=set(edges);need(all(tuple(sorted(x)) in es for x in combinations(tri,2)),'sound actual triangle')
    count=0
    with (P/'source.cnf').open() as f:
        need(next(f).split()==['p','cnf','2064','10671'],'CNF header')
        def clause(xs):
            nonlocal count
            need(list(map(int,next(f).split()))==xs+[0],'clause '+str(count+1));count+=1
        for v in range(516):clause(list(range(4*v+1,4*v+5)))
        for u,v in edges:
            for k in range(4):clause([-4*u-k-1,-4*v-k-1])
        for k,v in enumerate(tri):clause([4*v+k+1])
        need(not f.read(),'no trailing clauses')
    need(count==10671,'clause count')
    result={'verified':True,'vertices':516,'pairs':pairs,'strict_edges':2538,'coordinate_denominator':96,'basis_radicands':RAD,'CNF_clauses_checked':count,'triangle':tri,'CNF_sha256':hashlib.sha256((P/'source.cnf').read_bytes()).hexdigest(),'independent_of_generator':True,'new_solver_calls':0}
    (P/'SOURCE_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()

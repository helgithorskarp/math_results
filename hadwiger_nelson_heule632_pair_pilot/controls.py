#!/usr/bin/env python3
"""Exhaustive Boolean encoder controls and three checked native fixtures."""
import argparse
from itertools import combinations,product
import json
from pathlib import Path
import time
import build
import independent
import native


def main(out,kissat,drat):
    start=time.monotonic();out.mkdir(parents=True,exist_ok=False);possible=list(combinations(range(3),2));tested=0
    for edge_bits in range(8):
        edges=[e for i,e in enumerate(possible) if edge_bits&(1<<i)]
        cls,raw,vs,tri=build.formula(range(3),edges,4)
        alt=independent.formula(range(3),edges,4);build.need(raw==alt[1] and tri==alt[3],'independent small CNF')
        for word in product((False,True),repeat=12):
            sat=all(any(word[abs(x)-1]==(x>0) for x in cl) for cl in cls)
            sets=[{c for c in range(4) if word[4*v+c]} for v in range(3)]
            valid=all(len(s)==1 for s in sets)
            if valid:
                colours=[next(iter(s)) for s in sets]
                valid=all(colours[u]!=colours[v] for u,v in edges) and all(colours[v]==c for c,v in enumerate(tri))
            build.need(sat==valid,'Boolean encoder equivalence');tested+=1
    records=[]
    for i,(n,k,status) in enumerate([(4,4,'SAT'),(5,4,'UNSAT'),(5,5,'SAT')]):
        edges=list(combinations(range(n),2));clauses,raw,vertices,triangle=build.formula(range(n),edges,k)
        build.need(raw==independent.formula(range(n),edges,k)[1],'independent native fixture CNF')
        cnf=out/f'{i}.cnf';proof=out/f'{i}.drat';log=out/f'{i}.log';cnf.write_bytes(raw)
        info=native.solve(kissat,cnf,proof,log);build.need(info['status']==status,'native fixture verdict')
        if status=='SAT':
            answer=build.decode(log.read_text(),vertices,k,clauses);build.check_colouring(answer,vertices,edges,k)
        else:
            checked=native.check_proof(drat,cnf,proof,out/f'{i}.check.log');build.need(checked['verified'],'native fixture DRAT');info['drat']=checked
        records.append(dict(vertices=n,colours=k,**info))
    result={'status':'ALL ENCODING AND NATIVE CONTROLS VERIFIED','boolean_assignments':tested,'native_fixtures':records,'seconds':time.monotonic()-start}
    (out/'controls.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--kissat',type=Path,required=True);ap.add_argument('--drat-trim',type=Path,required=True)
    a=ap.parse_args();main(a.out,a.kissat,a.drat_trim)

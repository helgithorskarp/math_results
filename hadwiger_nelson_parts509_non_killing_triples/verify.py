#!/usr/bin/env python3
"""Certify two missing-witness cases as non-killing, using the committed interface.

No graph construction or a=6 exclusion is claimed. This checks a semantic
obligation in an unfinished certificate; traces and full CNFs stay local.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO/'hadwiger_nelson_parts509_pool_shape_closure'))
import exactgeom


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def formula(D, U, L, edges, witnesses):
    ls=set(L)
    active=[v for v in U if v not in D];pos={v:i for i,v in enumerate(active)};n=len(active)
    z=[2*n+p+1 for p in range(len(witnesses))]
    def unequal(i,c):
        return [-(2*i+b+1) if (c>>b)&1 else 2*i+b+1 for b in range(2)]
    clauses=[z]
    for a,b in edges:
        if a in pos and b in pos:
            for c in range(4):clauses.append(unequal(pos[a],c)+unequal(pos[b],c))
        elif (a in ls and b in pos) or (b in ls and a in pos):
            l,u=(a,b) if a in ls else (b,a)
            for p,w in enumerate(witnesses):clauses.append([-z[p]]+unequal(pos[u],int(w[l])))
    # At least one selector suffices; any true one supplies an L witness.
    return active, 2*n+len(z), clauses


def main():
    if not __debug__:
        raise RuntimeError('Run this verifier without Python optimization flags')
    ap=argparse.ArgumentParser()
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--kissat',default='kissat')
    ap.add_argument('--drat-trim',default='drat-trim')
    args=ap.parse_args()
    out=args.work;out.mkdir(parents=True,exist_ok=True)
    expected=json.loads((HERE/'expected.json').read_text())
    points,_=exactgeom.build(REPO);den,ipts=exactgeom.scale_points(points)
    U=sorted(json.loads((REPO/'hadwiger_nelson_parts509_s_replacement_budget/pool_S.json').read_text())['W_S'])
    L=list(range(374));ls=set(L);us=set(U)
    assert len(set((tuple(points[v][0]),tuple(points[v][1])) for v in L+U))==len(L+U)
    edges=exactgeom.unit_pairs(ipts,den,L+U)
    iface_path=REPO/'hadwiger_nelson_parts509_interface_lemma/interface_L.json'
    iface=json.loads(iface_path.read_text());witnesses=[r['witness_colouring_L'] for r in iface['classes']]
    assert all(all(c[a]!=c[b] for a,b in edges if a in ls and b in ls) for c in witnesses)
    assert sorted({a if a in ls else b for a,b in edges if (a in ls)!=(b in ls)})==iface['interface_L']
    # Positive control: a published full-pool colouring for D={486} must
    # satisfy this encoding. This catches a spurious universal UNSAT formula.
    controls=json.loads((REPO/'hadwiger_nelson_parts509_pool_shape_closure/killing_sets.json').read_text())
    assert controls['U']==U
    control=next(r for r in controls['sets'] if r['D']==[486])
    active,nv,clauses=formula(control['D'],U,L,edges,witnesses)
    colours={v:int(witnesses[control['p']][v]) for v in L}
    colours.update({v:int(c) for v,c in zip(U,control['c']) if c!='.'})
    assert set(colours)==set(L+active)
    assert all(colours[a]!=colours[b] for a,b in edges if a in colours and b in colours)
    positive={2*i+b+1 for i,v in enumerate(active) for b in range(2) if (colours[v]>>b)&1}
    positive.add(2*len(active)+control['p']+1)
    assert all(any((lit>0)==(abs(lit) in positive) for lit in row) for row in clauses)
    print('Published D={486} colouring satisfies the generated formula: VERIFIED',flush=True)
    results=[]
    for D in [[374,375,383],[396,412,479]]:
        active,nv,clauses=formula(D,U,L,edges,witnesses);n=len(active)
        stem='D_'+'_'.join(map(str,D));cnf=out/(stem+'.cnf');proof=out/(stem+'.drat')
        cnf.write_text(f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
        start=time.monotonic()
        with (out/(stem+'.solver.log')).open('w') as f:
            run=subprocess.run(['timeout','-k','5','180',args.kissat,'-q','-f',str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT)
        assert run.returncode==20,run.returncode
        with (out/(stem+'.verify.log')).open('w') as f:
            check=subprocess.run(['timeout','-k','5','180',args.drat_trim,str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT)
        assert check.returncode==0 and 's VERIFIED' in (out/(stem+'.verify.log')).read_text()
        r=dict(D=D,vertices=len(L)+n,unit_edges=sum(a not in D and b not in D for a,b in edges),
               variables=nv,clauses=len(clauses),cnf_sha256=digest(cnf),proof_sha256=digest(proof),
               proof_bytes=proof.stat().st_size,status='DRAT VERIFIED',seconds=time.monotonic()-start,
               interface_sha256=digest(iface_path),
               trust='Exact geometry and checked DRAT; classification completeness inherited from committed 20-class interface lemma.')
        for key,value in expected[len(results)].items():
            assert r[key]==value,(key,r[key],value)
        results.append(r);(out/'result.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n');print(json.dumps(r),flush=True)


if __name__=='__main__':main()

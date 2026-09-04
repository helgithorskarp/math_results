#!/usr/bin/env python3
"""Check colouring covers and refute six-point transversals for two triples.

The colouring witnesses are checked on every exact unit edge. No completeness
claim about the stored interface classes is needed for this positive cover.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
sys.path.insert(0,str(REPO/'hadwiger_nelson_parts509_pool_shape_closure'))
import exactgeom


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()


def at_most(lits,k):
    """Forward prefix counts, with the (k+1)st count forbidden.

    Induction forces s[i,j] when >=j of the first i literals are true.
    Conversely, the actual prefix counts extend every input assignment
    with <=k true literals to a model. Only that equivalence is required.
    """
    assert lits and 0<=k<len(lits)
    nv=max(lits);clauses=[];previous=[]
    for i,x in enumerate(lits,1):
        current=list(range(nv+1,nv+min(i,k+1)+1));nv+=len(current)
        clauses.append([-x,current[0]])
        for j,y in enumerate(previous):
            clauses.append([-y,current[j]])
            if j+1<len(current):clauses.append([-x,-y,current[j+1]])
        previous=current
    clauses.append([-previous[k]])
    return nv,clauses


def check_witnesses(record,U,L,edges,L_witnesses):
    R=record['R'];rs=set(R);us=set(U);ls=set(L)
    assert R==sorted(rs) and rs<=set(range(374,509))
    families=[]
    for w in record['witnesses']:
        p=w['p'];c=w['c']
        assert type(p) is int and 0<=p<len(L_witnesses)
        assert len(c)==len(U) and set(c)<=set('.0123')
        deleted={v for v,a in zip(U,c) if a=='.'}
        assert deleted & set(range(374,509))==rs
        assert deleted<=us
        colours={v:int(L_witnesses[p][v]) for v in L}
        colours.update({v:int(a) for v,a in zip(U,c) if a!='.'})
        assert set(colours)==ls | (us-deleted)
        assert set(colours.values())<=set(range(4))
        assert all(colours[a]!=colours[b] for a,b in edges if a in colours and b in colours)
        E=tuple(sorted(deleted-rs))
        assert E and all(v>=509 for v in E)
        families.append(E)
    assert len(set(families))==len(families)
    return families


def main():
    if not __debug__:raise RuntimeError('Run without Python optimization flags')
    ap=argparse.ArgumentParser()
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--kissat',default='kissat')
    ap.add_argument('--drat-trim',default='drat-trim')
    ap.add_argument('--seconds',type=int,default=300)
    ap.add_argument('--expect',type=Path,default=HERE/'expected.json')
    args=ap.parse_args();assert args.seconds>0
    args.work.mkdir(parents=True,exist_ok=True)
    cert=json.loads((HERE/'colourings.json').read_text())
    assert [r['R'] for r in cert]==[[374,375,383],[396,412,479]]
    points,_=exactgeom.build(REPO);den,ipts=exactgeom.scale_points(points)
    U=sorted(json.loads((REPO/'hadwiger_nelson_parts509_s_replacement_budget/pool_S.json').read_text())['W_S'])
    L=list(range(374));S=[v for v in U if v<509];Q=[v for v in U if v>=509]
    assert S==list(range(374,509)) and len(Q)==168
    assert len({(tuple(points[v][0]),tuple(points[v][1])) for v in L+U})==677
    edges=exactgeom.unit_pairs(ipts,den,L+U)
    assert len(edges)==3400
    interface=REPO/'hadwiger_nelson_parts509_interface_lemma/interface_L.json'
    L_witnesses=[r['witness_colouring_L'] for r in json.loads(interface.read_text())['classes']]
    qid={v:i+1 for i,v in enumerate(Q)}
    nv,card=at_most(list(qid.values()),6)
    expected=json.loads(args.expect.read_text())
    results=[]
    for i,record in enumerate(cert):
        start=time.monotonic()
        family=check_witnesses(record,U,L,edges,L_witnesses)
        clauses=[[qid[v] for v in E] for E in family]+card
        stem='R_'+'_'.join(map(str,record['R']))
        cnf=args.work/(stem+'.cnf');proof=args.work/(stem+'.drat')
        cnf.write_text(f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
        print(f"R={record['R']}: {len(family)} exact colouring witnesses VERIFIED",flush=True)
        with (args.work/(stem+'.solver.log')).open('w') as f:
            solved=subprocess.run([args.kissat,'-q','-f',str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT,timeout=args.seconds)
        assert solved.returncode==20,solved.returncode
        with (args.work/(stem+'.verify.log')).open('w') as f:
            checked=subprocess.run([args.drat_trim,str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT,timeout=args.seconds)
        assert checked.returncode==0 and 's VERIFIED' in (args.work/(stem+'.verify.log')).read_text()
        result=dict(R=record['R'],budget=6,witnesses=len(family),pool_points=677,unit_edges=len(edges),
                    variables=nv,clauses=len(clauses),cnf_sha256=digest(cnf),
                    status='EXACT COLOURINGS AND DRAT VERIFIED')
        assert result==expected[i],(result,expected[i])
        results.append(result)
        (args.work/'result.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
        evidence=dict(result,proof_sha256=digest(proof),proof_bytes=proof.stat().st_size,
                      seconds=time.monotonic()-start,colourings_sha256=digest(HERE/'colourings.json'),
                      interface_sha256=digest(interface))
        (args.work/(stem+'.manifest.json')).write_text(json.dumps(evidence,indent=2,sort_keys=True)+'\n')
        print(json.dumps(evidence,sort_keys=True),flush=True)


if __name__=='__main__':main()

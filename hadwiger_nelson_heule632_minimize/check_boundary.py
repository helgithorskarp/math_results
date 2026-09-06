#!/usr/bin/env python3
"""Check the mandatory-vertex reduction, optionally regenerating its witnesses.

No search.py import: this encoding makes inactive colour variables false.
"""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path
import resource
import sys
from threading import Timer
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'hadwiger_nelson_heule632_pair_pilot'))
import independent as I


def check(out,witness_file):
    start=time.monotonic();out.mkdir(parents=True,exist_ok=False)
    cert=json.loads((HERE/'certificate.json').read_text());boundary=json.loads((HERE/'boundary.json').read_text())
    _,edges,_=I.geometry();vs=cert['retained'];active=set(vs);mandatory=boundary['mandatory_vertices'];optional=boundary['optional_vertices']
    I.check(vs==sorted(active) and len(vs)==560,'fixed final support')
    I.check(mandatory==sorted(set(mandatory)) and optional==sorted(set(optional)) and not set(mandatory)&set(optional) and set(mandatory)|set(optional)==active,'partition')
    I.check(len(mandatory)==492 and len(optional)==68 and comb(68,16)==boundary['exact_size_508_supports'],'exact family domain')
    rows={};queries=0;regen=witness_file is None
    if witness_file is None:
        from pysat.solvers import Glucose4
        limits=json.loads((HERE/'plan.json').read_text())['limits']
        resource.setrlimit(resource.RLIMIT_AS,(limits['address_space_bytes'],)*2)
        number={v:i for i,v in enumerate(vs)};n=len(vs);clauses=[]
        for i in range(n):
            colours=list(range(4*i+1,4*i+5));selector=4*n+i+1
            clauses.append([-selector,*colours]);clauses.extend([[-a,-b] for a,b in combinations(colours,2)])
            clauses.extend([[-a,selector] for a in colours])
        for u,v in edges:
            if u in active and v in active:clauses.extend([[-(4*number[u]+c),-(4*number[v]+c)] for c in range(1,5)])
        for c,v in enumerate(cert['triangle']):clauses.append([-(4*n+number[v]+1),4*number[v]+c+1])
        with Glucose4(bootstrap_with=clauses) as solver:
            for v in mandatory:
                assumptions=[(4*n+i+1)*(-1 if u==v else 1) for i,u in enumerate(vs)]
                solver.clear_interrupt();solver.conf_budget(boundary['regeneration_conflicts_per_query'])
                timer=Timer(boundary['regeneration_interrupt_seconds'],solver.interrupt);timer.daemon=True;timer.start()
                try:answer=solver.solve_limited(assumptions=assumptions,expect_interrupt=True)
                finally:timer.cancel();timer.join();solver.clear_interrupt()
                queries+=1
                if answer is not True:
                    (out/'partial_witnesses.json').write_text(json.dumps(rows,sort_keys=True)+'\n')
                    raise ValueError(f'Witness regeneration incomplete at vertex {v}: {answer}; no negative conclusion')
                truth={abs(x):x>0 for x in solver.get_model()}
                I.check(all(truth[abs(x)]==(x>0) for x in assumptions),'regeneration selectors')
                I.check(all(any(truth[abs(x)]==(x>0) for x in clause) for clause in clauses),'regeneration model clauses')
                text=['.']*632
                for u in active-{v}:
                    cs=[c for c in range(4) if truth[4*number[u]+c+1]];I.check(len(cs)==1,'regeneration one-hot');text[u]=str(cs[0])
                rows[str(v)]={'colouring':''.join(text),'source':'independent-regeneration'}
                I.colouring(rows[str(v)]['colouring'],sorted(set(range(632))-(active-{v})),edges,4)
                if queries%100==0:print('Regenerated',queries,'positive witnesses',flush=True)
        witness_file=out/'witnesses.json';witness_file.write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n')
    else:rows=json.loads(witness_file.read_text())
    I.check(sorted(map(int,rows))==mandatory,'one positive certificate per mandatory vertex')
    edge_checks=0
    for label,row in rows.items():edge_checks+=I.colouring(row['colouring'],sorted(set(range(632))-(active-{int(label)})),edges,4)
    # Check a malformed witness by changing one actual retained edge to equality.
    v=mandatory[0];bad=list(rows[str(v)]['colouring']);u,w=next((u,w) for u,w in edges if u in active-{v} and w in active-{v});bad[w]=bad[u]
    try:I.colouring(''.join(bad),sorted(set(range(632))-(active-{v})),edges,4)
    except ValueError:pass
    else:raise ValueError('improper deletion witness accepted')
    report={'status':'MANDATORY492 OPTIONAL68 FAMILY REDUCTION VERIFIED','positive_rows':len(rows),'edge_checks':edge_checks,'mandatory_vertices':len(mandatory),'optional_vertices':len(optional),'maximum_optional_at_508':16,'size508_supports':comb(68,16),'witnesses_regenerated':regen,'native_queries':queries,'witness_file_bytes':witness_file.stat().st_size,'witness_file_sha256':sha256(witness_file.read_bytes()).hexdigest(),'family_closed':False,'record_improvement':False,'seconds':time.monotonic()-start}
    (out/'verification.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--regenerate',action='store_true');g.add_argument('--witnesses',type=Path)
    a=ap.parse_args();check(a.out,a.witnesses)

#!/usr/bin/env python3
"""Decode the PB rows and check degree semantics without a solver search."""
import argparse
from itertools import product
import json
from pathlib import Path
import re
import subprocess
import tempfile
from engine import HERE,REPO,SELECTION,compute,require


def controls(checker):
    facts,instances,graphs=compute()
    require(facts==json.loads((HERE/'expected.json').read_text()),'exact facts differ')
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    family=[set(row['D']) for row in old['family']]
    minimal=[i for i,D in enumerate(family) if not any(E<D for E in family)]
    decoded_rows=degree_cases=degree_checks=0
    local=[13,14,15,125,126,127,184,185,186]
    for fact in facts:
        q=fact['q'];adj,F,R,degree=graphs[q]
        rows=[]
        for line in instances[q].decode().splitlines()[1:]:
            left,right=line.split(' >= ');rhs=int(right.removesuffix(' ;'))
            tokens=left.split();require(len(tokens)%2==0,'OPB term width')
            terms={}
            for c,v in zip(tokens[::2],tokens[1::2],strict=True):
                require(re.fullmatch(r'x[1-9][0-9]*',v) is not None,'OPB variable')
                label=old['free'][int(v[1:])-1]
                require(label not in terms,'duplicate OPB variable');terms[label]=int(c)
            rows.append((terms,rhs))
        hits=[i for i in minimal if i not in fact['missing_killing']]
        require(len(rows)==len(hits)+5,'OPB row count')
        for row,i in zip(rows[:len(hits)],hits,strict=True):
            terms,rhs=row
            require(set(terms)==family[i] and set(terms.values())=={1} and rhs==1,'killing semantics')
        require(rows[-5]==(dict.fromkeys(old['pool'],1),3),'pool quota semantics')
        require(rows[-4]==(dict.fromkeys(old['free'],-1),-56),'budget semantics')
        # Derive the condition directly from actual fixed and optional neighbours.
        for (terms,rhs),v in zip(rows[-3:],[184,185,186],strict=True):
            require(v in R and rhs==0 and terms[v]==len(adj[v]&F)-4,'conditional coefficient')
            require(set(terms)-{v}==adj[v]&R,'conditional neighbour labels')
            require(all(c==1 for u,c in terms.items() if u!=v),'neighbour coefficients')
        require(all(len(adj[v]&F)>=4 for v in adj if v not in {184,185,186}),'all other degree conditions')
        for assignment in product([False,True],repeat=len(local)):
            chosen={v for v,b in zip(local,assignment,strict=True) if b}
            for remainder in [set(),R-set(local)]:
                S=F|chosen|remainder
                degrees=[len(adj[v]&S) for v in S]
                pb=all(sum(c for v,c in terms.items() if v in S)>=rhs for terms,rhs in rows[-3:])
                require((min(degrees)>=4)==pb,'degree truth table')
                degree_cases+=1;degree_checks+=len(degrees)
        decoded_rows+=len(rows)
    with tempfile.TemporaryDirectory(prefix='hn-four-proof-control-') as directory:
        d=Path(directory)
        (d/'sat.opb').write_text('* #variable= 1 #constraint= 1\n+1 x1 >= 1 ;\n')
        (d/'false.pb').write_text('pseudo-Boolean proof version 2.0\nf 1\noutput NONE\nconclusion UNSAT : 1\nend pseudo-Boolean proof\n')
        r=subprocess.run([str(checker.resolve()),str(d/'sat.opb'),str(d/'false.pb')],capture_output=True,text=True)
        require(r.returncode!=0 and 'VERIFIED UNSATISFIABLE' not in r.stdout,'false proof accepted')
    return dict(status='PB ROW SEMANTICS, DEGREE TRUTH TABLES AND PROOF REJECTION VERIFIED',
                supports=SELECTION,decoded_PB_rows=decoded_rows,local_assignments_per_support=512,
                degree_cases=degree_cases,direct_vertex_degree_checks=degree_checks,
                false_unsat_conclusions_rejected=1)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--veripb',type=Path,required=True);args=ap.parse_args()
    result=controls(args.veripb)
    require(result==json.loads((HERE/'controls_expected.json').read_text()),'controls differ')
    print(json.dumps(result,indent=2,sort_keys=True))

#!/usr/bin/env python3
"""Definition-level degree controls and semantic rejection of false proofs."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import subprocess
import tempfile
from verify import HERE,REPO,geometry_audit,require


def compute(checker):
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    prior=json.loads((REPO/'hadwiger_nelson_parts509_degree6_point613_residual/expected.json').read_text())
    audit,adj,fixed,optional,omitted=geometry_audit(old,prior)
    local={14,15,126,185};cases=checks=0
    for size in range(5):
        for chosen in combinations(sorted(local),size):
            for remainder in [set(),optional-local]:
                S=fixed|set(chosen)|remainder
                degrees=[len(adj[v]&S) for v in sorted(S)]
                require((min(degrees)>=4)==bool(S&{14,126}),'degree equivalence truth table')
                cases+=1;checks+=len(S)
    # This demonstrates local novelty only, not a model of the budgeted residual.
    X=set(old['free'])-omitted-{14,126}
    family=[set(row['D']) for row in old['family']]
    minimal=[i for i,D in enumerate(family) if not any(E<D for E in family)]
    require(all(X&family[i] for i in minimal if i not in [245,316]),'monotone model')
    require(len(X)>56 and len(adj[184]&(set(old['forced'])|{613}|X))==3,'monotone separation scope')
    rejected=0
    with tempfile.TemporaryDirectory(prefix='hn613-proof-controls-') as directory:
        d=Path(directory)
        (d/'sat.opb').write_text('* #variable= 1 #constraint= 1\n+1 x1 >= 1 ;\n')
        (d/'false.pb').write_text('pseudo-Boolean proof version 2.0\nf 1\noutput NONE\nconclusion UNSAT : 1\nend pseudo-Boolean proof\n')
        bad=(HERE/'closure.pb').read_text().replace('conclusion UNSAT : 367','conclusion UNSAT : 341')
        require(bad!=(HERE/'closure.pb').read_text(),'negative-control substitution')
        (d/'wrong-conclusion.pb').write_text(bad)
        for formula,proof in [(d/'sat.opb',d/'false.pb'),(HERE/'residual.opb',d/'wrong-conclusion.pb')]:
            r=subprocess.run([str(Path(checker).resolve()),str(formula),str(proof)],capture_output=True,text=True)
            require(r.returncode!=0 and 'VERIFIED UNSATISFIABLE' not in r.stdout,'invalid proof accepted')
            rejected+=1
    return dict(status='DEGREE AND PROOF-REJECTION CONTROLS VERIFIED',local_assignments=16,
                degree_cases=cases,direct_vertex_degree_checks=checks,
                monotone_counterexample_free_vertices=len(X),monotone_counterexample_meets_budget=False,
                false_unsat_conclusions_rejected=rejected)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--veripb',type=Path,required=True);args=ap.parse_args()
    result=compute(args.veripb);require(result==json.loads((HERE/'controls_expected.json').read_text()),'controls differ')
    print(json.dumps(result,indent=2,sort_keys=True))

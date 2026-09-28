"""Local truth-table and one-colour set-criterion audits of reflected fibres."""
import argparse
import itertools
import json
from pathlib import Path
from search import geometry,triple_clauses


def audit(output):
    a=7;n=35;m=geometry(a);trials=0
    def direct(x,assignment):
        aa,b=x%a,x%5
        if not aa:return assignment[m['index'][0,min(b,5-b)]]
        if not b:return assignment[m['index'][min(aa,a-aa),0]]
        state=assignment[m['index'][aa if b in (1,2) else -aa%a,1]]
        return 1-state if state in (0,1) and b in (2,3) else state
    for x in range(1,n):
        for y in range(x,n):
            z=(x+y)%n
            if not z:continue
            xyz=(x,y,z);cnf=triple_clauses(m,xyz);nodes=sorted({m['point'][t][0] for t in xyz})
            for labels in itertools.product(range(6),repeat=len(nodes)):
                assignment=dict(zip(nodes,labels))
                literal=len({direct(t,assignment) for t in xyz})==1
                encoded=any(all(assignment[(-v-1)//6]==(-v-1)%6 for v in cl) for cl in cnf)
                if literal!=encoded:raise RuntimeError('local projection mismatch')
                trials+=1
    sf=lambda B:all((x+y)%a not in B for x in B for y in B)
    diff=lambda B:{(x-y)%a for x in B for y in B}
    cases=0
    for emask in range(8):
        E={x for u in range(1,4) if emask>>(u-1)&1 for x in (u,a-u)}
        for qmask in range(64):
            C={x for x in range(1,a) if qmask>>(x-1)&1}
            for kind in (0,1,2):
                if kind==2:
                    B=C|{-x%a for x in C}
                    points={(x,0) for x in E}|{(x,b) for x in C for b in (1,2)}|{(-x%a,b) for x in C for b in (3,4)}
                    expected=sf(E) and sf(B) and not E&diff(C)
                else:
                    R=C|{0};b=kind+1
                    points={(x,0) for x in E}|{(x,b) for x in R}|{(-x%a,-b%5) for x in R}
                    expected=sf(E) and not E&diff(R)
                actual=all(((x+u)%a,(b+v)%5) not in points for x,b in points for u,v in points)
                if actual!=expected:raise RuntimeError(('set criterion mismatch',kind,E,C))
                cases+=1
    report=dict(status='REFLECTED_SHARED_AUDIT_OK',axis_factor=a,modulus=n,
                literal_local_assignments=trials,complete_one_colour_cases=cases)
    Path(output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);audit(p.parse_args().output)

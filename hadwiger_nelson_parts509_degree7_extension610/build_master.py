#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
import argparse,itertools,json
from cardinality import Builder

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def propagate(rows,assignment):
    values=dict(assignment)
    while True:
        changed=False
        for row in rows:
            if any(abs(v) in values and values[abs(v)]==(v>0) for v in row):continue
            left=[v for v in row if abs(v) not in values]
            if not left:return False
            if len(left)==1:
                v=left[0];values[abs(v)]=v>0;changed=True
        if not changed:return True


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--metadata',type=Path,required=True);args=ap.parse_args()
    checks=0
    for n in range(8):
        for k in range(n+2):
            for required in (False,True):
                builder=Builder(n);t=builder.threshold(list(range(1,n+1)),k)
                builder.clause(t if required else builder.neg(t))
                for values in itertools.product((False,True),repeat=n):
                    assert propagate(builder.rows,dict(enumerate(values,1)))==((sum(values)>=k)==required)
                    checks+=1
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    R=old['free'];var={v:i+1 for i,v in enumerate(R)}
    builder=Builder(len(R))
    for i,row in enumerate(old['family']):
        if i!=188:builder.clause(*(var[v] for v in row['D']))
    builder.clause(builder.neg(builder.threshold(list(var.values()),57)))
    builder.clause(builder.threshold([var[v] for v in old['pool']],3))
    cnf=builder.dimacs();args.out.write_bytes(cnf)
    facts=dict(free_labels=R,lifted_killing_rows=424,excluded_killing_index=188,
               maximum_old_free_vertices=56,minimum_old_pool_vertices=3,
               variables=builder.variables,clauses=len(builder.rows),sha256=sha256(cnf).hexdigest(),
               exhaustive_counter_assignments=checks)
    args.metadata.write_text(json.dumps(facts,indent=2)+'\n')
    print(json.dumps({k:v for k,v in facts.items() if k!='free_labels'},indent=2))


if __name__=='__main__':main()

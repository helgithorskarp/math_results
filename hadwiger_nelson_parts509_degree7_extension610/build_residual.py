#!/usr/bin/env python3
"""Encode the exact three-deletion/three-addition residual; no solver run."""
from pathlib import Path
from hashlib import sha256
from math import comb
import argparse,json
from cardinality import Builder

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def compute(old):
    deleted_fixed={15,23}
    original_free=[v for v in old['free'] if v<509 and v not in deleted_fixed]
    pool=old['pool']
    assert len(original_free)==56 and len(pool)==76
    deletion={v:i+1 for i,v in enumerate(original_free)}
    addition={v:len(deletion)+i+1 for i,v in enumerate(pool)}
    builder=Builder(len(deletion)+len(addition))
    for i,row in enumerate(old['family']):
        if i==188:continue
        clause=[]
        for v in row['D']:
            if v in deletion:clause.append(-deletion[v])
            elif v in addition:clause.append(addition[v])
            else:assert v in deleted_fixed
        builder.clause(*clause)
    for variables in [list(deletion.values()),list(addition.values())]:
        builder.clause(builder.threshold(variables,3))
        builder.clause(builder.neg(builder.threshold(variables,4)))
    cnf=builder.dimacs()
    meta=dict(deletion_labels=original_free,addition_labels=pool,exact_deletions=3,exact_additions=3,
              fixed_omitted_original_vertices=[15,23],fixed_added_point=610,
              raw_support_pairs=comb(56,3)*comb(76,3),variables=builder.variables,clauses=len(builder.rows),
              sha256=sha256(cnf).hexdigest(),solver_launched=False)
    return cnf,meta


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--metadata',type=Path,required=True);args=ap.parse_args()
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    cnf,meta=compute(old)
    args.out.write_bytes(cnf)
    args.metadata.write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps({k:v for k,v in meta.items() if k not in ('deletion_labels','addition_labels')},indent=2))


if __name__=='__main__':main()

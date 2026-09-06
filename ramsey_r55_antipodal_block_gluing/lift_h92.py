"""Connect a fully assigned 523-bit H92 visible vector to the block oracle.

Checks fixed-family degrees outside the holes, residual bounds and both
densities before gluing. No visible assignment search or SAT call is made.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import glue

SCHEMA_SHA = 'ee1fa61df8ca667e348f3d3acf99136a26f0b96705e19f035dd18f86c05d15f2'


def need(ok,message):
    if not ok:
        raise ValueError(message)


def run(schema_path, values, work_limit):
    need(type(work_limit) is int and work_limit >= 0, 'nonnegative work limit')
    need(hashlib.sha256(schema_path.read_bytes()).hexdigest() == SCHEMA_SHA,'complete audited H92 schema identity')
    schema = json.loads(schema_path.read_text())
    need(type(values) is list and len(values) == 523 and all(type(x) is bool for x in values),'523 actual Boolean visible bits')
    red = {tuple(e[:2]) for e in schema['fixed_pairs'] if e[2]} | {
        tuple(e) for e,x in zip(schema['visible_pairs'],values) if x}
    blocks = [[b['left'],b['right']] for b in schema['blocks']]
    covered = {v for L,R in blocks for v in L+R}
    residual = [target-sum(v in e for e in red) for v,target in enumerate(schema['degree_targets'])]
    for v in sorted(set(range(43))-covered):
        if residual[v] != 0:
            return {'status':'NO_LIFT_OUTSIDE_DEGREE','vertex':v,'residual':residual[v]}
    for L,R in blocks:
        for side,upper in ((L,len(R)),(R,len(L))):
            for v in side:
                if not 0 <= residual[v] <= upper:
                    return {'status':'NO_LIFT_MARGIN_BOUND','vertex':v,'residual':residual[v],'upper':upper}
    for root in (0,1):
        Q = [v for v in range(43) if v != root and tuple(sorted((root,v))) not in red]
        actual = sum(e in red for e in it.combinations(Q,2))
        if actual != 124:
            return {'status':'NO_LIFT_DENSITY','root':root,'actual':actual,'required':124}
    data = {'n':43,'blocks':blocks,'red_visible_edges':[list(e) for e in sorted(red)],
            'row_margins':[[residual[v] for v in L] for L,R in blocks],
            'column_margins':[[residual[v] for v in R] for L,R in blocks]}
    result = glue.decide(data,work_limit)
    result['scope'] = 'one fixed H92 visible assignment, prescribed stars/degrees/densities, all global K5 conditions'
    return result


def main():
    p = argparse.ArgumentParser(); p.add_argument('--schema',required=True,type=Path)
    p.add_argument('--values',required=True,type=Path); p.add_argument('--output',required=True,type=Path)
    p.add_argument('--work-limit',type=int,default=1000000); a = p.parse_args()
    result = run(a.schema,json.loads(a.values.read_text())['visible_bits'],a.work_limit)
    with a.output.open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True); f.write('\n')
    print(json.dumps(result),flush=True)


if __name__ == '__main__':
    main()

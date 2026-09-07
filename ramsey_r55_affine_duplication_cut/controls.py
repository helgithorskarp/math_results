#!/usr/bin/env python3
"""Adverse proof-consumer checks and the complete internal-bit coordinate map."""
import argparse
import itertools
import json
from pathlib import Path
import audit_formula
import model
import runtime
import verify


def rejected(fn):
    try:
        fn()
    except (ValueError, FileNotFoundError):
        return
    raise ValueError('bad evidence was accepted')


def run(args):
    work = runtime.external(args.work)
    dest = runtime.external(args.output)
    dest.mkdir(parents=True,exist_ok=False)
    checker = runtime.check_tool(args.drat_trim,'drat-trim')
    baseline = {'doubled_rows':[1,2,3,4,5],'internal_hex':'0'*111}
    base = int(model.generate(baseline)['red_hex'],16)
    physical = list(itertools.combinations(range(43),2))
    internal = [i for i,(u,v) in enumerate(physical) if not u < 20 <= v]
    for j,i in enumerate(internal):
        changed = model.generate({**baseline,'internal_hex':format(1 << j,'0111x')})
        if int(changed['red_hex'],16) ^ base != 1 << i:
            raise ValueError('internal coordinate transport')
    A=list(range(1,16))+baseline['doubled_rows']
    B=list(range(1,16))+list(range(1,16,2))
    for i,(u,v) in enumerate(physical):
        if u < 20 <= v:
            x,y=A[u],B[v-20]
            dot=sum(((x >> k)&1)*((y >> k)&1) for k in range(4))%2
            if (base >> i)&1 != dot:
                raise ValueError('dense cross coordinate')
    first=work/'runs/o00c0'
    # Fake success metadata for every branch, with absent proof bytes.
    fake=dest/'fabricated'
    for i in range(16):
        for c in (0,1):
            p=fake/'runs'/f'o{i:02d}c{c}'
            p.mkdir(parents=True)
            (p/'result.json').write_text('{"solver_status":"UNSAT","proof_checked":true}\n')
    rejected(lambda:verify.verify_all(fake,checker))
    empty=dest/'empty.drat'
    empty.write_bytes(b'')
    rejected(lambda:runtime.proof_check(checker,first/'input.cnf',empty,dest/'empty.log'))
    truncated=dest/'truncated.drat'
    data=(first/'proof.drat').read_bytes()
    truncated.write_bytes(data[:len(data)//2])
    old=dest/'truncated.log'
    old.write_text('s VERIFIED\n')
    rejected(lambda:runtime.proof_check(checker,first/'input.cnf',truncated,old))
    # A well-formed file with one physical constraint omitted must fail coverage.
    lines=(first/'input.cnf').read_text().splitlines()
    header=lines[0].split()
    header[-1]=str(int(header[-1])-1)
    wrong=dest/'omitted.cnf'
    wrong.write_text(' '.join(header)+'\n'+'\n'.join(lines[2:])+'\n')
    rejected(lambda:audit_formula.audit(wrong,[1,2,3,4,5],0))
    # Corrupt an auxiliary gate while keeping the DIMACS count consistent.
    k=next(i for i,l in enumerate(lines[1:],1) if any(abs(int(x))>253 for x in l.split()[:-1]))
    wrong2=dest/'missing_gate_clause.cnf'
    wrong2.write_text(' '.join(header)+'\n'+'\n'.join(lines[1:k]+lines[k+1:])+'\n')
    rejected(lambda:audit_formula.audit(wrong2,[1,2,3,4,5],0))
    return {'status':'ADVERSE_CONSUMER_CONTROLS_PASSED','internal_coordinates_checked':len(internal),
            'cross_coordinates_checked':460,'fabricated_complete_status_family_rejected':True,
            'empty_proof_rejected':True,'truncated_proof_and_stale_success_log_rejected':True,
            'omitted_physical_clause_rejected':True,'missing_auxiliary_gate_clause_rejected':True}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('work')
    p.add_argument('output')
    p.add_argument('--drat-trim',required=True)
    print(json.dumps(run(p.parse_args()),sort_keys=True))

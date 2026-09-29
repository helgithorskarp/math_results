"""Certify an exact one-step support-exchange obstruction for one given word.

Every old colour other than6 may stay or become6.  Old6 points may receive
any colour.  The old hole must be filled.  At most one new hole is allowed,
and --exclude-hole prohibits it at a specified point.  UNSAT proves only
this explicitly listed neighbourhood of the supplied word is empty.
"""
import argparse
from itertools import combinations
import hashlib
import json
from pathlib import Path
import time
from pysat.solvers import Solver


def encode(word,exclude_hole):
    assert word.count(0)==1
    n=len(word);domains={};var={};top=0
    for x,c in enumerate(word,1):
        domains[x]=(list(range(1,7)) if c==0 else
                    list(range(7)) if c==6 else [0,c,6])
        for d in domains[x]:top+=1;var[x,d]=top
    clauses=[]
    for x,ds in domains.items():
        choices=[var[x,d] for d in ds]
        clauses.append(choices)
        clauses.extend([-a,-b] for a,b in combinations(choices,2))
    schur=0
    for z in range(2,n+1):
        for a in range(1,z//2+1):
            row=sorted(set((a,z-a,z)))
            for c in range(1,7):
                if all(c in domains[x] for x in row):
                    clauses.append([-var[x,c] for x in row]);schur+=1
    holes=[var[x,0] for x in domains if (x,0) in var]
    clauses.extend([-a,-b] for a,b in combinations(holes,2))
    if (exclude_hole,0) in var:clauses.append([-var[exclude_hole,0]])
    else:assert word[exclude_hole-1]==0
    return clauses,domains,var,top,schur


def independent_formula_check(word,excluded,clauses,domains,var):
    # Derive variable availability directly from the allowed point operation.
    for x in range(1,len(word)+1):
        allowed=[]
        for c in range(7):
            if (c==0 and word[x-1]!=0) or (c!=0 and
               (word[x-1] in [0,6] or c in [word[x-1],6])):allowed.append(c)
        assert set(allowed)==set(domains[x])
    expected=[]
    for x in range(1,len(word)+1):
        expected.append(tuple(sorted(var[x,c] for c in domains[x])))
        for a in domains[x]:
            for b in domains[x]:
                if a<b:expected.append(tuple(sorted([-var[x,a],-var[x,b]])))
    for a in range(1,len(word)+1):
        for b in range(a,len(word)-a+1):
            for c in range(1,7):
                if all((v,c) in var for v in [a,b,a+b]):
                    expected.append(tuple(sorted({-var[a,c],-var[b,c],-var[a+b,c]})))
    for a in range(1,len(word)+1):
        for b in range(a+1,len(word)+1):
            if (a,0) in var and (b,0) in var:
                expected.append(tuple(sorted([-var[a,0],-var[b,0]])))
    if (excluded,0) in var:expected.append((-var[excluded,0],))
    assert sorted(expected)==sorted(tuple(sorted(c)) for c in clauses)


def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True)
    p.add_argument('--exclude-hole',type=int,required=True);p.add_argument('--out',required=True)
    p.add_argument('--budget',type=int,default=300000)
    args=p.parse_args();word=list(map(int,Path(args.input).read_text().strip()))
    clauses,domains,var,top,rows=encode(word,args.exclude_hole)
    independent_formula_check(word,args.exclude_hole,clauses,domains,var)
    cnf=Path(args.out+'.cnf');proof=Path(args.out+'.drat')
    cnf.write_text(f'p cnf {top} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
    record={'settings':vars(args),'input_word':''.join(map(str,word)),
            'variables':top,'clauses':len(clauses),'schur_clauses':rows,
            'cnf_sha256':hashlib.sha256(cnf.read_bytes()).hexdigest(),
            'independent_clause_audit':True,'independently_proof_checked':False}
    start=time.monotonic()
    with Solver(name='g3',bootstrap_with=clauses,with_proof=True) as s:
        s.conf_budget(args.budget);answer=s.solve_limited()
        record.update(status={True:'SAT',False:'UNSAT',None:'UNKNOWN'}[answer],
                      solver_stats=s.accum_stats(),seconds=time.monotonic()-start)
        if answer is False:
            proof.write_text('\n'.join(s.get_proof())+'\n')
            record.update(proof_bytes=proof.stat().st_size,
                          proof_sha256=hashlib.sha256(proof.read_bytes()).hexdigest())
        elif answer:
            m=set(s.get_model());candidate=[]
            for x,ds in domains.items():
                cs=[c for c in ds if var[x,c] in m];assert len(cs)==1;candidate.append(cs[0])
            assert candidate.count(0)<=1 and candidate[args.exclude_hole-1]!=0
            assert all(not candidate[x-1] or candidate[x-1]!=candidate[y-1] or
                       candidate[x-1]!=candidate[x+y-1]
                       for x in range(1,len(word)+1) for y in range(x,len(word)-x+1))
            record['candidate_word']=''.join(map(str,candidate))
    Path(args.out+'.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ['input_word','candidate_word']}))


if __name__=='__main__':main()

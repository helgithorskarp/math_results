"""Exhaustive small-oriented-graph check of the Hall CNF against matching."""
import hashlib
import itertools
import json
from pathlib import Path
import time
from pysat.solvers import Solver
from generate_cnf import build

def need(ok,message):
    if not ok:raise ValueError(message)

def matching(rows,root):
    left=rows[root]
    reach=0
    for u in range(len(rows)):
        if left>>u&1:reach|=rows[u]
    right=reach & ~(left|1<<root)
    states={0}
    for u in range(len(rows)):
        if not(left>>u&1):continue
        next_states=set(states)
        choices=rows[u]&right
        for occupied in states:
            for v in range(len(rows)):
                if (choices>>v&1) and not(occupied>>v&1):next_states.add(occupied|1<<v)
        states=next_states
    return max(s.bit_count() for s in states)

def target(rows,root,source):
    reach=0
    for u in range(len(rows)):
        if source>>u&1:reach|=rows[u]
    return reach & ~(rows[root]|1<<root)


def check_degrees():
    # Exercise the actual production degree/flag clauses, before Hall
    # conditions are added, on every possible outgoing row of order 15.
    cnf,pool=build(15,audit_degrees=True)
    checks=0
    with Solver(name='cadical195',bootstrap_with=cnf.clauses) as solver:
        for mask in range(1<<14):
            degree=mask.bit_count()
            fixed=[pool.id(('e',0,j))*(1 if mask>>(j-1)&1 else -1)
                   for j in range(1,15)]
            for h7,h8 in itertools.product((False,True),repeat=2):
                expected=6<=degree<=8 and h7==(degree>=7) and h8==(degree>=8)
                assumption=fixed+[pool.id(('h7',0))*(1 if h7 else -1),
                                  pool.id(('h8',0))*(1 if h8 else -1)]
                need(solver.solve(assumptions=assumption)==expected,
                     f'degree flag disagreement: {mask}, {h7}, {h8}')
                checks+=1
    return checks

def main():
    start=time.monotonic();graphs=0;witnesses=0;nonmatching=0;minimal=0
    digest=hashlib.sha256()
    for n in range(2,6):
        cnf,pool=build(n,audit_root=0)
        pairs=list(itertools.combinations(range(n),2))
        with Solver(name='cadical195',bootstrap_with=cnf.clauses) as solver:
            for code in range(3**len(pairs)):
                rows=[0]*n;value=code
                for i,j in pairs:
                    value,t=divmod(value,3)
                    if t==1:rows[i]|=1<<j
                    if t==2:rows[j]|=1<<i
                assumps=[pool.id(('e',i,j))*(1 if rows[i]>>j&1 else -1)
                         for i in range(n) for j in range(n) if i!=j]
                sat=solver.solve(assumptions=assumps)
                rank=matching(rows,0);expected=rank<rows[0].bit_count()
                need(sat==expected,f'Hall CNF/matching disagreement n={n} code={code}')
                deficient=[]
                sub=rows[0]
                while sub:
                    reach=target(rows,0,sub)
                    if sub.bit_count()>reach.bit_count():deficient.append(sub)
                    sub=(sub-1)&rows[0]
                need(bool(deficient)==expected,'direct Hall disagreement')
                for sub in deficient:
                    if any(other!=sub and other&sub==other for other in deficient):continue
                    reach=target(rows,0,sub)
                    need(reach.bit_count()==sub.bit_count()-1,'minimal Hall size')
                    for v in range(n):
                        if reach>>v&1:need(sum(bool(sub>>u&1 and rows[u]>>v&1) for u in range(n))>=2,'unique preimage')
                    minimal+=1
                if sat:
                    assignment=set(solver.get_model())
                    source=sum(1<<u for u in range(1,n) if pool.id(('left',0,u)) in assignment)
                    actual=target(rows,0,source)
                    heads=sum(1<<u for u in range(1,n) if pool.id(('right',0,u)) in assignment)
                    need(source in deficient and actual==heads,'decoded witness')
                    witnesses+=1
                graphs+=1;nonmatching+=expected
                digest.update(bytes([n,rank,rows[0].bit_count(),int(sat)]))
        print(json.dumps({'completed_order':n,'graphs':graphs}),flush=True)
    degree_checks=check_degrees()
    result={'graphs':graphs,'decoded_witnesses':witnesses,'nonstrong_roots':nonmatching,
            'minimal_Hall_witnesses':minimal,'entry_digest':digest.hexdigest(),
            'degree_flag_checks':degree_checks,
            'elapsed_seconds':time.monotonic()-start,'status':'HALL ENCODING AGREES WITH DEFINITION-LEVEL MATCHING'}
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()

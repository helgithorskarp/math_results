#!/usr/bin/env python3
"""Regenerate and independently check the fixed aggregate profile exclusion.

Requires python-sat==1.8.dev24 and an external DRAT-trim executable.
Generated CNF/proofs must be written outside this repository.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import subprocess
import time
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver
from verify import graph, require, check_girth_and_identities, hoffman_singleton_edges, verify_boundary_profile

HERE=Path(__file__).resolve().parent


def encode(spec, classes, sinks):
    types=spec['types'];aggregate=spec['edges_between_types']
    require(all(t['degree']==sum(t['neighbors']) for t in types),'invalid type degree')
    vt=[i for i,t in enumerate(types) for _ in range(t['count'])]
    d=[types[i]['degree'] for i in vt];n=len(d)
    pool=IDPool();cnf=CNF()
    allowed={(i,j) for i,j,e in aggregate if e}
    E={(u,v):pool.id(('edge',u,v)) for u,v in combinations(range(n),2)
       if tuple(sorted((vt[u],vt[v]))) in allowed}
    def edge(u,v):return E.get(tuple(sorted((u,v))))
    def exact(lits,k):
        if k<0 or k>len(lits):cnf.append([])
        elif lits:cnf.extend(CardEnc.equals(lits,bound=k,vpool=pool,encoding=EncType.seqcounter).clauses)
    for u in range(n):exact([edge(u,v) for v in range(n) if v!=u and edge(u,v)],d[u])
    for u in range(n):
        for j,degree in enumerate(classes):
            exact([edge(u,v) for v in range(n) if v!=u and d[v]==degree and edge(u,v)],types[vt[u]]['neighbors'][j])
    for i,j,total in aggregate:
        exact([e for (u,v),e in E.items() if tuple(sorted((vt[u],vt[v])))==(i,j)],total)
    for u,v in combinations(range(n),2):
        short=[]
        if edge(u,v):short.append(edge(u,v))
        for k in range(n):
            if k in (u,v):continue
            a,b=edge(u,k),edge(v,k)
            if not a or not b:continue
            p=pool.id(('path',u,v,k));short.append(p)
            cnf.extend([[-p,a],[-p,b],[-a,-b,p]])
        if len(short)>1:cnf.extend(CardEnc.atmost(short,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
        if u in sinks or v in sinks:cnf.append(short)
    return cnf,E,n


def graph_spec(G):
    d=list(map(len,G));classes=sorted(set(d))
    signatures=[(d[v],tuple(sum(d[u]==k for u in G[v]) for k in classes)) for v in range(len(G))]
    sigs=sorted(set(signatures));old=sorted(range(len(G)),key=lambda v:(signatures[v],v))
    index={v:i for i,v in enumerate(old)};ti={s:i for i,s in enumerate(sigs)}
    counts=Counter(signatures)
    types=[{'degree':s[0],'neighbors':list(s[1]),'count':counts[s]} for s in sigs]
    aggregate=Counter(tuple(sorted((ti[signatures[u]],ti[signatures[v]])))
                      for u in range(len(G)) for v in G[u] if u<v)
    edges=sorted(tuple(sorted((index[u],index[v]))) for u in range(len(G)) for v in G[u] if u<v)
    sinks=[index[v] for v in range(len(G)) if 1+sum(d[u] for u in G[v])==len(G)]
    return {'types':types,'edges_between_types':[[i,j,e] for (i,j),e in sorted(aggregate.items())]},classes,sinks,edges


def controls():
    fixture=json.loads((HERE/'lower_bound_54_185.json').read_text())
    cases=[('Hoffman-Singleton',graph(50,hoffman_singleton_edges())),
           ('existing-54-185',graph(fixture['n'],fixture['edges']))]
    result=[]
    for name,G in cases:
        check_girth_and_identities(G)
        spec,classes,sinks,edges=graph_spec(G);cnf,E,n=encode(spec,classes,sinks)
        edge_set=set(edges)
        require(all(e in E for e in edge_set),'control edge omitted')
        for uv,e in E.items():cnf.append([e if uv in edge_set else -e])
        with Solver(name='g4',bootstrap_with=cnf) as solver:
            require(solver.solve(),'positive profile control rejected')
            model=set(x for x in solver.get_model() if x>0)
            decoded=[uv for uv,e in E.items() if e in model]
            require(set(decoded)==edge_set,'control decoder mismatch')
            require(check_girth_and_identities(graph(n,decoded))==len(edges),'control graph mismatch')
        result.append({'name':name,'n':n,'edges':len(edges),'status':'SAT and decoded'})
    for name,G in [('triangle',graph(3,[(0,1),(1,2),(0,2)])),
                   ('quadrilateral',graph(4,[(0,1),(1,2),(2,3),(0,3)]))]:
        spec,classes,sinks,edges=graph_spec(G);cnf,E,n=encode(spec,classes,[])
        with Solver(name='g4',bootstrap_with=cnf) as solver:
            require(solver.solve() is False,'forbidden-cycle profile accepted')
        result.append({'name':name,'status':'UNSAT'})
    return result


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--checker',type=Path,required=True)
    ap.add_argument('--conflicts',type=int,default=300000);args=ap.parse_args()
    work=args.work.resolve();checker=args.checker.resolve()
    require(not work.is_relative_to(HERE.parents[1]),'work directory must be outside repository')
    require(checker.is_file(),'DRAT-trim executable missing')
    work.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();verify_boundary_profile();control_results=controls()
    print('PASS: complete profile encoding on positive and negative controls',flush=True)
    spec=json.loads((HERE/'boundary_profile.json').read_text())
    vt=[t['degree'] for t in spec['types'] for _ in range(t['count'])]
    cnf,E,n=encode(spec,[6,7,8],[v for v,d in enumerate(vt) if d==8])
    cnf_path=work/'profile.cnf';proof_path=work/'profile.drup';cnf.to_file(str(cnf_path))
    with Solver(name='g4',bootstrap_with=cnf,with_proof=True) as solver:
        solver.conf_budget(args.conflicts);t=time.monotonic()
        answer=solver.solve_limited(expect_interrupt=True)
        record={'status':'UNSAT' if answer is False else ('SAT' if answer else 'UNKNOWN'),
                'variables':cnf.nv,'clauses':len(cnf.clauses),'edge_variables':len(E),
                'solver_seconds':time.monotonic()-t,'statistics':solver.accum_stats()}
        if answer is not False:
            (work/'result.json').write_text(json.dumps(record,indent=2)+'\n')
            raise RuntimeError('No fixed-profile exclusion established; inspect result.json')
        proof=solver.get_proof();proof_path.write_text('\n'.join(proof)+'\n')
    t=time.monotonic()
    checked=subprocess.run([str(checker),str(cnf_path),str(proof_path),'-t','120'],capture_output=True,text=True)
    (work/'drat_check.txt').write_text(checked.stdout+checked.stderr)
    require(checked.returncode==0 and 's VERIFIED' in checked.stdout,'proof verification failed')
    record.update(checker_status='VERIFIED',checker_seconds=time.monotonic()-t,
                  cnf_sha256=digest(cnf_path),proof_sha256=digest(proof_path),
                  cnf_bytes=cnf_path.stat().st_size,proof_bytes=proof_path.stat().st_size,
                  controls=control_results,total_seconds=time.monotonic()-start,
                  peak_rss_kb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (work/'result.json').write_text(json.dumps(record,indent=2)+'\n')
    print('PASS: fixed aggregate profile UNSAT; DRAT-trim VERIFIED')
    print(json.dumps(record,sort_keys=True))


if __name__=='__main__':main()

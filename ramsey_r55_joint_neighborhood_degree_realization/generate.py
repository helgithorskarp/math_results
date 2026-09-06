"""Joint two-neighborhood selection with a complete target-degree graph.

Not the complete Ramsey43 formula: only the two marked BLUE neighborhoods
are constrained to avoid red K5/blue K4. H is a fixed checked input.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

PARENT=Path(__file__).resolve().parent
sys.path.insert(0,str(PARENT))
from encoding import CounterEncoder

H_HASH={92:'926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466',
        93:'2e33d5c585ef3af1beff09dfd76cfc7484f8ea1ea1dfadcc957923ec033cda74'}
SOLVER_HASH='2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45'

def need(ok,message):
    if not ok:raise ValueError(message)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def dump(path,data):
    with path.open('x') as f:json.dump(data,f,sort_keys=True,indent=2);f.write('\n')

def build(density):
    path=PARENT/f'H{density}.json';need(sha(path)==H_HASH[density],'H identity')
    h={tuple(e) for e in json.loads(path.read_text())['red_edges']}
    fixed={e:e in h for e in it.combinations(range(20),2)}
    def put(u,v,c):
        e=tuple(sorted((u,v)))
        need(e not in fixed or fixed[e]==c,'fixed conflict');fixed[e]=c
    for v in range(43):
        if v!=38:put(v,38,v<20)
    for v in range(20,29):put(0,v,False);put(1,v,True)
    for v in range(29,38):put(0,v,True);put(1,v,False)
    for v in range(39,43):put(0,v,True);put(1,v,True)
    edges=[e for e in it.combinations(range(43),2) if e not in fixed]
    index={e:i+1 for i,e in enumerate(edges)}
    need((len(fixed),len(edges))==(276,627),'pair partition')
    Q=[];clauses=set();clique_counts=[]
    for a in (0,1):
        core=[v for v in range(20) if v!=a and tuple(sorted((a,v))) not in h]
        q=core+list(range(20+9*a,29+9*a));need(len(q)==22,'Q order');Q.append(q)
        counts={}
        for color,k in ((True,5),(False,4)):
            count=0
            for s in it.combinations(sorted(q),k):
                es=list(it.combinations(s,2))
                if any(e in fixed and fixed[e]!=color for e in es):continue
                clauses.add(tuple(sorted((-1 if color else 1)*index[e] for e in es if e in index)))
                count+=1
            counts['red_K5' if color else 'blue_K4']=count
        clique_counts.append(counts)
    enc=CounterEncoder(len(edges),sorted(clauses,key=lambda x:(len(x),x)))
    base=len(enc.clauses)
    for q in Q:
        pairs=list(it.combinations(sorted(q),2))
        total=124-sum(fixed[e] for e in pairs if e in fixed)
        enc.interval([index[e] for e in pairs if e in index],total,total)
    degrees=[]
    for v in range(43):
        target=20 if v in (0,1,38) else 21
        f=sum(c for e,c in fixed.items() if v in e)
        variables=[index[e] for e in edges if v in e]
        enc.interval(variables,target-f,target-f)
        degrees.append(dict(vertex=v,target=target,fixed_red=f,free_incident=len(variables),free_red=target-f))
    meta=dict(H_density=density,H_sha256=sha(path),primary_variables=len(edges),
              fixed_pairs=len(fixed),fixed_red=sum(fixed.values()),Q_global_labels=Q,
              local_clique_counts=clique_counts,base_clauses=base,degree_rows=degrees,
              ordering='none',scope='fixed H; two exact local Q graphs; full43 target degrees; not full Ramsey43')
    return fixed,edges,enc,meta

def parse_status(code,output):
    statuses=[line for line in output.splitlines() if line.startswith('s ')]
    need(code in (0,10,20),'solver process exit')
    expect={0:'s UNKNOWN',10:'s SATISFIABLE',20:'s UNSATISFIABLE'}[code]
    need(statuses==[expect],'solver status mismatch')
    return {0:'UNKNOWN',10:'SAT',20:'UNSAT_UNCHECKED'}[code]

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--kissat',type=Path,required=True);p.add_argument('--seconds',type=int,default=90)
    p.add_argument('--emit-only',action='store_true')
    p.add_argument('--density',type=int,nargs='+',choices=(92,93),default=[92,93]);a=p.parse_args()
    need(a.seconds>0,'cap');a.work.mkdir(exist_ok=False)
    need(sha(PARENT/'encoding.py')=='902f06f7bd3ec062aaa717743bd972ab0f3fcaaff43d3ade2197b4252820dbcd','encoder identity')
    need(sha(a.kissat)==SOLVER_HASH,'solver identity')
    for d in a.density:
        start=time.monotonic();work=a.work/str(d);work.mkdir()
        fixed,edges,enc,report=build(d);cnf=work/'case.cnf'
        with cnf.open('x') as f:
            f.write(f'p cnf {enc.variables} {len(enc.clauses)}\n')
            for row in enc.clauses:f.write(' '.join(map(str,row))+' 0\n')
        report.update(status='EMITTED',variables=enc.variables,clauses=len(enc.clauses),
                      formula_bytes=cnf.stat().st_size,formula_sha256=sha(cnf),
                      source_sha256=sha(Path(__file__)),build_seconds=time.monotonic()-start,
                      solver_cap_seconds=a.seconds)
        dump(work/'interface.json',report)
        print(json.dumps({k:report[k] for k in ('H_density','status','variables','clauses','formula_sha256')}),flush=True)
        if a.emit_only:continue
        t=time.monotonic();log=work/'solver.log';trace=work/'trace.drat'
        with log.open('x') as f:
            try:code=subprocess.run([str(a.kissat),f'--time={a.seconds}',str(cnf),str(trace)],stdout=f,stderr=subprocess.STDOUT,timeout=a.seconds+30).returncode
            except subprocess.TimeoutExpired:code=None
        output=log.read_text();status=parse_status(code,output)
        report.update(status=status,solver_exit=code,solver_seconds=time.monotonic()-t,
                      solver_sha256=sha(a.kissat),max_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        if code==10:
            values={}
            for line in output.splitlines():
                if line.startswith('v '):
                    for token in line.split()[1:]:
                        lit=int(token)
                        if lit:
                            need(abs(lit) not in values or values[abs(lit)]==(lit>0),'model consistency')
                            values[abs(lit)]=lit>0
            need(set(values)==set(range(1,enc.variables+1)),'complete model')
            need(all(any(values[abs(l)]==(l>0) for l in row) for row in enc.clauses),'all model clauses')
            red={e for e,c in fixed.items() if c}|{e for i,e in enumerate(edges,1) if values[i]}
            graph=work/'graph.json';dump(graph,dict(n=43,red_edges=sorted(red)))
            report.update(status='SAT_MODEL_CHECKED_GRAPH_PENDING_AUDIT',graph_sha256=sha(graph))
        report.update(total_seconds=time.monotonic()-start,trace_bytes=trace.stat().st_size,
                      trace_sha256=sha(trace),log_sha256=sha(log),trace_is_checked_refutation=False)
        dump(work/'result.json',report)
        print(json.dumps({k:report[k] for k in ('H_density','status','solver_seconds','total_seconds')}),flush=True)

if __name__=='__main__':main()

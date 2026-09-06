"""Four necessary overlapping blue-neighborhood completions, not full lifts."""
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
HASHES={92:'926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466',
        93:'2e33d5c585ef3af1beff09dfd76cfc7484f8ea1ea1dfadcc957923ec033cda74'}


def need(ok,text):
    if not ok:raise ValueError(text)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(density,anchor):
    need(density in HASHES and anchor in (0,1),'case domain')
    path=PARENT/f'H{density}.json';need(sha(path)==HASHES[density],'H identity')
    H=json.loads(path.read_text());red={tuple(e) for e in H['red_edges']}
    core=[v for v in range(20) if v!=anchor and tuple(sorted((v,anchor))) not in red]
    need(len(core)==13,'blue H neighborhood size')
    other=core.index(1-anchor)
    fixed={(u,v):tuple(sorted((core[u],core[v]))) in red for u,v in it.combinations(range(13),2)}
    for v in range(13,22):fixed[other,v]=True
    edges=[e for e in it.combinations(range(22),2) if e not in fixed]
    index={e:i+1 for i,e in enumerate(edges)}
    need((len(fixed),len(edges))==(87,144),'pair domain')
    clauses=set();census={}
    for color,size in ((True,5),(False,4)):
        count=0
        for subset in it.combinations(range(22),size):
            pairs=list(it.combinations(subset,2))
            if any(fixed[e]!=color for e in pairs if e in fixed):continue
            clauses.add(tuple(sorted((-1 if color else 1)*index[e] for e in pairs if e in index)))
            count+=1
        census['red_K5' if color else 'blue_K4']=count
    enc=CounterEncoder(len(edges),sorted(clauses,key=lambda c:(len(c),c)))
    base=len(enc.clauses);target=124-sum(fixed.values())
    enc.interval(list(range(1,len(edges)+1)),target,target)
    meta=dict(H_density=density,H_anchor=anchor,Q_core_H_labels=core,Q_other_mark=other,
              fixed_pairs=len(fixed),fixed_red=sum(fixed.values()),primary_variables=len(edges),
              base_clauses=base,possible_cliques=census,Q_red_edges=124,free_red_sum=target,
              ordering='none',scope='chosen H; one marked blue neighborhood; not a43-vertex extension')
    return fixed,edges,enc,meta


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--kissat',type=Path,required=True);p.add_argument('--seconds',type=int,default=60)
    p.add_argument('--emit-only',action='store_true');a=p.parse_args()
    need(a.seconds>0,'positive cap');a.work.mkdir(exist_ok=False)
    need(sha(PARENT/'encoding.py')=='902f06f7bd3ec062aaa717743bd972ab0f3fcaaff43d3ade2197b4252820dbcd','encoding identity')
    for density in (92,93):
        for anchor in (0,1):
            start=time.monotonic();work=a.work/f'{density}-{anchor}';work.mkdir()
            fixed,edges,enc,report=build(density,anchor);cnf=work/'case.cnf'
            with cnf.open('x') as f:
                f.write(f'p cnf {enc.variables} {len(enc.clauses)}\n')
                for row in enc.clauses:f.write(' '.join(map(str,row))+' 0\n')
            report.update(status='EMITTED',variables=enc.variables,clauses=len(enc.clauses),
                          source_sha256=sha(Path(__file__)),H_sha256=HASHES[density],
                          formula_sha256=sha(cnf),formula_bytes=cnf.stat().st_size,
                          build_seconds=time.monotonic()-start,solver_cap_seconds=a.seconds)
            def save():
                (work/'result.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
                print(json.dumps(report),flush=True)
            save()
            if a.emit_only:continue
            log=work/'solver.log';trace=work/'trace.drat';t=time.monotonic()
            with log.open('x') as f:
                try:code=subprocess.run([str(a.kissat),f'--time={a.seconds}',str(cnf),str(trace)],stdout=f,stderr=subprocess.STDOUT,timeout=a.seconds+30).returncode
                except subprocess.TimeoutExpired:code=None
            report.update(solver_exit=code,solver_seconds=time.monotonic()-t,
                          status={0:'UNKNOWN',10:'SAT_UNCHECKED',20:'UNSAT_UNCHECKED'}.get(code,'ERROR'),
                          max_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                          solver_sha256=sha(a.kissat))
            if code==10:
                values={}
                for row in log.read_text().splitlines():
                    if row.startswith('v '):
                        for token in row.split()[1:]:
                            lit=int(token)
                            if lit:
                                need(abs(lit) not in values or values[abs(lit)]==(lit>0),'model consistency')
                                values[abs(lit)]=lit>0
                need(set(values)==set(range(1,enc.variables+1)),'complete model')
                need(all(any(values[abs(l)]==(l>0) for l in row) for row in enc.clauses),'model clauses')
                red={e for e,c in fixed.items() if c}|{e for i,e in enumerate(edges,1) if values[i]}
                graph=work/'graph.json';graph.write_text(json.dumps(dict(n=22,red_edges=sorted(red)),indent=2,sort_keys=True)+'\n')
                report.update(status='SAT_MODEL_CHECKED_GRAPH_PENDING_AUDIT',graph_sha256=sha(graph))
            report.update(total_seconds=time.monotonic()-start,trace_bytes=trace.stat().st_size,
                          trace_sha256=sha(trace),log_sha256=sha(log),trace_is_checked_refutation=False)
            save()


if __name__=='__main__':main()

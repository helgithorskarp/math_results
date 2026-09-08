"""One fresh direct graph-colouring refutation for the positive surgery seed."""
from pathlib import Path
from itertools import combinations
import argparse,hashlib,json,os,resource,shutil,threading,time
D=Path(__file__).resolve().parent
P=D

def need(ok,why):
    if not ok:raise ValueError(why)

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def main():
    global P
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['prepare','solve']);ap.add_argument('--work',type=Path,required=True);a=ap.parse_args()
    P=a.work.resolve();P.mkdir(parents=True,exist_ok=True)
    if a.action=='prepare':
        need(not (P/'QUERY_STARTED').exists(),'query already started')
        for name in ['SOURCE.json','CONTRACT.json']:shutil.copyfile(D/name,P/name)
    plan=json.loads((P/'CONTRACT.json').read_text());need(sha(P/'SOURCE.json')==plan['source_sha256'],'source hash')
    s=json.loads((P/'SOURCE.json').read_text());labels=s['labels'];index={v:i for i,v in enumerate(labels)}
    edges=sorted((index[u],index[v]) for u,v in s['edges']);n=len(labels);adj=[set() for _ in labels]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    tri=next((u,v,w) for u,v in edges for w in sorted(adj[u]&adj[v]) if v<w)
    if a.action=='prepare':
        need(not (P/'QUERY_STARTED').exists(),'query already started')
        with (P/'source.cnf').open('w') as f:
            f.write(f'p cnf {4*n} {n+4*len(edges)+3}\n')
            for v in range(n):f.write(' '.join(str(4*v+k+1) for k in range(4))+' 0\n')
            for u,v in edges:
                for k in range(4):f.write(f'{-4*u-k-1} {-4*v-k-1} 0\n')
            for k,v in enumerate(tri):f.write(f'{4*v+k+1} 0\n')
        out={'vertices':n,'edges':len(edges),'triangle':tri,'CNF_sha256':sha(P/'source.cnf')}
        (P/'SOURCE_CNF_META.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));return
    from pysat.solvers import Glucose42
    from pysat.formula import CNF
    audit=json.loads((P/'SOURCE_AUDIT.json').read_text());need(audit['verified'] and audit['CNF_sha256']==sha(P/'source.cnf'),'independent geometry and CNF audit')
    resource.setrlimit(resource.RLIMIT_AS,(plan['source_memory_bytes'],)*2)
    resource.setrlimit(resource.RLIMIT_FSIZE,(plan['source_proof_bytes'],)*2)
    (P/'QUERY_STARTED').open('x').close()
    with Glucose42(bootstrap_with=CNF(from_file=str(P/'source.cnf')).clauses,with_proof=True) as solver:
        stop=threading.Event();start=time.monotonic();reason=[]
        def watch():
            last=-1
            while not stop.wait(1):
                elapsed=time.monotonic()-start;size=os.fstat(solver.prfile.fileno()).st_size
                if int(elapsed)//30!=last:last=int(elapsed)//30;print('RUNNING',round(elapsed,1),'seconds',size,'proof bytes',flush=True)
                if elapsed>=plan['source_seconds'] or size>=plan['source_proof_bytes']-4194304:
                    reason.append('wall' if elapsed>=plan['source_seconds'] else 'proof_bytes');solver.interrupt();return
        t=threading.Thread(target=watch,daemon=True);t.start();solver.conf_budget(plan['source_conflicts'])
        ans=solver.solve_limited(expect_interrupt=True);elapsed=time.monotonic()-start;stop.set();t.join()
        name='source.drat' if ans is False else 'source.partial.drat';solver.prfile.flush();solver.prfile.seek(0)
        with (P/name).open('wb') as f:shutil.copyfileobj(solver.prfile,f)
        if ans is True:
            model=set(x for x in solver.get_model() if x>0);word=[next(k for k in range(4) if 4*v+k+1 in model) for v in range(n)]
            need(all(word[u]!=word[v] for u,v in edges),'source model');(P/'source_colouring.bin').write_bytes(bytes(word))
        out={'answer':'UNSAT' if ans is False else 'SAT' if ans else 'UNKNOWN','seconds':elapsed,'statistics':solver.accum_stats(),'interrupt_reason':reason,'proof_file':name,'proof_bytes':(P/name).stat().st_size,'proof_sha256':sha(P/name),'proof_verified':False,'CNF_sha256':sha(P/'source.cnf')}
        (P/'SOURCE_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)

if __name__=='__main__':main()

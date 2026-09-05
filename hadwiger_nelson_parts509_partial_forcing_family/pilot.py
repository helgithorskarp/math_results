#!/usr/bin/env python3
"""One bounded selector query and, if SAT, one graph query per support."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
from engine import HERE,POINTS,compute,require
from controls import check


def save(path,value):
    temp=path.with_name(path.name+'.tmp')
    temp.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n');temp.replace(path)


def digest(path):
    h=sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest()


def limits():resource.setrlimit(resource.RLIMIT_AS,(4294967296,4294967296))


def run(cmd,log):
    start=time.monotonic()
    with log.open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,preexec_fn=limits)
    return dict(command=cmd,exit_code=r.returncode,wall_seconds=time.monotonic()-start,
                maximum_child_rss_kib_cumulative=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
    for name in ['roundingsat','veripb','kissat','drat-trim']:ap.add_argument('--'+name,type=Path,required=True)
    a=ap.parse_args();a.work=a.work.resolve();a.work.mkdir(parents=True,exist_ok=True)
    require(not (a.work/'pilot.json').exists(),'existing pilot: do not restart completed queries')
    start=time.monotonic();facts,supports=compute()
    require(facts==json.loads((HERE/'expected.json').read_text()),'expected exact facts')
    require(check(facts,supports)==json.loads((HERE/'controls_expected.json').read_text()),'preflight controls')
    result=dict(status='running',supports=[]);save(a.work/'pilot.json',result)
    for fact in facts:
        q=fact['q'];s=supports[q];d=a.work/str(q);d.mkdir(exist_ok=True)
        if (d/'selector.opb').exists():require((d/'selector.opb').read_bytes()==s['opb'],'preflight instance identity')
        (d/'selector.opb').write_bytes(s['opb'])
        row=dict(q=q,status='running',OPB_sha256=fact['OPB_sha256']);result['supports'].append(row)
        save(a.work/'pilot.json',result)
        row['native_PB']=run([str(a.roundingsat.resolve()),str(d/'selector.opb'),'--time-limit=120',
                              '--print-sol=1','--proof-log='+str(d/'selector.pb')],d/'solver.log')
        text=(d/'solver.log').read_text()
        if 's UNSATISFIABLE' in text:
            row['status']='UNSAT_PENDING_CHECK';save(a.work/'pilot.json',result)
            row['PB_checker']=run([str(a.veripb.resolve()),str(d/'selector.opb'),str(d/'selector.pb')],d/'checker.log')
            require(row['PB_checker']['exit_code']==0 and 's VERIFIED UNSATISFIABLE' in (d/'checker.log').read_text(),'complete PB proof rejected')
            row.update(status='SUPPORT_CLOSED_THROUGH508',PB_proof_bytes=(d/'selector.pb').stat().st_size,
                       PB_proof_sha256=digest(d/'selector.pb'))
        elif 's SATISFIABLE' in text:
            tokens=[v for line in text.splitlines() if line.startswith('v ') for v in line.split()[1:]]
            assignment={}
            for token in tokens:
                if token=='0':continue
                positive=not token.startswith(('-','~'));v=token.lstrip('-~');v=v[1:] if v.startswith('x') else v
                require(int(v) not in assignment,'duplicate PB model variable');assignment[int(v)]=positive
            require(set(assignment)==set(range(1,len(s['free'])+1)),'complete primary model')
            X={v for i,v in enumerate(s['free'],1) if assignment[i]}
            require(all(sum(c for v,c in coeff.items() if v in X)>=rhs for coeff,rhs in s['rows']),'decoded primary model')
            labels=sorted(s['fixed']|X);pos={v:i for i,v in enumerate(labels)}
            edges=[(u,v) for u,v in s['edges'] if u in pos and v in pos]
            require(len(labels)<=508 and min(len(s['adj'][v]&set(labels)) for v in labels)>=4,'candidate size and degree')
            clauses=[[4*i+c+1 for c in range(4)] for i in range(len(labels))]
            clauses += [[-(4*pos[u]+c+1),-(4*pos[v]+c+1)] for u,v in edges for c in range(4)]
            triangle=next((u,v,w) for u,v in edges for w in sorted(s['adj'][u]&s['adj'][v]) if w>v and w in pos)
            clauses += [[4*pos[v]+c+1] for c,v in enumerate(triangle)]
            cnf=(f'p cnf {4*len(labels)} {len(clauses)}\n'+''.join(' '.join(map(str,C))+' 0\n' for C in clauses)).encode()
            (d/'candidate.cnf').write_bytes(cnf)
            row.update(status='SAT_SELECTOR_CHECKED',selector=sorted(X),candidate_labels=labels,
                       candidate_vertices=len(labels),candidate_edges=len(edges),pinned_triangle=list(triangle),
                       candidate_cnf_sha256=sha256(cnf).hexdigest())
            save(a.work/'pilot.json',result)
            row['native_graph']=run([str(a.kissat.resolve()),'--time=60',str(d/'candidate.cnf'),str(d/'candidate.drat')],d/'graph.log')
            if row['native_graph']['exit_code']==10:
                positive={int(x) for line in (d/'graph.log').read_text().splitlines() if line.startswith('v ') for x in line.split()[1:] if int(x)>0}
                colouring=''.join(str(next(c for c in range(4) if 4*i+c+1 in positive)) for i in range(len(labels)))
                require(all(colouring[pos[u]]!=colouring[pos[v]] for u,v in edges),'candidate colouring')
                row.update(status='SELECTOR_PASSES_BUT_CANDIDATE_FOUR_COLOURABLE',candidate_colouring=colouring)
            elif row['native_graph']['exit_code']==20:
                row['status']='CANDIDATE_UNSAT_PENDING_CHECK';save(a.work/'pilot.json',result)
                row['graph_checker']=run([str(a.drat_trim.resolve()),str(d/'candidate.cnf'),str(d/'candidate.drat')],d/'graph_checker.log')
                require(row['graph_checker']['exit_code']==0 and 's VERIFIED' in (d/'graph_checker.log').read_text(),'complete graph proof rejected')
                row.update(status='RECORD_CANDIDATE_NON_FOUR_COLOURABLE_VERIFIED',graph_proof_sha256=digest(d/'candidate.drat'))
            else:row['status']='SAT_SELECTOR_GRAPH_UNKNOWN'
        else:row['status']='PB_UNKNOWN'
        result['wall_seconds']=time.monotonic()-start;save(a.work/'pilot.json',result)
        print(json.dumps({k:v for k,v in row.items() if k not in ['selector','candidate_labels','candidate_colouring']}),flush=True)
        if row['status']=='RECORD_CANDIDATE_NON_FOUR_COLOURABLE_VERIFIED':break
    result['status']='completed';result['wall_seconds']=time.monotonic()-start;save(a.work/'pilot.json',result)
    print(json.dumps(dict(status='completed',cases=[(r['q'],r['status']) for r in result['supports']],wall_seconds=result['wall_seconds'])),flush=True)


if __name__=='__main__':main()

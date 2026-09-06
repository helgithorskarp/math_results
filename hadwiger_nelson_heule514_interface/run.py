#!/usr/bin/env python3
"""One bounded simultaneous H514 decision; negative answers are hints."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import time
from pysat.solvers import Solver
import engine as E

def save(p,x):
    t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(x,separators=(',',':'))+'\n');t.replace(p)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);args=parser.parse_args();w=args.work;w.mkdir(exist_ok=False)
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,)*2);start=time.monotonic();data=E.inputs();initial=E.transport(data);rows=E.minimal(initial)
    save(w/'graph.json',dict(coordinates=[[[str(x) for x in a] for a in p] for p in data['points']],edges=data['edges'],large=data['large'],small=data['small'],centres=[r['centre_index'] for r in data['chosen']]))
    save(w/'initial_rows.json',initial);save(w/'initial_minimal.json',rows)
    n,clauses=E.activated(data['edges']);raw=E.raw(n,clauses);(w/'activation.cnf').write_bytes(raw)
    native=[];history=[];status='BOUND_REACHED';target=None;master_counts=[]
    with Solver(name='cadical195',bootstrap_with=clauses) as oracle:
        for turn in range(65):
            mn,mc=E.master(rows);(w/'master.cnf').write_bytes(E.raw(mn,mc))
            with Solver(name='cadical195',bootstrap_with=mc) as master:
                master.conf_budget(100000);t=time.monotonic();answer=master.solve_limited();master_counts.append(dict(answer=answer,seconds=time.monotonic()-t,variables=mn,clauses=len(mc)))
                if answer is not True:
                    status='COVERAGE_AWAITING_INDEPENDENT_CHECK' if answer is False else 'MASTER_UNKNOWN';break
                selected_omissions=sorted(x-1 for x in master.get_model() if 1<=x<=E.N)
                O=selected_omissions[:6]
            E.need(len(O)==6 and all(not set(r['D'])<=set(O) for r in rows),'uncovered target selection')
            if turn==64:target=O;break
            assumptions=[(4*E.N+1+v)*(-1 if v in O else 1) for v in range(E.N)]
            oracle.conf_budget(100000);t=time.monotonic();answer=oracle.solve_limited(assumptions=assumptions)
            rec=dict(turn=turn,omitted=O,answer=answer,seconds=time.monotonic()-t)
            if answer is not True:
                status='NATIVE_UNKNOWN' if answer is None else 'TARGET_NEEDS_CERTIFICATE';target=O;history.append(rec)
                selected=sorted(set(range(E.N))-set(O));tn,tc=E.graph_cnf(selected,data['edges']);(w/'target.cnf').write_bytes(E.raw(tn,tc));save(w/'target_vertices.json',selected);break
            pos={x for x in oracle.get_model() if x>0}
            c=''.join('.' if v in O else str(next(j for j in range(4) if 4*v+j+1 in pos)) for v in range(E.N))
            E.need(E.check(c,data['edges'])==O,'candidate colouring');c=E.extend(c,data['adj'],data['large']+data['small']);D=E.check(c,data['edges']);E.need(D and set(D)<=set(O),'extension')
            row=dict(kind='native',native_index=len(native),D=D,colouring=c);native.append(row);rows=E.minimal(rows+[row]);rec.update(D=D,cut_count=len(rows));history.append(rec)
            save(w/'progress.json',dict(status=status,rows=rows,history=history));print(json.dumps(rec),flush=True)
    save(w/'native_witnesses.json',native);save(w/'final_rows.json',rows)
    result=dict(status=status,vertices=E.N,edges=len(data['edges']),initial_rows=len(initial),initial_antichain=len(E.minimal(initial)),final_antichain=len(rows),initial_forced=sum(len(r['D'])==1 for r in E.minimal(initial)),final_forced=sum(len(r['D'])==1 for r in rows),native_queries=len(history),native_positives=len(native),master_calls=master_counts,history=history,target_omitted=target,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,activation_sha256=sha256(raw).hexdigest())
    save(w/'result.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ['history','master_calls']},sort_keys=True),flush=True)

if __name__=='__main__':main()

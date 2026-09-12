"""Produce and check every member of the declared complete 97-case subdivision."""
import argparse,ctypes,hashlib,importlib.metadata,json,sys,time
from pathlib import Path
import problem
import verify

def main():
    p=argparse.ArgumentParser();p.add_argument('--scratch',required=True);p.add_argument('--drat-trim',required=True);a=p.parse_args()
    problem.require(importlib.metadata.version('python-sat')=='1.9.dev15','Pinned python-sat 1.9.dev15 required')
    from pysat.solvers import Solver
    out=Path(a.scratch).resolve();out.mkdir(exist_ok=False);checker=Path(a.drat_trim).resolve();problem.require(checker.is_file(),'proof checker')
    expected=json.loads((problem.HERE/'EXPECTED.json').read_text());orbits=problem.orbit_partition();results=[];started=time.monotonic()
    for index,(rep,members) in enumerate(orbits):
        case=out/f'orbit-{index:03d}';case.mkdir();raw=problem.dimacs(rep);cnf=case/'input.cnf';cnf.write_bytes(raw);nv,clauses,_=problem.formula(rep)
        record={'core':4,'orbit_index':index,'representative':rep,'orbit_size':len(members),'variables':nv,'clauses':len(clauses),'cnf_sha256':hashlib.sha256(raw).hexdigest(),'status':'STARTED'}
        problem.require(record['cnf_sha256']==expected['results'][index]['cnf_sha256'],'changed declared formula');(case/'STARTED.json').write_text(json.dumps(record,indent=2)+'\n');t=time.monotonic()
        if expected['results'][index]['status']=='TAIL_UNDECIDED':
            record.update(status='TAIL_UNDECIDED',solver_called=False,solver_seconds=None,reason='This tail relaxation is not part of the refuted geometry. Its complete full43 receiver remains UNKNOWN.')
            (case/'result.json').write_text(json.dumps(record,indent=2)+'\n');results.append(record);(out/'PARTIAL_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
            print(json.dumps({k:record[k] for k in ['orbit_index','representative','status']}),flush=True);continue
        with Solver(name='cadical300',bootstrap_with=clauses,with_proof=True) as solver:
            status=solver.solve();problem.require(type(status) is bool,'UNKNOWN is not a decision');record['solver_seconds']=time.monotonic()-t;record['stats']=solver.accum_stats()
            if status:
                values={abs(v):int(v>0) for v in solver.get_model()};n,fixed,free,var=problem.geometry(rep)
                problem.require(set(range(1,nv+1))<=set(values) and all(any(values[abs(l)]==int(l>0) for l in c) for c in clauses),'bad solver model')
                graph=dict(fixed);graph.update({e:values[v] for e,v in var.items()});g={'order':n,'red_edges':[list(e) for e,c in graph.items() if c]};problem.check_graph(rep,g)
                record.update(status='SAT_TAIL_ONLY',physical_tail_word=problem.physical_word(g))
            else:
                problem.require(ctypes.CDLL(None).fflush(None)==0,'proof flush failed');solver.solver.prfile.seek(0);proof=solver.solver.prfile.read()+b'a\x00'
                # A final empty record has force only if independent proof checking accepts it.
                path=case/'proof.drat';path.write_bytes(proof);tcheck=time.monotonic();receipt=verify.checked_proof(cnf,path,checker)
                record.update(status='UNSAT_CHECKED',proof_bytes=len(proof),proof_sha256=receipt['proof_sha256'],checker_seconds=time.monotonic()-tcheck)
        problem.require(record['status']==expected['results'][index]['status'],'decision differs from declared exact classification')
        (case/'result.json').write_text(json.dumps(record,indent=2)+'\n');results.append(record);(out/'PARTIAL_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps({k:record[k] for k in ['orbit_index','representative','status','solver_seconds']}),flush=True)
    report={'core':4,'cases':97,'physical_cut_complete':True,'tail_classification_complete':False,'unsat':sum(r['status']=='UNSAT_CHECKED' for r in results),'sat_tail':sum(r['status']=='SAT_TAIL_ONLY' for r in results),'tail_undecided':sum(r['status']=='TAIL_UNDECIDED' for r in results),'seconds':time.monotonic()-started,'python':sys.version,'python_sat':importlib.metadata.version('python-sat'),'checker_sha256':hashlib.sha256(checker.read_bytes()).hexdigest(),'results':results}
    (out/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n')
    audit=verify.verify(out,checker);(out/'INDEPENDENT_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps({k:v for k,v in audit.items() if k!='proof_receipts'},sort_keys=True))
if __name__=='__main__':main()

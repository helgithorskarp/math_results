"""Cold exact replay; guarded/incomplete outcomes never establish exclusion."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time
from common import BASE,g,masks,star,vertices,compact,write,cnf_text,OFFSETS
import build
import patterns


def sha(data):return hashlib.sha256(data).hexdigest()


def unit_conflict(clauses):
    assigned=set()
    while True:
        changed=False
        for c in clauses:
            if any(v in assigned for v in c):continue
            rest=[v for v in c if -v not in assigned]
            if not rest:return True
            if len(rest)==1:assigned.add(rest[0]);changed=True
        if not changed:return False


def geometry(rows):
    shape,fixture=g.inputs();root,_,_=g.mesh(shape)
    occupied=set();prefixes=[];previous_vertices=None
    for level in range(5):
        for p in fixture:
            if p['level']!=level:continue
            g.check.isometry(p['matrix']);f={g.move(t,p) for t in shape}
            assert len(f)==214 and occupied.isdisjoint(f);occupied.update(f)
        stats,vs,_=g.mesh(occupied)
        if previous_vertices is not None:assert all(g.star(v)<=occupied for v in previous_vertices)
        previous_vertices=vs;prefixes.append({'level':level,'cells':stats['cells'],'chi':stats['chi']})
    cs={compact(t) for t in occupied};vm=masks(cs)
    for v,mask in vm.items():
        assert {vertices(t) for t in star(v)}==g.star(v)
        direct=sum(1<<j for j,(k,x,y) in enumerate(OFFSETS)
                   if (k,v[0]+x,v[1]+y) in cs)
        assert mask==direct
    checks=[]
    for row in rows:
        canonical={k:v for k,v in row.items() if k not in ('check','pattern_sha256')}
        digest=sha(json.dumps(canonical,sort_keys=True,separators=(',',':')).encode())
        assert digest==row['pattern_sha256']
        check=patterns.check(shape,row);assert check==row['check']
        checks.append({'pattern_sha256':digest,**check})
    return {'root_cells':root['cells'],'prefixes':prefixes,'patterns':checks}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--phase',choices=('geometry','formula'),required=True)
    ap.add_argument('--work',type=Path,required=True);ap.add_argument('--checker',type=Path)
    ap.add_argument('--write-expected',action='store_true')
    a=ap.parse_args();start=time.monotonic();work=a.work.resolve()
    assert not work.is_relative_to(BASE);work.mkdir(parents=True,exist_ok=True)
    rows=json.loads((BASE/'patterns.json').read_text())
    if a.phase=='geometry':result=geometry(rows)
    else:
        assert a.checker and a.checker.is_file()
        fixed,poses,feet,owners,pruned,pairs,inv=build.inventory()
        clauses,conflicts=build.formula(feet,owners,pruned,pairs)
        base=cnf_text(len(poses),clauses);base_sha=sha(base.encode())
        assert base_sha=='a1df05627a7f8708e81cd6ce7d7f57c290da596acf75e6a37ef8a75e27c18bf5'
        del base
        cuts=set();counts=[]
        for row in rows:
            cs=build.instances(row,fixed,poses);counts.append(len(cs));cuts.update(cs)
        clauses += [list(c) for c in sorted(cuts)]
        cnf=cnf_text(len(poses),clauses);(work/'instance.cnf').write_text(cnf)
        result={'inventory':inv,'base_binary_conflicts':conflicts,'base_cnf_sha256':base_sha,
                'pattern_instance_counts':counts,'distinct_pattern_clauses':len(cuts),
                'variables':len(poses),'clauses':len(clauses),'cnf_sha256':sha(cnf.encode())}
        write(work/'pre-solver.json',result)
        print(json.dumps(result),flush=True)
        from pysat.solvers import Solver
        with Solver(name='glucose4',bootstrap_with=clauses,with_proof=True) as solver:
            solver.conf_budget(20000);status=solver.solve_limited()
            assert status is False,'SAT/UNKNOWN supplies no exclusion'
            trace='\n'.join(solver.get_proof())+'\n';(work/'proof.drat').write_text(trace)
            stats=solver.accum_stats()
        run=subprocess.run([str(a.checker.resolve()),str((work/'instance.cnf').resolve()),
                            str((work/'proof.drat').resolve())],capture_output=True,text=True,timeout=10)
        log=run.stdout+run.stderr;(work/'drat-check.txt').write_text(log)
        if run.returncode==1 and 'c trivial UNSAT' in log:assert unit_conflict(clauses)
        assert 's VERIFIED' in log and (run.returncode==0 or
               run.returncode==1 and 'c trivial UNSAT' in log)
        result['status']='UNSAT; independently DRAT verified'
        write(work/'native.json',{'solver_stats':stats,'proof_bytes':len(trace.encode()),
                                  'proof_sha256':sha(trace.encode()),'checker_returncode':run.returncode})
    expected_file=BASE/'expected.json'
    expected=json.loads(expected_file.read_text()) if expected_file.exists() else {}
    if a.write_expected:
        expected[a.phase]=result;write(expected_file,expected)
    else:assert result==expected[a.phase],'expected manifest mismatch'
    write(work/(a.phase+'-result.json'),result)
    print(json.dumps({'agent':'six-heesch-2','role':'researcher','phase':a.phase,
                      'seconds':round(time.monotonic()-start,3),
                      'peak_parent_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))


if __name__=='__main__':main()

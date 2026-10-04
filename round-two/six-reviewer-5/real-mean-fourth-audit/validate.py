"""Serial full replays and intended mathematical/type/preimport defects."""
import argparse, hashlib, json, os, resource, shutil, subprocess, sys, time
from pathlib import Path


def require(ok, label):
    if not ok:raise ValueError(label)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--scratch',required=True);parser.add_argument('--summary',required=True)
    parser.add_argument('--second-python');args=parser.parse_args()
    src=Path(__file__).resolve().parent;scratch=Path(args.scratch).resolve()
    require(src not in scratch.parents and scratch!=src,'validation outside source')
    require(not scratch.exists(),'fresh validation directory');scratch.mkdir(parents=True)
    env=dict(os.environ)
    for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[name]='1'
    from_verify=(src/'verify.py').read_text()
    cold=scratch/'source-only';shutil.copytree(src,cold,ignore=shutil.ignore_patterns('__pycache__'))
    rows=[];reference=None
    def child(code,optimized,label,damage=None,positive=False,python=None):
        nonlocal reference
        path=scratch/(label+'.json');cmd=[python or sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(code/'verify.py'),'--record',str(path)]
        if damage:cmd+=['--damage',damage]
        start=time.monotonic();run=subprocess.run(cmd,cwd=scratch,env=env,text=True,capture_output=True,timeout=45)
        row=dict(label=label,positive=positive,code=run.returncode,seconds=time.monotonic()-start,peak_child_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,stdout=run.stdout,stderr=run.stderr)
        if positive:
            require(run.returncode==0,label+' whole positive failed')
            whole=path.read_bytes()
            if reference is None:reference=whole
            require(whole==reference,label+' entire normal/O/relocated/interpreter record differs')
            row['whole_record_equal']=True
        else:
            require(run.returncode!=0 and 'intended defect escaped' not in run.stderr,label+' defect not rejected mathematically')
            require('Timeout' not in run.stderr,label+' timeout is not a rejection')
        rows.append(row);print(json.dumps(dict(label=label,code=run.returncode,seconds=row['seconds'])),flush=True)
    for code,label in ((src,'local'),(cold,'cold')):
        for optimized in (False,True):child(code,optimized,label+('-O' if optimized else '-normal'),positive=True)
    if args.second_python:
        for optimized in (False,True):child(cold,optimized,'second-python'+('-O' if optimized else '-normal'),positive=True,python=args.second_python)
    for damage in ('third','pair-third','fourth','pair-fourth','M','beta','inward','balance','multiplicity','anchor','cost-multiplicity','column'):
        for optimized in (False,True):child(src,optimized,damage+('-O' if optimized else '-normal'),damage=damage)
    for kind in ('float','boolean','drop-root','alter-coefficient'):
        code=scratch/('fixture-'+kind);shutil.copytree(cold,code);fixture=code/'FRESH-BASE.json';v=json.loads(fixture.read_text())
        if kind=='float':v['rows'][-1]['label']=8.0
        elif kind=='boolean':v['rows'][-1]['label']=True
        elif kind=='drop-root':v['rows'].pop()
        else:v['rows'][0]['primitive'][0][0][1][0][1][0][1][0]+=1
        fixture.write_text(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n')
        seal=code/'SHA256SUMS';lines=seal.read_text().splitlines()
        lines=[hashlib.sha256(fixture.read_bytes()).hexdigest()+'  FRESH-BASE.json' if line.endswith('  FRESH-BASE.json') else line for line in lines]
        seal.write_text('\n'.join(lines)+'\n');child(code,True,'fixture-'+kind)
    for kind in ('arithmetic','census'):
        code=scratch/('source-'+kind);shutil.copytree(cold,code)
        if kind=='arithmetic':(code/'algebra.py').write_text("raise RuntimeError('BAD MODULE IMPORTED')\n"+(code/'algebra.py').read_text())
        else:(code/'SHA256SUMS').write_text((code/'SHA256SUMS').read_text().splitlines()[0]+'\n')
        child(code,True,'source-'+kind);require('source seal' in rows[-1]['stderr'] and 'BAD MODULE IMPORTED' not in rows[-1]['stderr'],'preimport source gate')
    out=dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',complete=True,serial_children=1,native_threads=1,
      fixed_child_guard_seconds=45,positive_replays=sum(r['positive'] for r in rows),
      mathematical_rejects=24,whole_fixture_rejects=4,preimport_source_rejects=2,whole_record_bytes=len(reference)-1,
      whole_record_sha256=hashlib.sha256(reference[:-1]).hexdigest(),children=rows)
    Path(args.summary).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='children'}))


if __name__=='__main__':main()

"""Regenerate bounded proposals and independently check the entire H8 cover."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time
import urllib.request

HERE=Path(__file__).resolve().parent


def need(ok,message):
    if not ok:raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable(value):
    return json.loads(json.dumps({k:v for k,v in value.items()
                                if k not in ['seconds','maxrss_kib','python','optimization']}))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repository-root',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--drat-source',type=Path)
    args=parser.parse_args()
    need(sys.version_info>=(3,11),'CPython >=3.11 required')
    need(importlib.metadata.version('python-sat')=='1.8.dev24' and
         importlib.metadata.version('six')=='1.17.0','Pinned solver-proposal packages required')
    root=args.repository_root.resolve();output=args.output_dir.resolve()
    manifest=json.loads((HERE/'INPUTS.json').read_text())
    expected=json.loads((HERE/'EXPECTED.json').read_text())
    for relative,digest in manifest['source_sha256'].items():
        path=root/relative
        need(path.resolve().is_relative_to(root) and sha(path)==digest,'Changed pinned input: '+relative)
    output.mkdir(parents=True,exist_ok=False)
    author=root/'round-two/six-vdw-2/order8-rigidity'
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',
             MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',TMPDIR=str(output))
    began=time.monotonic();stages=[]

    def run(label,command):
        started=time.monotonic()
        process=subprocess.Popen(list(map(str,command)),env=env,text=True,
                                 stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        try:stdout,stderr=process.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid,signal.SIGKILL);process.communicate()
            (output/'incomplete.json').write_text(json.dumps({'status':'TIMEOUT_NO_VERDICT','stage':label}))
            raise RuntimeError('Operational timeout, no mathematical verdict: '+label)
        (output/(label+'.log')).write_text(stdout+stderr)
        need(process.returncode==0,label+' failed; see local log; no mathematical verdict')
        stages.append({'stage':label,'seconds':time.monotonic()-started})
        print(label+' completed',flush=True)
        return stdout

    for length in range(2,19):
        run('encode-'+str(length),[sys.executable,'-B',author/'encode.py',
                                   output/f'run-{length}.cnf','--length',length])
    fields=[]
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal'
        path=output/('field-'+mode+'.json')
        run('field-'+mode,[sys.executable,'-B']+(['-O'] if optimized else [])+
            [HERE/'field.py','--case-dir',output,'--output',path])
        row=json.loads(path.read_text());need(stable(row)==expected['field'],'Complete independent field receipt differs')
        fields.append(row)
    source=output/'drat-trim.c'
    if args.drat_source:source.write_bytes(args.drat_source.read_bytes())
    else:source.write_bytes(urllib.request.urlopen(manifest['converter']['url'],timeout=20).read())
    need(sha(source)==manifest['converter']['sha256'],'Unrecognized official converter source')
    converter=output/'drat-trim'
    run('compile-proposal-transformer',['gcc','-O2','-std=gnu99',source,'-o',converter])
    for length in range(2,19):
        cnf=output/f'run-{length}.cnf'
        run('propose-'+str(length),[sys.executable,'-B',author/'solve.py',cnf,'--conflicts',50000])
        proposed=json.loads(cnf.with_suffix('.solve.json').read_text())
        need(proposed['status']=='UNSAT_PENDING_CHECK','Incomplete proposal; no exclusion')
        transformed=run('transform-'+str(length),[converter,cnf,cnf.with_suffix('.drat'),
                                                '-t',25,'-L',cnf.with_suffix('.lrat')])
        need('s VERIFIED' in transformed,'No complete transformed proposal; no exclusion')
    proofs=[];controls=[]
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal'
        path=output/('proof-'+mode+'.json')
        run('proof-'+mode,[sys.executable,'-B']+(['-O'] if optimized else [])+
            [HERE/'check.py','--case-dir',output,'--author-expected',author/'expected.json','--output',path])
        row=json.loads(path.read_text());need(stable(row)==expected['proof'],'Complete independent proof receipt differs')
        proofs.append(row)
        stdout=run('controls-'+mode,[sys.executable,'-B']+(['-O'] if optimized else [])+
            [HERE/'controls.py','--case-dir',output,'--work',output/('controls-'+mode)])
        row=json.loads(stdout);need(row==expected['controls'],'Complete independent controls receipt differs')
        controls.append(row)
    record={'agent':'six-reviewer-5','role':'independent reviewer',
            'status':'H8_EXCLUSION_AND_SHARP_COSET_INTERVAL_CLASSIFICATION_VERIFIED',
            'source_files_checked':len(manifest['source_sha256']),
            'python':sys.version.split()[0],'python_sat':'1.8.dev24','threads':1,'CPU_jobs_at_once':1,
            'seconds':time.monotonic()-began,'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'field_modes':[{'optimization':z['optimization'],'seconds':z['seconds'],
                            'maxrss_kib':z['maxrss_kib'],'case_CNF_hashes':[r['CNF_sha256'] for r in z['cases']]}
                           for z in fields],
            'proof_modes':[{'optimization':z['optimization'],'seconds':z['seconds'],
                            'maxrss_kib':z['maxrss_kib'],'cases':len(z['cases']),
                            'RUP_additions':z['RUP_additions'],'hint_reads':z['hint_reads'],
                            'all_reference_proof_bytes_match':all(r['reference_proof_byte_match'] for r in z['cases'])}
                           for z in proofs],
            'controls':controls,'minimum_AP_window':fields[0]['minimum_AP_window'],
            'minimizing_supports':fields[0]['minimizing_supports'],'stages':stages,
            'native_status_trusted_as_proof':False,'imported_order11_classification_reproved':False}
    (output/'VALIDATION.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ['stages','field_modes']},indent=2))


if __name__=='__main__':
    main()

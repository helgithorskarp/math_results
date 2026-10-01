"""Independent nativeDRAT and solver-free PythonRUP proof replay.

Credits six-sorting-1/7452 for the pinned watched-literal RUP implementation.
Native cores are checked against the complete actual CNF before replay.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import signal
import subprocess
import time
from shared import HERE,inputs,read,residual_tails,tail_path


def clauses(path):
    header=None;body=[]
    with path.open() as source:
        for line in source:
            if line.startswith('c') or not line.strip():continue
            fields=line.split()
            if fields[0]=='p':
                assert fields[1]=='cnf' and len(fields)==4
                header=tuple(map(int,fields[2:]))
            else:
                values=list(map(int,fields));assert values[-1]==0 and all(values[:-1])
                body.append(tuple(sorted(set(values[:-1]))))
    assert header is not None and len(body)==header[1]
    return header[0],body


def main():
    assert __debug__
    parser=argparse.ArgumentParser()
    parser.add_argument('--repository',type=Path,default=HERE.parent)
    parser.add_argument('--output',type=Path,default=HERE/'generated')
    parser.add_argument('--drat-trim',type=Path,
                        help='Also replay fresh raw DRAT and compare its native outputs with supplied evidence')
    args=parser.parse_args();inputs(args.repository);began=time.monotonic()
    path=args.repository/'sorting13_maximum_preparation/watched_rup.py'
    spec=importlib.util.spec_from_file_location('credited_peer_rup',path)
    rup=importlib.util.module_from_spec(spec);spec.loader.exec_module(rup)
    controls=rup.self_check();cert=read(HERE/'certificate.json');records=[]
    for tail in residual_tails(args.output):
        index,image=tail['parent_index'],tail['image']
        base=tail_path(args.output,tail)
        raw=base.with_suffix('.drat');meta=read(base.with_suffix('.metadata.json'))
        expected=next(r for r in cert['tail_certificates'] if (r['parent_index'],r['image'])==(index,image))
        assert hashlib.sha256(base.read_bytes()).hexdigest()==meta['cnf_sha256']==expected['cnf_sha256']
        core=HERE/expected['public_core_file'];trimmed=HERE/expected['public_rup_file']
        assert hashlib.sha256(core.read_bytes()).hexdigest()==expected['core_sha256']
        assert hashlib.sha256(trimmed.read_bytes()).hexdigest()==expected['trimmed_drat_sha256']
        if args.drat_trim is not None:
            assert hashlib.sha256(raw.read_bytes()).hexdigest()==expected['raw_drat_sha256']
            native_core=base.with_suffix('.core.cnf');native_trimmed=base.with_suffix('.trimmed.drat')
            command=[str(args.drat_trim.resolve()),str(base),str(raw),'-c',str(native_core),'-l',str(native_trimmed),
                 '-L',str(base.with_suffix('.lrat')),'-t','40']
            native=subprocess.run(command,capture_output=True,text=True,timeout=45)
            base.with_suffix('.native-check.log').write_text(native.stdout+native.stderr)
            assert native.returncode==0 and 's VERIFIED' in native.stdout,native.stdout[-1000:]
            assert '0 RAT lemmas in core' in native.stdout
            assert native_core.read_bytes()==core.read_bytes()
            assert hashlib.sha256(native_trimmed.read_bytes()).hexdigest()==expected['native_trimmed_drat_sha256']
            lines=native_trimmed.read_text().splitlines()
            clean='\n'.join(line for line in lines if not line.startswith('d '))+'\n'
            assert clean.encode()==trimmed.read_bytes()
            assert sum(line.startswith('d ') for line in lines)==expected['native_trimmed_deletions_omitted']
            compact=subprocess.run([str(args.drat_trim.resolve()),str(core),str(trimmed),'-t','40'],
                                   capture_output=True,text=True,timeout=45)
            base.with_suffix('.native-compact-check.log').write_text(compact.stdout+compact.stderr)
            assert compact.returncode==0 and 's VERIFIED' in compact.stdout
            assert '0 RAT lemmas in core' in compact.stdout
        n,body=clauses(core);full_n,full_body=clauses(base)
        assert n==full_n==meta['variables']
        assert set(body)<=set(full_body),'Native core contains a clause outside the full CNF'
        assert not rup.WatchedRUP(n,body).entails_by_rup(())
        def stop(signum,frame):raise TimeoutError('PythonRUP40-second bound: incomplete replay gives no exclusion')
        signal.signal(signal.SIGALRM,stop);signal.alarm(40)
        assert not any(line.startswith('d ') for line in trimmed.read_text().splitlines())
        try:additions,deletions=rup.replay(n,body,trimmed)
        finally:signal.alarm(0)
        result=dict(parent_index=index,image=image,status='NATIVE_DRAT_AND_PYTHON_RUP_FULL_MEMBERSHIP_VERIFIED' if args.drat_trim else 'SUPPLIED_PYTHON_RUP_AND_FULL_CNF_MEMBERSHIP_VERIFIED',
                    variables=n,full_clauses=len(full_body),core_clauses=len(body),RUP_additions=additions,
                    ignored_deletions=deletions,RAT_lemmas=0,cnf_sha256=expected['cnf_sha256'],
                    raw_drat_sha256=expected['raw_drat_sha256'],
                    core_sha256=hashlib.sha256(core.read_bytes()).hexdigest(),
                    trimmed_drat_sha256=hashlib.sha256(trimmed.read_bytes()).hexdigest())
        assert deletions==0
        for key in ('core_clauses','RUP_additions','core_sha256','trimmed_drat_sha256'):
            if key in expected:assert result[key]==expected[key],('Unexpected deterministic proof manifest',index,key)
        records.append(result);print(json.dumps(result),flush=True)
    result=dict(agent='six-sorting-2',role='researcher',status='NINE_TAIL_PROOFS_ACTUALLY_VERIFIED',records=records,
                native_DRAT_checked=args.drat_trim is not None,
                tiny_truth_controls=controls,premature_empty_rejected=True,
                seconds=time.monotonic()-began,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                trust='Native checker plus independently implemented RUP, not a reviewer verdict; semantic CNF and class coverage are separate checks')
    (args.output/'tail-proof-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)


if __name__=='__main__':main()

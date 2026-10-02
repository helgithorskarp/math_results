"""Reproduce compact exact checks. Ordinary proof and prior premises are explicit."""
from argparse import ArgumentParser
from pathlib import Path
import hashlib,json,os,resource,subprocess,sys,time


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n'


def worker(work):
    from analytic import derive
    from audit import profile_audit,literal_H_audit
    from controls import identity_controls,damage_controls
    root=Path(__file__).resolve().parent
    start=time.monotonic()
    work.mkdir(parents=True,exist_ok=True)
    record,all_marks,kept=derive()
    audit=profile_audit(record,all_marks,kept)
    local=literal_H_audit(record)
    controls=identity_controls(root/'primary21.rows')
    damage=damage_controls(record,all_marks,kept)
    output=dict(analytic=record,profile_audit=audit,literal_H_audit=local,
                identity_controls=controls,damage_controls=damage)
    raw=canonical(output)
    (work/'MATHEMATICAL.json').write_text(raw)
    (work/'ordered-degree-domain.json').write_text(canonical(dict(all=all_marks,retained=kept)))
    expected=root/'EXPECTED.json'
    status='UNSEALED_VALIDATION_COMPLETE'
    if expected.exists():
        data=json.loads(expected.read_text())
        if type(data)!=dict or canonical(data)!=raw:
            raise ValueError('Entire typed mathematical record differs from frozen expected')
        status='REPRODUCTION_PASS'
    seconds=time.monotonic()-start
    if seconds>25:
        raise RuntimeError('INCOMPLETE fixed25s mathematical guard; no proof verdict')
    receipt=dict(status=status,agent='six-books-2',role='researcher',
                 mathematical_bytes=len(raw.encode()),mathematical_sha256=hashlib.sha256(raw.encode()).hexdigest(),
                 seconds=seconds,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 threads=1,program_guard_seconds=25,
                 trust='Exact source checks of new ordinary proof bridges; no prior theorem replay, independent peer verdict or proof assistant.')
    (work/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


def main():
    p=ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--worker',action='store_true')
    args=p.parse_args()
    if args.worker:
        worker(args.work)
        return
    env=dict(os.environ)
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
        env[name]='1'
    command=[sys.executable]
    if sys.flags.optimize:
        command.append('-O')
    command += [str(Path(__file__).resolve()),'--work',str(args.work.resolve()),'--worker']
    result=subprocess.run(command,env=env,timeout=30,check=False)
    if result.returncode:
        raise SystemExit(result.returncode)


if __name__=='__main__':
    main()

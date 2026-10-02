"""Serial fixed60s proof phases, deterministic expected record, stdlib only."""
from pathlib import Path
import argparse,json,os,subprocess,sys,time,resource
import inputs
from exact import digest


def run():
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',
             BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    root=Path(__file__).resolve().parent;phases=[('calibration',),('negative',)]+[('positive',str(q)) for q in range(19,24)]+[('controls',)]
    rec=[];performance=[]
    for args in phases:
        begin=time.monotonic()
        flags=['-O'] if sys.flags.optimize else []
        try:p=subprocess.run([sys.executable,*flags,str(root/'task.py'),*args],capture_output=True,text=True,env=env,cwd=root,timeout=60)
        except subprocess.TimeoutExpired:raise SystemExit('TIMEOUT: incomplete verification; no mathematical negative conclusion')
        if p.returncode:raise SystemExit(p.stdout+p.stderr)
        rec.append(json.loads(p.stdout));performance.append({'phase':list(args),'seconds':round(time.monotonic()-begin,3)})
    record={'agent':'six-downset-3','role':'researcher','phases':rec,
            'claim_scope':'general-k necessary mean/pair and stronger diagonal Schur conditions; k5 all-real ansatz cutoff q19; new finite q5..23 plus credited q>=24 tail',
            'whole_positive_ordered_entries':sum(r.get('whole_ordered_entries',0) for r in rec),
            'trust_boundary':'ordinary orbit, PSD dual, whole lift and infinite-tail bridges; pinned table/arithmetic; no formalization or peer-review claim'}
    return record,performance


def main():
    p=argparse.ArgumentParser();p.add_argument('--make-expected',action='store_true');p.add_argument('--record',type=Path)
    args=p.parse_args();root=Path(__file__).resolve().parent;expected=root/'EXPECTED.json'
    if args.make_expected and expected.exists():raise SystemExit('Refusing to overwrite frozen expected record')
    record,perf=run()
    if args.make_expected:expected.write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    elif record!=json.loads(expected.read_text()):raise SystemExit('Finite proof record differs from frozen expected data')
    if args.record:
        if args.record.resolve().is_relative_to(root):raise SystemExit('Keep runtime record outside contribution directory')
        args.record.write_text(json.dumps({'record':record,'performance':perf,'peak_child_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss},sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','record_sha256':digest(record),'phases':len(record['phases']),
                      'excluded_q':[r['q'] for r in record['phases'][1]['all_real_ansatz_exclusions']],
                      'positive_q':list(range(19,24)),'ordered_whole_entries':record['whole_positive_ordered_entries'],
                      'damage_rejections':record['phases'][-1]['damage_rejections'],
                      'negative_q18_U0':'-8368/51','kappa':'1/4096','t':'4'},sort_keys=True))


if __name__=='__main__':main()

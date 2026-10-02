"""Portable serial replay. Fixed60s per task; exact complete frozen record.

stdout is the mathematical record, stderr contains private timing progress.
--record-only emits the same record before comparison, for initial freezing.
No missing/timeout phase counts as mathematical infeasibility.
"""
from pathlib import Path
import os,sys,json,subprocess,time
import bootstrap
from exact import require,digest

ROOT=Path(__file__).resolve().parent
FINITE_PAIRS=((4,2),(5,2),(6,2),(8,3),(9,3),(10,3),(11,3))
TASKS=[(str(q),str(k),'continuity') for q,k in FINITE_PAIRS if (q,k)!=(8,3)]
TASKS += [('8','3',phase,kap,t) for kap in ('0','1/4096') for t in ('3/8','1/2') for phase in ('corner-lower','corner-upper')]
TASKS += [(str(q),str(k),phase) for q,k in FINITE_PAIRS for phase in ('whole-lower','whole-gap')]


def census(records):
    def key(d):
        return (str(d['q']),str(d['k']),d['phase']) + (
            (d['kappa'],d['t']) if d['phase'].startswith('corner-') else ())
    require(len(TASKS)==28 and len(records)==28 and sorted(key(d) for d in records)==sorted(TASKS),
            'complete six floors/eight corner forms/fourteen whole forms required')


def parameter_checks():
    from boundary_parameters import record,parameters
    from entries import certificate
    from fractions import Fraction as F
    pairs=FINITE_PAIRS+((7,2),(12,3),(1000000,2),(1000000,3))
    out={'samples':[record(q,k) for q,k in pairs]}
    _,entry=certificate(1000000,3)
    values=[str(entry(A,B)) for A,B in ((0,0),(0,1),(1,0),(1,2),(3,4),(8,16),(3|8,5|16))]
    require(values[1]==values[2],'large scalar-only empty symmetry')
    out['large_scalar_only_entries']=values
    return out


def main(record_only=False):
    env=dict(os.environ)
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
        env[name]='1'
    def child(script,*args):
        cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(ROOT/script),*args]
        start=time.monotonic()
        try:run=subprocess.run(cmd,text=True,capture_output=True,env=env,timeout=60)
        except subprocess.TimeoutExpired:raise RuntimeError('fixed60s operational limit; incomplete, no mathematical conclusion')
        require(run.returncode==0,'child failed: '+repr(cmd)+'\n'+run.stderr)
        print(json.dumps({'task':[script,*args],'seconds':round(time.monotonic()-start,3)}),file=sys.stderr,flush=True)
        return json.loads(run.stdout)
    finite=[child('finite.py',*task) for task in TASKS];census(finite)
    rec={'agent':'six-downset-3','role':'researcher','finite':finite,
         'duals':child('duals.py'),'parameters':child('verify.py','--parameters'),
         'damage_rejections':child('controls.py')}
    require(len(rec['damage_rejections'])==26,'complete corruption census')
    rec['record_sha256']=digest(rec)
    if not record_only:
        expected=json.loads((ROOT/'EXPECTED.json').read_text())
        require(rec==expected,'entire mathematical record differs from frozen EXPECTED.json')
    print(json.dumps(rec,sort_keys=True,indent=2))


if __name__=='__main__':
    require(len(sys.argv)<=2 and (len(sys.argv)==1 or sys.argv[1] in ('--record-only','--parameters')),'unknown replay argument')
    if len(sys.argv)==2 and sys.argv[1]=='--parameters':print(json.dumps(parameter_checks(),sort_keys=True,indent=2))
    else:main(record_only=len(sys.argv)==2)

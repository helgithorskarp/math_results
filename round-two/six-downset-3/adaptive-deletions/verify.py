"""One serial exact child per task; fixed60s guards and deterministic records.

python3 verify.py                 compare the complete frozen EXPECTED.json
python3 -O verify.py              assertion-disabled replay, same records
python3 verify.py --task endpoint run one resumable task
python3 verify.py --emit          regenerate complete expected output
"""
from pathlib import Path
import sys,os,json,time,subprocess,resource
import bootstrap
from exact import require,digest

HERE=Path(__file__).resolve().parent
TASKS=[('endpoint',),('scalars',),('bridge',),('entries',),('damages',)]+[
    ('original',str(q),str(k),phase) for q,k in ((4,1),(7,2),(12,3))
    for phase in ('seed','core-gap','lower','upper','whole-gap')]


def task(args):
    require(tuple(args) in TASKS,'unknown bounded verification task')
    if args[0]=='endpoint':
        from endpoint import endpoint
        return endpoint()
    if args[0]=='scalars':
        from parameters import checks
        return checks()
    if args[0] in ('bridge','entries','damages'):
        from checks import bridge,entry_checks,damages
        return {'bridge':bridge,'entries':entry_checks,'damages':damages}[args[0]]()
    from original import phase
    return phase(int(args[1]),int(args[2]),args[3])


def replay(compare=True):
    frozen=json.loads((HERE/'EXPECTED.json').read_text()) if compare else None
    env=dict(os.environ)
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
        env[key]='1'
    records={}
    for args in TASKS:
        name=' '.join(args);start=time.monotonic()
        command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(HERE/'verify.py'),'--task',*args]
        try:
            child=subprocess.run(command,cwd=HERE,env=env,text=True,capture_output=True,timeout=60,check=False)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError('PAUSED fixed60s operational task limit: '+name+'; no mathematical nonexistence inference') from exc
        require(child.returncode==0,'exact task failed: '+name+'\n'+child.stderr[-4000:])
        records[name]=json.loads(child.stdout)
        if compare:require(records[name]==frozen['records'][name],'frozen certificate mismatch: '+name)
        print(name+' OK '+str(round(time.monotonic()-start,3))+'s',file=sys.stderr,flush=True)
    out={'agent':'six-downset-3','role':'researcher','records':records,'record_sha256':digest(records)}
    if compare:require(out==frozen,'complete expected record differs')
    print('one serial child, fixed60s per task; max child RSS '+str(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)+' KiB',file=sys.stderr)
    return out


if __name__=='__main__':
    if sys.argv[1:2]==['--task']:out=task(sys.argv[2:])
    else:
        require(sys.argv[1:] in ([],['--emit']),'unknown verification arguments')
        out=replay(compare=not sys.argv[1:])
    print(json.dumps(out,sort_keys=True,indent=2))

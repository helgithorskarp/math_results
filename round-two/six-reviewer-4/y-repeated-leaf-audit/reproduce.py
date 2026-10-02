#!/usr/bin/env python3
"""Serial, fixed-guard native reproduction; no author inputs or dependencies."""
from pathlib import Path
import argparse, hashlib, json, os, resource, signal, subprocess, time

ROOT = Path(__file__).resolve().parent
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')

def child(args, cwd=None):
    env = dict(os.environ)
    env.update({k: '1' for k in THREADS})
    start = time.monotonic()
    p = subprocess.Popen(list(map(str,args)), cwd=cwd, env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, start_new_session=True)
    try:
        out, err = p.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL); p.communicate()
        raise RuntimeError('INCOMPLETE: fixed 60-second direct child guard')
    if p.returncode:
        raise RuntimeError(f'child failed ({p.returncode}): {err}')
    return {'seconds': round(time.monotonic()-start,6), 'stdout':out,
            'stderr':err, 'peak_child_rss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}

def record(prefix):
    fs=[]
    for line in Path(str(prefix)+'-interfaces.txt').read_text().splitlines():
        v=list(map(int,line.split()))
        if len(v)!=12: raise RuntimeError('interface encoding')
        fs.append({'flag':v[0], 'T_rows':v[1:4], 'SY_rows':v[4:6], 'Q_ranks_X':v[6:12]})
    if len({json.dumps(x,sort_keys=True) for x in fs}) != len(fs):
        raise RuntimeError('duplicate interface')
    counts=[]
    for line in Path(str(prefix)+'-counts.txt').read_text().splitlines():
        v=line.split();counts.append([v[0],*map(int,v[1:])])
    return {'complete':True,'interfaces':sorted(fs,key=lambda x:json.dumps(x,sort_keys=True)), 'counts':counts}

def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    runs={}; binary=a.out.resolve()/'census'; prefix=a.out.resolve()/'native'
    runs['build']=child(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',ROOT/'census.cpp','-o',binary])
    runs['native']=child([binary,prefix]);data=canonical(record(prefix));(a.out/'record.json').write_bytes(data)
    result={'complete':True,'guard_seconds':60,'one_intensive_child_at_a_time':True,'native_threads':1,
            'python_optimized':not __debug__,'record_bytes':len(data),'record_sha256':hashlib.sha256(data).hexdigest(),'runs':runs}
    (a.out/'run.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

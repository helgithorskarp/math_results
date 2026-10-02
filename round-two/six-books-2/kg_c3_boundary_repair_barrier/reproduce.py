"""Cold exact replay of boundary repair and all admissible promotion completions."""
from pathlib import Path
from itertools import combinations
import argparse,hashlib,json,os,resource,subprocess,sys,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import model

def strict_json(path):
    def unique(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('duplicate JSON key')
            result[key]=value
        return result
    return json.loads(Path(path).read_text(),object_pairs_hook=unique)

def validate_parents(parents):
    if type(parents) is not list or len(parents)!=28:raise ValueError('complete28 parent list')
    seen=set()
    for r in parents:
        if type(r) is not dict or set(r)!={'index','weight','J','P','D'}:raise ValueError('parent fields')
        if type(r['index']) is not int or not 0<=r['index']<305874 or type(r['weight']) is not int or r['weight']!=6:
            raise ValueError('parent index/weight')
        for key,size,high in [('J',3,7),('P',4,35),('D',9,35)]:
            a=r[key]
            if type(a) is not list or len(a)!=size or any(type(v) is not int or not 0<=v<high for v in a) or a!=sorted(set(a)):
                raise ValueError('strict parent recipe')
        key=tuple(tuple(r[k]) for k in ['J','P','D'])
        if key in seen:raise ValueError('duplicate parent recipe')
        seen.add(key)

def mathematical_summary(work):
    expected=strict_json(HERE/'EXPECTED.json')
    outputs={}
    for name,filename in [('cover','cover-summary.json'),('direct','direct-summary.json'),
                          ('pool','pool-summary.json'),('completion','completion-summary.json')]:
        actual=strict_json(work/filename)
        subset={key:actual[key] for key in expected[name]}
        if subset!=expected[name]:raise ValueError('frozen mathematical output differs: '+name)
        outputs[name]=subset
    if hashlib.sha256((work/'optimal.txt').read_bytes()).hexdigest()!=expected['native_optimal_stream_sha256']:
        raise ValueError('complete native optimum inventory differs from frozen hot stream')
    return outputs

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--optimized',action='store_true')
    args=parser.parse_args();work=args.work.resolve()
    if work==HERE or HERE in work.parents:raise ValueError('generated work must be outside public source')
    if work.exists() and any(work.iterdir()):raise ValueError('use an EMPTY work directory')
    work.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();expected=strict_json(HERE/'EXPECTED.json')
    parents=strict_json(HERE/'PARENTS.json');validate_parents(parents)
    if hashlib.sha256((HERE/'PARENTS.json').read_bytes()).hexdigest()!=expected['parent_fixture_sha256']:
        raise ValueError('frozen complete boundary recipes changed')
    # The separately imported census supplies completeness of this compact list.
    fixture=(HERE/'primary21.rows').read_text().splitlines()
    if len(fixture)!=21 or any(len(line)!=21 or set(line)-{'0','1'} for line in fixture):
        raise ValueError('primary21 binary row encoding')
    sets=[{v for v,value in enumerate(line) if value=='1'} for line in fixture]
    baseline=model.literal_summary(sets)
    if baseline['edges']!=93 or baseline['violations'] or max(baseline['red_pages'])!=3 or max(baseline['blue_pages'])!=6:
        raise ValueError('primary21 baseline')
    environment=os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:environment[key]='1'
    python=[sys.executable]+(['-O'] if args.optimized else [])
    commands=[['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic',str(HERE/'direct.cpp'),'-o',str(work/'direct')],
              python+[str(HERE/'cover.py'),str(work)],
              [str(work/'direct'),str(work/'parents.txt'),str(work/'optimal.txt'),str(work/'pools.txt')],
              python+[str(HERE/'pools.py'),str(work)],
              python+[str(HERE/'complete.py'),str(work)]]
    for i,command in enumerate(commands):
        result=subprocess.run(command,env=environment,capture_output=True,text=True,timeout=30)
        (work/('phase-'+str(i)+'.stdout')).write_text(result.stdout)
        (work/('phase-'+str(i)+'.stderr')).write_text(result.stderr)
        result.check_returncode()
        if i==0 and result.stderr:raise ValueError('compiler warnings')
        if i==2:(work/'direct-summary.json').write_text(json.dumps(json.loads(result.stdout),indent=2)+'\n')
    mathematical=mathematical_summary(work)
    (work/'mathematical-summary.json').write_text(json.dumps(mathematical,indent=2,sort_keys=True)+'\n')
    report=dict(status='COMPLETE_COLD_BOUNDARY_REPAIR_REPLAY',seconds=time.monotonic()-start,
                primary21=dict(edges=93,max_red_pages=3,max_blue_pages=6),
                optimized_python=args.optimized,threads=1,child_guard_seconds=30,
                soft_phase_seconds=25,peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                python=sys.version.split()[0],
                source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.iterdir() if p.is_file()},
                mathematical_summary_sha256=hashlib.sha256((work/'mathematical-summary.json').read_bytes()).hexdigest(),
                trust='Same-author distinct cover/direct/Gray algorithms; written bridges unformalized; predecessor9337 supplies complete boundary list.')
    (work/'replay-summary.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()

"""Finite serial replay; each math child has a fixed20s wall guard, no solver."""
import argparse,hashlib,json,os,pathlib,resource,subprocess,sys,time
from literal import need,digest
HERE=pathlib.Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',required=True);ap.add_argument('--result',required=True);args=ap.parse_args()
    root=pathlib.Path(args.work).resolve();root.mkdir(parents=True,exist_ok=False)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.update({s:'1' for s in THREADS});times=[];modes=[];start=time.monotonic()
    def child(mode,script,argv):
        cmd=[sys.executable]+(['-O'] if mode else [])+[str(HERE/script)]+list(map(str,argv));begin=time.monotonic()
        try:proc=subprocess.run(cmd,env=env,capture_output=True,timeout=20)
        except subprocess.TimeoutExpired as e:
            raise RuntimeError('INCOMPLETE: fixed20s guard in '+script+'; no absence conclusion, no retry') from e
        elapsed=time.monotonic()-begin;times.append(dict(mode='optimized' if mode else 'normal',script=script,seconds=elapsed))
        need(proc.returncode==0,'child failed: '+script+': '+proc.stderr.decode()[-2500:])
        result=json.loads(proc.stdout);print(json.dumps(dict(progress=len(times),script=script,mode=mode,seconds=round(elapsed,4))),flush=True);return result
    for mode in (0,1):
        work=root/('optimized' if mode else 'normal');work.mkdir();cover=work/'cover.json';cores=work/'cores.json';allcores=work/'all-cores.json'
        output={};output['cover']=child(mode,'cover.py',['--output',cover]);output['cover_check']=child(mode,'cover_check.py',['--input',cover,'--cores',cores])
        output['extension']=child(mode,'extension.py',['--cover',cover,'--cores',cores,'--output',allcores]);records=[];checks=[];proposal=[]
        partitions=[(lo,min(lo+40,490)) for lo in range(0,490,40)]+[(490,515)]
        for lo,hi in partitions:
            path=work/f'allocation-{lo}-{hi}.json';proposal.append(child(mode,'allocate.py',['--cores',allcores,'--lo',lo,'--hi',hi,'--output',path]));checks.append(child(mode,'allocation_check.py',['--input',path,'--cores',allcores,'--lo',lo,'--hi',hi]));records.extend(json.load(open(path)))
        output['allocation']=proposal;output['allocation_check']=checks;output['controls']=[]
        for part in ('degrees','budgets','allocations','cover-damage','allocation-damage'):
            output['controls'].append(child(mode,'controls.py',['--part',part,'--cover',cover,'--data',work/'allocation-0-40.json','--cores',allcores,'--lo',0,'--hi',40]))
        corpus=work/'whole-allocation.json';corpus.write_text(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n')
        hist={};row_costs=0;casehist={};elementary={};bounds={}
        for r in records:
            label='/'.join(map(str,r['core'][:2]));casehist[label]=casehist.get(label,0)+1;row_costs+=len(r['rows'])
            for container,key in ((elementary,r['elementary_lower']),(bounds,r['lower'])):
                container.setdefault(label,{})[str(key)]=container.setdefault(label,{}).get(str(key),0)+1
            for leaf in r['residual']:hist[str(leaf['minimum_missing'])]=hist.get(str(leaf['minimum_missing']),0)+1
        output['whole_allocation']=dict(cases=len(records),actual_row_costs=row_costs,case_histogram=casehist,elementary_lower_histogram=elementary,allocated_lower_histogram=bounds,residual_minimum_histogram=hist,record_sha256=digest(records),file_sha256=hashlib.sha256(corpus.read_bytes()).hexdigest(),private_bytes=corpus.stat().st_size,residual_core_cases=sum(r['lower']<=r['cap'] for r in records),actual_residual_row_choices=sum(r['row_choices'] for r in records))
        output['whole_files']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (cover,cores,allcores,corpus)};modes.append(output)
    need(modes[0]==modes[1],'whole normal/optimized records or private data differ')
    result=dict(schema=1,actual_agent='six-reviewer-4',role='independent mathematical reviewer',python=sys.version.split()[0],fixed_child_wall_guard_seconds=20,thread_environment={s:'1' for s in THREADS},serial_child_count=len(times),whole_normal_optimized_equal=True,elapsed_seconds=time.monotonic()-start,maximum_child_seconds=max(t['seconds'] for t in times),peak_children_rss_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,mathematical_records=modes[0],all_child_times=times)
    pathlib.Path(args.result).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(complete=True,result=args.result,elapsed_seconds=result['elapsed_seconds'],maximum_child_seconds=result['maximum_child_seconds'],serial_child_count=len(times),private_whole_equal=True)),flush=True)
if __name__=='__main__':main()

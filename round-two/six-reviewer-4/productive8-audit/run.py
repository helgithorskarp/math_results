"""Finite source-only normal/-O replay; each serial math child has fixed20s guard."""
import argparse,hashlib,json,os,pathlib,resource,subprocess,sys,time
HERE=pathlib.Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
def need(ok,why):
    if not ok:raise ValueError(why)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',required=True);ap.add_argument('--result',required=True);args=ap.parse_args();root=pathlib.Path(args.work).resolve();root.mkdir(parents=True,exist_ok=False);times=[];modes=[];start=time.monotonic();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.update({s:'1'for s in THREADS})
    def child(mode,script,argv):
        cmd=[sys.executable]+(['-O']if mode else [])+[str(HERE/script)]+list(map(str,argv));begin=time.monotonic()
        try:r=subprocess.run(cmd,env=env,capture_output=True,timeout=20)
        except subprocess.TimeoutExpired as e:raise RuntimeError('INCOMPLETE fixed20s child guard, no absence conclusion or retry: '+script)from e
        elapsed=time.monotonic()-begin;times.append(dict(mode=mode,script=script,seconds=elapsed));need(r.returncode==0,'child failed '+script+': '+r.stderr.decode()[-2000:]);print(json.dumps(dict(progress=len(times),mode=mode,script=script,seconds=round(elapsed,4))),flush=True);return json.loads(r.stdout)
    for mode in (0,1):
        work=root/('optimized'if mode else 'normal');work.mkdir();out={};out['base']=child(mode,'base.py',['--output',work/'base.json']);out['base_check']=child(mode,'base_check.py',['--input',work/'base.json']);out['odd']=child(mode,'odd.py',['--output',work/'odd.json']);out['odd_check']=child(mode,'odd_check.py',['--input',work/'odd.json']);out['binary']=child(mode,'binary.py',['--output',work/'binary.json']);out['binary_check']=child(mode,'binary_check.py',['--input',work/'binary.json','--odd',work/'odd.json']);out['raw']=[]
        for r in (1,3,4,5,7):
            A=child(mode,'raw.py',['--parent',r,'--method','odd','--output',work/f'raw-{r}-odd.bin']);B=child(mode,'raw.py',['--parent',r,'--method','physical','--output',work/f'raw-{r}-physical.bin']);need(A==B and (work/f'raw-{r}-odd.bin').read_bytes()==(work/f'raw-{r}-physical.bin').read_bytes(),'every raw physical phase pair');out['raw'].append(A)
        out['controls']=child(mode,'controls.py',['--work',work]);out['whole_files']={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in sorted(work.iterdir())};out['all_raw_original_pairs']=sum(r['raw_original_phase_pairs']for r in out['raw']);modes.append(out)
    need(modes[0]==modes[1],'whole normal/optimized math or file bytes differ')
    result=dict(actual_agent='six-reviewer-4',role='independent mathematical reviewer',python=sys.version.split()[0],fixed_child_wall_guard_seconds=20,numerical_threads={v:'1'for v in THREADS},serial_mathematical_children=len(times),elapsed_seconds=time.monotonic()-start,maximum_child_seconds=max(t['seconds']for t in times),peak_children_rss_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,whole_normal_optimized_equal=True,mathematical_records=modes[0],all_child_times=times)
    pathlib.Path(args.result).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(dict(complete=True,children=len(times),seconds=result['elapsed_seconds'],maximum_child=result['maximum_child_seconds'],whole_data_equal=True)),flush=True)
if __name__=='__main__':main()

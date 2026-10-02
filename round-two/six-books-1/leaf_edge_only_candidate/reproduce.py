"""Serial cold reproduction. Each numerical child has the unchanged90s guard."""
from pathlib import Path
import argparse,hashlib,json,os,resource,subprocess,sys,time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
STATE=Path('/scratch/research-team-sol61-six-20260929/state')
def barriers():
    if any((STATE/n).exists() for n in ('PAUSED','PAUSED.json')):raise RuntimeError('active pause barrier')
    h=STATE/'monitor/HANDOVER.json'
    if h.exists() and json.loads(h.read_text()).get('phase')!='completed':raise RuntimeError('incomplete handover')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);args=parser.parse_args()
    work=args.work.resolve()
    if work.exists() and any(work.iterdir()):raise RuntimeError('cold work directory must be empty')
    work.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[key]='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    prefix=[sys.executable]+(['-O'] if sys.flags.optimize else [])
    runs=[]
    def child(script,*options):
        barriers();start=time.monotonic()
        completed=subprocess.run(prefix+[str(script),*map(str,options)],capture_output=True,text=True,env=env,timeout=90)
        index=len(runs);(work/f'child-{index}.stdout').write_text(completed.stdout);(work/f'child-{index}.stderr').write_text(completed.stderr)
        runs.append({'script':str(script.relative_to(ROOT)),'arguments':list(map(str,options)),
                     'returncode':completed.returncode,'wall_seconds':time.monotonic()-start,
                     'cumulative_child_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
        (work/'run-receipt.json').write_text(json.dumps({'optimized':bool(sys.flags.optimize),'children':runs},indent=2)+'\n')
        if completed.returncode:raise RuntimeError('incomplete/rejected child '+str(script.name)+': '+completed.stderr[-1200:])
        print(json.dumps({'child':index,'script':script.name,'complete':True}),flush=True)
    for r in (0,1):
        for stage in (14,16):child(ROOT/'cross_edge_only/derive.py','--core',r,'--stage',stage,'--scratch',work)
        for stage in ('endpoints','rows','joins'):child(ROOT/'cross_edge_only/join.py','--core',r,'--stage',stage,'--scratch',work)
        child(ROOT/'cross_edge_only/check_join.py','--core',r,'--scratch',work)
    child(ROOT/'caseI_edge_only/projection.py','--out',work/'caseI-projections.json')
    child(ROOT/'caseI_edge_only/cycle_audit.py','--projection',work/'caseI-projections.json','--out',work/'caseI-cycle.json')
    child(HERE/'validate.py','--work',work)
    raw=(work/'RESULT.json').read_bytes();expected=HERE/'RESULTS.json'
    if expected.exists() and raw!=expected.read_bytes():raise RuntimeError('whole sealed mathematical result differs')
    print(json.dumps({'status':'REPRODUCTION_PASS','record_bytes':len(raw),'whole_record_sha256':hashlib.sha256(raw).hexdigest(),
                      'children':len(runs),'damaged_records_rejected':16}),flush=True)
if __name__=='__main__':main()

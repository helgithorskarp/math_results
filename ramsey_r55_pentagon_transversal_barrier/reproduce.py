"""Replay the complete cover certificate and incidence countermodel in scratch."""
from pathlib import Path
import hashlib,json,resource,subprocess,sys,time
src=Path(__file__).resolve().parent
if len(sys.argv)!=2:
    raise SystemExit('usage: python3 -B reproduce.py NEW_EXTERNAL_SCRATCH_DIRECTORY')
work=Path(sys.argv[1]).resolve()
if work.exists() or work==src.parent or src.parent in work.parents:
    raise SystemExit('scratch must be a new directory outside the repository')
work.mkdir(parents=True);start=time.perf_counter();timings={}
def run(name,args):
    t=time.perf_counter();r=subprocess.run(args,capture_output=True,text=True)
    timings[name]=time.perf_counter()-t
    if r.returncode:
        raise RuntimeError(str(args)+'\n'+r.stdout+'\n'+r.stderr)
    return r.stdout
compiler=run('compiler',['g++','--version']).splitlines()[0]
run('compile',['g++','-std=c++17','-O3','-Wall','-Wextra','-Wpedantic',str(src/'cover.cpp'),'-o',str(work/'cover')])
summary=run('generate',[str(work/'cover'),str(src/'control43.edges'),str(work/'control43.cover')])
if summary.strip()!='cycles 18535 nodes 408771 leaves 204386 status COMPLETE_21_COVER':
    raise ValueError('generator did not finish as expected')
a=json.loads(run('audit',[sys.executable,'-B',str(src/'audit.py'),str(src/'control43.edges')]))
c=json.loads(run('independent_cover_check',[sys.executable,'-B',str(src/'check_cover.py'),str(src/'control43.edges'),str(work/'control43.cover')]))
if {'audit':a,'cover':c}!=json.loads((src/'EXPECTED.json').read_text()):
    raise ValueError('exact expected output mismatch')
r={'status':'REPRODUCED_FINAL_INCIDENCE_BARRIER','final_gate_met':False,
   'global_good43_decisions':0,'compiler':compiler,'python':sys.version.split()[0],
   'seconds':time.perf_counter()-start,'timings':timings,
   'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
   'proof_bytes':(work/'control43.cover').stat().st_size,
   'proof_sha256':hashlib.sha256((work/'control43.cover').read_bytes()).hexdigest(),
   'expected_sha256':hashlib.sha256((src/'EXPECTED.json').read_bytes()).hexdigest()}
(work/'replay.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print(json.dumps(r,indent=2,sort_keys=True))

"""Regenerate and independently check all local assignments in fresh scratch."""
from pathlib import Path
import subprocess,sys,json,time,resource,hashlib
src=Path(__file__).resolve().parent
if len(sys.argv)!=2:
    raise SystemExit('usage: python3 -B reproduce.py NEW_EXTERNAL_SCRATCH_DIRECTORY')
work=Path(sys.argv[1]).resolve()
if work == src or src in work.parents or work.exists():
    raise SystemExit('scratch must be a new directory outside the source package')
work.mkdir(parents=True)
start=time.perf_counter()
def run(args):
    r=subprocess.run(args,capture_output=True,text=True)
    if r.returncode:
        raise RuntimeError(str(args)+'\n'+r.stdout+'\n'+r.stderr)
    return r.stdout
compiler=run(['g++','--version']).splitlines()[0]
run(['g++','-std=c++17','-O3','-Wall','-Wextra','-Wpedantic',str(src/'enumerate_cross.cpp'),'-o',str(work/'enumerate_cross')])
counts=run([str(work/'enumerate_cross'),str(work/'matrices.txt')])
if list(map(int,counts.split())) != [1,22,454,8138,103790,344282]:
    raise ValueError('generation count mismatch')
cross=json.loads(run([sys.executable,'-B',str(src/'check_cross.py'),str(work/'matrices.txt')]))
join=json.loads(run([sys.executable,'-B',str(src/'check_join.py')]))
expected=json.loads((src/'EXPECTED.json').read_text())
if {'cross':cross,'join':join} != expected:
    raise ValueError('exact evidence mismatch')
r={'status':'REPRODUCED_FAILED_COMPONENT_APPROACH_CHECKPOINT',
   'milestone_1_met':False,'global_terminal_decisions':0,
   'compiler':compiler,'python':sys.version.split()[0],
   'seconds':time.perf_counter()-start,
   'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
   'matrix_stream_bytes':(work/'matrices.txt').stat().st_size,
   'matrix_stream_sha256':hashlib.sha256((work/'matrices.txt').read_bytes()).hexdigest(),
   'expected_sha256':hashlib.sha256((src/'EXPECTED.json').read_bytes()).hexdigest()}
(work/'replay.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print(json.dumps(r,indent=2,sort_keys=True))

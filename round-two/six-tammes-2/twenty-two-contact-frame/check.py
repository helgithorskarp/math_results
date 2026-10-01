"""Recompute exact frame identities and every literal partition witness."""
from pathlib import Path
import json,os,signal
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):os.environ[name]='1'
import geometry,audit,replay
HERE=Path(__file__).resolve().parent
def check():
    result={'status':'CHECKED_COMPLETE_AUTHOR_REDUCTION','agent':'six-tammes-2','role':'researcher','geometry':geometry.derive(),'integer_audit':audit.derive(),'covers':[replay.replay(json.loads((HERE/('PLAN-'+mode+'.json')).read_text())) for mode in ('bad','g-half')]}
    if result!=json.loads((HERE/'EXPECTED.json').read_text()):raise ValueError('recomputed exact evidence differs from expected output')
    return result
if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda s,f:(_ for _ in ()).throw(TimeoutError('160-second full-check guard; incomplete')))
    signal.alarm(160)
    print(json.dumps(check(),indent=2))

"""Recompute exact algebra and every literal interval obligation."""
from pathlib import Path
import hashlib,json,os,signal
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):os.environ[name]='1'
import algebra,replay
HERE=Path(__file__).resolve().parent
def evidence():
    exact=algebra.derive()
    if exact!=json.loads((HERE/'ALGEBRA.json').read_text()):raise ValueError('recomputed exact algebra differs')
    return {'status':'CHECKED_COMPLETE_AUTHOR_STRIP_AND_CRITICAL_VERTEX_LEMMA',
            'agent':'six-tammes-2','role':'researcher','algebra_sha256':hashlib.sha256(json.dumps(exact,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'covers':[replay.replay(json.loads((HERE/f'PLAN-{mode}.json').read_text())) for mode in ('z-out','t-low','dz-68')]}
def check():
    out=evidence()
    if out!=json.loads((HERE/'EXPECTED.json').read_text()):raise ValueError('recomputed proof evidence differs')
    return out
if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda s,f:(_ for _ in ()).throw(TimeoutError('160-second full-check guard; incomplete')))
    signal.alarm(160)
    print(json.dumps(check(),indent=2))

"""Serial, bounded reproduction and meaningful corrupted-source controls."""
import hashlib,json,os,resource,subprocess,sys,tempfile,time
from pathlib import Path

HERE=Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
ENV=dict(os.environ,**{k:'1' for k in THREADS})
def run(path,opt):
    t=time.monotonic()
    p=subprocess.run([sys.executable,'-I','-B',*(['-O'] if opt else []),str(path),'--full'],
                     cwd=path.parent,env=ENV,capture_output=True,timeout=45)
    return p,time.monotonic()-t
def main():
    expected=json.loads((HERE/'SUMMARY.json').read_text())['record_sha256'];rows=[]
    raw=None
    for opt in (False,True):
        p,t=run(HERE/'audit.py',opt)
        digest=hashlib.sha256(p.stdout.rstrip(b'\n')).hexdigest()
        if p.returncode or digest!=expected:raise ValueError('whole independent baseline failed '+p.stderr.decode())
        if raw is not None and raw!=p.stdout:raise ValueError('entire normal/O bytes differ')
        raw=p.stdout;rows.append({'phase':'baseline','optimized':opt,'seconds':t,'sha256':digest})
    source=(HERE/'audit.py').read_text()
    damages=[
      ('integral normalization','return 9*(-a)**p*sum','return 8*(-a)**p*sum'),
      ('chain factor','return 9*(-a)**p*sum','return 9*sum'),
      ('full total domain','Q(403,100)*u/k','Q(4)*u/k'),
      ('missing extremal face','for k in range(9-p):','for k in range(8-p):'),
      ('missing Bernstein row','for i in range(9)]','for i in range(8)]'),
      ('inverse top degree','for x in range(i,9):','for x in range(i,8):'),
      ('interpolation normalization','v/100,u)','v/99,u)'),
      ('finite Taylor highest term','if I&J:continue','if I&J or J==255:continue'),
      ('Gaussian phase orientation','Q(16,130)','Q(15,130)'),
      ('signed positive control','ga(Q(1971,3584))','ga(Q(-1971,3584))'),
      ('order8 term','Q(7,2), Q(1)]','Q(7,2), Q(0)]'),
      ('offdiagonal loss','+70*n[1]','+80*n[1]'),
      ('penalty constant','-Q(39,5)*dm','-Q(8)*dm'),
      ('coarse E2 divisor','Q(14,27)*dr','Q(14,26)*dr'),
    ]
    with tempfile.TemporaryDirectory() as td:
        altered=Path(td)/'audit.py'
        for name,a,b in damages:
            if a not in source:raise ValueError('damage did not apply '+name)
            altered.write_text(source.replace(a,b,1))
            for opt in (False,True):
                p,t=run(altered,opt)
                changed=hashlib.sha256(p.stdout.rstrip(b'\n')).hexdigest()!=expected
                if p.returncode==0 and not changed:raise ValueError('accepted damaged mathematics '+name)
                rows.append({'phase':name,'optimized':opt,'seconds':t,
                             'rejected_by_mathematical_guard':p.returncode!=0,
                             'rejected_by_full_record_digest':changed})
    return {'normal_optimized_full_record_equal':True,'checks':len(rows),
            'source_damage_controls':len(damages),'record_sha256':expected,
            'guard_seconds':45,'threads':1,'serial':True,
            'peak_child_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'rows':rows}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))

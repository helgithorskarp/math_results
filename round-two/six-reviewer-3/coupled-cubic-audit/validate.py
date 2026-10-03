"""Serial meaningful mathematical damages; fixed45s/one native thread per child."""
import hashlib,json,os,subprocess,sys,tempfile,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ENV=dict(os.environ)
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:ENV[k]='1'
def child(root,optimized):
    cmd=[sys.executable]+(['-O'] if optimized else [])+[str(root/'audit.py')]
    return subprocess.run(cmd,capture_output=True,text=True,env=ENV,timeout=45)
def main():
    expected=json.loads((HERE/'SUMMARY.json').read_text());results=[]
    for opt in [False,True]:
        t=time.monotonic();r=child(HERE,opt)
        if r.returncode or json.loads(r.stdout)!=expected:raise ValueError('whole summary normal/optimized mismatch')
        results.append({'optimized':opt,'case':'baseline','seconds':time.monotonic()-t,'status':'PASS'})
    source=(HERE/'audit.py').read_text()
    damages=[
      ('missing_center',"Rc=sum(x*z for x,z in zip(X,fc))","Rc=R",'identity full_centered_Lagrange'),
      ('wrong_variance_count','fbar=sum(f)/8','fbar=sum(f)/7','identity quadratic_sum'),
      ('quartic_wrong7','7*V**2-8*S4+correction','6*V**2-8*S4+correction','identity free_quartic_with_mean_correction'),
      ('wrong_signed_feedback','pc*t**-4-w*uc*t**-1/12','pc*t**-4+w*uc*t**-1/12','identity combined_signed_cube'),
      ('wrong_fourth_normal','else -F(1,12)','else F(1,12)','full9 paired cubic sign'),
      ('bad_physical_determinant','F(1379,1000),F(987,4)','F(551,400),F(987,4)','strict budget refined_physical_det'),
      ('objective_as_physical_delta',"('original',F(247)),('refined',F(987,4))","('original',F(230)),('refined',F(987,4))",'strict budget original_stability_sqrt_D_gt31over2'),
      ('old_sqrt272_bound','Dcoef-F(31,2)**2','Dcoef-F(16)**2','strict budget original_stability_sqrt_D_gt31over2'),
    ]
    with tempfile.TemporaryDirectory(prefix='coupled-cubic-validation-') as temp:
        base=Path(temp);(base/'polys.py').write_bytes((HERE/'polys.py').read_bytes())
        for name,before,after,diagnostic in damages:
            if source.count(before)!=1:raise ValueError('ambiguous damage '+name)
            (base/'audit.py').write_text(source.replace(before,after))
            for opt in [False,True]:
                t=time.monotonic();r=child(base,opt)
                # wrong_count may first trip full_Lagrange? The Lagrange identity
                # holds for arbitrary centering; its mean correction uses /7.
                if name=='wrong_variance_count':diagnostic='identity full_variance_remainder'
                if r.returncode==0 or diagnostic not in r.stderr:raise ValueError('damage did not reject at intended mathematical guard '+name+': '+r.stderr)
                results.append({'optimized':opt,'case':name,'seconds':time.monotonic()-t,'status':'REJECTED','diagnostic':diagnostic})
    receipt={'status':'PASS','checks':len(results),'baseline_record':expected['record_sha256'],'serial':True,'guard_seconds':45,'native_threads':1,'runs':results}
    print(json.dumps(receipt,sort_keys=True))
if __name__=='__main__':main()

"""Bounded serial whole replays and substantive mathematical/schema rejects."""
import argparse,copy,hashlib,json,os,resource,shutil,subprocess,sys,time
from pathlib import Path


def main():
    p=argparse.ArgumentParser();p.add_argument('--scratch',required=True);p.add_argument('--summary',required=True);a=p.parse_args()
    root=Path(__file__).resolve().parent;work=Path(a.scratch).resolve()
    if work.exists():raise ValueError('fresh validation scratch required')
    work.mkdir(parents=True);cold=work/'cold'
    cold.mkdir()
    for name in ['field.py','intervals.py','check.py','refine.py','verify.py','EXPECTED.json','PRIMARY_SEAL.json']:
        shutil.copyfile(root/name,cold/name)
    env={**os.environ,**{k:'1'for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']}}
    expected=json.loads((root/'EXPECTED.json').read_text());canonical=json.dumps(expected,sort_keys=True,separators=(',',':')).encode()
    rows=[]
    def child(folder,script,mode,args,reason=None):
        cmd=[sys.executable,'-I','-B']+(['-O']if mode else [])+[str(folder/script),*map(str,args)]
        start=time.monotonic();r=subprocess.run(cmd,capture_output=True,text=True,timeout=45,env=env)
        if reason is None:
            if r.returncode or not json.loads(r.stdout)['complete']:raise ValueError('whole positive failed '+r.stderr)
        elif not r.returncode or reason not in r.stderr:raise ValueError('intended rejection failed '+str(args)+r.stderr)
        rows.append({'folder':'cold'if folder==cold else 'local','script':script,'optimized':mode,'args':[str(x).replace(str(work),'WORK').replace(str(root),'SOURCE')for x in args],
                     'positive':reason is None,'intended_rejection':reason,'seconds':round(time.monotonic()-start,6),
                     'peak_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'exit_code':r.returncode})
    for folder in [root,cold]:
        for mode in [False,True]:
            output=work/('whole-'+str(len(rows))+'.json');child(folder,'verify.py',mode,['--output',output])
            if output.read_bytes()!=canonical:raise ValueError('whole positive bytes differ')
    damages={'third-mean':'individual active normal','fourth-scale':'individual active normal',
             'unbalanced':'individual active normal','root-fourth':'all original root equations',
             'inward-sign':'original inward root equation','scalar-linear':'entire first-power coefficient',
             'dual-weight':'entire positive dual center payment'}
    for damage,reason in damages.items():
        for mode in [False,True]:child(root,'check.py',mode,['--damage',damage],reason)
    for damage,reason in [('underpay','entire fifth-normal coefficient enclosure'),('slack','uniform fifth inward surplus one')]:
        for mode in [False,True]:child(root,'refine.py',mode,['--damage',damage],reason)
    for damage in ['fourth-root','fifth-budget','wrong-type','missing-label']:
        fixture=copy.deepcopy(expected)
        if damage=='fourth-root':fixture['baseline']['all_nine_original_roots_eta0_to5'][4][4][0][0]='1'
        elif damage=='fifth-budget':fixture['tau_R_integer_coefficients'][0]-=1
        elif damage=='wrong-type':fixture['tau_16']=728.0
        else:fixture['all_nine_fifth_center_responses'].pop()
        path=work/(damage+'.json');path.write_text(json.dumps(fixture))
        for mode in [False,True]:child(root,'verify.py',mode,['--expected',path],'whole-record')
    source=(cold/'check.py').read_bytes();(cold/'check.py').write_bytes(source+b'# damaged source\n')
    for mode in [False,True]:child(cold,'verify.py',mode,[],'PREIMPORT source mismatch check.py')
    (cold/'check.py').write_bytes(source)
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer','complete':True,
            'positive_whole_normal_O_local_cold':4,'intended_rejections':len(rows)-4,
            'canonical_bytes':len(canonical),'canonical_sha256':hashlib.sha256(canonical).hexdigest(),
            'fixed_child_guard_seconds':45,'serial_children':True,'native_threads':1,
            'resource_limit_hit':False,'rows':rows}
    Path(a.summary).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='rows'},sort_keys=True))


if __name__=='__main__':main()

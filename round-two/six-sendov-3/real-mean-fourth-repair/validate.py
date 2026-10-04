"""Bounded serial local/cold, method, typed whole-fixture and source checks."""
from pathlib import Path
from hashlib import sha256
import argparse,copy,json,os,resource,shutil,subprocess,sys,time
HERE=Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
         'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
def manifest(folder):
    names=sorted(p.name for p in folder.iterdir() if p.name!='SHA256SUMS')
    (folder/'SHA256SUMS').write_text(''.join(sha256((folder/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names))
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--baseline',type=Path,default=HERE.parent/'optimal-cap-construction/EXPECTED.json')
    parser.add_argument('--scratch',type=Path,required=True)
    parser.add_argument('--summary',type=Path,required=True)
    args=parser.parse_args()
    work=args.scratch.resolve()
    if work==HERE or HERE in work.parents:raise ValueError('validation work root must be outside published source')
    if work.exists():raise ValueError('fresh validation directory required')
    work.mkdir(parents=True)
    baseline=work/'baseline.json';shutil.copyfile(args.baseline,baseline)
    env=dict(os.environ)
    for name in THREADS:env[name]='1'
    names=sorted(p.name for p in HERE.iterdir())
    cases=[]
    def relocated(label):
        folder=work/label;folder.mkdir()
        for name in names:shutil.copyfile(HERE/name,folder/name)
        return folder
    def run(label,folder,optimized=False,damage=None,should_reject=False,gate=None):
        cmd=[sys.executable,'-I','-B']
        if optimized:cmd+=['-O']
        cmd+=[str(folder/'verify.py'),'--baseline',str(baseline)]
        if damage:cmd+=['--damage',damage]
        t=time.monotonic()
        result=subprocess.run(cmd,cwd=work,env=env,text=True,capture_output=True,timeout=45)
        seconds=time.monotonic()-t
        (work/(label+'.stdout')).write_text(result.stdout)
        (work/(label+'.stderr')).write_text(result.stderr)
        diagnostic=result.stderr.strip().splitlines()[-1] if result.stderr.strip() else None
        if should_reject:
            if result.returncode==0 or (gate and gate not in result.stderr):
                raise ValueError('required rejection or intended gate failed: '+label)
            whole=None
        else:
            if result.returncode:raise ValueError('positive whole check failed: '+label+' '+str(diagnostic))
            whole=json.loads(result.stdout)
            if not whole['complete']:raise ValueError('incomplete positive '+label)
        cases.append({'label':label,'optimized':optimized,'intended_reject':should_reject,
            'exit_code':result.returncode,'seconds':seconds,
            'intended_gate':gate,'diagnostic_last_line':diagnostic,'whole_output':whole})
        args.summary.parent.mkdir(parents=True,exist_ok=True)
        args.summary.write_text(json.dumps({'complete':False,'completed_cases':cases},indent=2)+'\n')
        print(label,'required rejection' if should_reject else 'whole positive',round(seconds,4),flush=True)
    damage_gates={
        'unbalanced_mean':'ENTIRE balanced eta² critical mean',
        'freeze_third':'ALL4 actual third normals repaired',
        'omit_pair_compensation':'ALL4 actual third normals repaired',
        'drop_quadratic_pair':'ALL4 active actual normals through4',
        'wrong_cost_linear':'ENTIRE repaired quadratic fourth cost',
        'wrong_dual':'ENTIRE repaired scalar/positive-dual elimination',
        'outward_ninth':'ENTIRE epsilon9 inward primitive',
        'wrong_positivity':'intentional strict physical-sign damage'}
    fixture_names=('mean_linear_sign','dropped_root_coefficient','boolean_as_integer','sign_as_number')
    for optimized in (False,True):
        suffix='O' if optimized else 'N'
        run('local-'+suffix,HERE,optimized)
        run('cold-'+suffix,relocated('cold-'+suffix),optimized)
        for damage,gate in damage_gates.items():
            run('math-'+damage+'-'+suffix,HERE,optimized,damage,True,gate)
        for defect in fixture_names:
            folder=relocated('fixture-'+defect+'-'+suffix)
            value=json.loads((folder/'EXPECTED.json').read_text())
            if defect=='mean_linear_sign':
                value['constants']['L'][0][1][0]='0'
            elif defect=='dropped_root_coefficient':
                if not value['whole_all_nine_original_roots_epsilon0to9'][3]['all_root_coefficients'][8][0]:
                    raise ValueError('intended root-coefficient damage is empty')
                value['whole_all_nine_original_roots_epsilon0to9'][3]['all_root_coefficients'][8][0]=[]
            elif defect=='boolean_as_integer':
                value['schema']=True
            elif defect=='sign_as_number':
                value['positive_rational_signs'][0]['rational_lower']=1
            (folder/'EXPECTED.json').write_text(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n')
            manifest(folder)
            run('fixture-'+defect+'-'+suffix,folder,optimized,should_reject=True,gate='WHOLE CANONICAL')
    for optimized in (False,True):
        label='preimport-source-'+('O' if optimized else 'N')
        folder=relocated(label)
        with (folder/'means.py').open('a') as f:f.write('\n# intentional changed-source rejection\n')
        run(label,folder,optimized,should_reject=True,gate='SOURCE SHA256 means.py')
    summary={'agent':'six-sendov-3','role':'researcher','complete':True,
        'python':sys.version.split()[0],
        'math_source_hashes':{n:sha256((HERE/n).read_bytes()).hexdigest()
            for n in ('arithmetic.py','series.py','means.py','verify.py','EXPECTED.json')},
        'native_threads':{n:env[n] for n in THREADS},
        'maximum_simultaneous_mathematical_children':1,'per_child_timeout_seconds':45,
        'positive_runs':sum(not r['intended_reject'] for r in cases),
        'intended_rejections':sum(r['intended_reject'] for r in cases),
        'peak_child_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        'all_cases':cases,'analytic_bridges_unformalized':True,'independent_review':False}
    args.summary.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('all_cases','math_source_hashes','native_threads')},indent=2),flush=True)
if __name__=='__main__':main()

"""Serial source-only45s mathematical children; all six native thread variables1."""
from pathlib import Path
import subprocess,sys,tempfile,json,time,hashlib,os,copy,resource

def run(argv,cwd,expected_code):
    start=time.monotonic()
    p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=45)
    if (p.returncode==0)!=expected_code:
        raise ValueError('unexpected child result '+str(argv)+' '+p.stderr[:600])
    return {'args':argv[1:],'expected_success':expected_code,'actual_returncode':p.returncode,
            'seconds':round(time.monotonic()-start,6),'stdout':p.stdout.strip(),
            'rejection_tail':p.stderr.strip().splitlines()[-1:] if p.returncode else []}

def main():
    here=Path(__file__).resolve().parent
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
        os.environ[name]='1'
    reports=[]
    # Cold means a directory containing only the three kernels and exact own fixture.
    with tempfile.TemporaryDirectory(prefix='receiving-source-') as tmp:
        cold=Path(tmp)
        for name in ['core.py','controls.py','check.py','EXPECTED.json']:
            (cold/name).write_bytes((here/name).read_bytes())
        expected=json.loads((here/'EXPECTED.json').read_text())
        for opt in ([],['-O']):
            base=[sys.executable,'-B']+opt
            for where in [here,cold]:
                reports.append(run(base+['check.py'],where,True))
            for damage in ['old_rms','old_tail','drop_d3','flip_cubic']:
                reports.append(run(base+['core.py',damage],cold,False))
            reports.append(run(base+['-c',"import controls; controls.build('drop_d3')"],cold,False))
            bads=[]
            r=copy.deepcopy(expected);del r['core']['maps']['universal_joint_cubic_variance'];bads.append(r)
            r=copy.deepcopy(expected);r['core']['margins']['physical_square_det']='0';bads.append(r)
            r=copy.deepcopy(expected);r['core']['all9_phase_maps']['4'].pop('3');bads.append(r)
            r=copy.deepcopy(expected);r['core']['endpoint']=True;bads.append(r)
            r=copy.deepcopy(expected);r['controls'][2]['primitive'][6][0]='0';bads.append(r)
            r=copy.deepcopy(expected);r['controls']=r['controls'][:-1];bads.append(r)
            for i,r in enumerate(bads):
                (cold/'bad.json').write_text(json.dumps(r))
                reports.append(run(base+['check.py','bad.json'],cold,False))
            (cold/'bad.json').write_text('{"core":{},"core":{},"controls":[]}')
            reports.append(run(base+['check.py','bad.json'],cold,False))
    hashes={n:hashlib.sha256((here/n).read_bytes()).hexdigest()for n in ['core.py','controls.py','check.py','EXPECTED.json','PROOF.md','validate.py']}
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'python':sys.version,'fixed_child_guard_seconds':45,'serial_children':True,
            'native_threads':1,'reports':reports,'sealed_candidate_hashes':hashes,
            'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (here/'PRIMARY_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'children':len(reports),'peak_child_rss_kib':result['peak_child_rss_kib'],
                      'maximum_child_seconds':max(x['seconds']for x in reports)},sort_keys=True))

if __name__=='__main__':main()

"""Cold full-record agreement and bounded semantic defects, serial only."""
from pathlib import Path
import sys,subprocess,tempfile,shutil,json,os,hashlib,time

def main():
    src=Path(__file__).resolve().parent
    names=['ring.py','certificates.py','bridges.py','written_minima.py','check.py']
    sealed={n:hashlib.sha256((src/n).read_bytes()).hexdigest()for n in names}
    env=os.environ.copy()
    for n in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[n]='1'
    records=[];reference=None
    with tempfile.TemporaryDirectory(prefix='complete-double-audit-')as temporary:
        root=Path(temporary)
        for n in names:shutil.copyfile(src/n,root/n)
        def run(label,opt=False,expected=None):
            nonlocal reference
            output=root/'record.json'
            if output.exists():output.unlink()
            start=time.monotonic();cmd=[sys.executable,'-I','-B']+(['-O']if opt else[])+[str(root/'check.py'),str(output)]
            p=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=45)
            if expected is None:
                if p.returncode:raise ValueError(label+': '+p.stderr[-1200:])
                raw=output.read_bytes();data=json.loads(raw)
                if reference is None:reference=(raw,data)
                if (raw,data)!=reference:raise ValueError('entire parsed and byte record disagreement')
                summary=json.loads(p.stdout.splitlines()[-1]);peak=summary['peak_RSS_KiB']
            else:
                if p.returncode!=1 or output.exists()or ('ValueError: '+expected)not in p.stderr or 'SyntaxError' in p.stderr:
                    raise ValueError(label+': semantic rejection missing '+p.stderr[-500:])
                peak=None
            records.append({'name':label,'optimization':opt,'expected_semantic_rejection':expected,'exit':p.returncode,'seconds':round(time.monotonic()-start,6),'peak_RSS_KiB':peak})
            print(label,'PASS',flush=True)
        for n,opt in [('local-normal',False),('local-optimized',True),('cold-normal',False),('cold-optimized',True)]:run(n,opt)
        defects=[('wrong-original-derivative','ring.py','scale(v,8)for v in want','scale(v,7)for v in want','whole original derivative identity'),
          ('wrong-J-minus','certificates.py','(1,0,0):-612','(1,0,0):-611','whole rational J polynomial identity'),
          ('wrong-u-cap','certificates.py','kappa=9 if side==1 else 16','kappa=10 if side==1 else 16','complete independently reconstructed written minima'),
          ('wrong-h-factor','certificates.py','(i-10,r,v)','(i-9,r,v)','whole positive-q0 reduced identity and census'),
          ('wrong-q-factor','certificates.py','(i-10,j,k)','(i-9,j,k)','whole real-q0 reverse factor identity'),
          ('wrong-range-endpoint','bridges.py','Q(21,100)-Q(1,8)','Q(22,100)-Q(1,8)','all written rational range margins'),
          ('wrong-Hermite-constant','bridges.py','(0,3,-6912)','(0,3,-6911)','every whole Hermite minor'),
          ('wrong-quartic-corner','certificates.py','Q(3,32)-Q(5,564)','Q(1,32)-Q(5,564)','complete strict coefficient positivity')]
        for index,(name,file,old,new,expected)in enumerate(defects):
            text=(src/file).read_text()
            if text.count(old)!=1:raise ValueError('unique semantic defect selector')
            damaged=text.replace(old,new);compile(damaged,file,'exec');(root/file).write_text(damaged)
            run(name,index%2==1,expected);shutil.copyfile(src/file,root/file)
    if {n:hashlib.sha256((src/n).read_bytes()).hexdigest()for n in names}!=sealed:raise ValueError('sealed primary source changed')
    raw=reference[0];data=reference[1]
    summary={'agent':'six-reviewer-1','role':'independent mathematical reviewer','python':sys.version.split()[0],
      'source_hashes':sealed,'whole_record_bytes':len(raw),'whole_record_sha256':hashlib.sha256(raw).hexdigest(),
      'all_four_entire_parsed_and_byte_records_equal':True,'positive_children':4,'semantic_rejections':len(defects),
      'serial_math_children':1,'fixed_child_timeout_seconds':45,'all_six_native_thread_environment_variables':1,
      'records':records,'tensor_minima':[z['unscaled_min']for z in data['boxes']],
      'quartic_minima':[z['minimum']for z in data['quartic_boxes']],
      'all10492_controls_positive_and_all_inverse_identities':True,'quantitative_refinements':data['quantitative_refinements']}
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items()if k not in ['records','source_hashes','tensor_minima','quartic_minima']},sort_keys=True))

if __name__=='__main__':main()

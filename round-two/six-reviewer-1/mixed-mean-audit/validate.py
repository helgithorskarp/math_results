"""Four whole-record replays and resealed mathematical adverse gates."""
from pathlib import Path
import sys,subprocess,tempfile,shutil,os,json,hashlib,time
here=Path(__file__).resolve().parent;dest=Path(sys.argv[1]).resolve();dest.mkdir(parents=True,exist_ok=True)
env=os.environ.copy()
for n in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:env[n]='1'
rows=[];whole=None
def command(folder,opt,args):return [sys.executable,'-I','-B']+(['-O']if opt else[])+[str(folder/'verify.py'),*args]
def positive(folder,opt,label):
    global whole
    out=dest/label;t=time.monotonic();p=subprocess.run(command(folder,opt,['all',str(out)]),capture_output=True,text=True,env=env,timeout=120)
    if p.returncode:raise ValueError('whole replay '+label+' '+p.stderr)
    data=(out/'whole.json').read_bytes()
    if whole is None:whole=data
    if data!=whole:raise ValueError('four complete regenerated records disagree')
    rows.append({'name':label,'optimized':opt,'whole_bytes_equal':True,**json.loads(p.stdout)})
def copy(folder):
    for p in here.iterdir():
        if p.is_file():shutil.copyfile(p,folder/p.name)
def negative(folder,opt,label,key,gate):
    out=dest/(label+'.json');args=['stage',key,str(out),str(dest/'local-normal')]
    p=subprocess.run(command(folder,opt,args),capture_output=True,text=True,env=env,timeout=45)
    if p.returncode==0 or gate not in p.stderr:raise ValueError('intended adverse mathematical gate '+label+' '+p.stderr)
    rows.append({'name':label,'optimized':opt,'returncode':p.returncode,'intended_gate':gate,'rejected':True})
for opt in [False,True]:positive(here,opt,'local-'+('optimized'if opt else'normal'))
with tempfile.TemporaryDirectory(prefix='mixed-mean-cold-')as tmp:
    folder=Path(tmp);copy(folder)
    for opt in [False,True]:positive(folder,opt,'cold-'+('optimized'if opt else'normal'))
faults=[
 ('seventh-repair','family.py','s7=-Q(2,49)','s7=-Q(3,49)','root-3-0','all individual active normals through degree nine'),
 ('ninth-center','family.py','n9=-E(Q(35,81))','n9=-E(Q(36,81))','root-3-0','all individual active normals through degree nine'),
 ('ninth-scale','family.py','s9=-E(Q(34849,42336))','s9=-E(Q(34850,42336))','root-3-0','all individual active normals through degree nine'),
 ('mixed-t4','family.py','b4=-Q(2,49)','b4=-Q(3,49)','root-3-0','complete individual mixed tenth polynomial and t4 cancellation'),
 ('root-mixed-coefficient','root.py','Q(83,8232)','Q(84,8232)','root-3-0','complete individual mixed tenth polynomial and t4 cancellation'),
 ('binomial-fifth','scalar.py','co*=Q(-(2*k-1),2*k)','co*=Q(-(2*k-1),2*k) if k!=5 else Q(-10,10)','scalar-0','complete binomial inverse-square-root equation'),
 ('physical-pair-variance','scalar.py','Q(3,4)),n=n)','Q(1,2)),n=n)','scalar-0','all complete physical scalar routes agree'),
 ('physical-multiplicity','scalar.py','F=sa(ss(U,6),S','F=sa(ss(U,5),S','scalar-0','all complete physical scalar routes agree'),
 ('motion-sign','controls.py','sgn*motionB','-sgn*motionB','controls','whole mixed motion linear term'),
 ('mean-threshold','controls.py','27*b3-a3','26*b3-a3','controls','strict original sign sharp_threshold_below27')]
for label,file,old,new,key,gate in faults:
    with tempfile.TemporaryDirectory(prefix='mixed-mean-fault-')as tmp:
        folder=Path(tmp);copy(folder);s=(folder/file).read_text()
        if old not in s:raise ValueError('exact adverse location absent '+label)
        (folder/file).write_text(s.replace(old,new,1))
        seal=json.loads((folder/'PRIMARY_SEAL.json').read_text())
        seal['files']={n:hashlib.sha256((folder/n).read_bytes()).hexdigest()for n in seal['files']}
        (folder/'PRIMARY_SEAL.json').write_text(json.dumps(seal))
        for opt in [False,True]:negative(folder,opt,label+('-optimized'if opt else'-normal'),key,gate)
with tempfile.TemporaryDirectory(prefix='mixed-mean-unsealed-')as tmp:
    folder=Path(tmp);copy(folder);p=folder/'field.py';p.write_text('raise RuntimeError("DEFECTIVE MATHEMATICS IMPORTED")\n'+p.read_text())
    for opt in [False,True]:negative(folder,opt,'preimport-seal-'+str(opt),'root-3-0','source seal before import')
summary={'agent':'six-reviewer-1','role':'independent mathematical reviewer','four_entire_records_equal':True,'mathematical_defects_rejected':20,'preimport_seal_rejections':2,'native_threads':1,'maximum_concurrent_CPU_children':1,'per_mathematical_child_timeout_seconds':45,'resource_limit_hit':False,'records':rows}
(dest/'VALIDATION.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items()if k!='records'}))

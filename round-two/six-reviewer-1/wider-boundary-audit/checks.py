"""Portable serial semantic-damage and fixture-integrity checks."""
from pathlib import Path
import argparse,json,os,resource,shutil,subprocess,sys,tempfile,time
import core

def main():
    root=Path(__file__).resolve().parent;env=dict(os.environ)
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[key]='1'
    receipts=[]
    def run(cmd,expect,cwd=None):
        start=time.monotonic();p=subprocess.run([sys.executable,'-B','-O',*cmd],cwd=cwd,capture_output=True,text=True,env=env,timeout=45)
        core.need((p.returncode==0)==expect,'unexpected child result: '+p.stderr[-250:]);receipts.append({'expected_success':expect,'returncode':p.returncode,'wall_seconds':round(time.monotonic()-start,6)})
    with tempfile.TemporaryDirectory(prefix='wider-boundary-audit-')as tmp:
        cold=Path(tmp)
        for name in ['core.py','owned_centered.py','validate.py','EXPECTED.json']:shutil.copyfile(root/name,cold/name)
        run([str(cold/'validate.py')],True)
        original=(cold/'core.py').read_text()
        damage=[('sc(D,-5)','sc(D,-6)'),('expected=Q(487362179,8131200000);cut=Q(1,20)','expected=Q(487362179,8131200000);cut=Q(1,16)'),('expected=Q(32075187,73400320);cut=Q(3,7)','expected=Q(32075187,73400320);cut=Q(1,2)'),('b[4]=sc(pw(v,2),Q(3,32))','b[4]=sc(pw(v,2),Q(1,32))'),('Q(1,32)**2-Q(45,2)*e','Q(1,40)**2-Q(45,2)*e'),('r0=Q(4999,5000)','r0=Q(6399,6400)'),('tail-Q(7,200)','tail-Q(1,8)'),('41-(Q(619,97)+Q(9,500))**2','40-(Q(619,97)+Q(9,500))**2'),('Q((8-2*k)**2,8*k*(8-k))','Q((8-2*k)**2,4*k*(8-k))')]
        for old,new in damage:
            core.need(original.count(old)==1,'unique semantic change');(cold/'core.py').write_text(original.replace(old,new));run(['-c','import core;core.complete_build()'],False,cold)
        (cold/'core.py').write_text(original)
        base=json.loads((root/'EXPECTED.json').read_text());variants=[]
        def changed(name,fn):
            p=json.loads(json.dumps(base));fn(p);variants.append((name,json.dumps(p)))
        changed('boolean',lambda p:p.__setitem__('schema',True));changed('floating',lambda p:p.__setitem__('eta_endpoint',0.00004))
        changed('whole-stream',lambda p:p['polar']['streams']['mean']['coefficients'].pop());changed('sector',lambda p:p['sector']['complete_15_sector_integrals'].pop())
        changed('Bernstein',lambda p:p['radial_penalty_five']['blocks'][0]['whole_Bernstein_coefficients'][0].pop())
        changed('ordered-Hessian',lambda p:p['fresh_definition_level_controls']['whole_Gaussian_controls'][0]['whole_ordered_Hessian'].pop())
        variants.extend([('nonfinite','{"schema":NaN}'),('duplicate','{"schema":1,"schema":1}')])
        for name,text in variants:
            f=cold/(name+'.json');f.write_text(text);run([str(cold/'validate.py'),'--fixture',str(f)],False)
    print(json.dumps({'status':'PASS','agent':'six-reviewer-1','role':'independent mathematical reviewer','cold_optimized':True,'optimized_build_only_semantic_rejections':len(damage),'optimized_fixture_rejections':len(variants),'max_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'checks':receipts},sort_keys=True))
if __name__=='__main__':main()

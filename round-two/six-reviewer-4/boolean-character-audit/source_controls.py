"""Bounded optimized semantic source damages, isolated from sealed originals."""
import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path
from geometry import canonical,need

def checks(certificate,work):
    source=Path(__file__).resolve().parent;work.mkdir(parents=True,exist_ok=True);env=dict(os.environ)
    for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):env[k]='1'
    damages=[('reverse-character-classes','return int(x not in squares(p))','return int(x in squares(p))'),
             ('drop-scale-character-sign','oldbits[i]=newbits[j]^sign','oldbits[i]=newbits[j]'),
             ('wrong-common-phase','SIG=(0,0,0,1,1,1)','SIG=(0,1,0,1,0,1)'),
             ('wrong-retained-third-root','else (0,1,t)','else (0,1,(t+1)%103)')]
    results=[]
    for name,before,after in damages:
        d=work/name;d.mkdir(exist_ok=True)
        for n in('geometry.py','positive.py'):(d/n).write_bytes((source/n).read_bytes())
        text=(d/'geometry.py').read_text();need(text.count(before)==1,'one exact independent source mutation');(d/'geometry.py').write_text(text.replace(before,after))
        out=d/'unused.json';r=subprocess.run([sys.executable,'-O',str(d/'positive.py'),'--certificate',str(certificate.resolve()),'--start','0','--end','32','--output',str(out)],env=env,capture_output=True,timeout=10)
        need(r.returncode!=0 and b'ValueError' in r.stderr,'semantic source damage must fail by mathematical check, not timeout')
        results.append({'name':name,'optimized_semantic_rejection':True,'mutated_source_sha256':hashlib.sha256((d/'geometry.py').read_bytes()).hexdigest()})
    return {'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','isolated_optimized_source_damages':results,'count':len(results),'range':[0,32],'source_pin_or_expected_result_comparison_not_used_for_rejection':True,'original_sources_unmodified':True}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.write_bytes(canonical(checks(a.certificate,a.work)))

"""Six sequential required replays plus semantic rejection controls."""
from argparse import ArgumentParser
from copy import deepcopy
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
HERE=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise RuntimeError(message)

def main():
    p=ArgumentParser();p.add_argument('--scratch',type=Path,required=True);a=p.parse_args();a.scratch.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):env[key]='1'
    receipts=[];outputs={};started=time.monotonic()
    def run(name,optimized,extra=(),reject=False):
        command=[sys.executable]+(['-O'] if optimized else [])+['-B',str(HERE/(name+'.py'))]+list(extra)
        t=time.monotonic();job=subprocess.run(command,capture_output=True,text=True,env=env,timeout=20)
        need((job.returncode!=0) if reject else (job.returncode==0),('damaged evidence accepted' if reject else 'required replay failed')+': '+name+' '+job.stderr)
        receipts.append(dict(engine=name,optimized=optimized,rejection_control=reject,seconds=time.monotonic()-t,exit_code=job.returncode))
        return json.loads(job.stdout) if not reject else None
    for optimized in (False,True):
        for name in ('check','audit','controls'):
            out=a.scratch/(name+('-O' if optimized else '')+'.json')
            extra=['--output',str(out)]
            if name=='audit':extra+=['--scratch',str(a.scratch/('build-O' if optimized else 'build'))]
            outputs[name,optimized]=run(name,optimized,extra)
    for name in ('check','audit','controls'):need(outputs[name,False]==outputs[name,True],'normal/optimized replay differs')
    cert=json.loads((HERE/'certificate.json').read_text())
    damages=[('wrong_prime','copy_prime',5),('wrong_target','omitted_remainder9',3),('missing_resource','original_cofactors',cert['original_cofactors'][:-1]),('merged_nines','nine_cofactors',[9]),('wrong_additional','four_cofactor',24),('wrong_boundary','conditional_upper',109),('wrong_mass','other_resource_mass',145),('wrong_histogram','equality_histogram',[160,0,0,0,0,0,0,0,0,0]),('wrong_loss','equality_overlap_loss',0),('global_overclaim','global_L_min_8_improved',True)]
    for tag,key,value in damages:
        damaged=deepcopy(cert);damaged[key]=value;path=a.scratch/(tag+'.json');path.write_text(json.dumps(damaged))
        for optimized in (False,True):
            for name in ('check','audit'):
                extra=['--certificate',str(path)]
                if name=='audit':extra+=['--scratch',str(a.scratch/'damage-build')]
                run(name,optimized,extra,True)
    fixture=json.loads((HERE/'positive-tail.json').read_text())
    for tag in ('wrong_anchor_phase','missing_point','repeat_modulus','full_cover_overclaim'):
        damaged=deepcopy(fixture)
        if tag=='wrong_anchor_phase':damaged['classes'][0][0]=(damaged['classes'][0][0]+1)%damaged['classes'][0][1]
        elif tag=='missing_point':damaged['target_t'].pop()
        elif tag=='repeat_modulus':damaged['classes'][-1][1]=damaged['classes'][0][1]
        else:damaged['full_15120_cover_asserted']=True
        path=a.scratch/(tag+'.json');path.write_text(json.dumps(damaged))
        for optimized in (False,True):run('controls',optimized,['--fixture',str(path)],True)
    result=dict(agent='six-covering-1',role='researcher',utc=datetime.now(timezone.utc).isoformat(),required_replays=6,normal_optimized_agree=True,semantic_certificate_damages=len(damages),certificate_engine_mode_rejections=4*len(damages),positive_fixture_damages=4,fixture_mode_rejections=8,seconds=time.monotonic()-started,max_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,receipts=receipts,expected_sha256=hashlib.sha256((HERE/'expected.json').read_bytes()).hexdigest(),proof=outputs['check',False],audit=outputs['audit',False],positive=outputs['controls',False],independent_reviewer_verdict_claimed=False)
    (a.scratch/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('receipts','proof','audit','positive')}))
if __name__=='__main__':main()

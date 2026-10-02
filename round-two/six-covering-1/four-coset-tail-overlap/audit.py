"""Compile/replay the separate literal C++ auditor, with explicit checks."""
from argparse import ArgumentParser
import json
import os
from pathlib import Path
import subprocess
HERE=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise RuntimeError(message)

def main():
    p=ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');p.add_argument('--scratch',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args()
    # Independent fixed-domain validation; no producer/model imports.
    fixed={'schema':1,'candidate_period':720,'target_remainder4':0,'omitted_remainder9':6,'copy_prime':7,'original_cofactors':[d for d in range(2,721) if 720%d==0],'whole_copy_cofactors':[2,4],'selected_cofactors':[8,3,6,12,5,10,20],'nine_cofactors':[9,18,36],'four_cofactor':16,'tested_holes':111,'conditional_upper':110,'other_resource_mass':144,'joint_threshold':411,'equality_histogram':[40,20,20,30,15,15,10,5,5,0],'equality_union_extra_ceiling':85,'equality_overlap_loss':15,'global_L_min_8_improved':False,'tail_completion_asserted':False}
    need(json.loads(a.certificate.read_text())==fixed,'certificate domain or conclusion mismatch')
    a.scratch.mkdir(parents=True,exist_ok=True);exe=a.scratch/'literal-audit'
    env=os.environ.copy()
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):env[name]='1'
    build=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra',str(HERE/'audit.cpp'),'-o',str(exe)],capture_output=True,text=True,env=env,timeout=20)
    need(build.returncode==0,'audit compiler failed: '+build.stderr)
    replay=subprocess.run([str(exe.resolve())],capture_output=True,text=True,env=env,timeout=35)
    need(replay.returncode==0,'literal audit failed: '+replay.stderr)
    result=json.loads(replay.stdout);expected=json.loads((HERE/'expected.json').read_text())
    need(all(result.get(k)==v for k,v in expected.items()),'independent replay counters differ')
    extra={'raw_original_phase_families':16919,'literal_progression_points':146160,'original_equality_copy_phase_controls':111600}
    need(all(result.get(k)==v for k,v in extra.items()),'original physical controls differ')
    positive=json.loads((HERE/'positive-expected.json').read_text())
    need(all(result.get(k)==positive[k] for k in ('positive_template_first_demand','positive_template_first_group_capacity','positive_template_raw_pair_checks','positive_template_singleton_phase_checks')),'literal template obstruction counters differ')
    if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()

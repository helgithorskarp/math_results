"""Semantic adverse controls, serial and bounded, normal AND python -O."""
from pathlib import Path
from time import monotonic
import argparse
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

BASE=Path(__file__).resolve().parent
THREADS=['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
         'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']


def controls():
    start=monotonic();env=os.environ.copy();env.update({k:'1' for k in THREADS});env['PYTHONDONTWRITEBYTECODE']='1'
    original=json.loads((BASE/'CERTIFICATE.json').read_bytes());cases=[]
    def setcase(name,key,val,message):
        d=copy.deepcopy(original);d[key]=val;cases.append((name,d,message))
    setcase('omit signed mixed pivot compensation','mixed_pivot_multiplier',0,'ALL81 original bad-degree responses')
    setcase('reverse signed mixed pivot compensation','mixed_pivot_multiplier',-1,'ALL81 original bad-degree responses')
    setcase('wrong mixed gauge half factor','mixed_gauge_numerator',2,'complete good-total residual response')
    setcase('reverse sigma good compensation','sigma_gauge_numerator',1,'complete good-total residual response')
    setcase('omit original loop compensation','loop_gauge_numerator',0,'complete good-total residual response')
    setcase('omit actual empty loop from completion','empty_loop_multiplier',0,'ALL278 actual stochastic responses')
    setcase('erase actual empty row completion','empty_row_multiplier',0,'ALL278 actual stochastic responses')
    setcase('wrong mixed erasure coefficient','mixed_edge_numerator',-1,'complete mixed-edge residual response')
    d=copy.deepcopy(original);Q=[list(map(int,r.split())) for r in d['twice_inverse_rows']]
    d['twice_inverse_rows']=[' '.join(str(Q[j][i]) for j in range(81)) for i in range(81)]
    cases.append(('transpose incidence inverse orientation',d,'entries of'))
    d=copy.deepcopy(original);r=d['twice_inverse_rows'][-1].split();r[-1]=str(int(r[-1])+1)
    d['twice_inverse_rows'][-1]=' '.join(r);cases.append(('alter last original inverse entry',d,'entries of'))
    setcase('understate proper operator cost','proper_operator_cost_coefficient','99/10','proper operator cost bound')
    setcase('understate actual entry cost','actual_entry_cost_coefficient','1999/1000','actual entry cost bound')
    setcase('forget positive mixed trace entries','trace_support_edge_count',7885,'ALL good and potentially positive mixed')
    setcase('insufficient Frobenius trace coefficient','trace_coefficient',1360,'full Frobenius trace cost bound')
    setcase('unpaid wider local operator ball','local_radius_eta_denominator_power',11,'entire closed local ball strict NN sign')
    setcase('use proper dimension for actual lift norm','lift_operator_square',277,'actual E transpose E norm factor278')
    setcase('mix old and new center scales','eta','1/1152921504606846976','explicit SAME-carrier ordinary stronger-center')
    setcase('wrong M-unit actual operator coefficient','M_operator_cost_coefficient','139/12','M units actual OPERATOR distance')
    setcase('unpaid strict global blend','global_blend_coefficient',2,'global blend pays STRICT NN signs')
    setcase('local bound masquerades as global entry bound','global_M_entry_cost_coefficient','1/110','global FULL feasible optimizer entry distance')
    setcase('omit bounded-diameter global operator term','global_M_operator_cost_coefficient','139/11','global FULL feasible optimizer operator distance')
    runs=[]
    def reject(name,base,certificate,msg,optimized):
        remaining=min(45,60-(monotonic()-start))
        if remaining<=0:raise ValueError('60s serial adverse-control driver guard')
        out=certificate.parent/('bad-result-O.json' if optimized else 'bad-result.json')
        out.unlink(missing_ok=True)
        cmd=[sys.executable]+(['-O'] if optimized else [])+[str(base/'check.py'),'--certificate',str(certificate),'--out',str(out)]
        t=monotonic();r=subprocess.run(cmd,env=env,capture_output=True,timeout=remaining)
        error=r.stderr.decode()
        if r.returncode==0 or 'ValueError:' not in error or msg not in error or r.stdout or out.exists():
            raise ValueError('semantic defect was not meaningfully rejected: '+name+' '+error[-1000:])
        runs.append({'defect':name,'mode':'optimized' if optimized else 'normal',
                     'seconds':monotonic()-t,'meaningful_ValueError':True,'no_result_file':True,
                     'gate':error.strip().splitlines()[-1]})
    with tempfile.TemporaryDirectory(prefix='q18-projection-adverse-') as td:
        root=Path(td)
        for i,(name,d,msg) in enumerate(cases):
            p=root/(str(i)+'.json');p.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
            for optimized in [False,True]:reject(name,BASE,p,msg,optimized)
        cold=root/'source-damaged';cold.mkdir()
        for p in BASE.iterdir():
            if p.is_file():shutil.copyfile(p,cold/p.name)
        with (cold/'PROOF.md').open('a') as f:f.write('\nChanged mathematical claim.\n')
        unread=root/'malformed-input.json';unread.write_text('{')
        for optimized in [False,True]:
            reject('source gate precedes malformed mathematical input',cold,unread,'whole source file changed: PROOF.md',optimized)
    return {'actual_agent':'six-downset-3','role':'researcher','semantic_defects':len(cases),
            'normal_and_optimized_semantic_rejections':2*len(cases),'source_first_rejections':2,
            'all_rejections_meaningful':True,'runs':runs,'elapsed_seconds':monotonic()-start,
            'native_threads':1,'per_child_guard_seconds':45,'driver_guard_seconds':60,
            'independent_review_claimed':False}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    args.out.parent.mkdir(parents=True,exist_ok=True);result=controls()
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'meaningful_rejections':len(result['runs']),'seconds':result['elapsed_seconds']},sort_keys=True))

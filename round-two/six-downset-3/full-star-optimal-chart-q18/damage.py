"""Meaningful semantic controls: defects must raise the designated ValueError.

These are not source-manifest tests. Altered mathematical data enters the
fresh verifier itself, in both normal and optimized isolated children.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time

BASE = Path(__file__).resolve().parent
ENV = os.environ.copy()
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    ENV[name] = '1'


def damaged_inputs(data):
    d=copy.deepcopy(data); words=d['twice_inverse_rows'][0].split(); words[0]=str(int(words[0])+1)
    d['twice_inverse_rows'][0]=' '.join(words)
    yield 'alter-literal-inverse-entry',d,'every entry of A times the claimed inverse'
    d=copy.deepcopy(data); d['twice_inverse_rows'][0]=' '.join(d['twice_inverse_rows'][0].split()[:-1])
    yield 'omit-inverse-column',d,'entire inverse over2'
    d=copy.deepcopy(data); d['bad_vertex_order'][0],d['bad_vertex_order'][1]=d['bad_vertex_order'][1],d['bad_vertex_order'][0]
    yield 'mislabel-original-incidence-row',d,'all original bad labels'
    d=copy.deepcopy(data); d['pivot_edge_order'][0]=[24,24]
    yield 'unsupported-pivot-loop',d,'81 distinct actual supported pivot edges'
    d=copy.deepcopy(data); d['inverse_denominator']=1
    yield 'wrong-inverse-denominator',d,'entire inverse over2'
    d=copy.deepcopy(data); d['selected_edge_numerator']=1
    yield 'wrong-selected-coordinate-scale',d,'identity left inverse'
    d=copy.deepcopy(data); d['pivot_compensation_multiplier']=0
    yield 'omit-bad-degree-compensation',d,'EVERY original bad-degree equation'
    d=copy.deepcopy(data); d['good_gauge_numerator']=-1
    yield 'wrong-good-total-compensation',d,'EVERY original bad-degree equation and good total'
    d=copy.deepcopy(data); d['anchored_a_numerator']=-1
    yield 'wrong-physical-star-anchor',d,'every physical star kernel row'
    d=copy.deepcopy(data); d['rho_eta_denominator_power']=13
    yield 'uncertified-larger-real-cube',d,'uniform cube keeps every strict NN sign'
    d=copy.deepcopy(data); d['dependency_not_rechecked']=False
    yield 'conceal-external-PSD-premise',d,'explicit published ordinary same-carrier'


def main(out):
    spec=importlib.util.spec_from_file_location('sourcecheck',BASE/'sourcecheck.py')
    source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
    source.check_bundle(BASE)
    data=json.loads((BASE/'CHART.json').read_text()); cases=list(damaged_inputs(data)); results=[]
    with tempfile.TemporaryDirectory(prefix='q18-chart-semantic-') as tmp:
        root=Path(tmp)
        for mode in ('normal','optimized'):
            for name,bad,reason in cases:
                src=root/(name+'.json'); dst=root/(name+'.out.json')
                src.write_text(json.dumps(bad,sort_keys=True)+'\n')
                cmd=[sys.executable,'-I','-B']+(['-O'] if mode=='optimized' else [])+[
                    str(BASE/'check.py'),'--certificate',str(src),'--out',str(dst)]
                started=time.monotonic()
                run=subprocess.run(cmd,capture_output=True,text=True,env=ENV,timeout=45,check=False)
                if run.returncode!=1 or 'ValueError:' not in run.stderr or reason not in run.stderr or dst.exists():
                    raise ValueError('semantic control not rejected as intended: '+mode+'/'+name+' '+run.stderr)
                results.append({'mode':mode,'defect':name,'designated_rejection':reason,
                                'exit_code':run.returncode,'seconds':time.monotonic()-started,
                                'stderr_sha256':hashlib.sha256(run.stderr.encode()).hexdigest()})
    out.write_text(json.dumps({'actual_agent':'six-downset-3','role':'researcher',
                   'semantic_controls_not_parent_replays':True,'complete_rejections':len(results),
                   'native_threads':1,'child_guard_seconds':45,'results':results},sort_keys=True,indent=2)+'\n')
    print(json.dumps({'complete_rejections':len(results),'all_designated_ValueErrors':True}))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();main(args.out)

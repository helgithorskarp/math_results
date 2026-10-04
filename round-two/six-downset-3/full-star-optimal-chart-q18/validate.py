"""Source-gated normal/O/cold COMPLETE replays; no parent proof replay."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import resource
import shutil
import subprocess
import sys
import tempfile
import time

BASE=Path(__file__).resolve().parent


def source_gate(root):
    spec=importlib.util.spec_from_file_location('sourcecheck',root/'sourcecheck.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.check_bundle(root),module.REQUIRED


def run():
    seal,names=source_gate(BASE);env=os.environ.copy();receipts=[];started=time.monotonic()
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):env[k]='1'
    expected=(BASE/'EXPECTED.json').read_bytes(); chart=(BASE/'CHART.json').read_bytes()
    with tempfile.TemporaryDirectory(prefix='q18-chart-source-replay-') as td:
        td=Path(td); cold=td/'cold';cold.mkdir()
        for name in sorted(names|{'BUNDLE.json','SHA256SUMS'}):shutil.copyfile(BASE/name,cold/name)
        source_gate(cold)
        for mode,root,opt in (('normal',BASE,False),('optimized',BASE,True),('cold',cold,False)):
            out=td/(mode+'.json'); cmd=[sys.executable,'-I','-B']+(['-O'] if opt else [])
            cmd += [str(root/'check.py'),'--out',str(out)]
            t=time.monotonic(); r=subprocess.run(cmd,env=env,text=True,capture_output=True,timeout=45,check=False)
            if r.returncode or not out.exists() or out.read_bytes()!=expected:
                raise ValueError('whole mathematical chart replay failed: '+mode+' '+r.stderr)
            receipts.append({'mode':mode,'whole_expected_record_equal':True,'seconds':time.monotonic()-t})
        out=td/'cold-regenerated-chart.json';t=time.monotonic()
        r=subprocess.run([sys.executable,'-I','-B',str(cold/'produce.py'),'--out',str(out)],
                         env=env,capture_output=True,text=True,timeout=45,check=False)
        if r.returncode or not out.exists() or out.read_bytes()!=chart:
            raise ValueError('whole cold inverse reproduction failed '+r.stderr)
        receipts.append({'mode':'cold-producer','whole_original_certificate_equal':True,'seconds':time.monotonic()-t})
    return {'actual_agent':'six-downset-3','role':'researcher',**seal,
            'complete_record_bytes':len(expected),'complete_record_SHA256':hashlib.sha256(expected).hexdigest(),
            'complete_chart_bytes':len(chart),'complete_chart_SHA256':hashlib.sha256(chart).hexdigest(),
            'positive_receipts':receipts,'parent_center_and_PSD_dependency_not_rechecked':True,
            'native_threads':1,'serial_children':1,'child_guard_seconds':45,
            'timeout_or_incomplete_is_not_mathematical_evidence':True,'seconds':time.monotonic()-started,
            'peak_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();r=run()
    args.out.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps(r,sort_keys=True))

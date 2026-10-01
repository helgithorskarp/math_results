"""Regenerate compact QR31-by20 cover and check every product parameter."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time


def require(ok,message):
    if not ok:raise ValueError(message)


def run(work):
    source=Path(__file__).resolve().parent;work.mkdir(parents=True,exist_ok=True)
    expected=json.loads((source/'expected.json').read_text());env=os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE']='1'
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[name]='1'
    begin=time.monotonic();stages=[]
    def invoke(script,arguments,optimized=False,rejection=None):
        command=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(source/script)]+list(map(str,arguments))
        result=subprocess.run(command,capture_output=True,text=True,env=env,timeout=35)
        if rejection is not None:
            require(result.returncode!=0 and 'ValueError' in result.stderr and rejection in result.stderr,'damaged cover accepted or wrong rejection')
            return
        require(result.returncode==0,'incomplete source replay: '+result.stderr)
        return json.loads(result.stdout)
    generated=invoke('generate.py',[work]);require(generated['status']=='COMPLETE_QR31_X_C20_AP_COVER','no complete cover')
    cover=work/'cover.json'
    require(hashlib.sha256(cover.read_bytes()).hexdigest()==expected['cover_sha256'],'cover provenance')
    for optimized in [False,True]:
        result=invoke('check.py',[cover],optimized);stages.append(result)
        for key in ['status','covered','checked_prefix_length','antipodal_cases','nonantipodal_cases','cover_sha256']:
            require(result[key]==expected[key],'completed checker evidence mismatch '+key)
    value=json.loads(cover.read_text());controls=[]
    for label,mutate,rejection in [
        ('missing_case',lambda d:d['records'].pop(),'complete antipodal table size'),
        ('wrong_scope',lambda d:d.update(parameter_words=2097151),'cover metadata'),
        ('zero_step',lambda d:d['records'][1023].__setitem__(3,0),'actual interval AP bounds'),
        ('wrong_color',lambda d:d['records'][1023].__setitem__(4,1-d['records'][1023][4]),'nonmonochromatic claimed AP')]:
        damaged=copy.deepcopy(value);mutate(damaged);path=work/(label+'.json');path.write_text(json.dumps(damaged)+'\n')
        for optimized in [False,True]:invoke('check.py',[path],optimized,rejection)
        controls.append(label)
    summary={'author':'six-vdw-1','role':'researcher','status':'COMPLETE_QR31_BY20_FAMILY_REPLAY',
             'python_version':platform.python_version(),'covered':expected['covered'],'checked_prefix_length':2296,
             'affine_image_prefix_length':2480,'cover_sha256':expected['cover_sha256'],
             'normal_and_optimized_verified':True,'damaged_controls_rejected_both_modes':controls,
             'elapsed_seconds':time.monotonic()-begin,'stages':stages,
             'proof_limit':'Exact specific product family and its affine images; no unrestricted W(2,7) exclusion or peer-review verdict.'}
    (work/'validation.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True)
    run(parser.parse_args().work)

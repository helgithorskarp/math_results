"""Portable replay of the own seal's positive, source and fixture controls.

Added after the initial seal to package its already completed controls.
No author executable is used. Each child is serial and bounded to45 seconds.
"""
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
THREADS=['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
         'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']
ENV=dict(os.environ,**{k:'1' for k in THREADS},PYTHONDONTWRITEBYTECODE='1')
MUTATIONS=[
 ('Fourier-lost-conjugation','rows[(k - l) % 9] += a * bar(b)','rows[(k - l) % 9] += a * b'),
 ('Fourier-wrong-conjugate-exponent','rows[(l - k) % 9] += bar(a) * b','rows[(k - l) % 9] += bar(a) * b'),
 ('Fourier-wrong-degree','rows[(k - l) % 9] -= 9 * a * bar(b)','rows[(k - l) % 9] -= 8 * a * bar(b)'),
 ('complex-top-trace-sign','- 27 * re(d[8] * bar(d[7]))','+ 27 * re(d[8] * bar(d[7]))'),
 ('wrong-cube-pair','rho = lambda k: Q(1) if k % 3 == 0 else Q(-1, 2)',
  'rho = lambda k: Q(1) if k % 3 == 0 else Q(-1, 3)'),
 ('third-Newton-mixed-term','-u**3/4+3*u*t2/4-t3/2','-u**3/4+2*u*t2/4-t3/2'),
 ('fourth-Newton-whole-term','+9*t2*t2/40+3*u*t3/5-9*t4/20','+9*t2*t2/40+3*u*t3/5'),
 ('M0-H-sign','(Q(45,112)-Q(9,4)*kappa)*H','(Q(45,112)+Q(9,4)*kappa)*H'),
 ('M1-second-order-term','Q(27,4)*eta+18*eta*eta+19*eta*x','Q(27,4)*eta-18*eta*eta+19*eta*x'),
 ('stale-extended-endpoint','r=Q(1,25);extended_e=Q(1,16384)',
  'r=Q(1,25);extended_e=Q(1,65536)')]


def run(script,fixture,optimized=False):
    args=[sys.executable,'-B']+(['-O'] if optimized else [])
    return subprocess.run(args+[str(script),'--expect',str(fixture)],
                          env=ENV,capture_output=True,text=True,timeout=45)


def main():
    start=time.monotonic();seal=json.loads((ROOT/'INDEPENDENCE.json').read_text())
    for name,h in seal['source_sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:
            raise ValueError('frozen source or expected fixture changed')
    source=ROOT/'audit.py';fixture=ROOT/'EXPECTED.json';body=source.read_text()
    positive=[]
    for optimized in [False,True]:
        p=run(source,fixture,optimized)
        if p.returncode:raise ValueError(p.stderr.strip())
        positive.append(json.loads(p.stdout))
    if positive[0]!=positive[1]:raise ValueError('normal/optimized mismatch')
    rejected=[]
    with tempfile.TemporaryDirectory(prefix='.validation-',dir=ROOT) as temp:
        tmp=Path(temp)
        for name,old,new in MUTATIONS:
            if old not in body:raise ValueError('source mutation missing')
            pth=tmp/(name+'.py');pth.write_text(body.replace(old,new,1))
            p=run(pth,fixture)
            if p.returncode!=1 or not p.stderr.startswith('FAIL:'):
                raise ValueError('source damage not rejected correctly: '+name)
            rejected.append({'name':name,'reason':p.stderr.strip()})
        expected=json.loads(fixture.read_text());bad=[]
        x=copy.deepcopy(expected);x['original']['ratio']='24';bad.append(('wrong-whole-ratio',json.dumps(x)))
        x=copy.deepcopy(expected);x['identities']['Fourier-row-1']=[];bad.append(('missing-whole-row',json.dumps(x)))
        x=copy.deepcopy(expected);x['complete_cross_bounds']['8']['used_bound']=10.0;bad.append(('integer-to-float',json.dumps(x)))
        x=copy.deepcopy(expected);x['extension']['polynomials'].pop('whole-T');bad.append(('missing-window-polynomial',json.dumps(x)))
        bad.extend([('duplicate-key','{"a":1,"a":2}'),('nonfinite','{"a":NaN}'),
                    ('malformed','{'),('extra-global-claim',json.dumps(dict(expected,global_conjecture=True)))])
        for name,data in bad:
            pth=tmp/(name+'.json');pth.write_text(data);p=run(source,pth,True)
            if p.returncode!=1 or not p.stderr.startswith('FAIL:'):
                raise ValueError('fixture damage not rejected correctly: '+name)
            rejected.append({'name':name,'reason':p.stderr.strip()})
    old=seal['semantic_source_damages']+seal['optimized_external_fixture_rejections']
    if [(r['name'],r['reason']) for r in rejected]!=[(r['name'],r['reason']) for r in old]:
        raise ValueError('original rejection reasons changed')
    print(json.dumps({'status':'PASS','full_record_sha256':positive[0]['full_record_sha256'],
                      'whole_identities':19,'strict_margins':41,'full_literal_controls':5,
                      'source_damage_rejections':10,'optimized_fixture_rejections':8,
                      'frozen_bytes_unchanged':True,'native_threads_one':True,'serial':True,
                      'wall_seconds':round(time.monotonic()-start,6)}))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,subprocess.TimeoutExpired) as error:
        print('FAIL:',error,file=sys.stderr);raise SystemExit(1)

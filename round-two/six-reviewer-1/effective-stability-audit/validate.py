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
MUTATIONS=[('primitive-nonagon-sign', 'p[j - 3] -= p[j]', 'p[j - 3] += p[j]'), ('lost-phase-conjugation', 'OMEGA_POWERS[(-j) % 9]', 'OMEGA_POWERS[j % 9]'), ('fourth-third-moment-sign', '+ (cosine(3 * k) - 1) * H3 / 18', '- (cosine(3 * k) - 1) * H3 / 18'), ('complete-Newton-third-sign', '-T3 / 2)', 'T3 / 2)'), ('complex-motion-wrong-inverse', 'mm * (1 - w) + kk * (w**-1 - w)', 'mm * (1 - w) + kk * (w**-2 - w)'), ('full-Gram-wrong-sign', '- 4 * cross**2, 4 * wedges)', '+ 4 * cross**2, 4 * wedges)'), ('unclosed-reciprocal-cost', 'new_cost = (37 +', 'new_cost = (38 +'), ('unclosed-root-motion-cost', "'new motion Delta13over2': F(13, 2)", "'new motion Delta13over2': F(6)")]


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
        x=copy.deepcopy(expected);x['whole_phase_table'].pop();bad.append(('missing-whole-phase',json.dumps(x)))
        x=copy.deepcopy(expected);x['proved_remainder']='13';bad.append(('false-remainder',json.dumps(x)))
        x=copy.deepcopy(expected);x['identities'][0]['terms']=float(x['identities'][0]['terms']);bad.append(('float-identity-count',json.dumps(x)))
        x=copy.deepcopy(expected);x['global_first_power_proved']=True;bad.append(('extra-global-claim',json.dumps(x)))
        bad.extend([('duplicate-key','{"schema":0,"schema":1}'),('nonfinite','{"schema":NaN}')])
        for name,data in bad:
            pth=tmp/(name+'.json');pth.write_text(data);p=run(source,pth,True)
            if p.returncode!=1 or not p.stderr.startswith('FAIL:'):
                raise ValueError('fixture damage not rejected correctly: '+name)
            rejected.append({'name':name,'reason':p.stderr.strip()})
    old=seal['source_damages']+seal['fixture_damages']
    if [(r['name'],r['reason']) for r in rejected]!=[(r['name'],r['reason']) for r in old]:
        raise ValueError('original rejection reasons changed')
    print(json.dumps({'status':'PASS','full_record_sha256':positive[0]['whole_record_sha256'],
                      'whole_identities':54,'strict_margins':56,'full_literal_controls':4,
                      'source_damage_rejections':8,'optimized_fixture_rejections':6,
                      'frozen_bytes_unchanged':True,'native_threads_one':True,'serial':True,
                      'wall_seconds':round(time.monotonic()-start,6)}))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,subprocess.TimeoutExpired) as error:
        print('FAIL:',error,file=sys.stderr);raise SystemExit(1)

"""Serial normal/O cold runs and bounded semantic damage checks.

No resource setting is raised. A timeout is an operational failure,
never a mathematical absence certificate. Each child has a 45s guard.
"""
from pathlib import Path
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time


def main():
    root=Path(__file__).resolve().parent
    env=os.environ.copy()
    for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
              'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
        env[k]='1'
    results=[];start=time.monotonic()
    def child(path,mode,fixture=None,reject=None):
        cmd=[sys.executable,'-I','-B']+(['-O'] if mode else [])+[str(path/'verify.py')]
        if fixture:cmd+=['--expected',str(fixture)]
        p=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=45)
        if reject is None:
            if p.returncode:raise ValueError('cold verification failed: '+p.stderr)
            return json.loads(p.stdout)
        if p.returncode==0 or not any(v in p.stderr for v in reject):
            raise ValueError('damage did not specifically reject: '+p.stderr)
        return {'returncode':p.returncode,'reason':p.stderr.splitlines()[-1]}
    normal=child(root,False);optimized=child(root,True)
    if normal['canonical_sha256']!=optimized['canonical_sha256']:
        raise ValueError('normal/O record disagreement')
    record=json.loads((root/'EXPECTED.json').read_text())
    with tempfile.TemporaryDirectory(prefix='coefficient-E-audit-') as tmp:
        base=Path(tmp);cold=base/'cold';cold.mkdir()
        for name in ['algebra.py','audit.py','verify.py','EXPECTED.json']:
            shutil.copyfile(root/name,cold/name)
        portable=child(cold,True)
        if portable['canonical_sha256']!=normal['canonical_sha256']:
            raise ValueError('portable record disagreement')
        mutations=[
            ('scaled row', 'audit.py', 'rr=[chart(v,d) for v,d in zip(original,[2,1,2,1,2])]',
             'rr=[chart(v,d) for v,d in zip(original,[2,2,2,1,2])]', ['chart parity']),
            ('quadratic coefficient','audit.py','Q(367,180)','Q(369,180)', ['whole-E-quadratic']),
            ('lower equation sign','audit.py','n2*g0**2-n1*g1*g0+n0*g1**2',
             'n2*g0**2+n1*g1*g0+n0*g1**2',['cross contents','whole-undivided']),
            ('constant pivot','audit.py','118272-(31304*r','118273-(31304*r',['entire-A2']),
            ('nonprime','audit.py','prime=263','prime=261',['prime check']),
            ('missing sign','algebra.py','sign=-1 if sum','sign=1 if sum',['signed-determinant-control']),
            ('adjoint leading','algebra.py','out[k-1]-k*a[k]','out[k-1]-(k+1)*a[k]',
             ['coefficient identity','complete pencil term counts']),
        ]
        for i,(label,name,old,new,reasons) in enumerate(mutations):
            path=base/('source-'+str(i));path.mkdir()
            for file in ['algebra.py','audit.py','verify.py','EXPECTED.json']:
                shutil.copyfile(root/file,path/file)
            text=(path/name).read_text()
            if text.count(old)!=1:raise ValueError('ambiguous damage '+label)
            (path/name).write_text(text.replace(old,new))
            results.append({'source_damage':label,'optimized':True,**child(path,True,reject=reasons)})
        fixtures=[]
        damaged=copy.deepcopy(record);damaged['original_residual'][0][0][1]+=1
        fixtures.append(('coefficient',json.dumps(damaged),['value mismatch']))
        damaged=copy.deepcopy(record);damaged['primitive_determinants'][1].pop()
        fixtures.append(('omitted determinant tail',json.dumps(damaged),['list length mismatch']))
        damaged=copy.deepcopy(record);damaged['prime']=True
        fixtures.append(('boolean alias',json.dumps(damaged),['type mismatch']))
        damaged=copy.deepcopy(record);damaged['unit_U'][0]=(damaged['unit_U'][0]+1)%263
        fixtures.append(('unit coefficient',json.dumps(damaged),['value mismatch']))
        fixtures.append(('duplicate key','{"schema":1,"schema":1}', ['duplicate fixture key']))
        fixtures.append(('nonfinite','{"schema":NaN}', ['nonfinite fixture value']))
        for i,(label,text,reasons) in enumerate(fixtures):
            path=base/('fixture-'+str(i)+'.json');path.write_text(text)
            results.append({'fixture_damage':label,'optimized':True,**child(root,True,path,reasons)})
    summary={'agent':'six-reviewer-1','role':'independent mathematical reviewer',
             'normal':normal,'optimized':optimized,'portable':portable,'damage_rejections':results,
             'serial_math_children':True,'native_threads':1,'per_child_guard_seconds':45,
             'unchanged_scope':'1CPU2GiB','total_seconds':time.monotonic()-start}
    (root/'VALIDATION.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'canonical_sha256':normal['canonical_sha256'],'rejections':len(results),
                      'wall_seconds':summary['total_seconds']},sort_keys=True))


if __name__=='__main__':
    main()

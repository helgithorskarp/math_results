"""Serial malformed-data and incorrect-mathematics controls, native threads 1."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('independent_basin', ROOT/'check.py')
own = importlib.util.module_from_spec(spec)
spec.loader.exec_module(own)


def rejects(operation, label):
    try:
        operation()
    except ValueError:
        return
    raise ValueError('incorrect mathematics accepted: '+label)


def main():
    record = own.build()
    rejects(lambda: own.require(own.Q(record['derivatives']['M_4']) < 1100, 'wrong M4'), 'false fourth-order cap')
    rejects(lambda: own.require(own.Q(7, 3)**2 >= 7, 'wrong phase norm'), 'false phase one-norm')
    rejects(lambda: own.require(own.Q(3, 4)-own.Q(19, 8)-own.Q(800, 160000) >= own.Q(3, 8), 'wrong slack box'), 'excessive slack box')
    rejects(lambda: own.require(own.Q(1, 40)-own.Q(1200, 10000) >= own.Q(1, 80), 'wrong phase box'), 'excessive phase box')
    rejects(lambda: own.require(all(-own.Q(v) > 0 for v in record['heavy_curvature']['bernstein_margin']), 'negative curvature'), 'reversed curvature sign')
    rejects(lambda: own.require((own.Jet([own.Q(2, 5), 1], 3)**2*own.Jet([own.Q(3, 7), 1], 3)).c[3] == 2, 'wrong derivative factorial'), 'third derivative normalization')
    changes = []
    x=copy.deepcopy(record); x['version']=True; changes.append(('boolean_version',x))
    x=copy.deepcopy(record); x['caps'][0]['numerator'][1]='1'; changes.append(('coefficient',x))
    x=copy.deepcopy(record); x['caps'][0]['denominator_bernstein'].pop(); changes.append(('omitted_Bernstein',x))
    x=copy.deepcopy(record); x['heavy_curvature']['bernstein_margin'][0]='-1'; changes.append(('curvature',x))
    x=copy.deepcopy(record); x['derivatives']['M_4']='1'; changes.append(('derivative',x))
    x=copy.deepcopy(record); x['caps'].append(copy.deepcopy(x['caps'][0])); changes.append(('duplicate_cap',x))
    x=copy.deepcopy(record); x['domains']['enlarged']['slack_denominator']=51; changes.append(('domain',x))
    x=copy.deepcopy(record); x['extra']=0; changes.append(('extra_field',x))
    env=dict(os.environ)
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
        env[key]='1'
    total=0
    with tempfile.TemporaryDirectory(prefix='basin-fixture-') as d:
        for name, damaged in changes:
            p=Path(d)/(name+'.json');p.write_text(json.dumps(damaged))
            for optimized in [False,True]:
                cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(ROOT/'check.py'),'--expected',str(p)]
                run=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=45)
                own.require(run.returncode == 1 and 'ValueError: fixture' in run.stderr,
                            'damaged fixture must fail at a typed comparison: '+name)
                total+=1
    print(json.dumps({'status':'PASS','mathematical_damages':6,
                      'external_fixture_damages':8,'normal_optimized_rejections':total}))


if __name__ == '__main__':
    main()

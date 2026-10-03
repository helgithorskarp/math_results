"""Bounded serial semantic and whole-record damage controls, normal and -O."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from verify import DAMAGES

ERRORS = ('Direct curvature constant','Both actual stationary rows solved','Physical winning drift norm and cross coefficient','Whole all-real coefficient dominance','Both original unaveraged odd rows','Entire literal first anchored jet','Complete actual FIRST-power cubic objective')


def main():
    started = time.monotonic()
    env = dict(os.environ,**{n:'1' for n in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                                           'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')})
    runs = []
    with tempfile.TemporaryDirectory(prefix='six-reviewer-4-quadratic-motion-') as temporary:
        tmp = Path(temporary)
        def child(optimized,script=ROOT/'verify.py',args=(),expected_code=0,marker=None):
            cmd = [sys.executable,'-I','-B']+(['-O']if optimized else [])+[str(script),*args]
            before = time.monotonic()
            p = subprocess.run(cmd,cwd=tmp,env=env,timeout=30,capture_output=True)
            if (p.returncode==0) != (expected_code==0):
                raise ValueError('Unexpected control outcome: '+repr(cmd)+' '+p.stderr.decode()[-1500:])
            if marker and marker not in p.stderr.decode():
                raise ValueError('Control did not reach the intended mathematical/fixture rejection')
            runs.append(dict(optimized=optimized,args=list(args),exit_code=p.returncode,
                             seconds=time.monotonic()-before,stdout_bytes=len(p.stdout),
                             stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),intended_error=marker))
            return p.stdout
        positives = [child(o,args=('--record',))for o in (False,True)]
        if positives[0] != positives[1]:
            raise ValueError('Whole ordinary/optimized record mismatch')
        for o in (False,True):
            for damage,error in zip(DAMAGES,ERRORS):
                child(o,args=('--damage',damage),expected_code=1,marker=error)
        original = json.loads(positives[0])
        fixtures = []
        missing = tmp/'missing.json'
        fixtures.append((missing,'No such file'))
        malformed = tmp/'malformed.json'
        malformed.write_text('{')
        fixtures.append((malformed,'JSONDecodeError'))
        for label in ('boolean_index','missing_constant','changed_normal','deleted_case','extra_field'):
            value = json.loads(json.dumps(original))
            if label=='boolean_index':
                value['quadratic_motion']['all9_original_maps'][0]['j'] = True
            elif label=='missing_constant':
                del value['stationary_original_values']['Gamma']
            elif label=='changed_normal':
                value['quadratic_motion']['all9_affine_squared_norms'][0]['a'][0] = '1'
            elif label=='deleted_case':
                value['literal_fixed100_witness']['all9_actual_inward_normals'].pop()
            else:
                value['unintended_extra_field'] = True
            p = tmp/(label+'.json')
            p.write_text(json.dumps(value)+'\n')
            fixtures.append((p,'Entire typed mathematical record mismatch'))
        for o in (False,True):
            for p,error in fixtures:
                child(o,args=('--expected',str(p)),expected_code=1,marker=error)
        cold = tmp/'source-only'
        cold.mkdir()
        # Only sealed core files and the compact manifest are available.
        manifest = json.loads((ROOT/'MANIFEST.json').read_text())
        for n in list(manifest['core_files'])+['MANIFEST.json']:
            shutil.copyfile(ROOT/n,cold/n)
        for o in (False,True):
            data = child(o,script=cold/'verify.py',args=('--record',))
            if data != positives[0]:
                raise ValueError('Whole empty relocated source-only record mismatch')
        with (cold/'exact.py').open('a') as stream:
            stream.write('\n# actual preimport source damage\n')
        for o in (False,True):
            child(o,script=cold/'verify.py',expected_code=1,marker='Core source seal mismatch: exact.py')
    print(json.dumps(dict(actual_agent='six-reviewer-4',role='independent mathematical reviewer',
                          mathematical_damages_per_mode=len(DAMAGES),external_fixture_damages_per_mode=7,
                          preimport_source_damages=2,whole_four_positive_records_equal=True,
                          one_cpu_child_at_a_time=True,each_initial_guard_seconds=30,
                          total_seconds=time.monotonic()-started,runs=runs),sort_keys=True))


if __name__=='__main__':
    main()

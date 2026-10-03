"""Cold compact source-only reconstruction; one bounded serial child at a time."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1', BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1',
           VECLIB_MAXIMUM_THREADS='1', PYTHONHASHSEED='0')


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def operations_allow():
    name = os.environ.get('RESEARCH_OPERATIONS_STATE')
    if not name:
        return
    root = Path(name)
    for directory in (root, root/'monitor'):
        if any((directory/marker).exists() for marker in ('PAUSED', 'PAUSED.json')):
            raise ValueError('Operations pause; no new computation')
        path = directory/'HANDOVER.json'
        if path.exists() and json.loads(path.read_text()).get('phase') != 'completed':
            raise ValueError('Incomplete handover; no new computation')
    health = json.loads((root/'monitor/health.json').read_text())
    if health['campaign_state'] != 'running' or health['credit_budget']['status'] != 'authorized':
        raise ValueError('Operations budget/state barrier; no new computation')


def main():
    operations_allow()
    if WORK.exists() and any(WORK.iterdir()):
        raise ValueError('Cold run requires an absent or empty work directory; use a fresh source copy')
    WORK.mkdir(exist_ok=True)
    started = time.monotonic()
    stages = []
    for script, optimized in [('generate.py', False), ('verify.py', False),
                              ('verify.py', True), ('check_controls.py', False)]:
        operations_allow()
        command = [sys.executable]+(['-O'] if optimized else [])+[str(ROOT/script)]
        before = time.monotonic()
        result = subprocess.run(command, env=ENV, capture_output=True, text=True, timeout=55)
        (WORK/(script+('-O' if optimized else '')+'.log')).write_text(result.stdout+result.stderr)
        if result.returncode != 0:
            raise ValueError('Incomplete or failed child supplies no theorem: '+script+'\n'+result.stderr)
        record = json.loads(result.stdout)
        if digest(record['finite']) != record['finite_sha256']:
            raise ValueError('Child complete finite binding differs')
        stages.append({'script': script, 'optimized': optimized, 'seconds': time.monotonic()-before,
                       'returncode': result.returncode, 'finite_sha256': record['finite_sha256']})
    normal = json.loads((WORK/'checked.json').read_text())
    optimized = json.loads((WORK/'checked-O.json').read_text())
    proposal = json.loads((WORK/'proposal.json').read_text())
    controls = json.loads((WORK/'controls.json').read_text())
    if normal['finite'] != optimized['finite'] or normal['finite_sha256'] != optimized['finite_sha256']:
        raise ValueError('Entire normal/O records differ')
    finite = {'original_proposal_finite_sha256': proposal['finite_sha256'],
              'complete_scalar_finite_sha256': normal['finite_sha256'],
              'semantic_controls_finite_sha256': controls['finite_sha256'],
              'entire_normal_O_finite_records_equal': True,
              'all8_semantic_damages_reject': True, 'cold_source_only_complete': True,
              'arbitrary_preparation_length_bound_assumed': False,
              'depth_bound_assumed': False, 'certified_lower_bound_for_the_chosen_head_tail': 45,
              'global_size44_exclusion_claimed': False,
              'external_person_review_claimed': False, 'formalized': False}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'COMPLETE_COLD_UNIVERSAL_CONDITIONAL_MAXIMUM_TAIL_OBSTRUCTION_AUTHOR_CERTIFICATE',
              'finite': finite, 'finite_sha256': digest(finite), 'stages': stages,
              'seconds': time.monotonic()-started, 'python_version': sys.version}
    (WORK/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()

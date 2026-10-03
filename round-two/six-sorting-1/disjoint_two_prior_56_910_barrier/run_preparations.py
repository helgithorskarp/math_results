"""Fresh serial reconstruction; copied source is credited, old negatives absent.

Each mathematical child has a55s wall guard and unchanged internal guards.
Full normal/-O finite records must agree. Interrupted phases stay incomplete.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from controls import operations_allow

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work'
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1', BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1',
           VECLIB_MAXIMUM_THREADS='1', PYTHONHASHSEED='0')
STAGES = []


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def child(script, *args, optimized=False):
    operations_allow()
    command = [sys.executable] + (['-O'] if optimized else []) + [str(ROOT/script), *map(str, args)]
    started = time.monotonic()
    result = subprocess.run(command, capture_output=True, text=True, env=ENV, timeout=55)
    label = f'{len(STAGES):02}-' + script.replace('/', '-') + ('-O' if optimized else '')
    (WORK/(label+'.log')).write_text(result.stdout+result.stderr)
    need(result.returncode == 0, 'Incomplete child: '+label+'; no negative inference')
    record = {'script': script, 'args': list(args), 'optimized': optimized,
              'seconds': time.monotonic()-started, 'returncode': result.returncode}
    STAGES.append(record)
    (WORK/'preparation-stages.json').write_text(json.dumps(STAGES, indent=2)+'\n')
    print(json.dumps(record), flush=True)
    return result.stdout


def pair(name):
    a = json.loads((WORK/(name+'.json')).read_text())
    b = json.loads((WORK/(name+'-O.json')).read_text())
    need(a['finite'] == b['finite'] and digest(a['finite']) == a['finite_sha256'] == b['finite_sha256'],
         'Entire normal/O finite records differ: '+name)
    return a


def main():
    started = time.monotonic()
    operations_allow()
    child('prior/base.py')
    n = json.loads(child('prior/verify_base.py'))
    o = json.loads(child('prior/verify_base.py', optimized=True))
    need(n == o, 'Entire scalar base records differ')
    for name, finite in [('base-checked', n), ('base-checked-O', o)]:
        (WORK/(name+'.json')).write_text(json.dumps({'finite': finite, 'finite_sha256': digest(finite)}, indent=2)+'\n')
    child('cover.py')
    child('verify_original.py')
    child('verify_original.py', optimized=True)
    original = pair('original-checked')
    child('preparations.py', 3, 4)
    child('verify_preparations.py', 3, 4)
    child('verify_preparations.py', 3, 4, optimized=True)
    preparation = pair('checked03')
    child('screen_cuts.py', 3, 4)
    child('verify_cuts.py', 3, 4)
    child('verify_cuts.py', 3, 4, optimized=True)
    cuts = pair('free-cut-independent-03-04')
    proposal = json.loads((WORK/'branch03.json').read_text())
    screened = json.loads((WORK/'cuts03.json').read_text())
    finite = {'branch_index': 3, 'literal_HIGH_word': [[5, 6], [9, 10]],
              'full_functions': len(proposal['functions']),
              'preparation_full_function_list_sha256': proposal['full_functions_sha256'],
              'preparation_scalar_finite_sha256': preparation['finite_sha256'],
              'original_scalar_finite_sha256': original['finite_sha256'],
              'free_cut_scalar_finite_sha256': cuts['finite_sha256'],
              'cut_census': screened['census'],
              'retained_functions': len(screened['retained_function_ids']),
              'entire_normal_O_finite_records_equal': True,
              'old_negative_corpus_read': False, 'whole_route_exclusion_claimed': False}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'FRESH_COMPLETE_PREPARATION_AND_SUFFICIENT_FREE_CUT_PHASE_ONLY',
              'finite': finite, 'finite_sha256': digest(finite),
              'seconds': time.monotonic()-started,
              'independent_person_review': 'not requested; pending if later published'}
    (WORK/'preparation-phase-complete.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()

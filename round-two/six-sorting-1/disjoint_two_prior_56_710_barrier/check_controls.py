"""Six serial semantic rejection checks, repairing full transport digests.

Original valid proposal bytes are restored after every check. A failed or
incomplete check contributes no negative mathematical conclusion.
"""
import copy
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


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def transport_front(record):
    record['survivors_sha256'] = digest(record['survivors'])
    record['rejections_sha256'] = digest(record['rejections'])
    omitted = {'agent', 'role', 'status', 'survivors', 'rejections', 'finite_sha256',
               'seconds', 'maximum_rss_kib', 'scope'}
    record['finite_sha256'] = digest({k: v for k, v in record.items() if k not in omitted})


def main():
    operations_allow()
    first, last = map(int, sys.argv[1:3])
    frontpath = WORK / f'fronts02-{first:05}-{last:05}.json'
    casepath = WORK / f'constant02-{first:05}-{last:05}.json'
    originals = {p: p.read_bytes() for p in (frontpath, casepath)}
    front, proposal = (json.loads(originals[p]) for p in (frontpath, casepath))
    changes = []
    damaged = copy.deepcopy(front)
    cut = next(r for r in damaged['rejections'] if r['kind'] == 'PUBLIC_CONDITIONAL_MAXIMUM_OBSTRUCTION')
    dead = [2, 3, 4, 5, 7, 8]
    actual_nonzero_port = next(p for p in (5, 7, 8) if cut['F24'] >> dead.index(p) & 1)
    cut['chosen_head_port'] = actual_nonzero_port
    transport_front(damaged)
    changes.append(('actual_nonzero_head', frontpath, damaged, 'verify_fronts.py',
                    ['2', str(first), str(last)], 'Public universal cut is not applicable'))
    damaged = copy.deepcopy(front)
    removed = damaged['survivors'].pop(0)
    damaged['census']['surviving_complete_fronts'] -= 1
    key = str(removed['remaining_gate_budget'])
    # These integer keys are strings after the original JSON serialization.
    damaged['remaining_gate_budgets'][key] -= 1
    if not damaged['remaining_gate_budgets'][key]:
        del damaged['remaining_gate_budgets'][key]
    sizes = [len(r['nine_core_states']) for r in damaged['survivors']]
    damaged['front_image_size_range'] = [min(sizes), max(sizes)]
    transport_front(damaged)
    changes.append(('omitted_actual_tail_front', frontpath, damaged, 'verify_fronts.py',
                    ['2', str(first), str(last)], 'One necessary tail function is silently missing'))
    damaged = copy.deepcopy(proposal)
    case = next(r for r in damaged['cases'] if r['constant16_exceeds44'])
    witness = case['selected_witnesses'][0]
    witness['B7'] = 17
    witness['label'] += 1
    case['selected_mass'] = sum(1 << r['label'] for r in case['selected_witnesses'])
    damaged['cases_sha256'] = damaged['finite']['cases_sha256'] = digest(damaged['cases'])
    damaged['finite_sha256'] = digest(damaged['finite'])
    offset = damaged['cases'].index(case)
    changes.append(('unjustified_larger_constant', casepath, damaged, 'verify_constant.py',
                    ['2', str(first), str(last), str(offset), str(offset+1)],
                    'Unjustified S7 constant or nested label'))
    records = []
    for label, path, damaged, script, arguments, reason in changes:
        for optimized in (False, True):
            operations_allow()
            need(all(p.read_bytes() == raw for p, raw in originals.items()), 'Valid inputs were not restored')
            path.write_text(json.dumps(damaged, indent=2)+'\n')
            command = [sys.executable] + (['-O'] if optimized else []) + [str(ROOT/script)] + arguments
            start = time.monotonic()
            try:
                result = subprocess.run(command, env=ENV, capture_output=True, text=True, timeout=55)
            finally:
                path.write_bytes(originals[path])
            output = result.stdout + result.stderr
            need(result.returncode != 0 and reason in output,
                 'Semantic damage did not reject for its intended reason: ' + label)
            records.append({'label': label, 'optimized': optimized, 'intended_reason': reason,
                            'rejected': True, 'returncode': result.returncode,
                            'seconds': time.monotonic()-start})
            (WORK/(f'control-{label}'+('-O' if optimized else '')+'.log')).write_text(output)
    need(all(p.read_bytes() == raw for p, raw in originals.items()), 'Valid input bytes changed')
    finite = {'retained_interval': [first, last],
              'semantic_rejections': [{k:v for k,v in r.items() if k != 'seconds'} for r in records],
              'all6_intended_semantic_rejections': len(records) == 6,
              'entire_transport_digests_repaired': True, 'valid_original_proposals_unchanged': True}
    result = {'agent':'six-sorting-1', 'role':'researcher',
              'status':'COMPLETE_SIX_PRIVATE_RESIDUAL_SEMANTIC_REJECTION_CONTROLS',
              'finite':finite, 'finite_sha256':digest(finite), 'timings':records,
              'external_person_review_claimed':False}
    (WORK/f'controls-{first:05}-{last:05}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()

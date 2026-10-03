"""Bounded original3+3 proposals using the credited99-domain pool and S7>=16.

Never an exact suffix solver. Every insufficient mass is preserved open.
The generic label mechanism is published9007; no novelty is claimed for it.
"""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

from controls import operations_allow

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'work'


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    operations_allow()
    start = time.monotonic()
    deadline = start+45
    first, last, case_first, case_last = map(int, sys.argv[1:5])
    source = ROOT/'prior'
    pins = {r['path']:r['sha256'] for r in json.loads((source/'source-manifest.json').read_text())['files']}
    for name in ('pruning.py','profile.py','fixture.json'):
        need(hashlib.sha256((source/name).read_bytes()).hexdigest() == pins[name], 'Credited primitive changed')
    profile = load('credited_new_route_packed_profile', source/'profile.py')
    pruning = load('credited_new_route_packed_carriers', source/'pruning.py')
    pool = json.loads((source/'fixture.json').read_text())['selected_original_pool']
    need(len(pool) == len({tuple(x) for x in pool}) == 99, 'Literal credited pool differs')
    front = json.loads((OUT/f'fronts03-{first:05}-{last:05}.json').read_text())
    normal = json.loads((OUT/f'check03-{first:05}-{last:05}.json').read_text())
    optimized = json.loads((OUT/f'check03-{first:05}-{last:05}-O.json').read_text())
    need(normal['finite'] == optimized['finite'] and digest(normal['finite']) == normal['finite_sha256'] ==
         optimized['finite_sha256'] and normal['finite']['producer_front_sha256'] == front['finite_sha256'],
         'Fresh whole front cover is not independently checked')
    need(0 <= first < last and last-first <= 128 and
         0 <= case_first < case_last <= len(front['survivors']) and case_last-case_first <= 1000,
         'A bounded explicit slice of at most1000 surviving fronts is required')
    cases, counts = [], Counter()
    for index in range(case_first, case_last):
        need(time.monotonic() < deadline, 'Incomplete45s selection; no nonexistence inference')
        if index % 32 == 0:
            operations_allow()
        record = front['survivors'][index]
        need(digest(record['prefix']) == record['prefix_sha256'], 'Actual literal prefix binding differs')
        classes = {}
        for low, high in pool:
            actual = pruning.pruning(record['prefix'], low, high, profile)
            original = actual['outer_record']
            label = original[4]+original[5]+16
            key = tuple(original[2:4])
            witness = {'original_LOW_mask':low, 'original_HIGH_mask':high,
                       'outer_record':original, 'retained_Q_sha256':digest(actual['retained_prefix']),
                       'B7':16, 'label':label}
            if key not in classes or label > classes[key]['label']:
                classes[key] = witness
        witnesses, mass = [], 0
        for witness in sorted(classes.values(), key=lambda r:(-r['label'],r['outer_record'][2:4])):
            witnesses.append(witness)
            mass += 1 << witness['label']
            if mass > 1 << 44:
                break
        closed = mass > 1 << 44
        counts['fronts_tested'] += 1
        counts['constant16_exclusion_proposals' if closed else 'constant16_inconclusive_preserved_open'] += 1
        counts['selected_original_outer_occurrences'] += len(witnesses)
        cases.append({'branch_index':3, 'front_index':index,
                      'prefix_sha256':record['prefix_sha256'], 'nine_core_sha256':record['nine_core_sha256'],
                      'whole99_class_mass':sum(1 << r['label'] for r in classes.values()),
                      'constant16_exceeds44':closed, 'selected_mass':mass, 'selected_witnesses':witnesses})
    finite = {'branch_index':3, 'new_reserve_open_function_interval':[first,last],
              'case_slice':[case_first,case_last], 'census':dict(counts),
              'producer_front_sha256':front['finite_sha256'], 'cases_sha256':digest(cases),
              'inconclusive_front_indices':[r['front_index'] for r in cases if not r['constant16_exceeds44']],
              'whole_route_exclusion_claimed':False}
    result = {'agent':'six-sorting-1', 'role':'researcher',
              'status':'FRESH_BOUNDED_CONSTANT16_PROPOSALS_NEED_SCALAR_ORIGINAL_CUBE_REPLAY',
              'finite':finite, 'finite_sha256':digest(finite), 'cases':cases,
              'seconds':time.monotonic()-start,
              'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (OUT/f'constant03-{first:05}-{last:05}-{case_first:05}-{case_last:05}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'}),flush=True)


if __name__ == '__main__':
    main()

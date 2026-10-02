"""Intended-reason certificate rejection controls for the scalar checker."""
import argparse
import copy
import json
from pathlib import Path
import resource
import time

import verify as v


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    started = time.monotonic()
    v.INPUT = Path(args.input)
    certificate = json.loads(v.INPUT.read_text())
    context = v.make_context()
    cases = []

    def change(name, callback, reason):
        damaged = copy.deepcopy(certificate)
        callback(damaged)
        cases.append((name, damaged, reason))

    change('schema', lambda c: c.update(schema='wrong'), 'certificate schema or budget differs')
    change('input order', lambda c: c.update(n=14), 'certificate schema or budget differs')
    change('budget', lambda c: c.update(size_budget=45), 'certificate schema or budget differs')
    change('fixture binding', lambda c: c.update(fixture_sha256='0'*64), 'full cover fixture binding differs')
    change('prefix binding', lambda c: c['result'].update(prefix_sha256='0'*64), 'wrong prefix pin')
    change('first LOW merge', lambda c: c['result'].update(first_LOW_merge=[3,4]), 'wrong first LOW merge')
    change('preparation support', lambda c: c['result'].update(dead_ports=[5,6,7,9,10]), 'wrong dead ports')
    change('required repair record', lambda c: c['result']['repair_reserved_originals'][0]['record'].__setitem__(4,7), 'original repair/activity rows differ')
    change('activity image', lambda c: c['result']['activity_image_masks'].__setitem__(0,c['result']['activity_image_masks'][0]^1), 'original activity images differ')
    change('whole function', lambda c: c['result']['states'][1]['full64_function'].__setitem__(0,c['result']['states'][1]['full64_function'][0]^1), 'representative whole function differs')
    change('missing whole function', lambda c: c['result']['states'].pop(1), 'missing or duplicate function state')
    change('extra repeated representative gate', lambda c: c['result']['states'][1]['shortest_word'].append(c['result']['states'][1]['shortest_word'][-1]), 'representative shortest length differs')
    change('missing admissible edge', lambda c: c['result']['transitions'].pop(), 'entire admissible edge set differs')
    change('incomplete closure', lambda c: c['result'].update(complete_closure=False), 'incomplete closure')
    change('original deletion count', lambda c: c['result']['blocked'][0]['witness']['record'].__setitem__(4,8), 'selected original record differs')
    change('original restriction', lambda c: c['result']['blocked'][0]['witness']['record'].__setitem__(0,1), 'selected original is not tight')
    change('imported size bound', lambda c: c['result']['blocked'][0]['witness'].update(imported_size=34), 'wrong imported size')
    change('marked free-cut port', lambda c: c['result']['blocked'][0]['witness'].update(physical_port=12), 'selected cut port is marked')
    change('incorrect full rank witness', lambda c: c['result']['blocked'][0]['witness'].update(full_Boolean_witness=0), 'full wrong-rank witness differs')
    change('incorrect full witness value', lambda c: c['result']['blocked'][0]['witness'].update(actual_bit=1-c['result']['blocked'][0]['witness']['actual_bit']), 'full wrong-rank witness differs')
    rejected = []
    for name, damaged, reason in cases:
        try:
            v.verify(damaged,context)
        except ValueError as error:
            v.need(str(error) == reason, 'unintended rejection: '+name+': '+str(error))
            rejected.append(name)
        else:
            raise ValueError('damaged certificate accepted: '+name)
    expected = json.loads((v.SOURCE/'certificate.json').read_text())
    compact_cases = []
    for name in ('full_function_columns_sha256','entire_admissible_transitions_sha256','exit_bindings','repair_reservations'):
        damaged = copy.deepcopy(expected)
        if isinstance(damaged[name],list):
            damaged[name].pop()
        else:
            damaged[name] = '0'*64
        compact_cases.append((name,damaged))
    for name, damaged in compact_cases:
        try:
            v.check_compact(certificate,damaged)
        except ValueError as error:
            v.need(str(error) == 'compact mathematical binding differs', 'unintended compact rejection')
            rejected.append('compact '+name)
        else:
            raise ValueError('damaged compact binding accepted: '+name)
    positive = v.positive_controls()
    print(json.dumps({'agent':'six-sorting-2','role':'researcher',
                      'status':'ALL24_DAMAGES_REJECTED_FOR_INTENDED_REASONS',
                      'rejected':rejected,'positive_controls':positive,
                      'seconds':time.monotonic()-started,
                      'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__ == '__main__':
    main()

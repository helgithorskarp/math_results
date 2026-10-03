#!/usr/bin/env python3
"""Semantic damage controls; bypass byte seals to exercise mathematics."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import resource
import tempfile
import time
import decoder
import geometry as b
import polygon

HERE = Path(__file__).resolve().parent


def run():
    start = time.monotonic()
    raw = (HERE / 'witness_h7.txt').read_text().splitlines()
    fixtures = []
    x = list(raw); x[4] = x[4].replace('<1,0,', '<2,0,', 1)
    fixtures.append(('nonisometric linear map', x, 7, False))
    x = list(raw); x[4] = '1 <1,0,1,0,1,0>'
    fixtures.append(('off-lattice affine cell image', x, 7, False))
    x = list(raw); x[2] = str(int(x[2])+1); x.append(x[4])
    fixtures.append(('duplicate physical placement', x, 7, False))
    x = list(raw); x[2] = str(int(x[2])-1); del x[4]
    fixtures.append(('deleted first-corona placement', x, 7, False))
    fixtures.append(('wrong uncapped prototype for capped source',
                     (HERE / 'witness_h8l.txt').read_text().splitlines(), 8, False))
    records = []
    with tempfile.TemporaryDirectory(prefix='heesch-positive-controls-') as directory:
        for name, lines, m, cap in fixtures:
            path = Path(directory) / 'damaged.txt'
            path.write_text('\n'.join(lines) + '\n')
            reason = None
            try:
                witness, _ = decoder.decode(path, m, cap, HERE / 'drafter_tables.py')
                polygon.check(witness)
            except ValueError as error:
                reason = str(error)
            b.require(reason is not None, 'semantic damage accepted: ' + name)
            records.append({'case': name, 'rejected': True, 'reason': reason})
        # Exercise full-table coverage, rather than merely common prefix rows.
        import ast
        table_source = (HERE / 'drafter_tables.py').read_text()
        damaged_lines = []
        for line in table_source.splitlines():
            if line.startswith('DRAFTER_VERTICES = '):
                data = ast.literal_eval(line.split(' = ', 1)[1])
                line = 'DRAFTER_VERTICES = ' + repr(data[:-1])
            damaged_lines.append(line)
        path = Path(directory) / 'incomplete_tables.py'
        path.write_text('\n'.join(damaged_lines) + '\n')
        reason = None
        try:
            decoder.tables_match(path)
        except ValueError as error:
            reason = str(error)
        b.require(reason == 'incomplete fundamental triangle table',
                  'incomplete geometric lookup table accepted')
        records.append({'case': 'missing fundamental triangle row',
                        'rejected': True, 'reason': reason})
        # The foreign header never certifies the upper, or a false seventh lower.
        lines = list(raw); lines[1] = '~ 7 7 1'
        path = Path(directory) / 'unsupported-header.txt'
        path.write_text('\n'.join(lines) + '\n')
        witness, result = decoder.decode(path, 7, False, HERE / 'drafter_tables.py')
        b.require(max(r['level'] for r in witness['copies']) == 6 and
                  not result['global_finite_upper_claimed'], 'trusted a producer upper header')
        records.append({'case': 'unsupported seventh header',
                        'claimed_upper_ignored': True, 'actual_maximum_level': 6})
    out = {'actual_author': 'six-heesch-3', 'role': 'researcher', 'cases': records,
           'byte_integrity_seals_bypassed_to_test_semantics': True,
           'finite_upper_or_record_claimed': False}
    out['stable_full_record_sha256'] = sha256(json.dumps(out, sort_keys=True,
        separators=(',', ':')).encode()).hexdigest()
    out['elapsed_seconds'] = time.monotonic() - start
    out['peak_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return out


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))

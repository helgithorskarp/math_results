#!/usr/bin/env python3
"""Bounded data-integrity controls; run children sequentially."""
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    root = Path(__file__).resolve().parent
    expected = json.loads((root / 'EXPECTED.json').read_text())
    mutations = [('nine_incidence_records', 29), ('large_point_star_words', 31743),
                 ('own_incidence_records_sha256', '0' * 64),
                 ('degree_free_ten', {'forced_blue_small_pairs': 44})]
    count = 0
    with tempfile.TemporaryDirectory(prefix='independent-row-audit-') as tmp:
        temp = Path(tmp)
        for optimized in (False, True):
            prefix = [sys.executable, '-B'] + (['-O'] if optimized else [])
            for field, value in mutations:
                data = copy.deepcopy(expected)
                data[field] = value
                record = temp / 'wrong.json'
                record.write_text(json.dumps(data))
                r = subprocess.run(prefix + [str(root / 'audit.py'), '--expected', str(record)],
                                   capture_output=True, text=True, timeout=45)
                require(r.returncode != 0 and 'complete expected result equality' in r.stderr,
                        'damaged expected record rejected')
                count += 1
            # A separate scratch copy changes only the known-input bytes.
            (temp / 'audit.py').write_bytes((root / 'audit.py').read_bytes())
            (temp / 'EXPECTED.json').write_bytes((root / 'EXPECTED.json').read_bytes())
            (temp / 'primary21.txt').write_bytes((root / 'primary21.txt').read_bytes() + b' ')
            r = subprocess.run(prefix + [str(temp / 'audit.py')], capture_output=True,
                               text=True, timeout=45)
            require(r.returncode != 0 and 'unchanged primary21 bytes' in r.stderr,
                    'damaged known-input bytes rejected')
            count += 1
    require(count == 10, 'all data-integrity controls completed')
    print(json.dumps({'damaged_inputs_rejected': count,
                      'damage_types': 5, 'modes': ['normal', 'optimized']}, indent=2))


if __name__ == '__main__':
    main()

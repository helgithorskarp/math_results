#!/usr/bin/env python3
"""Small negative input checks; each subprocess is sequential and bounded."""
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    here = Path(__file__).resolve().parent
    expected = json.loads((here / 'expected.json').read_text())
    mutations = [
        ('gram', 'nine_row_canonical_incidences', 29),
        ('gram', 'nine_row_F_margin_rejections', 1259),
        ('gram', 'nine_row_records_sha256', '0' * 64),
        ('literal', 'nine_row_star_domain_sizes', [1]),
        ('literal', 'forced_red_page_counts', [3]),
        ('literal', 'literal_large_star_words', 30720),
    ]
    rejected = 0
    with tempfile.TemporaryDirectory(prefix='book-row-cap-') as tmp:
        root = Path(tmp)
        for optimized in (False, True):
            for index, (program, field, value) in enumerate(mutations):
                damaged = copy.deepcopy(expected)
                damaged[program][field] = value
                p = root / ('expected-%d.json' % index)
                p.write_text(json.dumps(damaged))
                cmd = [sys.executable, '-B'] + (['-O'] if optimized else [])
                cmd += [str(here / (program + '.py')), '--expected', str(p)]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                require(result.returncode != 0 and 'exact expected' in result.stderr,
                        'damaged expected result must be rejected')
                rejected += 1
            p = root / 'primary21-damaged.txt'
            p.write_bytes((here / 'primary21.txt').read_bytes() + b' ')
            cmd = [sys.executable, '-B'] + (['-O'] if optimized else [])
            cmd += [str(here / 'literal.py'), '--primary', str(p)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            require(result.returncode != 0 and 'unchanged primary21 fixture' in result.stderr,
                    'damaged fixture must be rejected')
            rejected += 1
    require(rejected == 14, 'complete normal/optimized negative controls')
    print(json.dumps({'damaged_input_rejections': rejected,
                      'modes': ['normal', 'optimized'],
                      'different_damage_types': 7}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()

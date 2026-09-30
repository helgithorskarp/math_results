#!/usr/bin/env python3
"""Proof-critical controls for the local-window transcript checker."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('generator', type=Path)
    parser.add_argument('checker', type=Path)
    parser.add_argument('--temp-root', type=Path, default=Path('build'))
    args = parser.parse_args()
    generator, checker = args.generator.resolve(), args.checker.resolve()
    args.temp_root.mkdir(parents=True, exist_ok=True)
    passed = []
    with tempfile.TemporaryDirectory(dir=args.temp_root) as name:
        work = Path(name)
        original = work/'phase0.bin'
        subprocess.run([str(generator), '0', '1', str(original)],
                       check=True, capture_output=True, text=True)
        data = original.read_bytes()

        def run(label, content, message, *extra):
            path = work/(label+'.bin')
            path.write_bytes(content)
            proc = subprocess.run([str(checker), *extra, str(path)],
                                  capture_output=True, text=True)
            if message is None:
                assert proc.returncode == 0, (label, proc.stderr)
                result = json.loads(proc.stdout)
                assert result['cases'] == 1233 and not result['full_domain'], result
                assert result['radius'] == 308 and result['packing_bound'] == 18
            else:
                assert proc.returncode != 0 and message in proc.stderr, (
                    label, proc.returncode, proc.stdout, proc.stderr)
            passed.append(label)

        chunk = ('--range', '0', '1')
        run('valid_chunk', data, None, *chunk)
        run('chunk_cannot_certify_full_domain', data, 'incomplete phase coverage')
        run('truncated_header', data[:10], 'truncated header', *chunk)
        run('truncated_last_packing', data[:-1], 'truncated packing', *chunk)
        run('trailing_byte', data+b'x', 'trailing bytes', *chunk)
        changed = bytearray(data); changed[0] ^= 1
        run('wrong_magic', changed, 'invalid magic', *chunk)
        for label, offset, value, message in (
                ('wrong_modulus', 8, 619, 'wrong modulus'),
                ('wrong_terms', 10, 6, 'progression length'),
                ('weaker_bound', 12, 17, 'packing bound'),
                ('wrong_window', 14, 617, 'window radius'),
                ('range_outside_request', 18, 2, 'outside expected range')):
            changed = bytearray(data)
            struct.pack_into('<H', changed, offset, value)
            run(label, changed, message, *chunk)
        changed = bytearray(data); struct.pack_into('<I', changed, 20, 1232)
        run('wrong_case_count', changed, 'wrong chunk case count', *chunk)
        changed = bytearray(data); struct.pack_into('<HH', changed, 24, 616, 0)
        run('constant_progression', changed, 'invalid crossing progression', *chunk)
        # All these are for first implicit case (s,t,e)=(0,0,1).
        changed = bytearray(data); struct.pack_into('<HH', changed, 24, 616, 1)
        run('pole_progression', changed, 'contains a pole', *chunk)
        changed = bytearray(data); struct.pack_into('<HH', changed, 24, 616, 2)
        run('nonmonochromatic_progression', changed, 'not monochromatic', *chunk)
        # A valid crossing AP in the full two-block domain, outside this window.
        changed = bytearray(data); struct.pack_into('<HH', changed, 24, 0, 103)
        run('outside_window', changed, 'invalid crossing progression', *chunk)
        changed = bytearray(data); changed[28:32] = changed[24:28]
        run('intersecting_progressions', changed, 'progressions intersect', *chunk)
        proc = subprocess.run([str(checker), *chunk, str(original), str(original)],
                              capture_output=True, text=True)
        assert proc.returncode != 0 and 'duplicate phase coverage' in proc.stderr, proc.stderr
        passed.append('duplicate_chunk')
    print(json.dumps({'status':'CONTROLS_PASSED','count':len(passed),'controls':passed}))


if __name__ == '__main__':
    main()

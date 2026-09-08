#!/usr/bin/env python3
"""Reproduce source identities, every certificate entry, and physical controls."""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main(catalog):
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != digest:
            raise ValueError('source integrity: ' + name)
    outputs = {}
    with tempfile.TemporaryDirectory(prefix='r55-degree-excess-') as scratch:
        for optimized in (False, True):
            python = [sys.executable] + (['-O'] if optimized else []) + ['-B']
            generated = Path(scratch) / ('optimized.json' if optimized else 'normal.json')
            subprocess.run(python + [str(HERE / 'produce.py'), '--output', str(generated)], check=True)
            if generated.read_bytes() != (HERE / 'CERTIFICATE.json').read_bytes():
                raise ValueError('regenerated certificate bytes')
            for script, args, expected in [
                    ('verify.py', ['--catalog', str(catalog), '--certificate', str(generated)], 'EXPECTED_VERIFY.json'),
                    ('controls.py', [], 'EXPECTED_CONTROLS.json'),
                    ('edge_window.py', ['--self-check'], 'EXPECTED_INTERFACE.json')]:
                result = subprocess.run(python + [str(HERE / script)] + args,
                                        check=True, capture_output=True, text=True)
                obj = json.loads(result.stdout)
                if obj != json.loads((HERE / expected).read_text()):
                    raise ValueError('expected result mismatch: ' + script)
                if optimized and outputs[script] != result.stdout:
                    raise ValueError('optimized mode mismatch: ' + script)
                outputs[script] = result.stdout
    return {'status': 'REPRODUCED_GLOBAL_GOOD43_EDGE_WINDOW', 'edge_window': [390, 513],
            'normal_and_optimized_agree': True, 'target_found': False,
            'certificate_sha256': hashlib.sha256((HERE / 'CERTIFICATE.json').read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--catalog', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(main(args.catalog.resolve()), sort_keys=True))

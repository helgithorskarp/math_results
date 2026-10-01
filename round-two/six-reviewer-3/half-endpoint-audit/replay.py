#!/usr/bin/env python3
"""Hash-bind pinned source downloads and replay sequential exact comparisons.

No graph, ledger, signing key or campaign installation is required. Network
access is only for frozen public GitHub source; Python 3.11+ standard library.
"""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import urllib.request

BASE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixture-damages', action='store_true',
                        help='also replay missing/malformed/altered external fixtures in both modes')
    args = parser.parse_args()
    inputs = json.loads((BASE/'INPUTS.json').read_text())
    env = dict(os.environ)
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
        env[key] = '1'
    begin = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='half-endpoint-replay-') as temp:
        root = Path(temp)
        original = root/'author'
        original.mkdir()
        for row in inputs['files']:
            require(len(row['commit']) == 40 and all(ch in '0123456789abcdef' for ch in row['commit']), 'source commit format')
            url = 'https://raw.githubusercontent.com/helgithorskarp/math_results/'+row['commit']+'/'+row['path']
            request = urllib.request.Request(url, headers={'User-Agent':'independent-math-replay/1.0'})
            with urllib.request.urlopen(request, timeout=20) as response:
                raw = response.read(row['bytes']+1)
                require(response.status == 200, 'pinned source download HTTP status')
            require(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'], 'pinned source bytes '+row['path'])
            dest = original/Path(row['path']).name if row['label'].startswith('author-') else root/row['label']
            dest.write_bytes(raw)
        require(len(list(original.iterdir())) == inputs['author_files'], 'complete original source download')
        for label, script, digest in [('independent', BASE/'audit.py', inputs['independent_record_sha256']),
                                      ('author', original/'verify.py', inputs['author_record_sha256'])]:
            output = []
            fixture = BASE/'EXPECTED.json' if label == 'independent' else original/'expected.json'
            if args.fixture_damages:
                altered = json.loads(fixture.read_text())
                altered['unexpected_extra_field'] = True
                (root/(label+'-altered.json')).write_text(json.dumps(altered))
                (root/(label+'-malformed.json')).write_text('{')
            for optimized in (False, True):
                command = [sys.executable, '-I', '-B']+(['-O'] if optimized else [])+[str(script)]
                full = command+(['--author-fixture',str(original/'expected.json')] if label == 'independent' else [])
                start = time.monotonic()
                result = subprocess.run(full, env=env, capture_output=True, text=True, timeout=20)
                require(result.returncode == 0 and result.stderr == '' and digest in result.stdout,
                        label+' complete replay failed: '+result.stderr)
                output.append(result.stdout)
                print(label, 'optimized' if optimized else 'normal',
                      round(time.monotonic()-start,3), 'seconds:', result.stdout.strip())
                if args.fixture_damages:
                    for kind in ('missing','malformed','altered'):
                        result = subprocess.run(command+['--fixture',str(root/(label+'-'+kind+'.json'))],
                                                env=env,capture_output=True,text=True,timeout=20)
                        require(result.returncode != 0, label+' accepted '+kind+' external fixture')
            require(output[0] == output[1], label+' normal/optimized full records differ')
        print('PASS',len(inputs['files']),'pinned source hashes; nine complete mathematical fields; sequential threads 1;',
              round(time.monotonic()-begin,3),'seconds total')


if __name__ == '__main__':
    main()

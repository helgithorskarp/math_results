#!/usr/bin/env python3
"""Download hash-bound public inputs and replay exact checks, sequentially.

Python3.11+ standard library; no graph, key, ledger or campaign installation.
All author stdout is compared with COMPLETE frozen bytes, not digest text.
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
    parser.add_argument('--fixture-damages', action='store_true')
    args = parser.parse_args()
    inputs = json.loads((BASE/'INPUTS.json').read_text())
    env = dict(os.environ)
    env.pop('PYTHONPATH', None)
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
        env[key] = '1'
    begin = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='two-fives-replay-') as temp:
        root = Path(temp)
        author = root/'author'
        author.mkdir()
        for row in inputs['files']:
            require(len(row['commit']) == 40 and all(ch in '0123456789abcdef' for ch in row['commit']), 'pinned commit format')
            url = 'https://raw.githubusercontent.com/helgithorskarp/math_results/'+row['commit']+'/'+row['path']
            request = urllib.request.Request(url,headers={'User-Agent':'independent-math-replay/1.0'})
            with urllib.request.urlopen(request, timeout=20) as response:
                raw = response.read(row['bytes']+1)
                require(response.status == 200, 'pinned source HTTP status')
            require(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'], 'pinned bytes '+row['path'])
            destination = author/Path(row['path']).name if row['label'].startswith('author-') else root/row['label']
            destination.write_bytes(raw)
        require(len(list(author.iterdir())) == inputs['author_files'], 'complete original source inputs')
        independent_stdout = ('PASS 266 exact checks; 8 damages rejected; full-record SHA256 '
                              +inputs['independent_record_sha256']+'\n').encode()
        outputs = {}
        for optimized in (False, True):
            mode = ['-O'] if optimized else []
            independent = [sys.executable,'-I','-B']+mode+[str(BASE/'audit.py')]
            start = time.monotonic()
            result = subprocess.run(independent+['--author-fixture',str(author/'EXPECTED.json')],
                                    env=env,capture_output=True,timeout=20)
            require(result.returncode == 0 and not result.stderr and result.stdout == independent_stdout,
                    'independent full frozen record and source fields')
            outputs.setdefault('independent',[]).append(result.stdout)
            print('independent', 'optimized' if optimized else 'normal',
                  round(time.monotonic()-start,3),'seconds:',result.stdout.decode().strip())
            for script, fixture in (('check.py','EXPECTED.json'),('audit.py','AUDIT_EXPECTED.json')):
                start = time.monotonic()
                result = subprocess.run([sys.executable,'-B']+mode+[str(author/script)],
                                        cwd=author,env=env,capture_output=True,timeout=20)
                require(result.returncode == 0 and not result.stderr
                        and result.stdout == (author/fixture).read_bytes(),
                        'author COMPLETE stdout fixture '+script)
                outputs.setdefault(script,[]).append(result.stdout)
                print('author',script,'optimized' if optimized else 'normal',
                      round(time.monotonic()-start,3),'seconds; complete fixture',len(result.stdout),'bytes')
            if args.fixture_damages:
                altered = json.loads((BASE/'EXPECTED.json').read_text())
                altered['endpoint_metric_records'][0]['class_gaps'][0] = '91/209'
                (root/'altered.json').write_text(json.dumps(altered))
                (root/'malformed.json').write_text('{')
                for kind in ('missing','malformed','altered'):
                    result = subprocess.run(independent+['--fixture',str(root/(kind+'.json'))],
                                            env=env,capture_output=True,timeout=20)
                    require(result.returncode != 0, 'accepted '+kind+' complete external fixture')
        require(all(rows[0] == rows[1] for rows in outputs.values()), 'whole normal/optimized outputs differ')
        print('PASS',len(inputs['files']),'pinned input hashes; ten complete source mathematical fields;',
              'six external fixture controls;' if args.fixture_damages else '',
              'threads 1; sequential; total',round(time.monotonic()-begin,3),'seconds')


if __name__ == '__main__':
    main()

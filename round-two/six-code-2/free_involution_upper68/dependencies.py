"""Replay three explicitly imported public lemmas, with pinned runtime bytes."""
from hashlib import sha256
import json
import os
import subprocess
import sys
from common import HERE, THREADS, require


def replay(repository, work):
    record = json.loads((HERE / 'DEPENDENCIES.json').read_text())
    for item in record['runtime_files']:
        path = repository / item['path']
        raw = path.read_bytes()
        require(len(raw) == item['bytes'] and sha256(raw).hexdigest() == item['sha256'],
                'published dependency bytes differ: ' + item['path'])
    environment = dict(os.environ)
    environment.update({key: '1' for key in THREADS})
    python = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else [])
    commands = [
        ('universal20', ['constant_weight_upper71_review1/verify.py',
         '--certificate', 'constant_weight_upper71_review1/certificate.json',
         '--baseline', 'constant_weight_upper71_review1/baseline69.txt', '--controls',
         '--expected', 'constant_weight_upper71_review1/expected.json']),
        ('absent_pair', ['constant_weight_absent_pair_review1/audit.py',
         '--check', 'constant_weight_absent_pair_review1/expected.json']),
        ('multiplicity_two', ['constant_weight_pair_two_review2/reproduce.py',
         '--work', str(work / 'pair-two-generated')])]
    results = []
    for name, command in commands:
        run = subprocess.run(python + command, cwd=repository, env=environment,
                             capture_output=True, text=True, timeout=60)
        (work / (name + '.stdout')).write_text(run.stdout)
        (work / (name + '.stderr')).write_text(run.stderr)
        require(run.returncode == 0, 'INCOMPLETE public dependency replay: ' + name)
        results.append(dict(name=name, complete=True))
        print('dependency COMPLETE', name, flush=True)
    return dict(replays=results, runtime_files=len(record['runtime_files']),
                transitive_upper57_census_rerun=False)

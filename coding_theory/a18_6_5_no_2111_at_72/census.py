"""Complete all mapping fibers, retaining private resumable native streams."""
from pathlib import Path
import hashlib
import json
import resource
import subprocess
import time

from paths import BASE, WORK
ROOT = WORK


def run_native(mode, count):
    started = time.monotonic()
    with (ROOT/'mapping_fibers.txt').open('rb') as matrix, (ROOT/f'all_{mode}.jsonl').open('w') as output, (ROOT/f'all_{mode}.stderr').open('w') as error:
        result = subprocess.run([str(ROOT/'pair_fibers.exe'), mode, '0', str(count), '200000', '10'],
                                stdin=matrix, stdout=output, stderr=error, timeout=300)
    if result.returncode:
        raise RuntimeError('INCOMPLETE native census: '+(ROOT/f'all_{mode}.stderr').read_text()[:1000])
    return round(time.monotonic()-started, 6)


def run():
    started = time.monotonic()
    spec = json.loads((ROOT/'mapping_specs.json').read_text())
    if hashlib.sha256((ROOT/'mapping_fibers.txt').read_bytes()).hexdigest() != spec['matrix_sha256']:
        raise RuntimeError('matrix fingerprint differs')
    status = dict(agent='six-code-3', role='researcher', status='INCOMPLETE',
                  matrix_sha256=spec['matrix_sha256'], completed_modes=[])
    path = ROOT/'census.json'
    path.write_text(json.dumps(status, indent=2)+'\n')
    count = len(spec['fibers'])
    status['prune_seconds'] = run_native('prune', count)
    status['completed_modes'].append('prune')
    path.write_text(json.dumps(status, indent=2)+'\n')
    print('pruned census COMPLETE', status['prune_seconds'], flush=True)
    status['literal_seconds'] = run_native('literal', count)
    status['completed_modes'].append('literal')
    print('literal census COMPLETE', status['literal_seconds'], flush=True)
    pairs = {}
    primary_nodes = literal_nodes = maximum_nodes = 0
    positive_fibers = 0
    largest_count = 0
    with (ROOT/'all_prune.jsonl').open() as a, (ROOT/'all_literal.jsonl').open() as b:
        for i, entry in enumerate(spec['fibers']):
            left = json.loads(a.readline())
            right = json.loads(b.readline())
            if (left['index'] != i or right['index'] != i or left['status'] != 'COMPLETE'
                    or right['status'] != 'COMPLETE' or left['accepted'] != right['accepted']
                    or len(set(left['accepted'])) != len(left['accepted'])
                    or left['accepted'] != sorted(left['accepted'])
                    or any(type(r) is not int or not 0 <= r < 5040 for r in left['accepted'])):
                raise RuntimeError('native complete output differs entrywise or is malformed')
            key = (entry['first'], entry['second'])
            pairs.setdefault(key, dict(first=key[0], second=key[1], fibers=0,
                                       positive_fibers=0, normalized_maps=0, raw_compatible_maps=0))
            pair = pairs[key]
            n = len(left['accepted'])
            pair['fibers'] += 1
            pair['positive_fibers'] += bool(n)
            pair['normalized_maps'] += n
            pair['raw_compatible_maps'] += n*entry['orbit_size']
            primary_nodes += left['nodes']
            literal_nodes += right['nodes']
            maximum_nodes = max(maximum_nodes, left['nodes'])
            largest_count = max(largest_count, n)
            positive_fibers += bool(n)
        if a.read().strip() or b.read().strip():
            raise RuntimeError('extra native output fibers')
    if len(pairs) != 64 or literal_nodes != 5040*count:
        raise RuntimeError('incomplete ordered-pair or literal mapping domain')
    status.update(status='COMPLETE compatibility census; two algorithms agree entrywise',
                  fibers=count, positive_fibers=positive_fibers, pairs=[pairs[k] for k in sorted(pairs)],
                  primary_nodes=primary_nodes, literal_nodes=literal_nodes,
                  max_primary_nodes=maximum_nodes, largest_fiber_accepted=largest_count,
                  normalized_compatible_maps=sum(p['normalized_maps'] for p in pairs.values()),
                  raw_compatible_maps=sum(p['raw_compatible_maps'] for p in pairs.values()),
                  seconds=round(time.monotonic()-started, 6),
                  parent_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    path.write_text(json.dumps(status, indent=2)+'\n')
    for first in range(8):
        print('first', first, 'raw compatible maps',
              [pairs[(first, second)]['raw_compatible_maps'] for second in range(8)], flush=True)
    print({k:status[k] for k in ['status','fibers','positive_fibers','normalized_compatible_maps',
                               'raw_compatible_maps','primary_nodes','max_primary_nodes','seconds']})
    return status


if __name__ == '__main__':
    run()

"""Compact replay; full representative audits are deliberately opt-in."""
from pathlib import Path
import argparse
import hashlib
import json
import time
import audit
import bounds

HERE = Path(__file__).resolve().parent


def manifest():
    count = 0
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        wanted, name = line.split('  ', 1)
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest() != wanted:
            raise ValueError('source identity: '+name)
        count += 1
    return count


def main(cache=None, shard=0, shards=1):
    start = time.monotonic(); expected = json.loads((HERE/'VALIDATION.json').read_text())
    controls = audit.propagation_controls(); exact = bounds.rows()
    if controls != expected['controls'] or exact != expected['exact_bounds']:
        raise ValueError('compact expected result')
    tasks = []
    if cache is not None:
        names = [row['task'] for row in json.loads(audit.REPRESENTATIVES.read_text())]
        tasks = [audit.compare_task(name, cache) for name in names[shard::shards]]
        published = {row['task']: row for row in json.loads((HERE/'REPRESENTATIVE_AUDIT.json').read_text())['tasks']}
        for task in tasks:
            if json.loads(json.dumps(task)) != published[task['task']]:
                raise ValueError('full representative replay mismatch')
    return {'status': 'VERIFIED_TRIANGLE_INTERFACE_REPLAY', 'manifest_entries': manifest(),
            'controls': controls, 'exact_bounds': exact, 'representative_tasks_audited': len(tasks),
            'shard': shard, 'shards': shards, 'solver_calls': 0,
            'seconds': time.monotonic()-start}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--cache', type=Path)
    parser.add_argument('--shard', type=int, default=0); parser.add_argument('--shards', type=int, default=1)
    args = parser.parse_args()
    if not 0 <= args.shard < args.shards:
        raise ValueError('shard range')
    print(json.dumps(main(args.cache, args.shard, args.shards), indent=2, sort_keys=True))

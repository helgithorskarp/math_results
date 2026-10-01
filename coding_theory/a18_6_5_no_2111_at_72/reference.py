"""Measure and independently check every fiber of the first star pair."""
from itertools import combinations, permutations
from pathlib import Path
import json
import resource
import subprocess
import time

from paths import WORK
ROOT = WORK


def native(mode, end):
    started = time.monotonic()
    with (ROOT/'mapping_fibers.txt').open('rb') as matrix:
        result = subprocess.run([str(ROOT/'pair_fibers.exe'), mode, '0', str(end), '200000', '10'],
                                stdin=matrix, capture_output=True, text=True, timeout=60)
    (ROOT/f'pilot_{mode}.jsonl').write_text(result.stdout)
    if result.returncode:
        raise RuntimeError(result.stderr)
    records = [json.loads(line) for line in result.stdout.splitlines()]
    if len(records) != end or any(r['status'] != 'COMPLETE' for r in records):
        raise RuntimeError('INCOMPLETE native pilot')
    return records, round(time.monotonic()-started, 6)


def literal_python(entry, first, second):
    started = time.monotonic()
    image = entry['fixed'][:]
    source_free = [u for u, v in enumerate(image) if v == -1]
    target_free = sorted(set(range(16))-set(image))
    ar = [w >> 1 for w in first['words'] if not w & 1]
    br = [[u for u in range(16) if w >> (u+1) & 1] for w in second['words'] if not w & 1]
    accepted = []
    nodes = 0
    for ordinal, assignment in enumerate(permutations(target_free)):
        nodes += 1
        if nodes % 128 == 0 and time.monotonic()-started > 10:
            raise RuntimeError('INCOMPLETE reference mapping fiber time guard')
        for u, v in zip(source_free, assignment):
            image[u] = v
        mapped = [sum(1 << image[u] for u in word) for word in br]
        if any((a & b).bit_count() > 2 for b in mapped for a in ar):
            continue
        accepted.append(ordinal)
        # Separate literal full five-word witness check, with both centers restored.
        left = {w | (1 << 17) for w in first['words']}
        right = {1 | sum(1 << (17 if u == 0 else image[u-1]+1)
                         for u in range(17) if w >> u & 1) for w in second['words']}
        union = left | right
        if (len(left & right) != 3 or len(union) != 37
                or any(w.bit_count() != 5 for w in union)
                or any((u & v).bit_count() > 2 for u, v in combinations(union, 2))
                or sum(bool(w & 1) for w in union) != 20
                or sum(bool(w & (1 << 17)) for w in union) != 20):
            raise RuntimeError('accepted map fails full literal thirty-seven-word check')
    if nodes != 5040 or time.monotonic()-started > 10:
        raise RuntimeError('INCOMPLETE reference mapping domain/guard')
    return dict(index=entry['index'], status='COMPLETE', nodes=nodes,
                seconds=round(time.monotonic()-started, 6), accepted=accepted)


def run():
    carrier = json.loads((ROOT/'tail_carrier.json').read_text())
    specs = json.loads((ROOT/'mapping_specs.json').read_text())['fibers']
    end = carrier['pairs'][0]['orbit_count']
    first, seconds_prune = native('prune', end)
    second, seconds_literal = native('literal', end)
    separate = []
    for i in range(end):
        record = literal_python(specs[i], carrier['stars'][0], carrier['stars'][0])
        if not first[i]['accepted'] == second[i]['accepted'] == record['accepted']:
            raise RuntimeError('three independent complete outputs differ entrywise')
        separate.append(record)
        print(i, 'accepted', len(record['accepted']), 'python seconds', record['seconds'], flush=True)
        (ROOT/'pilot_python.json').write_text(json.dumps(separate, indent=2)+'\n')
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE first0/second0 mapping census',
                  fibers=end, accepted_maps_in_normalized_prefixes=sum(len(q['accepted']) for q in first),
                  raw_compatible_maps=sum(len(first[i]['accepted'])*specs[i]['orbit_size'] for i in range(end)),
                  prune_seconds=seconds_prune, cpp_literal_seconds=seconds_literal,
                  python_seconds=sum(q['seconds'] for q in separate),
                  primary_nodes=sum(q['nodes'] for q in first), max_primary_nodes=max(q['nodes'] for q in first),
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    (ROOT/'pilot_summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result)
    return result


if __name__ == '__main__':
    run()

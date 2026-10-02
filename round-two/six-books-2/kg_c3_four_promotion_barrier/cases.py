"""Partition every J3/P4 choice by the checked six-element orbit action.

Each completed J block enumerates all 52360 promoted quadruples. The merge
is separate and compares direct labeled counts to every explicit group orbit.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import sys
import time

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE
sys.path.insert(0, str(PREVIOUS))
import model as m


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def group():
    geometry = m.geometry()
    effective = sorted(set(tuple(tuple(x) for x in entry) for entry in m.centralizer(geometry)))
    m.need(len(effective) == 6, 'effective action order')
    return effective


def partition(work, seconds):
    started = time.monotonic()
    work.mkdir(parents=True, exist_ok=True)
    source = {p.name: digest(p) for p in (Path(__file__), PREVIOUS/'model.py')}
    effective = group()
    joins = list(combinations(range(7), 3))
    first = 0
    while (work/f'join-{first:02d}.metadata.json').exists():
        meta = json.loads((work/f'join-{first:02d}.metadata.json').read_text())
        m.need(meta['join_index'] == first and meta['J'] == list(joins[first]) and
               meta['sources'] == source, 'completed J-block input/source')
        m.need(digest(work/f'join-{first:02d}.txt') == meta['sha256'], 'completed J-block bytes')
        first += 1
    m.need(first <= 35 and not any((work/f'join-{i:02d}.metadata.json').exists()
           for i in range(first+1, 35)), 'consecutive completed J-blocks')
    next_index = first
    for join_index in range(first, 35):
        if next_index > first and time.monotonic()-started >= seconds:
            break
        J = joins[join_index]
        counts = Counter()
        transforms = [(tuple(sorted(v[i] for i in J)), b) for v, r, b in effective]
        for P in combinations(range(35), 4):
            key = min((image, tuple(sorted(b[i] for i in P))) for image, b in transforms)
            counts[key] += 1
        m.need(sum(counts.values()) == 52360, 'complete promoted-quadruple block')
        path = work/f'join-{join_index:02d}.txt'
        m.need(not path.exists(), 'refuse unconfirmed existing block output')
        path.write_text(''.join(' '.join(map(str, (*key[0], *key[1], count)))+'\n'
                                for key, count in sorted(counts.items())))
        meta = dict(join_index=join_index, J=J, labeled=52360, canonical_keys=len(counts),
                    sha256=digest(path), sources=source)
        (work/f'join-{join_index:02d}.metadata.json').write_text(json.dumps(meta, indent=2)+'\n')
        next_index += 1
    return dict(status='ALL_J_BLOCKS_COMPLETE' if next_index == 35 else 'COMPLETED_J_PREFIX',
                first=first, next=next_index, total=35, seconds=time.monotonic()-started,
                sources=source, peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def merge(work):
    started = time.monotonic()
    effective = group()
    counts = Counter()
    joins = list(combinations(range(7), 3))
    for index, J in enumerate(joins):
        path = work/f'join-{index:02d}.txt'
        meta = json.loads((work/f'join-{index:02d}.metadata.json').read_text())
        m.need(meta['J'] == list(J) and meta['join_index'] == index and digest(path) == meta['sha256'], 'J-block identity/hash')
        block_total = 0
        with path.open() as stream:
            for line in stream:
                fields = tuple(map(int, line.split()))
                m.need(len(fields) == 8 and fields[-1] > 0, 'partition record')
                key = (fields[:3], fields[3:7])
                counts[key] += fields[-1]
                block_total += fields[-1]
        m.need(block_total == 52360, 'complete J block labeled total')
    m.need(sum(counts.values()) == 1832600, 'full labeled product domain')
    output = work/'cases.txt'
    m.need(not output.exists(), 'case manifest already exists')
    with output.open('w') as stream:
        for index, ((J, P), weight) in enumerate(sorted(counts.items())):
            orbit = {(tuple(sorted(v[i] for i in J)), tuple(sorted(b[i] for i in P)))
                     for v, r, b in effective}
            m.need(weight == len(orbit) and min(orbit) == (J, P) and 6 % weight == 0,
                   'direct complete-domain count vs explicit full orbit')
            stream.write(' '.join(map(str, (index, *J, *P, weight)))+'\n')
    result = dict(status='COMPLETE_EXPLICIT_CASE_QUOTIENT', labeled=1832600,
        representatives=len(counts), multiplicities=dict(sorted(Counter(counts.values()).items())),
        manifest_sha256=digest(output), manifest_bytes=output.stat().st_size,
        sources={p.name:digest(p) for p in (Path(__file__), PREVIOUS/'model.py')},
        seconds=time.monotonic()-started, peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (work/'cases.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--seconds', type=float, default=25)
    ap.add_argument('--merge', action='store_true')
    args = ap.parse_args()
    m.need(0 < args.seconds <= 25, 'bounded phase')
    print(json.dumps(merge(args.work) if args.merge else partition(args.work, args.seconds), indent=2))

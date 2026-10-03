"""Positive actual D/y point images of the specified Q and two extra parents.

six-code-2, researcher. The four generators are credited to the retained
C23 source. No full automorphism order or all h6 boundary coverage is assumed.
"""
import argparse
from operations import check_operations
from collections import deque
import hashlib
import json
import os
from pathlib import Path
import resource
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def main():
    parser = argparse.ArgumentParser()
    for key in ('parent', 'spec', 'work'):
        parser.add_argument('--' + key, type=Path, required=True)
    args = parser.parse_args()
    need(not args.work.exists(), 'fresh h6 point image directory required')
    args.work.mkdir(parents=True)
    begin, states = time.monotonic(), 0

    def guard():
        check_operations()
        need(time.monotonic() - begin < 60 and states <= 2000000,
             'INCOMPLETE original60s/two-million h6 point image guard')

    parent_raw = args.parent.read_bytes()
    spec_raw = args.spec.read_bytes()
    spec = json.loads(spec_raw)
    need(hashlib.sha256(parent_raw).hexdigest() == spec['literal_parent_sha256'], 'literal D source bytes')
    words = tuple(sorted(json.loads(parent_raw)['words']))
    need(len(words) == len(set(words)) == 68 and all(type(w) is int and 0 <= w < 1 << 17 and w.bit_count() == 5 for w in words),
         'literal D domain')
    old_set = set(words)
    q, extras = spec['noncontained_q'], tuple(spec['extra_empty_parents'])
    need(type(q) is int and q.bit_count() == 4 and 0 <= q < 1 << 17 and not any(q & b == q for b in words),
         'literal noncontained Q')
    blockers = tuple(b for b in words if (q & b).bit_count() >= 3)
    need(len(blockers) == 4 and len(extras) == len(set(extras)) == 2 and set(extras) <= old_set and not set(extras) & set(blockers),
         'literal two extra parents outside reserved four')
    bits = {w: tuple(v for v in range(17) if w >> v & 1) for w in set(words) | {q}}

    def image(w, p):
        return sum(1 << p[v] for v in bits[w])

    def check_map(p):
        need(len(p) == 18 and all(type(v) is int for v in p) and sorted(p) == list(range(18)) and p[17] == 17,
             'actual y-fixed point bijection')
        need({image(w, p) for w in words} == old_set, 'actual whole D image')

    generators = tuple(tuple(p) for p in spec['point_generators'])
    for p in generators:
        check_map(p)
    identity = tuple(range(18))
    maps, seen, queue = [identity], {identity}, deque([identity])
    while queue:
        p = queue.popleft()
        for g in generators:
            states += 1
            new = tuple(g[p[v]] for v in range(18))
            if new not in seen:
                seen.add(new); maps.append(new); queue.append(new)
        if states % 1024 == 0:
            guard()
    need(len(maps) == spec['expected_generated_actual_maps'], 'generated subgroup count differs')
    targets = {}
    stabilizer_pairs = set()
    for index, p in enumerate(maps):
        states += 1
        check_map(p)
        iq = image(q, p)
        ie = tuple(sorted(image(w, p) for w in extras))
        actual_blockers = {b for b in words if (b & iq).bit_count() >= 3}
        need(actual_blockers == {image(w, p) for w in blockers} and not actual_blockers & set(ie),
             'whole transported Q and six-parent boundary')
        targets.setdefault((iq, *ie), index)
        if iq == q:
            stabilizer_pairs.add(ie)
        if index % 128 == 0:
            guard()
    guard()
    packet = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'COMPLETE_POSITIVE_ACTUAL_POINT_IMAGES_OF_ONE_LITERAL_H6_PAIR',
              'parent_sha256': hashlib.sha256(parent_raw).hexdigest(), 'spec_sha256': hashlib.sha256(spec_raw).hexdigest(),
              'parent_words': words, 'noncontained_q': q, 'additional_empty_parents': sorted(extras),
              'hole_words': sorted(set(blockers) | set(extras)), 'point_maps': maps,
              'targets': [list(key) + [targets[key]] for key in sorted(targets)],
              'generated_map_count': len(maps), 'target_count': len(targets),
              'Q15_stabilizer_extra_pairs': sorted(stabilizer_pairs),
              'full_automorphism_order_assumed': False, 'minimal_orbits_assumed': False,
              'all_extra_pairs_or_global_endpoint_claim': False}
    raw = encoded(packet); (args.work / 'COVER.json').write_bytes(raw)
    result = {'agent': 'six-code-2', 'role': 'researcher', 'status': packet['status'],
              'maps': len(maps), 'targets': len(targets), 'distinct_Q_images': len({key[0] for key in targets}),
              'Q15_extra_pairs': sorted(stabilizer_pairs), 'states': states,
              'cover_bytes': len(raw), 'cover_sha256': hashlib.sha256(raw).hexdigest(),
              'original_seconds': 60, 'original_states': 2000000}
    (args.work / 'EXACT_RESULT.json').write_bytes(encoded(result))
    execution = {'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (args.work / 'EXECUTION.json').write_bytes(encoded(execution))
    print(json.dumps(result | execution, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()

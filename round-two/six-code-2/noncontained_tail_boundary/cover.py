"""Positive point maps covering every noncontained old four-tail of classicalD.

Four literal seed-preserving bijections produce candidate maps. This is
positive coverage only: neither group-order completeness nor target-code
symmetry is assumed. The final maps are individually checked on all68
parent words and against an independently enumerated physical domain.
"""
import argparse
from collections import deque
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def image(word, p):
    return sum(1 << p[v] for v in range(18) if word >> v & 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    need(not args.work.exists(), 'fresh positive noncontained-Q-cover directory required')
    args.work.mkdir(parents=True)
    begin = time.monotonic()
    raw = args.parent.read_bytes()
    old = tuple(sorted(json.loads(raw)['words']))
    need(len(old) == len(set(old)) == 68, 'literal parent count')
    old_set = set(old)
    expected = {sum(1 << v for v in ps) for ps in combinations(range(17), 4)
                if not any(set(ps) <= {v for v in range(17) if w >> v & 1} for w in old)}
    need(len(expected) == 2040, 'all physical2040 noncontained four-tails')
    # Credited literal generators of prior standard-plane semilinear maps;
    # conjugate by the actual previously checked standard-to-coalesced map.
    q = (0, 1, 2, 14, 4, 6, 13, 3, 12, 9, 10, 5, 11, 15, 8, 7, 16, 17)
    qinv = tuple(q.index(v) for v in range(18))
    standard = (
        (1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 16, 17),
        (0, 4, 8, 12, 6, 2, 14, 10, 11, 15, 3, 7, 13, 9, 5, 1, 16, 17),
        (16, 1, 3, 2, 15, 12, 9, 11, 10, 6, 8, 7, 5, 14, 13, 4, 0, 17),
        (0, 1, 3, 2, 6, 7, 5, 4, 13, 12, 14, 15, 11, 10, 8, 9, 16, 17))
    generators = tuple(tuple(q[g[qinv[v]]] for v in range(18)) for g in standard)
    for p in generators:
        need(sorted(p) == list(range(18)) and p[17] == 17 and
             {image(w, p) for w in old} == old_set, 'literal generator fails whole parent')
    canonical = 15
    need(canonical in expected, 'canonicalQ is not physically noncontained')
    identity = tuple(range(18))
    seen, todo, maps, states = {identity}, deque([identity]), {}, 0
    while todo and len(maps) < len(expected):
        p = todo.popleft()
        target = image(canonical, p)
        need(target in expected, 'positive target outside physical noncontained-Q carrier')
        if target not in maps:
            need(sorted(p) == list(range(18)) and p[17] == 17 and
                 {image(w, p) for w in old} == old_set, 'selected map fails whole parent')
            maps[target] = p
        for g in generators:
            states += 1
            nxt = tuple(g[p[v]] for v in range(18))
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
        if states % 1024 == 0:
            need(states <= 2_000_000 and time.monotonic() - begin < 60,
                 'INCOMPLETE initial60s/two-million positive-cover guard')
    need(set(maps) == expected, 'positive maps do not cover every1360 noncontained-Q triple')
    rows = [{'target_q': t, 'point_map': maps[t]} for t in sorted(maps)]
    packet = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'POSITIVE_ACTUAL_ALL2040_NONCONTAINED_Q_POINT_MAPS',
              'canonical_q': canonical, 'parent_words': old, 'maps': rows,
              'scope': 'Every old four-tail not contained inD. All selected maps fixy and preserve wholeD. No target symmetry or group-order/closure completeness premise.'}
    b = encoded(packet)
    (args.work / 'NONCONTAINED_Q_MAPS.json').write_bytes(b)
    record = {'agent': 'six-code-2', 'role': 'researcher', 'status': packet['status'],
              'physical_old_four_tails': 2380, 'physical_noncontained_four_tails': 2040,
              'positive_maps': len(rows), 'whole_parent_images': len(rows) * 68,
              'generated_candidate_maps': len(seen), 'generator_compositions': states,
              'parent_input_sha256': hashlib.sha256(raw).hexdigest(), 'certificate_bytes': len(b),
              'certificate_sha256': hashlib.sha256(b).hexdigest(),
              'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'initial_whole_guard_seconds': 60, 'initial_state_guard': 2_000_000,
              'independent_positive_cover_audit': 'pending; whole-parent images checked in this producer'}
    (args.work / 'SUMMARY.json').write_bytes(encoded(record))
    print(json.dumps(record, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()

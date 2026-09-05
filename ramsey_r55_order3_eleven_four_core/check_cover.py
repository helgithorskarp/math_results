#!/usr/bin/env python3
"""Independent literal graph census, full-group orbits and 43-vertex normalization audit."""
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import hashlib
import json
import resource
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sigma(v):
    return 3*(v//3)+(v+1) % 3 if v < 33 else v


def core_positions():
    ids = {}
    representatives = []
    for i, j in combinations(range(4), 2):
        for d in range(3):
            orbit = [tuple(sorted((3*i+t, 3*j+(t+d) % 3))) for t in range(3)]
            index = len(representatives)
            representatives.append((3*i, 3*j+d))
            for p in orbit:
                ids[p] = index
    return ids, representatives


def graph(code, ids):
    rows = [0]*12
    for a, b in combinations(range(12), 2):
        red = a//3 == b//3 or bool(code & (1 << ids[a, b]))
        if red:
            rows[a] |= 1 << b
            rows[b] |= 1 << a
    return rows


def clique(rows, vertices, size):
    if size == 0:
        return True
    while vertices.bit_count() >= size:
        bit = vertices & -vertices
        vertices ^= bit
        if clique(rows, vertices & rows[bit.bit_length()-1], size-1):
            return True
    return False


def normalized(rows):
    words = [tuple(int(bool(rows[0] & (1 << v))) for v in range(t, t+3)) for t in (3, 6, 9)]
    return all(w in ((0, 0, 0), (1, 0, 0), (1, 1, 0)) for w in words) and list(map(sum, words)) == sorted(map(sum, words))


def normalizes(tau, sign):
    return all(tau[sigma(v)] == (sigma(tau[v]) if sign == 1 else sigma(sigma(tau[v]))) for v in range(43))


def full_maps():
    maps = []
    for pi in permutations(range(4)):
        for shifts in product(range(3), repeat=4):
            for sign in (1, -1):
                tau = [3*pi[i]+(sign*s+shifts[i]) % 3 for i in range(4) for s in range(3)]
                tau += [3*i+(sign*s) % 3 for i in range(4, 11) for s in range(3)]+list(range(33, 43))
                require(sorted(tau) == list(range(43)) and normalizes(tau, sign), 'full normalizer identity')
                maps.append(tau)
    require(len({tuple(t) for t in maps}) == 3888, 'full-map census')
    bad = list(range(43))
    for i in range(4):
        bad[3*i+1], bad[3*i+2] = bad[3*i+2], bad[3*i+1]
    require(not normalizes(bad, 1) and not normalizes(bad, -1), 'minority-only inversion accepted')
    later = []
    for i in range(4, 11):
        tau = list(range(43))
        tau[3*i:3*i+3] = [3*i+1, 3*i+2, 3*i]
        later.append(tau)
    for i in range(4, 10):
        tau = list(range(43))
        tau[3*i:3*i+6] = list(range(3*i+3, 3*i+6))+list(range(3*i, 3*i+3))
        later.append(tau)
    for i in range(33, 42):
        tau = list(range(43))
        tau[i], tau[i+1] = tau[i+1], tau[i]
        later.append(tau)
    require(len(later) == 22 and all(t[:12] == list(range(12)) and normalizes(t, 1) for t in later), 'later core-preserving maps')
    return maps


def primary43(reps):
    classes = set()
    for a, b in combinations(range(43), 2):
        if b < 33 and a//3 == b//3:
            continue
        orbit = []
        for _ in range(3):
            orbit.append(tuple(sorted((a, b))))
            a, b = sigma(a), sigma(b)
        classes.add(min(orbit))
    cross = sorted(p for p in classes if p[1] < 33)
    fixed = sorted(p for p in classes if p[0] >= 33)
    links = sorted((p for p in classes if p[0] < 33 <= p[1]), key=lambda p: p[::-1])
    require((len(cross), len(fixed), len(links)) == (165, 45, 110), 'full primary census')
    ids = {p: i+1 for i, p in enumerate(cross+fixed+links)}
    return [ids[p] for p in reps]


def dig(values):
    return hashlib.sha256(''.join(str(v)+'\n' for v in sorted(values)).encode()).hexdigest()


def preflight(cover):
    require(cover['format'] == 'r55-k11-four-core-cover-v1' and cover['classes'] == 197, 'cover format')
    cases = cover['cases']
    require(len(cases) == 197 and [r['index'] for r in cases] == list(range(197)), 'case coverage')
    require(len({r['bits'] for r in cases}) == 197, 'duplicate representative')
    units = primary43(core_positions()[1])
    for row in cases:
        bits = row['bits']
        require(len(bits) == 18 and set(bits) <= {'0', '1'}, 'bit string')
        code = sum(int(b) << i for i, b in enumerate(bits))
        require(code == row['code'], 'bit/code mismatch')
        require(row['units'] == [v if code >> i & 1 else -v for i, v in enumerate(units)], 'unit meanings')


def audit(cover, work):
    start = time.monotonic()
    preflight(cover)
    ids, reps = core_positions()
    valid, normalized_count = set(), 0
    for code in range(2**18):
        rows = graph(code, ids)
        blue = [4095 ^ (1 << i) ^ row for i, row in enumerate(rows)]
        if not clique(rows, 4095, 5) and not clique(blue, 4095, 5):
            valid.add(code)
            normalized_count += normalized(rows)
    print('PASS literal 262144-graph census '+str(len(valid)), flush=True)
    require(cover['raw_binary'] == 2**18 and cover['labeled_valid'] == len(valid) and cover['valid_sha256'] == dig(valid), 'literal validity census')
    require(cover['normalized_valid'] == normalized_count, 'normalized census')
    noncomplete = {code for code in range(2**18) if all(code >> (3*i) & 7 != 7 for i in range(6))}
    patterns = cover['forbidden_patterns']
    require(len(patterns) == 108 and len(set(patterns)) == 108 and all(p.bit_count() == 9 for p in patterns), 'pattern format')
    require({code for code in noncomplete if not any(code & p == p for p in patterns)} == valid, 'complete occupancy criterion')
    require(cover['noncomplete'] == len(noncomplete) and cover['labeled_invalid'] == len(noncomplete)-len(valid), 'noncomplete census')
    maps = full_maps()
    effective = {tuple(ids[tuple(sorted((tau[a], tau[b])))] for a, b in reps) for tau in maps}
    require(len(effective) == cover['effective_core_maps'] == 1296 and cover['normalizer_maps'] == len(maps), 'effective action')
    units = primary43(reps)
    seen, member_pairs = set(), []
    class_hashes = []
    cases = cover['cases']
    require(len(cases) == cover['classes'] == 197 and [r['index'] for r in cases] == list(range(197)), 'class labels')
    require([r['bits'] for r in cases] == sorted(r['bits'] for r in cases), 'class order')
    for case in cases:
        code = sum(int(b) << i for i, b in enumerate(case['bits']))
        require(len(case['bits']) == 18 and set(case['bits']) <= {'0', '1'} and case['code'] == code, 'representative encoding')
        rows = graph(code, ids)
        orbit = set()
        for tau in maps:
            transported = 0
            for i, (a, b) in enumerate(reps):
                if rows[tau[a]] & (1 << tau[b]):
                    transported |= 1 << i
            orbit.add(transported)
        require(orbit <= valid and not orbit & seen, 'invalid or overlapping class')
        choices = [''.join(str(x >> i & 1) for i in range(18)) for x in orbit if normalized(graph(x, ids))]
        require(choices and min(choices) == case['bits'], 'normalized representative choice')
        require((len(orbit), len(choices), dig(orbit)) == (case['labeled'], case['normalized'], case['members_sha256']), 'complete member comparison')
        require(case['units'] == [v if code >> i & 1 else -v for i, v in enumerate(units)], 'full-graph primary cube')
        seen |= orbit
        member_pairs.extend((x, code) for x in orbit)
        class_hashes.append(case['members_sha256'])
    require(seen == valid, 'full coverage')
    member_hash = hashlib.sha256(''.join(f'{a} {b}\n' for a, b in sorted(member_pairs)).encode()).hexdigest()
    require(member_hash == cover['membership_sha256'], 'complete membership table')
    report = dict(verified=True, binary_graphs_checked=2**18, locally_valid=len(valid), classes=len(cases),
                  normalized_cores=normalized_count, full_maps=len(maps), effective_core_maps=len(effective),
                  literal_core_transports=len(maps)*len(cases), later_generators=22,
                  rejected_partial_inversion=True, primary_variables=320, cube_variables=units,
                  valid_sha256=dig(valid), membership_sha256=member_hash, class_hashes=class_hashes)
    work.mkdir(parents=True, exist_ok=True)
    (work / 'report.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    (work / 'measurement.json').write_text(json.dumps(dict(elapsed_seconds=round(time.monotonic()-start, 6),
                                                         maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss), indent=2)+'\n')
    print('PASS all 197 literal full-group orbits and complete normalization bridge', flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--cover', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    a = p.parse_args()
    audit(json.loads(a.cover.read_text()), a.work)

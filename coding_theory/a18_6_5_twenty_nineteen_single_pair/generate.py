#!/usr/bin/env python3
"""Complete exact leave/pair-cover census; residual bounds use proper colors.

The streamed replay file is local operational evidence, not a publication
artifact. A guard failure aborts without a complete summary.
"""
import argparse
import hashlib
import itertools as it
import json
import resource
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'a18_6_5_saturated_single_pair'))
from geometry import automorphisms, image, normalization, points, word

T = word([1, 2, 3])
L = T | 1
PAIRS = list(it.combinations(range(16), 2))
PAIR_INDEX = {e: j for j, e in enumerate(PAIRS)}
PAIR_FULL = (1 << 120) - 1


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def pair_mask(block):
    return sum(1 << PAIR_INDEX[e] for e in it.combinations(points(block), 2))


def encoded(value):
    return (json.dumps(value, separators=(',', ':'), sort_keys=True) + '\n').encode()


def orbit_cover(domain, group, transform):
    remaining = set(domain)
    answer = []
    while remaining:
        first = min(remaining)
        members = {transform(first, g) for g in group}
        require(members <= remaining, 'invalid or overlapping symmetry orbit')
        remaining.difference_update(members)
        answer.append((first, len(members)))
    require(sum(size for _, size in answer) == len(domain), 'incomplete orbit cover')
    return answer


def templates(k, deficient_t):
    outside = list(range(3, 3 + k))
    low = list(range(deficient_t, 3))
    assignments = {}
    for targets in it.product(outside, repeat=len(low)):
        degrees = tuple(targets.count(p) for p in outside)
        assignments.setdefault(degrees, []).append(tuple(zip(low, targets)))
    forced = tuple((0, p) for p in outside) if deficient_t else ()
    answer = set()
    for chosen in it.combinations(list(it.combinations(outside, 2)), 9 - len(forced) - len(low)):
        degrees = [sum(p in edge for edge in chosen) for p in outside]
        need = tuple((2 if deficient_t else 3) - d for d in degrees)
        for attached in assignments.get(need, []):
            edges = tuple(sorted(forced + attached + chosen))
            require(len(edges) == len(set(edges)) == 9, 'invalid nine-edge template')
            answer.add(edges)
    require(len(answer) == (28 if deficient_t else 605), 'template count mismatch')
    return sorted(answer)


def prepare():
    plane = normalization()['first_plane']
    flag = [g for g in automorphisms(plane) if g[0] == 0 and image(L, g) == L]
    require(len(flag) == 72 and {g[1] for g in flag} == {1, 2, 3}, 'bad flag group')
    outside = [p for p in range(16) if p not in [1, 2, 3]]
    abstract = [None, templates(5, 0), templates(4, 1)]
    leaves = []
    groups = []
    labelled = 0
    support_counts = []
    for profile in range(3):
        group = [g for g in flag if g[1] == 1] if profile == 2 else flag
        if profile == 0:
            domain = {(word(s), p) for s in it.combinations(outside, 4) for p in s}
            transform = lambda v, g: (image(v[0], g), g[v[1]])
        else:
            k = 5 if profile == 1 else 4
            domain = {word(s) for s in it.combinations(outside, k)}
            transform = image
        supports = orbit_cover(domain, group, transform)
        support_counts.append(len(supports))
        for support_index, (representative, support_size) in enumerate(supports):
            support, doubled = representative if profile == 0 else (representative, None)
            stabilizer = [g for g in group if image(support, g) == support and
                          (doubled is None or g[doubled] == doubled)]
            require(stabilizer, 'empty support stabilizer')
            if profile == 0:
                edges = list(it.combinations(points(support), 2)) + [(p, doubled) for p in [1, 2, 3]]
                candidates = {sum(1 << PAIR_INDEX[tuple(sorted(e))] for e in edges)}
            else:
                mapping = [1, 2, 3] + list(points(support))
                candidates = {sum(1 << PAIR_INDEX[tuple(sorted((mapping[a], mapping[b])))]
                                  for a, b in template) for template in abstract[profile]}
            maps = [[PAIR_INDEX[tuple(sorted((g[a], g[b])))] for a, b in PAIRS] for g in stabilizer]
            local = orbit_cover(candidates, maps,
                                lambda v, g: sum(1 << g[j] for j in bits(v)))
            labelled += len(candidates) * support_size * (3 if profile == 2 else 1)
            groups.append([profile, support_index, support, doubled, support_size,
                           len(stabilizer), len(candidates), len(local)])
            for leave, size in local:
                leaves.append([len(leaves), profile, support_index, leave, size])
    require(support_counts == [50, 30, 40], 'support orbit mismatch')
    require(labelled == 841555 and len(leaves) == 11855, 'leave coverage mismatch')
    return plane, groups, leaves


class PairCover:
    def __init__(self, columns):
        self.columns = columns
        self.rows = [pair_mask(b) for b in columns]
        self.containing = [0] * 120
        for j, row in enumerate(self.rows):
            for k in bits(row):
                self.containing[k] |= 1 << j
        self.conflicts = []
        for row in self.rows:
            mask = 0
            for k in bits(row):
                mask |= self.containing[k]
            self.conflicts.append(mask)

    def run(self, leave, node_cap=200000, time_cap=10.0):
        started = time.monotonic()
        require(not leave & pair_mask(T), 'leave uses a shared-triple pair')
        target = PAIR_FULL ^ pair_mask(T) ^ leave
        require(target.bit_count() == 108, 'incorrect target pair count')
        available = (1 << len(self.rows)) - 1
        for k in bits(PAIR_FULL ^ target):
            available &= ~self.containing[k]
        answers = []
        nodes = 0

        def visit(left, active, chosen):
            nonlocal nodes
            nodes += 1
            if nodes > node_cap or (nodes % 256 == 0 and time.monotonic() - started > time_cap):
                raise RuntimeError('INCOMPLETE pair-cover node/time guard')
            if not left:
                answer = tuple(sorted(self.columns[j] for j in chosen))
                require(len(answer) == 18, 'incorrect cover cardinality')
                answers.append(answer)
                return
            options, size = 0, len(self.rows) + 1
            for k in bits(left):
                choices = active & self.containing[k]
                count = choices.bit_count()
                if count < size:
                    options, size = choices, count
                    if count <= 1:
                        break
            for j in bits(options):
                require(self.rows[j] & left == self.rows[j], 'invalid active column')
                visit(left ^ self.rows[j], active & ~self.conflicts[j], chosen + (j,))

        visit(target, available, ())
        require(len(answers) == len(set(answers)), 'duplicate exact cover')
        return sorted(answers), nodes


def coloring(neighbors, active):
    saturation = [0] * len(neighbors)
    colors = [-1] * len(neighbors)
    domain = active
    degrees = [(row & active).bit_count() for row in neighbors]
    while active:
        v = max(bits(active), key=lambda j: (saturation[j].bit_count(), degrees[j], -j))
        forbidden, color = saturation[v], 0
        while forbidden >> color & 1:
            color += 1
        colors[v] = color
        active ^= 1 << v
        for j in bits(active & neighbors[v]):
            saturation[j] |= 1 << color
    require(all(colors[i] != colors[j] for i in bits(domain)
                for j in bits(neighbors[i] & domain)), 'improper coloring')
    return [colors[i] for i in bits(domain)], 1 + max(colors, default=-1)


def run(args):
    started = time.monotonic()
    plane, groups, leaves = prepare()
    allowed = [word(a) for a in it.combinations(range(16), 4)
               if (word(a) & T).bit_count() <= 1 and
               all((word(a) & line).bit_count() <= 2 for line in plane)]
    pool = [word(a) for a in it.combinations(range(16), 5)
            if (word(a) & T).bit_count() <= 2 and
            all((word(a) & line).bit_count() <= 2 for line in plane if line != L)]
    require(len(allowed) == 714 and len(pool) == 378, 'baseline universe mismatch')
    masks = {b: sum(1 << j for j, v in enumerate(pool) if (b & v).bit_count() <= 2)
             for b in allowed}
    neighbors = [sum(1 << j for j, b in enumerate(pool) if i != j and (a & b).bit_count() <= 2)
                 for i, a in enumerate(pool)]
    solver = PairCover(allowed)
    digest = hashlib.sha256()
    digest.update(encoded({'groups': groups, 'leaves': leaves, 'plane': plane,
                           'allowed': allowed, 'pool': pool}))
    first = [b | (1 << 17) for b in plane if b != L] + [T | (1 << 16) | (1 << 17)]
    histograms = [Counter() for _ in range(3)]
    stats = [{'leaves': 0, 'realized_leaves': 0, 'star_pairs': 0,
              'cover_nodes': 0, 'max_cover_nodes': 0, 'max_common_fives': 0,
              'max_color_upper': 0} for _ in range(3)]
    args.replay.parent.mkdir(parents=True, exist_ok=True)
    with args.replay.open('w') as replay:
        replay.write(encoded({'groups': groups, 'leaves': leaves, 'plane': plane,
                              'allowed': allowed, 'pool': pool}).decode())
        for index, profile, support_index, leave, size in leaves:
            covers, nodes = solver.run(leave)
            cases = []
            s = stats[profile]
            s['leaves'] += 1
            s['realized_leaves'] += bool(covers)
            s['star_pairs'] += len(covers)
            s['cover_nodes'] += nodes
            s['max_cover_nodes'] = max(s['max_cover_nodes'], nodes)
            for cover in covers:
                active = (1 << len(pool)) - 1
                for b in cover:
                    active &= masks[b]
                colors, upper = coloring(neighbors, active)
                common = [pool[j] for j in bits(active)]
                stars = first + [b | (1 << 16) for b in cover]
                require(len(stars) == 38 and len(set(stars)) == 38 and
                        all((a & b).bit_count() <= 2 for a, b in it.combinations(stars, 2)),
                        'invalid star union')
                require(all((b & v).bit_count() <= 2 for b in stars for v in common),
                        'invalid residual word')
                s['max_common_fives'] = max(s['max_common_fives'], len(common))
                s['max_color_upper'] = max(s['max_color_upper'], upper)
                histograms[profile][upper] += 1
                cases.append([cover, common, colors])
            record = {'index': index, 'covers': cases}
            line = encoded(record)
            digest.update(line)
            replay.write(line.decode())
            if (index + 1) % 100 == 0 or index + 1 == len(leaves):
                replay.flush()
                progress = {'status': 'INCOMPLETE until all leaves finish', 'completed_leaves': index + 1,
                            'total_leaves': len(leaves), 'stats': stats,
                            'seconds': round(time.monotonic() - started, 4)}
                args.progress.write_text(json.dumps(progress, indent=2) + '\n')
                print(json.dumps(progress, separators=(',', ':')), flush=True)
    result = {'agent': 'six-code-3', 'role': 'researcher', 'status': 'COMPLETE',
              'scope': 'point degrees20,19; pair multiplicity1; exact cover and proper color bounds',
              'support_orbits': [50, 30, 40], 'labelled_leaves': 841555,
              'leaf_orbits': len(leaves), 'profiles': stats,
              'color_upper_histograms': [dict(sorted(h.items())) for h in histograms],
              'max_color_upper': max(s['max_color_upper'] for s in stats),
              'code_size_upper': 38 + max(s['max_color_upper'] for s in stats),
              'replay_sha256': digest.hexdigest()}
    args.summary.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'result': result, 'seconds': round(time.monotonic() - started, 4),
                      'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--replay', required=True, type=Path)
    p.add_argument('--summary', required=True, type=Path)
    p.add_argument('--progress', required=True, type=Path)
    run(p.parse_args())

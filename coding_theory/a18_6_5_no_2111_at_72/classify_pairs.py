"""Classify the complete compatible-pair corpus with both centers fixed."""
from collections import deque
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import resource
import time

from paths import BASE, WORK
ROOT = WORK


def image_word(word, point):
    return sum(1 << point[u] for u in range(18) if word >> u & 1)


def image_star(words, point):
    return tuple(sorted(image_word(w, point) for w in words))


def validate_union(left, right):
    union = set(left) | set(right)
    if (len(left) != 20 or len(right) != 20 or len(set(left) & set(right)) != 3
            or len(union) != 37 or any(w.bit_count() != 5 for w in union)
            or any((u & v).bit_count() > 2 for u, v in combinations(union, 2))
            or sum(bool(w & 1) for w in union) != 20
            or sum(bool(w & (1 << 17)) for w in union) != 20):
        raise RuntimeError('literal ordered joint-star witness fails')


def run():
    started = time.monotonic()
    carrier = json.loads((ROOT/'tail_carrier.json').read_text())
    specs = json.loads((ROOT/'mapping_specs.json').read_text())['fibers']
    census = json.loads((ROOT/'census.json').read_text())
    if not census['status'].startswith('COMPLETE'):
        raise RuntimeError('incomplete mapping census')
    pairs = {}
    with (ROOT/'all_prune.jsonl').open() as stream:
        for spec in specs:
            record = json.loads(stream.readline())
            if record['status'] != 'COMPLETE' or record['index'] != spec['index']:
                raise RuntimeError('incomplete native corpus')
            if not record['accepted']:
                continue
            first = carrier['stars'][spec['first']]
            second = carrier['stars'][spec['second']]
            left = tuple(sorted(w | (1 << 17) for w in first['words']))
            point = spec['fixed'][:]
            source_free = [u for u, v in enumerate(point) if v == -1]
            target_free = sorted(set(range(16))-set(point))
            wanted = set(record['accepted'])
            family = pairs.setdefault((spec['first'], spec['second']), {})
            case_started = time.monotonic()
            nodes = 0
            for ordinal, assignment in enumerate(permutations(target_free)):
                if ordinal not in wanted:
                    continue
                for u, v in zip(source_free, assignment):
                    point[u] = v
                right = tuple(sorted(1 | sum(1 << (17 if u==0 else point[u-1]+1)
                                            for u in range(17) if w >> u & 1)
                                     for w in second['words']))
                validate_union(left, right)
                full = [tuple(p)+(17,) for p in first['automorphisms']]
                literal = {image_star(right, p) for p in full}
                # A separate orbit walk using already checked generators.
                walked = {right}
                queue = deque(walked)
                generators = [tuple(p)+(17,) for p in first['generators']]
                while queue:
                    old = queue.popleft()
                    nodes += 1
                    if nodes > 200000 or time.monotonic()-case_started > 10:
                        raise RuntimeError('INCOMPLETE joint orbit node/time guard')
                    for g in generators:
                        new = image_star(old, g)
                        if new not in walked:
                            walked.add(new)
                            queue.append(new)
                if walked != literal:
                    raise RuntimeError('joint packing orbit methods differ entrywise')
                canonical = min(literal)
                stabilizers = [p for p in full if image_star(canonical, p) == canonical]
                if len(literal)*len(stabilizers) != len(full):
                    raise RuntimeError('joint orbit-stabilizer mismatch')
                entry = dict(first=spec['first'], second=spec['second'], left=list(left), right=list(canonical),
                             center_fixing_automorphism_order=len(stabilizers),
                             raw_map_multiplicity=len(full)*len(second['automorphisms'])//len(stabilizers),
                             orbit_size=len(literal), orbit_sha256=hashlib.sha256(
                                 json.dumps(sorted(literal), separators=(',', ':')).encode()).hexdigest())
                if canonical in family and family[canonical] != entry:
                    raise RuntimeError('inconsistent repeated joint orbit')
                family[canonical] = entry
            if time.monotonic()-case_started > 10:
                raise RuntimeError('INCOMPLETE joint orbit final time guard')
    cases = []
    counts = [[0]*8 for _ in range(8)]
    for pair in census['pairs']:
        key = (pair['first'], pair['second'])
        family = pairs.get(key, {})
        if sum(q['raw_map_multiplicity'] for q in family.values()) != pair['raw_compatible_maps']:
            raise RuntimeError('independent raw mapping multiplicity reconstruction differs')
        counts[key[0]][key[1]] = len(family)
        for canonical in sorted(family):
            entry = family[canonical]
            entry['index'] = len(cases)
            validate_union(entry['left'], entry['right'])
            cases.append(entry)
    result = dict(agent='six-code-3', role='researcher',
                  status='COMPLETE ordered-center joint-star classification',
                  classes=len(cases), ordered_class_counts=counts, cases=cases,
                  seconds=round(time.monotonic()-started, 6),
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  ordinary_completeness_bridges_formalized=False, independent_peer_review=False)
    (ROOT/'joint_classes.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'], result['classes'])
    for row in counts: print(row)
    return result


if __name__ == '__main__':
    run()

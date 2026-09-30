#!/usr/bin/env python3
"""Generate the eight-anchor carrier and compact exhaustive no-cover trees.

See NO_DEFICIT_THREE.md for the ordinary coverage and completion bridges.
All arithmetic is exact. Guards raise INCOMPLETE; they prove nothing.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from math import factorial
from functools import reduce
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
from check_pair_completion import template, symmetries, require, encoded, U, V, A, B, D


def cases():
    result = []
    for kind in ('middle', 'end', 'triangle'):
        leave, covered, valid = template(kind)
        maps = symmetries(kind, leave)
        remaining = set(valid)
        while remaining:
            rep = min(remaining)
            orbit = {family_image(rep, p) for p in maps}
            require(orbit <= remaining, 'disjoint shared-tail orbits')
            remaining -= orbit
            fixed = tuple(tuple(sorted((V,) + tail)) for tail in rep)
            used = set().union(*(pairs(q) for q in fixed))
            require(len(used) == 12 and not used & leave, 'legal shared words')
            rows = tuple(sorted(pairs(range(17)) - leave - used))
            require(len(rows) == 108 and all(V not in e for e in rows), 'eighteen-block domain')
            result.append({'index': len(result), 'kind': kind, 'leave': tuple(sorted(leave)),
                           'representative': rep, 'fixed': fixed, 'rows': rows})
    require([c['representative'] for c in result] == [
        ((8,9,10),(11,12,13)), ((8,9,11),(10,12,13)),
        ((9,10,15),(11,12,13)), ((8,9,12),(10,11,13)),
        ((8,10,12),(9,11,13))], 'five ordered first cases')
    return result

O = frozenset(range(8))
IDENTITY = tuple(range(18))


def pairs(q):
    return set(combinations(sorted(q), 2))


def image(q, p):
    return tuple(sorted(p[x] for x in q))


def family_image(quads, p):
    return tuple(sorted(image(q, p) for q in quads))


def partitions(points, size=3):
    if not points:
        yield ()
        return
    first, *rest = sorted(points)
    for extra in combinations(rest, size - 1):
        block = (first,) + extra
        left = tuple(x for x in rest if x not in extra)
        for tail in partitions(left, size):
            yield tuple(sorted((block,) + tail))


def set_partitions(points):
    if not points:
        yield ()
        return
    first, *rest = sorted(points)
    for tail in set_partitions(rest):
        yield tuple(sorted(((first,),) + tail))
        for i, block in enumerate(tail):
            yield tuple(sorted(tail[:i] + tail[i+1:] + (tuple(sorted((first,) + block)),)))


def small_maps(case):
    maps = [p for p in symmetries(case['kind'], set(case['leave']))
            if p[A] == A and p[B] == B
            and family_image(case['representative'], p) == case['representative']]
    require(len(maps) == (2 if case['index'] == 4 else 4), 'small fixed-anchor group')
    return maps


def anchor_a_patterns(case):
    available = set(D) - {A} - {y if x == A else x for x, y in case['leave'] if A in (x, y)}
    special = frozenset(available) - O
    require(len(available) == 12 and O <= available and len(special) == 4, 'A neighbor partition')
    rowset = set(case['rows']) | set().union(*(pairs(q) for q in case['fixed']))
    fixed_pairs = set().union(*(pairs(q) for q in case['fixed']))
    allowed = rowset - fixed_pairs
    raw = {tuple(sorted(p + ((),) * (4-len(p)))) for p in set_partitions(special)
           if len(p) <= 4 and all(len(block) <= 3 and pairs(block) <= allowed for block in p)}
    require(len(raw) == (5 if case['index'] == 4 else 3), 'complete special partitions')
    maps = small_maps(case)
    remaining, records = set(raw), []
    while remaining:
        rep = min(remaining)
        orbit = {family_image(rep, p) for p in maps}
        require(orbit <= remaining, 'disjoint A-pattern orbit')
        remaining -= orbit
        next_ordinary = 0
        quads = []
        for block in rep:
            count = 3-len(block)
            ordinary = tuple(range(next_ordinary, next_ordinary+count))
            next_ordinary += count
            quads.append(tuple(sorted((A,) + block + ordinary)))
        require(next_ordinary == 8 and len(quads) == 4, 'ordinary filling')
        require(all(pairs(q) <= allowed for q in quads), 'legal normalized A quartet')
        counts = Counter(e for q in quads for e in pairs(q))
        require(set(counts.values()) == {1}, 'A quartet repeated pair')
        empty = sum(not b for b in rep)
        fillings = factorial(8) // (factorial(empty) *
                                  reduce(lambda x, b: x*factorial(3-len(b)), rep, 1))
        records.append({'pattern': rep, 'pattern_orbit': sorted(orbit),
                        'labeled_fillings_per_pattern': fillings,
                        'quads': tuple(sorted(quads))})
    require(len(records) == (4 if case['index'] == 4 else 2), 'eight A quartet types')
    # Independent direct domain: all 15400 partitions of the twelve actual points.
    direct = set()
    histogram = Counter()
    examined = 0
    for part in partitions(available):
        examined += 1
        if all(pairs((A,) + tail) <= allowed for tail in part):
            direct.add(part)
            pattern = tuple(sorted(tuple(x for x in tail if x in special) for tail in part))
            histogram[pattern] += 1
    require(examined == 15400, 'complete twelve-point partition universe')
    require(set(histogram) == raw, 'direct special-pattern domain agrees')
    for record in records:
        require(all(histogram[p] == record['labeled_fillings_per_pattern'] for p in record['pattern_orbit']),
                'entrywise multinomial filling comparison')
    require(len(direct) == (8120 if case['index'] == 4 else 5880), 'direct compatible quartet count')
    return records, {'partitions_checked': examined, 'compatible_labeled_quartets': len(direct),
                     'special_patterns': len(raw), 'A_quartet_orbits': len(records)}


def close_generators(generators):
    reached, stack = {IDENTITY}, [IDENTITY]
    while stack:
        p = stack.pop()
        for g in generators:
            q = tuple(g[p[x]] for x in range(18))
            if q not in reached:
                reached.add(q)
                stack.append(q)
                require(len(reached) <= 256, 'unexpected A stabilizer size')
    return tuple(sorted(reached))


def a_stabilizer(case, a_record):
    quads = a_record['quads']
    tails = [tuple(x for x in q if x != A) for q in quads]
    special = set().union(*(set(t)-O for t in tails))
    groups = [(tuple(x for x in t if x in special), tuple(x for x in t if x in O)) for t in tails]
    generators = []
    for _, group in groups:
        for x, y in zip(group, group[1:]):
            p = list(IDENTITY)
            p[x], p[y] = p[y], p[x]
            generators.append(tuple(p))
    empties = [group for s, group in groups if not s]
    for left, right in zip(empties, empties[1:]):
        p = list(IDENTITY)
        for x, y in zip(left, right):
            p[x], p[y] = p[y], p[x]
        generators.append(tuple(p))
    pattern = a_record['pattern']
    for small in small_maps(case):
        if family_image(pattern, small) != pattern:
            continue
        p = list(small)
        unused = list(groups)
        for s, group in groups:
            wanted = image(s, small)
            candidates = [(j, target) for j, (ts, target) in enumerate(unused) if ts == wanted]
            require(candidates, 'special stabilizer matches an A word')
            j, target = candidates[0]
            del unused[j]
            require(len(group) == len(target), 'matching ordinary group sizes')
            for x, y in zip(group, target):
                p[x] = y
        generators.append(tuple(p))
    group = close_generators(generators)
    for p in group:
        require(len(set(p)) == 18 and all(p[x] == x for x in (U,V,A,B)), 'actual fixed-anchor permutation')
        require(family_image(case['leave'], p) == case['leave'], 'A stabilizer preserves leave')
        require(family_image(case['fixed'], p) == tuple(sorted(case['fixed'])), 'A stabilizer preserves common words')
        require(family_image(quads, p) == quads, 'A stabilizer preserves quartet')
    return group


def b_records(case, a_record):
    fixed = tuple(sorted(case['fixed'] + a_record['quads']))
    existing = tuple(q for q in fixed if B in q)
    require(len(existing) == (1 if case['kind'] == 'middle' else 0), 'fixed B words')
    neighbors = set(D) - {B} - {y if x == B else x for x,y in case['leave'] if B in (x,y)}
    used = set().union(*(set(q)-{B} for q in existing)) if existing else set()
    free = neighbors - used
    require(len(free) == (9 if existing else 12), 'B free-tail domain')
    fixed_pairs = set().union(*(pairs(q) for q in fixed))
    remaining_rows = set(case['rows']) - fixed_pairs
    valid = set()
    examined = 0
    for part in partitions(free):
        examined += 1
        quads = tuple(sorted(tuple(sorted((B,) + tail)) for tail in part))
        if all(pairs(q) <= remaining_rows for q in quads):
            valid.add(quads)
    require(examined == (280 if existing else 15400), 'complete B-tail partition domain')
    group = a_stabilizer(case, a_record)
    remaining, records = set(valid), []
    while remaining:
        rep = min(remaining)
        orbit = {family_image(rep, p) for p in group}
        require(orbit <= remaining, 'disjoint B quartet orbit')
        remaining -= orbit
        quads = tuple(sorted(fixed + rep))
        require(len(quads) == (9 if existing else 10), 'fixed anchor words')
        used_pairs = Counter(e for q in quads for e in pairs(q))
        require(set(used_pairs.values()) == {1}, 'fixed anchor repeated pair')
        require(sum(A in q for q in quads) == sum(B in q for q in quads) == 4, 'both anchor multiplicities')
        require(sum(V in q for q in quads) == 2, 'marked pair multiplicity')
        rows = tuple(sorted(set(case['rows']) - set(used_pairs)))
        require(len(rows) == (66 if existing else 60), 'small residual pair universe')
        require(all(not ({A,B,V} & set(e)) for e in rows), 'remaining pairs avoid three anchors')
        vertices = tuple(x for x in D if x not in (A,B))
        columns = tuple(q for q in combinations(vertices,4) if pairs(q) <= set(rows))
        records.append({'orbit_size': len(orbit), 'b_quads': rep, 'fixed_quads': quads,
                        'rows': rows, 'columns': columns,
                        'input_sha256': sha256(encoded([rows,columns])).hexdigest()})
    return records, {'partitions_checked': examined, 'compatible_labeled_B_groups': len(valid),
                     'checked_A_stabilizer_size': len(group), 'B_group_orbits': len(records)}


def generate():
    result = []
    summary = []
    for case in cases():
        if case['index'] not in (1,3,4):
            continue
        roots, checks = anchor_a_patterns(case)
        for ai, a_record in enumerate(roots):
            bs, bcheck = b_records(case,a_record)
            summary.append({'first_case': case['index'], 'a_case': ai,
                            'a_pattern': a_record['pattern'], 'a_quads': a_record['quads'],
                            'A_coverage': checks, 'B_coverage': bcheck})
            for bi, record in enumerate(bs):
                result.append({'index': len(result), 'first_case': case['index'],
                               'a_case': ai, 'b_case': bi, **record})
    require(len(result) == 198, 'complete 198-case carrier')
    return {'summary': summary, 'cases': result}


class CoverFound(Exception):
    """A positive exact cover contradicts the desired obstruction."""


def no_cover_tree(rows, columns, node_limit=200000, seconds=10):
    row_index = {e: i for i,e in enumerate(rows)}
    masks = tuple(sum(1 << row_index[e] for e in pairs(q)) for q in columns)
    options = [0] * len(rows)
    for i, mask in enumerate(masks):
        require(mask.bit_count() == 6, 'quadruple column has six distinct rows')
        for r in range(len(rows)):
            if mask >> r & 1:
                options[r] |= 1 << i
    conflicts = []
    for mask in masks:
        value = 0
        for r in range(len(rows)):
            if mask >> r & 1:
                value |= options[r]
        conflicts.append(value)
    nodes = 0
    started = time.monotonic()

    def visit(left, active):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit or (nodes % 128 == 0 and time.monotonic()-started > seconds):
            raise RuntimeError('INCOMPLETE: certificate guard reached')
        if not left:
            raise CoverFound('a complete exact cover exists')
        choices = [( (options[r] & active).bit_count(), r, options[r] & active)
                   for r in range(len(rows)) if left >> r & 1]
        _, pivot, available = min(choices)
        branches = []
        while available:
            bit = available & -available
            i = bit.bit_length()-1
            available ^= bit
            require(masks[i] & left == masks[i], 'active column uses a covered row')
            branches.append([i, visit(left ^ masks[i], active & ~conflicts[i])])
        return [pivot, branches]

    tree = visit((1 << len(rows))-1, (1 << len(columns))-1)
    return tree, nodes


def build():
    inputs = generate()
    cert_cases = []
    node_counts = []
    for case in inputs['cases']:
        tree, nodes = no_cover_tree(case['rows'], case['columns'])
        node_counts.append(nodes)
        cert_cases.append({k:case[k] for k in
                           ('index','first_case','a_case','b_case','orbit_size','fixed_quads','input_sha256')}
                          | {'tree':tree})
    certificate = {'schema':'pair-two-completion-v1', 'carrier_summary':inputs['summary'],
                   'cases':cert_cases}
    report = {'agent':'six-code-1','role':'researcher',
              'status':'COMPLETE_EXACT_NO_COVERS',
              'first_cases':[1,3,4], 'A_types':len(inputs['summary']),
              'residual_cases':len(cert_cases), 'nodes':sum(node_counts),
              'maximum_nodes_per_case':max(node_counts),
              'candidate_quadruple_range':[min(len(c['columns']) for c in inputs['cases']),
                                            max(len(c['columns']) for c in inputs['cases'])],
              'input_stream_sha256':sha256(encoded([
                  [c['first_case'],c['a_case'],c['b_case'],c['fixed_quads'],c['rows'],c['columns']]
                  for c in inputs['cases']])).hexdigest(),
              'certificate_sha256':sha256(encoded(certificate)).hexdigest(),
              'certificate_bytes':len(encoded(certificate)),
              'global_72_word_exclusion':False,
              'independent_peer_review':False,
              'ordinary_completeness_bridges_formalized':False}
    return certificate, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-certificate',action='store_true',
                        help='regenerate compact certificate and primary manifest')
    args = parser.parse_args()
    certificate, report = build()
    cp = HERE/'pair_two_certificate.json'
    ep = HERE/'pair_two_expected.json'
    if args.write_certificate:
        cp.write_bytes(encoded(certificate))
        expected = json.loads(ep.read_text()) if ep.exists() else {}
        expected['primary'] = report
        ep.write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
    else:
        require(cp.read_bytes() == encoded(certificate), 'certificate regeneration differs')
        require(json.loads(ep.read_text())['primary'] == report, 'primary manifest differs')
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()

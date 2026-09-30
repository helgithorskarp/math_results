"""Separate exhaustive raw-label audit using unoriented cells and bitset links.

No production predicate, schema or enumerator is imported. Every saved
boundary partition and final partition is compared with EXPECTED.json.
This is a separate same-author algorithm, not an independent reviewer.
"""
from itertools import combinations, product
from pathlib import Path
import argparse
import json


ANCHORS = ('F','U','X','R','S','Z','B','C','Y')
BASE = (('R','X','F'), ('S','R','F'), ('Z','S','F'),
        ('F','X','B','U'), ('F','U','C','Z'), ('U','B','Y','C'),
        ('R','S','K','L'), ('R','L','P','X'), ('S','Z','Q','K'))
RAW_CASES = {
    'strip_both_ordinary':
        (ANCHORS+('L','K','P','Q','H'),
         BASE+(('L','K','H'), ('L','H','P'), ('K','Q','H')),
         'maxima', {'B':1, 'C':1}, {'F':3,'U':0,'R':2,'S':2,'L':2,'K':2}, (11,14)),
    'strip_L_ordinary_K_zero':
        (ANCHORS+('L','K','P','Q','H'), BASE+(('L','K','H'),),
         'maxima', {'B':1, 'C':1}, {'F':3,'U':0,'R':2,'S':2,'L':2,'K':0}, (11,14)),
    'strip_L_zero_K_ordinary':
        (ANCHORS+('L','K','P','Q','H'), BASE+(('K','H','L'),),
         'maxima', {'B':1, 'C':1}, {'F':3,'U':0,'R':2,'S':2,'L':0,'K':2}, (11,14)),
    'one_T_L':
        (ANCHORS+('L','K','P','Q','H','A','D','J','M'),
         BASE+(('C','Q','Z'), ('K','H','L'), ('K','Q','H'),
               ('X','P','A','B'), ('L','H','D','P'), ('B','A','J','Y'), ('C','Y','M','Q')),
         'full', {}, {'F':3,'U':0,'B':0,'C':1,'X':1,'L':1}, (12,15,18)),
    'one_T_K':
        (ANCHORS+('K','L','P','Q','H','A','D','J','M'),
         BASE+(('C','Q','Z'), ('L','K','H'), ('L','H','P'),
               ('X','P','A','B'), ('K','Q','D','H'), ('B','A','J','Y'), ('C','Y','M','Q')),
         'full', {}, {'F':3,'U':0,'B':0,'C':1,'X':1,'K':1}, (12,15,18))}


def normalize(labels):
    rename, answer = {}, []
    for value in labels:
        if value not in rename:
            rename[value] = len(rename)
        answer.append(rename[value])
    return tuple(answer)


def face_key(face):
    rotated = [face[i:] + face[:i] for i in range(len(face))]
    reverse = face[::-1]
    rotated.extend(reverse[i:] + reverse[:i] for i in range(len(face)))
    return min(rotated)


def specification(case):
    names, words, mode, maxima, exact, boundaries = RAW_CASES[case]
    number = {name:i for i,name in enumerate(names)}
    return {'names':names, 'faces':tuple(tuple(number[n] for n in w) for w in words),
            'mode':mode, 'maxima':{number[n]:v for n,v in maxima.items()},
            'exact':{number[n]:v for n,v in exact.items()}, 'boundaries':boundaries,
            'distinct':tuple((number[n],number[a]) for n in ('L','K') for a in ANCHORS[:8])
                         + ((number['L'],number['K']),)}


def check(labels, spec, use_orientability=True):
    assigned = len(labels)
    for a, b in spec['distinct']:
        if a < assigned and b < assigned and labels[a] == labels[b]:
            return False
    faces = set()
    for word in spec['faces']:
        if max(word) < assigned:
            actual = tuple(labels[i] for i in word)
            if len(set(actual)) != len(actual):
                return False
            faces.add(face_key(actual))
    # Raw labels range over 0..17. No requirement that all labels occur.
    degree = [4] * 18
    degree[0], degree[1] = 5, 3
    maximum = [2] * 18
    maximum[0], maximum[1] = 3, 0
    exact = maximum[:] if spec['mode'] == 'full' else [None] * 18
    for index, value in spec['maxima'].items():
        if index < assigned:
            maximum[labels[index]] = min(maximum[labels[index]], value)
    fixed = {}
    for index, value in spec['exact'].items():
        if index < assigned:
            actual = labels[index]
            if actual in fixed and fixed[actual] != value:
                return False
            fixed[actual] = value
            exact[actual] = value
            maximum[actual] = min(maximum[actual], value)
    if any(t is not None and t > maximum[v] for v,t in enumerate(exact)):
        return False
    neighbors, banned = [0]*18, [0]*18
    link = [{} for _ in range(18)]
    corners, triangles = [0]*18, [0]*18
    for face in faces:
        size = len(face)
        if size == 4:
            for offset in (0,1):
                a, b = face[offset], face[offset+2]
                banned[a] |= 1 << b
                banned[b] |= 1 << a
        for i, v in enumerate(face):
            a, b = face[i-1], face[(i+1) % size]
            neighbors[v] |= (1 << a) | (1 << b)
            corners[v] += 1
            triangles[v] += size == 3
            if b in link[v].get(a, set()):
                return False
            link[v].setdefault(a, set()).add(b)
            link[v].setdefault(b, set()).add(a)
    for v in range(18):
        if (neighbors[v] & banned[v] or neighbors[v].bit_count() > degree[v]
                or corners[v] > degree[v] or triangles[v] > maximum[v]):
            return False
        if exact[v] is not None and corners[v]-triangles[v] > degree[v]-exact[v]:
            return False
        if any(len(row) > 2 for row in link[v].values()):
            return False
        unseen = set(link[v])
        while unseen:
            stack = [unseen.pop()]
            component = set(stack)
            while stack:
                item = stack.pop()
                for other in link[v][item]:
                    if other not in component:
                        component.add(other)
                        unseen.remove(other)
                        stack.append(other)
            if all(len(link[v][item]) == 2 for item in component):
                if len(component) != degree[v] or neighbors[v].bit_count() != degree[v]:
                    return False
                if exact[v] is not None and triangles[v] != exact[v]:
                    return False
    for a, b in combinations(range(18), 2):
        if (neighbors[a] & neighbors[b]).bit_count() > 2:
            return False
    if use_orientability:
        # An orientable cell embedding admits one sign per actual face so
        # all shared boundary edges are traversed in opposite directions.
        boundary, actual_faces = {}, sorted(faces)
        for index, face in enumerate(actual_faces):
            for i, a in enumerate(face):
                b = face[(i+1) % len(face)]
                boundary.setdefault(tuple(sorted((a,b))), []).append(
                    (index, 1 if a < b else -1))
        dual = [[] for _ in actual_faces]
        for occupants in boundary.values():
            if len(occupants) > 2:
                return False
            if len(occupants) == 2:
                (a,sa), (b,sb) = occupants
                multiplier = -sa*sb
                dual[a].append((b,multiplier))
                dual[b].append((a,multiplier))
        signs = {}
        for root in range(len(actual_faces)):
            if root in signs:
                continue
            signs[root], stack = 1, [root]
            while stack:
                a = stack.pop()
                for b, multiplier in dual[a]:
                    desired = signs[a]*multiplier
                    if b in signs:
                        if signs[b] != desired:
                            return False
                    else:
                        signs[b] = desired
                        stack.append(b)
    # No production orientation, K4 test or global face-count shortcut.
    return True


def audit(case, production):
    spec, initial = specification(case), {tuple(range(9))}
    previous, states, blocks = 9, initial, []
    for end in spec['boundaries']:
        final, raw, accepted_raw = set(), 0, 0
        for prefix in sorted(states):
            for tail in product(range(end), repeat=end-previous):
                raw += 1
                labels = prefix+tail
                if check(labels, spec):
                    accepted_raw += 1
                    final.add(normalize(labels))
        expected = (production['survivors'] if end == len(spec['names'])
                    else production['passing_partitions_by_depth'].get(str(end), []))
        if [list(p) for p in sorted(final)] != expected:
            raise RuntimeError('Boundary partitions differ entrywise: '+case+' '+str(end))
        blocks.append({'start_depth':previous, 'end_depth':end, 'raw_tuples':raw,
                       'accepted_raw_tuples':accepted_raw, 'normalized_partitions':sorted(final)})
        previous, states = end, final
    if states:
        raise RuntimeError('Unexpected full alias assignment: '+case)
    return {'names':spec['names'], 'blocks':blocks,
            'total_raw_tuples':sum(b['raw_tuples'] for b in blocks),
            'final_normalized_partitions':[], 'with_at_most_15_classes':[]}


def controls():
    positive = []
    for case in RAW_CASES:
        spec = specification(case)
        identity = tuple(range(len(spec['names'])))
        if check(identity, spec):
            raise RuntimeError('Full negative control accepted: '+case)
        if case.startswith('strip_'):
            trimmed = dict(spec)
            trimmed['faces'] = spec['faces'][:-1]
            if not check(identity, trimmed):
                raise RuntimeError('Trimmed generic positive control rejected: '+case)
            positive.append(case+'_without_last_T')
        elif not check(identity[:15], spec):
            raise RuntimeError('Main positive prefix rejected: '+case)
        else:
            positive.append(case+'_fifteen_slot_prefix')
    # On a triangle-maxima-only strip, an unclassified vertex may have
    # three Q corners and at most two Ts. Such a prefix must not be treated
    # as an ordinary two-T vertex. This control tests that distinction.
    generic = specification('strip_both_ordinary')
    generic = dict(generic)
    generic['faces'] = generic['faces'][:6] + ((8,6,9,10), (8,10,11,12))
    generic['distinct'] = ()
    generic['exact'] = {0:3,1:0,3:2,4:2}
    if not check(tuple(range(14)), generic):
        raise RuntimeError('Unclassified three-Q vertex wrongly rejected')
    full = dict(generic)
    full['mode'], full['maxima'] = 'full', {}
    if check(tuple(range(14)), full):
        raise RuntimeError('Ordinary three-Q vertex wrongly accepted')
    # A fixed eleven-class quotient of the earlier paired strip passes
    # every local condition but has a contradictory signed dual cycle.
    # Copy its cells explicitly; no earlier program or data is imported.
    quotient = (0,1,2,3,4,5,6,7,8,9,10,8,10,7,6,9)
    cells = ((0,2,3),(0,4,5),(2,3,9),(4,5,10),
             (0,1,6,2),(0,3,8,4),(0,5,7,1),(1,7,11,6),
             (2,6,12,9),(3,9,13,8),(4,8,14,10),(5,10,15,7))
    twisted = {'faces':cells, 'distinct':(), 'mode':'maxima', 'maxima':{}, 'exact':{}}
    if not check(quotient, twisted, False) or check(quotient, twisted, True):
        raise RuntimeError('Nonorientable local quotient control differs')
    return {'positive_partial_consistency':positive,
            'all_five_full_identity_negative_controls_rejected':True,
            'unclassified_three_Q_prefix_accepted_ordinary_version_rejected':True,
            'nonorientable_quotient_local_accept_signed_dual_reject':quotient}


def run(case=None):
    chosen = (case,) if case is not None else tuple(RAW_CASES)
    production = json.loads((Path(__file__).resolve().parent/'EXPECTED.json').read_text())['covers']
    results = {name:audit(name, production[name]) for name in chosen}
    return {'agent':'six-tammes-1', 'role':'researcher',
            'status':'SEPARATE_SAME_AUTHOR_RAW_LABEL_UNORIENTED_SIGNED_DUAL_AUDIT',
            'results':results, 'total_raw_tuples':sum(r['total_raw_tuples'] for r in results.values()),
            'controls':controls(),
            'entrywise_comparison':'Every normalized block-boundary and final partition matches EXPECTED.json.',
            'scope':'No production import. Written original-face forcing, role and topology bridges are unformalized; independent review pending.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=tuple(RAW_CASES))
    args = parser.parse_args()
    print(json.dumps(run(args.case), indent=2, sort_keys=True))

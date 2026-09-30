"""Separate raw-label, unoriented-link and signed-dual audit.

No production module, predicate or enumerator is imported. Face schemas
are copied from the written patches. Run all cases, or --case NAME.
"""
from itertools import combinations, product
from pathlib import Path
import argparse, json

A=('F','U','X','R','S','Z','B','C','D')
BASE=(('F','X','R'),('F','S','Z'),
      ('F','U','B','X'),('F','R','D','S'),('F','Z','C','U'),('U','C','Y','B'))
UNORIENTED_SCHEMAS={
 'both_paired':(
     A+('J','K','Y','L','M','N','O'),
     BASE+(('X','R','J'),('S','Z','K'),
           ('X','B','L','J'),('R','J','M','D'),('S','D','N','K'),('Z','K','O','C')),
     9,12,None,(('F','J'),('F','K')),False),
 'extra_equals_J':(
     A+('J','K','L','Y','M','N','P','W'),
     BASE+(('X','R','J'),('S','D','K'),('Z','C','L'),
           ('X','B','M','J'),('R','J','N','D'),('S','K','L','Z'),('C','L','P','Y'),('J','M','W','N')),
     10,13,'J',tuple(('J',a) for a in A),True),
 'extra_outside_J_ordinary':(
     A+('E','J','K','L','Y','M','N','P'),
     BASE+(('X','R','J'),('S','D','K'),('Z','C','L'),
           ('X','B','M','J'),('R','J','N','D'),('S','K','L','Z'),('C','L','P','Y'),('J','M','N')),
     10,14,'E',(('J','F'),('J','E')),True),
 'extra_endpoint_X':(
     A+('K','H','L','Y','A','M','N','O'),
     BASE+(('R','K','D'),('S','Z','L'),
           ('R','X','H','K'),('X','B','A','H'),('S','D','M','L'),('Z','L','N','C'),('D','K','O','M'),
           ('B','Y','A'),('C','N','Y'),('L','M','N'),('K','H','O')),
     9,13,'X',(('L','F'),),True),
 'extra_inner_R_SZ_paired':(
     A+('K','H','L','Y','A','M','N','O'),
     BASE+(('X','B','K'),('S','Z','L'),
           ('R','X','K','H'),('R','H','A','D'),('B','Y','M','K'),('S','D','N','L'),('Z','L','O','C'),
           ('D','A','N'),('C','O','Y'),('L','N','O'),('K','M','H')),
     9,13,'R',(('L','F'),),True),
 'extra_inner_R_SZ_separate':(
     A+('K','H','L','M','Y','A','N','P'),
     BASE+(('X','B','K'),('S','D','L'),('Z','C','M'),
           ('R','X','K','H'),('R','H','A','D'),('B','Y','N','K'),('S','L','M','Z'),
           ('D','A','P','L'),('C','M','P','Y'),('K','N','H'),('L','P','M')),
     9,13,'R',(),True)}

def normalize(labels):
    rename = {}
    answer = []
    for old in labels:
        if old not in rename:
            rename[old] = len(rename)
        answer.append(rename[old])
    return tuple(answer)


def face_key(face):
    rotations = [face[i:] + face[:i] for i in range(len(face))]
    reverse = face[::-1]
    rotations.extend(reverse[i:] + reverse[:i] for i in range(len(face)))
    return min(rotations)


def schemas(names, faces):
    ids = {name: i for i, name in enumerate(names)}
    return tuple(tuple(ids[name] for name in f) for f in faces)


def check(labels, spec, use_orientability=True):
    names, face_words, initial, early, extra, required_distinct, use_triangle_roles = spec
    for a, b in required_distinct:
        if a < len(labels) and b < len(labels) and labels[a] == labels[b]:
            return False
    faces = set()
    assigned = len(labels)
    for word in face_words:
        if max(word) >= assigned:
            continue
        actual = tuple(labels[v] for v in word)
        if len(set(actual)) != len(actual):
            return False
        faces.add(face_key(actual))
    # Label universe is fixed 0..16; unused points have no effect.
    edges = [0] * 17
    banned = [0] * 17
    link = [{} for _ in range(17)]
    corner_counts = [0] * 17
    triangle_counts = [0] * 17
    for face in faces:
        size = len(face)
        if size == 4:
            for offset in (0, 1):
                a, b = face[offset], face[offset + 2]
                banned[a] |= 1 << b
                banned[b] |= 1 << a
        for pos, v in enumerate(face):
            a, b = face[pos - 1], face[(pos + 1) % size]
            edges[v] |= (1 << a) | (1 << b)
            corner_counts[v] += 1
            triangle_counts[v] += size == 3
            if b in link[v].get(a, set()):
                # Different actual faces cannot occupy the same link edge.
                return False
            link[v].setdefault(a, set()).add(b)
            link[v].setdefault(b, set()).add(a)
    for v in range(17):
        degree = 5 if v == 0 else 3 if v == 1 else 4
        if edges[v] & banned[v] or edges[v].bit_count() > degree or corner_counts[v] > degree:
            return False
        extra_label = labels[extra] if extra is not None and extra < assigned else None
        role = 0 if v == 1 else 1 if v in (6, 7, 8, extra_label) else 2
        if use_triangle_roles and (triangle_counts[v] > role
                or corner_counts[v] - triangle_counts[v] > degree - role):
            return False
        if any(len(row) > 2 for row in link[v].values()):
            return False
        # A finite undirected link graph of max degree two consists of paths
        # and cycles. A cycle must be the entire prescribed spherical link.
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
                if len(component) != degree or edges[v].bit_count() != degree:
                    return False
                if use_triangle_roles and triangle_counts[v] != role:
                    return False
    for a, b in combinations(range(17), 2):
        if (edges[a] & edges[b]).bit_count() > 2:
            return False
    if use_orientability:
        # Choose orientations independently of the production face order.
        # Opposite traversals on every shared edge must be achievable by one
        # sign per actual face. A contradictory signed dual cycle obstructs
        # any embedding of these cells in an orientable sphere.
        boundary = {}
        actual_faces = sorted(faces)
        for index, face in enumerate(actual_faces):
            for i, a in enumerate(face):
                b = face[(i + 1) % len(face)]
                boundary.setdefault(tuple(sorted((a, b))), []).append(
                    (index, 1 if a < b else -1))
        dual = [[] for _ in actual_faces]
        for occupants in boundary.values():
            if len(occupants) > 2:
                return False
            if len(occupants) == 2:
                (a, sign_a), (b, sign_b) = occupants
                multiplier = -sign_a * sign_b
                dual[a].append((b, multiplier))
                dual[b].append((a, multiplier))
        signs = {}
        for root in range(len(actual_faces)):
            if root in signs:
                continue
            signs[root] = 1
            stack = [root]
            while stack:
                a = stack.pop()
                for b, multiplier in dual[a]:
                    desired = signs[a] * multiplier
                    if b in signs:
                        if signs[b] != desired:
                            return False
                    else:
                        signs[b] = desired
                        stack.append(b)
        # No prescribed oriented-edge rule, global counts or K4 test.
    return True


def specification(case):
    names, faces, initial, early, extra, distinct, roles = UNORIENTED_SCHEMAS[case]
    number={n:i for i,n in enumerate(names)}
    return (names,schemas(names,faces),initial,early,
            None if extra is None else number[extra],
            tuple((number[a],number[b]) for a,b in distinct),roles)


def audit(case):
    spec=specification(case)
    names,words,initial,early,extra,distinct,roles=spec
    early_states=set();raw_early=0
    for tail in product(range(early),repeat=early-initial):
        raw_early+=1
        labels=tuple(range(initial))+tail
        if check(labels,spec):
            early_states.add(normalize(labels))
    universe=16 if case=='both_paired' else 17
    final=set();raw_full=0;accepted_raw=0
    for prefix in sorted(early_states):
        for tail in product(range(universe),repeat=len(names)-early):
            raw_full+=1
            labels=prefix+tail
            if check(labels,spec):
                accepted_raw+=1;final.add(normalize(labels))
    production=json.loads((Path(__file__).resolve().parent/'EXPECTED.json').read_text())['covers'][case]
    if [list(p) for p in sorted(early_states)]!=production['passing_partitions_by_depth'][str(early)]:
        raise RuntimeError('Early normalized partitions differ entrywise: '+case)
    if [list(p) for p in sorted(final)]!=production['survivors']:
        raise RuntimeError('Final normalized partitions differ entrywise: '+case)
    if any(max(p)<15 for p in final):
        raise RuntimeError('Fifteen-point assignment unexpectedly survives: '+case)
    return {'names':names,'initial_distinct':initial,'early_boundary':early,
            'triangle_and_quadrilateral_roles_used':roles,'raw_early_tuples':raw_early,
            'early_normalized_states':sorted(early_states),'raw_full_tuples':raw_full,
            'accepted_raw_full_tuples':accepted_raw,'normalized_final_partitions':sorted(final),
            'with_at_most_15_classes':[]}


def controls():
    paired=specification('both_paired')
    quotient=(0,1,2,3,4,5,6,7,8,9,10,8,10,7,6,9)
    if not check(quotient,paired,False) or check(quotient,paired,True):
        raise RuntimeError('Nonorientable local quotient control differs')
    if check(tuple(range(15))+(14,12),specification('extra_equals_J')):
        raise RuntimeError('Ordinary vertex with three Q corners accepted')
    separate=specification('extra_inner_R_SZ_separate')
    if check(tuple(range(17)),separate):
        raise RuntimeError('Inner-separate Q-capacity control accepted')
    names,words,initial,early,extra,distinct,roles=separate
    last_Q=schemas(names,(('C','M','P','Y'),))[0]
    trimmed=(names,tuple(w for w in words if w!=last_Q),initial,early,extra,distinct,roles)
    if not check(tuple(range(17)),trimmed):
        raise RuntimeError('Trimmed positive partial patch rejected')
    return {'nonorientable_quotient_local_accept_dual_reject':quotient,
            'E_equals_J_fifteen_point_Q_capacity_rejected':True,
            'inner_separate_full_identity_rejected':True,
            'inner_separate_without_last_Q_identity_accepted':True}


def report(results):
    return {'agent':'six-tammes-1','role':'researcher',
            'status':'SEPARATE_RAW_LABEL_UNORIENTED_SIGNED_DUAL_AUDIT_SAME_AUTHOR',
            'results':results,'controls':controls(),
            'entrywise_comparison':'All early-boundary normalized partitions and every final partition match the separate production fixture.',
            'scope':'Separate representation and exhaustive algorithm by the same author; written face/role/topology bridges and independent review remain external.'}


def run(case=None):
    chosen=(case,) if case is not None else tuple(UNORIENTED_SCHEMAS)
    return report({c:audit(c) for c in chosen})


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',choices=tuple(UNORIENTED_SCHEMAS))
    args=parser.parse_args()
    print(json.dumps(run(args.case),indent=2,sort_keys=True))

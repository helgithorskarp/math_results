"""Exact original-face alias covers; see PROOF.md for the written bridges.

Standard library only. No solver, floating arithmetic or private input.
The generic strip tests use triangle maxima, not invented exact roles.
"""
from collections import Counter
from itertools import combinations
import json


def cyclic(face):
    return min(face[i:] + face[:i] for i in range(len(face)))


def necessary(partition, spec):
    assigned = len(partition)
    for a, b in spec['distinct']:
        if a < assigned and b < assigned and partition[a] == partition[b]:
            return 'forbidden_anchor_alias'
    faces = set()
    for word in spec['faces']:
        if max(word) >= assigned:
            continue
        face = tuple(partition[index] for index in word)
        if len(set(face)) != len(face):
            return 'nonsimple_face'
        if cyclic(face[::-1]) in faces:
            return 'reversed_face'
        # Repeated descriptions of the same actual face coalesce.
        faces.add(cyclic(face))
    count = max(partition) + 1
    degrees = [4] * count
    degrees[partition[0]], degrees[partition[1]] = 5, 3
    maxima = [2] * count
    maxima[partition[0]], maxima[partition[1]] = 3, 0
    exact = [None] * count
    if spec['mode'] == 'full':
        exact = maxima[:]
    for name, value in spec['maxima'].items():
        index = spec['number'][name]
        if index < assigned:
            maxima[partition[index]] = min(maxima[partition[index]], value)
    fixed = {}
    for name, value in spec['exact'].items():
        index = spec['number'][name]
        if index < assigned:
            actual = partition[index]
            if actual in fixed and fixed[actual] != value:
                return 'conflicting_exact_roles'
            fixed[actual] = value
            exact[actual] = value
            maxima[actual] = min(maxima[actual], value)
    if any(t is not None and t > maxima[v] for v, t in enumerate(exact)):
        return 'inconsistent_role_bounds'
    neighbors = [set() for _ in range(count)]
    outgoing = [dict() for _ in range(count)]
    incoming = [dict() for _ in range(count)]
    triangles, corners = [0] * count, [0] * count
    edges, nonedges, darts = set(), set(), set()
    for face in faces:
        size = len(face)
        if size == 4:
            nonedges.add(tuple(sorted((face[0], face[2]))))
            nonedges.add(tuple(sorted((face[1], face[3]))))
        for i, v in enumerate(face):
            before, after = face[i - 1], face[(i + 1) % size]
            if (v, after) in darts:
                return 'repeated_oriented_edge'
            darts.add((v, after))
            edges.add(tuple(sorted((v, after))))
            neighbors[v].update((before, after))
            triangles[v] += size == 3
            corners[v] += 1
            if (before in outgoing[v] and outgoing[v][before] != after
                    or after in incoming[v] and incoming[v][after] != before):
                return 'incompatible_star'
            outgoing[v][before], incoming[v][after] = after, before
    if edges & nonedges:
        return 'contact_Q_diagonal'
    for v in range(count):
        if len(neighbors[v]) > degrees[v] or corners[v] > degrees[v]:
            return 'excess_degree'
        if triangles[v] > maxima[v]:
            return 'excess_triangles'
        if exact[v] is not None and corners[v] - triangles[v] > degrees[v] - exact[v]:
            return 'excess_quadrilateral_corners'
        for start in outgoing[v]:
            visited, cursor = set(), start
            while cursor in outgoing[v] and cursor not in visited:
                visited.add(cursor)
                cursor = outgoing[v][cursor]
            if cursor in visited:
                if len(visited) != degrees[v] or len(neighbors[v]) != degrees[v]:
                    return 'proper_closed_link'
                if exact[v] is not None and triangles[v] != exact[v]:
                    return 'closed_star_wrong_triangle_role'
    for a, b in combinations(range(count), 2):
        if len(neighbors[a] & neighbors[b]) > 2:
            return 'three_common_contacts'
    for a, b, c in combinations(range(count), 3):
        if b in neighbors[a] and c in neighbors[a] and c in neighbors[b]:
            if neighbors[a] & neighbors[b] & neighbors[c]:
                return 'contact_K4'
    return None


ANCHORS = ('F', 'U', 'X', 'R', 'S', 'Z', 'B', 'C', 'Y')
CORE = (('F','X','R'), ('F','R','S'), ('F','S','Z'),
        ('F','U','B','X'), ('F','Z','C','U'), ('U','C','Y','B'),
        ('R','L','K','S'), ('R','X','P','L'), ('S','K','Q','Z'))
CASES = ('strip_both_ordinary', 'strip_L_ordinary_K_zero',
         'strip_L_zero_K_ordinary', 'one_T_L', 'one_T_K')


def schema(case):
    mode = 'maxima'
    maxima = {'B': 1, 'C': 1}
    exact = {'F': 3, 'U': 0, 'R': 2, 'S': 2}
    names = ANCHORS + ('L','K','P','Q','H')
    if case == 'strip_both_ordinary':
        words = CORE + (('L','H','K'), ('L','P','H'), ('K','H','Q'))
        exact.update(L=2, K=2)
    elif case == 'strip_L_ordinary_K_zero':
        words = CORE + (('L','H','K'),)
        exact.update(L=2, K=0)
    elif case == 'strip_L_zero_K_ordinary':
        words = CORE + (('K','L','H'),)
        exact.update(L=0, K=2)
    elif case == 'one_T_L':
        mode, maxima = 'full', {}
        names = ANCHORS + ('L','K','P','Q','H','A','D','J','M')
        words = CORE + (('C','Z','Q'), ('K','L','H'), ('K','H','Q'),
                        ('X','B','A','P'), ('L','P','D','H'),
                        ('B','Y','J','A'), ('C','Q','M','Y'))
        exact = {'F':3, 'U':0, 'B':0, 'C':1, 'X':1, 'L':1}
    elif case == 'one_T_K':
        mode, maxima = 'full', {}
        names = ANCHORS + ('K','L','P','Q','H','A','D','J','M')
        words = CORE + (('C','Z','Q'), ('L','H','K'), ('L','P','H'),
                        ('X','B','A','P'), ('K','H','D','Q'),
                        ('B','Y','J','A'), ('C','Q','M','Y'))
        exact = {'F':3, 'U':0, 'B':0, 'C':1, 'X':1, 'K':1}
    else:
        raise ValueError(case)
    number = {name: i for i, name in enumerate(names)}
    distinct_names = tuple((n, a) for n in ('L','K') for a in ANCHORS[:8]) + (('L','K'),)
    return {'case':case, 'names':names, 'number':number, 'words':words,
            'faces':tuple(tuple(number[n] for n in word) for word in words),
            'distinct':tuple((number[a],number[b]) for a,b in distinct_names),
            'mode':mode, 'maxima':maxima, 'exact':exact}


def cover(spec):
    nodes, rejects, passing, final = 0, Counter(), {}, []
    def visit(partition):
        nonlocal nodes
        nodes += 1
        if nodes > 200000:
            raise RuntimeError('INCOMPLETE: fixed local work budget')
        reason = necessary(partition, spec)
        if reason:
            rejects[reason] += 1
            return
        passing.setdefault(len(partition), []).append(partition)
        if len(partition) == len(spec['names']):
            final.append(partition)
            return
        # RGS: every earlier actual class, or one new class, is allowed.
        for value in range(max(partition) + 2):
            visit(partition + (value,))
    visit(tuple(range(9)))
    return {'names':spec['names'], 'faces':spec['words'], 'mode':spec['mode'],
            'maxima':spec['maxima'], 'exact':spec['exact'],
            'max_points':len(spec['names']), 'nodes':nodes,
            'passing_counts':{k:len(v) for k,v in passing.items()},
            'passing_partitions_by_depth':passing, 'rejects':dict(sorted(rejects.items())),
            'survivors':final, 'with_at_most_15_classes':[]}


def controls():
    positive, negative = {}, {}
    for case in CASES:
        spec = schema(case)
        identity = tuple(range(len(spec['names'])))
        negative[case + '_full_identity'] = necessary(identity, spec)
        if negative[case + '_full_identity'] is None:
            raise RuntimeError('Full negative control accepted: ' + case)
        if case.startswith('strip_'):
            trimmed = dict(spec)
            trimmed['faces'] = spec['faces'][:-1]
            if necessary(identity, trimmed) is not None:
                raise RuntimeError('Trimmed generic positive control rejected: ' + case)
            positive[case + '_without_last_T'] = identity
        else:
            if necessary(identity[:15], spec) is not None:
                raise RuntimeError('Main fifteen-slot positive prefix rejected: ' + case)
            positive[case + '_fifteen_slot_prefix'] = identity[:15]
    return {'positive_partial_consistency':positive, 'negative':negative}


def run():
    covers = {case:cover(schema(case)) for case in CASES}
    for case, result in covers.items():
        if result['survivors']:
            raise RuntimeError('Unexpected complete alias cover outcome: ' + case)
    return {'agent':'six-tammes-1', 'role':'researcher',
            'status':'AUTHOR_CHECKED_CONDITIONAL_ORIGINAL_FACE_CONTACT_SUBCASE_EXCLUSION',
            'excluded_subcase':{'profile':[1,3,1], 'F_contacts_U':True},
            'covers':covers, 'controls':controls(),
            'remaining_r1_profiles_full_interval':[[0,6,0],[0,4,1],[0,2,2],[1,5,0],[1,3,1]],
            'remaining_profile_1_3_1':'F-U noncontact; separated Q sectors and T fans of lengths two and one',
            'trust_boundary':'Written geometric capacities, anchors, face forcing, roles and topology; prior h7912 metric collar. Separate same-author audit, independent review pending. No global bound or unrestricted optimizer coverage.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))

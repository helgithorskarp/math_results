"""Exact complete alias cover of the forced paired and one-paired patches.

The sole sixteen-class survivor is not asserted a complete map or packing.
All later slots may reuse any earlier original unless the exact constraints forbid it.
The first nine names are distinct by the proved original F/U/Q structure.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import json

NAMES = ('F', 'U', 'X', 'R', 'S', 'Z', 'B', 'C', 'D',
         'J', 'K', 'Y', 'L', 'M', 'N', 'O')
NUMBER = {name: index for index, name in enumerate(NAMES)}
FACE_NAMES = (
    ('F', 'X', 'R'), ('F', 'S', 'Z'), ('R', 'X', 'J'), ('Z', 'S', 'K'),
    ('F', 'U', 'B', 'X'), ('F', 'R', 'D', 'S'), ('F', 'Z', 'C', 'U'),
    ('U', 'C', 'Y', 'B'),
    ('X', 'B', 'L', 'J'), ('R', 'J', 'M', 'D'),
    ('S', 'D', 'N', 'K'), ('Z', 'K', 'O', 'C'),
)
FACES = tuple(tuple(NUMBER[name] for name in face) for face in FACE_NAMES)


def cyclic(face):
    return min(face[i:] + face[:i] for i in range(len(face)))


def necessary(partition, zero, faces_spec=FACES, use_triangle_roles=True, required_distinct=()):
    """Only necessary complete-contact/star constraints; no invented faces."""
    assigned = len(partition)
    for a, b in required_distinct:
        if a < assigned and b < assigned and partition[a] == partition[b]:
            return 'identified_triangle_thirds'
    faces = set()
    for word in faces_spec:
        if any(index >= assigned for index in word):
            continue
        face = tuple(partition[index] for index in word)
        if len(set(face)) != len(face):
            return 'nonsimple_face'
        canon = cyclic(face)
        if cyclic(tuple(reversed(face))) in faces:
            return 'reversed_face'
        # Identical actual oriented faces are allowed to coalesce.
        faces.add(canon)
    count = max(partition) + 1
    degrees = [4] * count
    degrees[partition[0]], degrees[partition[1]] = 5, 3
    triangle_roles = [2] * count
    triangle_roles[partition[0]], triangle_roles[partition[1]] = 2, 0
    for name in ('B', 'C', 'D'):
        triangle_roles[partition[NUMBER[name]]] = 0 if name == zero else 1
    neighbors = [set() for _ in range(count)]
    outgoing = [dict() for _ in range(count)]
    incoming = [dict() for _ in range(count)]
    triangles = [0] * count
    corner_count = [0] * count
    edges, nonedges, darts = set(), set(), set()
    for face in faces:
        length = len(face)
        if length == 4:
            nonedges.add(tuple(sorted((face[0], face[2]))))
            nonedges.add(tuple(sorted((face[1], face[3]))))
        for i, v in enumerate(face):
            before, after = face[i - 1], face[(i + 1) % length]
            if (v, after) in darts:
                return 'repeated_oriented_edge'
            darts.add((v, after))
            edges.add(tuple(sorted((v, after))))
            neighbors[v].update((before, after))
            triangles[v] += length == 3
            corner_count[v] += 1
            if (before in outgoing[v] and outgoing[v][before] != after
                    or after in incoming[v] and incoming[v][after] != before):
                return 'incompatible_star'
            outgoing[v][before], incoming[v][after] = after, before
    if edges & nonedges:
        return 'contact_Q_diagonal'
    for v in range(count):
        if len(neighbors[v]) > degrees[v] or corner_count[v] > degrees[v]:
            return 'excess_degree'
        if use_triangle_roles and triangles[v] > triangle_roles[v]:
            return 'excess_triangles'
        # A closed subcycle of a spherical vertex link must be its whole star.
        for start in outgoing[v]:
            walked = set()
            cursor = start
            while cursor in outgoing[v] and cursor not in walked:
                walked.add(cursor)
                cursor = outgoing[v][cursor]
            if cursor in walked:
                if len(walked) != degrees[v] or len(neighbors[v]) != degrees[v]:
                    return 'proper_closed_link'
                if use_triangle_roles and triangles[v] != triangle_roles[v]:
                    return 'closed_star_wrong_triangle_role'
    for a, b in combinations(range(count), 2):
        if len(neighbors[a] & neighbors[b]) > 2:
            return 'three_common_contacts'
    # Four distinct pairwise c-contact vectors have a positive-definite Gram
    # matrix for 0<c<1, contradicting rank at most three.
    for a, b, c in combinations(range(count), 3):
        if b in neighbors[a] and c in neighbors[a] and c in neighbors[b]:
            if neighbors[a] & neighbors[b] & neighbors[c]:
                return 'contact_K4'
    return None


def cover(zero, max_points=16, names=NAMES, faces_spec=FACES, use_triangle_roles=True, required_distinct=()):
    rejects = Counter()
    prefixes = Counter()
    survivors = []
    passing = {}
    nodes = 0

    def visit(partition):
        nonlocal nodes
        nodes += 1
        reason = necessary(partition, zero, faces_spec, use_triangle_roles, required_distinct)
        if reason:
            rejects[reason] += 1
            return
        prefixes[len(partition)] += 1
        passing.setdefault(len(partition), []).append(partition)
        if len(partition) == len(names):
            survivors.append(partition)
            return
        # Restricted-growth strings enumerate every partition of these
        # slots, with the nine original anchors distinct, exactly once.
        number = max(partition) + 1
        for value in range(min(number + 1, max_points)):
            visit(partition + (value,))

    visit(tuple(range(9)))
    return {'zero_T_opposite': zero, 'max_points': max_points, 'visited_nodes': nodes,
            'surviving_prefix_counts': dict(sorted(prefixes.items())),
            'rejection_counts': dict(sorted(rejects.items())),
            'survivors': survivors, 'passing_partitions_by_depth': passing}


SINGLE_NAMES = ('F', 'U', 'X', 'R', 'S', 'Z', 'B', 'C', 'D',
                'J', 'K', 'L', 'Y', 'M', 'N', 'P')
SINGLE_FACE_NAMES = (
    ('F', 'X', 'R'), ('F', 'S', 'Z'), ('R', 'X', 'J'),
    ('S', 'D', 'K'), ('C', 'Z', 'L'), ('J', 'M', 'N'),
    ('F', 'U', 'B', 'X'), ('F', 'R', 'D', 'S'), ('F', 'Z', 'C', 'U'),
    ('U', 'C', 'Y', 'B'), ('X', 'B', 'M', 'J'), ('R', 'J', 'N', 'D'),
    ('S', 'K', 'L', 'Z'), ('C', 'L', 'P', 'Y'))
SINGLE_NUMBER = {name: i for i, name in enumerate(SINGLE_NAMES)}
SINGLE_FACES = tuple(tuple(SINGLE_NUMBER[name] for name in face) for face in SINGLE_FACE_NAMES)
NONORIENTABLE_QUOTIENT = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 8, 10, 7, 6, 9)


def run():
    paired = cover('D', 16, NAMES, FACES, False, ((0, 9), (0, 10)))
    single = cover('B', 16, SINGLE_NAMES, SINGLE_FACES, True, ((0, 9),))
    identity = tuple(range(16))
    for name, result in (('paired', paired), ('single', single)):
        if result['survivors'] != [identity]:
            raise RuntimeError('Unexpected normalized full partition: ' + name)
    negatives = {}
    for name, partition in (
        ('merged_triangle_third', identity[:9] + (0,) + identity[10:]),
        ('contact_Q_diagonal', identity[:12] + (3,) + identity[13:]),
        ('nonorientable_eleven_class_quotient', NONORIENTABLE_QUOTIENT)):
        reason = necessary(partition, 'D', FACES, False, ((0, 9), (0, 10)))
        if reason is None:
            raise RuntimeError('Negative control accepted: ' + name)
        negatives[name] = reason
    return {
        'agent': 'six-tammes-1', 'role': 'researcher',
        'status': 'AUTHOR_CHECKED_EXACT_ORIGINAL_FACE_ALIAS_EXCLUSION',
        'hypotheses': 'See PROOF.md. Necessary partial star/contact checks, not a global optimizer cover.',
        'names': {'paired': NAMES, 'single': SINGLE_NAMES},
        'oriented_faces': {'paired': FACE_NAMES, 'single': SINGLE_FACE_NAMES},
        'covers': {'paired': paired, 'single': single},
        'controls': {'negative': negatives, 'positive': 'All sixteen slots distinct satisfies both necessary patch predicates.'},
        'excluded_profile': [2, 2, 1],
        'remaining_r1_profiles_full_interval': [[0, 6, 0], [0, 4, 1], [0, 2, 2], [1, 5, 0], [1, 3, 1], [2, 4, 0]],
        'remaining_profiles_on_beta': {'r1': 6, 'r2': 12, 'r3': 11, 'total': 29},
        'trust_boundary': 'Hand forced-face/anchor/role bridges and spherical topology are unformalized; independent review pending. No floating arithmetic, solver, private input or incomplete search.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))

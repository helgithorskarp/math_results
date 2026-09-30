"""Different static, unoriented, raw-label audit of the named-slot alias cover.

No production predicate/enumerator is imported. The face schema is copied
from the written patch, and all preliminary raw labellings are checked.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import json

ANCHORS = ('F', 'U', 'X', 'R', 'S', 'Z', 'B', 'C', 'D')
PAIRED_NAMES = ANCHORS + ('J', 'K', 'Y', 'L', 'M', 'N', 'O')
SINGLE_NAMES = ANCHORS + ('J', 'K', 'L', 'Y', 'M', 'N', 'P')
PAIRED_FACES = (
    ('F', 'X', 'R'), ('F', 'S', 'Z'), ('R', 'X', 'J'), ('Z', 'S', 'K'),
    ('F', 'U', 'B', 'X'), ('F', 'R', 'D', 'S'), ('F', 'Z', 'C', 'U'),
    ('U', 'C', 'Y', 'B'), ('X', 'B', 'L', 'J'), ('R', 'J', 'M', 'D'),
    ('S', 'D', 'N', 'K'), ('Z', 'K', 'O', 'C'))
SINGLE_FACES = (
    ('F', 'X', 'R'), ('F', 'S', 'Z'), ('R', 'X', 'J'),
    ('S', 'D', 'K'), ('C', 'Z', 'L'), ('J', 'M', 'N'),
    ('F', 'U', 'B', 'X'), ('F', 'R', 'D', 'S'), ('F', 'Z', 'C', 'U'),
    ('U', 'C', 'Y', 'B'), ('X', 'B', 'M', 'J'), ('R', 'J', 'N', 'D'),
    ('S', 'K', 'L', 'Z'), ('C', 'L', 'P', 'Y'))


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


def check(labels, face_words, zero, use_triangle_roles=True, required_distinct=(), use_orientability=True):
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
    # Label universe is fixed 0..15; unused points have no effect.
    edges = [0] * 16
    banned = [0] * 16
    link = [{} for _ in range(16)]
    corner_counts = [0] * 16
    triangle_counts = [0] * 16
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
    for v in range(16):
        degree = 5 if v == 0 else 3 if v == 1 else 4
        if edges[v] & banned[v] or edges[v].bit_count() > degree or corner_counts[v] > degree:
            return False
        role = 0 if v == 1 or v == zero else 1 if v in (6, 7, 8) else 2
        if use_triangle_roles and triangle_counts[v] > role:
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
    for a, b in combinations(range(16), 2):
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


def audit(names, faces, early, zero, use_triangle_roles, required_distinct):
    words = schemas(names, faces)
    raw_early = 0
    early_states = set()
    for tail in product(range(early), repeat=early - 9):
        raw_early += 1
        labels = tuple(range(9)) + tail
        if check(labels, words, zero, use_triangle_roles, required_distinct):
            early_states.add(normalize(labels))
    full = set()
    raw_full = 0
    accepted_raw = 0
    for prefix in sorted(early_states):
        for tail in product(range(16), repeat=16 - early):
            raw_full += 1
            labels = prefix + tail
            if check(labels, words, zero, use_triangle_roles, required_distinct):
                accepted_raw += 1
                full.add(normalize(labels))
    return {
        'names': names, 'zero_T_original_label': zero,
        'triangle_roles_used': use_triangle_roles,
        'required_distinct_triangle_thirds': required_distinct,
        'raw_early_tuples': raw_early,
        'early_normalized_states': sorted(early_states),
        'raw_full_tuples': raw_full, 'accepted_raw_full_tuples': accepted_raw,
        'normalized_final_partitions': sorted(full),
        'with_at_most_15_classes': sorted(p for p in full if max(p) < 15)}


NONORIENTABLE_QUOTIENT = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 8, 10, 7, 6, 9)


def run():
    paired = audit(PAIRED_NAMES, PAIRED_FACES, 12, 8, False, ((0, 9), (0, 10)))
    single = audit(SINGLE_NAMES, SINGLE_FACES, 13, 6, True, ((0, 9),))
    results = {'paired': paired, 'single': single}
    production = json.loads((Path(__file__).resolve().parent / 'EXPECTED.json').read_text())
    for key, result in results.items():
        if result['normalized_final_partitions'] != [tuple(range(16))] or result['with_at_most_15_classes']:
            raise RuntimeError('Unexpected raw-label alias cover: ' + key)
        depth = '12' if key == 'paired' else '13'
        expected = production['covers'][key]
        actual_early = [list(v) for v in result['early_normalized_states']]
        actual_final = [list(v) for v in result['normalized_final_partitions']]
        if actual_early != expected['passing_partitions_by_depth'][depth] or actual_final != expected['survivors']:
            raise RuntimeError('Entrywise early/full normalized partition comparison differs: ' + key)
    words = schemas(PAIRED_NAMES, PAIRED_FACES)
    if not check(NONORIENTABLE_QUOTIENT, words, 8, False, ((0, 9), (0, 10)), False):
        raise RuntimeError('Unoriented local quotient control no longer passes local rules')
    if check(NONORIENTABLE_QUOTIENT, words, 8, False, ((0, 9), (0, 10)), True):
        raise RuntimeError('Nonorientable quotient incorrectly accepted')
    actual_faces = {face_key(tuple(NONORIENTABLE_QUOTIENT[v] for v in word)) for word in words}
    actual_edges = {tuple(sorted((face[i - 1], face[i])))
                    for face in actual_faces for i in range(len(face))}
    topology = {'vertices': len(set(NONORIENTABLE_QUOTIENT)),
                'edges': len(actual_edges), 'faces': len(actual_faces)}
    topology['Euler_characteristic'] = topology['vertices'] - topology['edges'] + topology['faces']
    if tuple(topology[k] for k in ('vertices', 'edges', 'faces', 'Euler_characteristic')) != (11, 22, 12, 1):
        raise RuntimeError('Unexpected quotient topology')
    return {
        'agent': 'six-tammes-1', 'role': 'researcher',
        'status': 'SEPARATE_RAW_LABEL_UNORIENTED_SIGNED_DUAL_AUDIT_SAME_AUTHOR',
        'results': results,
        'entrywise_comparison': 'Every normalized early-boundary tuple and every final partition agrees with the separate production expected fixture.',
        'control': {'nonorientable_quotient': NONORIENTABLE_QUOTIENT,
                    'passes_local_unoriented_rules': True, 'fails_signed_dual_orientability': True,
                    'closed_abstract_cell_complex': topology},
        'scope': 'Independent representation/algorithm by this author; independent mathematical review and formalization pending.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))

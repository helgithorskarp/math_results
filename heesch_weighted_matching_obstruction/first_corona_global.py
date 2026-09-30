"""Exact contact certificate for global first-corona endpoint rigidity.

The proof is geometric (first_corona_global.md), not an inference from rank.
Coordinates below mean physical (x, sqrt(3)*y); all arithmetic is rational.
"""
from collections import defaultdict, deque
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import endpoint_rigidity as er
import mixed_hand_profiles as mp
import hex_domain as hd

FIXTURE_SHA256 = er.FIXTURE_SHA256


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def negate(a):
    return tuple(-x for x in a)


def apply(matrix, point):
    return tuple(sum(x*y for x, y in zip(row, point)) for row in matrix)


def isometry(matrix, translation, point):
    return add(apply(matrix, point), translation)


def normal_form(epsilon):
    if epsilon not in (-1, 1):
        raise ValueError('The two normal forms differ by a global reflection')
    identity = ((F(1), F(0)), (F(0), F(1)))
    reflection = ((F(-1), F(0)), (F(0), F(1)))
    rotation = ((F(1, 2), F(-3*epsilon, 2)),
                (F(epsilon, 2), F(1, 2)))
    d, u, a = (F(1), F(0)), (F(-1, 2), F(-epsilon, 2)), (F(1, 2), F(epsilon, 6))
    vertices = [(F(0), F(0)) for _ in range(18)]
    for k in range(5):
        vertices[4*k] = (F(k), F(0))
        vertices[4*k+1] = add(add(a, u), (F(k), F(0)))
        if k < 4:
            vertices[4*k+2] = add(a, (F(k), F(0)))
            vertices[4*k+3] = add(u, (F(k+1), F(0)))
    h_translation = (F(8), F(0))
    k_translation = negate(apply(rotation, vertices[13]))
    motions = [(identity, (F(0), F(0))), (identity, u), (identity, negate(u)),
               (rotation, k_translation),
               (reflection, add(h_translation, u)), (reflection, h_translation)]
    metric = ((F(1), F(0)), (F(0), F(3)))
    for matrix, _ in motions:
        for i in range(2):
            for j in range(2):
                assert sum(matrix[k][i]*metric[k][l]*matrix[l][j]
                           for k in range(2) for l in range(2)) == metric[i][j]
    assert apply(rotation, d) == negate(u)
    assert add(a, u) == negate(apply(rotation, a))
    assert add(apply(reflection, u), negate(u)) == d
    assert len(set(vertices)) == 18
    return vertices, motions


def contact_groups(witness, vertices, descriptions):
    independently_decoded, interfaces = er.interface_endpoint_groups(witness, vertices)
    forward = defaultdict(set)
    for record in descriptions:
        forward[tuple(record['point'])].update([tuple(record['anchor']), tuple(record['other'])])
    if dict(forward) != independently_decoded:
        raise ValueError('Closed-form vertices and inverse full-port decoder disagree')
    return independently_decoded, interfaces


def proof_pairs():
    """Actual labelled endpoint equations used in the written proof."""
    blocks = {
        'h_fixes_two_points': [(0, 16, 5, 16), (0, 17, 5, 17)],
        'l_equals_g_h': [(1, 16, 4, 16), (1, 17, 4, 17)],
        'right_r_relations': [(4, i, 5, i+3) for i in range(0, 13, 2)],
        'root_g_relations': [(0, i, 1, i+1) for i in range(1, 16, 2)],
        'right_last_vertex': [(0, 17, 4, 14)],
        'left_k_relations': [(0, 0, 3, 13), (0, 1, 3, 11), (0, 2, 3, 15), (1, 1, 3, 7)],
        'g2_inverse_relations': [(0, 4, 2, 3), (0, 6, 2, 5)],
    }
    return blocks


def normalized_axial(vertex):
    # L(x,y)=(sqrt(3)*(x+y/2),3*y/2). Subtract L(-2,1),
    # divide by 3*sqrt(3), and write the result as (x,sqrt(3)*y).
    x, y = vertex
    return F(2*x+y+3, 6), F(y-1, 6)


def pose_propagation(witness, vertices, descriptions):
    """Determine all remaining poses using two distinct labelled endpoints."""
    groups, interfaces = contact_groups(witness, vertices, descriptions)
    by_pair = defaultdict(set)
    for incidents in groups.values():
        incidents = sorted(incidents)
        for position, (a, i) in enumerate(incidents):
            for b, j in incidents[position+1:]:
                by_pair[a, b].add((i, j))
    adjacency = defaultdict(list)
    for (a, b), matches in sorted(by_pair.items()):
        matches = sorted(matches)
        chosen = next(((p, q) for p in matches for q in matches
                       if p[0] != q[0] and p[1] != q[1]), None)
        if chosen:
            adjacency[a].append((b, chosen))
            adjacency[b].append((a, tuple((j, i) for i, j in chosen)))
    reached, queue, tree = {0}, deque([0]), []
    while queue:
        a = queue.popleft()
        for b, pairs in sorted(adjacency[a]):
            if b not in reached:
                reached.add(b)
                queue.append(b)
                tree.append({'from': a, 'to': b, 'endpoint_matches': pairs})
    if len(reached) != len(witness['patch']):
        raise ValueError('The two-endpoint contact graph does not reach every pose')
    return {'copies_reached': len(reached), 'two_endpoint_tree_edges': len(tree),
            'shared_vertex_groups': len(groups), 'unit_interfaces': interfaces,
            'tree_sha256': hashlib.sha256(json.dumps(tree, separators=(',', ':'), sort_keys=True).encode()).hexdigest()}


def arc_orientation_certificate(witness, vertices, motions):
    """Infer relative hands from labelled oriented arcs, without reading hands.

    Prototype arcs are directed with prototype interior on the left. Adjacent
    Jordan-disc interiors on opposite sides of a shared arc require opposite
    induced boundary orientations. Start-start matching forces opposite hands;
    start-end matching forces equal hands.
    """
    index = {point: i for i, point in enumerate(vertices)}
    ports = []
    for owner, neighbor in hd.boundary(witness['tile']):
        d = er.N.index((neighbor[0]-owner[0], neighbor[1]-owner[1]))
        ends = []
        for e in ((d-1) % 6, (d+1) % 6):
            ends.append(index[(3*owner[0]+er.N[d][0]+er.N[e][0],
                               3*owner[1]+er.N[d][1]+er.N[e][1])])
        ports.append(tuple(ends))
    following = dict(ports)
    if len(following) != len(vertices):
        raise ValueError('Prototype oriented ports are not a simple cycle')
    cycle, current = [], 0
    while current not in cycle:
        cycle.append(current)
        current = following[current]
    if current != 0 or len(cycle) != len(vertices):
        raise ValueError('Prototype oriented ports fail to visit every vertex')
    edges = defaultdict(list)
    for a, motion in enumerate(motions):
        for port, (i, j) in enumerate(ports):
            ends = tuple(add(er.multiply(motion['matrix'], vertices[b]), motion['translation'])
                         for b in (i, j))
            edges[tuple(sorted(ends))].append((a, port, ends))
    constraints, adjacency = [], defaultdict(list)
    for owners in edges.values():
        if len(owners) == 1:
            continue
        if len(owners) != 2:
            raise ValueError('A shared full arc must have exactly two owners')
        (a, i, x), (b, j, y) = sorted(owners)
        if x == y:
            delta = -1
        elif x == y[::-1]:
            delta = 1
        else:
            raise ValueError('Inconsistent arc endpoint correspondence')
        constraints.append((a, i, b, j, delta))
        adjacency[a].append((b, delta)); adjacency[b].append((a, delta))
    hands, queue = {0: 1}, deque([0])
    while queue:
        a = queue.popleft()
        for b, delta in adjacency[a]:
            value = hands[a]*delta
            if b in hands:
                if hands[b] != value:
                    raise ValueError('Boundary orientation constraints are inconsistent')
            else:
                hands[b] = value; queue.append(b)
    if len(hands) != len(motions):
        raise ValueError('The shared-arc graph does not reach every copy')
    inferred = [hands[a] for a in range(len(motions))]
    if inferred != [motion['hand'] for motion in motions]:
        raise ValueError('Arc orientation inference disagrees with the original poses')
    return {'prototype_counterclockwise_vertex_cycle': cycle,
            'oriented_full_arc_constraints': len(constraints),
            'copies_reached': len(hands), 'unique_hands_relative_to_root': inferred,
            'constraint_sha256': hashlib.sha256(json.dumps(sorted(constraints), separators=(',', ':')).encode()).hexdigest()}


def main():
    path = Path(__file__).with_name('signed_hex4_depth5.witness.json')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != FIXTURE_SHA256:
        raise ValueError('The attributed Mann-five baseline changed')
    witness = json.loads(raw)
    first = dict(witness, depth=1, patch=[record for record in witness['patch'] if record['level'] <= 1])
    vertices, original_motions, rows, descriptions, _, checks = er.framework(first)
    groups, interfaces = contact_groups(first, vertices, descriptions)
    if (len(first['patch']), len(vertices), len(groups), len(rows), interfaces) != (6, 18, 30, 70, 30):
        raise ValueError('The six-copy endpoint network changed')
    if [motion['hand'] for motion in original_motions] != [1, 1, 1, 1, -1, -1]:
        raise ValueError('The proof requires the original handedness pattern')
    blocks = proof_pairs()
    for pairs in blocks.values():
        for a, i, b, j in pairs:
            if not any({(a, i), (b, j)} <= incidents for incidents in groups.values()):
                raise ValueError('A proof equation is absent from the actual contact network')
    branch_results = []
    for epsilon in (1, -1):
        normal_vertices, normal_motions = normal_form(epsilon)
        for incidents in groups.values():
            points = {isometry(*normal_motions[a], normal_vertices[i]) for a, i in incidents}
            if len(points) != 1:
                raise ValueError('The normal form fails a full-network equation')
        branch_results.append({'epsilon': epsilon, 'all_35_vector_equations_exact': True})
    normal_vertices, normal_motions = normal_form(1)
    if list(map(normalized_axial, vertices)) != normal_vertices:
        raise ValueError('The normal form differs from the baseline endpoint geometry')
    for a, motion in enumerate(original_motions):
        for i, vertex in enumerate(vertices):
            moved = add(er.multiply(motion['matrix'], vertex), motion['translation'])
            if normalized_axial(moved) != isometry(*normal_motions[a], normal_vertices[i]):
                raise ValueError('A normalized original pose differs from the exact normal form')
    profiles = mp.analyze(first)
    if (profiles['even_coefficient_rank'], profiles['odd_coefficient_rank'],
        profiles['free_even_functions'], profiles['free_odd_functions'],
        profiles['odd_full_rank_core_determinant']) != (17, 18, 1, 0, '4'):
        raise ValueError('First-corona profile freedom changed')
    all_vertices, all_motions, _, all_descriptions, _, all_checks = er.framework(witness)
    propagation = pose_propagation(witness, all_vertices, all_descriptions)
    def rational_points(points):
        return [[str(x) for x in point] for point in points]
    result = {
        'agent': 'six-heesch-3', 'role': 'researcher', 'fixture_sha256': FIXTURE_SHA256,
        'first_corona_copies': 6, 'prototype_vertices': 18,
        'first_corona_shared_vertex_groups': len(groups), 'first_corona_unit_interfaces': interfaces,
        'first_corona_vector_equations': len(rows)//2,
        'required_proof_equations': {name: [list(pair) for pair in pairs] for name, pairs in blocks.items()},
        'coordinate_convention': 'Physical (x, sqrt(3)*y); d=(1,0), prototype vertex0=(0,0)',
        'positive_normal_form_vertices': rational_points(normal_vertices),
        'positive_normal_form_motions': [{'matrix': rational_points(matrix), 'translation': [str(x) for x in translation]}
                                        for matrix, translation in normal_motions],
        'normal_form_branches': branch_results,
        'global_rigidity_proof': 'Two-point isometry uniqueness implies Q=Q^2, then d=Hu-u and |u|=|d| force the +/-60-degree normal form',
        'first_corona_checks': checks, 'full_five_corona_checks': all_checks,
        'first_corona_profile_law': {'ports': profiles['ports'], 'unit_interfaces': profiles['unit_interfaces'],
            'distinct_signed_equations': profiles['distinct_signed_equations'],
            'even_rank': profiles['even_coefficient_rank'], 'odd_rank': profiles['odd_coefficient_rank'],
            'free_even_functions': profiles['free_even_functions'], 'free_odd_functions': profiles['free_odd_functions'],
            'odd_core_determinant': profiles['odd_full_rank_core_determinant'],
            'fixture_vector_is_even_kernel_vector': profiles['fixture_vector_is_even_kernel_vector']},
        'full_fixture_pose_propagation': propagation,
        'first_corona_arc_orientation': arc_orientation_certificate(first, vertices, original_motions),
        'full_fixture_arc_orientation': arc_orientation_certificate(witness, all_vertices, all_motions),
        'scope': 'Global labelled endpoint rigidity with distinct prototype vertices and original copy handedness; boundary curves and other contact networks require separate analysis',
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

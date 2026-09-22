"""Independent exact audit for the sparse-one-skeleton theorem.

Python 3.11+, standard library only.  This deliberately does not import the
producer's code.  It exhausts all triangle systems on six labelled vertices,
uses two independent prime-field eliminations, explores every maximal peeling
choice, recognizes every minimal dependence from definitions, and exhausts
small top-dimensional Morse matchings and weighted objectives.
"""

from array import array
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: i for i, edge in enumerate(EDGES)}
TRIANGLES = tuple(combinations(VERTICES, 3))


def oriented_column(triangle, prime):
    a, b, c = triangle
    column = [0] * len(EDGES)
    column[EDGE_INDEX[b, c]] = 1
    column[EDGE_INDEX[a, c]] = -1 % prime
    column[EDGE_INDEX[a, b]] = 1
    return tuple(column)


COLS = {prime: tuple(oriented_column(t, prime) for t in TRIANGLES)
        for prime in (2, 3)}
TRIANGLE_EDGE_MASKS = tuple(
    sum(1 << EDGE_INDEX[e] for e in combinations(t, 2)) for t in TRIANGLES
)
EDGE_TRIANGLE_MASKS = tuple(
    sum(1 << i for i, t in enumerate(TRIANGLES) if edge <= set(t))
    for edge in map(set, EDGES)
)
K5_EDGE_MASKS = tuple(
    sum(1 << i for i, edge in enumerate(EDGES) if omitted not in edge)
    for omitted in VERTICES
)


def rank_mod(mask, prime):
    """Rank of the selected oriented triangle columns over F_prime."""
    pivots = {}
    while mask:
        bit = mask & -mask
        vector = list(COLS[prime][bit.bit_length() - 1])
        mask ^= bit
        for pivot, basis_vector in pivots.items():
            coefficient = vector[pivot]
            if coefficient:
                vector = [(x - coefficient * y) % prime
                          for x, y in zip(vector, basis_vector)]
        pivot = next((i for i in range(len(EDGES) - 1, -1, -1)
                      if vector[i]), None)
        if pivot is not None:
            inverse = pow(vector[pivot], -1, prime)
            pivots[pivot] = tuple((inverse * x) % prime for x in vector)
    return len(pivots)


def triangle_mask(triangles):
    indices = {t: i for i, t in enumerate(TRIANGLES)}
    return sum(1 << indices[tuple(sorted(t))] for t in triangles)


def free_triangle_mask(mask):
    """Triangles having at least one edge of current triangle-degree one."""
    answer = 0
    for incidence in EDGE_TRIANGLE_MASKS:
        hit = mask & incidence
        if hit and not hit & (hit - 1):
            answer |= hit
    return answer


def general_sparse(n, edge_set):
    """Definition-level test of (H), used for the adversarial controls."""
    edge_set = set(edge_set)
    for size in range(3, n + 1):
        for vertices in combinations(range(n), size):
            chosen = set(vertices)
            induced = sum(set(edge) <= chosen for edge in edge_set)
            if induced > 3 * size - 6:
                return False
    return True


def is_sphere_circuit(mask):
    """Definition-level closed-surface and Euler-two recognition."""
    faces = [TRIANGLES[i] for i in range(len(TRIANGLES)) if mask >> i & 1]
    require(faces, 'empty circuit candidate')
    edge_degrees = Counter(e for t in faces for e in combinations(t, 2))
    require(set(edge_degrees.values()) == {2}, 'circuit is not edge-degree two')

    # Connected triangle adjacency.
    adjacent = {i: set() for i in range(len(faces))}
    for i, j in combinations(range(len(faces)), 2):
        if len(set(faces[i]) & set(faces[j])) == 2:
            adjacent[i].add(j)
            adjacent[j].add(i)
    seen, stack = set(), [0]
    while stack:
        i = stack.pop()
        if i not in seen:
            seen.add(i)
            stack.extend(adjacent[i] - seen)
    require(len(seen) == len(faces), 'circuit dual graph is disconnected')

    vertices = {v for t in faces for v in t}
    require(len(vertices) - len(edge_degrees) + len(faces) == 2,
            'circuit Euler characteristic is not two')
    for vertex in vertices:
        link_edges = [tuple(x for x in t if x != vertex)
                      for t in faces if vertex in t]
        link = {v: set() for e in link_edges for v in e}
        for a, b in link_edges:
            link[a].add(b)
            link[b].add(a)
        require(link and all(len(neighbors) == 2 for neighbors in link.values()),
                'vertex link is not two-regular')
        link_seen, link_stack = set(), [next(iter(link))]
        while link_stack:
            v = link_stack.pop()
            if v not in link_seen:
                link_seen.add(v)
                link_stack.extend(link[v] - link_seen)
        require(len(link_seen) == len(link), 'vertex link is disconnected')


def top_matching_masks(fixture_mask):
    """Enumerate acyclic edge/triangle matchings and return matched face sets."""
    face_ids = [i for i in range(len(TRIANGLES)) if fixture_mask >> i & 1]
    choices = [(-1,) + tuple(EDGE_INDEX[e] for e in combinations(TRIANGLES[i], 2))
               for i in face_ids]
    attained = set()
    assignments = valid = acyclic = 0
    for selection in product(*choices):
        assignments += 1
        matched_edges = [edge for edge in selection if edge >= 0]
        if len(matched_edges) != len(set(matched_edges)):
            continue
        valid += 1
        matched = [face_ids[j] for j, edge in enumerate(selection) if edge >= 0]
        outgoing = {i: set() for i in matched}
        indegree = {i: 0 for i in matched}
        for target in matched:
            matched_edge = set(EDGES[selection[face_ids.index(target)]])
            for source in matched:
                if source != target and matched_edge <= set(TRIANGLES[source]):
                    if target not in outgoing[source]:
                        outgoing[source].add(target)
                        indegree[target] += 1
        ready = [i for i in matched if indegree[i] == 0]
        visited = 0
        while ready:
            source = ready.pop()
            visited += 1
            for target in outgoing[source]:
                indegree[target] -= 1
                if indegree[target] == 0:
                    ready.append(target)
        if visited == len(matched):
            acyclic += 1
            attained.add(sum(1 << i for i in matched))
    return attained, assignments, valid, acyclic


def greedy_mask(fixture_mask, weights, ranks):
    selected = 0
    faces = [i for i in range(len(TRIANGLES)) if fixture_mask >> i & 1]
    for i in sorted(faces, key=lambda j: (-weights[faces.index(j)], j)):
        candidate = selected | 1 << i
        if ranks[candidate] == ranks[selected] + 1:
            selected = candidate
    return selected


def digest_masks(masks):
    digest = sha256()
    for mask in masks:
        digest.update(mask.to_bytes(4, 'little'))
    return digest.hexdigest()


def main():
    count = 1 << len(TRIANGLES)
    supports = array('H', [0]) * count
    for mask in range(1, count):
        bit = mask & -mask
        supports[mask] = supports[mask ^ bit] | TRIANGLE_EDGE_MASKS[bit.bit_length() - 1]

    admitted = bytearray(count)
    ranks2 = bytearray(count)
    ranks3 = bytearray(count)
    some_sequence_clears = bytearray(count)
    every_maximal_clears = bytearray(count)
    some_sequence_clears[0] = 1
    every_maximal_clears[0] = 1
    admitted_masks = []
    circuits = []
    rank_disagreements = some_peeling_disagreements = all_peeling_disagreements = 0
    peeling_order_disagreements = 0

    for mask, support in enumerate(supports):
        # For six vertices, constraints at sizes 3 and 4 are automatic; at
        # size 5 only K5 fails, and at size 6 the bound is twelve edges.
        sparse = (support.bit_count() <= 12
                  and all(support & k5 != k5 for k5 in K5_EDGE_MASKS))
        if not sparse:
            continue
        admitted[mask] = 1
        admitted_masks.append(mask)
        r2 = rank_mod(mask, 2)
        r3 = rank_mod(mask, 3)
        ranks2[mask], ranks3[mask] = r2, r3
        rank_disagreements += r2 != r3

        if mask:
            free = free_triangle_mask(mask)
            some_sequence_clears[mask] = bool(free) and any(
                some_sequence_clears[mask ^ (1 << i)]
                for i in range(len(TRIANGLES)) if free >> i & 1
            )
            every_maximal_clears[mask] = bool(free) and all(
                every_maximal_clears[mask ^ (1 << i)]
                for i in range(len(TRIANGLES)) if free >> i & 1
            )
        independent = r2 == mask.bit_count()
        some_peeling_disagreements += independent != bool(some_sequence_clears[mask])
        all_peeling_disagreements += independent != bool(every_maximal_clears[mask])
        peeling_order_disagreements += (some_sequence_clears[mask]
                                        != every_maximal_clears[mask])

        if not independent and all(
                ranks2[mask ^ (1 << i)] == mask.bit_count() - 1
                for i in range(len(TRIANGLES)) if mask >> i & 1):
            circuits.append(mask)

    require(len(admitted_masks) == 74558, 'unexpected admitted-system count')
    require(rank_disagreements == 0, 'F2/F3 rank disagreement under (H)')
    require(some_peeling_disagreements == 0, 'rank/some-sequence peeling disagreement')
    require(all_peeling_disagreements == 0, 'rank/all-orders peeling disagreement')
    require(peeling_order_disagreements == 0, 'peeling success depends on order')
    for mask in circuits:
        require(ranks3[mask] == mask.bit_count() - 1,
                'minimal F2 dependence is not an F3 circuit')
        require(all(ranks3[mask ^ (1 << i)] == mask.bit_count() - 1
                    for i in range(len(TRIANGLES)) if mask >> i & 1),
                'circuit minimality differs over F3')
        is_sphere_circuit(mask)

    # Named smallest and overlapping adversaries.
    tetra = tuple(combinations(range(4), 3))
    bipyramid = ((0, 1, 3), (0, 2, 3), (1, 2, 3),
                 (0, 1, 4), (0, 2, 4), (1, 2, 4))
    shared = tuple(sorted(set(tetra) | set(combinations((0, 1, 2, 4), 3))))
    octahedron = tuple(tuple(sorted(t)) for t in product((0, 1), (2, 3), (4, 5)))
    fixtures = {
        'single_triangle': ((0, 1, 2),),
        'tetrahedron': tetra,
        'triangular_bipyramid': bipyramid,
        'two_tetrahedra_shared_face': shared,
        'octahedron': octahedron,
    }
    fixture_masks = {name: triangle_mask(faces) for name, faces in fixtures.items()}
    require(ranks2[fixture_masks['single_triangle']] == 1,
            'single triangle should be independent')
    require(fixture_masks['tetrahedron'] in circuits,
            'tetrahedral boundary should be the smallest sphere circuit')
    require(min(mask.bit_count() for mask in circuits) == 4,
            'a circuit smaller than the tetrahedral sphere was found')

    matching_assignments = matching_valid = matching_acyclic = 0
    attainable_by_fixture = {}
    for name, fixture_mask in fixture_masks.items():
        attained, assignments, valid, acyclic = top_matching_masks(fixture_mask)
        independent_subsets = {
            submask for submask in range(count)
            if submask & ~fixture_mask == 0
            and ranks2[submask] == submask.bit_count()
        }
        require(attained == independent_subsets,
                f'top Morse matching sets differ from independent sets: {name}')
        attainable_by_fixture[name] = attained
        matching_assignments += assignments
        matching_valid += valid
        matching_acyclic += acyclic

    weighted_cases = 0
    for name, fixture_mask in fixture_masks.items():
        faces = [i for i in range(len(TRIANGLES)) if fixture_mask >> i & 1]
        independent_subsets = attainable_by_fixture[name]
        for weights in product(range(3), repeat=len(faces)):
            greedy = greedy_mask(fixture_mask, weights, ranks2)
            greedy_value = sum(weights[j] for j, i in enumerate(faces) if greedy >> i & 1)
            optimum = max(sum(weights[j] for j, i in enumerate(faces) if subset >> i & 1)
                          for subset in independent_subsets)
            require(greedy_value == optimum,
                    f'weighted greedy failure for {name}, weights={weights}')
            # Since exactly the independent sets occur as matched triangle
            # sets, this also checks the minimum critical-triangle cost.
            require(sum(weights) - greedy_value ==
                    min(sum(weights[j] for j, i in enumerate(faces) if not subset >> i & 1)
                        for subset in independent_subsets),
                    f'critical-triangle optimum failure for {name}')
            weighted_cases += 1

    # Smallest standard characteristic and hypothesis adversary: RP2.
    projective_plane = ((0, 1, 2), (0, 1, 3), (0, 2, 4), (0, 3, 5),
                        (0, 4, 5), (1, 2, 5), (1, 3, 4), (1, 4, 5),
                        (2, 3, 4), (2, 3, 5))
    projective_mask = triangle_mask(projective_plane)
    require(supports[projective_mask] == (1 << len(EDGES)) - 1,
            'RP2 fixture should have complete six-vertex graph')
    require(not general_sparse(6, EDGES), 'RP2 support unexpectedly satisfies (H)')
    require(general_sparse(7, EDGES) is False,
            'isolated vertex must not repair hereditary sparsity')
    require(len(EDGES) == 3 * 7 - 6,
            'isolated-vertex control should pass only the global count')
    require(rank_mod(projective_mask, 2) == 9 and rank_mod(projective_mask, 3) == 10,
            'RP2 should expose characteristic dependence outside (H)')
    require(free_triangle_mask(projective_mask) == 0,
            'RP2 should be a nonpeelable rationally acyclic core')

    circuit_sizes = Counter(mask.bit_count() for mask in circuits)
    output = {
        'vertices': 6,
        'triangle_systems': count,
        'admitted_triangle_systems': len(admitted_masks),
        'admitted_masks_sha256': digest_masks(admitted_masks),
        'rank_disagreements_F2_F3': rank_disagreements,
        'rank_vs_some_peeling_disagreements': some_peeling_disagreements,
        'rank_vs_every_maximal_peeling_disagreements': all_peeling_disagreements,
        'some_vs_every_peeling_disagreements': peeling_order_disagreements,
        'sphere_circuits': len(circuits),
        'sphere_circuit_sizes': {str(size): number
                                 for size, number in sorted(circuit_sizes.items())},
        'sphere_circuit_masks_sha256': digest_masks(circuits),
        'morse_fixtures': len(fixtures),
        'morse_assignments': matching_assignments,
        'valid_top_matchings': matching_valid,
        'acyclic_top_matchings': matching_acyclic,
        'weighted_objectives': weighted_cases,
        'negative_control': {
            'name': 'six-vertex RP2 plus isolated vertex',
            'rank_F2': rank_mod(projective_mask, 2),
            'rank_F3': rank_mod(projective_mask, 3),
            'free_triangles': free_triangle_mask(projective_mask).bit_count(),
            'global_edge_count_passes': True,
            'hereditary_bound_passes': False,
        },
    }
    expected_path = Path(__file__).with_name('expected.json')
    if expected_path.exists():
        require(output == json.loads(expected_path.read_text()),
                'output differs from expected.json')
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

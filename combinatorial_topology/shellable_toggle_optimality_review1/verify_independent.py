#!/usr/bin/env python3
"""Independent exact audit of the shelling-to-toggle theorem (stdlib only)."""

from collections import Counter, deque
from hashlib import sha256
from heapq import heappop, heappush
from itertools import combinations
import json


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def powerset(vertices):
    vertices = tuple(sorted(vertices))
    return {
        frozenset(choice)
        for size in range(len(vertices) + 1)
        for choice in combinations(vertices, size)
    }


def complex_faces(facets):
    answer = set()
    for facet in facets:
        answer |= powerset(facet)
    return answer


def upper_mobius(faces):
    """Compute mu(H,new_top) from its defining recurrence."""
    answer = {}
    for face in sorted(faces, key=lambda x: (-len(x), tuple(x))):
        answer[face] = -1 - sum(value for larger, value in answer.items()
                                 if face < larger)
    return answer


def restriction_face(facet, old_faces):
    new_faces = powerset(facet) - old_faces
    if not new_faces:
        return None
    restriction = set(facet)
    for face in new_faces:
        restriction &= face
    restriction = frozenset(restriction)
    interval = {face for face in powerset(facet) if restriction <= face}
    return restriction if interval == new_faces else None


def find_shelling(facets):
    """Subset DP; returns one shelling or None, with no theorem formulas used."""
    facets = tuple(sorted(facets, key=lambda x: (len(x), tuple(x))))
    full = (1 << len(facets)) - 1
    parent = {0: None}
    queue = deque([0])
    transition_count = 0
    while queue:
        state = queue.popleft()
        old = complex_faces([facets[i] for i in range(len(facets)) if state >> i & 1])
        for i, facet in enumerate(facets):
            if state >> i & 1:
                continue
            restriction = restriction_face(facet, old)
            if restriction is None:
                continue
            transition_count += 1
            nxt = state | (1 << i)
            if nxt not in parent:
                parent[nxt] = (state, i, restriction)
                queue.append(nxt)
    if full not in parent:
        return None, transition_count
    reverse_order = []
    state = full
    while state:
        previous, i, restriction = parent[state]
        reverse_order.append((facets[i], restriction))
        state = previous
    return tuple(reversed(reverse_order)), transition_count


def clear_union(generators):
    """Literal-set version of the recursive union-clearing word."""
    generators = tuple(generators)
    if not generators:
        return ()
    last = generators[-1]
    earlier = generators[:-1]
    inner = tuple(face & last for face in earlier)
    return clear_union(earlier) + tuple(reversed(clear_union(inner))) + (last,)


def compile_word(shelling):
    word = []
    for facet, restriction in shelling:
        generators = tuple(facet - {vertex} for vertex in sorted(restriction))
        word.extend(clear_union(generators))
        word.append(facet)
    return tuple(word)


def replay(faces, mobius, word):
    on = set()
    unsigned = Counter()
    signed = Counter()
    for step, face in enumerate(word):
        require(face in faces, f"nonface at step {step}")
        require(mobius[face] != 0, f"zero Mobius move at step {step}")
        ideal = powerset(face)
        lit = on & ideal
        require(not lit or lit == ideal, f"nonmonochromatic move at step {step}")
        sign = -1 if lit else 1
        signed[face] += sign
        unsigned[face] += 1
        on ^= ideal
    require(on == faces, "word did not reach the all-on state")
    return unsigned, signed


def audit_shelling(shelling):
    facets = tuple(facet for facet, _ in shelling)
    restrictions = tuple(restriction for _, restriction in shelling)
    q = len(facets[0])
    require(all(len(facet) == q for facet in facets), "purity premise failed")
    faces = complex_faces(facets)
    mobius = upper_mobius(faces)
    word = compile_word(shelling)
    unsigned, signed = replay(faces, mobius, word)

    dual_count = Counter()
    for facet, restriction in shelling:
        for face in powerset(facet):
            if facet - restriction <= face:
                dual_count[face] += 1
    for face in faces:
        expected = (-1) ** (q - len(face) + 1) * dual_count[face]
        require(mobius[face] == expected, "dual-interval Mobius formula failed")
        require(unsigned[face] == abs(mobius[face]), "facewise count failed")
        require(signed[face] == -mobius[face], "net multiplicity failed")
    h_at_two = sum(2 ** len(restriction) for restriction in restrictions)
    require(len(word) == h_at_two == sum(abs(x) for x in mobius.values()),
            "length identity failed")
    return {
        "facets": len(facets),
        "faces": len(faces),
        "moves": len(word),
        "zeros": sum(value == 0 for value in mobius.values()),
        "max_abs_mu": max(abs(value) for value in mobius.values()),
    }


def shortest_cost(facets, costs=None):
    faces = sorted(complex_faces(facets), key=lambda x: (len(x), tuple(x)))
    require(len(faces) <= 16, "state-space guard")
    index = {face: i for i, face in enumerate(faces)}
    mobius = upper_mobius(set(faces))
    moves = []
    for face in faces:
        if mobius[face] == 0:
            continue
        mask = sum(1 << index[subface] for subface in powerset(face))
        weight = 1 if costs is None else costs[face]
        moves.append((mask, weight))
    goal = (1 << len(faces)) - 1
    if costs is None:
        queue = deque([0])
        distance = {0: 0}
        while queue:
            state = queue.popleft()
            if state == goal:
                return distance[state]
            for mask, _ in moves:
                if state & mask in (0, mask):
                    nxt = state ^ mask
                    if nxt not in distance:
                        distance[nxt] = distance[state] + 1
                        queue.append(nxt)
    else:
        heap = [(0, 0)]
        distance = {0: 0}
        while heap:
            value, state = heappop(heap)
            if distance[state] != value:
                continue
            if state == goal:
                return value
            for mask, weight in moves:
                if state & mask in (0, mask):
                    nxt = state ^ mask
                    candidate = value + weight
                    if candidate < distance.get(nxt, 10 ** 30):
                        distance[nxt] = candidate
                        heappush(heap, (candidate, nxt))
    raise AssertionError("claimed shellable instance was unwinnable")


def enumerate_five_labels():
    labels = range(5)
    family_count = shellable_count = nonshellable_count = transitions = 0
    bfs_count = 0
    histograms = {"dimensions": Counter(), "moves": Counter(), "zeros": Counter()}
    canonical = []
    for q in range(1, 6):
        possible = tuple(frozenset(facet) for facet in combinations(labels, q))
        for mask in range(1, 1 << len(possible)):
            family_count += 1
            facets = tuple(possible[i] for i in range(len(possible)) if mask >> i & 1)
            shelling, local_transitions = find_shelling(facets)
            transitions += local_transitions
            if shelling is None:
                nonshellable_count += 1
                continue
            shellable_count += 1
            record = audit_shelling(shelling)
            histograms["dimensions"][q - 1] += 1
            histograms["moves"][record["moves"]] += 1
            histograms["zeros"][record["zeros"]] += 1
            canonical.append((q, mask, record["moves"], record["zeros"], record["max_abs_mu"]))
            if record["faces"] <= 12:
                require(shortest_cost(facets) == record["moves"], "independent BFS mismatch")
                bfs_count += 1
    payload = json.dumps(canonical, separators=(",", ":")).encode()
    return {
        "nonempty_uniform_families": family_count,
        "shellable_families": shellable_count,
        "nonshellable_families": nonshellable_count,
        "reachable_shelling_transitions": transitions,
        "independent_BFS_optima": bfs_count,
        "dimension_histogram": dict(sorted(histograms["dimensions"].items())),
        "move_histogram": dict(sorted(histograms["moves"].items())),
        "zero_histogram": dict(sorted(histograms["zeros"].items())),
        "canonical_sha256": sha256(payload).hexdigest(),
    }


def adversarial_cases():
    cases = {
        "one_vertex_simplex": [(0,)],
        "four_isolated_vertices": [(0,), (1,), (2,), (3,)],
        "triangle_boundary_last_restriction_is_facet": [(0, 1), (1, 2), (0, 2)],
        "two_triangles_shared_edge": [(0, 1, 2), (0, 1, 3)],
        "tetrahedron_boundary": [tuple(x) for x in combinations(range(4), 3)],
        "cone_over_four_cycle": [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1)],
    }
    result = {}
    for name, raw in cases.items():
        facets = tuple(frozenset(facet) for facet in raw)
        shelling, _ = find_shelling(facets)
        require(shelling is not None, f"fixture {name} unexpectedly nonshellable")
        result[name] = audit_shelling(shelling)

    # Smallest geometric failure modes for completeness premises.
    disjoint_edges = tuple(map(frozenset, [(0, 1), (2, 3)]))
    vertex_glued_triangles = tuple(map(frozenset, [(0, 1, 2), (0, 3, 4)]))
    require(find_shelling(disjoint_edges)[0] is None, "disconnected edge pair accepted")
    require(find_shelling(vertex_glued_triangles)[0] is None,
            "codimension-two triangle gluing accepted")

    nonpure = tuple(map(frozenset, [(0, 1, 2), (0, 1, 3), (0, 2, 3), (0, 4)]))
    order = tuple((facet, restriction_face(facet, complex_faces(nonpure[:i])))
                  for i, facet in enumerate(nonpure))
    require(all(restriction is not None for _, restriction in order),
            "nonpure interval control lost")
    naive = compile_word(order)
    mu = upper_mobius(complex_faces(nonpure))
    require(mu[frozenset({0})] == 0 and frozenset({0}) in naive,
            "purity cancellation control failed")
    try:
        replay(complex_faces(nonpure), mu, naive)
    except AssertionError as error:
        require("zero Mobius" in str(error), "wrong nonpure rejection")
    else:
        raise AssertionError("nonpure naive compiler unexpectedly legal")

    weighted = {}
    for name in ("four_isolated_vertices", "triangle_boundary_last_restriction_is_facet",
                 "two_triangles_shared_edge", "tetrahedron_boundary"):
        facets = tuple(frozenset(facet) for facet in cases[name])
        faces = complex_faces(facets)
        mu = upper_mobius(faces)
        costs = {face: (sum(face) + 3 * len(face) + 1) % 6 for face in faces}
        bound = sum(costs[face] * abs(mu[face]) for face in faces)
        require(shortest_cost(facets, costs) == bound, "weighted Dijkstra mismatch")
        weighted[name] = bound

    result["premise_rejections"] = {
        "disjoint_edges": True,
        "triangles_glued_only_at_vertex": True,
        "nonpure_zero_at_vertex_0": True,
    }
    result["weighted_Dijkstra_optima"] = weighted
    return result


def main():
    evidence = {
        "five_label_exhaustive": enumerate_five_labels(),
        "adversarial_cases": adversarial_cases(),
    }
    canonical = json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode()
    output = {
        "status": "VERIFIED",
        "evidence_sha256": sha256(canonical).hexdigest(),
        "evidence": evidence,
    }
    print(json.dumps(output, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()

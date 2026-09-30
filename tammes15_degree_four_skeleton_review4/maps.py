"""Independent undirected cellular-face census. No author modules imported."""
from collections import deque
from itertools import combinations, permutations
from pathlib import Path
import argparse
import hashlib
import json

N = 8
PAIRS = tuple(combinations(range(N), 2))
EDGE = {p: k for k, p in enumerate(PAIRS)}
DEGREES = (3, 3, 4, 4, 4, 4, 4, 4)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def degree_graphs():
    """Finish the vertex of largest remaining degree, with dynamic order.

    Every final graph determines exactly one choice at each deterministic
    vertex-selection step. No degree realization is quotiented here.
    """
    answer = set()
    rem = list(DEGREES)
    states = 0

    def visit(active, mask):
        nonlocal states
        states += 1
        if not active:
            need(not any(rem), 'all degree requirements met')
            need(mask not in answer, 'unique dynamically generated graph')
            answer.add(mask)
            return
        if sum(rem) % 2 or any(rem[v] < 0 or rem[v] >= len(active) for v in active):
            return
        v = min(active, key=lambda z: (-rem[z], z))
        others = tuple(z for z in active if z != v)
        cand = tuple(z for z in others if rem[z])
        k = rem[v]
        for chosen in combinations(cand, k):
            new = mask
            for w in chosen:
                rem[w] -= 1
                new |= 1 << EDGE[tuple(sorted((v, w)))]
            rem[v] = 0
            visit(others, new)
            rem[v] = k
            for w in chosen:
                rem[w] += 1

    visit(tuple(range(N)), 0)
    return answer, states


def orbit_partition(graphs):
    maps = []
    for first in ((0, 1), (1, 0)):
        for rest in permutations(range(2, N)):
            p = first + rest
            maps.append(tuple(EDGE[tuple(sorted((p[i], p[j])))] for i, j in PAIRS))
    need(len(maps) == 1440, 'entire degree-preserving group')
    pending = set(graphs)
    result = []
    while pending:
        root = min(pending)
        bits = tuple(k for k in range(len(PAIRS)) if root & (1 << k))
        orbit = {sum(1 << m[k] for k in bits) for m in maps}
        need(orbit <= pending, 'complete disjoint graph orbit')
        pending.difference_update(orbit)
        result.append((root, len(orbit)))
    need(sum(size for root, size in result) == len(graphs), 'whole graph orbit partition')
    return result


def adjacency(mask):
    result = [[] for _ in range(N)]
    for k, (i, j) in enumerate(PAIRS):
        if mask & (1 << k):
            result[i].append(j)
            result[j].append(i)
    need(tuple(map(len, result)) == DEGREES, 'exact graph degrees')
    return result


def cycle_key(seq):
    seq = tuple(seq)
    return min(s[k:] + s[:k] for s in (seq, tuple(reversed(seq))) for k in range(len(s)))


def cycles(adj):
    """Each simple UNORIENTED triangle/quadrilateral appears exactly once."""
    out = []
    for length in (3, 4):
        for vertices in combinations(range(len(adj)), length):
            for tail in permutations(vertices[1:]):
                if tail[0] > tail[-1]:
                    continue
                face = (vertices[0],) + tail
                if all(face[(i + 1) % length] in adj[face[i]] for i in range(length)):
                    out.append(face)
    need(len(out) == len(set(map(cycle_key, out))), 'unique unoriented candidate cycles')
    return out


def orient_faces(faces, adj):
    """Orient adjacent faces oppositely along every shared edge.

    A connected closed surface with these vertex links and Euler
    characteristic two must be a sphere; we additionally check orientation
    consistency explicitly and reconstruct the actual local rotations.
    """
    sides = {}
    for fi, f in enumerate(faces):
        for a, b in zip(f, f[1:] + f[:1]):
            sides.setdefault(tuple(sorted((a, b))), []).append((fi, int(a > b)))
    need(all(len(x) == 2 for x in sides.values()), 'every edge has two face sides')
    nb = [[] for _ in faces]
    for choices in sides.values():
        (i, a), (j, b) = choices
        need(i != j, 'distinct incident simple faces')
        flip = 1 ^ a ^ b
        nb[i].append((j, flip))
        nb[j].append((i, flip))
    signs = {0: 0}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j, flip in nb[i]:
            expected = signs[i] ^ flip
            if j in signs:
                need(signs[j] == expected, 'sphere orientation consistency')
            else:
                signs[j] = expected
                queue.append(j)
    need(len(signs) == len(faces), 'connected dual face complex')
    rotations = []
    for global_flip in (0, 1):
        predecessor = [dict() for _ in adj]
        for i, f in enumerate(faces):
            if signs[i] ^ global_flip:
                f = tuple(reversed(f))
            for k, v in enumerate(f):
                left, right = f[k - 1], f[(k + 1) % len(f)]
                need(left not in predecessor[v], 'unique oriented local predecessor')
                predecessor[v][left] = right
        rotation = []
        for v, neighbors in enumerate(adj):
            need(set(predecessor[v]) == set(neighbors), 'all local predecessors assigned')
            successor = {b: a for a, b in predecessor[v].items()}
            seq = [min(neighbors)]
            for k in range(len(neighbors) - 1):
                seq.append(successor[seq[-1]])
            need(len(set(seq)) == len(neighbors) and successor[seq[-1]] == seq[0], 'single local rotation')
            rotation.append(tuple(seq))
        rotations.append(tuple(rotation))
    need(rotations[0] != rotations[1], 'two distinct global orientations')
    return rotations


def cellular_covers(adj, nt=6, nq=3):
    """Unoriented edge double covers with cyclic manifold vertex links.

    Branch on the edge with fewest possible completions, selecting all its
    remaining incident faces at once. For each eventual cover this choice
    is unique. We never enumerate a product of local rotations or a
    partition of directed darts.
    """
    edges = tuple((i, j) for i in range(len(adj)) for j in adj[i] if i < j)
    edge_index = {e: k for k, e in enumerate(edges)}
    cs = cycles(adj)
    face_edges = [tuple(edge_index[tuple(sorted((a, b)))] for a, b in zip(f, f[1:] + f[:1])) for f in cs]
    corners = [tuple((v, f[k - 1], f[(k + 1) % len(f)]) for k, v in enumerate(f)) for f in cs]
    containing = [[k for k, es in enumerate(face_edges) if i in es] for i in range(len(edges))]
    counts = [0] * len(edges)
    links = [[0] * len(adj) for _ in adj]
    full = [sum(1 << j for j in ns) for ns in adj]
    chosen = set()
    covers = set()
    visits = 0

    def undo(k):
        for e in face_edges[k]:
            counts[e] -= 1
        for v, a, b in corners[k]:
            links[v][a] ^= 1 << b
            links[v][b] ^= 1 << a

    def put(k):
        if any(counts[e] == 2 for e in face_edges[k]):
            return False
        for v, a, b in corners[k]:
            if links[v][a] & (1 << b) or links[v][a].bit_count() == 2 or links[v][b].bit_count() == 2:
                return False
        for e in face_edges[k]:
            counts[e] += 1
        for v, a, b in corners[k]:
            links[v][a] |= 1 << b
            links[v][b] |= 1 << a
        for v, a, b in corners[k]:
            component = 0
            todo = 1 << a
            while todo:
                bit = todo & -todo
                todo -= bit
                w = bit.bit_length() - 1
                if component & bit:
                    continue
                component |= bit
                todo |= links[v][w] & ~component
            closed = all(links[v][w].bit_count() == 2 for w in range(len(adj)) if component & (1 << w))
            if closed and component != full[v]:
                undo(k)
                return False
        return True

    def visit(taken_t, taken_q):
        nonlocal visits
        visits += 1
        if taken_t > nt or taken_q > nq:
            return
        if all(x == 2 for x in counts):
            need((taken_t, taken_q) == (nt, nq), 'final face quotas')
            key = tuple(sorted(chosen))
            need(key not in covers, 'unique edge-completion cover traversal')
            covers.add(key)
            return
        if sum(2 - x for x in counts) != 3 * (nt - taken_t) + 4 * (nq - taken_q):
            return
        best = None
        for e, count in enumerate(counts):
            if count == 2:
                continue
            possible = [k for k in containing[e] if k not in chosen
                        and (taken_t < nt if len(cs[k]) == 3 else taken_q < nq)
                        and all(counts[x] < 2 for x in face_edges[k])]
            missing = 2 - count
            if len(possible) < missing:
                return
            score = len(possible) * (len(possible) - 1) // 2 if missing == 2 else len(possible)
            if best is None or score < best[0]:
                best = (score, possible, missing)
        for group in combinations(best[1], best[2]):
            added = []
            for k in group:
                if not put(k):
                    break
                chosen.add(k)
                added.append(k)
            if len(added) == len(group):
                visit(taken_t + sum(len(cs[k]) == 3 for k in added),
                      taken_q + sum(len(cs[k]) == 4 for k in added))
            for k in reversed(added):
                chosen.remove(k)
                undo(k)

    visit(0, 0)
    need(not chosen and not any(counts) and not any(any(r) for r in links), 'all reversible state restored')
    result = []
    for key in sorted(covers):
        fs = tuple(cs[k] for k in key)
        need(len(adj) - len(edges) + len(fs) == 2, 'closed surface Euler characteristic two')
        result.extend(orient_faces(fs, adj))
    need(len(result) == len(set(result)), 'unique complete oriented maps')
    return sorted(result), {'unoriented_cycle_candidates': len(cs), 'edge_cover_states': visits,
                            'unoriented_sphere_covers': len(covers)}


def small_controls():
    graphs = {
        'tetrahedron': ([[j for j in range(4) if j != i] for i in range(4)], 4, 0),
        'octahedron': ([[j for j in range(6) if j != i and j != (i ^ 1)] for i in range(6)], 8, 0),
        'triangular_prism': ([[1, 2, 3], [0, 2, 4], [0, 1, 5], [0, 4, 5], [1, 3, 5], [2, 3, 4]], 2, 3),
    }
    out = {}
    for name, (adj, nt, nq) in graphs.items():
        rotations, counts = cellular_covers(adj, nt, nq)
        need(len(rotations) == 2, 'two oriented polyhedral embeddings: ' + name)
        out[name] = counts
    return out


def run(reference):
    graphs, states = degree_graphs()
    need(len(graphs) == 15740, 'complete labelled degree graph count')
    reps = orbit_partition(graphs)
    expected_reps = [(x['mask'], x['orbit']) for x in reference['cover']['graph_representatives']]
    need(reps == expected_reps, 'all graph representatives and entire orbit sizes match')
    expected = {}
    for item in reference['cover']['spherical_rotation_entries']:
        expected.setdefault(item['graph_mask'], set()).add(tuple(map(tuple, item['rotation'])))
    result = []
    for mask, size in reps:
        rotations, counts = cellular_covers(adjacency(mask))
        need(set(rotations) == expected.get(mask, set()), 'all oriented map entries match for ' + str(mask))
        result.append({'graph_mask': mask, 'orbit_size': size, 'rotations': rotations, **counts})
    return {'agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'labelled_graphs': len(graphs), 'labelled_graph_sha256': digest(sorted(graphs)),
            'degree_generator_states': states, 'graph_orbits': len(reps), 'maps': result,
            'oriented_sphere_maps': sum(len(x['rotations']) for x in result),
            'all_oriented_entries_match_original': True, 'controls': small_controls()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('reference', type=Path)
    args = parser.parse_args()
    print(json.dumps(run(json.loads(args.reference.read_text())), indent=2, sort_keys=True))

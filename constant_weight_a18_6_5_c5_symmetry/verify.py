"""Independently reconstruct and check the specified C5 symmetry exclusion.

No search program, stored orbit database, solver, or triple-incidence encoding
is imported. The verifier uses point sets, direct word intersections, complete
four-clique enumeration, explicit group generators, and certificate inferences.
The analytic bridge requires the known theorem A(17,6,4) <= 20; see PROOF.md.
"""
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json

G = tuple((i // 5) * 5 + (i + 1) % 5 if i < 15 else i for i in range(18))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def image(word, permutation):
    return tuple(sorted(permutation[p] for p in word))


def reconstruct():
    unseen = set(combinations(range(18), 5))
    all_orbits = []
    while unseen:
        start = min(unseen)
        orbit = {start}
        word = image(start, G)
        while word != start:
            require(word not in orbit, 'orbit failed to return to start')
            orbit.add(word)
            word = image(word, G)
        require(orbit <= unseen, 'overlapping enumerated orbits')
        unseen -= orbit
        all_orbits.append(tuple(sorted(orbit)))
    require(Counter(map(len, all_orbits)) == {1: 3, 5: 1713}, 'raw orbit census')
    admissible = []
    for orbit in all_orbits:
        if len(orbit) == 5 and all(len(set(a) & set(b)) <= 2
                                 for a, b in combinations(orbit, 2)):
            admissible.append(orbit)
    admissible.sort()
    require(len(admissible) == 1125, 'admissible full-orbit census')
    return admissible


def compatible(a, b):
    return all(len(x & y) <= 2 for x in a for y in b)


def adjacency(orbits):
    result = [set() for _ in orbits]
    for i, j in combinations(range(len(orbits)), 2):
        if compatible(orbits[i], orbits[j]):
            result[i].add(j)
            result[j].add(i)
    return result


def links4(adj):
    """Enumerate by the uniquely determined first two vertices of each K4."""
    links = set()
    for a in range(len(adj)):
        for b in sorted(v for v in adj[a] if v > a):
            common = {v for v in adj[a] & adj[b] if v > b}
            for c in sorted(common):
                for d in common & adj[c]:
                    if d > c:
                        links.add((a, b, c, d))
    return links


def generators():
    result = []
    for start in (0, 5, 10):
        p = list(range(18))
        for j in range(5):
            p[start + j] = start + (j + 1) % 5
        result.append(tuple(p))
    for start in (0, 5):
        p = list(range(18))
        for j in range(5):
            p[start + j], p[start + 5 + j] = start + 5 + j, start + j
        result.append(tuple(p))
    p = list(range(18))
    for start in (0, 5, 10):
        for j in range(5):
            p[start + j] = start + 2 * j % 5
    result.append(tuple(p))
    p = list(range(18))
    p[15], p[16] = 16, 15
    result.append(tuple(p))
    return result


def normalization(full, links, representative):
    index = {orbit: i for i, orbit in enumerate(full)}
    g2 = tuple(G[G[i]] for i in range(18))
    actions = []
    for p in generators():
        require(sorted(p) == list(range(18)) and p[17] == 17, 'bad generator')
        inv = tuple(p.index(i) for i in range(18))
        conjugate = tuple(p[G[inv[i]]] for i in range(18))
        require(conjugate in (G, g2), 'generator does not normalize C5')
        actions.append([index[tuple(sorted(image(w, p) for w in orbit))]
                        for orbit in full])
    visited = {representative}
    queue = deque([representative])
    while queue:
        link = queue.popleft()
        for action in actions:
            other = tuple(sorted(action[i] for i in link))
            require(other in links, 'normalizer image missing from link enumeration')
            if other not in visited:
                visited.add(other)
                queue.append(other)
    require(visited == links, 'not all links are equivalent to the representative')
    return len(visited)


def check_tree(tree, candidates, need, adj):
    """Check a multiway clique split, followed by a proper-color bound.

    Children include a chosen vertex; the verifier computes their candidate
    sets. After each child that vertex is removed. Remaining candidates lie
    in fewer than `need` independently checked color classes.
    """
    require(need > 0, 'certificate reached a target clique')
    if tree == {'small': True}:
        require(len(candidates) < need, 'invalid cardinality leaf')
        return 1
    require(isinstance(tree, dict) and set(tree) == {'colors', 'children'},
            'invalid certificate node')
    colors = tree['colors']
    require(isinstance(colors, list) and all(isinstance(c, list) and c for c in colors),
            'invalid color classes')
    flattened = [v for cls in colors for v in cls]
    require(all(type(v) is int for v in flattened), 'noninteger vertex')
    require(len(flattened) == len(set(flattened)) and set(flattened) == candidates,
            'colors do not partition all candidates')
    for cls in colors:
        require(all(b not in adj[a] for a, b in combinations(cls, 2)),
                'color class contains an edge')
    branch_vertices = [v for cls in reversed(colors[need - 1:]) for v in reversed(cls)]
    require(len(tree['children']) == len(branch_vertices), 'missing or extra branch')
    p = set(candidates)
    nodes = 1
    for v, child in zip(branch_vertices, tree['children']):
        nodes += check_tree(child, p & adj[v], need - 1, adj)
        p.remove(v)
    require(p <= set(v for cls in colors[:need - 1] for v in cls),
            'uncovered residual branch')
    return nodes


def read_witness(path):
    rows = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    require(len(rows) == 68, 'lower-bound witness must have 68 words')
    require(all(len(r) == 18 and set(r) <= {'0', '1'} for r in rows), 'invalid binary word')
    words = [tuple(i for i, bit in enumerate(r) if bit == '1') for r in rows]
    require(all(len(w) == 5 for w in words) and len(set(words)) == 68, 'witness weight/distinctness')
    require(all(len(set(a) & set(b)) <= 2 for a, b in combinations(words, 2)), 'invalid packing')
    require({image(w, G) for w in words} == set(words), 'witness lacks specified symmetry')
    return words


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    folder = Path(__file__).resolve().parent
    path = args.certificate or folder / 'certificate.json'
    raw = path.read_bytes()
    certificate = json.loads(raw)
    require(set(certificate) == {'format', 'representative', 'residual', 'target', 'tree'}
            and certificate['format'] == 'c5-multiway-color-v1', 'unknown certificate format')
    require(type(certificate['target']) is int and certificate['target'] == 10, 'wrong target')
    full = reconstruct()
    point_sets = [tuple(map(frozenset, orbit)) for orbit in full]
    ids = [i for i, orbit in enumerate(full) if 17 in orbit[0]]
    require(len(ids) == 230, 'through-point17 orbit census')
    local_links = links4(adjacency([point_sets[i] for i in ids]))
    links = {tuple(ids[i] for i in choice) for choice in local_links}
    require(len(links) == 100, '20-word link census')
    profiles = Counter()
    for link in links:
        words = [w for i in link for w in full[i]]
        require(len(set(words)) == 20, 'link duplicate')
        require(all(len(set(a) & set(b)) <= 2 for a, b in combinations(words, 2)), 'bad link')
        profile = tuple(sorted(sum(p in w for w in words) for p in range(17)))
        profiles[profile] += 1
    require(profiles == {(0,) + (5,) * 16: 100}, 'link degree profiles')
    representative = tuple(certificate['representative'])
    require(all(type(i) is int for i in representative) and representative == min(links),
            'wrong representative')
    normalized = normalization(full, links, representative)
    core = tuple(w for i in representative for w in point_sets[i])
    residual = [i for i, orbit in enumerate(point_sets) if compatible(core, orbit)]
    require(residual == certificate['residual'] and len(residual) == 159, 'incomplete residual universe')
    require(all(17 not in w for i in residual for w in full[i]), 'residual hits saturated point')
    adj = adjacency([point_sets[i] for i in residual])
    nodes = check_tree(certificate['tree'], set(range(len(residual))), 10, adj)
    witness = read_witness(folder / 'witness68.txt')
    orbit_raw = json.dumps(full, separators=(',', ':')).encode() + b'\n'
    link_raw = json.dumps(sorted(links), separators=(',', ':')).encode() + b'\n'
    result = {'agent': 'six-code-2', 'role': 'researcher', 'cycle_type': '5^3 1^3',
              'raw_orbits': {'1': 3, '5': 1713}, 'admissible_full_orbits': len(full),
              'through_point17_orbits': len(ids), 'degree20_links': len(links),
              'normalizer_orbit_size': normalized, 'representative': list(representative),
              'residual_orbits': len(residual), 'residual_edges': sum(map(len, adj)) // 2,
              'no10_certificate_nodes': nodes, 'witness_words': len(witness),
              'restricted_maximum': 68, 'global_bounds_changed': False,
              'full_orbits_sha256': sha256(orbit_raw).hexdigest(),
              'links_sha256': sha256(link_raw).hexdigest(),
              'certificate_sha256': sha256(raw).hexdigest(),
              'external_theorem': 'A(17,6,4) <= 20 (Brouwer, 1975)',
              'proof_status': 'exact finite certificate plus ordinary analytic coverage proof; not formalized'}
    if args.expect:
        require(result == json.loads(args.expect.read_text()), 'expected output mismatch')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

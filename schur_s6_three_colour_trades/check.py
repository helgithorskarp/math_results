"""Exact verification of small additive obstructions; no solver dependency."""
from collections import deque
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def violations(colours):
    """Directly check every integer triple, including repeated summands."""
    c = [0] + list(colours)
    return [[x, z-x, z, c[z]]
            for z in range(2, len(c)) for x in range(1, z//2+1)
            if c[x] == c[z-x] == c[z]]


def colourable(vertices, k, root):
    """Return (model or None, node count, edge count) by exhaustive search.

    The only symmetry reduction fixes the supplied root to colour 0.
    Singleton propagation deletes a colour only when all other distinct
    vertices of a Schur triple are already forced to that colour.
    """
    require(type(k) is int and k >= 1, 'invalid colour count')
    require(all(type(v) is int and v > 0 for v in vertices), 'invalid vertices')
    require(vertices == sorted(set(vertices)), 'vertices must be sorted and unique')
    require(root in vertices if vertices else root is None, 'root outside set')
    index = {v: i for i, v in enumerate(vertices)}
    edges = sorted({tuple(sorted({index[x], index[y], index[x+y]}))
                    for x, y in combinations_with_replacement(vertices, 2)
                    if x+y in index})
    incident = [[] for _ in vertices]
    for edge in edges:
        for v in edge:
            incident[v].append(tuple(w for w in edge if w != v))
    degree = list(map(len, incident))
    nodes = 0

    def singleton(mask):
        return mask != 0 and mask & (mask-1) == 0

    def search(domains, queue):
        nonlocal nodes
        nodes += 1
        while queue:
            v = queue.popleft()
            colour = domains[v]
            require(singleton(colour), 'queued domain is not a singleton')
            for others in incident[v]:
                if len(others) == 1:  # x+x=z has only two distinct vertices
                    targets = others
                else:
                    a, b = others
                    targets = []
                    if domains[a] == colour:
                        targets.append(b)
                    if domains[b] == colour:
                        targets.append(a)
                for w in targets:
                    if not domains[w] & colour:
                        continue
                    domains[w] &= ~colour
                    if domains[w] == 0:
                        return None
                    if singleton(domains[w]):
                        queue.append(w)
        choices = [v for v, mask in enumerate(domains) if not singleton(mask)]
        if not choices:
            require(all(len({domains[v] for v in edge}) > 1 for edge in edges),
                    'invalid terminal model')
            return [mask.bit_length()-1 for mask in domains]
        v = min(choices, key=lambda w: (domains[w].bit_count(), -degree[w], w))
        colours = domains[v]
        while colours:
            colour = colours & -colours
            colours -= colour
            branch = domains.copy()
            branch[v] = colour
            answer = search(branch, deque([v]))
            if answer is not None:
                return answer
        return None

    domains = [(1 << k)-1 for _ in vertices]
    if vertices:
        domains[index[root]] = 1
    answer = search(domains, deque(v for v, d in enumerate(domains) if singleton(d)))
    return answer, nodes, len(edges)


def verify(fixtures, certificate):
    require(set(fixtures) == {'baseline', 'near537', 'team_near_190',
                              'team_near_359'}, 'fixture coverage')
    require(certificate.get('format') == 1, 'unsupported certificate format')
    fixture_checks = {}
    palettes = {}
    colourings = {}
    for name, fixture in fixtures.items():
        text = fixture['colours']
        require(type(text) is str and set(text) <= set('123456'), 'invalid colours')
        n = 536 if name == 'baseline' else 537
        require(len(text) == n, 'wrong colouring length')
        require(sha256((text+'\n').encode()).hexdigest() == fixture['sha256'],
                'fixture hash mismatch')
        c = list(map(int, text))
        bad = violations(c)
        require(bad == fixture['expected_violations'], 'wrong fixture violations')
        if name == 'baseline':
            require(not bad, 'baseline is not sum-free')
            palettes[name] = set(combinations(range(1, 7), 3))
        else:
            bad_colours = {row[3] for row in bad}
            require(len(bad_colours) == 1, 'expected exactly one defective colour')
            palettes[name] = {p for p in combinations(range(1, 7), 3)
                              if bad_colours <= set(p)}
        colourings[name] = [0]+c
        fixture_checks[name] = {'n': n, 'violations': bad, 'sha256': fixture['sha256']}
    seen = set()
    results = []
    for row in certificate['cases']:
        name = row['input']
        require(name in fixtures, 'unknown fixture')
        palette = tuple(row['palette'])
        require(palette in palettes[name], 'unexpected palette')
        key = (name, palette)
        require(key not in seen, 'duplicate palette')
        seen.add(key)
        c = colourings[name]
        allowed = {v for v in range(1, len(c)) if c[v] in palette}
        if name == 'baseline':
            allowed.add(537)
        vertices = row['vertices']
        require(set(vertices) <= allowed, 'obstruction outside palette union')
        answer, nodes, edges = colourable(vertices, 3, row['root'])
        require(answer is None, 'claimed obstruction is three-colourable')
        results.append({'input': name, 'palette': list(palette),
                        'vertices': len(vertices), 'edges': edges, 'nodes': nodes})
    expected = {(name, p) for name, ps in palettes.items() for p in ps}
    require(seen == expected, 'missing palette cases')
    return {'fixtures': fixture_checks, 'cases': results,
            'total_cases': len(results), 'total_nodes': sum(x['nodes'] for x in results),
            'max_vertices': max(x['vertices'] for x in results)}


def main():
    directory = Path(__file__).resolve().parent
    fixtures = json.loads((directory/'fixtures.json').read_text())
    certificate = json.loads((directory/'certificate.json').read_text())
    result = verify(fixtures, certificate)
    expected = json.loads((directory/'expected.json').read_text())
    require(result == expected, 'result differs from expected.json')
    print('PASS fixtures={} palettes={} nodes={} max_vertices={}'.format(
        len(fixtures), result['total_cases'], result['total_nodes'], result['max_vertices']))
    print('certificate_sha256='+sha256((directory/'certificate.json').read_bytes()).hexdigest())


if __name__ == '__main__':
    main()

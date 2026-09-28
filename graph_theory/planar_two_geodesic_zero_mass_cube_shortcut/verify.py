"""Exact solver-free continuum certificate audit; Python 3.11+.

This verifier uses explicit oriented cube faces, Floyd--Warshall,
affine endpoint comparisons, ordinary set components, and RUP replay.
It imports no discovery code or external package.
"""
from itertools import combinations
from pathlib import Path
import hashlib, json, time

HERE = Path(__file__).resolve().parent

def fixture():
    faces=[[0,4,6,2],[1,3,7,5],[0,1,5,4],[2,6,7,3],[0,2,3,1],[4,5,7,6]]
    cube=sorted({tuple(sorted((a,b))) for face in faces for a,b in zip(face,face[1:]+face[:1])})
    labels={e:14+i for i,e in enumerate(cube)};triangles=[];core=set();edges=set()
    for i,face in enumerate(faces):
        f=8+i
        for a,b in zip(face,face[1:]+face[:1]):
            z=labels[tuple(sorted((a,b)))];triangles.extend([(a,z,f),(z,b,f)])
            core.add((a,f))
    darts=set()
    for face in triangles:
        for a,b in zip(face,face[1:]+face[:1]):
            assert (a,b) not in darts;darts.add((a,b));edges.add(tuple(sorted((a,b))))
    assert all((b,a) in darts for a,b in darts)
    adj={v:set() for v in range(26)}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    # One link cycle at each vertex, with a connected one-skeleton and
    # Euler characteristic two, certifies the supplied spherical embedding.
    for v in adj:
        rotation={}
        for face in triangles:
            if v in face:
                i=face.index(v);a,b=face[(i+1)%3],face[(i+2)%3]
                assert a not in rotation;rotation[a]=b
        assert set(rotation)==adj[v] and set(rotation.values())==adj[v]
        first=min(rotation);u=first;visited=set()
        while u not in visited:visited.add(u);u=rotation[u]
        assert u==first and visited==adj[v]
    assert len(components(adj,set()))==1
    assert len(core)==24 and len(edges)==72 and len(triangles)==48 and 26-72+48==2
    return adj,sorted(edges),sorted(core),triangles


def components(adj,removed):
    unseen=set(adj)-removed;out=[]
    while unseen:
        K={unseen.pop()};todo=list(K)
        while todo:
            v=todo.pop();new=adj[v]&unseen;unseen-=new;K|=new;todo.extend(new)
        out.append(K)
    return out


ADJ, EDGES, CORE, FACES = fixture()
MARKS = set(range(15, 26))

def floyd(n, costs):
    infinity = sum(costs.values()) + 1
    d = [[0 if a == b else infinity for b in range(n)] for a in range(n)]
    for (a, b), w in costs.items():
        assert w > 0
        d[a][b] = d[b][a] = w
    for k in range(n):
        for a in range(n):
            for b in range(n):
                d[a][b] = min(d[a][b], d[a][k] + d[k][b])
    return d


def mass_blocks(pair):
    assert len(pair) == 2
    return [K & MARKS for K in components(ADJ, set(pair[0]) | set(pair[1]))]


def mass_rule(certificate, check_path):
    large = []
    for pair in certificate['pairs']:
        for path in pair:
            check_path(path)
        blocks = [K for K in mass_blocks(pair) if len(K) > 4]
        large.append(blocks)
    if certificate['kind'] == 'four-residue':
        assert len(large) == 1 and large == [[]]
    else:
        assert certificate['kind'] == 'disjoint-exceptional-blocks'
        assert len(large) == 2 and all(len(row) == 1 for row in large)
        assert not large[0][0] & large[1][0]
        assert [sum(1 << v for v in row[0]) for row in large] == certificate['exceptional_blocks']


def affine_checker(prices, ends, lo, hi, parents):
    d = floyd(14, prices)
    def check(path):
        assert path and len(path) == len(set(path)) and 14 not in [path[0], path[-1]]
        assert all(v in ADJ for v in path)
        middle = list(path)
        if middle[0] in MARKS:
            assert len(middle) > 1 and parents[middle[0]] == middle[1]
            middle.pop(0)
        if middle[-1] in MARKS:
            assert len(middle) > 1 and parents[middle[-1]] == middle[-2]
            middle.pop()
        assert all(v < 15 for v in middle) and middle[0] < 14 and middle[-1] < 14
        constant, slope = 0, 0
        if 14 in middle:
            i = middle.index(14)
            assert {middle[i - 1], middle[i + 1]} == set(ends)
            slope = 1
        for a, b in zip(middle, middle[1:]):
            if 14 not in (a, b):
                constant += prices[tuple(sorted((a, b)))]
        a, b = middle[0], middle[-1]
        u, v = ends
        for intercept, coefficient in [(d[a][b], 0), (d[a][u] + d[v][b], 1), (d[a][v] + d[u][b], 1)]:
            assert constant - intercept + (slope - coefficient) * lo <= 0
            if hi is None:
                assert slope <= coefficient
            else:
                assert constant - intercept + (slope - coefficient) * hi <= 0
    return check


def rup(clauses, proof):
    working = [set(c) for c in clauses]
    additions = 0
    for line in proof:
        if line.startswith('d '):
            continue
        literals = list(map(int, line.split()))
        assert literals[-1] == 0
        clause = set(literals[:-1])
        true = {-v for v in clause}
        conflict = any(-v in true for v in true)
        while not conflict:
            progress = False
            for c in working:
                if c & true:
                    continue
                remaining = {v for v in c if -v not in true}
                if not remaining:
                    conflict = True
                    break
                if len(remaining) == 1:
                    true.update(remaining)
                    progress = True
            if not progress:
                break
        assert conflict, ('non-RUP clause', line)
        working.append(clause)
        additions += 1
    assert working[-1] == set()
    return additions


def verify(data):
    assert data['schema'] == 'radial-cube-zero-mass-shortcut-v1'
    assert data['vertices'] == 26 and data['shortcut_vertex'] == 14
    assert data['mass_support'] == sorted(MARKS)
    expected_prices = {
        'A': [14,38,7,23,20,17,8,30,11,21,14,29,10,28,36,4,3,7,30,6,2,4,9,5],
        'B': [7,10,4,8,7,11,9,6,16,14,3,23,3,16,15,16,3,10,22,9,12,3,12,7],
    }
    assert len(data['rows']) == 4
    assert {(r['metric'], tuple(r['opposite_pair'])) for r in data['rows']} == {
        (name, pair) for name in expected_prices for pair in [(0, 1), (10, 12)]}
    ids = {(z, p): 1 + 4 * (z - 15) + j for z in sorted(MARKS) for j, p in enumerate(sorted(ADJ[z]))}
    base = []
    for z in sorted(MARKS):
        group = [ids[z, p] for p in sorted(ADJ[z])]
        base.append(group)
        base.extend([-a, -b] for a, b in combinations(group, 2))
    result = {'sweeps': 4, 'cells': 0, 'templates': 0, 'four_residue': 0,
              'adaptive': 0, 'rup_additions': 0}
    for row in data['rows']:
        prices = {(a, b): w for a, b, w in row['original_prices']}
        assert sorted(prices) == CORE
        assert [prices[e] for e in CORE] == expected_prices[row['metric']]
        d = floyd(14, prices)
        u, v = row['opposite_pair']
        breaks = {0}
        for a in range(14):
            for b in range(14):
                difference = d[a][b] - min(d[a][u] + d[v][b], d[a][v] + d[u][b])
                if difference > 0:
                    breaks.add(difference)
        points = sorted(breaks)
        assert [(c['lower'], c['upper']) for c in row['cells']] == list(zip(points, points[1:] + [None]))
        for cell in row['cells']:
            result['cells'] += 1
            clauses = list(base)
            assert cell['templates']
            for template in cell['templates']:
                conditions = template['conditions']
                assert len(dict(conditions)) == len(conditions)
                assert all(z in MARKS and p in ADJ[z] for z, p in conditions)
                check = affine_checker(prices, (u, v), cell['lower'], cell['upper'], dict(conditions))
                mass_rule(template, check)
                clauses.append([-ids[z, p] for z, p in conditions])
                result['templates'] += 1
                result['four_residue' if template['kind'] == 'four-residue' else 'adaptive'] += 1
            result['rup_additions'] += rup(clauses, cell['rup_proof'])
    assert result['cells'] == 40
    return result


if __name__ == '__main__':
    start = time.monotonic()
    source = HERE / 'certificate.json'
    result = verify(json.loads(source.read_text()))
    result.update({'status': 'PASS', 'certificate_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                   'seconds': round(time.monotonic() - start, 3)})
    print(json.dumps(result, sort_keys=True))

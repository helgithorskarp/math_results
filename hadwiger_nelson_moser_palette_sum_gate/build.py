"""One exact point-sum of two established physical relation sources."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

RAD = tuple(math.prod(p for j, p in enumerate((3, 5, 7, 11)) if i >> j & 1)
            for i in range(16))
D = 24


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def norm(row):
    answer = [0] * 16
    for offset in (0, 16):
        terms = [(RAD[j], v) for j, v in enumerate(row[offset:offset+16]) if v]
        for r, x in terms:
            for s, y in terms:
                g = math.gcd(r, s)
                answer[RAD.index(r*s//(g*g))] += x*y*g
    return tuple(answer)


def edges(points):
    target = (D*D,) + (0,)*15
    return [(i, j) for i, j in itertools.combinations(range(len(points)), 2)
            if norm(tuple(x-y for x, y in zip(points[i], points[j]))) == target]


def construct(inp):
    m = []
    for a, b, c, d in inp['moser_rows']:
        r = [0]*32
        for offset, rad, value in ((0, 1, a), (0, 33, b),
                                   (16, 3, c), (16, 11, d)):
            r[offset+RAD.index(rad)] = value*(D//inp['moser_denominator'])
        m.append(tuple(r))
    p = []
    for row in inp['palette_rows']:
        r = [0]*32
        for offset in (0, 16):
            for j, rad in enumerate(inp['palette_radicals']):
                r[offset+RAD.index(rad)] = row[offset//2+j]*(D//inp['palette_denominator'])
        p.append(tuple(r))
    if len(m) != 11 or len(p) != 16 or len(set(m)) != 11 or len(set(p)) != 16:
        raise ValueError('source size/collision')
    me, pe = edges(m), edges(p)
    if len(me) != 19 or len(pe) != 25:
        raise ValueError('source complete-edge mismatch')
    points = sorted({tuple(x+y for x, y in zip(a, b)) for a in m for b in p})
    index = {q: i for i, q in enumerate(points)}
    matrix = [[index[tuple(x+y for x, y in zip(a, b))] for b in p] for a in m]
    if any(len(set(row)) != 16 for row in matrix):
        raise ValueError('noninjective translated palette source')
    if any(len({matrix[i][j] for i in range(11)}) != 11 for j in range(16)):
        raise ValueError('noninjective translated Moser source')
    inherited = set()
    for j in range(16):
        inherited.update(tuple(sorted((matrix[a][j], matrix[b][j]))) for a, b in me)
    for i in range(11):
        inherited.update(tuple(sorted((matrix[i][a], matrix[i][b]))) for a, b in pe)
    full = edges(points)
    if not inherited <= set(full):
        raise ValueError('inherited contact missing')
    terminal_ids = sorted({matrix[i][j] for i in inp['moser_terminals'] for j in range(16)} |
                          {matrix[i][j] for i in range(11) for j in inp['palette_terminals']})
    return dict(denominator=D, radicals=RAD, points=points, edges=full,
                inherited_edges=sorted(inherited), address_matrix=matrix,
                terminal_ids=terminal_ids,
                moser_edges=me, palette_edges=pe,
                points_sha256=digest(points), edges_sha256=digest(full))


def cnf(n, edges, colours):
    clauses = []
    for v in range(n):
        vs = [colours*v+c+1 for c in range(colours)]
        clauses.append(vs)
        clauses.extend([-a, -b] for a, b in itertools.combinations(vs, 2))
    clauses.extend([-colours*a-c-1, -colours*b-c-1]
                   for a, b in edges for c in range(colours))
    return f'p cnf {n*colours} {len(clauses)}\n' + ''.join(
        ' '.join(map(str, row))+' 0\n' for row in clauses)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(exist_ok=False)
    graph = construct(json.loads(Path(__file__).with_name('inputs.json').read_text()))
    (args.out/'graph.json').write_text(json.dumps(graph, separators=(',', ':'))+'\n')
    for k in (4, 5):
        (args.out/f'full{k}.cnf').write_text(cnf(len(graph['points']), graph['edges'], k))
    (args.out/'inherited4.cnf').write_text(cnf(len(graph['points']), graph['inherited_edges'], 4))
    print(json.dumps({'points': len(graph['points']), 'unit_edges': len(graph['edges']),
                      'inherited_edges': len(graph['inherited_edges']),
                      'additional_contacts': len(graph['edges'])-len(graph['inherited_edges']),
                      'all_pairs': math.comb(len(graph['points']), 2),
                      'interface_points': len(graph['terminal_ids']),
                      'points_sha256': graph['points_sha256'],
                      'edges_sha256': graph['edges_sha256']}, indent=2))


if __name__ == '__main__':
    main()

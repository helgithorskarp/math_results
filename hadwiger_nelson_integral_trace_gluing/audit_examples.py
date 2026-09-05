"""Real-coordinate dot/area audit, independent of the new algebra and colouring modules."""
from fractions import Fraction as Q
from pathlib import Path
from hashlib import sha256
from math import lcm
from itertools import combinations
import importlib.util,json

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok: raise ValueError(message)


def radical_module():
    path = HERE.parent/'hadwiger_nelson_mixed506_single_hub_reduction/check_examples.py'
    require(sha256(path.read_bytes()).hexdigest() == '8405039707b294ace3af5fd9deffc0a738c17133d442056a4013b9b4b588a50f', 'input pin mismatch')
    s = importlib.util.spec_from_file_location('real_radical_inputs', path)
    R = importlib.util.module_from_spec(s); s.loader.exec_module(R)
    return R


def plus(x, y): return tuple(a+b for a, b in zip(x, y))
def minus(x, y): return tuple(a-b for a, b in zip(x, y))


def configurations():
    R = radical_module()
    def extract(z):
        x, y = z
        require(all(x[i] == 0 for i in range(8) if i not in (0, 6)) and
                all(y[i] == 0 for i in range(8) if i not in (2, 4)), 'bad radical support')
        return tuple(Q(v) for v in (x[0], x[6], y[2], y[4]))
    A, VR = R.read(159), R.read(214)
    BR = list(dict.fromkeys([R.cscale(x, 6) for x in A]+[R.cmul(R.e(5, 0, 0, 1), x) for x in A]))
    B = [tuple(v/72 for v in extract(x)) for x in BR]; V = [tuple(v/12 for v in extract(x)) for x in VR]
    zero = (Q(0),)*4
    H = [(Q(0),)*4, (Q(1), 0, 0, 0), (Q(1, 2), 0, Q(1, 2), 0),
         (Q(-1, 2), 0, Q(1, 2), 0), (Q(-1), 0, 0, 0),
         (Q(-1, 2), 0, Q(-1, 2), 0), (Q(1, 2), 0, Q(-1, 2), 0)]
    out = {}
    def shift(source, x): return [plus(minus(p, source[0]), x) for p in source]
    def pair(name, a, b, P, S):
        # In the non-real pair control Q was counter-rotated, cancelling rho.
        out[name] = (a, b, [(x, zero) for x in P]+[(zero, y) for y in S], len(P))
    for name, a, b, y in [('even_control', 2, 3, Q(4, 3)), ('unit', 1, 6, Q(1, 3))]:
        x, y = (Q(1), 0, 0, 0), (y, 0, 0, 0)
        pair(name+'_wheels', a, b, shift(H, x), shift(H, y))
        pair(name+'_mixed506', a, b, shift(B, x), shift(V, y))
    for k, m, a, b in [(1, 1, 1, 3), (2, 3, 19, 27), (3, 5, 43, 75)]:
        x = (0, 0, Q(m, 1 << k), 0)
        pair(f'even_depth_{k}_wheels', a, b, shift(H, x), shift(H, x))
        if k == 2: pair('even_nonreal_mixed506', a, b, shift(B, x), shift(V, x))
    pair('even_old_path', 2, 3, [(t, 0, 0, 0) for t in (Q(0), Q(4, 3), Q(-8, 27))],
         [(t, 0, 0, 0) for t in (Q(1), Q(7, 9), Q(-95, 81))])
    pair('even_common_centre', 2, 3, H, H)
    pair('even_no_cross', 2, 3, H, [plus((10, 0, 0, 0), x) for x in H])
    rho = R.e(Q(-1, 2), 0, Q(1, 2), 0)
    rotated = [extract(R.cmul(rho, R.e(*y))) for y in H]
    out['unit_nonreal_grid'] = (1, 6, [(x, y) for x in H for y in rotated], None)
    out['unit_fractional_grid'] = (1, 6, [(plus((Q(1, 2), 0, 0, 0), x), plus((Q(1, 4), 0, 0, 0), y))
                                          for x in H for y in H], None)
    return out


def dot(x, y):
    a, b, c, d = x; A, B, C, D = y
    return (a*A+33*b*B+3*c*C+11*d*D, a*B+b*A+c*D+d*C)


def area(x, y):
    a, b, c, d = x; A, B, C, D = y
    return (a*C+11*b*D-c*A-11*d*B, a*D+3*b*C-d*A-3*c*B)


def run(row, config):
    a, b, points, n = config; D = b*b-a*a
    require(row['rotation_a_b_D'] == [a, b, D], 'rotation parameters differ')
    L = lcm(*(Q(v).denominator for p in points for x in p for v in x))
    pts = [(tuple(int(v*L) for v in x), tuple(int(v*L) for v in y)) for x, y in points]
    aliases, first = [], {}
    for i, p in enumerate(points): aliases.append(first.setdefault(p, i))
    h, edges, cross = sha256(), set(), []
    for i, j in combinations(range(len(pts)), 2):
        X, Y = minus(pts[i][0], pts[j][0]), minus(pts[i][1], pts[j][1])
        nx, ny, xy, ar = dot(X, X), dot(Y, Y), dot(X, Y), area(X, Y)
        values = [Q(b*(nx[t]+ny[t])+2*a*xy[t], b*L*L) for t in range(2)]+[
                  Q(-2*ar[t], b*L*L) for t in range(2)]
        h.update((f'{i},{j}:'+','.join(f'{v.numerator}/{v.denominator}' for v in values)+'\n').encode())
        if values == [0, 0, 0, 0]: require(aliases[i] == aliases[j], 'physical overlap differs')
        if values == [1, 0, 0, 0]:
            edges.add(tuple(sorted((aliases[i], aliases[j]))))
            if n is not None and i < n <= j: cross.append([i, j-n])
    edges = sorted(edges)
    colours = [int(c) for c in row['colours']]
    require(len(colours) == len(pts) and all(c in range(4) for c in colours), 'invalid colour data')
    require(all(colours[i] == colours[aliases[i]] for i in range(len(pts))), 'overlap colouring differs')
    require(all(i != j and colours[i] != colours[j] for i, j in edges), 'colouring is improper')
    require(len(first) == row['vertices'] and len(edges) == row['strict_edges'], 'graph sizes differ')
    require(h.hexdigest() == row['squared_distance_sha256'], 'complete distance streams differ')
    require(sha256(''.join(f'{i},{j}\n' for i, j in edges).encode()).hexdigest() == row['edge_sha256'], 'edge hashes differ')
    require(cross == row['cross_edges'], 'cross edge lists differ')
    forest = None
    if n is not None:
        parent = list(range(len(pts)))
        def root(v):
            while v != parent[v]: v = parent[v]
            return v
        for i, j in sorted({tuple(sorted((aliases[i], aliases[n+j]))) for i, j in cross}):
            u, v = root(i), root(j)
            require(u != v, 'cross interface is not a forest')
            parent[u] = v
        forest = True
    if row['case'] == 'unit_wheels':
        require(cross == [[0, 0]] and row['naive_residue_collisions'] == 1, 'negative control differs')
        # Both rational anchors 1 and 1/3 have residue 1, but their placed distance is one.
    return {'case': row['case'], 'pairs_checked': len(pts)*(len(pts)-1)//2,
            'strict_edges': len(edges), 'cross_forest': forest, 'all_distances_edges_and_colours_match': True}


def main():
    rows = json.loads((HERE/'expected_examples.json').read_text())['cases']; configs = configurations()
    require(set(configs) == {r['case'] for r in rows}, 'case list differs')
    out = [run(row, configs[row['case']]) for row in rows]
    print(json.dumps({'cases_checked': len(out), 'total_pair_checks': sum(r['pairs_checked'] for r in out),
                      'all_entries_match': True, 'cases': out}, indent=2))


if __name__ == '__main__': main()

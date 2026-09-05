"""Independent real-coordinate dot/cross audit; imports neither new generator nor colouring."""
from fractions import Fraction as Q
from pathlib import Path
from hashlib import sha256
from math import lcm
from itertools import combinations
import importlib.util,json

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def source_inputs():
    path = HERE.parent/'hadwiger_nelson_mixed506_single_hub_reduction/check_examples.py'
    require(sha256(path.read_bytes()).hexdigest() == '8405039707b294ace3af5fd9deffc0a738c17133d442056a4013b9b4b588a50f', 'input audit pin mismatch')
    spec = importlib.util.spec_from_file_location('real_radical_inputs', path)
    R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
    A, V = R.read(159), R.read(214)
    B = list(dict.fromkeys([R.cscale(a, 6) for a in A]+[R.cmul(R.e(5, 0, 0, 1), a) for a in A]))
    def extract(points, den):
        out = []
        for x, y in points:
            require(all(x[i] == 0 for i in range(8) if i not in (0, 6)) and
                    all(y[i] == 0 for i in range(8) if i not in (2, 4)), 'wrong real support')
            out.append(tuple(Q(v, den) for v in (x[0], x[6], y[2], y[4])))
        return out
    require(len(B) == 292 and len(V) == 214, 'wrong source order')
    return extract(B, 72), extract(V, 12)


def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def subtract(x, y):
    return tuple(a-b for a, b in zip(x, y))


def configurations():
    zero = (Q(0),)*4
    wheel = [(0, 0, 0, 0), (1, 0, 0, 0), (Q(1, 2), 0, Q(1, 2), 0),
             (Q(-1, 2), 0, Q(1, 2), 0), (-1, 0, 0, 0),
             (Q(-1, 2), 0, Q(-1, 2), 0), (Q(1, 2), 0, Q(-1, 2), 0)]
    B, V = source_inputs()
    seeds = [(0, 5, 0, 2, 1, 2), (1, 10, 0, 1, 7, 4), (2, 4, 0, 1, 1, 2),
             (3, 8, 0, 1, 7, 2), (4, 16, 0, 3, 11, 6)]
    out = {}
    for k, den, a, b, c, d in seeds:
        x, y = (Q(a, den), Q(0), Q(b, den), Q(0)), (Q(c, den), Q(0), Q(d, den), Q(0))
        out[f'wheel_depth_{k}'] = ([add(x, w) for w in wheel], [add(y, w) for w in wheel], c, d)
        if k < 4:
            out[f'mixed506_depth_{k}'] = ([add(subtract(w, B[0]), x) for w in B],
                                          [add(subtract(w, V[0]), y) for w in V], c, d)
    out['common_centre'] = (wheel, wheel, 1, 2)
    out['no_cross_edges'] = (wheel, [add((10, 0, 0, 0), w) for w in wheel], 1, 2)
    return out


def dot(p, q):
    a, b, c, d = p; A, B, C, D = q
    return (a*A+33*b*B+3*c*C+11*d*D, a*B+b*A+c*D+d*C)


def sqrt3_cross(p, q):
    a, b, c, d = p; A, B, C, D = q
    return (3*(a*C-c*A)+33*(b*D-d*B), a*D-d*A+3*(b*C-c*B))


def check(row, config):
    P, S, c, d = config
    n, N = len(P), c*c+3*d*d
    require(row['rotation_root_squared'] == N and row['rotation_numerator'] == [c, d], 'rotation changed')
    D = lcm(*(Q(v).denominator for p in P+S for v in p))
    pts = [tuple(int(v*D) for v in p) for p in P+S]
    total = len(pts)
    require([n, total-n] == row['source_orders'], 'source orders changed')
    norm = [dot(p, p) for p in pts]
    h, edges, cross, pairs, zero_pairs = sha256(), [], [], 0, []
    aliases = list(range(total))
    zero_P = [i for i in range(n) if pts[i] == (0, 0, 0, 0)]
    zero_S = [i for i in range(n, total) if pts[i] == (0, 0, 0, 0)]
    if zero_P and zero_S:
        aliases[zero_S[0]] = zero_P[0]
    for i, j in combinations(range(total), 2):
        pairs += 1
        if i < n <= j:
            # dot(p,u*q) = (c*dot(p,q)+d*sqrt(3)*cross(p,q))/sqrt(N).
            dp, cp = dot(pts[i], pts[j]), sqrt3_cross(pts[i], pts[j])
            values = [Q(norm[i][t]+norm[j][t], D*D) for t in range(2)]+[
                Q(-2*(c*dp[t]+d*cp[t]), N*D*D) for t in range(2)]
        else:
            diff = subtract(pts[i], pts[j])
            nn = dot(diff, diff)
            values = [Q(nn[0], D*D), Q(nn[1], D*D), Q(0), Q(0)]
        h.update((f'{i},{j}:'+','.join(f'{v.numerator}/{v.denominator}' for v in values)+'\n').encode())
        if values == [0, 0, 0, 0]:
            zero_pairs.append((i, j))
            require(aliases[i] == aliases[j], 'unaccounted physical overlap')
        if values == [1, 0, 0, 0]:
            edges.append(tuple(sorted((aliases[i], aliases[j]))))
            if i < n <= j:
                cross.append([i, j-n])
    edges = sorted(set(edges))
    colours = [int(c) for c in row['colours']]
    require(len(colours) == total and all(c in range(4) for c in colours), 'invalid colouring')
    require(all(colours[i] == colours[aliases[i]] for i in range(total)), 'overlap colouring changed')
    require(all(i != j and colours[i] != colours[j] for i, j in edges), 'improper colouring')
    require(h.hexdigest() == row['squared_distance_sha256'], 'complete squared distances disagree')
    require(cross == row['cross_edges'], 'complete cross edge lists disagree')
    require(len(edges) == row['strict_edges'] and len(set(aliases)) == row['vertices'], 'strict graph differs')
    require(sha256(''.join(f'{i},{j}\n' for i, j in edges).encode()).hexdigest() == row['edge_sha256'], 'edge hashes differ')
    # For these controls each cross component is a star, verified without C4 enumeration.
    adj = {i: set() for i in range(total)}
    for i, j in cross:
        adj[i].add(n+j); adj[n+j].add(i)
    require(all(len(adj[i]) <= 1 or len(adj[j]) <= 1 for i, j in [(i, n+j) for i, j in cross]), 'cross graph is not a star forest')
    return {'case': row['case'], 'pairs_checked': pairs, 'strict_edges': len(edges),
            'cross_edges': len(cross), 'cross_star_forest': True, 'all_distances_edges_and_colours_match': True}


def main():
    rows = json.loads((HERE/'expected_examples.json').read_text())['cases']
    configs = configurations()
    require(set(configs) == {r['case'] for r in rows}, 'case sets differ')
    checks = [check(row, configs[row['case']]) for row in rows]
    print(json.dumps({'cases_checked': len(checks), 'total_pair_checks': sum(r['pairs_checked'] for r in checks),
                      'all_entries_match': True, 'cases': checks}, indent=2))


if __name__ == '__main__':
    main()

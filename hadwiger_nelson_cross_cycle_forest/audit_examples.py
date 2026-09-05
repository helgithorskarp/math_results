"""No-import rational Gram and component audit of the exact cycle examples."""
from fractions import Fraction as Q
from pathlib import Path
from collections import Counter
from hashlib import sha256
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def conic(P, S, a, b, h):
    values = P+S
    n = len(P)

    def norm(i, j):
        r, s = values[i], values[j]
        if j < n:
            return a*(r-s)**2
        if i >= n:
            return b*(r-s)**2
        return a*r*r+b*s*s-2*h*r*s

    return n, len(S), norm


def lattice():
    points = [(0, 0), (2, 0), (2, 2), (0, 2), (1, 0), (2, 1), (1, 2), (0, 1)]

    def norm(i, j):
        a, b = (points[i][k]-points[j][k] for k in range(2))
        return Q(a*a+a*b+b*b)

    return 4, 4, norm


def component_cycles(n, cross):
    adj = [set() for _ in range(n)]
    for i, j in cross:
        adj[i].add(j)
        adj[j].add(i)
    require(all(len(a) <= 2 for a in adj), 'calibration cross graph exceeds degree two')
    unseen = set(range(n))
    sizes = Counter()
    while unseen:
        v = min(unseen)
        todo, seen = [v], {v}
        for w in todo:
            for z in adj[w]:
                if z not in seen:
                    seen.add(z)
                    todo.append(z)
        unseen -= seen
        if all(len(adj[w]) == 2 for w in seen):
            sizes[len(seen)] += 1
        else:
            require(sum(len(adj[w]) for w in seen) == 2*(len(seen)-1), 'component is not a path')
    return dict(sorted(sizes.items()))


def main():
    rows = json.loads((Path(__file__).parent/'expected_examples.json').read_text())['examples']
    r = [Q(3, 7), Q(5, 7), Q(-8, 7)]
    models = {
        'non_base_cross_four_cycle': conic([Q(1, 4), Q(-1, 4)], [Q(1, 4), Q(-1, 4)], 3, 13, 0),
        'field_preserving_six_cycle': conic(r, r, 1, 1, Q(-1, 2)),
        'field_preserving_eight_cycle': lattice(),
        'field_preserving_twelve_cycle': conic([Q(x, 7) for x in (-5, -8, -3, 5, 8, 3)],
            [Q(x, 7) for x in (-13, -11, 2, 13, 11, -2)], 3, 1, Q(3, 2)),
        'larger_field_non_base_eight_cycle': conic([Q(x, 5) for x in (7, 1, -7, -1)],
            [Q(x, 5) for x in (4, -3, -4, 3)], 1, 2, 1),
        'non_base_quadratic_path': conic([Q(0), Q(4, 3), Q(-8, 27)],
            [Q(1), Q(7, 9), Q(-95, 81)], 1, 1, Q(2, 3))
    }
    require(set(models) == {r['case'] for r in rows}, 'case list mismatch')
    out, pair_count = [], 0
    for row in rows:
        n, m, norm = models[row['case']]
        require(n+m == row['vertices'], 'vertex count mismatch')
        stream, edges, cross = [], [], []
        for i in range(n+m):
            for j in range(i+1, n+m):
                d = Q(norm(i, j))
                require(d > 0, 'distinctness or positivity failure')
                stream.append(f'{i},{j}:{d.numerator}/{d.denominator}\n')
                if d == 1:
                    edges.append((i, j))
                    if i < n <= j:
                        cross.append((i, j))
        require(sha256(''.join(stream).encode()).hexdigest() == row['squared_distance_sha256'],
                'complete squared-distance stream mismatch')
        require(sha256(''.join(f'{i},{j}\n' for i, j in edges).encode()).hexdigest() == row['edge_sha256'],
                'complete strict edge stream mismatch')
        require([[i, j-n] for i, j in cross] == row['cross_edges'], 'cross edges mismatch')
        colours = row['colours']
        require(len(colours) == n+m and all(c in range(4) for c in colours)
                and all(colours[i] != colours[j] for i, j in edges), 'improper certificate colouring')
        cc = component_cycles(n+m, cross)
        require(cc == {int(k): v for k, v in row['cross_cycle_lengths'].items()}, 'component cycle mismatch')
        pair_count += len(stream)
        out.append({'case': row['case'], 'pairs_checked': len(stream), 'cross_cycle_lengths': cc})
    print(json.dumps({'cases_checked': len(rows), 'pairs_checked': pair_count,
                      'all_squared_distances_edges_colours_and_components_match': True,
                      'cases': out}, indent=2))


if __name__ == '__main__':
    main()

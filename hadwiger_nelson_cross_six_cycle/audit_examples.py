"""Independent rational Gram-matrix and physical-vertex DFS audit of examples."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def line_distances(P, Q, cosine=None, height2=None):
    points = P+Q
    n = len(P)

    def distance(i, j):
        a, b = points[i], points[j]
        if (i < n) == (j < n):
            return (a-b)**2
        if cosine is not None:
            return a*a+b*b-2*cosine*a*b
        return (a-b)**2+height2

    return n, len(Q), distance


def hexagon(wheel=False, reflected=False):
    P = [0, 2, 4]
    Q = [1, 5, 3] if reflected else [1, 3, 5]
    if wheel:
        P, Q = [None]+P, [None]+Q
    points = P+Q
    cosine = [F(1), F(1, 2), F(-1, 2), F(-1), F(-1, 2), F(1, 2)]

    def distance(i, j):
        a, b = points[i], points[j]
        if a is None or b is None:
            return F(a is not b)
        return 2-2*cosine[(a-b) % 6]

    return len(P), len(Q), distance


def cycle_dfs(n, m, cross, aliases, physical):
    neighbours = [[] for _ in range(n+m)]
    for i, j in cross:
        neighbours[i].append(n+j)
        neighbours[n+j].append(i)
    cycles = set()

    def walk(path):
        if len(path) == 6:
            if path[0] in neighbours[path[-1]]:
                edges = tuple(sorted(tuple(sorted((path[k], path[(k+1) % 6])))
                                     for k in range(6)))
                cycles.add(edges)
            return
        used = {aliases[i] if physical else i for i in path}
        for j in neighbours[path[-1]]:
            if (aliases[j] if physical else j) not in used:
                walk(path+[j])

    for i in range(n):
        walk([i])
    return len(cycles)


def main():
    rows = json.loads((Path(__file__).parent/'expected_examples.json').read_text())['examples']
    r = [F(3, 7), F(5, 7), F(-8, 7)]
    z = list(map(F, (-1, 0, 1)))
    cases = {
        'regular_hexagon': hexagon(),
        'connected_hexagonal_wheel': hexagon(wheel=True),
        'collinear_six_cycle': line_distances(r, r, cosine=F(-1, 2)),
        'reflected_hexagon': hexagon(reflected=True),
        'external_translation_path': line_distances(
            [F(0), F(1, 2), F(1)], [F(-1, 4), F(1, 4), F(3, 4)], height2=F(15, 16)),
        'quadratic_rotation_path_through_centre': line_distances(
            [F(0), F(4, 3), F(-8, 27)], [F(1), F(7, 9), F(-95, 81)], cosine=F(2, 3)),
        'external_rotation_four_cycle': (2, 2, lambda i, j:
            F(0) if i == j else F(3, 4) if i < 2 and j < 2 else
            F(13, 4) if i >= 2 and j >= 2 else F(1)),
        'folded_labelled_cycle': line_distances(z, z, cosine=F(-1, 2))
    }
    require(set(cases) == {row['case'] for row in rows}, 'case list mismatch')
    counts, total_pairs, labelled_pairs = [], 0, 0
    for row in rows:
        n, m, distance = cases[row['case']]
        matrix = [[distance(i, j) for j in range(n+m)] for i in range(n+m)]
        require(all(matrix[i][j] == matrix[j][i] and matrix[i][j] >= 0
                    for i in range(n+m) for j in range(n+m)), 'invalid Gram distance')
        representatives, aliases = [], []
        for i in range(n+m):
            matches = [k for k, j in enumerate(representatives) if matrix[i][j] == 0]
            if matches:
                require(len(matches) == 1, 'ambiguous point identification')
                aliases.append(matches[0])
            else:
                aliases.append(len(representatives))
                representatives.append(i)
        edges = [(i, j) for i, a in enumerate(representatives)
                 for j, b in enumerate(representatives) if i < j and matrix[a][b] == 1]
        cross = [(i, j) for i in range(n) for j in range(m) if matrix[i][n+j] == 1]
        require(cross == [tuple(e) for e in row['cross_edges']], 'cross edges mismatch')
        digest = sha256(''.join(f'{i},{j}\n' for i, j in edges).encode()).hexdigest()
        require(digest == row['edge_sha256'] and len(edges) == row['strict_edges'],
                'strict edge stream mismatch')
        require(len(representatives) == row['vertices'], 'vertex quotient mismatch')
        colours = row['colours']
        require(len(colours) == len(representatives) and all(c in range(4) for c in colours)
                and all(colours[i] != colours[j] for i, j in edges), 'invalid colouring')
        physical = cycle_dfs(n, m, cross, aliases, True)
        labelled = cycle_dfs(n, m, cross, aliases, False)
        require(physical == row['physical_cross_six_cycles']
                and labelled == row['labelled_cross_six_cycles'], 'DFS cycle mismatch')
        total_pairs += len(representatives)*(len(representatives)-1)//2
        labelled_pairs += (n+m)*(n+m-1)//2
        counts.append({'case': row['case'], 'physical_cycles': physical,
                       'labelled_cycles': labelled})
    print(json.dumps({'cases_checked': len(rows), 'labelled_point_pairs': labelled_pairs,
                      'distinct_point_pairs': total_pairs,
                      'all_gram_distances_edges_colours_and_cycles_match': True,
                      'cycles': counts}, indent=2))


if __name__ == '__main__':
    main()

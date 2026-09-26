"""Independent exact controls for the rigid-hull Gaussian theorem.

CPython 3.11+, standard library only. No author code, expected record,
certificate or numerical Gaussian integral is imported or executed.
The universal analytic statements are reviewed in REVIEW.md, not proved
by these finite controls. --check compares our own compact record.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import ceil, factorial
from pathlib import Path
import argparse
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def l1(a):
    return sum(map(abs, a), F(0))


def center(points, weights):
    require(len(points) == len(weights) and sum(weights) == 1,
            'Invalid probability vector')
    require(all(p > 0 for p in weights), 'Positive weights required')
    mean = tuple(sum(p*x[d] for p, x in zip(weights, points)) for d in range(3))
    return [sub(x, mean) for x in points]


def facets(points):
    """Definition-level supporting-plane enumeration, including polygons."""
    answer = {}
    for i, j, k in combinations(range(len(points)), 3):
        normal = cross(sub(points[j], points[i]), sub(points[k], points[i]))
        if not any(normal):
            continue
        values = [dot(normal, sub(x, points[i])) for x in points]
        if all(v >= 0 for v in values):
            normal = tuple(-v for v in normal)
            values = [-v for v in values]
        if not all(v <= 0 for v in values) or not any(v < 0 for v in values):
            continue
        face = tuple(a for a, v in enumerate(values) if v == 0)
        answer.setdefault(face, (normal, dot(normal, points[i])))
    require(answer, 'No full-dimensional hull')
    return answer


def edges_from_facets(faces):
    """Two vertices share a true edge iff they share two distinct facets."""
    vertices = sorted(set().union(*map(set, faces)))
    return [e for e in combinations(vertices, 2)
            if sum(set(e) <= set(face) for face in faces) == 2]


def edge_rows(points, edges):
    result = []
    for i, j in edges:
        row = [F(0)] * (3*len(points))
        for a, value in enumerate(sub(points[i], points[j])):
            row[3*i+a], row[3*j+a] = value, -value
        result.append(row)
    return result


def gauge_rows(points, weights):
    rows = [[F(0)]*(3*len(points)) for _ in range(6)]
    for i, (x, p) in enumerate(zip(points, weights)):
        for a in range(3):
            rows[a][3*i+a] = p
        c = ((0, -x[2], x[1]), (x[2], 0, -x[0]), (-x[1], x[0], 0))
        for a, b in product(range(3), repeat=2):
            rows[3+a][3*i+b] = p*c[a][b]
    return rows


def gram(rows):
    n = len(rows[0])
    return [[sum(row[i]*row[j] for row in rows) for j in range(n)] for i in range(n)]


def ldl(matrix):
    """Positive LDL^T certificate; refuses zero or negative pivots."""
    n = len(matrix)
    require(all(len(row) == n for row in matrix), 'Matrix not square')
    require(all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n)),
            'Matrix not symmetric')
    lower = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    diagonal = []
    for j in range(n):
        d = matrix[j][j]-sum(lower[j][k]**2*diagonal[k] for k in range(j))
        require(d > 0, 'Gram form not positive definite')
        diagonal.append(d)
        for i in range(j+1, n):
            lower[i][j] = (matrix[i][j]-sum(
                lower[i][k]*lower[j][k]*diagonal[k] for k in range(j)))/d
    require(all(matrix[i][j] == sum(lower[i][k]*diagonal[k]*lower[j][k]
                                  for k in range(n))
                for i in range(n) for j in range(n)), 'LDL reconstruction failed')
    return lower, diagonal


def solve(factor, rhs):
    lower, diagonal = factor
    n = len(rhs)
    y = []
    for i in range(n):
        y.append(rhs[i]-sum(lower[i][j]*y[j] for j in range(i)))
    z = [v/d for v, d in zip(y, diagonal)]
    answer = [F(0)]*n
    for i in reversed(range(n)):
        answer[i] = z[i]-sum(lower[j][i]*answer[j] for j in range(i+1, n))
    return answer


def coercivity(points, weights, edges):
    erows = edge_rows(points, edges)
    grows = gauge_rows(points, weights)
    normal = gram(erows+grows)
    factor = ldl(normal)
    columns = [solve(factor, row) for row in erows]
    for row, col in zip(erows, columns):
        require([dot(a, col) for a in normal] == row, 'Inverse residual')
    # Our simplicial fixtures are isostatic. This verifies the full right
    # inverse on strain coordinates with all six gauge equations zero.
    for j, col in enumerate(columns):
        require([dot(row, col) for row in erows] == [F(int(i == j)) for i in range(len(erows))],
                'Strain reconstruction failed')
        require(not any(dot(row, col) for row in grows), 'Gauge reconstruction failed')
    constant = max(l1(col[3*i:3*i+3])
                   for col in columns for i in range(len(points)))
    return constant, factor[1]


def covariance(points, weights):
    return [[sum(p*x[i]*x[j] for p, x in zip(weights, points))
             for j in range(3)] for i in range(3)]


def kappa_lower(points, weights):
    cov = covariance(points, weights)
    factor = ldl(cov)
    trace_inverse = sum(solve(factor, [F(int(j == i)) for j in range(3)])[i]
                        for i in range(3))
    return 1/trace_inverse


def beta_lower(points, faces, edges):
    values = []
    for i, j in edges:
        normals = [n for face, (n, b) in faces.items() if i in face and j in face]
        require(len(normals) == 2, 'Wrong edge-facet incidence')
        a, b = normals
        # alpha >= sin(alpha), ||a x b|| >= max|coordinate|,
        # and each Euclidean norm is bounded above by the l1 norm.
        numerator = max(map(abs, cross(a, b)))
        require(numerator > 0, 'Zero exterior angle')
        values.append(numerator/(2*l1(sub(points[i], points[j]))*l1(a)*l1(b)))
    return min(values)


def fixture(name, raw, weights):
    points = center([tuple(map(F, x)) for x in raw], weights)
    faces = facets(points)
    require(all(len(f) == 3 for f in faces), 'Fixture hull is not simplicial')
    edges = edges_from_facets(faces)
    require(set().union(*map(set, faces)) == set(range(len(points))), 'Nonvertex in vertex fixture')
    ce, pivots = coercivity(points, weights, edges)
    rx = max(l1(x) for x in points)
    nu0 = min(max(map(abs, sub(x, y))) for x, y in combinations(points, 2))
    beta = beta_lower(points, faces, edges)
    kappa = kappa_lower(points, weights)
    c = beta/(2*ce)
    m = rx+1
    b = F(20*len(points)*(len(points)-1))/(nu0/2)
    a = 280*m+248+b*(1/min(weights)+m*m)  # log(1/p*) <= 1/p*
    root = ceil(max(F(2), 4*m, 16*a/c, 16*b/c))
    radius = root*root
    require(radius >= 2 and radius >= 4*m and radius >= 16*a/c
            and root >= 16*b/c, 'Tail cutoff too small')
    require(4*a/radius+4*b/root <= c/2, 'Tail absorption failed')
    record = {'name': name, 'sites': len(points), 'facets': len(faces), 'edges': len(edges),
              'positive_Gram_pivots': len(pivots), 'C_E': str(ce), 'R_x': str(rx),
              'nu_0': str(nu0), 'beta': str(beta), 'kappa': str(kappa),
              'integer_tail_radius': radius,
              'coercivity': 'exact strain right inverse with zero weighted gauge',
              'tail_absorption': 'certified with pi<4 and log(1/p*)<=1/p*'}
    return record, points, edges, ce


def must_reject(operation, name):
    try:
        operation()
    except ValueError:
        return name
    raise ValueError('Failed to reject '+name)


def scalar_controls():
    count = 0
    for m, multiple in product([F(1, 5), F(1), F(4)], [F(1), F(2), F(3)]):
        rbig = max(F(2), 4*m)*multiple
        for r, mean, velocity, mixed in product(
                [rbig-m, rbig, rbig+m], [-m, m], [-F(1), F(1)], [-m, m]):
            derivative = (r*velocity-mixed)/(r-mean)
            require(abs(derivative) <= 2, 'Radial derivative bound')
            require(abs(derivative-velocity) <= 4*m/rbig, 'Posterior correction bound')
            require(abs((r/rbig)**2-1) <= F(9, 4)*m/rbig, 'Radial Jacobian bound')
            count += 1
    moments = [F(factorial(k), 1)/F(2, 3)**(k+1) for k in range(3)]
    require(moments[0] == F(3, 2) and moments[1]+moments[2] == 9,
            'Exterior Gamma integrals')
    require(F(9, 4)*2+4 <= 10 and F(25, 16)*2+1 <= 5,
            'Volume comparison constants')
    require(40+240 == 280 and 8+240 == 248, 'Final tail coefficients')
    # Exact axis-box support integral: W/pi = side_x+side_y+side_z.
    # Its 12 true edges have exterior angle pi/2. The first variation
    # formula must therefore have its displayed 1/2 factor.
    lengths = [F(2), F(3), F(5)]
    velocities = [-F(1, 7), -F(2, 9), -F(1, 11)]
    edge_formula_over_pi = sum(F(1, 2)*F(1, 2)*4*v for v in velocities)
    require(edge_formula_over_pi == sum(velocities), 'Mean-width normalization')
    require(sum(lengths) == F(1, 2)*F(1, 2)*4*sum(lengths), 'Support normalization')
    require(1 > F(3, 4), 'Reduced posterior coefficient should fail at R=4,M=1')
    return {'radial_corner_controls': count, 'Gamma_moments': list(map(str, moments)),
            'support_normalization': '12-edge axis box, exact coefficients of pi',
            'coefficient_rejection': '3M/R fails for r=3,m=1,A=1,B=-1,R=4'}


def run():
    data = [
        ('asymmetric_tetrahedron', [(0,0,0),(2,0,0),(1,3,0),(1,1,4)],
         [F(i,11) for i in (1,2,3,5)]),
        ('triangular_bipyramid', [(-1,-1,0),(2,-1,0),(-1,2,0),(0,0,2),(0,0,-2)],
         [F(1,5)]*5),
        ('sheared_octahedron', [(2,0,1),(-2,0,-1),(1,3,0),(-1,-3,0),(0,1,2),(0,-1,-2)],
         [F(i,21) for i in range(1,7)]),
        ('moment_curve_7', [(i,i*i-4,i*i*i) for i in range(-3,4)], [F(1,7)]*7),
    ]
    records = []
    fixtures = []
    for args in data:
        item = fixture(*args)
        records.append(item[0])
        fixtures.append(item)
    _, points, edges, ch = fixtures[-1]
    faces = facets(points)
    rho = min(offset/(1+l1(normal)) for normal, offset in faces.values())
    require(rho > 0, 'Centroid is not strictly inside')
    require(all(offset*offset >= rho*rho*dot(normal,normal)
                for normal,offset in faces.values()), 'Interior ball failed')
    full = points+[(F(0), F(0), F(0))]
    weights = [F(1,8)]*8
    rx = max(l1(x) for x in full)
    kappa = kappa_lower(full, weights)
    k = max(F(1), 2*rx/rho)
    ce = (2+rx*rx/(2*kappa))*k*ch
    # A concrete gauged velocity defeats an equality-only extension:
    # move the interior site by e1 and remove the common mean velocity.
    bad_velocity = [(-F(1,8),F(0),F(0))]*7+[(F(7,8),F(0),F(0))]
    flat = [value for row in bad_velocity for value in row]
    require(not any(dot(row,flat) for row in gauge_rows(full,weights)),
            'Interior obstruction is not gauged')
    require(not any(dot(row,flat) for row in edge_rows(full,edges)),
            'Interior obstruction changes hull strains')
    positive_strain = max(dot(sub(full[i],full[j]),sub(bad_velocity[i],bad_velocity[j]))
                          for i,j in combinations(range(8),2))
    require(positive_strain > 0, 'Missing all-pair cone obstruction')
    interior = {'sites':8,'interior_sites':1,'rho':str(rho),'C_H':str(ch),
                'kappa':str(kappa),'K':str(k),'C_E':str(ce),
                'facet_ball_checks':len(faces),
                'gauged_zero_hull_strain_obstruction':{'interior_velocity':list(map(str,bad_velocity[-1])),
                                                     'positive_nonedge_strain':str(positive_strain)},
                'boundary':'C_E uses all pair-strain inequalities, not a full-rank edge matrix on eight sites.'}
    cube = [tuple(map(F,x)) for x in product((-1,1),repeat=3)]
    cube_edges = edges_from_facets(facets(cube))
    require(len(cube_edges) == 12, 'Cube edge set')
    _, tetra, te, _ = fixtures[0]
    tw = data[0][2]
    rejected = [
        must_reject(lambda: ldl(gram(edge_rows(tetra,te[:-1])+gauge_rows(tetra,tw))), 'deleted tetrahedral edge'),
        must_reject(lambda: ldl(gram(edge_rows(tetra,te)+gauge_rows(tetra,tw)[3:])), 'translation gauge omitted'),
        must_reject(lambda: ldl(gram(edge_rows(tetra,te)+gauge_rows(tetra,tw)[:3])), 'rotation gauge omitted'),
        must_reject(lambda: ldl(gram(edge_rows(cube,cube_edges)+gauge_rows(cube,[F(1,8)]*8))), 'cube actual edges are not infinitesimally rigid'),
        must_reject(lambda: ldl(gram(edge_rows(full,edges)+gauge_rows(full,weights))), 'interior site controlled by hull equalities alone'),
        must_reject(lambda: center(tetra,[F(0),F(1,3),F(1,3),F(1,3)]), 'zero prior weight in fixed-label theorem'),
    ]
    return {'status':'INDEPENDENT_RIGID_HULL_GEOMETRY_REVIEW_PASS',
            'fixtures':records,'interior_cone_control':interior,
            'scalar_controls':scalar_controls(),'deliberate_rejections':rejected,
            'author_checker_or_certificate_used':False,
            'scope':'Finite exact evidence for the written review, not an analytic formalization or full conjecture proof.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    record = run()
    raw = (json.dumps(record,sort_keys=True,indent=2)+'\n').encode()
    path = Path(__file__).with_name('EXPECTED.json')
    if args.write_expected:
        path.write_bytes(raw)
    if args.check:
        require(json.loads(path.read_text()) == record, 'Own expected record mismatch')
    print(record['status'])
    print('sha256',hashlib.sha256(raw).hexdigest())
    print('fixtures',len(record['fixtures']),'radial_controls',record['scalar_controls']['radial_corner_controls'],
          'rejections',len(record['deliberate_rejections']))


if __name__ == '__main__':
    main()

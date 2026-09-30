"""Independent medial interpretation and denominator-free angle audit."""
from collections import Counter, deque
from pathlib import Path
import argparse
import json
import sympy as sp
import maps

C = sp.Symbol('c')
H = 1 + 2*C
RHO = sp.Matrix([[0, 1], [C*H, 0]])
SUM = sp.Matrix([[C, 1], [H, -C]])


def need(ok, message):
    if not ok:
        raise ValueError(message)


def zero(expr):
    return sp.Poly(sp.expand(expr), C, domain=sp.QQ).is_zero


def normalized_faces(ts, qs):
    return [sorted(maps.cycle_key(f) for f in fs) for fs in (ts, qs)]


def medial_faces(rotation):
    edges = tuple(sorted((i, j) for i, ns in enumerate(rotation) for j in ns if i < j))
    edge_index = {e: k for k, e in enumerate(edges)}
    next_dart = {}
    for v, seq in enumerate(rotation):
        for k, prev in enumerate(seq):
            next_dart[(prev, v)] = (v, seq[k - 1])
    white = []
    pending = set(next_dart)
    while pending:
        start = min(pending)
        current = start
        face = []
        vertices = []
        while True:
            need(current in pending, 'disjoint complete face orbit')
            pending.remove(current)
            vertices.append(current[0])
            face.append(edge_index[tuple(sorted(current))])
            current = next_dart[current]
            if current == start:
                break
        need(len(vertices) in (3, 4) and len(set(vertices)) == len(vertices), 'simple T/Q G face')
        white.append(tuple(face))
    black = [tuple(edge_index[tuple(sorted((i, j)))] for j in ns) for i, ns in enumerate(rotation)]
    both = black + white
    ts = [f for f in both if len(f) == 3]
    qs = [f for f in both if len(f) == 4]
    need(len(ts) == 8 and len(qs) == 9, 'all original medial faces')
    edge_counts = Counter(tuple(sorted((a, b))) for f in both for a, b in zip(f, f[1:] + f[:1]))
    need(len(edge_counts) == 30 and set(edge_counts.values()) == {2}, 'medial edges twice incident')
    original_nb = [set() for _ in edges]
    for a, b in edge_counts:
        original_nb[a].add(b)
        original_nb[b].add(a)
    need(len(edges) == 15 and all(len(x) == 4 for x in original_nb), 'fifteen degree-four original vertices')
    tcount = Counter(v for f in ts for v in f)
    return ts, qs, [tcount[v] for v in range(15)]


def links_from_faces(cert):
    ts, qs = cert['Ts'], cert['Qs']
    need(len(ts) == 8 and len(qs) == 9, 'fixed face counts')
    need(all(len(f) == 3 and len(set(f)) == 3 for f in ts), 'simple triangles')
    need(all(len(f) == 4 and len(set(f)) == 4 for f in qs), 'simple quadrilaterals')
    tc = Counter(v for f in ts for v in f)
    corners = {v: [] for v in range(15)}
    links = [(2*i, 2*i + 1, 'rho') for i in range(9)]
    for i, f in enumerate(qs):
        for k, v in enumerate(f):
            need(type(v) is int and v in corners, 'original vertex label')
            corners[v].append(2*i + k % 2)
    for v in range(15):
        need(tc[v] <= 2 and len(corners[v]) == 4 - tc[v], 'complete degree-four corner incidence')
        if tc[v] == 2:
            need(len(set(corners[v])) == 2, 'distinct two-T Q slots')
            links.append((*corners[v], 'S'))
    return links, corners, tc


def coefficient_list(expr):
    p = sp.Poly(sp.expand(expr), C, domain=sp.QQ)
    return [str(x) for x in reversed(p.all_coeffs())] if not p.is_zero else []


def projective_audit(cert):
    links, corners, tc = links_from_faces(cert)
    labels = {}
    neighbors = [[] for _ in range(18)]
    for a, b, label in links:
        key = tuple(sorted((a, b)))
        need(key not in labels, 'unique independent angle-link edge')
        labels[key] = label
        neighbors[a].append((b, label))
        neighbors[b].append((a, label))
    walk = cert['closure_cycle']
    need(len(walk) > 3 and walk[0] == walk[-1], 'nontrivial closed angle walk')
    word = []
    reduced = []
    product = sp.eye(2)
    for a, b in zip(walk, walk[1:]):
        label = labels[tuple(sorted((a, b)))]
        word.append(label)
        if reduced and reduced[-1] == label:
            reduced.pop()
        else:
            reduced.append(label)
        product = {'rho': RHO, 'S': SUM}[label] * product
    need(reduced == ['rho', 'S', 'rho'], 'conjugate reflection word')
    scalar = sp.cancel(product[0, 0] / (RHO*SUM*RHO)[0, 0])
    need(all(zero(x) for x in product - scalar*(RHO*SUM*RHO)), 'full homogeneous loop composition')
    need(all(zero(x) for x in RHO*RHO - C*H*sp.eye(2)), 'rho square is positive scalar identity')
    need(all(zero(x) for x in SUM*SUM - (1+C)**2*sp.eye(2)), 'S square is positive scalar identity')
    z = sp.Symbol('z')
    need(sp.expand((z-1)*(H*z+1) - (H*z*z - 2*C*z - 1)) == 0, 'unique positive S fixed point')
    center = walk[1]
    points = {center: sp.Matrix([1, 1])}
    paths = {center: [center]}
    queue = deque([center])
    while queue:
        a = queue.popleft()
        for b, label in sorted(neighbors[a]):
            new = {'rho': RHO, 'S': SUM}[label] * points[a]
            new = new.applyfunc(sp.expand)
            if b in points:
                need(zero(new[0]*points[b][1] - new[1]*points[b][0]), 'all homogeneous link identities')
            else:
                points[b] = new
                paths[b] = paths[a] + [b]
                queue.append(b)
    need(len(points) == 18, 'all angle slots reached')
    # Every matrix is invertible for c>0. At an actual strict-convex
    # corner every half tangent is positive and finite. Thus all vectors
    # along these physical paths have a positive, nonzero denominator;
    # no special parameter can be discarded by a formal cancellation.
    need(zero(RHO.det() + C*H) and zero(SUM.det() + (1+C)**2), 'nonzero projective determinants')
    values = {i: sp.cancel(v[0]/v[1]) for i, v in points.items()}
    one = cert['one_T_vertex']
    upper = cert['upper_bound_slot']
    need(one == 2 and upper == 10 and tc[one] == 1 and set(corners[one]) == {10, 13, 14}, 'exact required original one-T star')
    need(zero(points[14][0] - points[14][1]), 'star contains pi-minus-alpha corner')
    need(sp.cancel(values[10] - C/(1-2*C*C)) == 0, 'critical upper slot')
    need(sp.cancel(values[13] - (1-2*C*C-C**3)/(C*C*(1+C))) == 0, 'critical other slot')
    # Record the actual homogeneous common factors. Each is nonzero
    # and positive for c>0, so the critical formulas discard no pole.
    critical_pairs = {10: (C, 1-2*C*C),
                      13: (1-C-C*C, C*C), 14: (1, 1)}
    common = {}
    for slot, (p, q) in critical_pairs.items():
        factor = sp.cancel(points[slot][0]/p)
        need(zero(points[slot][0] - factor*p)
             and zero(points[slot][1] - factor*q), 'critical homogeneous factor')
        # QQ[c] expanded coefficients are all nonnegative and nonzero.
        poly = sp.Poly(sp.expand(factor), C, domain=sp.QQ)
        need(all(x >= 0 for x in poly.all_coeffs()) and not poly.is_zero,
             'critical common factor positive for c>0')
        common[slot] = str(sp.factor(factor))
    residual = sp.cancel(H*values[10]*values[13] - 1)
    excess = sp.cancel(values[10] - 1/C)
    need(sp.cancel(residual + excess) == 0, 'star equation forces Q upper endpoint')
    need(sp.cancel(residual - (1-3*C*C)/(C*(1-2*C*C))) == 0, 'forced c squared one-third')
    # A full algebraic certificate at the only forced candidate, including
    # the violation of the WEAK lower corner bound z13 >= 1/H.
    obstruction = sp.cancel(values[13] - 1/H)
    numerator, denominator = sp.fraction(obstruction)
    num = sp.rem(sp.Poly(numerator, C), sp.Poly(3*C*C-1, C)).as_expr()
    den = sp.rem(sp.Poly(denominator, C), sp.Poly(3*C*C-1, C)).as_expr()
    modulus = sp.Poly(3*C*C-1, C)
    need(sp.rem(sp.Poly(den*(5-9*C)-num, C), modulus).is_zero,
         'candidate lower-corner gap equals 5-9c')
    need(sp.gcd(sp.Poly(den, C), modulus).degree() == 0, 'candidate gap denominator nonzero')
    need(27 > 25, 'at positive c squared one-third,9c>5')
    # Print the actual reduced fraction for transparent interpretation.
    return {'original_word': word, 'reduced_word': reduced,
            'loop_scalar': sp.factor(scalar).__str__(), 'fixed_slot': center,
            'projective_paths': paths,
            'homogeneous_vectors': {i: [coefficient_list(p), coefficient_list(q)] for i, (p, q) in points.items()},
            'critical_common_positive_factors': common,
            'rational_values': {i: str(x) for i, x in values.items()},
            'star_slots': corners[one], 'star_residual': str(residual),
            'Q_upper_difference': str(excess), 'weak_lower_gap_at_forced_candidate': [str(num), str(den)],
            'weak_lower_gap_in_quadratic_field': '5-9c<0 at c=1/sqrt(3), since27>25',
            'weak_lower_contradiction': 'u13=pi-2alpha<alpha since alpha>pi/3; completeness of contact graph unnecessary',
            'generalized_parameter_domain': 'Every possible 15-point packing,113/225<=c<1; no upper cutoff'}


def run(map_output, cert):
    matched = []
    rejected = []
    target = normalized_faces(cert['Ts'], cert['Qs'])
    for row in map_output['maps']:
        for rotation in row['rotations']:
            ts, qs, tc = medial_faces(tuple(map(tuple, rotation)))
            if max(tc) > 2:
                rejected.append({'graph_mask': row['graph_mask'], 'three_T_vertices': [i for i, v in enumerate(tc) if v > 2]})
            else:
                need(normalized_faces(ts, qs) == target, 'full original face complex comparison')
                matched.append({'graph_mask': row['graph_mask'], 'triangle_counts': tc})
    need(len(rejected) == 8 and len(matched) == 2, 'all ten sphere maps handled')
    need(all(x['graph_mask'] == cert['graph_mask'] for x in matched), 'unique surviving abstract graph type')
    return {'agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'three_T_maps_rejected': rejected, 'full_face_complex_matches': matched,
            'projective_angles': projective_audit(cert)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('map_output', type=Path)
    parser.add_argument('certificate', type=Path)
    args = parser.parse_args()
    print(json.dumps(run(json.loads(args.map_output.read_text()), json.loads(args.certificate.read_text())), indent=2, sort_keys=True))

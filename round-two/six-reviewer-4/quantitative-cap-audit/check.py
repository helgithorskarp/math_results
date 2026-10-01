"""Independent quantitative J74 cap audit, reviewer six-reviewer-4.

Uses hash-pinned code from this reviewer's earlier sufficient geometry/contact
audits. No researcher module executes. New reductions are written in REVIEW.md.
"""
import argparse
import copy
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def need(ok, why):
    if not ok:
        raise ValueError(why)


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    out = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out


def load():
    manifest = json.loads((HERE/'DEPENDENCIES.json').read_text())
    for name, digest in manifest['sha256'].items():
        need(hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest,
             'pinned independent dependency '+name)
    sys.path.insert(0, str(HERE/'../mirror-rigidity-audit'))
    contact = module('independent_contact_audit', HERE/'../mirror-rigidity-audit/audit.py')
    projection = module('independent_projection_audit', HERE/'../j74-projection-audit/audit.py')
    return contact, projection


C, G = load()
S, dot, cross = C.S, C.dot, C.cross
add, sub, scale = C.add, C.sub, C.scale
ZERO = (S(), S(), S())
R2 = S(11, 4, 4)
A0 = S(13, 7, 2)


def mmul(a, b):
    return [[sum((x*y for x, y in zip(row, col)), S())
             for col in zip(*b)] for row in a]


def eliminate(a):
    """Independent pivoted Gauss-Jordan inverse, not a cofactor formula."""
    n = len(a)
    out = [list(row)+[S(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if out[i][j] != 0), None)
        need(pivot is not None, 'full column rank')
        out[j], out[pivot] = out[pivot], out[j]
        q = out[j][j]
        out[j] = [x/q for x in out[j]]
        for i in range(n):
            if i != j:
                q = out[i][j]
                out[i] = [x-q*y for x, y in zip(out[i], out[j])]
    inv = [row[n:] for row in out]
    identity = [[S(i == j) for j in range(n)] for i in range(n)]
    need(mmul(a, inv) == mmul(inv, a) == identity, 'two literal inverse identities')
    return inv


def singleton_profiles(vertices, inputs, weights):
    profiles = []
    for j, (m, record) in enumerate(zip(C.axes(), weights)):
        qix = sorted(i for i, v in enumerate(vertices) if dot(v, m) == 0)
        need(record['axis'] == j and len(qix) == 4
             and sorted(record['equatorial_original_indices']) == qix,
             'four and only four equatorial originals')
        beta = list(map(C.pair, record['equatorial_weights']))
        need(len(beta) == 4 and min(beta) > 0 and sum(beta, S()) == 1,
             'positive normalized weights')
        pairs = list(zip(record['equatorial_original_indices'], beta))
        need(tuple(sum((b*vertices[i][k] for i, b in pairs), S())
                   for k in range(3)) == ZERO, 'physical barycenter zero')
        moment = [[sum((b*vertices[i][k]*vertices[i][l] for i, b in pairs), S())
                   for l in range(3)] for k in range(3)]
        excess = [[moment[k][l]-(S(k == l)-m[k]*m[l])/2 for l in range(3)] for k in range(3)]
        trace = sum((excess[k][k] for k in range(3)), S())
        determinant = (trace**2-sum((excess[k][l]*excess[l][k]
                                   for k in range(3) for l in range(3)), S()))/2
        need(trace > 0 and determinant > 0 and C.matvec(excess, m) == ZERO,
             'strict positive planar moment excess above one half')
        boundary = inputs['boundary_profiles'][j]['boundary_original_indices']
        height2 = min(dot(m, vertices[i])**2 for i in boundary if i not in qix)
        sep2 = min(dot(sub(vertices[a], vertices[b]), sub(vertices[a], vertices[b]))
                   for a, b in combinations(qix, 2))
        best = max(combinations(qix, 2), key=lambda ab: dot(cross(vertices[ab[0]], vertices[ab[1]]),
                                                         cross(vertices[ab[0]], vertices[ab[1]])))
        gramdet = dot(cross(vertices[best[0]], vertices[best[1]]),
                      cross(vertices[best[0]], vertices[best[1]]))
        need(height2 >= S(1, 0, 4) and sep2 >= 1 and gramdet > S(81, 0, 4)
             and 2*R2 < 10, 'radial gaps and well-conditioned physical pair')
        profiles.append({'axis': j, 'singletons': qix, 'moment_trace': str(trace),
                         'moment_determinant': str(determinant), 'height2': str(height2),
                         'separation2': str(sep2), 'basis_gram_determinant': str(gramdet)})
    need(len(profiles) == 6, 'six complete singleton profiles')
    return profiles


def correspondence(vertices, inputs, profiles):
    known = {(r['source_axis'], r['receiver_axis'],
              tuple(tuple(C.vec(v)) for v in r['proper_matrix_columns'])): i
             for i, r in enumerate(inputs['motions'])}
    need(len(known) == 22, 'distinct receiver-marked proper motions')
    records, gaps = [], []
    count = 0
    for s, source in enumerate(profiles):
        q = source['singletons']
        a, b = next((vertices[i], vertices[j]) for i, j in combinations(q, 2)
                    if dot(cross(vertices[i], vertices[j]), cross(vertices[i], vertices[j])) > 0)
        frame = list(zip(a, b, cross(a, b)))
        frame_inverse = eliminate(frame)
        for r, target in enumerate(profiles):
            for perm in permutations(target['singletons']):
                count += 1
                # Full labelled squared-distance comparison, including all diagonals.
                mismatch = max(C.absolute(dot(vertices[i], vertices[j])-dot(vertices[x], vertices[y]))
                               for i, x in zip(q, perm) for j, y in zip(q, perm))
                if mismatch != 0:
                    gaps.append(mismatch)
                    continue
                match = dict(zip(q, perm))
                ia, ib = next((i, j) for i, j in combinations(q, 2)
                              if dot(cross(vertices[i], vertices[j]), cross(vertices[i], vertices[j])) > 0)
                aa, bb = vertices[match[ia]], vertices[match[ib]]
                matrix = mmul(list(zip(aa, bb, cross(aa, bb))), frame_inverse)
                cols = tuple(tuple(v) for v in zip(*matrix))
                need(C.det(matrix) == 1 and all(dot(cols[i], cols[j]) == S(i == j)
                                              for i in range(3) for j in range(3)),
                     'proper frame lift of each isometry')
                need(all(C.matvec(matrix, vertices[i]) == vertices[x] for i, x in zip(q, perm)),
                     'all four actual singleton images')
                need((s, r, cols) in known, 'literal proper catalogue lift')
                records.append({'source_axis': s, 'receiver_axis': r,
                                'source_indices': q, 'target_indices': list(perm),
                                'catalogue_index': known[s, r, cols]})
    need(count == 864 and len(gaps) == 842 and len(records) == 22
         and sorted(x['catalogue_index'] for x in records) == list(range(22)),
         'complete correspondence, no unidentified lift')
    gap = min(gaps)
    need(gap == S(0, 3, 10) and gap > S(1, 0, 2), 'exact minimum Gram mismatch')
    return {'bijections': count, 'failed': len(gaps), 'isometries': records, 'gap': str(gap)}


def recovery(vertices, inputs):
    records = []
    for j, record in enumerate(inputs['profiles']):
        m = C.axes()[j]
        e = C.project((S(), S(1), S()), m)
        if dot(e, e) == 0:
            e = C.project((S(), S(), S(1)), m)
        f = cross(m, e)
        need(0 < dot(e, e) <= 1 and dot(e, e) == dot(f, f) and dot(e, f) == 0,
             'bounded orthogonal physical recovery basis')
        for number, fan in enumerate(record['fans']):
            rows = []
            for a, b in fan['original_edges']:
                delta = sub(vertices[b], vertices[a]);h = dot(cross(delta, m), vertices[a])
                normal = scale(1/h, cross(delta, m))
                need(h > 0 and 1/h <= 2 and dot(normal, normal) <= 1,
                     'actual normal and edge height bounds')
                for i in (a, b):
                    rows.append((i, normal, cross(vertices[i], normal)))
            common = []
            for i, beta in zip(record['equatorial_original_indices'], map(C.pair, record['equatorial_weights'])):
                rr = [row for row in rows if row[0] == i]
                need(len(rr) == 2, 'two actual singleton contacts')
                d = sub(rr[0][1], rr[1][1])
                theta = dot(sub(scale(1/R2, vertices[i]), rr[1][1]), d)/dot(d, d)
                common += [(rr[0], beta*theta), (rr[1], beta*(1-theta))]
            omega = [w for _, w in common]
            need(min(omega) > 0 and sum(omega, S()) == 1, 'positive common balance weights')
            linear = [(dot(row[2], m), dot(row[1], e), dot(row[1], f)) for row, _ in common]
            need(all(sum((w*l[k] for w, l in zip(omega, linear)), S()) == 0
                     for k in range(3)), 'literal common linear balance')
            # A different triple than the producer's first nonzero choice.
            triple = max(combinations(range(8), 3), key=lambda t:C.absolute(C.det([linear[i] for i in t])))
            inv = eliminate([linear[i] for i in triple])
            bounds = []
            for co in inv:
                alpha = [S()]*8
                for i, value in zip(triple, co):
                    alpha[i] = value
                low = min(a/w for a, w in zip(alpha, omega));high = max(a/w for a, w in zip(alpha, omega))
                positive = [a-low*w for a, w in zip(alpha, omega)]
                negative = [high*w-a for a, w in zip(alpha, omega)]
                need(min(positive) >= 0 and min(negative) >= 0,
                     'two nonnegative physical coordinate recovery combinations')
                coordinate = [sum((a*l[k] for a, l in zip(alpha, linear)), S()) for k in range(3)]
                need(coordinate == [S(k == len(bounds)) for k in range(3)], 'literal recovered coordinate')
                bounds.append(max(sum(positive, S()), sum(negative, S())))
            total = sum(bounds, S())
            need(total <= 60, 'independent balanced recovery constant sixty')
            for k, ray in enumerate(map(C.vec, fan['critical_tilt_rays'])):
                other = C.vec(fan['critical_tilt_rays'][1-k])
                inverse = min(1/(-dot(g, ray)) for _, _, g in rows
                              if dot(g, other) == 0 and dot(g, ray) < 0)
                need(inverse <= 80, 'actual complete facet reciprocal eighty')
            records.append({'axis': j, 'fan': number, 'triple': list(triple),
                            'coordinate_bounds': list(map(str, bounds)), 'total': str(total)})
    need(len(records) == 46, 'all closed recovery systems')
    return records


def area_localizer():
    vertices, _ = G.construct()
    _, _, raw, _ = G.facets(vertices)
    directions = {G.axis(G.cross(a, b)) for a, b in combinations(raw, 2)}-{None}
    levels = sorted(set(G.candidate_value(raw, d) for d in directions))
    need(len(directions) == 613 and len(levels) == 104, 'complete credited polar candidates')
    need(levels[0] == G.S(207, 91, 2) and levels[1] == G.S(16727, 7293, 160),
         'exact first and second area levels')
    need(S(levels[1].a, levels[1].b, levels[1].d) > (A0+S(1, 0, 80))**2,
         'strict nonminimum polar gap')
    vectors = [tuple(S(a, b, 800) for a, b in v) for v in raw]
    radii = []
    for j, m in enumerate(C.axes()):
        signed = ZERO
        zeros = []
        for b in vectors:
            value = dot(b, m)
            if value == 0:
                zeros.append(b)
            else:
                signed = add(signed, scale(S(1 if value > 0 else -1, 0, 2), b))
        need(signed == scale(A0, m) and len(zeros) == 12,
             'exact global support drift and zero-dot tangent generators')
        dirs = set()
        for b in zeros:
            d = cross(m, b);pivot = next(x for x in d if x != 0)
            dirs.add(scale(1/pivot, d))
        radius2 = min((sum((C.absolute(dot(b, d)) for b in zeros), S())/2)**2/dot(d, d)
                      for d in dirs)
        wanted = S(1385, 619, 200) if j == 0 else S(65, 29, 10)
        need(radius2 == wanted and radius2 > S(49, 0, 4), 'complete tangent inradius')
        radii.append({'axis':j,'projective_edge_normals':len(dirs),'radius_squared':str(radius2)})
    need(S(14) < A0 < S(29, 0, 2) and S(113, 50) < 225,
         'credited brightness minimum and Lipschitz fifteen bounds')
    need(F(7,2)*F(999,1000)-F(29,2)/40 > 3, 'global chord linearizer')
    return {'polar_candidates':613,'area_levels':104,'next_area_squared':str(S(16727,7293,160)),
            'tangent_disks':radii,'audited_scope':'Only the area-localizer part of 8602; no RID passage-transfer verdict.'}


def rotation_plane_identity():
    Pmod = module('independent_rotation_polynomials', HERE/'../mirror-rigidity-audit/symbolic.py')
    P, symbol = Pmod.P, Pmod.symbol
    x,y,z = [symbol(name) for name in ['px','py','rho']]
    w = [x,y,z]
    skew = [[P(),-z,y],[z,P(),-x],[-y,x,P()]]
    def multiply(a,b):
        return [[sum((v*t for v,t in zip(row,col)),P()) for col in zip(*b)] for row in a]
    square = multiply(skew,skew)
    disp = [[2*(skew[i][j]+square[i][j]) for j in range(3)] for i in range(3)]
    actual = multiply(list(zip(*disp)),disp)
    eta2 = x*x+y*y+z*z
    desired = [[4*(1+eta2)*(P(int(i==j))*eta2-w[i]*w[j]) for j in range(3)] for i in range(3)]
    need(actual == desired, 'generic exact proper-rotation displacement Gram identity')
    bad = [[4*(1+eta2)*(P(int(i==j))*eta2+w[i]*w[j]) for j in range(3)] for i in range(3)]
    need(actual != bad, 'consequential sign damage detected')
    reflection = [[S(1),S(),S()],[S(),S(1),S()],[S(),S(),S(-1)]]
    need(C.det(reflection) == -1
         and C.matvec(reflection,(S(1),S(),S())) == (S(1),S(),S())
         and C.matvec(reflection,(S(),S(1),S())) == (S(),S(1),S())
         and C.matvec(reflection,(S(),S(),S(1))) == (S(),S(),S(-1)),
         'improper motion fixes a plane but moves its normal: properness is essential')
    return {'zero_coefficient_identities':9,'sign_damage_detected':True,
            'improper_plane_counterexample_checked':True,
            'scope':'For proper 3D rotations the full operator displacement equals its restriction norm on any 2D plane; spectral intersection proof in REVIEW.md.'}


def gates(d=F(1,1000000), k=F(1,100000000), radius=F(1,5000000000), sharpened=False):
    a,b,h=1200,961600,2402
    motion, safety = (20,25) if sharpened else (40,50)
    checks = [15*d <= F(1,80), 5*d <= F(1,100), F(45,4)/(1-F(1,10000)) < 12,
              F(1,2)-F(9,4)*d >= F(1,4), 16*59*(5*d)**2 < F(1,2), 1-20*d*d >= F(1,2),
              225000*d+F(27,2) < 20, 40*d < 1, 90*d < F(1,2), motion*d <= 1,
              1/(1-d*d/2) <= 2, (motion+1)*d < F(1,15), 2*motion*d*d < 1,
              motion+2+2*motion*d < (motion+3)*(1-2*motion*d*d), radius <= d, safety*radius <= k,
              k <= F(1,100), 120*k <= F(1,2), a*k*k <= F(1,4), (a+b)*k <= F(1,100),
              (1-(a+b)*k)**2/20-2*b*k*(1+b*k) >= F(1,40), 1-k*k >= F(99,100),
              (2+8*h)*k+(2*h+2*h*h)*k*k < F(1,100), 200*k <= F(1,100), 3*radius <= F(1,80)]
    need(all(checks), 'complete rational domain and error gates')
    return len(checks)


def run():
    inputs = json.loads((HERE/'../mirror-rigidity-audit/inputs.json').read_text())
    weights = json.loads((HERE/'weights.json').read_text())
    physical = C.run(inputs, controls=False)
    expected_base = json.loads((HERE/'../mirror-rigidity-audit/expected.json').read_text())
    expected_base['negative_controls_rejected'] = 0
    need(physical == expected_base, 'entire credited independent support record')
    need(physical['constants']['X'] <= 1 and physical['constants']['Y'] <= 1
         and max(p['winding_inverse'] for p in physical['profiles']) < 100,
         'weighted drift and strict wall-cross bounds')
    vertices = [C.as_fields(v,20) for v in C.construct()[0]]
    profiles = singleton_profiles(vertices, inputs, weights)
    match = correspondence(vertices, inputs, profiles)
    recover = recovery(vertices, inputs)
    rejected = 0
    for d,k,r in [(F(1,1000000),F(1,100),F(1,5000000000)),
                  (F(1,1000000),F(1,100000000),F(1,1000000))]:
        try:gates(d,k,r)
        except ValueError:rejected += 1
        else:raise ValueError('unsafe joint parameter control accepted')
    damaged = copy.deepcopy(weights);damaged[0]['equatorial_weights'][0]=['-1','0']
    try:singleton_profiles(vertices,inputs,damaged)
    except ValueError:rejected += 1
    else:raise ValueError('negative moment weight accepted')
    damaged = copy.deepcopy(inputs);damaged['motions'].pop()
    try:correspondence(vertices,damaged,profiles)
    except ValueError:rejected += 1
    else:raise ValueError('incomplete proper correspondence accepted')
    try:gates(radius=F(1,1000000000),sharpened=True)
    except ValueError:rejected += 1
    else:raise ValueError('unsafe sharpened radius accepted')
    return {'actual_reviewer':'six-reviewer-4','role':'independent mathematical reviewer',
            'singleton_profiles':profiles,'correspondence':match,'recovery':recover,
            'area_localizer':area_localizer(),'rational_gates':gates(),
            'rotation_plane':rotation_plane_identity(),
            'sharpened_rational_gates':gates(radius=F(1,2500000000),sharpened=True),
            'damaged_controls_rejected':rejected,'original_supports_rechecked':physical['all_original_contact_supports'],
            'receiver_radius':'1/5000000000','pose_radius':'1/1000000',
            'sharpened_receiver_radius':'1/2500000000','sharpened_pose_operator_factor':20,
            'scope':'Full 8891 quantitative classification; 8602 area-localizer subclaim only. Existing named-body/minimum catalogue and Cayley identity audits credited.'}


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');args=parser.parse_args()
    out=run()
    if args.emit:print(json.dumps(out,indent=2,sort_keys=True))
    else:
        need(out == json.loads((HERE/'expected.json').read_text()), 'complete independent evidence record')
        print('PASS')

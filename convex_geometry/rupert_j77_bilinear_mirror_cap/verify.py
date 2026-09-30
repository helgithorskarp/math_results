"""Exact finite hypotheses for J77's 1/100000 complete mirror receiving cap.

Author six-rupert-2, researcher. Python3.11+, standard library, Q(sqrt5).
The continuous finite-scale estimates are stated in PROOF.md.
"""
import argparse
import copy
import importlib.util
import json
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

deps = json.loads((HERE / 'dependencies.json').read_text())
require(len(deps) == 1 and deps[0]['source_directory'] ==
        'convex_geometry/rupert_j77_effective_mirror_cap' and
        deps[0]['source_commit'] == 'edef7ccfb5e2b89d9a781aa70ff178d70521490b',
        'one declared exact finite-input parent')
require(set(deps[0]['sha256']) == {'.gitignore', 'README.md', 'PROOF.md',
        'verify.py', 'certificates.json', 'dependencies.json', 'expected.json'},
        'all seven direct input files pinned')
for name, digest in deps[0]['sha256'].items():
    require(sha256((REPO / deps[0]['source_directory'] / name).read_bytes()).hexdigest() == digest,
            'changed direct source input: ' + name)
M = load_module('j77_bilinear_finite_input', REPO / deps[0]['source_directory'] / 'verify.py')
MV = load_module('j77_bilinear_multivariate', HERE / 'multivariate.py')
Q = M.Q
V = M.V
dot, cross, add, sub, scale = M.dot, M.cross, M.add, M.sub, M.scale
pos, nonneg, absq, norm1, enc, decode = M.pos, M.nonneg, M.absq, M.norm1, M.enc, M.decode
CAP = F(1, 100000)
CR = F(1001, 1000)
CL = F(2001, 1000)

def square(x):
    return x * x

def coverage(data):
    require(data['agent'] == 'six-rupert-2' and data['role'] == 'researcher', 'actual author and role')
    require(type(data['receiver_cap_denominator']) is int and data['receiver_cap_denominator'] == 100000,
            'proved physical cap only')
    ids = [r['parent'] for r in data['cases']]
    require(len(ids) == len(set(ids)) == 7 and set(ids) == {21, 23, 28, 30, 31, 32, 33},
            'all seven closed receiving strata')
    for r in data['cases']:
        require(len(r['normal_duals']) == 6 and
                {(d['coordinate'], d['sign']) for d in r['normal_duals']} ==
                {(k, s) for k in range(3) for s in (-1, 1)}, 'both signs of all three common coordinates')
        require(len(r['cone_duals']) == 2 and
                {d['coordinate'] for d in r['cone_duals']} == {0, 1}, 'both negative motion coefficients')

def positive_common(rows, weights, ids, target):
    require(len(ids) == len(set(ids)) == 3 and set(ids) <= set(range(6)), 'distinct common dual basis')
    matrix = [[rows[i][k] for i in ids] for k in range(3)]
    require(M.U.critical.gaussian_determinant(matrix) != 0, 'nonsingular common dual basis')
    values = M.P.solve(matrix, target)
    coefficients = [Q()] * 6
    for i, value in zip(ids, values):
        coefficients[i] = value
    shift = max([Q()] + [-c / w for c, w in zip(coefficients, weights)])
    coefficients = [c + shift * w for c, w in zip(coefficients, weights)]
    for c in coefficients:
        nonneg(c, 'nonnegative critical common dual coefficient')
    require(all(sum((c * row[k] for c, row in zip(coefficients, rows)), Q()) == target[k]
                for k in range(3)), 'all three common-coordinate dual identities')
    return coefficients

def reflection_algebra():
    R = MV.Ring(Q, 7)
    z, one = R.zero, R.one
    r = (z, R.variable(0), R.variable(1))
    w = (R.variable(2), R.variable(3), R.variable(4))
    C = (z, R.variable(5), R.variable(6))
    e = R.vector(M.E)
    w0 = R.cross(e, r)
    D = R.add(one, R.dot(w0, w))
    Nt = tuple(R.add(w0[k], R.neg(w[k]), R.multiply(w[0], r[k])) for k in (1, 2))
    Nx = R.add(w[0], R.dot(r, w))
    N = (Nx,) + Nt
    left = R.add(square_poly(R, D), R.dot(N, N))
    right = R.multiply(R.add(one, R.dot(r, r)), R.add(one, R.dot(w, w)))
    require(left == right, 'universal reflected quaternion norm identity')
    require(R.multiply(w[0], R.add(one, R.dot(r, r))) == R.add(Nx, R.dot(r[1:], Nt)),
            'universal inverse axial reflection identity')
    # Apply the numerator map twice, clearing both denominators.
    DD = R.add(D, R.dot(w0[1:], Nt))
    NNx = R.add(Nx, R.dot(r[1:], Nt))
    NNt = tuple(R.add(R.multiply(w0[k], D), R.neg(Nt[k-1]), R.multiply(Nx, r[k])) for k in (1, 2))
    require(all(R.multiply(DD, w[k]) == ((NNx,) + NNt)[k] for k in range(3)),
            'universal Cayley reflection involution')
    return R, r, w, C, w0, Nt, D

def square_poly(ring, polynomial):
    return ring.multiply(polynomial, polynomial)

def stress_algebra(symbols, contacts, weights, A, B, K):
    R, r, w, C, w0, Nt, D = symbols
    e = R.vector(M.E)
    actual = R.zero
    for weight, (a, b, j) in zip(weights, contacts):
        edge = sub(V[b], V[a])
        h = dot(cross(edge, M.E), V[j])
        v = R.vector(V[j])
        m = R.vector_scale(R.constant(1 / h), R.cross(R.vector(edge), R.vector_add(e, r)))
        f = R.dot(m, R.vector_add(R.cross(w, v), R.cross(w, R.cross(w, v)), C))
        actual = R.add(actual, R.scale(weight, f))
    p, rho, rt, bp = w[1:], w[0], r[1:], R.vector(B)
    leading = R.add(*(R.scale(A[i][j], R.multiply(p[i], Nt[j])) for i in range(2) for j in range(2)))
    formula = R.add(leading,
        R.neg(R.multiply(R.determinant2(p, Nt), R.determinant2(p, bp[1:]))),
        R.multiply(rho, R.add(R.dot(bp, r), R.neg(R.dot(p, rt)),
            R.multiply(R.determinant2(p, rt), R.determinant2(p, bp[1:])))),
        R.neg(R.multiply(square_poly(R, rho), R.add(R.one, R.dot(w0, bp)))),
        R.scale(K, R.dot(w0, C)))
    require(actual == formula, 'full universal weighted original-contact stress identity')
    return {'independent_variables':7, 'nonzero_monomials':len(actual),
            'total_degree':max(map(sum, actual)), 'polynomial_sha256':M.digest(R.terms(actual))}

def quantitative_gates():
    d, cr, cl = CAP, CR, CL
    mu, mr = F(807, 100), F(374, 100)
    numerator = F(3, 2) * mu * 35
    gates = {
      'physical_chord_to_raw_chart':cr * (1 - d*d/2) - 1,
      'receiving_parent_covered':F(1, 4) - 4*d,
      'probe_quadratic_remainder_below_23_10':F(23, 10) - F(9, 4)*(1+6*d),
      'mirror_axis_angle_ratio':1 - square(F(1, 2000)) - square(F(1000, 1001)),
      'reflected_full_angle_below_18_delta':18 - (15 + 2*cr),
      'both_Cayley_norms_below_10_delta':10*(1 - 81*d*d/2) - 9,
      'positive_reflected_denominator':1 - 10*cr*d*d,
      'common_translation_absorption':1 - 9*mu*d,
      'own_C_norm_below_424_delta_eta':424*(1 - 9*mu*d) - numerator,
      'pair_C_norm_below_425_delta_min_eta':425 - 424*(1+100*d*d),
      'own_rho_below_131_delta_eta':131 - mr*(35+6*424*d),
      'pair_rho_below_133_delta_min_eta':133 - (1+10*cr*d*d)*(131+cr),
      'raw_receiver_below_CL_max_Cayley':cl*(1-10*d) - (2+10*cr*d*d)
    }
    for name, gap in gates.items():
        pos(Q(gap), 'strict rational absorption: ' + name)
    return gates

def stratum(case, data, permutation, symbols):
    oldcontacts = case['contacts']
    contacts = [(permutation[b], permutation[a], permutation[j]) for a, b, j in oldcontacts]
    weights = decode(data['input_common_weights'])
    common = case['common_indices']
    require(len(weights) == len(common) == 6, 'all six persistent common contacts')
    ms, gs = [], []
    for a, b, j in contacts:
        edge = sub(V[b], V[a])
        h = dot(cross(edge, M.E), V[j])
        ms.append(scale(1/h, cross(edge, M.E)))
        gs.append(cross(V[j], ms[-1]))
    rows = [[gs[i][0], ms[i][1], ms[i][2]] for i in common]
    require(all(gs[i][1:] == (Q(), Q()) and V[contacts[i][2]][0] == 0 for i in common),
            'critical common sources fixed by the actual body mirror')
    for k in range(3):
        require(sum((w * row[k] for w, row in zip(weights, rows)), Q()) == 0, 'critical common balance')
    normal_records = []
    for d in data['normal_duals']:
        k, sign = d['coordinate'], d['sign']
        cs = positive_common(rows, weights, d['basis'], [Q(sign*int(k==j)) for j in range(3)])
        total = sum(cs, Q())
        upper = Q(F(374,100)) if k == 0 else Q(F(807,100))
        pos(upper-total, 'coordinate common dual weight sum strictly bounded')
        normal_records.append({'coordinate':k, 'sign':sign, 'basis':d['basis'],
                               'weight_sum':total, 'identity_sha256':M.digest(cs)})
    rays = []
    for a in case['extreme_motions']:
        ray = M.rotate(decode(a)[:3])
        rays.append(scale(1/norm1(ray), ray))
    cone_records = []
    hs = [None, None]
    for d in data['cone_duals']:
        k = d['coordinate']
        i = case['facet_rows'][k]
        f = -dot(gs[i], rays[k])
        pos(f, 'positive oriented facet magnitude')
        require(dot(gs[i], rays[1-k]) == 0, 'opposite motion ray lies in the facet')
        cs = positive_common(rows, weights, d['basis'],
                 [-x/f for x in (gs[i][0], ms[i][1], ms[i][2])])
        # Direct check in all five variables (rho,xi0,xi1,Cy,Cz).
        facet = [gs[i][0], dot(gs[i],rays[0]), dot(gs[i],rays[1]), ms[i][1], ms[i][2]]
        fullcommon = [[row[0],Q(),Q(),row[1],row[2]] for row in rows]
        require(all(facet[j]/f + sum((c*row[j] for c,row in zip(cs,fullcommon)),Q()) ==
                    -int(j==k+1) for j in range(5)), 'full five-coordinate negative cone dual')
        total = sum(cs,Q())
        H = d['negative_coefficient_bound']
        require(type(H) is int and H > 0, 'positive printed negative-cone coefficient bound')
        pos(Q(H) - (35*total+39/f+6*425*CAP*(total+1/f)), 'finite-scale negative coefficient bound')
        hs[k] = H
        cone_records.append({'coordinate':k, 'facet_row':i, 'basis':d['basis'],
                  'facet_weight':1/f, 'common_weight_sum':total, 'negative_coefficient_bound':H,
                  'identity_sha256':M.digest([cs,1/f])})
    vv = [V[contacts[i][2]] for i in common]
    mm = [ms[i] for i in common]
    kk = [sub(V[contacts[i][1]],V[contacts[i][0]])[0] /
          dot(cross(sub(V[contacts[i][1]],V[contacts[i][0]]),M.E),V[contacts[i][2]]) for i in common]
    S = [[sum((wt*v[i+1]*m[j+1] for wt,v,m in zip(weights,vv,mm)),Q()) for j in range(2)] for i in range(2)]
    require(S[0][1] == S[1][0] and S[0][0]+S[1][1] == 1, 'critical symmetric stress and trace one')
    A = [[Q(int(i==j))-S[i][j] for j in range(2)] for i in range(2)]
    B = tuple(sum((wt*k*v[j] for wt,k,v in zip(weights,kk,vv)),Q()) for j in range(3))
    K = sum((wt*k for wt,k in zip(weights,kk)),Q())
    corners = [[sum((a[i+1]*A[i][j]*b[j+1] for i in range(2) for j in range(2)),Q())
                for b in rays] for a in rays]
    for row in corners:
        for v in row:
            pos(v, 'pairwise cone-positive common stress including both closed rays')
    beta = min(v for row in corners for v in row)
    N = sum(hs)
    W = sum((h*max(row) for h,row in zip(hs,corners)),Q())
    d = Q(CAP)
    b0 = 1-(133+N)*d
    pos(b0, 'positive coefficient sum lower bound')
    bilinear = beta*square(b0)-4*(1+N*d)*W*d
    pos(bilinear, 'finite bilinear lower bound for both motions')
    B1, K1 = norm1(B), absq(K)
    up, low = 1+10*CR*d*d, 1-10*CR*d*d
    error = (up*10*d*B1 + 133*CR*CL*B1*d + 133*CR*d*d +
        133*CR*B1*10*d*d*d + 133*133*d*d*(1+CR*B1*d) + 425*CR*CL*K1*d)
    gap = low*bilinear-error
    pos(gap, 'strict complete-cap bilinear contradiction')
    algebra = stress_algebra(symbols, [contacts[i] for i in common], weights, A, B, K)
    return {'parent':case['parent'], 'normal_duals':normal_records, 'negative_cone_duals':cone_records,
            'stress_S':S, 'stress_A':A, 'stress_B':B, 'stress_K':K, 'bilinear_corners':corners,
            'bilinear_corner_minimum':beta, 'B_l1':B1, 'K_absolute':K1,
            'negative_coefficient_sum_bound':N, 'bilinear_error_weight':W,
            'finite_bilinear_lower_bound':bilinear, 'finite_stress_error_bound':error,
            'final_strict_gap':gap, 'universal_original_contact_algebra':algebra}

def malformed(data, old, permutation, symbols):
    attempts = []
    d = copy.deepcopy(data); d['cases'].pop(); attempts.append(lambda d=d:coverage(d))
    d = copy.deepcopy(data); d['receiver_cap_denominator']=10000; attempts.append(lambda d=d:coverage(d))
    d = copy.deepcopy(data); d['cases'][0]['normal_duals'].pop(); attempts.append(lambda d=d:coverage(d))
    d = copy.deepcopy(data['cases'][0]); d['normal_duals'][0]['basis']=[0,0,1]
    attempts.append(lambda d=d:stratum(old[d['parent']],d,permutation,symbols))
    d = copy.deepcopy(data['cases'][0]); d['cone_duals'][0]['negative_coefficient_bound']=1
    attempts.append(lambda d=d:stratum(old[d['parent']],d,permutation,symbols))
    for fail in attempts:
        try:
            fail()
        except (ValueError,KeyError,IndexError,TypeError,ZeroDivisionError):
            continue
        raise ValueError('malformed critical mathematical data accepted')
    return len(attempts)

def check(self_test):
    inherited = M.check(True)
    b = (json.dumps(inherited,indent=1)+'\n').encode()
    require(b == (REPO/deps[0]['source_directory']/'expected.json').read_bytes(),
            'EVERY complete finite-parent expected byte')
    old = json.loads((REPO/'convex_geometry/rupert_j77_uniform_local_exclusion/certificates.json').read_text())
    old = {c['parent']:c for c in old['cases']}
    source = json.loads((REPO/deps[0]['source_directory']/'certificates.json').read_text())
    source = {c['parent']:c for c in source['cases']}
    index = {v:i for i,v in enumerate(V)}
    permutation = [index[M.rotate(v)] for v in V]
    data = json.loads((HERE/'certificates.json').read_text()); coverage(data)
    for case in data['cases']:
        require(case['input_common_weights'] == source[case['parent']]['common_weights'], 'identical replayed contact weights')
    symbols = reflection_algebra()
    rational = quantitative_gates()
    records = [stratum(old[c['parent']],c,permutation,symbols) for c in data['cases']]
    bad = malformed(data,old,permutation,symbols) if self_test else 0
    for pair, sign in tuple(M.area.SIGNS.items()):
        require(M.area.interval_sign(pair) == sign, 'independent rational sqrt5 sign enclosure')
    return enc({'agent':'six-rupert-2', 'role':'researcher',
        'proof_status':'author-checked finite hypotheses and universal identities plus written continuous proof; unformalized',
        'target':'J77 paragyrate diminished rhombicosidodecahedron', 'global_Rupert_resolved':False,
        'independent_review_asserted':False, 'original_vertices':55,
        'complete_original_source_cap':'dist(n,{+/-R^j e})<=1/100000; original proper Q, all translations,lambda>=1',
        'closed_classification_up_to_actual_right_body_gauge':'lambda1,t0,Qh=I or M_n M_p',
        'larger_1_1000_cap_excluded':False, 'strict_passage_excluded_on_stated_cap':True,
        'closed_strata':len(records), 'nonnegative_common_coordinate_duals':42, 'negative_motion_coefficient_duals':14,
        'pairwise_positive_bilinear_corners':28, 'universal_contact_polynomial_identities':7,
        'universal_reflected_Cayley_identities':3, 'new_numeric_gates':rational, 'stratum_records':records,
        'malformed_controls_with_self_test':bad, 'fixture_sha256':M.digest(data),
        'whole_finite_parent_expected_bytes':len(b), 'whole_finite_parent_expected_sha256':sha256(b).hexdigest(),
        'direct_pinned_input_files':7, 'transitive_pinned_input_files':49,
        'distinct_independent_sign_enclosures_including_parents':len(M.area.SIGNS),
        'failed_larger_candidate':'1/90000 fails these conservative final gates in parents30/31; no nonexistence or passage conclusion'})

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    out=(json.dumps(check(args.self_test),indent=1)+'\n').encode()
    require(out==(HERE/'expected.json').read_bytes(), 'EVERY expected output byte; invoke with --self-test')
    print(out.decode(),end='')
